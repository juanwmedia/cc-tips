---
date: 2026-05-16
type: tip
title_es: "Claude Agent SDK: Claude Code, pero llamado desde tu código"
title_en: "Claude Agent SDK: Claude Code, but called from your code"
---

> **TL;DR** `pip install claude-agent-sdk` (or `npm install @anthropic-ai/claude-agent-sdk`), import `query`, pass a prompt and the list of allowed tools, and you get the same agent that runs in your terminal — programmable. CI/CD, cron, API, whatever. Under the hood: the agent loop, the built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch...), the skills in `~/.claude/`, hooks, subagents, MCP, sessions with resume/fork. **It's not the Client SDK** (where you implement the tool loop yourself). It's the full agent running in your process. The important note: **starting June 15, 2026**, SDK usage on subscription plans draws from a new **monthly Agent SDK credit**, separate from your interactive usage limits.

If you've been using Claude Code in the terminal for a while, here's the confusion saver: **Claude Agent SDK** and **Claude Code SDK** are the same SDK. Anthropic renamed it during 2026 — Google's PAA is still full of people asking *"What is the difference between Claude Code and Claude Agent SDK?"*. The real difference is the interface: in your terminal you call `claude`, in your code you call it as a library.

Under the hood it's the **same agent loop** that runs when you type `claude` in your terminal: reads files, runs commands, edits code, manages context. The library exposes the primitives you already know (skills, hooks, subagents, MCP, permissions) as arguments to the `query` function.

## Hello world

Python, with Read + Edit + Bash allowed:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)  # Claude reads the file, finds the bug, edits it

asyncio.run(main())
```

TypeScript equivalent:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.ts",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

That's it. You don't implement the tool loop. You don't serialize tool_use or tool_result. Claude handles all of it inside the library.

## Setup

**1. Install the SDK.**

```bash
pip install claude-agent-sdk                      # Python
npm install @anthropic-ai/claude-agent-sdk        # TypeScript
```

> The TypeScript SDK bundles a native Claude Code binary, so you don't need to install Claude Code separately.

**2. Configure your API key.**

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Other supported auth providers: Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google Vertex AI (`CLAUDE_CODE_USE_VERTEX=1`), Azure AI Foundry (`CLAUDE_CODE_USE_FOUNDRY=1`), Claude Platform on AWS (`CLAUDE_CODE_USE_ANTHROPIC_AWS=1`).

## Claude Code (CLI) vs Agent SDK: when to use which

Same capabilities, different surface. Anthropic's own table:

| Use case | Best choice |
|---|---|
| Interactive local development | CLI |
| CI/CD pipelines | SDK |
| Custom applications | SDK |
| One-off tasks | CLI |
| Production automation | SDK |

> *"Many teams use both: CLI for daily development, SDK for production."* — docs.

## What you can plug in (same as local)

| Primitive | How to pass it to `query` | For |
|---|---|---|
| **Built-in tools** | `allowed_tools=["Read", "Edit", "Bash", ...]` | Restrict what the agent can touch |
| **[Hooks](/en/tips/claude-code-hooks-automate-workflow)** | `hooks={"PostToolUse": [...]}` | Validate, log, block, or transform agent actions |
| **[Subagents](/en/tips/claude-code-create-custom-agents)** | `agents={"code-reviewer": AgentDefinition(...)}` | Spawn specialized agents with scoped tools |
| **[MCP servers](/en/tips/claude-code-mcp-quick-setup)** | `mcp_servers={"playwright": {...}}` | Connect databases, browsers, external APIs |
| **[Permissions](/en/tips/claude-code-permissions-3-key-concepts)** | `allowed_tools` + `permission_mode` | Granular allow / ask / deny |
| **[Sessions](/en/tips/claude-code-session-recap-resume-context)** | `resume=session_id` | Resume conversations (forkable too) |
| **[Skills](/en/tips/claude-code-skills-custom-slash-commands)** | Auto-loaded from `.claude/skills/*/SKILL.md` | Reuse your custom commands |
| **CLAUDE.md** | Auto-loaded from cwd | Same instructions as local |

Skills, slash commands and `CLAUDE.md` load by default from `.claude/` and `~/.claude/`. To restrict sources, pass `setting_sources` in your options.

## The SDK ≠ Client SDK

The classic mix-up. The [Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks) gives you direct API access: you send prompts and **you implement the tool loop**. The Agent SDK ships with it built-in:

```python
# Client SDK — you write the loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK — Claude handles tools
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

If you find yourself writing `while response.stop_reason == "tool_use"`, you're in the wrong SDK.

## Cost note — starting June 15, 2026

Anthropic introduces a **monthly Agent SDK credit** on subscription plans, separate from interactive Claude Code usage. SDK calls (and `claude -p`, the headless mode) count against that credit, not against your interactive limits. Official detail in the [pricing notice](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan).

Before June 15, all SDK usage counts as regular API (tokens billed to your account).

## Pairs well with

- [GitHub Actions](/en/tips/claude-code-github-actions-pr-review) — the `@claude` PR-review action runs on top of the Agent SDK. Knowing this lets you extend it.
- [Subagents](/en/tips/claude-code-create-custom-agents) — the pattern you already used locally, now via `agents={}`.
- [Plugins](/en/tips/claude-code-plugin-marketplace-distribution) — loadable programmatically via the `plugins` option.
- [Slash commands cheat sheet](/en/tips/claude-code-slash-commands-cheat-sheet) — everything you invoke with `/` is also invokable from the SDK.

> Official docs: [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Python SDK](https://code.claude.com/docs/en/agent-sdk/python) · [TypeScript SDK](https://code.claude.com/docs/en/agent-sdk/typescript)
