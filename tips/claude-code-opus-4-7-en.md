---
date: 2026-04-16
type: tip
title_es: "Opus 4.7 ha llegado a Claude Code: deja de supervisar, empieza a delegar"
title_en: "Opus 4.7 Is in Claude Code: Stop Supervising, Start Delegating"
---
> **TL;DR** Opus 4.7 landed this morning (April 16, 2026) in Claude Code and it changes the game: `xhigh` effort by default, 1M-token context window, adaptive reasoning, and the new `/ultrareview` command. Max users get it as default; Pro users have to switch with `/model opus`. It's the first model you can actually hand a multi-hour task to without checking in every ten minutes to fix it.

## How it works

Opus 4.7 replaces Opus 4.6 as Anthropic's most capable model. In Claude Code it introduces three visible changes from the first prompt: [effort level](/en/tips/claude-code-effort-level-adjust-reasoning) `xhigh` by default (a new step between `high` and `max`), adaptive reasoning (the model decides how much to think on its own), and a 1M-token context window enabled with no configuration on Max, Team, and Enterprise.

The agentic jump is where it matters. Anthropic reports 3× more tasks resolved on SWE-bench Verified vs Opus 4.6, 70% on CursorBench (vs 58%), and a third fewer tool errors on Notion Agent benchmarks. On vision, 98.5% vs 54.5% — that's not an improvement, it's a different model.

It also reports better cross-session memory: start a long task, close your session, come back the next day, and it picks up without you having to re-explain a thing. It extends [the automatic memory Claude Code already had between conversations](/en/tips/claude-code-auto-memory-between-sessions) into multi-hour work.

## What you'll see when you start a session

```bash
$ claude --version
2.1.111

$ /model
> opus   ─ Claude Opus 4.7 (xhigh)
  sonnet ─ Claude Sonnet 4.6 (high)
  haiku  ─ Claude Haiku 4.5

✔ opus selected. Effort: xhigh
```

## How to start using it

**1. Update to 2.1.111 or later**. Opus 4.7 doesn't show up in earlier versions:

```bash
claude update
claude --version   # should show 2.1.111+
```

**2. Select the model**. If you're on Max or Team Premium, Opus 4.7 is already your default. On Pro, API, and Enterprise plans, Sonnet 4.6 remains default until April 23, 2026 — switch manually until then:

```bash
/model opus
```

**3. Leave effort at `xhigh`**. It's the new default on Opus 4.7 across all plans and the level Anthropic recommends for [agentic coding tasks](/en/tips/claude-code-headless-mode-autonomous-agent). Drop to `high` only when you want more speed and fewer tokens; bump to `max` only for occasional problems where deep reasoning pays off (warning: `max` is prone to overthinking).

**4. Take advantage of the 1M context**. On Max, Team, and Enterprise, the [1 million tokens](/en/tips/claude-code-1m-context-window-tips) are enabled out of the box. To force it explicitly:

```bash
/model opus[1m]
```

**5. Review before merge with [`/ultrareview`](/en/tips/claude-code-ultrareview)**. The new command spins up a fleet of reviewer agents in the cloud to verify real bugs — not style suggestions. Three free runs on Pro and Max. And if you want full delegation without confirming every step, pair it with [permission modes](/en/tips/claude-code-permission-modes-shift-tab) in `acceptEdits` or `auto`.

## Reference

| Field | Value |
|---|---|
| Model ID | `claude-opus-4-7` |
| Claude Code alias | `opus` |
| Minimum Claude Code version | 2.1.111 |
| Context window | 1M tokens |
| Max output | 128k tokens |
| Pricing | $5/MTok input · $25/MTok output |
| Thinking | Adaptive (not Extended) |
| Default effort | `xhigh` |
| Effort levels | `low`, `medium`, `high`, `xhigh`, `max` |
| Training cutoff | January 2026 |
| Default model on | Max, Team Premium |

## When Sonnet still makes sense

Opus 4.7 isn't always the answer. Sonnet 4.6 handles 80% of daily coding work cheaper and faster — and the [right model](/en/tips/claude-code-choose-right-model) depends on the task. Reserve Opus 4.7 for: deep debugging, large refactors, long sessions with heavy context, and anything that used to force you to babysit every 15 minutes. For CRUD and boilerplate, stick with Sonnet.

> Official docs: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) · [Model configuration](https://code.claude.com/docs/en/model-config)
