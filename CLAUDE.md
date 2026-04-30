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
- **Conversational language follows the user; tip content is ES or EN only.**
  If a user works in Italian, the surface and prompts are in Italian; the tip
  content is served in EN. Technical terms (hooks, skills, MCP, subagents,
  plugins) stay in English regardless.

## Related repos

- `juanwmedia/ai-infra` — hosts `/claude-code-tip` (publish flow, source of
  manifest updates) and `/share` consumer side.
- `juanwmedia/wmedia.es` — Laravel app that hosts the tips and the MCP server.
