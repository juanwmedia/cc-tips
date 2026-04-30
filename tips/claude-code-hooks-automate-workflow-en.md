---
date: 2026-02-23
type: tip
title_es: "Hooks en Claude Code — Automatiza Tu Flujo de Trabajo"
title_en: "Claude Code Hooks — Automate Your Workflow"
---
# Quick Tip: Claude Code Hooks — Automate Your Workflow

Hooks are commands that run automatically at specific points in Claude Code's lifecycle. Unlike CLAUDE.md instructions (which Claude may ignore), hooks are **deterministic**: if the condition is met, they always execute. Three handler types cover everything from simple validations to AI-powered verification.

For a complete guide with 5 essential hooks and advanced patterns, see the [full hooks article](/en/writing/claude-code-hooks-practical-guide).

Result:

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\""
      }]
    }]
  }
}
```

## The 3 hook types

**1. Command — Run a script**

The most common. Receives context via stdin as JSON, and the exit code decides the outcome: `0` passes, `2` blocks.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo $CLAUDE_TOOL_INPUT | jq -e '.command | test(\"rm -rf|--force|DROP TABLE\") | not'"
      }]
    }]
  }
}
```

This hook blocks destructive commands like `rm -rf`, `--force`, or `DROP TABLE` before they execute.

**2. Prompt — Let the LLM decide**

For subjective decisions a script can't handle. Claude evaluates context with a prompt in a single pass.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "prompt",
        "prompt": "Check that the code follows the project style guide. Block if it introduces console.log statements in production code. $ARGUMENTS"
      }]
    }]
  }
}
```

**3. Agent — Subagent with tools**

For complex verification. Spawns a subagent with access to Read, Grep, and Glob that can inspect files before deciding.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "agent",
        "prompt": "Verify that every new function has a corresponding test file. Check the test directory for matching test files. Block if tests are missing. $ARGUMENTS"
      }]
    }]
  }
}
```

## Quick reference

| Event | When it fires | Typical use |
|---|---|---|
| `PreToolUse` | Before a tool runs | Block dangerous actions |
| `PostToolUse` | After a successful tool | Format, lint, type-check |
| `Notification` | When Claude sends a notification | Custom desktop alerts |
| `Stop` | When Claude finishes its response | Final validation, auto-commit |
| `PreCompact` | Before context compression | Re-inject critical instructions |
| `SessionStart` | When a session begins | Environment setup |

| Type | AI involved | Best for |
|---|---|---|
| `command` | No | Binary validations (pass/fail) |
| `prompt` | Yes (single pass) | Subjective decisions |
| `agent` | Yes (multi-turn) | Complex verification with tools |

## Configuration

Hooks are defined in `settings.json`. Three scope levels:

- `~/.claude/settings.json` — All projects
- `.claude/settings.json` — Project-level (shareable with the team)
- `.claude/settings.local.json` — Project-level (private)

The fastest way to create one: type `/hooks` inside Claude Code.

**Related:** [The 6 extension mechanisms](/en/tips/claude-code-skills-hooks-mcp-plugins-comparison) · [Skills: custom slash commands](/en/tips/claude-code-skills-custom-slash-commands) · [Permissions system](/en/tips/claude-code-permissions-3-key-concepts)

> Official docs: [Hooks](https://code.claude.com/docs/en/hooks) · [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
