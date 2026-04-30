---
date: 2026-03-21
type: tip
title_es: "Controla Claude Code desde Telegram o Discord con Channels"
title_en: "Control Claude Code from Telegram or Discord with Channels"
---
# Quick Tip: Control Claude Code from Telegram or Discord with Channels

> **TL;DR** Claude Code now accepts messages from Telegram and Discord while working in your terminal. Text it from your phone, it executes, and replies through the same channel. Bidirectional, secure (sender allowlist), activated with `--channels`.

Channels is a system that pushes external events into your Claude Code session via an MCP server. Telegram, Discord, or any service you implement. Claude reads the message, acts with all its tools (bash, editing, reading, subagents), and replies through the same channel.

If this sounds like what [OpenClaw](https://openclaw.ai/) does — an AI assistant that lives in your chat apps and executes tasks on your machine — it's no coincidence. Anthropic is building that same vision, but integrated natively into Claude Code: with access to [hooks](/en/writing/claude-code-hooks-practical-guide), [skills](/en/writing/claude-code-skills-custom-workflows), [subagents](/en/writing/claude-code-subagents-guide-ai), and MCP.

Result — you text your Telegram bot:

```
You (Telegram): Are any tests failing in the project?

Claude Code (terminal): runs npm test, analyzes results

Claude Code (Telegram): 2 tests failing in auth.test.ts:
  - testLoginExpiredToken: expected 401, got 500
  - testRefreshToken: timeout after 5s
```

## Setup (Telegram)

### **1. Create a Telegram bot**

Open [BotFather](https://t.me/BotFather) in Telegram, send `/newbot`, give it a name, and copy the token.

### **2. Install the plugin**

```
/plugin install telegram@claude-plugins-official
```

### **3. Configure the token**

```
/telegram:configure <your-token>
```

### **4. Restart with channels enabled**

```bash
claude --channels plugin:telegram@claude-plugins-official
```

### **5. Pair your account**

Send any message to your bot in Telegram. It replies with a pairing code. In Claude Code:

```
/telegram:access pair <code>
/telegram:access policy allowlist
```

The second line locks access to your account only.

## Reference

| Aspect | Detail |
|---|---|
| What it is | MCP server that pushes events into your session |
| Supported channels | Telegram, Discord, fakechat (localhost demo) |
| Direction | Bidirectional — Claude reads and replies through the same channel |
| Security | Sender allowlist + pairing code |
| Activation flag | `--channels plugin:<name>@claude-plugins-official` |
| Session required | Claude Code must be running (not a persistent service) |
| Permissions | Permission prompts pause the session until you approve locally |
| Status | Research preview (v2.1.80+) |
| Authentication | claude.ai login only (no API key or Console) |
| Enterprise | Disabled by default — admin must enable `channelsEnabled` |

> Official docs: [Channels — Push events into a running session](https://code.claude.com/docs/en/channels)

## Requirements

- Claude Code v2.1.80+
- [Bun](https://bun.sh) installed (`bun --version` to verify)
- claude.ai login (API key not supported)
- Team/Enterprise: admin must enable channels in managed settings
