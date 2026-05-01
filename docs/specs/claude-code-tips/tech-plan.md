---
title: "Claude Code Tips Plugin — Technical Plan"
status: approved
based_on_spec_version: 1
created: 2026-04-28
last_updated: 2026-04-28
---

# Claude Code Tips Plugin — Technical Plan

## Context

Spec at `docs/specs/cc-tips/spec.md` is approved (17 ACs). Greenfield build: only `CLAUDE.md` + `docs/specs/` exist in the project dir. This plan creates the entire plugin: 5 skills (one auto-invocable + four user-only), 1 SessionStart hook, the bundled tip manifest, and the initial port of 55 paired tips from `~/.claude/skills/claude-code-tip/examples/`. Also wires a new Step 11 into the existing `/claude-code-tip` skill so future publishes auto-update the plugin manifest.

Repo creation on GitHub (`gh repo create juanwmedia/cc-tips --public`) and the first push happen during `/close`, not /build.

## Findings from exploration

### Tip corpus
- 110 markdown files = **55 complete pairs**, 0 singletons, 0 anomalies. (Initial agent report claimed 26 singletons because it paired by slug; slugs intentionally differ between ES and EN per `/claude-code-tip` skill rules. Pairing by frontmatter `(title_es, title_en)` is the correct key, verified by direct inspection: 55 pairs, all clean.)
- Frontmatter: 4 fields (`date`, `type`, `title_es`, `title_en`). Each file carries BOTH titles (so pairing by frontmatter works regardless of which language version you're holding). **No topic field.** Topic lives in wmedia.es DB at `tips.hub_topic`.
- Image patterns: only markdown `![alt](https://wmedia.es/storage/writing/<hash>.svg)`. One Mermaid block found. No HTML `<img>` or embedded `<svg>`.

### `/claude-code-tip` publish skill
- Step 10 is the final step today: `git -C ~/code/ai-infra add -A && commit && push`.
- `allowed-tools` already includes `Bash(git *)` — no new patterns needed.
- Insertion point for auto-publish: new Step 11, runs always after Step 10 (not opt-in, per AC-16).

### Reference plugin patterns
- `plugin.json` minimal in observed plugins: name, description, author. We add `version` since the documented schema supports it and we need it for cache-keying updates.
- Hooks: separate script files in `hooks/`, referenced from `hooks.json` via `${CLAUDE_PLUGIN_ROOT}/hooks/<script>.sh`.
- `disable-model-invocation: true` is documented but not seen in observed plugins. We use it deliberately to keep the always-loaded description budget cost equal to ONE skill (not five).

## Design Decisions

### D1: manifest.json at plugin root
Shared across 4 skills (main, list, open, share). Plugin-root path `${CLAUDE_PLUGIN_ROOT}/manifest.json` is uniform across skills. Diverges from observed pattern (data inside skill subdirs) — justified by cross-skill shared access.

### D2: Content transformation — LLM-driven, not regex
Tip content is transformed for terminal rendering by an LLM applying judgment per tip, not by regex/static rules. Rationale: the corpus is varied (code blocks, tables, mermaid, callouts, the occasional embedded HTML, prose density variation) and a regex pipeline produces poor edge cases. Token cost is acceptable for a one-time port of 55 tips.

**Working rules the LLM follows** (guidance, not enforcement):
- **Drop**: image references that won't render in terminal (markdown `![](https://...svg)`, any `<img>`, embedded `<svg>` blocks).
- **Replace mermaid blocks**: conditional on the tip's manifest entry.
  - If the tip has `external_url_<lang>` populated → `[Diagram available online: <external_url>]`.
  - If not (plugin-only tip without external publication) → `[Diagram not available in terminal output]`.
- **Keep**: code blocks, tables, lists, headers, blockquotes (TL;DR callout), inline links `[text](url)`, strikethrough, horizontal rules. The body's information density.
- **Judge**: any borderline content (HTML snippets, ASCII art) — keep if it renders cleanly in a terminal, drop or replace otherwise.

**Implementation**:
- For initial port: spawn worker subagents (`general-purpose`, sonnet) in batches of ~10 paired tips. Each worker reads its batch, transforms with judgment, writes cleaned versions to `tips/<slug>-{es,en}.md`. Returns: list of files written + any concerns.
- For ongoing auto-publish (Step 11 in `/claude-code-tip`): the skill body instructs Claude to do the same per-tip transformation with judgment. No script.

No regex pipeline anywhere.

### D3: Topic enrichment for initial port
Tip frontmatter has no topic. The port script queries the wmedia.es production SQLite DB once via SSH for `(slug_en, slug_es, hub_topic)` of all paired tips, builds a lookup, enriches each manifest entry. Tips with `hub_topic IS NULL` in the DB default to `fundamentals` and are listed in `port-untagged.txt` for manual classification later.

### D4: Initial seed = 55 complete pairs
All 55 paired tips ship in v1. No singletons exist (verified). No skipping logic needed.

### D5: Stable id assignment
Sort 55 paired tips by frontmatter `date` ascending (oldest first). Assign id 1..55 in that order. Post-v1, ids are immutable; auto-publish uses max+1.

### D6: SessionStart welcome hook — bash
`hooks/welcome.sh` reads/creates `${CLAUDE_PLUGIN_DATA}/progress.json`. If `first_seen_at` is null:
- Emits JSON `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}` with the welcome message embedded as instruction to Claude.
- Atomically sets `first_seen_at` (tmpfile + mv) so subsequent sessions emit nothing.

Welcome content in English (no language signal at session start).

### D7: 5-skill structure with `disable-model-invocation: true`
Skills under `skills/`, plugin-namespaced as `/cc-tips:<name>`:
- `cc-tips` (auto-invocable, default frontmatter) — main discovery + read marker logic. Description ~118 chars.
- `list` (`disable-model-invocation: true`) — listing
- `open` (`disable-model-invocation: true`) — open by id
- `share` (`disable-model-invocation: true`) — contribute via gh / web URL
- `welcome` (`disable-model-invocation: true`) — re-trigger welcome

Description budget cost ≈ one skill, not five.

### D8: Auto-publish step in `/claude-code-tip` (new Step 11)
Sequence after Step 10 succeeds (Claude executes with judgment per tip — no script):
1. Read both `examples/<slug>-{es,en}.md` (the source markdown that was just published to wmedia.es).
2. Transform each language's content for terminal rendering per D2 working rules (LLM judgment — drop image refs, replace mermaid blocks, keep code/tables/lists/etc.).
3. Write the cleaned versions to `~/code/cc-tips/tips/<slug>-{es,en}.md`.
4. Read `~/code/cc-tips/manifest.json`, find max id. Append a new entry with `id=max+1`, slug, topic (from the wmedia DB record fetched in earlier publish steps), `version=1`, titles, summaries (use the tip's TL;DR or generate a one-liner), all four URL fields per D9, `contributed_by_github_username: null`. Write manifest back.
5. `git -C ~/code/cc-tips add -A && git commit -m "Add tip: <slug>" && git push`.

On failure (network/conflict/auth): per AC-17, inform user with manual recovery steps; do NOT roll back wmedia.

### D9: Manifest supports plugin-only tips (no external URL) [Clarified during build]
The spec's manifest example only shows `url_es` / `url_en` (the raw GitHub markdown URLs, always present). It doesn't account for tips that exist on wmedia.es. In v1 all 55 ported tips are wmedia-published, so every entry has a wmedia URL. But future contribution flows might add tips to the plugin without publishing to wmedia. The manifest must support this from day one to avoid a schema migration later.

Manifest entry — final field set:
```json
{
  "id": 1,
  "slug": "claude-code-checkpoints",
  "topic": "sessions",
  "version": 1,
  "title_es": "...", "title_en": "...",
  "summary_es": "...", "summary_en": "...",
  "url_es": "https://raw.githubusercontent.com/juanwmedia/cc-tips/main/tips/<slug-es>.md",
  "url_en": "https://raw.githubusercontent.com/juanwmedia/cc-tips/main/tips/<slug-en>.md",
  "external_url_es": "https://wmedia.es/es/tips/<slug-es>",
  "external_url_en": "https://wmedia.es/en/tips/<slug-en>",
  "contributed_by_github_username": null
}
```

`external_url_es` and `external_url_en` are nullable. All 55 v1-port entries will have them populated. Step 11 (auto-publish) populates them. Future plugin-only paths may leave them null.

This is a forward-compatible field addition not present in the spec. To be reconciled in `/close`.

## Tasks

### Batch 1: plugin scaffold (parallel, mechanical — haiku)
- [ ] **T1**: Create `.claude-plugin/plugin.json` with name, description (~118 chars), version `1.0.0`, author.
  - **File**: `~/code/cc-tips/.claude-plugin/plugin.json`
  - **Covers**: foundational
- [ ] **T2**: Create top-level `README.md` (public-facing usage doc).
  - **File**: `~/code/cc-tips/README.md`
  - **Covers**: foundational
- [ ] **T3**: Create `LICENSE` (MIT).
  - **File**: `~/code/cc-tips/LICENSE`
  - **Covers**: foundational
- [ ] **T4**: Create `.gitignore` (ignore local cache, OS detritus).
  - **File**: `~/code/cc-tips/.gitignore`
  - **Covers**: foundational

### Batch 2: skills (parallel — sonnet)
- [ ] **T5**: Write `skills/cc-tips/SKILL.md` (auto-invocable). Description ~118 chars. Body: organic surface logic, daily cap, read-marker check, language detection, attribution rendering reference.
  - **File**: `~/code/cc-tips/skills/cc-tips/SKILL.md`
  - **Covers**: AC-1, AC-2, AC-3, AC-5, AC-12, AC-13
- [ ] **T6**: Write `skills/list/SKILL.md` with `disable-model-invocation: true`. Body: render manifest as table grouped by topic, mark read/unread, optional topic filter, update reminder footer.
  - **File**: `~/code/cc-tips/skills/list/SKILL.md`
  - **Covers**: AC-6, AC-7
- [ ] **T7**: Write `skills/open/SKILL.md` with `disable-model-invocation: true`. Body: cache check, curl fetch on miss/version-mismatch, attribution line if present, update reminder footer, error handling.
  - **File**: `~/code/cc-tips/skills/open/SKILL.md`
  - **Covers**: AC-4, AC-8, AC-9, AC-10
- [ ] **T8**: Write `skills/share/SKILL.md` with `disable-model-invocation: true`. Body: draft from context, `gh issue create` primary, web URL fallback, contributor username from `gh api user --jq .login` when available.
  - **File**: `~/code/cc-tips/skills/share/SKILL.md`
  - **Covers**: AC-11
- [ ] **T9**: Write `skills/welcome/SKILL.md` with `disable-model-invocation: true`. Body: emit welcome message regardless of `first_seen_at`.
  - **File**: `~/code/cc-tips/skills/welcome/SKILL.md`
  - **Covers**: AC-15

### Batch 3: hooks (sequential within batch, parallel with batch 2 — haiku)
- [ ] **T10**: Write `hooks/welcome.sh` per D6 (reads/creates progress.json, emits welcome additionalContext if first_seen_at null, atomically sets first_seen_at).
  - **File**: `~/code/cc-tips/hooks/welcome.sh`
  - **Covers**: AC-14
- [ ] **T11**: Write `hooks/hooks.json` (SessionStart event runs `bash "${CLAUDE_PLUGIN_ROOT}/hooks/welcome.sh"`).
  - **File**: `~/code/cc-tips/hooks/hooks.json`
  - **Covers**: AC-14
- [ ] **T12**: `chmod +x hooks/welcome.sh`.
  - **Covers**: AC-14

### Batch 4: port orchestration script (sonnet)
- [ ] **T13**: Write `scripts/port-corpus.py`. Mechanical only — pairs files by frontmatter `(title_es, title_en)`, runs ONE `ssh forge@frontendleap.com "sqlite3 ... 'SELECT slug_en, slug_es, hub_topic FROM tips'"` to fetch topic mapping, writes `pair-index.json` (the input fed to workers) and later `manifest.json` (the output assembled from cleaned files). NO content transformation in this script.
  - **File**: `~/code/cc-tips/scripts/port-corpus.py`
  - **Covers**: build-time orchestration

### Batch 5: initial port — content transformation by LLM workers (sequential after batch 4)
- [ ] **T14**: Run `python3 scripts/port-corpus.py --pair` to produce `~/code/cc-tips/.port/pair-index.json` (the 55 pairs with source paths + DB topic for each).
  - **Output**: `.port/pair-index.json`
  - **Covers**: data prep
- [ ] **T15**: Spawn 6 worker subagents (general-purpose, sonnet) in parallel. Each gets ~9-10 pairs from `pair-index.json` and produces cleaned `~/code/cc-tips/tips/<slug>-{es,en}.md` per pair. Workers apply the D2 working rules with judgment. Each returns: list of files written + concerns.
  - **Output**: `~/code/cc-tips/tips/*.md` (110 files, two per pair)
  - **Covers**: AC-1, AC-6, AC-7, AC-8 (initial content)
- [ ] **T16**: Run `python3 scripts/port-corpus.py --manifest` to assemble `manifest.json` by reading frontmatter + content from the cleaned files in `tips/`, joining with topic data, assigning ids 1..55 by date order.
  - **Output**: `~/code/cc-tips/manifest.json`
  - **Covers**: AC-1 (manifest readiness)
- [ ] **T17**: Verify port: 55 entries in manifest, every entry has both `tips/<slug>-es.md` and `tips/<slug>-en.md` on disk, every entry's topic is a valid HubTopic value.
  - **Covers**: validation

### Batch 6: auto-publish wiring (sonnet)
- [ ] **T18**: Add Step 11 to `~/.claude/skills/claude-code-tip/SKILL.md` per D8.
  - **File**: `~/.claude/skills/claude-code-tip/SKILL.md`
  - **Covers**: AC-16, AC-17

### Batch 7: local validation
- [ ] **T19**: Run `claude --plugin-dir ~/code/cc-tips`. Smoke test: welcome appears in fresh session; `/cc-tips:list` returns table; `/cc-tips:open 1` fetches+caches+displays; `/cc-tips:welcome` re-triggers welcome.
  - **Covers**: integration smoke test for AC-1 through AC-15

## Cross-Feature Discoveries
(empty)

## Iteration Log

### B2 — 2026-04-30 — Auto-invocable skill replaced by SessionStart hook
- **Removed**: `skills/cc-tips/` entirely. The auto-invocable skill body had been doing 3 visible tool calls (Read manifest, Read progress, Bash state update) every time it activated — 3–4s latency for what should be a one-line inline mention. The skill abstraction was being misused: the only durable value was the description-loaded-into-context side effect; the body itself was misaligned with the actual UX goal.
- **Replaced by**: hook `hooks/welcome.sh` extended to always emit topic-awareness `additionalContext`, plus the welcome message on first session (gated by `first_seen_at`). Constructed via `python3` heredoc for bulletproof JSON escaping.
- **Durability**: confirmed via doc that SessionStart hooks re-fire after auto-compaction (`source: "compact"`), so topic awareness survives session compaction equally well to a skill description.
- **State**: `last_organic_surface_at` is no longer tracked. Daily cap is now an instruction in the hook's text ("at most once per session") rather than enforced state. Trade-off accepted: we trust the model to self-regulate one inline mention per session.
- **Outcome**: plugin reduced to 4 skills (list, open, share, welcome) + 1 hook. Zero tool calls visible when the model surfaces a tip mention inline.
- **AC coverage**: AC-1 (organic mention) now fulfilled by the hook-injected instruction; AC-2 (daily cap) becomes conversational not state-based; AC-5 (excluded after open) still enforced via `read_tips` in `/cc-tips:open`. All other ACs unchanged.
