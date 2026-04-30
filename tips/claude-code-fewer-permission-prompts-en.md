---
date: 2026-04-28
type: tip
title_es: "Allowlist automática en Claude Code: deja que se escriba sola"
title_en: "Automatic allowlist in Claude Code: let it write itself"
---
> **TL;DR** The official `/fewer-permission-prompts` skill scans your session history, detects which read-only commands you keep approving, and adds them to `.claude/settings.json` as a prioritized allowlist. No JSON editing by hand.

If you don't use [auto mode](/en/tips/claude-code-auto-mode-vs-yolo) but you're sick of approving `npm run typecheck` for the hundredth time, this skill is your shortcut. Anthropic shipped it specifically for people who keep the [6 permission modes](/en/tips/claude-code-permission-modes-shift-tab) and the manual friction, but want out of the daily approval fatigue.

## How it works internally

When you run `/fewer-permission-prompts`, Claude Code:

1. Finds your transcripts at `~/.claude/projects/<dir>/*.jsonl` (capped at the 50 most-recent sessions).
2. Extracts every Bash and MCP call, groups by command + first subcommand: `git log`, `gh pr view`, `mcp__slack__read_thread`.
3. Filters down to pure read-only: drops `rm`, `git push`, `npm install`, builds with side effects.
4. Drops what Claude Code already auto-allows without an allowlist entry (`cat`, `ls`, `git status`, `gh pr view`, `docker logs`...).
5. Blocks dangerous wildcards: `Bash(python3:*)`, `Bash(bun run *)`, `sudo`, interpreters and shells — anything that grants arbitrary code execution.
6. Ranks by frequency, drops anything appearing fewer than 3 times, shows you the top 20.

## The result

```text
| # | Pattern                          | Count | Notes                |
|---|----------------------------------|-------|----------------------|
| 1 | Bash(npm run typecheck)          | 87    | type-check loops     |
| 2 | Bash(git log *)                  | 54    | history exploration  |
| 3 | mcp__wmedia__get-tip-tool        | 31    | tip lookups          |
```

And your project's `.claude/settings.json` ends up like this (preserving anything that was already there):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run typecheck)",
      "Bash(git log *)",
      "mcp__wmedia__get-tip-tool"
    ]
  }
}
```

## How to invoke it

```bash
/fewer-permission-prompts
```

It's a built-in skill in Claude Code (v2.1+). No install, no setup. It generates the table, explains what it added and what it skipped, and writes to the current project's `.claude/settings.json` — not to the global `~/.claude/settings.json`, not to `.claude/settings.local.json`.

If the skill seems to "miss" commands you run daily (`ls`, `cat`, `git status`, `gh pr view`...), that's a good sign: those are already auto-allowed without needing an allowlist entry.

## Allowlist patterns you'll see

| Form | When it's used |
|---|---|
| `Bash(foo)` | Exact match, one specific invocation |
| `Bash(foo *)` | Prefix + space: matches `foo`, `foo bar`, `foo --opt` |
| `Bash(foo*)` | No space: careful, `Bash(ls*)` also matches `lsof` |
| `mcp__server__tool` | Full MCP tool name, no wildcards |

> Official docs: [Configure permissions](https://code.claude.com/docs/en/permissions)
