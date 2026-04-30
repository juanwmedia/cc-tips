---
date: 2026-02-21
type: tip
title_es: "Monitoriza el Uso de Tokens con el Comando /context"
title_en: "Monitor Token Usage with the /context Command"
---
# Quick Tip: Monitor Token Usage with the /context Command

Claude Code operates within a 200k token context window. Everything Claude needs to function — system prompt, tools, MCP servers, agents, memory files, skills, and your conversation — competes for that space. The `/context` command breaks down exactly how many tokens each component consumes, giving you full visibility into a resource that drains silently.

It's easy to overlook at first. You start adding MCP servers, custom agents, rules... and before you know it, a significant chunk of the context window is already pre-consumed before you type your first message. `/context` keeps you aware.

Result:

```
/context

Context Usage
claude-opus-4-5-20251101 · 51k/200k tokens (26%)

Estimated usage by category
  System prompt:     2.6k tokens  (1.3%)
  System tools:     17.6k tokens  (8.8%)
  MCP tools:          907 tokens  (0.5%)
  Custom agents:      935 tokens  (0.5%)
  Memory files:       302 tokens  (0.2%)
  Skills:              61 tokens  (0.0%)
  Messages:         30.5k tokens (15.3%)
  Free space:        114k        (57.0%)
  Autocompact buffer: 33k tokens (16.5%)
```

## Setup

No setup needed. The command is available in any session.

**1. Run the command**

Type `/context` at any point during your session:

```bash
/context
```

**2. Analyze the breakdown**

The output shows consumption per category. Pay close attention to:

- **System tools** and **MCP tools**: tool definitions load on every request. A few MCP servers can consume a significant percentage.
- **Free space**: your actual working space. This is what's left for messages, file reads, and command outputs.
- **Autocompact buffer**: a reserve Claude uses for automatic compaction when context fills up.

**3. Act on what you see**

If MCP tools consume too much, run `/mcp` to see per-server costs and disable those you don't need in this session. If free space drops below 30%, consider using `/compact` or starting a fresh session.

## Reference

| Category | What it includes |
|---|---|
| System prompt | Claude Code's internal instructions |
| System tools | Built-in tools (Read, Edit, Bash, Grep, Glob, etc.) |
| MCP tools | Tool definitions from connected MCP servers |
| Custom agents | Custom agents defined in `.claude/agents/` |
| Memory files | CLAUDE.md and auto memory files |
| Skills | Descriptions of registered skills |
| Messages | Your conversation: prompts, responses, and tool results |
| Free space | Tokens available to keep working |
| Autocompact buffer | Reserve for automatic compaction (~16.5%) |

> Official docs: [The context window](https://code.claude.com/docs/en/how-claude-code-works#the-context-window)
