---
date: 2026-05-03
type: tip
title_es: "/goal en Claude Code: define la condición de parada y vete a otra cosa"
title_en: "/goal in Claude Code: set the stop condition and walk away"
---

> **TL;DR** `/goal <condition>` leaves a persistent note: "don't return control to me until this holds". After every turn, Haiku reads the transcript and decides yes/no against your condition. No → Claude starts another turn automatically. Yes → control returns to you. Use it for sweeping refactors, migrations, or draining an issue queue — anything with a verifiable "done".

There are tasks you know will finish, but they force you to type "keep going" every two turns. Migrating an import across the repo. Getting a legacy test suite to pass. Draining a labeled issue queue. After each turn Claude stops and waits for your nod. `/goal` breaks that cycle: you state the stop condition and stop being a human cron.

## How it works

`/goal` wraps a session-scoped prompt-based [Stop hook](/en/tips/claude-code-hooks-automate-workflow). Every time Claude finishes a turn:

1. The condition and the conversation so far are sent to the small fast model (Haiku by default).
2. The evaluator returns yes/no plus a short reason.
3. "No" → Claude continues, with the reason injected as guidance for the next turn.
4. "Yes" → the goal clears itself and control returns to you.

The evaluator does NOT call tools — it only reads what Claude has already surfaced in the conversation. Conditions must be verifiable from the transcript.

## Result preview

```text
> /goal all tests in test/auth pass and the lint step is clean

◎ /goal active · 0m

# Claude runs npm test → 3 failures
# Evaluator: condition not met — 3 tests still failing in test/auth/*
# Claude fixes the first test → next turn
# Claude fixes the other two → next turn
# npm test green, npm run lint clean
# Evaluator: condition met

◎ /goal cleared — achieved in 4m 12s, 6 turns
```

## How to use it

**1. Set the condition**

```text
/goal all tests in test/auth pass and the lint step is clean
```

Setting the goal starts a turn immediately, with the condition as the directive — no extra prompt needed. Up to 4,000 characters per condition.

**2. Write conditions verifiable from the transcript**

The evaluator only sees what Claude has surfaced in the conversation:

- "`npm test` exits 0" → Claude runs it, the output lands in the transcript
- "every `getUser` call site now reads `fetchUser`" → Claude greps, the result is visible
- "the app is production-ready" → not verifiable, don't use it

Add constraints ("don't touch migrations") and an upper bound ("or stop after 20 turns") when there's a real risk of looping.

**3. Status and cancel**

```text
/goal         # status: condition, turns, time, tokens, last evaluator reason
/goal clear   # cancel (aliases: stop, off, reset, none, cancel)
```

Running `/clear` to start a new conversation also drops the active goal.

**4. Resume across sessions**

If the session ended with an active goal, `claude --resume` or `--continue` restores it. The condition persists; the turn counter and timer reset.

**5. Headless (CI / cron / scripts)**

```bash
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

Single invocation; runs until the condition holds or you hit Ctrl+C.

## /goal vs /loop vs your own Stop hook

| When | Mechanism |
|---|---|
| **`/goal`** | There's a verifiable *done*: migration, refactor, draining an issue queue |
| **[`/loop`](/en/tips/claude-code-loop-recurring-tasks)** | Watch something at intervals: deploys, logs, new PRs |
| **Your own Stop hook** | Deterministic logic in a bash script, or a rule you reuse across sessions |

`/goal` is the closest thing to "Claude, don't come back to me until this is done".

## Reference

| Aspect | Detail |
|---|---|
| Command | `/goal <condition>` · `/goal` (status) · `/goal clear` |
| Active goals | 1 per session |
| Max size | 4,000 characters |
| Evaluator | Configured small fast model (Haiku by default), no tool access |
| Cost | Evaluator tokens, typically negligible vs the main turn |
| Requirements | Trusted workspace, hooks enabled (`disableAllHooks` disables it) |
| Persistence | Survives `--resume` / `--continue` (counters reset) |
| Headless | `claude -p "/goal ..."` runs until met or Ctrl+C |

> Official docs: [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal)
