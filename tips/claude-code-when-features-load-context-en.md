---
date: 2026-02-27
type: tip
title_es: "Cuándo se carga cada feature en el contexto (y lo que cuesta)"
title_en: "When Each Feature Loads Into Context (and What It Costs)"
---

# Quick Tip: When Each Feature Loads Into Context (and What It Costs)

> **TL;DR** CLAUDE.md and MCP servers load at session start and consume context on every request. Skills load only descriptions initially (full content on use). Subagents run in isolated context. Hooks execute externally at zero cost. Knowing this lets you design a setup that saves tokens from the start.

The `/context` command shows what's consuming your context right now. But there's a step before that: understanding *when* each feature loads. Not everything costs the same or loads at the same time. Some features take up context the moment you start a session, others only when you use them, and others don't touch your context window at all. That distinction is the difference between an efficient setup and one that burns through tokens before you type your first prompt.

Result:

```
  Session start          On use            Isolated
┌──────────────────────────────────┐
│         Context window           │
│                                  │
│  CLAUDE.md            Skills     │   ┌──────────────┐
│  Full content,        Full       │   │ Separate ctx │
│  every request        content    │   │              │
│                       on use     │   │  Subagents   │
│  MCP servers                     │   │  Fresh,      │
│  Tool definitions,               │   │  isolated    │
│  every request                   │   └──────────────┘
│                                  │
│  Skills*                         │   Hooks
│  Descriptions only              │   Run externally,
│  (default)                       │   zero cost
└──────────────────────────────────┘

■ Always in context  ■ Loads on use  □ Outside main context
```

*Skills with `disable-model-invocation: true` load nothing until you invoke them.

## The 3 loading phases

### 1. Session start (always in context)

These load when Claude Code starts and stay in every request:

- **CLAUDE.md**: full content from all levels (managed, user, project). Files from your working directory upward load at launch; subdirectories are discovered as you access them.
- **MCP servers**: all tool definitions and JSON schemas. With Tool Search enabled (default), tools load up to 10% of context and the rest is deferred.
- **Skills**: names and descriptions only (~100 tokens per skill). Full content doesn't load yet.

```bash
# See what's consuming context right now
/context
```

### 2. On use (demand-loaded)

Skills load their full content when you invoke them with `/<name>` or Claude determines they're relevant. Until then, they only consume their description tokens.

```bash
# Triggers full skill content loading into context
/deploy
```

Skills with `disable-model-invocation: true` load absolutely nothing until you invoke them manually. Zero cost by default — use this for skills with side effects or that you only trigger yourself.

### 3. Isolated (outside main context)

Subagents work in their own context window. They don't inherit your conversation history or invoked skills — only CLAUDE.md, their specified skills, and whatever the lead agent passes. Hooks execute as external shell scripts without touching context at all.

## Reference

| Feature | When it loads | What loads | Context cost |
|---|---|---|---|
| CLAUDE.md | Session start | Full content | Every request |
| MCP servers | Session start | Tool definitions + schemas | Every request* |
| Skills | Start + on use | Descriptions at start, full content on use | Low until invoked** |
| Subagents | When spawned | Fresh context + specified skills | Isolated |
| Hooks | On trigger | Nothing (external execution) | Zero |

*With Tool Search enabled, tools beyond 10% of context are deferred until needed.
**Skills with `disable-model-invocation: true` have zero cost until invoked.

**Related:** [Monitor your context with /context](/en/tips/claude-code-context-command-token-usage) · [The 6 ways to extend Claude Code](/en/tips/claude-code-skills-hooks-mcp-plugins-comparison)

> Official docs: [Extend Claude Code](https://code.claude.com/docs/en/features-overview#understand-how-features-load)
