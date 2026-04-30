---
date: 2026-02-21
type: tip
title_es: "¿Cómo saber qué #@$%! piensa Claude en tiempo real?"
title_en: "What the #@$%! Is Claude Thinking? Watch It Live"
---

# Quick Tip: What the #@$%! Is Claude Thinking? Watch It Live

> **TL;DR** Press `Ctrl+O` to watch Claude think. Spot problems early. Stop bad decisions before they become bad code.

`Ctrl+O` toggles verbose output in Claude Code. When active, you see everything the model processes before and while it responds: tool call details, execution traces, and — crucially — the extended thinking blocks that reveal the model's internal reasoning.

This shortcut flies under the radar, but it's one of the most valuable when you're working with a thinking model. Being able to read the reasoning in real time turns you into a live reviewer — you can catch hallucinations, wrong assumptions, or flawed logic before they materialize into code changes.

This matters most when Claude is working on something complex. The thinking trace shows you how the model is approaching the problem. If you spot a wrong assumption, a hallucination, or a path that will lead nowhere, you can `Ctrl+C` immediately — before Claude writes files, runs commands, or burns through tokens on a dead end.

Result:

```
> Ctrl+O

Verbose output ON

⏺ Thinking…
  Let me analyze the authentication flow. The user wants to add
  JWT refresh tokens. I'll need to modify the middleware first,
  then update the token service...

  [thinking continues in real-time as gray italic text]
```

## How to use it

### **1. Toggle verbose output on**

Press `Ctrl+O` at any point during a session. A confirmation message appears and all subsequent responses include the thinking trace.

### **2. Watch the reasoning in real time**

As Claude streams its response, you'll see the thinking blocks rendered in gray italic text above the actual output. This is the model's internal reasoning — not a summary, the actual chain of thought.

### **3. Interrupt when needed**

If the reasoning reveals a wrong direction, press `Ctrl+C` to stop generation immediately. Then redirect with a corrected prompt.

### **4. Toggle off when done**

Press `Ctrl+O` again to return to clean output. Verbose mode persists during the session but resets when you exit.

## Reference

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Toggle verbose output on/off |
| `Ctrl+C` | Stop generation mid-response |
| `Alt+T` / `Option+T` | Toggle extended thinking on/off |

## When verbose mode is most useful

| Scenario | Why it helps |
|---|---|
| Complex refactors | See if Claude understands the dependency chain before it starts editing |
| Debugging sessions | Catch wrong hypotheses before Claude modifies working code |
| Architecture decisions | Verify the model's reasoning matches your mental model |
| Unfamiliar codebases | Confirm Claude is reading the right files and drawing correct conclusions |

> Official docs: [Interactive mode — Keyboard shortcuts](https://code.claude.com/docs/en/interactive-mode)
