---
date: 2026-03-10
type: tip
title_es: "Crea agentes personalizados en Claude Code con --agent"
title_en: "Create Custom Agents in Claude Code with --agent"
---
# Quick Tip: Create Custom Agents in Claude Code with --agent

Claude Code lets you create specialized agents as Markdown files with YAML frontmatter. Each agent has its own system prompt, restricted tools, and model. When you launch a session with `claude --agent <name>`, the entire conversation transforms — it's not a delegated [subagent](/en/writing/claude-code-subagents-guide-ai), it's your main session operating with a different persona and rules.

Think of it as having multiple versions of Claude Code, each one tailored for a specific role: reviewer, debugger, deployer, or whatever you need.

> **TL;DR** Create a `.md` file in `~/.claude/agents/`, define the role in YAML frontmatter, and launch with `claude --agent name`. Your entire session becomes that specialized agent.

Result — a ready-to-use code review agent:

```markdown
# ~/.claude/agents/reviewer.md
---
name: reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Glob, Grep, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Provide feedback organized by priority:
   - Critical (must fix)
   - Warnings (should fix)
   - Suggestions (consider improving)

Include specific examples of how to fix each issue.
```

## Setup

### **1. Create the agent file**

Create a `.md` file in one of these locations:

```bash
# Global — available across all your projects
~/.claude/agents/reviewer.md

# Project — shared with your team via git
.claude/agents/reviewer.md
```

### **2. Launch the session as the agent**

```bash
claude --agent reviewer
```

Claude Code starts with the system prompt, tools, and model you defined. You won't see the default prompt — you're inside the agent.

### **3. Use the interactive wizard**

If you'd rather not write the file manually:

```bash
claude
# Inside the session:
/agents
```

Select "Create new agent", choose the scope (user or project), and Claude guides you step by step — it can even generate the system prompt for you.

### **4. Define ephemeral agents from the CLI (optional)**

To test without creating a file, use `--agents` (plural) with inline JSON:

```bash
claude --agents '{
  "reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer. Focus on quality and security.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Note: `--agent` (singular) transforms your main session into an existing agent. `--agents` (plural) defines ephemeral subagents that Claude can delegate to during the session.

## Reference

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique identifier (lowercase letters and hyphens) |
| `description` | Yes | When this agent should be used |
| `tools` | No | Allowed tools. Inherits all if omitted |
| `disallowedTools` | No | Tools explicitly denied |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `plan`, `bypassPermissions` |
| `hooks` | No | Agent lifecycle [hooks](/en/writing/claude-code-hooks-practical-guide) |
| `memory` | No | `user`, `project`, or `local` — persistent memory across sessions |
| `skills` | No | [Skills](/en/writing/claude-code-skills-custom-workflows) preloaded into the agent's context |
| `mcpServers` | No | MCP servers available to the agent |

| Location | Scope | Priority |
|---|---|---|
| `--agents` (CLI flag) | Current session | 1 (highest) |
| `.claude/agents/` | Project | 2 |
| `~/.claude/agents/` | Global (personal) | 3 |
| Plugin's `agents/` directory | Where plugin is enabled | 4 (lowest) |

> Official docs: [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
