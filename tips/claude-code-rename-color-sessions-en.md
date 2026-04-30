---
date: 2026-03-23
type: tip
title_es: "Distingue tus sesiones de Claude Code de un vistazo"
title_en: "Tell Your Claude Code Sessions Apart at a Glance"
---
# Quick Tip: Tell Your Claude Code Sessions Apart at a Glance

> **TL;DR** Use `/rename` to name your session and `/color` to change the prompt bar color. When you have multiple sessions open or need to find an old one with `/resume`, name + color is the difference between "which one was it?" and knowing instantly.

Managing sessions in Claude Code is one of its weakest areas. Everything looks the same: same bar, same color, no title. If you work with parallel sessions or need to pick up a conversation from days ago, telling them apart is a memory exercise.

`/rename` and `/color` don't solve the root problem, but they make it much more manageable. With a descriptive name and a distinct color, each session has visual identity. And when you use `/resume` to browse past sessions, the name you gave it shows up as searchable text.

Result:

```
> /rename auth-refactor
> /color blue

# The prompt bar now shows "auth-refactor" with a blue border.
# When you run /resume, the session is listed as "auth-refactor".
```

## How to use it

### **1. Name at startup (recommended)**

```bash
claude -n "auth-refactor"
```

The name appears on the prompt bar and in `/resume`. You can resume the session directly:

```bash
claude -r "auth-refactor"
```

### **2. Rename during the session**

```
/rename auth-refactor
```

Without arguments, `/rename` auto-generates a name based on the conversation. My recommendation: name it yourself. Auto-generated names are generic and hard to remember.

### **3. Assign a color**

```
/color blue
```

Changes the border color of the input bar. Useful when you have multiple terminal tabs open — each with a different color.

### **4. Find sessions with /resume**

```
/resume
```

Opens an interactive picker. You can search by name, press `R` to rename a session, or `P` to preview it.

## Reference

| Command | What it does |
|---|---|
| `claude -n "name"` | Name the session at startup |
| `/rename name` | Rename the current session |
| `/rename` (no args) | Auto-generate name from context |
| `/color color` | Change the prompt bar border color |
| `/resume` | Interactive session picker (`R` = rename, `P` = preview) |
| `claude -r "name"` | Resume a session by name from CLI |

| Limitation | Detail |
|---|---|
| Directory | Sessions are tied to the working directory. `/resume` only shows sessions from the current directory. |
| Color persistence | Color applies to the current session. It does not persist when resuming. |

> Official docs: [CLI reference — Session flags](https://code.claude.com/docs/en/cli-reference)
