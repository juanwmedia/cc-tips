# Claude Code Tips

A Claude Code plugin that surfaces wmedia.es Claude Code tips inside the
session, contextually. When a user is working on a topic a tip covers, Claude
mentions it. Users can also contribute new tips via `/share`, which opens a
pre-filled GitHub issue against this repo.

## Why this exists

Tips published at https://wmedia.es/es/claude-code are valuable, but they live
outside the session — users only find them by visiting the site. This plugin
brings them in, contextually, where they are most useful. The contribution
loop is asymmetric: anyone can `/share` (low friction, an issue, not a PR),
only the maintainer promotes selected issues to tips via
`/claude-code-tip --from-issue` in the `ai-infra` repo.

## Decisions worth knowing

- **One skill, not many.** Skill descriptions are permanently loaded into
  context; the budget is finite (1,536 chars/skill, ~8k chars total).
- **Manifest bundled, markdowns on demand.** `manifest.json` ships in the
  plugin; tip markdowns are fetched from raw.githubusercontent.com via `curl`
  and cached versioned in `${CLAUDE_PLUGIN_DATA}/tips/<slug>-<lang>-v<N>.md`.
  This keeps the plugin repo lean and lets tips update without bumping the
  plugin version.
- **Plugin-only attribution at this stage.** No schema change in wmedia.es.
  Contributor GitHub usernames live in the manifest.
- **Auto-publish.** Every `/claude-code-tip` publish in `ai-infra` updates
  this plugin's manifest and pushes the tip markdown to this repo.
- **Conversational language follows the user.** Welcome, topic-awareness
  mentions, and command UI render in the user's working language; translate
  from the English source naturally.
- **Tip content has two curated authorings (Spanish and English) plus
  on-the-fly translation for everything else.** Spanish users see curated
  Spanish; English users see curated English; users in any other language
  (Italian, French, Portuguese, German, …) get the EN source translated by
  `/cc-tips:open` (Haiku) and cached locally at
  `<slug>-<lang>-v<version>.md`, so subsequent reads are instant. Technical
  terms (hooks, skills, MCP, subagents, plugins, Claude Code) stay in
  English regardless.
- **Hook is plain stdout, not JSON.** `welcome.sh` cats text fragments
  (`language-rule.md`, `welcome-msg.md`, `topic-awareness.md`) and
  runtime-derives the topic list from `manifest.json` via `jq`.
- **JSON parsing via `jq` everywhere.** Skills (`list`, `open`) and the hook
  use `jq` to filter the manifest and update `progress.json`. The cost
  gradient vs Read-tool is ~250× per call (25 K tokens vs ~100 tokens), so
  fighting `jq` was costing real money and context. Runtime deps are
  `bash`, `curl`, `jq`. No Python, no Node.
- **Manifest schema is lean (v1.2.0).** Per entry: `id`, `slug`, `topic`,
  `version`, `title_es`, `title_en`, `url_es`, `url_en`,
  `contributed_by_github_username`. Earlier versions also carried
  `slug_es`, `slug_en`, `summary_*`, `external_url_*` — all dropped as
  unused. If you ever need them again, restore them; nothing in the auto-
  publish flow assumes they're absent.

## Versioning discipline (READ BEFORE COMMITTING)

The plugin's version lives in `plugin/.claude-plugin/plugin.json`. Per Claude
Code: _"If `version` is set, users only receive updates when you bump it."_
Without a bump, `/plugin marketplace update juanwmedia-cc-tips` will NOT pull
your change for installed users — they will keep running the previous version.

**Bump on every commit that touches any of**:
- `plugin/skills/**` (any SKILL.md change, including footer/copy edits)
- `plugin/hooks/**` (any hook script or `.md` payload change)
- `plugin/manifest.json` (new tip, new field, schema change)
- `plugin/.claude-plugin/plugin.json` itself
- `tips/**` IS NOT bundled (post-restructure), so tip-content fixes do NOT
  require a version bump. Users get them on next `/cc-tips:open` via curl.

**Semver guidance**:
- Patch (`1.x.Y`): bug fix, copy fix, doc tweak inside a skill body, **new
  tip added to the manifest** (content addition, not a feature).
- Minor (`1.X.0`): new feature, new skill, new hook, behaviour change that
  is backwards-compatible for existing users.
- Major (`X.0.0`): breaking change in install layout, manifest schema, or
  user-facing command surface.

**Auto-publish (`/claude-code-tip` Step 11) must also bump.** When that flow
adds a new entry to `manifest.json`, it should also bump the **patch**
version of `plugin/.claude-plugin/plugin.json` and include the bump in the
same commit.

## GitHub Releases policy

GitHub Releases are **not** the install mechanism — `/plugin marketplace
update` reads `plugin/.claude-plugin/plugin.json` from `main`, not release
artifacts. Releases here exist purely as a curated changelog for users who
want to follow the project.

**Cut a release for every MINOR and MAJOR. Skip PATCHES.** A new tip is a
patch and should not produce its own release; that would be release noise.
Patches accumulate in the next minor's notes.

```bash
gh release create vX.Y.Z --title "vX.Y.Z — <one-line summary>" \
  --notes "..." --target <commit-sha>
```

The notes should group changes by section (Features / Skills / Hooks /
Schema / Tips since previous minor) and link to the commit range.

## Related repos

- `juanwmedia/ai-infra` — hosts `/claude-code-tip` (publish flow, source of
  manifest updates) and `/share` consumer side.
- `juanwmedia/wmedia.es` — Laravel app that hosts the tips and the MCP server.
