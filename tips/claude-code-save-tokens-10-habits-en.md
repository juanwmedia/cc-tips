---
date: 2026-04-08
type: tip
title_es: "Cómo ahorrar tokens en Claude Code: 10 hábitos de la documentación oficial"
title_en: "How to Save Tokens in Claude Code: 10 Habits From the Official Docs"
---
# Quick Tip: How to Save Tokens in Claude Code: 10 Habits From the Official Docs

> **TL;DR** If your Claude Code session is running out faster than it used to — it's not just you. Real complaints all over the place. But part of the fix is on you. Anthropic has a full page in the docs (*"Manage costs effectively"*) with 10 verifiable habits. Here are all 10, with the exact docs citation when relevant.

The funny thing about these 10 habits: none of them is esoteric. They're common sense. And precisely because they're common sense, they're the first ones you skip — when something is obvious, you dismiss it as "I already know that" before applying it.

## The 10 habits

### **1. Monitor where your tokens go**

`/context` breaks down each category: system prompt, MCP tools, messages, free space. If you don't check it periodically, you're driving blind. Dedicated tip: [/context to monitor token usage](/en/tips/claude-code-context-command-token-usage).

### **2. Clean between tasks**

`/clear` when switching tasks. Before that, `/rename` so you can find the session later with `/resume`.

> *"Stale context wastes tokens on every subsequent message."*

### **3. Compact with explicit instructions**

`/compact` is not just "summarize". You can tell Claude exactly what to preserve:

```bash
/compact Focus on code samples and API usage
```

You can also drop the instructions into `CLAUDE.md` under `# Compact instructions`.

### **4. Sonnet by default. Opus only for architecture**

`/model` to switch on the fly. Simple subagents with `model: haiku` in their config.

> *"Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning."*

Dedicated tip: [How to choose the right model in Claude Code](/en/tips/claude-code-choose-right-model).

### **5. Disable unused MCP servers, prefer native CLI tools**

`/mcp` to see and disable servers. Each active server still leaves its *tool names* in context even though the definitions are deferred. Prefer `gh`, `aws`, `gcloud`, `sentry-cli` over MCP servers — CLI tools don't even add the listing.

### **6. Preprocess verbose output with hooks**

A `PreToolUse` hook intercepts the command before it runs and can rewrite it via `updatedInput`. It turns 10,000 lines of test output into the 50 that matter. Claude only sees the filtered output. Dedicated tip: [Hooks in Claude Code: automate your workflow](/en/tips/claude-code-hooks-automate-workflow).

### **7. Move instructions from CLAUDE.md to Skills**

`CLAUDE.md` is loaded at session start. Those tokens are in your context from the first turn to the last. Skills load **on-demand** only when invoked. Move everything workflow-specific into a Skill. Docs target: keep `CLAUDE.md` under 200 lines.

### **8. Lower the thinking budget on simple tasks**

Thinking tokens are billed as output, and the default budget can be tens of thousands of tokens per request. `/effort low` when you don't need deep reasoning, or `MAX_THINKING_TOKENS=8000` from the environment to cap the global budget. Dedicated tip: [How to adjust the effort level in Claude Code](/en/tips/claude-code-effort-level-adjust-reasoning).

### **9. Delegate verbose operations to subagents**

`npm test`, `gh pr view`, processing logs: all of that burns context in your main conversation. Delegated to a subagent, the verbose output stays in its context — only the summary comes back. Watch out for the gotchas though: [subagents lose context](/en/tips/claude-code-subagent-context-loss).

> *"the verbose output stays in the subagent's context while only a summary returns to your main conversation."*

### **10. Plan mode before implementing**

`Shift+Tab` enters plan mode. Claude explores the codebase and proposes an approach **before** touching anything. If the initial direction is wrong, you find out in plan mode (cheap) instead of mid-implementation (expensive, with re-work).

> *"preventing expensive re-work when the initial direction is wrong."*

## Why it matters right now

There's a growing volume of complaints about sessions running out faster. The structural side you don't control — but the habits side you do. And the official docs tell you exactly how to fix it in 10 concrete points.

None of these is magic. They're all common sense. And precisely because they're common sense, they're the first ones you skip.

> Official docs: [Manage costs effectively](https://code.claude.com/docs/en/costs) · See also: [/context](/en/tips/claude-code-context-command-token-usage) · [1M context window](/en/tips/claude-code-1m-context-window-tips) · [When features load into context](/en/tips/claude-code-when-features-load-context)
