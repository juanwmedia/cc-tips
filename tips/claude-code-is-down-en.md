---
date: 2026-05-18
type: tip
title_es: "Claude Code está caído (o eres tú): cómo saberlo en 30 segundos"
title_en: "Is Claude Code down (or is it you)? How to tell in 30 seconds"
---

> **TL;DR** Three checks in order, 30 seconds each. **1) status.claude.com** — Anthropic publishes Claude Code uptime as a separate component (99.14% over the last 90 days) with Atom/RSS, email, SMS, Slack and webhooks. **2) DownDetector** — if the status page is slow to reflect an incident, this one collects user reports in real time. **3) `/doctor`** — rules out local issues (broken MCP, ripgrep, invalid settings). If everything's green and Claude still "feels dumber today," the culprit is almost always context pressure (autocompact thrashing), not the model.

There's a recurring meme on Reddit and X: *"Claude Code is getting dumber"*. Sometimes it's real (incident or degradation). Almost always it's one of three perception errors: your context window at 80%, an MCP that dumped 30k tokens of garbage, or anchoring from a too-long conversation. Here's how to tell them apart.

## 1. status.claude.com — first place to look

Anthropic publishes a status page with per-component uptime. Claude Code is **separate** from Claude API, Claude.ai, and Claude Cowork:

| Component | What it means |
|---|---|
| **Claude Code** | The CLI itself |
| **Claude API** (`api.anthropic.com`) | The backend your prompts hit. If this is down, Claude Code is too |
| **Claude.ai** | The web chat. Doesn't affect Claude Code |
| **Claude Console** | `platform.claude.com` (API key management) |

Hit "Subscribe" in the top right to get incidents via email, SMS, Slack, Microsoft Teams, webhook, or Atom/RSS before they hit you.

## 2. DownDetector — to corroborate

Sometimes Anthropic's status page takes 15-30 minutes to reflect an incident because the team needs to confirm it internally. DownDetector collects user reports in real time:

```
https://downdetector.com/status/claude-ai/
```

If DownDetector shows a spike and `status.claude.com` is still green, wait 10 minutes and check again. Real spike → it's going down even if officially nobody's said so yet.

## 3. `/doctor` — rule out local issues

If both checks above come back clean, the problem isn't Anthropic. It's your setup. Run:

```bash
/doctor
```

Audits installation, settings, MCP servers, and context usage in one pass. If Claude Code won't even start so you can't run `/doctor`:

```bash
claude doctor
```

Same report from outside the CLI. There's a [dedicated `/doctor` tip](/en/tips/claude-code-doctor-diagnostic) if you want to dig deeper.

## "Claude is dumber today" — what's actually happening

The model doesn't change between sessions. Anthropic ships releases with semver and `/release-notes` tells you if anything changed in your CLI. What does change is **your context**. Three symptoms commonly mistaken for model degradation:

**Autocompact thrashing**. Your context window fills, autocompact reduces it, and the next tool result fills it again. Claude Code stops retrying to avoid burning tokens. Symptom: short, slow responses that feel "lazy". Fix:

```bash
/compact "keep only the plan and the diff"
# or, if the earlier conversation isn't needed:
/clear
```

**MCP garbage**. An MCP server returns a huge blob (a schema, a DB dump, a Playwright result) and eats half your context. Symptom: the session slows down right after a tool call. Fix: disable that MCP with `/mcp` or cut the conversation branch with [`/branch`](/en/tips/claude-code-fork-session-branch-conversations).

**Anchoring**. You're 200 turns in and the first misread poisoned everything since. Symptom: Claude repeats mistakes even when you point out the right answer. Fix: `/clear`, start fresh. To preserve what was good, ask Claude to write a `/recap` first.

If you did all three and nothing changes: it's probably Claude. Report it with `/feedback` (auto-attaches session context).

## Subscribe before the next outage catches you

If your work depends on Claude Code, don't wait to refresh the status page when things feel off:

| Channel | Best for |
|---|---|
| Email / SMS | Critical outages, outside the browser |
| Slack / Microsoft Teams | Team channel notification |
| Webhook | Plug into your own internal status dashboard |
| Atom / RSS | If you keep everything in a reader |

Subscribe once and you'll know before your team.

## Pairs well with

- [`/doctor`](/en/tips/claude-code-doctor-diagnostic) — local diagnostic tool.
- [`/context` command](/en/tips/claude-code-context-command-token-usage) — see where your context window is going.
- [How to update Claude Code](/en/tips/claude-code-how-to-update) — a stale version sometimes behaves weirdly and gets blamed as "getting dumber".
- [Slash commands cheat sheet](/en/tips/claude-code-slash-commands-cheat-sheet) — includes `/compact`, `/clear`, `/recap`, `/feedback`.

> Official docs: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) · [Status page](https://status.claude.com/)
