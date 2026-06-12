---
date: 2026-06-12
type: tip
title_es: "MCP en Claude Code: conecta 20 servidores sin comerte el contexto"
title_en: "MCP in Claude Code: connect 20 servers without eating your context"
---

> **TL;DR** Your MCP tools **no longer load at session start**: they're deferred, and Claude looks them up with an internal tool (`ToolSearch`) only when it needs them. At launch, only tool names and one instruction per server enter context. It's the same trick you already know from skills, applied to MCP. It's on by default, and you tune it with `ENABLE_TOOL_SEARCH` if you want different behavior.

For months the rule was [five servers is enough, fifty just slows the agent down](/en/tips/claude-code-best-mcp-servers): every MCP dumped the full definitions of all its tools into context at startup, and connecting GitHub + Notion + Chrome DevTools cost you tens of thousands of tokens before you typed your first word. Tool Search quietly changed that math, and almost nobody noticed because, from the outside, everything works the same.

## The trick you already know (from skills)

[Skills](/en/tips/claude-code-skills-custom-slash-commands) have always worked this way: only the name and a one-line description live in context; the full body loads when invoked. Progressive disclosure: a cheap index always visible, expensive content only when needed.

Tool Search applies that same pattern to your MCPs, and the docs make the comparison outright: *"server instructions help Claude understand when to search for your tools, similar to how skills work."*

| | Skills | MCP tools (with Tool Search) |
|---|---|---|
| Always in context | name + description | tool names + server instructions |
| Loaded on demand | the SKILL.md body | the full schema, via `ToolSearch` |

## How it works

At session start, only the tool **names** and each server's **instructions** (truncated at 2KB) enter context. When Claude needs a specific tool, it calls `ToolSearch` (keyword search works, no exact name needed), the full schema enters context at that moment, and it uses the tool. Only the tools that actually get used cost context.

I see it daily: in the session where I'm writing this, there are about 90 deferred tool names (Notion, Canva, Chrome DevTools...) and Claude only loaded the schemas of the three it touched to publish. Before, all 90 schemas would have entered whole at startup.

Check it yourself with [`/context`](/en/tips/claude-code-context-command-token-usage): the MCP tools category that used to dominate the window is now a fraction.

## The knobs

It's on by default. To change the behavior, the `ENABLE_TOOL_SEARCH` variable (in your settings `env` block or at launch):

| Value | What it does |
|---|---|
| *(unset)* | Everything deferred, discovered on demand. The default |
| `auto` | Hybrid: if all tools fit within 10% of context, they load upfront; the overflow is deferred |
| `auto:N` | Same, with a custom threshold (0-100), e.g. `auto:5` |
| `false` | The old behavior: everything upfront, no deferral |
| `true` | Forces deferral even on Vertex or behind a proxy |

And per server: if one should always be visible without a search step (because you use it every turn), exempt it with `alwaysLoad` in its configuration:

```json
{
  "mcpServers": {
    "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/", "alwaysLoad": true }
  }
}
```

## The fine print

- **Haiku doesn't support it** (requires models with `tool_reference`).
- **Disabled by default on Vertex AI** (supported from Sonnet 4.5 and Opus 4.5; force it with `ENABLE_TOOL_SEARCH=true`).
- **It switches itself off** if your `ANTHROPIC_BASE_URL` points to a non-first-party proxy.
- If you publish your own MCP server, the **server instructions** are now your storefront: write them like a skill's `description` (what tasks your tools cover and when to search for them).

## So is the rule of five dead?

The context half of [that rule](/en/tips/claude-code-best-mcp-servers), yes. But curation still wins for two other reasons: every connected server still adds its names and instructions, and a giant menu of options still costs per-turn decisions. Connect the ones you use; the price of getting it wrong is just much lower now. [Cache](/en/tips/claude-code-prompt-caching-slow-expensive-turns) bonus: with tools deferred, connecting or disconnecting a server mid-session no longer invalidates the prefix.

> Official docs: [Scale with MCP Tool Search](https://code.claude.com/docs/en/mcp)

## Requirements

On by default on the Anthropic API with Sonnet and Opus. See the fine print for Haiku, Vertex AI, and proxies.
