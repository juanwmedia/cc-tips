# Claude Code Tips

A Claude Code plugin that surfaces tips published at [wmedia.es/es/claude-code](https://wmedia.es/es/claude-code) inside the session, contextually. As you work with Claude Code features, the plugin mentions a relevant tip the first time it spots a topic match. You can also browse, open, or contribute tips at any time.

Multilingual: the conversational layer (welcome, mentions, command UI) follows your working language. Tip content is curated in Spanish and English; if your working language is anything else (Italian, French, Portuguese, etc.), the plugin translates from English on the fly and caches the translation locally so subsequent reads are instant.

## Requirements

The plugin needs the following on the user's machine:

- `bash` — for the SessionStart hook. Native on macOS, Linux, and WSL. On native Windows, install [Git for Windows](https://git-scm.com/downloads/win) (the setup recommended by Claude Code itself), which provides Git Bash. WSL users do not need it.
- `curl` — for fetching tip markdowns. Native on macOS, Linux, WSL, and Windows 10 1809+ (Claude Code's minimum supported Windows version).

The plugin does NOT depend on `jq`, `python3`, or `node` at runtime. State and JSON manipulation use Claude Code's native Read/Write tools.

For contribution submission via `/cc-tips:share`, the [`gh` CLI](https://cli.github.com/) is recommended; if it is missing or unauthenticated, the plugin falls back to a pre-filled GitHub URL you can open manually.

## Install

```bash
/plugin marketplace add juanwmedia/cc-tips
/plugin install cc-tips@juanwmedia-cc-tips
```

To get new tips as they are published, enable auto-update for this plugin's marketplace in `/plugin marketplace`, or run `/plugin marketplace update juanwmedia-cc-tips` periodically.

## Commands

| Command | What it does |
|---|---|
| `/cc-tips:list` | Browse all tips, grouped by topic, with read/unread markers. Optional `<topic>` filter. |
| `/cc-tips:open <N>` | Open the tip with id `<N>` and mark it as read. |
| `/cc-tips:share` | Draft a tip from the current conversation and open a GitHub issue (via `gh` CLI or browser fallback). |
| `/cc-tips:welcome` | Re-show the welcome message. |

The plugin also surfaces tips automatically when you are working on a topic a tip covers (max one mention per topic per session, so different topics each get their own trigger).

## Topics

Tips are classified into one of:

`skills`, `mcp`, `hooks`, `subagents`, `plugins`, `memory-context`, `models-cost`, `permissions`, `sessions`, `autonomous`, `fundamentals`.

## Contributing

Run `/cc-tips:share` after a session where you have discovered a useful pattern. The skill drafts an issue from the conversation context, you review, and submit. The maintainer curates contributions and may publish them as full tips.

## License

MIT — see [LICENSE](LICENSE).
