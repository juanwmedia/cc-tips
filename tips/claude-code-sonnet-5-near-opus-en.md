---
date: 2026-06-30
type: tip
title_es: "Sonnet 5 en Claude Code: casi Opus 4.8, a precio de Sonnet"
title_en: "Sonnet 5 in Claude Code: near-Opus quality, at Sonnet prices"
---

> **TL;DR** Sonnet 5 is now in Claude Code. The `sonnet` alias now resolves to it (the universal route: `/model sonnet`), and it's the **Default** on Pro, Team Standard, and per-seat Enterprise. It ships a **native 1M-token context window**, quality *close to Opus 4.8* at a clearly lower price (intro $2/$10 per MTok through Aug 31), and makes `opusplan` (Opus plans, Sonnet executes) a great quality-to-cost combo. You need **Claude Code v2.1.197+**: `claude update`.

Working with Kimi 2.7 or Composer 2.5 (which is Kimi underneath), there's one thing you miss next to Opus: speed. It's a huge difference. You try Sonnet 4.6 and yes, it's faster, but it loses adherence: on reasoning-heavy tasks it falls short.

Sonnet 5 looks like Anthropic's answer to that gap. A frontier model that isn't trying to be the most powerful in its class, but the most balanced. Good news for when you don't need all the adherence, the power (and the price) of Opus 4.8, but still want quality agentic AI.

## What changes in Claude Code

The official docs are clear: on the Anthropic API, `sonnet` now resolves to **Sonnet 5** and `opus` to Opus 4.8. That's why the universal route to it is `/model sonnet`, whatever your plan.

Mind the Default, it's not what it seems: **Sonnet 5 is the Default on Pro, Team Standard, and per-seat Enterprise**. But on **Max, Team Premium, Enterprise pay-as-you-go, and the raw Anthropic API, the Default is still Opus 4.8**. On Max, if you change nothing, you stay on Opus, not Sonnet 5.

Three things that matter while coding:

- **Native 1M context.** Sonnet 5 ships a 1-million-token window by default; the old `sonnet[1m]` trick is now redundant.
- **`opusplan` levels up.** Opus 4.8 to plan, Sonnet 5 to execute. Top-quality planning, fast and cheap execution.
- **It's the most agentic Sonnet.** Per Anthropic, it finishes complex tasks where previous Sonnets stopped short, and checks its own output without being asked.

## How to confirm it or switch

### **1. Update (or it won't even show up)**

```bash
claude update
```

Sonnet 5 **requires Claude Code v2.1.197 or later**. On older versions it doesn't appear in the picker.

### **2. Check or pin the model**

```bash
/model            # opens the picker, shows your current model
/model sonnet     # pins Sonnet 5 as the default for new sessions
```

Since v2.1.153, `/model <alias>` saves your choice as the default by writing the `model` field in your settings. For the plan+execute combo:

```bash
/model opusplan   # Opus 4.8 plans, Sonnet 5 implements
```

### **3. When to stay on Opus 4.8**

Opus is still *"the model of choice for higher accuracy"*. For critical refactors, delicate architecture, or when adherence matters more than speed, `/model opus`. For day-to-day agentic work, Sonnet 5.

## Reference

| Alias / setting | Resolves to (subscription) |
|---|---|
| `sonnet` | Sonnet 5 |
| `opus` | Opus 4.8 |
| `opusplan` | Opus 4.8 (plan) + Sonnet 5 (execution) |
| `default` on Pro / Team Standard / per-seat Enterprise | Sonnet 5 |
| `default` on Max / Team Premium / Enterprise pay-as-you-go / API | Opus 4.8 |

| Sonnet 5 price (per MTok) | Input | Output |
|---|---|---|
| Intro (through Aug 31, 2026) | $2 | $10 |
| Standard | $3 | $15 |

> Note: on Bedrock, Vertex, and Foundry, `sonnet` still resolves to Sonnet 4.5; there, select the full model name or set `ANTHROPIC_DEFAULT_SONNET_MODEL`.

> Official docs: [Model configuration](https://code.claude.com/docs/en/model-config)

To understand which model wins (and why it sometimes resets on you), see [/model in Claude Code](/en/tips/claude-code-change-model-default). To decide when Sonnet vs when Opus, [how to choose the right model](/en/tips/claude-code-choose-right-model). And above Opus, [Fable 5](/en/tips/claude-code-fable-5-above-opus).

## Requirements

- Claude Code **v2.1.197+** (`claude update`). The `sonnet` alias resolves to Sonnet 5 on the API; it's the `default` only on Pro, Team Standard, and per-seat Enterprise.
