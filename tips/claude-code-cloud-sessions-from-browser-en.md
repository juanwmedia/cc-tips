---
date: 2026-04-05
type: tip
title_es: "Claude Code en la Nube: Sesiones Paralelas desde el Navegador"
title_en: "Claude Code on the Web: Parallel Cloud Sessions from Your Browser"
---
Giving up your local environment sounds intimidating. Your editor, your terminal, your dotfiles — there's comfort in having everything within reach. But for routine tasks — a review, a security scan, a quick exploration — you don't need all of that. Claude Code on the web runs those tasks on Anthropic-managed cloud infrastructure, directly from [claude.ai/code](https://claude.ai/code). Each session gets an isolated VM with your repo cloned, a pre-configured environment, and limited network access by default. Your terminal stays free. And you can run several tasks in parallel.

> **TL;DR** Visit [claude.ai/code](https://claude.ai/code), connect GitHub, describe the task. Claude clones, executes, tests, and prepares a PR. Also available from the terminal with `claude --remote "task"`. Requires Pro, Max, Team, or Enterprise.

Result:

```bash
> claude --remote "Fix the flaky test in auth.spec.ts"
# Session created on claude.ai/code

> claude --remote "Update the API documentation"
# Second session in parallel

> claude --remote "Refactor the logger to use structured output"
# Third session in parallel
```

## How to use it

### **1. From the browser**

1. Go to [claude.ai/code](https://claude.ai/code)
2. Connect your GitHub account and install the Claude GitHub App
3. Select an environment (or use the default)
4. Describe the task in natural language
5. Review changes in diff view, iterate with comments, and create a PR

### **2. From the terminal**

```bash
# Initial setup (uses gh CLI credentials)
/web-setup

# Launch a task in the cloud
claude --remote "Add input validation to the signup form"

# Launch several in parallel
claude --remote "Fix auth bug"
claude --remote "Add pagination to /api/users"
```

Each `--remote` creates its own cloud session. Monitor all of them with `/tasks`.

### **3. Pull a session into your terminal (teleport)**

```bash
# Interactive picker for web sessions
claude --teleport

# Specific session
claude --teleport <session-id>

# From inside Claude Code
/teleport
```

Teleport verifies you're in the correct repository, fetches the branch, and loads the full conversation history.

## Reference

| Command / Action | What it does |
|---|---|
| `claude --remote "task"` | Launch a cloud session from the terminal |
| `/web-setup` | Connect GitHub using `gh` CLI credentials |
| `claude --teleport` | Pull a web session into your local terminal |
| `/teleport` or `/tp` | Same, from inside Claude Code |
| `/tasks` | List background sessions |

| Detail | Value |
|---|---|
| VM | Isolated per session, managed by Anthropic |
| Base image | Ubuntu 24.04 with Node, Python, Go, Rust, Java, Ruby, PHP, PostgreSQL 16, Redis 7 |
| Network | Limited by default (package registries + GitHub). Configurable. |
| Parallel sessions | No hard limit; they share your plan's rate limits |
| Code platforms | GitHub only (GitHub Enterprise Server for Team/Enterprise) |
| Plans | Pro, Max, Team, Enterprise |

**Related:** [Control Claude Code from Your Phone](/en/tips/claude-code-remote-control-from-phone) · [Worktrees for parallel tasks](/en/tips/claude-code-worktrees-parallel-tasks)

> Official docs: [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)

## Requirements

- Pro, Max, Team, or Enterprise subscription (API keys not supported)
- GitHub account connected
- `gh` CLI installed and authenticated (for terminal setup; optional from the browser)
