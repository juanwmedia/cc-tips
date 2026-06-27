---
date: 2026-06-26
type: tip
title_es: "Claude Code te oculta su thinking: cómo recuperarlo de verdad (y los trucos que no funcionan)"
title_en: "Claude Code hides its thinking now: what actually brings it back (and the fixes that don't)"
---

> **TL;DR** On a Claude Code subscription, a recent update **redacts** the reasoning by default: the model still thinks (and you still pay for it), but you don't see it. Bringing it back takes two things in `~/.claude/settings.json`: `"showThinkingSummaries": true` (un-redacts it) and `"verbose": true` (displays it, or press `Ctrl+O` per session). Tested on v2.1.195. The other "fixes" going around don't do this.

I'm one of the few who actually reads the model's reasoning. I like watching a frontier model like Opus think: where it hesitates, what it discards, why it picks one path over another. One day it stopped showing up. No warning, no clear changelog, under the banner of speed. Unless you read the docs and the GitHub issues, you wouldn't even know they switched it off.

And there's a lot of confusion around it. My read: Anthropic is deliberately opaque here, because the confusion works in its favor. So, for our version of Claude Code (**2.1.195**), here is how to bring it back.

## Why you don't see it

Claude Code sends a header by default (`redact-thinking-2026-02-12`) that **redacts** the thinking blocks in the terminal. The reasoning still happens and is still billed, it just never reaches your screen. Getting it back is two separate levers, and that's where almost everyone trips: they flip only one.

- **Un-redact:** get the server to return the reasoning.
- **Display:** get the terminal to show it instead of collapsing it.

What you get once it's on:

```
> Hey Claude, how are you doing?

∴ The user is just saying hello, so I'll respond warmly
  and offer to help with whatever they need.
```

The reasoning, in gray, before the answer.

## How to bring it back

### **1. Un-redact with `showThinkingSummaries`**

In `~/.claude/settings.json`:

```json
{ "showThinkingSummaries": true }
```

Without this, a subscription session gets an **empty** thinking block. It's the piece almost nobody sets, and the one that actually brings the reasoning back.

### **2. Display it with `verbose` (or `Ctrl+O`)**

```json
{ "verbose": true }
```

`verbose: true` keeps it expanded for good. Prefer it per session? Press `Ctrl+O`. But `verbose` alone, without step 1, shows nothing: it expands an empty box.

### **3. What we tested (not hearsay)**

| `verbose` | `showThinkingSummaries` | Reasoning visible? |
|---|---|---|
| `false` | `false` | No (redacted by default) |
| `true` | `false` | **No** (verbose alone isn't enough) |
| `true` | `true` | **Yes** |

What we verified by hand: `showThinkingSummaries` is **required** (without it, nothing shows). And per the docs, `verbose`/`Ctrl+O` is the switch that displays it. The safe recipe is to set both.

## What does NOT work (whatever you read elsewhere)

| The claim | The reality |
|---|---|
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` brings it back | Controls the reasoning *budget*, not whether it shows. And has no effect on Opus 4.7+ |
| `/effort high` brings it back | Raises reasoning *depth*, not the display |
| `think` / `think hard` in the prompt | No longer keywords; only `ultrathink` is recognized, and it too is depth, not display |

## Heads-up: this is a snapshot of today

This moves fast. The redaction arrived with the `redact-thinking-2026-02-12` header, the setting is barely documented, and there are [issues reporting](https://github.com/anthropics/claude-code/issues/52376) that it didn't work on subscription. On **2.1.195** (ours), the combination above works. If you update and it stops, go back to the docs and the issues.

Once it's visible, reading it live pays off: [verbose mode turns you into a real-time reviewer](/en/tips/claude-code-verbose-output-see-thinking), able to kill a hallucination before it becomes code.

> Official docs: [Model configuration — extended thinking](https://code.claude.com/docs/en/model-config)

## Requirements

- Claude Code v2.1.x (tested on 2.1.195), subscription plan (Pro/Max).
- You're billed for thinking tokens even when redacted, so hiding it saves you nothing.
