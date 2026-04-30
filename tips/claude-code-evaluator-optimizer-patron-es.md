---
date: 2026-02-24
type: tip
title_es: "El patrón de Agentic AI que siempre te pone en tu sitio"
title_en: "The Agentic AI Pattern That Always Keeps You Honest"
---
# Quick Tip: El patrón de Agentic AI que siempre te pone en tu sitio

El Evaluator-Optimizer es uno de los cinco patrones de workflow que Anthropic define en [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): un LLM genera, otro evalúa y da feedback en bucle. Claude Code no tiene ese bucle automático — pero puedes construirlo como una inline skill que se invoca bajo demanda.

La clave del patrón: cada claim del output anterior se contrasta contra evidencia real — código fuente, documentación oficial, archivos de configuración. No opiniones. Hechos verificables.

Resultado:

```bash
/evaluate       # 1 pasada de evaluación
/evaluate 2     # 2 pasadas (la segunda evalúa la propia evaluación)
```

## Por qué una skill y no un sub-agente

El evaluador necesita ver lo que se acaba de producir. Un sub-agente o una skill con `context: fork` pierde el contexto de la conversación — tendría que redescubrir todo desde cero.

[Diagram available online — see the full tip at https://wmedia.es/es/tips/claude-code-evaluator-optimizer-patron]

La documentación oficial lo respalda: *"Consider Skills instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context."*

## La skill

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

- `disable-model-invocation: true` — tú decides cuándo evaluar, no Claude
- `allowed-tools` — el evaluador necesita leer y buscar para contrastar claims
- `$ARGUMENTS` — `/evaluate 2` ejecuta dos pasadas; sin argumento, una

## El sistema de veredictos

| Veredicto | Significado |
|---|---|
| `VERIFIED` | Evidencia directa lo respalda |
| `PARTIALLY CORRECT` | La idea central es correcta pero los detalles no |
| `UNVERIFIED` | No se encontró evidencia para confirmar ni negar |
| `INCORRECT` | La evidencia lo contradice directamente |
| `OUTDATED` | Fue correcto en algún momento pero ya no |

Regla: todo veredicto cita una fuente específica — ruta de archivo con línea, URL, output de comando. "Creo que" no es evidencia. Sin fuente = `UNVERIFIED`.

## En la práctica

Usé `/evaluate` sobre el propio análisis que produjo la skill. Resultado: 21 claims, 18 verificados, 3 parcialmente correctos. Ninguno incorrecto — pero tres asunciones sólidas tenían matices que no habría detectado sin el patrón. El artículo completo cubre el proceso de principio a fin: [Evaluator-Optimizer en Claude Code: de patrón a skill](https://wmedia.es/es/articulos/claude-code-evaluator-optimizer-como-skill).

> Official docs: [Skills](https://code.claude.com/docs/en/skills) · [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
