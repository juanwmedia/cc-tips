---
date: 2026-06-10
type: tip
title_es: "claude -p deja de comerse tus límites en Claude Code: por fin tiene crédito propio"
title_en: "Your claude -p scripts stop eating your Claude Code limits: they finally get their own credit"
---

> **TL;DR** Starting **June 15, 2026**, what `claude -p` and the Agent SDK spend on subscription plans comes out of a **separate monthly Agent SDK credit**, not your interactive limits. Your cron jobs, CI and scripts stop eating the quota you need for live coding. But it's opt-in: you **claim it once** from your account. It expires monthly and doesn't roll over.

You set up some automation with `claude -p`, drop it in a cron job or CI, and it spends all night. Until now it all came out of one pot: you'd sit down to actually code and find the limit drained by a script that ran at 3am. That split changes on June 15.

## What changes on June 15

From that date, programmatic and interactive usage stop competing. Two pots:

```
BEFORE                         FROM JUNE 15

one shared usage pot           interactive pot        Agent SDK credit
coding + claude -p             terminal, IDE,         claude -p, SDK,
compete for the limit          web, mobile            CI, cron, scripts
                               (your usual limits,    (its own budget
                                untouched)             in dollars)
```

The docs put it the same way across pages: *"a monthly Agent SDK credit, separate from your interactive usage limits."*

## How much credit your plan gives you

The credit is a dollar amount, and it varies by plan:

| Plan | Monthly Agent SDK credit |
|---|---|
| Pro | **$20** |
| Max 5x | **$100** |
| Max 20x | **$200** |
| Team (Standard) | **$20** |
| Team (Premium) | **$100** |
| Enterprise | **$20 to $200** depending on structure |

It's spent at standard API rates, so CI that runs on every PR or a runaway `/loop` drains it in days, not weeks. Cap actions and spend per call with [`--max-turns` and `--max-budget-usd`](/en/tips/claude-code-headless-mode-autonomous-agent).

## What's covered and what isn't

**Comes out of the Agent SDK credit:**

- `claude -p` (headless mode): scripts, cron, build hooks.
- The Agent SDK in your own projects (Python or TypeScript).
- GitHub Actions (the `@claude` PR-review action runs on the SDK).
- Third-party apps authenticated through the Agent SDK.

**Still on your normal limits (nothing changes):**

- Interactive Claude Code in the terminal or IDE.
- Conversations on web, desktop and mobile.
- Claude Cowork.

## You have to claim it (and it expires monthly)

It's a **one-time opt-in**: you claim the credit from your Claude account once and it's active. It doesn't switch on by itself, so if you never claim it your programmatic usage stays exactly as it is today. The credit **doesn't roll over** month to month: whatever you don't spend is gone, and you start fresh next month. And it's **per individual account**: on a team it can't be shared or pooled across teammates.

## What happens when it runs out

It comes down to one setting of yours:

- **With usage credits enabled:** extra Agent SDK usage flows on at standard API rates. Cap it monthly with `/usage-credits` so it can't run away.
- **Without usage credits:** Agent SDK requests **stop** until your credit refreshes next month.

So by default your automation halts instead of handing you a surprise bill. That's the safety net that was missing for leaving `claude -p` running unattended.

## Where it fits

This is the billing model, not how you use it. The pieces around it:

- You already know [how to run `claude -p`](/en/tips/claude-code-headless-mode-autonomous-agent): cron, `--allowedTools`, spend caps. This is which pot it draws from now.
- The [Agent SDK from your own code](/en/tips/claude-agent-sdk-build-agents) draws from this same credit.
- Your interactive side is unchanged: track it with [`/usage` and `/stats`](/en/tips/claude-code-track-usage-stats-dashboard).
- On the [map of the four ways to send Claude to the background](/en/tips/claude-code-background-agents-map), the credit only touches the headless/SDK quadrant; Agent View, `/loop` and Routines still come out of your plan.

> Official docs: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) · [Manage costs](https://code.claude.com/docs/en/costs) · [Use the Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

## Requirements

A subscription plan (Pro, Max, Team or Enterprise). The change takes effect **June 15, 2026**; the credit must be claimed once from your Claude account.
