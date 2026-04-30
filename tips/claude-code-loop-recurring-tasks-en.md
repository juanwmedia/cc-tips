---
date: 2026-03-31
type: tip
title_es: "Haz que Claude Code vigile tu código mientras trabajas"
title_en: "Make Claude Code Watch Your Code While You Work"
---
# Quick Tip: Make Claude Code Watch Your Code While You Work

> **TL;DR** `/loop 5m <prompt>` runs a prompt on a recurring interval inside your active session. Unlike a cron with `claude -p`, each iteration has full access to your conversation context: files read, decisions made, changes in progress. It's a watchdog with a brain, not a blind script.

You could set up a cron that runs `claude -p "check deploy status"` every 5 minutes. It works. But each execution starts from scratch — no memory of what happened before, no session context, no ability to act on what it finds.

`/loop` is different: it runs inside your open session. Claude knows which files you changed, what you were trying to do, and can compare with the previous iteration. If something changes, it can act immediately with all your tools.

The limitation: you need the session open. Close the terminal, and it's gone. Tasks also auto-expire after 3 days. For monitoring that survives a reboot, use [headless mode with cron](/en/tips/claude-code-headless-mode-autonomous-agent).

Result:

```
> /loop 5m check if the staging deploy at localhost:3000 is responding

Loop started (every 5m). Task ID: loop-a1b2c3
Next run: 12:05:00

# 12:05 — localhost:3000 returns 503. Deploy still in progress.
# 12:10 — localhost:3000 returns 200. Deploy complete. All health checks pass.
```

## How to use it

### **1. Basic syntax**

```
/loop [interval] <prompt>
```

Default interval is 10 minutes. Formats: `5m` (minutes), `2h` (hours), `1d` (days).

### **2. Practical examples**

```
# Watch a deploy
/loop 5m check if the staging deploy finished and tests pass

# Monitor PRs
/loop 15m check open PRs for new comments, summarize responses needed

# Detect merge conflicts
/loop 30m detect merge conflicts between current branch and main

# Scan logs for errors
/loop 5m scan app.log for FATAL/ERROR entries in the last 5 minutes
```

### **3. Best practices**

- Define alert conditions — you don't want noise on every iteration, only anomalies
- Limit the scope — `src/` instead of the entire project
- Set termination rules — "stop after 3 consecutive passes"

## /loop vs cron + claude -p

| Aspect | `/loop` | `cron + claude -p` |
|---|---|---|
| Context | Full session (files, history, decisions) | None — each run is fresh |
| Can act | Yes — edits, executes, uses tools | Yes, but without prior context |
| Accumulates knowledge | Yes — compares with previous iterations | No |
| Persistence | Only while session is open | Survives reboots |
| Expiry | 3 days automatically | No limit |
| Concurrency | Max 50 tasks per session | No limit |
| Use case | Watch while you work | Real monitoring / scheduled tasks |

## Reference

| Aspect | Detail |
|---|---|
| Command | `/loop [interval] <prompt>` |
| Default interval | 10 minutes |
| Formats | `5m`, `2h`, `1d` |
| Max tasks | 50 per session |
| Expiry | 3 days |
| Persistence | Does not survive terminal close |
| Type | Bundled skill (ships with Claude Code) |

> Official docs: [Skills — Bundled skills](https://code.claude.com/docs/en/skills#bundled-skills)
