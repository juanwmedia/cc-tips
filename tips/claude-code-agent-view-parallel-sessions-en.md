---
date: 2026-05-13
type: tip
title_es: "Agent View en Claude Code: una sola pantalla para todos los agentes que has lanzado"
title_en: "Agent View in Claude Code: one screen for every agent you've dispatched"
---

> **TL;DR** `claude agents` opens a panel where every row is a background Claude Code session. At a glance you see which one is waiting on you, which is still working, which is done. Sessions stay alive even after you close the terminal — a per-user supervisor hosts them. Three ways to dispatch: from the view itself, `/bg` inside a session, or `claude --bg "task"` from your shell. Press `Space` to peek and reply without attaching; `Enter` to enter the full conversation. It's the [`/tasks` panel](/en/tips/claude-code-tasks-panel) but at the session level, not the intra-session-task level.

You start a bug fix in one terminal. A PR review in another. An agent investigating a flaky test in a third. Twenty minutes later you have seven tabs open, you don't remember which one was waiting on your input, and two have died because you closed the tab by mistake. Agent View ends the juggling: one screen, one row per session, and a supervisor process keeping the sessions alive whether a terminal is attached or not.

## How it works

Each background session is a full Claude Code process hosted by a **per-user supervisor** — a daemon that starts itself the first time you push something to the background. The supervisor survives auto-updates, keeps sessions running while you have no terminals open, and exits on its own when nothing is left. State lives at `~/.claude/jobs/<id>/state.json`; logs at `~/.claude/daemon.log`.

Rows are auto-grouped: **Needs input** and **Ready for review** on top, **Working** in the middle, **Completed** at the bottom. Each row carries an icon whose color encodes state (animated = working, yellow = waiting on you, green = done, red = failed) and whose shape signals whether the process is alive (`✻` active, `∙` sleeping).

## Result preview

```text
Pinned
  ✽ clawd walk cycle          Write assets/sprites/clawd-walk.png         3m

Ready for review
  ∙ jump physics              github.com/example/game/pull/2048        ●  2h

Needs input
  ✻ power-up design           needs input: double jump or wall climb?     1m

Working
  ✽ collision detection       Edit src/physics/CollisionSystem.ts         2m
  ✢ playtest level 3          run 12 · all checkpoints cleared          in 4m

Completed
  ✻ title screen              result: menu, options, and credits done     9m
```

## How to use it

**1. Open Agent View**

```bash
claude agents
```

Takes over the full terminal, with a dispatch input at the bottom and the list above. `Esc` returns you to the shell without killing anything.

**2. Dispatch a new session (3 ways)**

```bash
# From Agent View: type into the input + Enter
> investigate the flaky SettingsChangeDetector test

# From inside an interactive session
/bg

# Straight from the shell, no Agent View
claude --bg "address review comments on PR 1234"
```

`@<subagent>` at the start of the prompt dispatches the session with a [custom subagent](/en/tips/claude-code-create-custom-agents) as the main agent. `@<repo>` targets the session to a different directory.

**3. Peek and reply inline**

Select a row with arrow keys, `Space` opens the peek panel: you see the last output or the specific question blocking the session. Type the reply, press `Enter` — no attach required. If it's a multi-choice prompt, number keys pick the option.

**4. Attach and detach**

`Enter` or `→` puts you inside the full conversation, exactly as if you had run `claude` in that directory. `←` on an empty prompt kicks you out back to the panel. Detach NEVER kills the session — only `/stop` from inside ends one.

**5. Manage from the shell (no Agent View needed)**

```bash
claude attach <id>     # open the session in this terminal
claude logs <id>       # show recent output
claude stop <id>       # stop (alias: claude kill)
claude respawn <id>    # restart a stopped session, conversation intact
claude rm <id>         # remove from the list + clean its worktree
```

Each session runs in its own [git worktree](/en/tips/claude-code-worktrees-parallel-tasks) under `.claude/worktrees/` — including the ones you push to the background with `/bg` from an interactive session. I've hit this firsthand: two terminals open on the same repo (uncommon, but it happens), `/bg` on one of them, and before touching a single file Claude moved it to its own worktree. Two sessions can't step on each other even if they tried — you pay for it with having to merge or push if you want to keep the changes before deleting the session.

## Where it sits in the parallelism map

| If you want to see… | Look at… |
|---|---|
| Background tasks inside **this** session | [`/tasks` panel](/en/tips/claude-code-tasks-panel) |
| All your **sessions** in parallel | **Agent View** (`claude agents`) |
| Subagents talking to each other | [Agent Teams](/en/tips/claude-code-agent-teams) |
| Clocks and events that wake agents | [map of autonomous primitives](/en/tips/claude-code-loop-routines-monitor-map) |

Agent View doesn't replace `/tasks` — they're different things: `/tasks` shows the tasks INSIDE a session; Agent View shows the sessions ALONGSIDE each other.

## Reference

| Aspect | Detail |
|---|---|
| Command | `claude agents` · `claude --bg "<task>"` · `/bg` inside a session |
| Key shortcuts | `Space` peek · `Enter`/`→` attach · `←` detach · `Ctrl+X` stop (2x = delete) · `Ctrl+T` pin · `?` help |
| States | working · needs input · idle · completed · failed · stopped |
| Persistence | Per-user supervisor, survives auto-updates and terminal closes. Machine sleep/shutdown does kill sessions (`claude respawn --all` brings them back) |
| Isolation | Each session in its own git worktree under `.claude/worktrees/` |
| Requirements | Claude Code v2.1.139+. Research preview |
| Plans | Pro, Max, Team, Enterprise, Claude API |
| Turn off | `disableAgentView: true` in settings · `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` |
| Quota | Each session consumes rate limit independently — 10 parallel agents burn 10× |

> Official docs: [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
