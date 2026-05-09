---
date: 2026-05-08
type: tip
title_es: "/doctor en Claude Code: deja de buscar tu error en Reddit"
title_en: "/doctor in Claude Code: stop searching for your error on Reddit"
---

> **TL;DR** Run `/doctor` inside Claude Code. It audits **installation, settings, MCP servers, and context usage** in one pass. Each check comes back green, yellow, or red. Press `f` and Claude fixes the reported issues for you. If Claude won't even start: run `claude doctor` from your shell.

Something feels off in Claude Code: search isn't finding files, an MCP won't connect, responses are getting slow, a skill that worked yesterday is gone today. The typical reaction: open Reddit, search the symptom, lose 40 minutes in dead-end threads. The reaction almost no one has: run `/doctor` and let Claude audit itself.

## How it works internally

`/doctor` runs a battery of checks in parallel and returns a report with **status icons**:

- 🟢 green — passes
- 🟡 yellow — warning (not optimal, but works)
- 🔴 red — error (this is broken)

And the piece few people know: after the report, **press `f` and Claude fixes the reported issues** without you having to copy-paste a fix from anywhere.

If Claude won't start at all and you can't run slash commands, there's a shell version: `claude doctor` from your terminal gives you the same report from outside the CLI.

## Result preview

```
> /doctor

Running diagnostics...

🟢 Installation       npm global · Claude Code v2.1.119
🟢 Settings           ~/.claude/settings.json valid
🟢 API connectivity   reachable, auth OK
🟡 Context usage      72% — consider /compact
🔴 MCP: github        connection refused (port 3000)
🟢 ripgrep            built-in OK
🟢 Skills             14 loaded

1 error · 1 warning · 5 OK

Press [f] to have Claude fix the reported issues, or [Enter] to dismiss.
```

You press `f`. Claude detects the GitHub MCP is pointing at an unexposed port, reads your `~/.claude/mcp.json`, proposes the fix, applies it, retries the connect. Green.

## When to run it

### **1. When something feels off**

Before Reddit, before Stack Overflow. It's the first step. If something comes back red, you know where to look. If everything's green, the problem isn't in your setup — it's something further upstream.

### **2. After install or upgrade**

You just installed Claude Code or ran `claude update`. Run `/doctor` to verify everything came out clean before you start working and hit an error 20 minutes in.

### **3. After switching install methods**

You migrated from npm to native installer, or between Pro and Bedrock. Bits of the previous configuration are still around. `/doctor` detects them.

### **4. When Claude won't start**

When you can't even get into a session, the shell version:

```bash
claude doctor
```

Same report, outside the CLI. Useful when the binary is broken or `PATH` can't find it.

## What it detects

| Category | What it checks |
|---|---|
| **Installation** | Type (npm global / native / local), version, binary integrity |
| **Settings** | `~/.claude/settings.json` valid, no invalid keys |
| **API connectivity** | Reaches the endpoint, auth works, no 5xx |
| **MCP servers** | Each configured server responds |
| **Skills** | Skills in your directory load without errors |
| **Context usage** | % of the context window used — suggests `/compact` if high |
| **ripgrep** | The bundled one works, or you need the system package |
| **PATH** | The `claude` binary is reachable |

## Reference

| Aspect | Detail |
|---|---|
| Inside the CLI | `/doctor` |
| Shell version | `claude doctor` |
| Fix key | `f` (after the report) |
| Status icons | 🟢 OK · 🟡 warning · 🔴 error |
| Coverage | Install, settings, API, MCP, skills, context, ripgrep, PATH |
| Average time | ~30 seconds |

> Official docs: [Troubleshooting — Claude Code Docs](https://code.claude.com/docs/en/troubleshooting)
