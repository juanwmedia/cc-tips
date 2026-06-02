---
date: 2026-06-02
type: tip
title_es: "ultracode en Claude Code: que Claude decida solo cuándo desplegar un ejército de agentes"
title_en: "ultracode in Claude Code: let Claude decide on its own when to deploy an army of agents"
---
> **TL;DR** `/effort ultracode` bumps your session to `xhigh` and lets Claude decide on its own, for every substantive task, whether it's worth spinning up an [agent workflow](/en/tips/claude-code-workflows-subagents-at-scale) (understand → change → verify). It's not a new reasoning level above `xhigh`: it's `xhigh` **plus** automatic orchestration. It lasts the session and you drop back with `/effort high`. Turn it on for hard, multi-step work; turn it off for routine work, because it costs more on every task.

There are two ways to get agents out of Claude Code. The manual one: you put `workflow` in your prompt or run `/deep-research`, and **you** decide when to parallelize, for one specific task. And the automatic one: `/effort ultracode`, where **Claude** decides, for the whole session. This tip is about the second, and about the only question that matters: when to flip that switch.

## What it actually is

`ultracode` is an option in the `/effort` menu, not a separate command. It does two things at once:

1. **Bumps reasoning to `xhigh`** (the high rung of [effort](/en/tips/claude-code-effort-level-adjust-reasoning)).
2. **Hands Claude the orchestration call.** Instead of waiting for you to ask for a workflow, Claude plans one on its own for every substantive task in the session.

Watch the name: it isn't reasoning "higher than `xhigh`". It's `xhigh`, and on top of that, the decision of when to deploy agents moves from you to Claude.

## What happens when you turn it on

```
> /effort ultracode
  Effort: ultracode · Claude plans a workflow for each substantive task

> refactor the auth module and add tests
  → workflow 1: understand the auth flow
  → workflow 2: make the change
  → workflow 3: verify it (agents that refute each other)
```

A single request turns into several workflows in a row: one to understand, one to change, one to verify. And this applies to every substantive task you ask for until you turn it off.

## How to use it

**1. Turn it on.**

```
/effort ultracode
```

It needs a model that supports `xhigh`. If yours doesn't, `ultracode` won't even show up in the `/effort` menu.

**2. Work as usual.** `ultracode` automates the *decision to plan* a workflow, not launching it blindly: in the default permission mode, Claude shows you the phases before running and you approve each run (you can open the script; it's not a black box).

**3. Turn it off.**

```
/effort high
```

It only lasts the current session and resets when you open a new one, but drop back to `high` as soon as you return to routine tasks.

## When to, and when not to

| Turn it on for | Don't turn it on for |
|---|---|
| Large migrations, multi-file refactors | Renames, one-line fixes |
| Bug or security audits across the codebase | Formatting or config changes |
| Research with cross-checked sources | Quick questions |
| A whole session of hard work | Routine day-to-day |

The rule: if the task doesn't need several agents checking each other, `ultracode` charges you `xhigh` plus orchestration for nothing.

## What can bite you

- **It costs more on every substantive task**, not just the big ones. Each request burns more tokens and takes longer. That's why it's a switch you flip on and off, not a default.
- **In Auto mode there's no such brake.** With Auto permissions (or bypass), ultracode doesn't just plan the workflow, it launches it without asking, and agent fleets start on their own.
- **If you disable workflows** (`/config`, `disableWorkflows`, or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`), `ultracode` disappears from the `/effort` menu.

## Reference

| Aspect | Detail |
|---|---|
| Command | `/effort ultracode` |
| What it is | `xhigh` effort + automatic orchestration (not a new level) |
| Scope | The whole session, every substantive task |
| Behavior | 1 request → several workflows in a row (understand → change → verify) |
| Turn off | `/effort high` (or a new session) |
| Requirement | A model with `xhigh`; otherwise it's not in the menu |
| Auto mode | Skips the workflow approval prompt |
| Availability | Research preview, part of [dynamic workflows](/en/tips/claude-code-workflows-subagents-at-scale) (v2.1.154+) |

> Official docs: [Let Claude decide with ultracode](https://code.claude.com/docs/en/workflows#let-claude-decide-with-ultracode)
