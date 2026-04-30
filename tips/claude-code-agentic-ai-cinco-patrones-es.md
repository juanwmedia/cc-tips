---
date: 2026-02-24
type: tip
title_es: "4 patrones Agentic AI en Claude Code que ya usas y uno que no conoces"
title_en: "4 Agentic AI Patterns You Already Use in Claude Code — and One You Don't"
---
# Quick Tip: 4 patrones Agentic AI en Claude Code que ya usas y uno que no conoces

En diciembre de 2024, Anthropic publicó [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — cinco patrones de workflow para sistemas con LLMs. Lo que no es obvio: Claude Code ya implementa cuatro de ellos nativamente. El quinto requiere una decisión de diseño.

Llevo meses aplicando estos patrones como parte de mi práctica profesional en Agentic AI. Este mapa resume cómo se conecta cada uno con las primitivas de Claude Code.

Resultado:

```
Patrón Anthropic            → Primitiva Claude Code
─────────────────────────────────────────────────────
Prompt Chaining             → Plan mode + Skills
Routing                     → CLAUDE.md condicional
Parallelization             → Sub-agents / Agent Teams
Orchestrator-Workers        → Task tool (sub-agents)
Evaluator-Optimizer         → Inline skill (/evaluate)
```

## Los 5 patrones

### 1. Prompt Chaining — Encadenar pasos

Descomponer una tarea en pasos secuenciales donde cada LLM procesa el output del anterior. En Claude Code: plan mode para diseñar la secuencia, skills para ejecutar cada paso como un slash command.

### 2. Routing — Dirigir al camino correcto

Clasificar el input y derivar a la ruta apropiada. En Claude Code: reglas condicionales en CLAUDE.md que activan comportamientos según el contexto del proyecto.

### 3. Parallelization — Dividir y conquistar

Ejecutar sub-tareas simultáneamente. En Claude Code: sub-agents que trabajan en paralelo con contextos aislados, o agent teams para colaboración coordinada.

### 4. Orchestrator-Workers — Un director, varios ejecutores

Un agente central que delega, coordina y sintetiza. En Claude Code: el Task tool lanza sub-agentes especializados y recoge sus resultados. Lo usas cada vez que Claude delega una búsqueda a un Explore sub-agent.

### 5. Evaluator-Optimizer — Generar, evaluar, iterar

Un LLM genera, otro evalúa y da feedback en bucle. En Claude Code no existe nativamente como bucle automático — la solución: una [inline skill que actúa como auditor basado en evidencia](https://wmedia.es/es/articulos/claude-code-evaluator-optimizer-como-skill). El patrón más difícil de ubicar, y el que más valor aporta en tareas complejas.

## Referencia rápida

| Patrón | Primitiva Claude Code | Cuándo usarlo |
|---|---|---|
| Prompt Chaining | Plan mode + Skills | Tareas con fases claras (investigar → diseñar → implementar) |
| Routing | CLAUDE.md condicional | Proyectos multi-stack o con reglas por contexto |
| Parallelization | Sub-agents / Agent Teams | Tareas independientes que no comparten estado |
| Orchestrator-Workers | Task tool | Tareas complejas que requieren coordinación central |
| Evaluator-Optimizer | Inline skill | Validar planes, reportes o implementaciones críticas |

> La clave está en conocer los [6 mecanismos de extensión](https://wmedia.es/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa) de Claude Code y saber cuál corresponde a cada patrón. Los patrones no son teóricos — son decisiones de arquitectura que tomas cada vez que diseñas un workflow.

> Official docs: [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) · [Skills](https://code.claude.com/docs/en/skills) · [Sub-agents](https://code.claude.com/docs/en/sub-agents)
