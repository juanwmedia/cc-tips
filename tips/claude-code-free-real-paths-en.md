---
date: 2026-05-01
type: tip
title_es: "¿Claude Code gratis? La trampa del 'plan free' y las 2 vías reales"
title_en: "Claude Code free? The 'free plan' trap and 2 real paths"
---

If you've Googled "Claude Code free" and landed on a post promising a "free plan," that post is wrong. Anthropic's own pricing page is unambiguous: **the Free tier does not include Claude Code**. Pro at $17/month (annual) is the entry point.

But there are two legitimate ways to use Claude Code at zero cost — one is a small starting credit, the other is worth $1,200. And there's an exception buried in the second one that most people miss.

## The trap: claude.ai Free ≠ Claude Code

Pulled from [claude.com/pricing](https://claude.com/pricing) directly:

| Tier | Price | Claude Code |
|---|---|---|
| Free | $0/month | ❌ Not included |
| Pro | $17/mo (annual) or $20/mo | ✅ Included |
| Max 5x | $100/month | ✅ Included |
| Max 20x | $200/month | ✅ Included |

The Free tier gets you Claude chat in the browser (Sonnet 4.6, limited daily messages). It does **not** get you the terminal `claude` command. Any post that says otherwise is outdated or wrong.

## Path 1 — Anthropic API with your own key

Create an account at [console.anthropic.com](https://console.anthropic.com), generate an API key, and wire it to Claude Code:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
claude
```

Billing is **pay-as-you-go** — you pay for the tokens you actually consume, no monthly subscription. It's the cheapest entry point for occasional use of full Claude Code (all models available).

What about the "free credits" some blogs mention? Anthropic has historically given a small welcome credit when you verify your phone on signup. **The official Anthropic docs don't explicitly mention it**, so verify the current amount on console.anthropic.com when you create the account — it may have changed or been discontinued. If it's still active, it gives you a few hours to test before billing kicks in.

## Path 2 — Claude for Open Source ($1,200 of value, 6 months)

Anthropic launched [Claude for Open Source](https://claude.com/contact-sales/claude-for-oss) in early 2026: **6 months of Claude Max 20x — the $200/month tier — at zero cost** for qualifying maintainers. That's $1,200 of value with full Max 20x tier access (Claude Code included).

Standard eligibility:

- Primary maintainer or core team member of a public repo with **5,000+ GitHub stars** or **1M+ monthly NPM downloads**
- Active in the last 3 months (commits, releases, or PR reviews)

The hidden door, straight from the program page: *"If you maintain something the ecosystem quietly depends on, apply anyway and tell us about it."* Translation: critical infrastructure libraries that fly under the star-count radar can still get in.

Up to 10,000 contributors accepted. Rolling applications.

## Reference

| Path | Cost | Claude Code? | When to pick it |
|---|---|---|---|
| **claude.ai Free** | $0 | ❌ No (the trap) | Don't, if you want Claude Code |
| **API + your own key** | Pay-as-you-go (welcome credit if active) | ✅ Yes, all models | Test driving Claude Code or occasional use |
| **Claude for Open Source** | $0 for 6 months | ✅ Yes (Max 20x) | You maintain a substantial OSS repo |
| **Pro (paid)** | $17-20/mo | ✅ Yes | Routine personal use |

## What to do today

If you don't qualify for the OSS program, the cheapest legitimate path is Pro at $17/month annual. Two complementary tips for stretching it: [10 habits to save tokens](/en/tips/claude-code-save-tokens-10-habits) and [tracking your usage with /stats](/en/tips/claude-code-track-usage-stats-dashboard).

> Source of truth on pricing: [claude.com/pricing](https://claude.com/pricing)
> OSS program: [claude.com/contact-sales/claude-for-oss](https://claude.com/contact-sales/claude-for-oss)

