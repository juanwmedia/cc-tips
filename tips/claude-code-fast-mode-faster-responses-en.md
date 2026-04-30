---
date: 2026-02-21
type: tip
title_es: "Acelera las Respuestas de Claude Code con Fast Mode"
title_en: "Speed Up Claude Code Responses with Fast Mode"
---
# Quick Tip: Speed Up Claude Code Responses with Fast Mode

Fast mode is an Opus 4.6 configuration that prioritizes token generation speed over cost. It's not a different model and not a version with reduced reasoning -- it's the same Opus 4.6 with the same intelligence, just up to 2.5x faster responses. The tradeoff: significantly higher cost per token.

Don't confuse fast mode with effort level adjustment. Lowering effort level does reduce reasoning quality in exchange for speed. Fast mode sacrifices nothing in quality -- only cost.

Result:

```
> /fast

Fast mode ON · $15/$75 per Mtok (50% off through Feb 16)
```

## Setup

**1. Enable fast mode**

Type `/fast` at any point during your session:

```bash
/fast
```

A `↯` icon appears next to the prompt while fast mode is active.

**2. Disable when you don't need it**

```bash
/fast
```

The same command toggles it off. When disabled, you stay on Opus 4.6 (it doesn't revert to your previous model).

**3. Enable by default (optional)**

To keep it always on, add to your user settings:

```json
{
  "fastMode": true
}
```

## Reference

| Aspect | Detail |
|---|---|
| Command | `/fast` (toggle on/off) |
| Model | Opus 4.6 (same model, no quality change) |
| Speed | Up to 2.5x faster output tokens |
| Cost (< 200K) | $30 / $150 per MTok (input / output) |
| Cost (> 200K) | $60 / $225 per MTok (input / output) |
| Discount | 50% off through February 16, 2026 |
| Rate limits | Separate from standard Opus; falls back to standard speed when exhausted |
| Persistence | Persists across sessions |
| Availability | Pro/Max/Team/Enterprise plans with extra usage enabled |

## When to use it

- **Rapid iteration**: code changes where waiting 30 seconds matters.
- **Live debugging**: interactive sessions where every second counts.
- **Deadline-driven work**: when speed justifies the extra cost.

For long autonomous tasks, batch processing, or CI/CD, standard mode is more cost-efficient.

> **Personal note:** Fast mode just launched at the time of writing. In the medium-sized tasks I've been able to test, the speed difference is noticeable, but I'm not yet sure it justifies paying double (2x) compared to standard Opus. During the 50% discount period (through February 16, 2026), fast mode costs the same as standard mode -- at that price, there's no question.

> Official docs: [Speed up responses with fast mode](https://code.claude.com/docs/en/fast-mode)
