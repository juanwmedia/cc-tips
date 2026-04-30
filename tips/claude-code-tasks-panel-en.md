---
date: 2026-04-27
type: tip
title_es: "Tu Claude Code está trabajando en paralelo. ¿Sabes verlo?"
title_en: "Your Claude Code Is Running in Parallel. Do You Know Where to See It?"
---

> **TL;DR** `/tasks` (alias `/bashes`) opens the panel where every parallel job in Claude Code converges: background bashes from `Ctrl+B`, cloud sessions from `--remote`, plans from `/ultraplan`, reviews from `/ultrareview`, memory consolidation, and subagents. If you've never opened it, it's probably because you haven't sent anything in yet.

## Why nobody knows it exists

You probably opened `/tasks` once, saw **"No tasks currently running"** and closed it. So did I. The panel isn't interesting on its own — it's interesting once you realize it's the **shared dashboard** of five Claude Code features you're probably already using separately.

Each of those features delegates work somewhere (your shell, a cloud VM, a subagent, Claude's subconscious) and reports back to the same panel. `/tasks` is where they reunite.

## The 5 things that populate your /tasks

**1. Local background bashes (`Ctrl+B`)**

While running a command with `!` ([bash mode](/en/tips/claude-code-bash-mode-run-shell-commands)), press `Ctrl+B` to send it to the background. It shows up in `/tasks` with its PID and live output. Perfect for long builds, heavy tests, or dev servers.

**2. Cloud sessions with `--remote`**

Every `claude --remote "task"` you launch creates a [parallel cloud session](/en/tips/claude-code-cloud-sessions-from-browser). You can fire 3 or 4 at once and see them all listed here, each linking to `claude.ai/code` for the diff.

**3. `/ultraplan` running in the cloud**

[`/ultraplan`](/en/tips/claude-code-ultraplan-cloud-planning) delegates planning to a web session. Your terminal stays free while the plan is woven in the background. `/tasks` shows you the state (`investigating`, `needs your input`, `ready`) and the link to review.

**4. `/ultrareview` in parallel**

[`/ultrareview`](/en/tips/claude-code-ultrareview) launches a fleet of reviewer agents in the cloud and takes 10–20 minutes. While they run, you keep coding. `/tasks` reports the progress of each one.

**5. Memory consolidation and subagents**

When Claude runs [memory consolidation](/en/tips/claude-code-auto-dream-memory-consolidation) or spawns a subagent with `run_in_background: true`, those land here too.

## How to navigate it

```
↑/↓     Move between tasks in the list
Enter   Open a task — see output, session link, Stop option
←/Esc   Close the panel and return to the conversation
```

Once inside a task you can read its full output or stop it if it's going off the rails.

## How work gets in there

| Path | Who triggers it | When it appears |
|---|---|---|
| `Ctrl+B` during a `!` | You, manually | The instant you press it |
| `claude --remote "..."` | You, from the CLI | When the cloud session is created |
| `/ultraplan` | You, command or keyword | After confirming the launch |
| `/ultrareview` | You, command or `/ultrareview <PR>` | After confirming the launch |
| Subagent with `run_in_background` | Claude, autonomously | At spawn |
| Memory consolidation | Claude, during `/auto-dream` | While running |

## The mental shift

`/tasks` doesn't fill up because you open it. It fills up when you start to delegate. The right question isn't "what does `/tasks` do?" but "what long-running work am I running serially that could be running in parallel?"

> Official docs: [Interactive mode — Background bash commands](https://code.claude.com/docs/en/interactive-mode) · [Commands reference](https://code.claude.com/docs/en/commands)
