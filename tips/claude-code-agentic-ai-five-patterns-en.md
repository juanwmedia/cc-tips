---
date: 2026-02-24
type: tip
title_es: "4 patrones Agentic AI en Claude Code que ya usas y uno que no conoces"
title_en: "4 Agentic AI Patterns You Already Use in Claude Code — and One You Don't"
---
# Quick Tip: 4 Agentic AI Patterns You Already Use in Claude Code — and One You Don't

In December 2024, Anthropic published [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — five workflow patterns for LLM-based systems. What's not obvious: Claude Code already implements four of them natively. The fifth requires a design decision.

I've been studying and applying these patterns as part of my professional practice in Agentic AI. This map shows how each one connects to Claude Code's primitives.

Result:

```
Anthropic Pattern           → Claude Code Primitive
─────────────────────────────────────────────────────
Prompt Chaining             → Plan mode + Skills
Routing                     → Conditional CLAUDE.md
Parallelization             → Sub-agents / Agent Teams
Orchestrator-Workers        → Task tool (sub-agents)
Evaluator-Optimizer         → Inline skill (/evaluate)
```

## The 5 patterns

### 1. Prompt Chaining — Sequential steps

Decompose a task into sequential steps where each LLM processes the previous one's output. In Claude Code: plan mode to design the sequence, skills to execute each step as a slash command.

### 2. Routing — Direct to the right path

Classify the input and route to the appropriate handler. In Claude Code: conditional rules in CLAUDE.md that activate behaviors based on project context.

### 3. Parallelization — Divide and conquer

Execute sub-tasks simultaneously. In Claude Code: sub-agents working in parallel with isolated contexts, or agent teams for coordinated collaboration.

### 4. Orchestrator-Workers — One director, many executors

A central agent that delegates, coordinates, and synthesizes. In Claude Code: the Task tool launches specialized sub-agents and collects their results. You see this every time Claude delegates a search to an Explore sub-agent.

### 5. Evaluator-Optimizer — Generate, evaluate, iterate

One LLM generates, another evaluates and provides feedback in a loop. Claude Code doesn't have this as a native automatic loop — the solution: an [inline skill that acts as an evidence-based auditor](https://wmedia.es/en/writing/claude-code-evaluator-optimizer-as-skill). The hardest pattern to place, and the one that adds the most value in complex tasks.

## Quick reference

| Pattern | Claude Code Primitive | When to use |
|---|---|---|
| Prompt Chaining | Plan mode + Skills | Tasks with clear phases (research → design → implement) |
| Routing | Conditional CLAUDE.md | Multi-stack projects or context-dependent rules |
| Parallelization | Sub-agents / Agent Teams | Independent tasks that don't share state |
| Orchestrator-Workers | Task tool | Complex tasks requiring central coordination |
| Evaluator-Optimizer | Inline skill | Validate plans, reports, or critical implementations |

> The key is knowing Claude Code's [6 extension points](https://wmedia.es/en/tips/claude-code-skills-hooks-mcp-plugins-comparison) and matching each pattern to the right one. These patterns aren't theoretical — they're architecture decisions you make every time you design a workflow.

> Official docs: [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) · [Skills](https://code.claude.com/docs/en/skills) · [Sub-agents](https://code.claude.com/docs/en/sub-agents)
