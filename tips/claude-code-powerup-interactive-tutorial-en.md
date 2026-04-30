---
date: 2026-04-02
type: tip
title_es: "Claude Code tiene un tutorial interactivo oculto: /powerup"
title_en: "Claude Code Has a Hidden Interactive Tutorial: /powerup"
---
# Quick Tip: Claude Code Has a Hidden Interactive Tutorial: /powerup

> **TL;DR** Type `/powerup` and access 18 interactive lessons with animated demos right in your terminal. Each one teaches a feature most people miss. Even if you're a power user, you'll discover something.

Since version 2.1.90, Claude Code includes a built-in lesson system. It's not static documentation — these are interactive tutorials with code snippets, animated demos, and gamified progress. Each "power-up" covers a specific feature you can try on the spot.

The interesting part: it's not just for beginners. As a heavy user, I discovered you can append `&` to the end of a bash command to have Claude run it in the background and supervise it — something I hadn't seen in any documentation.

Result:

```
> /powerup

Power-ups 0/18 unlocked ████░░░░░░░░░░░

Each power-up teaches one thing Claude Code can do
that most people miss. Open one, read it, try it, mark it done.

  o Talk to your codebase      @ files, line refs
  o Steer with modes           shift+tab, plan, auto
  o Undo anything              /rewind, Esc-Esc
  o Run in the background      tasks, /tasks
  o Teach Claude your rules    CLAUDE.md, /memory
  o Extend with tools          MCP, /mcp
  o Automate your workflow     skills, hooks
  o Multiply yourself          subagents, /agents
  o Code from anywhere         /remote-control, /teleport
  o Dial the model             /model, /effort
```

## How to use it

### **1. Open the power-ups menu**

```
/powerup
```

You'll see the full list with your progress. Select any to open it.

### **2. Read, try, mark as done**

Each power-up has explanatory text, code snippets, and an animated demo. Once you've tried it, mark it as completed. Your progress is saved.

### **3. Discover what you didn't know**

Some power-ups that surprise even advanced users:

- **Run in the background**: `! npm run build &` — the trailing `&` makes Claude run the command in the background and supervise it. You can keep working.
- **Steer with modes**: `Shift+Tab` cycles between default, plan, and auto mode without opening any menu.
- **Undo anything**: `Esc+Esc` opens rewind directly, without typing `/rewind`.

## Reference

| Aspect | Detail |
|---|---|
| Command | `/powerup` |
| Lessons | 18 power-ups |
| Format | Text + snippets + animated demos |
| Progress | Saved across sessions |
| Minimum version | v2.1.90+ |
| Level | Beginner to advanced |

> Official docs: [Changelog — v2.1.90](https://code.claude.com/docs/en/changelog)
