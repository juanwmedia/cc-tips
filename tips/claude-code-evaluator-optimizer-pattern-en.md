---
date: 2026-02-24
type: tip
title_es: "El patrón de Agentic AI que siempre te pone en tu sitio"
title_en: "The Agentic AI Pattern That Always Keeps You Honest"
---
# Quick Tip: The Agentic AI Pattern That Always Keeps You Honest

The Evaluator-Optimizer is one of five workflow patterns Anthropic defines in [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): one LLM generates, another evaluates and provides feedback in a loop. Claude Code doesn't have that automatic loop — but you can build it as an inline skill invoked on demand.

The pattern's core: every claim from the previous output is checked against real evidence — source code, official documentation, configuration files. Not opinions. Verifiable facts.

Result:

```bash
/evaluate       # 1 evaluation pass
/evaluate 2     # 2 passes (the second evaluates the evaluation itself)
```

## Why a skill, not a sub-agent

The evaluator needs to see what was just produced. A sub-agent or a skill with `context: fork` loses conversation context — it would have to rediscover everything from scratch.

[Diagram available online — see the full tip at https://wmedia.es/en/tips/claude-code-evaluator-optimizer-pattern]

The official documentation backs this: *"Consider Skills instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context."*

## The skill

```yaml
---
name: evaluate
description: Evaluator-Optimizer pattern. Critically evaluates every claim,
  decision, and assertion from the previous output against verifiable evidence
  from code, documentation, configuration, and other sources.
disable-model-invocation: true
argument-hint: [passes]
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---
```

- `disable-model-invocation: true` — you decide when to evaluate, not Claude
- `allowed-tools` — the evaluator needs to read and search to verify claims
- `$ARGUMENTS` — `/evaluate 2` runs two passes; no argument runs one

## The verdict system

| Verdict | Meaning |
|---|---|
| `VERIFIED` | Direct evidence supports it |
| `PARTIALLY CORRECT` | Core idea holds but details are wrong |
| `UNVERIFIED` | No evidence found to confirm or deny |
| `INCORRECT` | Evidence directly contradicts it |
| `OUTDATED` | Was true at some point but current state differs |

Rule: every verdict cites a specific source — file path with line number, URL, command output. "I believe" is not evidence. No source = `UNVERIFIED`.

## In practice

I ran `/evaluate` on the very analysis that produced the skill. Result: 21 claims, 18 verified, 3 partially correct. None incorrect — but three solid assumptions had nuances I wouldn't have caught without the pattern. The full article covers the process end to end: [Evaluator-Optimizer in Claude Code: From Pattern to Skill](https://wmedia.es/en/writing/claude-code-evaluator-optimizer-as-skill).

> Official docs: [Skills](https://code.claude.com/docs/en/skills) · [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
