---
name: welcome
description: Show the Claude Code Tips welcome message on demand.
disable-model-invocation: true
model: haiku
---

# /cc-tips:welcome

Render the welcome block on demand, regardless of whether the user has seen it before.

The session-start hook has already injected the LANGUAGE RULE. Apply it: render in the user's working language; translate the English source naturally if the working language is not English. Keep "Claude Code Tips" and slash command names in English.

## Welcome block (English source)

> **Welcome to Claude Code Tips.**
>
> This plugin surfaces tips from wmedia.es as you work. When you're exploring a Claude Code feature a tip covers, I'll mention it briefly (max one per topic per session).
>
> You can also:
>
> - `/cc-tips:list` — browse all available tips.
> - `/cc-tips:list <topic>` — filter by topic.
> - `/cc-tips:open <N>` — read a specific tip.
> - `/cc-tips:share` — contribute a tip you've discovered.
>
> To get new tips as they're published, enable auto-update for this plugin in `/plugin marketplace`, or run `/plugin marketplace update juanwmedia-cc-tips` periodically.

After rendering, do nothing else. Do not modify state.
