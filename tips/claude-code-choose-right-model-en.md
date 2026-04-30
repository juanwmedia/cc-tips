---
date: 2026-03-02
type: tip
title_es: "Cómo elegir el modelo adecuado en Claude Code"
title_en: "How to Choose the Right Model in Claude Code"
---
# Quick Tip: How to Choose the Right Model in Claude Code

Not every task needs the frontier model. A frontier model is the most advanced, capable model available at any given time — right now, that's Opus 4.6. It's tempting to use it for everything: if you have access to the best, why settle for less? But doing so wastes tokens, wait time, and resources. Most daily development tasks don't require deep reasoning.

Claude Code already applies this logic internally. Its Explore agent runs on Haiku for fast codebase searches. The `opusplan` alias automates the full strategy: Opus reasons through planning, Sonnet handles execution.

> **TL;DR** Use `opusplan` to plan with Opus and execute with Sonnet. Switch to Haiku for quick exploration. Don't use the frontier model for everything — allocate power where it actually matters.

Result:

```
> /model

    default
  ● opusplan   ← Plan: Opus 4.6 · Execution: Sonnet 4.6
    opus
    sonnet
    haiku
```

## The strategy: plan, execute, explore

**1. Plan with the frontier model**

Deep reasoning is only justified when designing architecture, evaluating trade-offs, or making decisions that affect the entire project. This is where Opus makes the difference.

```bash
claude --model opus
# Or switch mid-session:
/model opus
```

**2. Execute with Sonnet**

Writing functions, tests, refactoring — doesn't need the same level of reasoning. Sonnet 4.6 delivers comparable intelligence at lower cost and higher speed.

```bash
/model sonnet
```

**3. Explore with Haiku**

Codebase searches, file reads, structure analysis. Read-only tasks where speed matters more than depth.

```bash
/model haiku
```

**4. The shortcut: `opusplan`**

If you don't want to switch manually, `opusplan` automates the strategy:

```bash
claude --model opusplan
# Or during a session:
/model opusplan
```

Opus activates during plan mode. When Claude transitions to execution, it switches to Sonnet automatically. This is exactly what Claude Code's native agents do — each task gets the right model for the job.

## Reference

| Model | Alias | Relative cost | Best for |
|---|---|---|---|
| Opus 4.6 | `opus` | $$$ | Architecture, complex debugging, design decisions |
| Sonnet 4.6 | `sonnet` | $$ | Daily development, implementation, tests |
| Haiku 4.5 | `haiku` | $ | Exploration, searches, simple tasks |
| Opus → Sonnet | `opusplan` | Mixed | Full workflow: plan + execute |

## Permanent configuration

Add the model to your `settings.json` so you don't have to choose every session:

```json
{
  "model": "opusplan"
}
```

Or via environment variable:

```bash
export ANTHROPIC_MODEL=opusplan
```

If you want to further fine-tune Opus's reasoning during the planning phase, combine this strategy with [Claude Code effort level adjustment](/en/tips/claude-code-effort-level-adjust-reasoning): lower the effort for quick decisions and reserve `high` for architectural ones.

> Official docs: [Model configuration](https://code.claude.com/docs/en/model-config)
