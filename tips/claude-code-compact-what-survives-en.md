---
date: 2026-06-05
type: tip
title_es: "/compact en Claude Code: las instrucciones que desaparecen sin avisar (y cómo hacerlas sobrevivir)"
title_en: "/compact in Claude Code: the instructions that vanish without warning (and how to make them survive)"
---

> **TL;DR** When a session nears the limit, Claude Code compacts on its own, without you typing anything, and summarizes the conversation. But not everything comes back the same: the system prompt, your project-root CLAUDE.md, and auto memory get re-injected from disk; your `paths:` rules, nested CLAUDE.md, and skill bodies get lost or trimmed. That's why Claude sometimes "forgets" a rule mid-task. Golden rule: anything that must survive belongs in the root CLAUDE.md or at the top of your `SKILL.md`.

The unsettling part isn't the `/compact` you run yourself. It's the **automatic** one: as context nears the limit, Claude Code compacts on its own, mid-task, without you touching anything. And a rule that was governing your edits can quietly stop applying right there.

## How compaction works

Compaction replaces the conversation history with a structured summary. What comes back afterward depends on **how each instruction was loaded**:

- Whatever lives **outside** the history (system prompt, output style) stays intact.
- Whatever is **re-read from disk** at startup (root CLAUDE.md, unscoped rules, auto memory) gets re-injected.
- Whatever entered **as a message** in the history (`paths:` rules, nested CLAUDE.md, skill bodies) gets summarized with everything else and only comes back when it's triggered again.

Manual `/compact` and the automatic pass work the same way. The difference is that you don't choose the automatic one.

## What it looks like

```text
# Before: the paths: rule governs your edits
[Loaded .claude/rules/api-conventions.md]   ← applies to src/api/**

# Claude compacts on its own near the limit
⏺ Conversation compacted

# After: the same edit, without that rule
# (it comes back as soon as Claude re-reads a file in src/api/)
```

## What survives and what doesn't

| Mechanism | After compaction |
|---|---|
| System prompt and output style | Intact (not part of history) |
| Root CLAUDE.md and unscoped rules | Re-injected from disk |
| Auto memory (MEMORY.md) | Re-injected from disk |
| Rules with `paths:` frontmatter | **Lost until you read a matching file again** |
| Nested CLAUDE.md in subdirectories | **Lost until you re-read a file in that folder** |
| Invoked skill bodies | **Re-injected, but capped at 5,000 tokens per skill and 25,000 total; oldest dropped first** |
| Hooks | Not applicable (they run as code, not context) |

"Lost" isn't "erased forever": the `paths:` rules and nested CLAUDE.md come back on their own the moment Claude reads a matching file again. The problem is the window in between, where Claude works without them and never tells you.

## How to make them survive

**1. Rules that can never be missing**

If a rule must apply no matter what, don't leave it riding on a `paths:`. Drop the scope frontmatter or move it to the root CLAUDE.md, which always gets re-injected.

**2. Critical instructions at the top of SKILL.md**

When a skill is re-injected, truncation **keeps the start** of the file and drops the end. Put what really matters (the hard rules, the gotchas) in the first lines of `SKILL.md`, not the last.

**3. Compact yourself, with focus, before a long task**

Instead of waiting for the auto-compact to fire mid-task, run it yourself at a natural break and tell it what to keep. [Habit 3 of how to save tokens](/en/tips/claude-code-save-tokens-10-habits) covers `/compact` with instructions.

This is the flip side of [prompt caching](/en/tips/claude-code-prompt-caching-slow-expensive-turns): there `/compact` barely costs you in **spend**; here the cost is **fidelity**, what it takes out of your instructions. And to understand what loads at startup (before any compaction), see [when Claude Code loads each feature](/en/tips/claude-code-when-features-load-context).

> Official docs: [Explore the context window](https://code.claude.com/docs/en/context-window)
