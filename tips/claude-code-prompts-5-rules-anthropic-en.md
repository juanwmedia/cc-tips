---
date: 2026-06-24
type: tip
title_es: "Prompts en Claude Code: las 5 reglas que sigue Anthropic"
title_en: "Prompts in Claude Code: the 5 rules Anthropic actually follows"
---
> **TL;DR** Before you ask Claude Code for anything, put these five pieces into the prompt: the goal in one sentence, the concrete file with `@`, the reason behind the constraint, the instruction in positive form, and an input-to-output example. All five come straight from Anthropic's official docs. They work for vibe coding and for production code.

The pro industry is obsessed with specs. `/spec`, spec-driven development, 800-line markdown templates before a line of code gets written. Fine for your production monorepo. Not fine when you're fixing something in fifteen minutes, or when you're starting out, or when you're vibe-coding and you just want to ship.

For all of that, the prompt is still the unit. And a good prompt is still Claude Code's atomic unit in 2026. Anthropic published two pages of documentation months ago that almost nobody reads cover to cover: `best-practices` and `prompt-engineering`. These five rules come straight from them.

Result:

```
# Bad
> fix the login

# Good
> Change the login flow so that, once the email is validated,
  it redirects to /dashboard instead of /home.

  File: @src/auth/session.ts

  Why: /dashboard already has the user context loaded.
  /home triggers an extra round-trip that users notice as lag.

  Minimum change: don't refactor anything around it, don't touch
  the tests, don't add comments.

  Expected behavior:
    Before: login OK → router.push('/home') → fetch user → render
    After:  login OK → router.push('/dashboard') → render
```

## The five rules

### **1. The goal in one sentence, not the task**

Anthropic's *golden rule*: show your prompt to a coworker with no context on the task. If they'd be confused, Claude will be too. Don't describe the action ("fix"), describe the outcome ("redirect to /dashboard once the email is validated"). The verb matters: say **what changes for the user or for the code**, not what kind of work you want Claude to do.

### **2. Point at the file with `@`**

Almost any prompt gets better if it carries an `@path/to/file` inside it. Claude reads the file from disk before responding and stops hallucinating APIs or function names. It's the difference between "explain how the token gets validated" and "explain how the token gets validated in `@src/auth/session.ts`". If you don't know which file it is, use `@src/auth/` so Claude sees the directory listing first.

Combine it with the [other four ways to inject context](/en/tips/claude-code-five-ways-right-context): pipe, image, directory, and CLAUDE.md imports.

### **3. State the reason, not just the rule**

This is the one almost nobody applies. Anthropic shows it with an example that's already a classic:

- Rule alone: `NEVER use ellipses`
- Rule plus reason: `Your response will be read aloud by a text-to-speech engine, so never use ellipses because the engine doesn't know how to pronounce them`

The gap is huge. With the reason, Claude generalizes correctly to the edge cases you haven't anticipated. Without it, Claude follows the literal rule and breaks the moment the scenario shifts.

### **4. Ask in positive form, instruct in the imperative**

Two sub-rules from the same docs page:

**Positive, not negative.** "Don't use markdown" performs worse than "write in flowing prose paragraphs." Claude's brain (like yours) anchors better on what to DO than on what to avoid.

**Imperative, not consultative.** "Could you suggest some changes to improve this function?" gets you suggestions. "Cache the result of this function" gets you the cache. If you want action, use the action verb.

### **5. Drop in an input-to-output example**

*Multishot* is still the most underrated lever. For vibe coding, one example is enough:

```
Input: user with email_verified = false
Expected output: redirect to /verify-email
```

For serious work, Anthropic recommends 3 to 5 examples wrapped in `<example>` tags. The example hands Claude what no description can: the exact format, the tone, the length, the edge cases. If you only do one thing from this list, do this one.

## When the prompt stops being enough

When the change touches more than three files at once, when there are design decisions about what the thing will be called six months from now, or when you'll iterate on the same feature across several days. That's when [plan mode](/en/tips/claude-code-permission-modes-shift-tab) or a short spec starts paying off. For everything else, the five rules above are enough.

## Reference

| Rule | Question it answers | Cost of skipping it |
|---|---|---|
| Goal in one sentence | What exactly is changing? | Claude invents the goal |
| File with `@` | Which code are we talking about? | API hallucinations |
| The reason | Why this constraint? | Breaks at edge cases |
| Ask in positive form | What do you actually want? | Output fights you |
| Input→output example | What does "done right" look like? | Erratic format and tone |

> Official docs: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) and [Prompt engineering — Be clear and direct](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
