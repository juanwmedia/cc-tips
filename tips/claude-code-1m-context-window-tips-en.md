---
date: 2026-03-16
type: tip
title_es: "Claude Code ahora tiene 1M de tokens de contexto — y no deberías llenarlos"
title_en: "Claude Code Now Has 1M Tokens of Context — and You Shouldn't Fill Them"
---
# Quick Tip: Claude Code Now Has 1M Tokens of Context — and You Shouldn't Fill Them

> **TL;DR** Opus 4.6 includes 1 million context tokens by default on Max, Team, and Enterprise plans — 5x more than before, at no extra cost. But more context doesn't mean better results. Monitor with [`/context`](/en/tips/claude-code-context-command-token-usage), compact proactively, and don't let the session degrade.

Since version 2.1.75, Claude Code uses [Opus 4.6](/en/tips/claude-code-choose-right-model) with 1M tokens as the default model. The context window jumped from 200K to 1M — 5x more space before Claude needs to compact. This means longer sessions, fewer interruptions, and the ability to work with entire monorepos without fragmenting context.

But there's a catch: model performance degrades with distant tokens. This is known as context drift — the further information sits from the current point in the conversation, the less accurately the model retrieves it. Just because you can fill 1M tokens doesn't mean you should.

## Who has access

| Plan | Opus 4.6 1M | Sonnet 4.6 1M |
|---|---|---|
| Max, Team, Enterprise | Included | Requires extra usage |
| Pro | Requires extra usage | Requires extra usage |
| API (pay-as-you-go) | Full access | Full access |

No surcharge — the per-token price is the same across the entire window. On plans where it's included, it doesn't consume additional credits.

Pro doesn't have it included yet, but Anthropic's pattern with premium features is clear: Enterprise/Max first, then it trickles down.

## How to use it without wasting context

### **1. Monitor with [/context](/en/tips/claude-code-context-command-token-usage)**

Use the `/context` command to see how much context you're consuming in real time. Don't wait for Claude to auto-compact — get ahead of it.

### **2. Compact before Claude does**

Auto-compaction triggers at ~95% capacity. By that point, you've already lost precision on older tokens. Compact proactively:

```
/compact focus on the authentication module
```

The optional instructions tell Claude what to prioritize when summarizing.

### **3. Don't load context you don't need**

Having 1M doesn't mean you should dump the entire codebase. Load selectively — specific directories, relevant files. Claude [reads on demand](/en/tips/claude-code-when-features-load-context); you don't need to pre-load everything.

### **4. Select the 1M model explicitly**

If it's not active, select it manually:

```
/model opus[1m]
/model sonnet[1m]
```

Or when launching Claude Code:

```bash
claude --model opus[1m]
```

### **5. Control when compaction triggers**

If you want compaction before 95%, adjust the threshold:

```bash
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70
```

## Reference

| Aspect | Detail |
|---|---|
| Previous context | 200K tokens |
| Current context | 1M tokens (5x) |
| 1M model | Opus 4.6 (included on Max/Team/Enterprise) |
| Model aliases | `opus[1m]`, `sonnet[1m]` |
| Auto-compaction | ~95% by default, adjustable with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` |
| Disable 1M | `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` |
| Per-token price | No surcharge — same price across the entire window |

> Official docs: [Model configuration — Extended context](https://code.claude.com/docs/en/model-config#extended-context)
