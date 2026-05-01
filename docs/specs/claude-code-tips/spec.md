---
title: "Claude Code Tips Plugin"
status: approved
spec_version: 2
created: 2026-04-28
last_updated: 2026-05-01
---

# Claude Code Tips Plugin

## Overview

A Claude Code plugin that brings the Claude Code tips published at
wmedia.es into the session. Two surfaces:

- **Discovery** — when the user is working on a topic a tip covers, the
  plugin surfaces it briefly (id, topic, one-line summary) and tells the user
  how to open it.
- **Contribution** — when the user has discovered a useful pattern, they can
  run `/cc-tips:share` to draft a contribution as a GitHub issue.
  The maintainer curates issues and promotes selected ones into published tips.

The plugin ships as a public GitHub repo with a bundled manifest. Tip
markdowns are fetched on demand from the same repo via `curl` and cached
locally per-user. Every `/claude-code-tip` publish in `ai-infra` auto-appends
the new tip to this plugin's manifest and pushes the markdown to this repo,
so users stay current without plugin version bumps.

## User Stories

1. As a Claude Code user, I want relevant tips to appear contextually as I
   work, so I learn the tool through use rather than seeking content.
2. As a Claude Code user, I want tips I've already opened never to be
   re-surfaced, so I never see the same content twice unless I ask for it.
3. As a Claude Code user, I want to browse all available tips (with optional
   filtering by topic), so I can explore intentionally.
4. As a Claude Code user, I want to open a specific tip by its short numeric
   id, so I don't type long slugs.
5. As a Claude Code user, I want to contribute a tip I've discovered via a
   low-friction flow that doesn't require a pull request, so my insight reaches
   the maintainer without me opening a fork.
6. As a Claude Code user working in a language other than Spanish or English,
   I want the conversational layer in my language even though tip content is
   only ES or EN.
7. As a first-time user, I want a welcome message the moment I start Claude
   Code after installing the plugin, so I learn what the plugin does without
   waiting for a contextual match. I also want a way to see it again later.
8. As a Claude Code user, I want to be reminded periodically that I should
   keep the plugin updated, so I don't miss new tips.
9. As the plugin maintainer, I want new tips I publish to reach plugin users
   automatically through manifest sync, so the plugin stays current without
   plugin version bumps.

## Acceptance Criteria

### Discovery

1. GIVEN the user is working on a topic that an unread tip covers, WHEN the
   skill detects the topic match, THEN it surfaces one tip (the most
   relevant) with its id, topic, one-line summary, and the command to open
   it (`/cc-tips:open <N>`).
2. GIVEN a tip on topic T has already been surfaced organically in the
   current session, WHEN further matches on topic T occur in the same session,
   THEN no new organic surface is emitted for T. Different topics each get
   their own once-per-session trigger.
3. GIVEN no unread tips match the current context, WHEN matches are evaluated,
   THEN no organic surface is emitted.

### Read marker

4. GIVEN the user runs `/cc-tips:open <N>`, WHEN tip N exists in the
   manifest, THEN the tip's markdown is fetched (cache or curl), rendered in
   the response, and N is appended to `read_tips` in `progress.json`.
5. GIVEN tip N is in `read_tips`, WHEN the skill evaluates organic surface
   candidates, THEN tip N is permanently excluded.

### Listing

6. GIVEN the user runs `/cc-tips:list`, WHEN invoked with no
   argument, THEN all tips are listed grouped by topic with their id, title in
   the user's language, and a marker indicating read or unread. The output
   ends with a one-line reminder to keep the plugin updated.
7. GIVEN the user runs `/cc-tips:list <topic>`, WHEN the topic value
   matches a known topic from the hub taxonomy, THEN only tips in that topic
   are listed (with the same update reminder); if it doesn't match, an error
   lists the valid topics.

### Open

8. GIVEN tip N is in the manifest, WHEN the user runs
   `/cc-tips:open <N>` and the cached file matches the manifest's
   version, THEN the cache is read; if the cache is missing or version
   mismatches, `curl` fetches from `raw.githubusercontent.com` and saves to
   `${CLAUDE_PLUGIN_DATA}/tips/<slug>-<lang>-v<N>.md`. If the manifest entry
   has `contributed_by_github_username`, an attribution line ("Contributed by
   @username", with a link to the user's GitHub profile) is appended after
   the tip content. The rendered output ends with a one-line reminder to
   keep the plugin updated.
9. GIVEN the network or the GitHub raw URL is unavailable, WHEN the curl
   fails, THEN the user receives an error explaining the cause and suggesting
   retry; `read_tips` is not modified.
10. GIVEN tip N is not in the manifest, WHEN the user runs `/open <N>`, THEN
    the user receives "Tip N not found. Run `/cc-tips:list` to see
    available tips."

### Share

11. GIVEN the user runs `/cc-tips:share`, WHEN the skill activates,
    THEN it drafts an issue from recent conversation context (proposed title,
    body, suggested topic), presents it to the user for review, and on
    approval: tries `gh issue create --repo juanwmedia/cc-tips
    --title "..." --body "..." --label contribution`. If `gh` is missing or
    unauthenticated, it falls back to opening
    `https://github.com/juanwmedia/cc-tips/issues/new?title=...&body=...&labels=contribution`
    in the user's browser. The contributor's GitHub username (from
    `gh api user --jq .login` when available) is included in the issue body.

### Language fallback

12. GIVEN the user's recent prompts are in Spanish, WHEN the plugin surfaces
    or responds, THEN the conversational layer is in Spanish and tip content
    is served from the curated `<slug>-es-v<version>.md` cache (fetched from
    `url_es` on cache miss).
13. GIVEN the user's recent prompts are in English, WHEN the plugin surfaces
    or responds, THEN the conversational layer is in English and tip content
    is served from the curated `<slug>-en-v<version>.md` cache (fetched from
    `url_en` on cache miss).
13b. GIVEN the user's recent prompts are in any language other than Spanish
    or English (Italian, French, Portuguese, German, …), WHEN the plugin
    surfaces or responds, THEN the conversational layer is in that language;
    when `/cc-tips:open <N>` runs, the EN source is fetched, the open skill
    translates it on the fly preserving code blocks and technical terms in
    English, and the translation is cached at `<slug>-<lang>-v<version>.md`.
    Subsequent opens of the same tip in the same language hit the cache.
    Technical terms (hooks, skills, MCP, subagents, plugins, Claude Code) and
    slash command names remain in English regardless of working language.

### Welcome

14. GIVEN the SessionStart hook runs and the flag file
    `${CLAUDE_PLUGIN_DATA}/first_seen` does not exist, WHEN the user starts
    a Claude Code session, THEN before any other plugin output the welcome
    message is presented. It lists `/cc-tips:list`,
    `/cc-tips:open <N>`, `/cc-tips:share`, briefly describes
    the contextual recommendations behavior, and ends with "You won't see this
    auto-message again." After presentation, the flag file is created so
    subsequent sessions do not show it again.
15. GIVEN the user runs `/cc-tips:welcome`, WHEN invoked, THEN the
    welcome message is presented regardless of `first_seen_at`.

### Auto-publish (touches `/claude-code-tip` in `ai-infra`)

16. GIVEN the user (the maintainer) runs `/claude-code-tip` and the wmedia.es
    publish succeeds, WHEN the existing flow finishes, THEN a final step
    transforms the tip's markdown for terminal rendering (strips image tags,
    HTML, anything not renderable in plain terminal output), writes it to
    `~/code/cc-tips/tips/<slug>-{es,en}.md`, appends a manifest
    entry with the next stable id, commits, and pushes to
    `juanwmedia/cc-tips`.
17. GIVEN the auto-publish step fails (network, conflict, auth), WHEN the
    underlying wmedia.es publish has succeeded, THEN the user is informed and
    given manual recovery steps; the wmedia.es publish is NOT rolled back.

## Manifest schema (informative)

```json
{
  "version": "1.0.0",
  "tips": [
    {
      "id": 1,
      "slug": "claude-code-checkpoints",
      "topic": "sessions",
      "version": 1,
      "title_es": "...", "title_en": "...",
      "summary_es": "...", "summary_en": "...",
      "url_es": "https://raw.githubusercontent.com/juanwmedia/cc-tips/main/tips/claude-code-checkpoints-es.md",
      "url_en": "https://raw.githubusercontent.com/juanwmedia/cc-tips/main/tips/claude-code-checkpoints-en.md",
      "contributed_by_github_username": null
    }
  ]
}
```

Topics are the 11 from wmedia's `HubTopic` enum: `skills`, `mcp`, `hooks`,
`subagents`, `plugins`, `memory-context`, `models-cost`, `permissions`,
`sessions`, `autonomous`, `fundamentals`.

## ID stability

IDs are assigned sequentially at first publish (next = max + 1) and never
recycled. Retired tips leave gaps in the numbering.

## Out of Scope

- Public attribution on wmedia.es (no schema change in the wmedia.es app).
- A `--from-issue` flag on `/claude-code-tip` to convert GitHub issues into
  tips (deferred to a follow-up feature).
- Curated tip authorings beyond Spanish and English (other languages are
  served via on-the-fly LLM translation from the English source, cached).
- Active rate limiting beyond the per-topic-per-session organic surface cap.
- Editing or deleting a published tip via the plugin (handled at wmedia.es
  side and propagated through manifest version bumps).
- Pull-request-based contributions (issue is the only contribution shape in v1).
- A `/cc-tips:apply <N>` skill that contextualizes a tip to the current
  session (deferred to v2; tracked in the post-v1 issue queue).

## Open Questions

None.
