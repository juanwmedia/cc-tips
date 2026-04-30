---
date: 2026-03-28
type: tip
title_es: "Por qué tus subagentes devuelven resultados incompletos en Claude Code"
title_en: "Why Your Sub-Agents Return Incomplete Results in Claude Code"
---
# Quick Tip: Why Your Sub-Agents Return Incomplete Results in Claude Code

> **TL;DR** Sub-agents start with zero context — they don't inherit your conversation. They only receive the query Claude writes for them. If that query doesn't include the real objective, the summary they return will be incomplete. The fix: include the why in delegation, preload context with skills, and ask for follow-ups so Claude resumes the same sub-agent without losing the thread.

When Claude Code delegates a task to a sub-agent, that sub-agent starts from scratch. Its own context window, its own system prompt, its own CLAUDE.md loading. It inherits nothing from your conversation. It only receives a query that Claude writes based on what you asked.

The problem: that query is literal, not semantic. If you ask "investigate how the auth middleware works", the sub-agent reads files, summarizes functions and imports, and returns a summary. But it doesn't tell you about the edge case with expired tokens — because it doesn't know you're refactoring due to a token bug. You had that context. The sub-agent didn't.

The numbers confirm it: a sub-agent can read 6,100 tokens of files and return a 420-token summary. That compression is the whole point — it protects your main context. But it's also where the details that matter get lost.

Result — a sub-agent that drops critical information:

```
# Your main conversation has full context:
# - You're refactoring auth due to an expired token bug
# - The edge case is in refreshToken()
# - You need to know if the current middleware handles it

# Claude delegates to the sub-agent:
> "Investigate how the current auth middleware works"

# The sub-agent returns:
> "The middleware uses express-jwt, validates tokens on every
>  request, and has 3 protected routes. Structure:
>  middleware/auth.js, utils/token.js, routes/protected.js"

# Missing: the refreshToken() edge case — the actual reason for the task
```

## How to fix it

### **1. Include the objective, not just the question**

When delegating to a sub-agent, don't tell it what to investigate. Tell it WHY you're investigating:

```
# Bad — just the literal query:
"Investigate the auth middleware"

# Good — query + objective:
"Investigate the auth middleware. The goal is to refactor it
because there's a bug with expired tokens in refreshToken().
I need to know specifically how expired tokens are handled
and if there are edge cases in the renewal flow."
```

The sub-agent with objective context will prioritize relevant information in its summary.

### **2. Preload context with skills**

If your sub-agent needs context that isn't in the files, preload it in its definition:

```markdown
# .claude/agents/auth-investigator.md
---
name: auth-investigator
description: Investigates auth-related code with security focus.
tools: Read, Grep, Glob
model: sonnet
skills:
  - auth-context
---

You are an auth security investigator. When analyzing auth code:
1. Always check token expiration handling.
2. Look for race conditions in token refresh.
3. Report edge cases explicitly.
```

The `skills` field injects the full content of those skills into the sub-agent's system prompt. It's not a reference — it's direct injection.

### **3. Iterative retrieval — don't accept the first answer**

This approach is known as iterative retrieval — an established pattern in information retrieval (formalized in RAG by Iter-RetGen, EMNLP 2023) that applied to agents means: don't accept the first answer if it's incomplete.

When a sub-agent returns an incomplete summary, don't launch another one from scratch. Ask Claude to dig deeper. Internally, Claude resumes the same sub-agent with all its previous context — it doesn't start a new one:

```
# The sub-agent returned an incomplete summary.
# Tell Claude to dig deeper:

> "The summary doesn't mention how expired tokens are
>  handled. Ask the sub-agent to check refreshToken()
>  in utils/token.js and report the renewal flow."

# Claude resumes the same sub-agent internally.
# The sub-agent picks up with its full history of reads
# and reasoning. No need to re-read files.
```

The key: you talk to Claude in natural language. Claude handles sub-agent resumption under the hood. You don't need to know internal IDs or tools.

### **4. Design focused sub-agents**

A sub-agent that "investigates everything" returns generic summaries. A sub-agent with a specific role knows what to prioritize:

```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security issues, token handling, and auth vulnerabilities.
tools: Read, Grep, Glob
model: sonnet
---

Focus exclusively on:
1. Token validation and expiration.
2. Auth bypass possibilities.
3. Race conditions in session management.
Ignore: styling, formatting, naming conventions.
```

## Reference

| Concept | Detail |
|---|---|
| Context | Independent — does not inherit the main conversation. |
| What it receives | Its own system prompt + Claude's query + CLAUDE.md + skills + configured MCPs. |
| What it returns | Only the final summary text + token/duration metadata. |
| Follow-up | Ask in natural language. Claude resumes the same sub-agent internally. |
| Preload context | `skills` field in definition — injects full content into system prompt. |
| Control tools | `tools` (allowlist) or `disallowedTools` (denylist) in frontmatter. |
| Model | Configurable per sub-agent: `sonnet`, `opus`, `haiku`, or `inherit`. |
| Turn limit | `maxTurns` — limits how many iterations the sub-agent can take. |
| Recursion | Not supported — a sub-agent cannot spawn other sub-agents. |
| Transcripts | `~/.claude/projects/{project}/{session}/subagents/agent-{id}.jsonl` |

> Official docs: [Sub-agents](https://code.claude.com/docs/en/sub-agents)
