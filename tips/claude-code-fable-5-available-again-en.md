---
date: 2026-06-30
type: tip
title_es: "Fable 5 disponible de nuevo en Claude Code: esto es todo lo que tienes que saber"
title_en: "Fable 5 is back in Claude Code: everything you need to know"
---

> **TL;DR** Fable 5 returns to Claude Code on **July 1**, after being suspended on June 12 over a US export control. It comes back with a **stricter safety classifier**: it blocks the incident's technique in over 99% of cases, but in exchange it fires more false positives on ordinary coding tasks. When it blocks, your request goes to **Opus 4.8** with a notice. You don't have to do anything to get it back.

Fable 5 launched on June 9. Three days later it vanished from your picker with barely an explanation. The reason: Amazon researchers found a way to bypass its safeguards so it would identify software vulnerabilities, and the US government issued an export control that required restricting access to foreign nationals. Since Anthropic couldn't verify each user's nationality in real time, it cut access for everyone. Now it's back.

## What changes for you

The same model returns, but with reinforced safety. And that reinforcement has a side effect you will notice while coding:

- **A new, more sensitive classifier.** Anthropic trained a classifier that blocks the report's technique in **>99%** of cases. The margin is wider, so expect **more false positives on routine coding and debugging**, not just on security or biology.
- **The reroute to Opus 4.8 fires more often.** When a request is flagged, Claude Code notifies you and sends it to Opus 4.8, and the session continues on Opus. This already happened before; now it will happen more.
- **Access by plan through July 7.** For the first week, access depends on your plan; after that, on your usage credits.

## What to do (not much)

Nothing to install or enable: Fable 5 reappears in your picker on July 1 on its own (run `claude update` if your version is old). What's useful is knowing how to react to the reroute:

```bash
# If a request gets blocked, you're on Opus 4.8. To go back to Fable:
/model fable

# To decide each time instead of letting it switch on its own:
/config   # → turn off "switch models when a message is flagged"
```

And if the reroute fires on your very first message, it's often your own context triggering it (`CLAUDE.md`, directory names, git status). To check, start in [safe mode](/en/tips/claude-code-safe-mode) with `claude --safe-mode`.

The full detail on what Fable 5 is, how to switch to it, when it's worth it, and how that reroute works is in the deep-dive tip: [Fable 5 in Claude Code, the model above Opus](/en/tips/claude-code-fable-5-above-opus).

## The timeline

| Date | What happened |
|---|---|
| Jun 9 | Fable 5 and Mythos 5 launch |
| Jun 12 | US export control; Anthropic suspends access for everyone |
| Jun 26 | Mythos 5 restored |
| Jun 30 | Export control on Fable 5 lifted |
| **Jul 1** | **Fable 5 available again, globally, including Claude Code** |

> Official docs: [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5) · [Model configuration](https://code.claude.com/docs/en/model-config)

## Requirements

- Claude Code v2.1.170+ to see Fable 5 in the picker (`claude update`). Not available under zero data retention.
