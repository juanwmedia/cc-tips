---
date: 2026-02-21
type: tip
title_es: "Deshaz Cambios al Instante con Checkpoints"
title_en: "Rewind Changes Instantly with Checkpoints"
---
# Quick Tip: Rewind Changes Instantly with Checkpoints

Claude Code automatically snapshots your code before every edit. Each time you send a prompt, a checkpoint is created. If Claude takes a wrong turn — breaks a feature, goes down the wrong path, or over-engineers a solution — you can rewind to any previous state in seconds. Checkpoints persist across sessions and are cleaned up automatically after 30 days.

Result:

```
> Esc Esc  (press Escape twice)

┌─ Rewind to ──────────────────────────┐
│ ● Message 5: "Add auth middleware"   │
│ ○ Message 4: "Create user model"     │
│ ○ Message 3: "Set up database"       │
│                                      │
│ Restore: ◉ Both  ○ Code  ○ Convo    │
└──────────────────────────────────────┘
```

## Setup

No setup needed. Checkpointing is enabled by default.

**1. Make some changes with Claude**

Work normally — every prompt you send creates a checkpoint automatically.

**2. Rewind when needed**

Press `Esc` twice quickly, or type `/rewind`. Select the checkpoint and what to restore:

```
Esc + Esc     → Opens the rewind menu
/rewind       → Same thing, via command
```

**3. Choose what to restore**

| Option | What it does |
|---|---|
| **Both code and conversation** | Restores files and rewinds the chat to that point |
| **Code only** | Reverts file changes, keeps the full conversation |
| **Conversation only** | Rewinds the chat, keeps current file state |

## Reference

| Feature | Details |
|---|---|
| Trigger | `Esc` + `Esc` or `/rewind` |
| Checkpoint creation | Automatic on every user prompt |
| Persistence | Survives session restarts and `/resume` |
| Retention | 30 days (configurable via `cleanupPeriodDays`) |
| Tracks | File edits made through Claude's editing tools |
| Does NOT track | Bash commands (`rm`, `mv`, `cp`), external edits |

## Limitations

- Files modified by bash commands (e.g., `rm file.txt`) are not tracked
- Manual edits you make outside Claude Code are not captured
- Checkpoints are session-level recovery, not a replacement for Git

> Official docs: [Checkpointing](https://code.claude.com/docs/en/checkpointing)
