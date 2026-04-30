---
date: 2026-04-13
type: tip
title_es: "Visualiza tu consumo real de tokens en Claude Code con /usage y /stats"
title_en: "Visualize Your Actual Token Consumption in Claude Code with /usage and /stats"
---

> **TL;DR** `/usage` shows your plan limits and rate limit status. `/stats` opens a full dashboard with a heatmap, session count, token totals, model breakdown, and streaks. Together they answer the question everyone is asking right now: where are my tokens going?

At the time of writing, token consumption and session limits are a hotter topic than ever. Developers are running into limits, sessions feel shorter, and the default reaction is to blame the tool. But before optimizing anything, you need to see what's actually happening. Two built-in commands give you that visibility — and most people don't know they exist.

`/usage` is the quick check: are you near your plan limit? Is a rate limit active right now? It answers the immediate "can I keep working?" question.

`/stats` is the long view: how many sessions have you run, how many tokens across all of them, which models are you burning through, and what does your activity pattern look like over weeks and months.

Neither command costs tokens. Neither modifies anything. They're read-only diagnostics.

Result:

```
> /usage

Status    Config    Usage    Stats

Plan: Max
Rate limit: 1,247 / 2,000 requests remaining
Resets in: 3h 42m
```

```
> /stats

              Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar  Apr
Mon           ░░   ██   ░░   ██   ██   ██   ██   ░░   ░░   ██   ██   ██   ██
Wed           ░░   ██   ██   ██   ██   ██   ░░   ░░   ██   ██   ██   ██   ██
Fri           ░░   ░░   ██   ██   ░░   ██   ██   ██   ██   ██   ██   ██   ░░

All time · Last 7 days · Last 30 days

Favorite model: Opus 4.6       Total tokens: 10.5m
Sessions: 92                   Longest session: 40d 22h 54m
Active days: 66/99             Longest streak: 56 days
Most active day: Mar 28        Current streak: 8 days

↓ stats · r to cycle dates · ctrl+s to copy
```

## How to use them

### **1. Check your plan limits with /usage**

```bash
> /usage
```

Shows four tabs: **Status**, **Config**, **Usage**, and **Stats**. The Usage tab displays your current consumption against plan limits. If you're on Pro or Max, this is where you see how close you are to hitting the rate limit.

### **2. Explore your history with /stats**

```bash
> /stats
```

The Stats tab opens a visual dashboard with:

- **Activity heatmap**: GitHub-style grid showing which days you used Claude Code and how intensely
- **Session metrics**: total sessions, longest session, active days, streak data
- **Token breakdown by model**: how many tokens each model consumed (Opus, Sonnet, Haiku)
- **Tokens per day chart**: daily consumption over time

Use the keyboard shortcuts at the bottom to navigate: `r` to cycle between time ranges (all time, 7 days, 30 days), arrow keys to move between tabs, `Ctrl+S` to copy.

### **3. Combine with /context for full visibility**

`/usage` and `/stats` show your historical and plan-level data. For the current session's context breakdown, use [`/context`](/en/tips/claude-code-context-command-token-usage) — it shows exactly how system prompt, tools, MCP servers, and messages consume the 200k window right now.

The three together give you complete visibility: `/context` for the current session, `/stats` for the long-term trend, `/usage` for plan limits.

## Reference

| Command | What it shows | Scope | Costs tokens? |
|---|---|---|---|
| `/usage` | Plan limits, rate limit status | Account-level | No |
| `/stats` | Heatmap, sessions, tokens, models, streaks | All-time history | No |
| `/context` | Context window breakdown by category | Current session | No |
| `/cost` | Token cost in USD for current session | Current session (API users) | No |

## When to use which

| Situation | Command |
|---|---|
| "Am I about to hit my limit?" | `/usage` |
| "Which model am I burning through?" | `/stats` |
| "What's eating my context window right now?" | `/context` |
| "How much has this session cost in dollars?" | `/cost` |

> Official docs: [Commands reference](https://code.claude.com/docs/en/commands) | [Manage costs effectively](https://code.claude.com/docs/en/costs)

Related tips: [Monitor token usage with /context](/en/tips/claude-code-context-command-token-usage) | [10 habits to save tokens](/en/tips/claude-code-save-tokens-10-habits) | [Choose the right model](/en/tips/claude-code-choose-right-model)
