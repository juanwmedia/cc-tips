---
date: 2026-02-21
type: tip
title_es: "Ejecuta comandos en el terminal sin salir de Claude Code"
title_en: "Run Shell Commands Without Leaving Claude Code"
---
# Quick Tip: Run Shell Commands Without Leaving Claude Code

Claude Code has a built-in bash mode: type `!` followed by any command and it runs directly in your shell, without Claude interpreting or approving it. Output appears in real time and gets added to the conversation context — Claude sees the result and can act on it.

It's not an obvious feature, but once you discover it, it changes how you work. No need to open another terminal or split pane. You type, it runs, you keep talking.

> **TL;DR** Prefix any command with `!` to run it directly. Use `Ctrl+B` to send long-running processes to the background. Claude sees the output from both.

Result:

```
> ! git status

On branch feature/auth
Changes not staged for commit:
  modified:   src/auth/login.ts
  modified:   src/auth/session.ts
```

## How to use it

### 1. Run a quick command

Type `!` followed by the command:

```bash
! npm test
! git diff --stat
! ls -la src/
```

Claude doesn't intervene — the command goes straight to your shell. But the output is added to the conversation, so you can ask "what failed?" right after.

### 2. Send a long process to the background

If a command takes too long (builds, tests, dev servers), press `Ctrl+B` while it's running:

```bash
! npm run build
# taking too long → press Ctrl+B
# Claude is available again while the build finishes in background
```

You can also ask Claude directly to run something in the background.

### 3. History-based autocomplete

Type `!` followed by the first few letters and press `Tab`. Claude Code autocompletes from previous `!` commands in the current project.

```bash
! np  → Tab → ! npm test
```

## Reference

| Aspect | Detail |
|---|---|
| Prefix | `!` at the start of input |
| Execution | Directly in your shell, no Claude interpretation |
| Output | Shown in real time and added to conversation context |
| Background | `Ctrl+B` during execution (tmux: press twice) |
| Autocomplete | `Tab` completes from project's `!` command history |
| Permissions | No approval needed — it's your terminal |

> **Personal note:** This is one of those features you don't discover by reading the docs — you see someone use it. You're debugging, need a quick `git log` or a `cat` of a file, and instead of jumping to another tab you just type `! git log --oneline -5`. Seems minor, but it eliminates the constant context switching.

> Official docs: [Interactive mode — Bash mode](https://code.claude.com/docs/en/interactive-mode#bash-mode-with-prefix)
