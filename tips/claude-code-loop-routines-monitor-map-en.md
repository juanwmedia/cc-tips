---
date: 2026-05-07
type: tip
title_es: "Loop, Routines, Monitor en Claude Code: el mapa para no equivocarte de herramienta"
title_en: "Loop, Routines, Monitor in Claude Code: the map so you don't pick the wrong one"
---

> **TL;DR** Every Claude Code primitive for "let the agent work when I'm not there" fits inside a 2×3 matrix. Horizontal axis: what wakes it — a **clock** (cron) or an **event** (a line, a PR, a webhook). Vertical axis: where it runs — your active **session**, your persistent **Mac**, or Anthropic's **cloud**. One cell, one primitive. If you know the cell, the name doesn't matter.

Anthropic has stacked six different primitives in under a year: `/loop`, [Monitor](/en/tips/claude-code-monitor-tool-event-driven), Desktop scheduled tasks, [Routines](/en/tips/claude-code-routines-cloud-agents), [Channels](/en/tips/claude-code-channels-control-from-telegram), and the old `cron + claude -p` ([headless mode](/en/tips/claude-code-headless-mode-autonomous-agent)). Each one is named differently in CLI, Web, and Desktop app. And picking the wrong one costs you tokens, lost sessions, or an agent that dies the moment you close the lid.

There's a map.

## The two dimensions that explain everything

**Dimension 1 — what wakes Claude:**

- **Time-driven**: a clock. "Every 5 minutes", "every day at 9 am". Useful for periodic checks where the *moment* matters.
- **Event-driven**: something happens. A line in a log, a PR opening, a webhook landing. Useful when silence costs zero and you only want to react to *that*.

**Dimension 2 — where Claude runs:**

- **Intra-session**: your open terminal right now. Close it and it's gone. Has access to local files and the conversation context.
- **Local persistent**: your Mac, managed by the Desktop app. Survives restarts, but needs the machine awake.
- **Cloud**: Anthropic-managed VMs. Keeps working with the laptop closed. Starts from a fresh clone of the repo.

## The 2×3 matrix (every primitive in one cell)

| | **Time-driven** (clock) | **Event-driven** (event) |
|---|---|---|
| **Intra-session** | `/loop` | [Monitor](/en/tips/claude-code-monitor-tool-event-driven) |
| **Local persistent** | Desktop scheduled task | [Channels](/en/tips/claude-code-channels-control-from-telegram) (external push) |
| **Cloud (Anthropic)** | [Routine](/en/tips/claude-code-routines-cloud-agents) with Schedule trigger | [Routine](/en/tips/claude-code-routines-cloud-agents) with GitHub or API trigger |

Each cell answers two questions: *what wakes Claude* and *where it runs*. That's it.

## How to pick in 3 questions

1. **Do I need this while I'm working right now, in this session?** → row *Intra-session*. If the trigger is time, [`/loop`](/en/tips/claude-code-loop-recurring-tasks). If it's an event (a log line, a stdout signal), [Monitor](/en/tips/claude-code-monitor-tool-event-driven).
2. **Do I need it recurring, but only while my Mac is on?** → row *Local persistent*. Scheduled task → Desktop scheduled task. External push notification (Telegram, Discord) → [Channels](/en/tips/claude-code-channels-control-from-telegram).
3. **Does it have to run reliably even when I close the laptop?** → row *Cloud*. Schedule, GitHub event, or API webhook — it all lands inside a [Routine](/en/tips/claude-code-routines-cloud-agents).

If your question is "what's running right now?" — that's the [`/tasks` panel](/en/tips/claude-code-tasks-panel). It's the dashboard, not a primitive.

## The naming jungle (the same thing shows up under different names)

| Concept | CLI | Web (claude.ai/code) | Desktop app |
|---|---|---|---|
| Cloud agent | `/schedule` (alias `/routines`) | Routines | sidebar **Routines** → **New routine** → **Remote** |
| Local scheduled task | (no CLI equivalent) | (none) | sidebar **Routines** → **New routine** → **Local** |
| Intra-session loop | `/loop` (alias `/proactive`) | (none — needs live CLI) | (none) |
| Stop polling, watch events | Monitor tool (built-in) | (none) | (none) |

**The most expensive confusion**: `/schedule` in the CLI does **NOT** create a Desktop scheduled task on your Mac — it creates a Routine in the cloud. If you want a local Desktop task, open the Desktop app and pick **Local**.

## The detail few people know

`/loop` and Monitor are integrated on purpose. If you fire `/loop check whether CI passed` **with no interval**, Claude self-paces — and may decide to drop down to Monitor under the hood if polling is the wrong shape. The official docs say it [verbatim](https://code.claude.com/docs/en/scheduled-tasks#let-claude-choose-the-interval):

> *"When you ask for a dynamic `/loop` schedule, Claude may use the Monitor tool directly. Monitor [...] avoids polling altogether and is often more token-efficient."*

You ask "watch this"; Claude picks the mechanism.

## Quick reference

| Primitive | Persistence | Min interval | Best for |
|---|---|---|---|
| [`/loop`](/en/tips/claude-code-loop-recurring-tasks) | Active session only (auto-expires 7d) | 1 min | Watching while you work |
| [Monitor](/en/tips/claude-code-monitor-tool-event-driven) | Active session only | Async events | Log tails, waiting on signals |
| Desktop scheduled task | Mac awake | 1 min | Tasks with local file access |
| [Channels](/en/tips/claude-code-channels-control-from-telegram) | While your CLI is listening | External push | Receiving orders from Telegram/Discord |
| [Routine schedule](/en/tips/claude-code-routines-cloud-agents) | Cloud, always | 1 hour | Unattended cron without your Mac |
| [Routine event](/en/tips/claude-code-routines-cloud-agents) | Cloud, always | Webhook / GitHub event | Auto PR review, alert triage |

> Official docs: [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) · [Routines](https://code.claude.com/docs/en/routines) · [Monitor tool reference](https://code.claude.com/docs/en/tools-reference#monitor-tool)
