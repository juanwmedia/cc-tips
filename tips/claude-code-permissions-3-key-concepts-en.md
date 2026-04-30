---
date: 2026-02-21
type: tip
title_es: "3 cosas que debes saber sobre /permissions en Claude Code"
title_en: "3 Things You Must Know About /permissions in Claude Code"
---
# Quick Tip: 3 Things You Must Know About /permissions in Claude Code

The `/permissions` command looks like just another menu. In reality, it's the gateway to an access control system with modes, granular rules, and its own evaluation order. You don't need to master it all, but there are three concepts that will bite you if you don't know them.

> **TL;DR** Deny rules always win. Modes change everything. And the `Tool(specifier)` syntax supports wildcards and gitignore patterns. That covers 90%.

Result:

```bash
/permissions

Allow rules:
  Bash(npm run *)         # from .claude/settings.json
  Bash(git commit *)      # from .claude/settings.json
  Edit(/src/**)           # from .claude/settings.json

Deny rules:
  Bash(git push *)        # from .claude/settings.json
  Read(.env)              # from .claude/settings.json
```

## The 3 key concepts

### 1. Evaluation order: deny always wins

Rules are evaluated in this order: **deny → ask → allow**. First match wins. If a deny matches, it doesn't matter how many allow rules you have — the operation is blocked.

```json
{
  "permissions": {
    "allow": ["Bash(git *)"],
    "deny": ["Bash(git push *)"]
  }
}
```

In this example, `git commit -m "fix"` passes. `git push origin main` is blocked. The deny for `git push *` matches before the allow for `git *` gets a chance.

### 2. Modes change all behavior

Claude Code has 5 permission modes. You can cycle through the three main ones with **Shift+Tab** during your session:

| Mode | What it does |
|---|---|
| `default` | Prompts for permission on each new tool |
| `acceptEdits` | Auto-accepts file edits |
| `plan` | Read-only — Claude analyzes but modifies nothing |
| `dontAsk` | Denies everything not explicitly in allow |
| `bypassPermissions` | Skips all checks (isolated environments only) |

`dontAsk` is the most misunderstood mode: it's not "accept everything without asking" — it's the exact opposite. It denies everything except what you've pre-approved via `/permissions` or `permissions.allow`.

### 3. The syntax supports more than you think

Rules follow the `Tool(specifier)` format with wildcards:

| Rule | What it allows |
|---|---|
| `Bash(npm run *)` | Any npm script |
| `Bash(* --version)` | Any command with `--version` |
| `Edit(/src/**)` | Edit any file under `src/` (recursive) |
| `Read(.env)` | Read `.env` in the current directory |
| `Read(~/.ssh/*)` | Read files in your `.ssh` directory |
| `mcp__notion__*` | Any tool from the Notion MCP server |

For Read and Edit, patterns follow the gitignore spec: `*` matches within a directory, `**` matches recursively.

## Where rules are stored

| File | Scope |
|---|---|
| `~/.claude/settings.json` | Personal — all your projects |
| `.claude/settings.json` | Project — shared with the team |
| `.claude/settings.local.json` | Project — only you (gitignored) |

Project rules take precedence over personal ones. If a project denies something you allow, the project wins.

> Official docs: [Configure permissions](https://code.claude.com/docs/en/permissions)
