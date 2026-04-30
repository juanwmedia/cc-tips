---
date: 2026-03-11
type: tip
title_es: "Pregunta mientras Claude Code trabaja con /btw"
title_en: "Ask Questions While Claude Code Is Working with /btw"
---
# Quick Tip: Ask Questions While Claude Code Is Working with /btw

> **TL;DR** Type `/btw` followed by your question to get a quick answer without interrupting the current task. It doesn't get added to the history, has no tool access, and reuses the prompt cache (minimal cost).

Claude Code now has a command for side questions: `/btw`. When Claude is in the middle of a task — editing files, running tests, exploring the codebase — you can fire a quick question without interrupting its work or polluting the conversation history.

`/btw` is the inverse of a [subagent](/en/writing/claude-code-subagents-guide-ai): it sees your full conversation but has no tools. A subagent has full tools but starts with an empty context. Use `/btw` to ask about what Claude already knows; use a subagent to go find out something new.

The question and answer appear in an overlay. When you dismiss it, they vanish. The main context stays clean, Claude keeps working, and you have your answer.

Result:

```
> /btw what was the name of that config file we read earlier?

┌─────────────────────────────────────────────┐
│ The file was src/config/database.ts,        │
│ we read it when analyzing the Redis setup.  │
└─────────────────────────────────────────────┘

Press Space, Enter, or Escape to dismiss
```

## How to use it

### **1. While Claude is working**

When Claude is processing a response (you see the active spinner), type:

```
/btw what pattern are we using for error handlers?
```

The question runs independently. Claude doesn't stop what it's doing.

### **2. Between turns**

It also works when Claude is idle. Useful for quick lookups that don't warrant a full turn or adding noise to the context:

```
/btw which branch are we on?
```

### **3. Reference previous work**

`/btw` has full visibility into the current conversation. You can ask about code Claude already read, decisions it made, or anything in context:

```
/btw why did we choose SQLite over Postgres?
```

## Reference

| Aspect | Detail |
|---|---|
| Command | `/btw <question>` |
| Tool access | None — only answers from what's already in context |
| History | Not added to the main conversation |
| Follow-ups | None — one question, one answer |
| Availability | Works while Claude is processing or between turns |
| Cost | Minimal — reuses the parent conversation's prompt cache |
| Dismiss | `Space`, `Enter`, or `Escape` |

> Official docs: [Interactive mode — Side questions](https://code.claude.com/docs/en/interactive-mode#side-questions-with-btw)
