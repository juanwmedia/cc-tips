# Claude Code Tips

A Claude Code plugin that surfaces tips published at [wmedia.es/es/claude-code](https://wmedia.es/es/claude-code) inside the session, contextually. As you work with Claude Code features, the plugin mentions a relevant tip the first time it spots a topic match. You can also browse, open, or contribute tips at any time.

Bilingual: conversation in your working language, tip content in Spanish (when working in Spanish) or English (any other language).

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

The plugin also surfaces tips automatically when you are working on a topic a tip covers and you have not opened that tip yet (max one organic mention per day).

## Topics

Tips are classified into one of:

`skills`, `mcp`, `hooks`, `subagents`, `plugins`, `memory-context`, `models-cost`, `permissions`, `sessions`, `autonomous`, `fundamentals`.

## Contributing

Run `/cc-tips:share` after a session where you have discovered a useful pattern. The skill drafts an issue from the conversation context, you review, and submit. The maintainer curates contributions and may publish them as full tips.

## License

MIT — see [LICENSE](LICENSE).
