---
date: 2026-04-16
type: tip
title_es: "/ultrareview en Claude Code: la revisión que no quieres pero vas a necesitar"
title_en: "/ultrareview in Claude Code: The Review You Don't Want but Definitely Need"
---

> **TL;DR** `/ultrareview` is a new Claude Code command that launches a **fleet of reviewer agents in the cloud** to hunt for bugs before you merge. Every finding is independently reproduced and verified — no "you might want to use const" noise. Three free runs on Pro and Max, and the whole thing runs in the background while you keep working.

## How it works

`/ultrareview` landed in Claude Code on April 16, 2026 alongside [Opus 4.7](/en/tips/claude-code-opus-4-7) — it's one of the big changes in that launch.

When you run it, Claude Code uploads your branch state (or clones your GitHub PR if you pass a number) to the [same cloud infrastructure](/en/tips/claude-code-cloud-sessions-from-browser) it already uses for remote sessions, and orchestrates **multiple reviewer agents in parallel**. Each one explores the change from a different angle: logic, edge cases, security, performance. What separates `/ultrareview` from local [`/review`](https://code.claude.com/docs/en/commands) is that **every finding is independently reproduced before being reported**. If the bug can't be verified, it doesn't make the list.

It's the equivalent of putting a paranoid senior on your diff for 15 minutes with nothing else to do.

## What you'll see when it kicks off

```bash
$ /ultrareview 1234

Ultrareview scope:
  PR #1234 — feat: add rate limiting middleware
  Files changed: 8 · Lines: +342 / -56

Free runs remaining: 2/3
Estimated cost: 0 credits (within free runs)

[Confirm to launch review in background? y/n]

✔ Review started. Track with /tasks
```

## How to use it

**1. Update Claude Code to 2.1.86 or later** and authenticate with a Claude.ai account (it won't work with an API key alone):

```bash
claude update
/login
```

**2. Review your current branch** vs the default branch — includes uncommitted and staged changes:

```bash
/ultrareview
```

**3. Review a specific GitHub PR** (requires a `github.com` remote on the repo):

```bash
/ultrareview 1234
```

**4. Track the review in the background**. It takes 10–20 minutes and doesn't block your session. You can close Claude Code and come back later — the task keeps running:

```bash
/tasks   # see running and completed reviews
```

**5. When it finishes**, verified findings arrive with file, line, and explanation. Ask Claude to fix them directly from the results.

## /review vs /ultrareview

The comparison to have clear before picking one:

| Criterion | `/review` | `/ultrareview` |
|---|---|---|
| Execution | Local, in your session | Cloud sandbox |
| Depth | Single pass | Multi-agent fleet with independent verification |
| Duration | Seconds to minutes | 10–20 minutes |
| Cost | Counts toward normal usage | 3 free runs, then [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Best for | Fast feedback while iterating | Pre-merge confidence on substantial changes |

## Reference

| Field | Value |
|---|---|
| Command | `/ultrareview [PR]` |
| Minimum version | Claude Code 2.1.86 |
| Authentication | Claude.ai (API key alone doesn't work) |
| Plans with free runs | Pro and Max · 3 runs, **one-time** |
| Team and Enterprise | No free runs, billed as extra usage |
| Not available on | Bedrock, Vertex AI, Foundry, organizations with Zero Data Retention |
| Tracking | `/tasks` |
| Without arguments | Diffs current branch vs default branch (includes uncommitted) |
| With PR number | Clones the PR directly from GitHub |

## When to spend each run

The three free runs are **one-time** — they don't refresh monthly. Spend them wisely: don't use them on trivial PRs. The value is in large changes, wide refactors, or business-critical code (payments, auth, migrations) where a production bug costs more than the 10 minutes the review takes.

If you've burned through them, the cost is still much lower than a production incident — and [tracking usage](/en/tips/claude-code-track-usage-stats-dashboard) with `/usage` lets you keep spending in check.

And if what you want is the opposite phase — reasoning through a big change **before** writing a single line — `/ultrareview` has [its cloud planning counterpart](/en/tips/claude-code-ultraplan-cloud-planning): `/ultraplan`.

> Official docs: [Find bugs with ultrareview](https://code.claude.com/docs/en/ultrareview) · [Commands reference](https://code.claude.com/docs/en/commands)
