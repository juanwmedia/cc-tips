---
date: 2026-03-17
type: tip
title_es: "Controla Claude Code desde tu Móvil"
title_en: "Control Claude Code from Your Phone"
---
Remote Control connects your local Claude Code session to [claude.ai/code](https://claude.ai/code) or the Claude app for iOS and Android. The process stays on your machine — your phone is just a window into that session. Start a task on your laptop terminal, walk out the door, and keep giving Claude instructions from the bus. That simple.

> **TL;DR** `claude --rc` or `/rc` in an active session. Scan the QR code with your phone. Keep working from anywhere. The original terminal must stay open.

Result:

```
> claude --rc "Refactor API"
Remote Control session started

Session URL: https://claude.ai/code/session/abc123
Press spacebar to show QR code

╭──────────────────────────────────────╮
│ Remote Control: Refactor API         │
│ Status: Online                       │
│ Connected devices: 1                 │
╰──────────────────────────────────────╯
```

## How to use it

### **1. New session with Remote Control**

```bash
# Interactive session with remote access
claude --rc

# With a custom name
claude --rc "Refactor API"
```

Opens a normal terminal session that's also accessible from your phone or any browser.

### **2. Enable on an existing session**

If you're already working with Claude:

```
/rc
```

Carries over your full conversation. Shows URL and QR code to connect.

### **3. Server mode**

```bash
# No local interaction, only serves remote connections
claude remote-control --name "Backend" --spawn worktree
```

In server mode, each remote connection can spin up its own worktree (requires a git repository). Supports up to 32 concurrent sessions.

### **4. Connect from another device**

- **QR code**: in server mode, press spacebar to show the QR. With `/rc`, it appears automatically. Scan with your phone
- **Direct URL**: copy the session URL into any browser
- **Session list**: find it by name in [claude.ai/code](https://claude.ai/code) or the Claude app (computer icon with green dot = online)

### **5. What you need to know**

The original terminal **must stay open**. If you close it or stop the process, the session ends. If your laptop sleeps, the session reconnects automatically when it wakes up — but if it loses network for more than ~10 minutes while awake, the session times out and the process exits. You'll need to run the command again.

## Reference

| Command | What it does |
|---|---|
| `claude --rc` | Interactive session + Remote Control |
| `/rc` | Enable Remote Control on an existing session |
| `claude remote-control` | Server mode (remote connections only) |
| `--name "Name"` | Visible name in the session list (server mode) |
| `--spawn worktree` | Each remote session in its own worktree (server mode) |
| `--capacity <N>` | Max concurrent sessions, default: 32 (server mode) |

| Detail | Value |
|---|---|
| Original terminal | Must stay open |
| Laptop sleep | Auto-reconnects on wake |
| Timeout | ~10 min without network (while awake). Process exits. |
| Security | Outbound HTTPS only, no open ports |
| Sync | Bidirectional — terminal, browser, and phone in parallel |
| Plans | All plans. Team/Enterprise admins must enable Claude Code first. |
| Min version | v2.1.51+ |

> Official docs: [Remote Control](https://code.claude.com/docs/en/remote-control)

## Requirements

- Available on all plans (API keys not supported). Team and Enterprise admins must enable Claude Code in [admin settings](https://claude.ai/admin-settings/claude-code).
- Claude Code v2.1.51 or later
- Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) (optional — also works from any browser)
