---
date: 2026-02-21
type: tip
title_es: "Cómo ajustar el effort level en Claude Code"
title_en: "How to Adjust the Effort Level in Claude Code"
---
# Quick Tip: How to Adjust the Effort Level in Claude Code

When you use `/model` to switch models, it's easy to miss the slider that appears below: use the left/right arrow keys to adjust Opus 4.6's effort level. That slider controls how much reasoning Claude invests before responding. It's not a strict token budget — it's a behavioral signal. At `low`, Claude thinks less and responds faster. At `high` (the default), it dedicates more thinking tokens to complex problems.

Don't confuse effort level with [fast mode](/en/tips/claude-code-fast-mode-faster-responses). Fast mode speeds up token generation without reducing reasoning quality. Lowering effort does reduce reasoning in exchange for speed and cost.

> **TL;DR** Use `/model` + arrow keys to adjust effort on the fly. Or configure it permanently with `effortLevel` in settings or the `CLAUDE_CODE_EFFORT_LEVEL` environment variable.

Result:

```
> /model

  ● opus
    sonnet
    haiku

  Effort: ◄ ██████░░░░ medium ►
```

## 3 ways to configure effort level

### 1. From `/model` (interactive)

Type `/model`, select a supported model (currently Opus 4.6), and use the left/right arrow keys to move the effort slider:

```
/model
```

The change applies immediately to the current session.

### 2. Environment variable

```bash
export CLAUDE_CODE_EFFORT_LEVEL=low
```

Useful for scripts, CI/CD, or batch tasks where you know upfront that operations are simple.

### 3. Settings file

Add `effortLevel` to your `settings.json` (user or project):

```json
{
  "model": "opus",
  "effortLevel": "medium"
}
```

## Reference

| Level | Reasoning | When to use it |
|---|---|---|
| `low` | Minimal — fast and cheap responses | Simple tasks, renames, formatting |
| `medium` | Moderate — speed/quality balance | Daily development, straightforward implementations |
| `high` | Maximum (default) — deep reasoning | Architecture, complex debugging, difficult logic |

## How to monitor it

The effort level is not included in the JSON that the [status line](/en/tips/customize-your-claude-code-status-line) receives by default. But you can read the environment variable directly from your script:

```bash
EFFORT=${CLAUDE_CODE_EFFORT_LEVEL:-high}
```

And add it to your status line next to the model:

```
╸ my-project  main │ Opus (medium) │ ██░░░ 35%
```

You can also see the active model (though not the effort) with `/status`.

> Official docs: [Model configuration — Adjust effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level)
