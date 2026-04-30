---
date: 2026-04-17
type: tip
title_es: "Consigue Opus al precio de Sonnet en Claude Code"
title_en: "Get Opus Performance at Sonnet Prices in Claude Code"
---

> **TL;DR** Claude Code just shipped a new toggle (`/advisor`) that lets you run Sonnet as your main engine and consult Opus only when Sonnet stalls. Anthropic measured the combo: **−11.9% cost and +2.7% accuracy on SWE-bench** vs Sonnet alone. With Haiku + Opus advisor the jump is even bigger: **41.2% vs 19.7%** on BrowseComp. You pay Sonnet prices 90% of the time; Opus only shows up when it actually matters.

## How it works

It's not a model swap or a classic orchestration. It's a *player + coach* pattern:

- **The executor** (Sonnet or Haiku) does ALL the real work — reads files, writes code, calls tools, responds to you
- **The advisor** ([Opus 4.7](/en/tips/claude-code-opus-4-7) or Sonnet 4.6) stays on the bench as **just another tool** in the executor's toolbox
- When the executor hits a decision it can't solve (an ambiguous bug, a complex refactor, or simply "circling without progress"), it **calls the advisor** like it would call Bash
- The advisor reads **the full shared context** and returns a plan or correction in **400–700 tokens** — no code, no tool calls, just guidance
- The executor takes that advice and resumes work

The analogy: a junior dev with the senior's number on speed dial. The junior writes everything, only calls when stuck, and the senior never touches the keyboard.

## What you'll see when you type `/advisor`

```text
Advisor Tool

When Claude needs stronger judgment — a complex decision, an
ambiguous failure, a problem it's circling without progress — it
escalates to the advisor model for guidance, then resumes. The
advisor runs server-side and uses additional tokens.

For certain workloads, pairing Sonnet as the main model with Opus
as the advisor gives you near-Opus performance with reduced token
usage.

  1. Opus 4.7
  2. Sonnet 4.6
> 3. No advisor ✓

Enter to confirm · Esc to cancel
```

## How to activate it

**1. Type `/advisor`** in any Claude Code session. Default is `No advisor` — you opt in manually.

**2. Pick an advisor**:

- **Opus 4.7** if your executor is Sonnet 4.6 — the mainstream combo Anthropic recommends
- **Sonnet 4.6** if your executor is Haiku 4.5 — doubles Haiku's capability with minimal extra cost
- **No advisor** to turn it off

**3. Enter**. The advisor is live for the session. Sonnet keeps doing everything — it only escalates when it needs to.

**4. You don't invoke anything manually**. The executor decides when to consult based on its own uncertainty. You can nudge via prompt ("if you see anything suspicious, consult the advisor before touching code").

## When it pays off (and when it doesn't)

**Turn the advisor on when**:

- You're on a long task with many decisions (refactor, migration, complex feature)
- Sonnet is failing on a specific thing and you've already tried several times
- You're about to ship something critical (payments, auth, migrations) and want a second opinion in-flight

**Don't turn it on when**:

- You're doing CRUD, boilerplate, or renames — extra tokens, no return
- You're already using [Opus 4.7](/en/tips/claude-code-opus-4-7) as executor — no point consulting itself
- You're in pure `/plan` mode — for that use [`opusplan`](/en/tips/claude-code-choose-right-model), which is a different strategy

## Recommended combos

| Executor | Advisor | When |
|---|---|---|
| Sonnet 4.6 | **Opus 4.7** | The practical default — Opus quality at Sonnet cost |
| Haiku 4.5 | **Opus 4.7** | For [long-running exploration](/en/tips/claude-code-headless-mode-autonomous-agent) and heavy code reads |
| Haiku 4.5 | Sonnet 4.6 | Cheaper still, useful when you just need an occasional nudge |
| Opus 4.7 | *(anything)* | Doesn't make sense — Opus is already the most capable model |

## The numbers Anthropic published

| Metric | Number |
|---|---|
| Cost reduction (Sonnet + Opus advisor vs Sonnet alone) | **−11.9%** |
| SWE-bench Multilingual accuracy delta | **+2.7 pp** |
| Haiku + Opus advisor on BrowseComp | **41.2%** (Haiku alone: 19.7%) |
| Advisor tokens per consultation | **400–700** (1,400–1,800 with thinking) |

The number that closes the argument: **Haiku with Opus as advisor doubles its BrowseComp score**. That's not a marginal gain — that's consulting the big model at the precise moment it's needed and not the rest of the time.

## Reference

| Field | Value |
|---|---|
| Command | `/advisor` |
| Available advisors | Opus 4.7, Sonnet 4.6 |
| Default | No advisor (opt-in) |
| Execution | Server-side |
| Extra tokens per consultation | 400–700 (plan) · 1,400–1,800 (with thinking) |
| Invocation | The executor decides when to consult |
| API beta header | `advisor-tool-2026-03-01` |
| Source | [Anthropic Advisor Strategy](https://claude.com/blog/the-advisor-strategy) (April 9, 2026) |

It's the third major April change in Claude Code, after [Opus 4.7](/en/tips/claude-code-opus-4-7) and [`/ultrareview`](/en/tips/claude-code-ultrareview). All three move in the same direction: delegate more, supervise less, pay only for the horsepower you actually use.

> Official docs: [The advisor strategy — Anthropic](https://claude.com/blog/the-advisor-strategy) · [Advisor tool (API)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)
