---
date: 2026-06-09
type: tip
title_es: "Fable 5 en Claude Code: el modelo nuevo que está por encima de Opus"
title_en: "Fable 5 in Claude Code: the new model that sits above Opus"
---

> **TL;DR** Fable 5 is Claude Code's new ceiling, above Opus: built for your longest, hardest tasks. Switch to it with `/model fable` (you need v2.1.170 or later). It burns through your limits ~2× faster than Opus, so it isn't for everything. And it ships with a safety classifier that can reroute you to Opus on its own, sometimes on the very first message.

The model picker just went from four options to five. Fable 5 sits above Opus 4.8 as the most capable model: built for tasks that don't fit in a single sitting. It investigates before acting and verifies its own work more than smaller models do. It isn't the default: your account still starts on Opus 4.8 (or Sonnet, depending on your plan), and you step into Fable on purpose.

Result:

```
Select model

  1. Default (recommended)   Opus 4.8 with 1M context
> 2. Fable 5                 Most capable for your hardest and longest-running tasks
                             Uses your limits ~2× faster than Opus
  3. Sonnet                  Sonnet 4.6 · Efficient for routine tasks
  4. Haiku                   Haiku 4.5 · Fastest for quick answers
  5. Opus 4.8 ✓              Best for everyday, complex tasks (claude-opus-4-8)

Enter to set as default · s to use this session only
```

## **1. How to switch**

`/model fable`, or pick option 2 in the picker (`/model` with no argument). In the picker, `Enter` makes it your default for new sessions and `s` uses it for this session only. The `best` alias points to Fable 5 wherever your account has access.

## **2. The requirement (it just shipped)**

Fable 5 needs Claude Code **v2.1.170 or later**. If your picker doesn't show it, run `claude update`. It isn't available under zero data retention: there the picker omits it or shows it disabled.

## **3. When it's worth it**

The docs are blunt about how to get the most from it, and most of it runs against your reflexes from smaller models:

- **Describe the outcome, not the steps.** Hand it the result you want and let it plan the path. Pair it with [`/goal`](/en/tips/claude-code-goal-stop-condition) to keep it working until that outcome holds.
- **Hand it ambiguous problems:** root-cause investigations, outage debugging, architecture decisions. That's where the extra investigation pays off.
- **Stop reminding it to test:** it verifies its own work with less prompting, so the "remember to check this" nudges are usually wasted.
- **Size up larger tasks:** work you'd normally break into pieces. It holds long sessions without losing the thread.

Effort is `high` by default, up to `max`. On Fable 5 thinking can't be turned off: it always reasons adaptively.

## **4. The automatic reroute nobody warns you about**

This is the most practical part and almost nobody will see it coming. Fable 5 runs with safety classifiers for **cybersecurity and biology**. When one flags your request, Claude Code **re-runs it on Opus** (4.8 on the Anthropic API) with a notice, and the session continues on Opus. To get back: `/model fable`.

The surprising bit: it can trigger on the **first message**, before you've typed anything unusual, because that first request carries your `CLAUDE.md` and the repo's git status. A repository with security or biology material can trip it on that context alone.

- To check whether your customizations are the trigger, start with `claude --safe-mode`: it disables CLAUDE.md, skills, MCP, and hooks. Git status and directory names still count.
- To decide each time instead of letting it switch on its own, go to `/config` and turn off "switch models when a message is flagged".

If you work in pentesting, CTF, or biology-adjacent code, expect it to fire often.

## Fable 5 at a glance

| | |
|---|---|
| How to switch | `/model fable` · picker option 2 · `best` alias |
| Default | No (you stay on Opus 4.8 or Sonnet) |
| Minimum version | Claude Code v2.1.170 |
| Limits | burns them ~2× faster than Opus |
| Effort | `high` by default, up to `max` · thinking always on |
| Context | 1M tokens on the Anthropic API |
| Safety fallback | cybersecurity and biology → Opus, with a notice |

## Where it fits

Fable 5 is the new tier above [Opus 4.7](/en/tips/claude-code-opus-4-7) and Opus 4.8. If you're unsure what to use when, [the choose-your-model guide](/en/tips/claude-code-choose-right-model) still holds: Fable for the hardest, longest work, Opus for everyday, Sonnet for routine, Haiku for quick answers.

> Official docs: [Model configuration](https://code.claude.com/docs/en/model-config) | [Introducing Claude Fable 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)

## Requirements

Claude Code v2.1.170 or later (`claude update`). Not available under zero data retention.
