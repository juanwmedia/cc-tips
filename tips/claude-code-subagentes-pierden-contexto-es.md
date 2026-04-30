---
date: 2026-03-28
type: tip
title_es: "Por qué tus subagentes devuelven resultados incompletos en Claude Code"
title_en: "Why Your Sub-Agents Return Incomplete Results in Claude Code"
---
# Quick Tip: Por qué tus subagentes devuelven resultados incompletos en Claude Code

> **TL;DR** Los subagentes arrancan con contexto cero — no heredan tu conversación. Solo reciben la query que Claude les escribe. Si esa query no incluye el objetivo real, el resumen que devuelven será incompleto. La solución: incluir el por qué en la delegación, precargar contexto con skills, y pedir follow-up para que Claude reanude el mismo subagente sin perder el hilo.

Cuando Claude Code delega una tarea a un subagente, ese subagente arranca desde cero. Su propia ventana de contexto, su propio system prompt, su propia carga de CLAUDE.md. No hereda nada de tu conversación. Solo recibe una query que Claude escribe basándose en lo que le pediste.

El problema: esa query es literal, no semántica. Si le pides "investiga cómo funciona el middleware de auth", el subagente lee archivos, resume funciones e imports, y devuelve un resumen. Pero no te dice que hay un edge case con tokens expirados — porque no sabe que estás refactorizando por un bug de tokens. Tú tenías ese contexto. El subagente no.

Los números lo confirman: un subagente puede leer 6.100 tokens de archivos y devolver un resumen de 420 tokens. Esa compresión es la razón de ser del mecanismo — protege tu contexto principal. Pero también es donde se pierden los detalles que importan.

Resultado — un subagente que pierde información crítica:

```
# Tu conversación principal tiene contexto completo:
# - Estás refactorizando auth por un bug de tokens expirados
# - El edge case está en refreshToken()
# - Necesitas saber si el middleware actual lo maneja

# Claude delega al subagente:
> "Investiga cómo funciona el middleware de auth actual"

# El subagente devuelve:
> "El middleware usa express-jwt, valida tokens en cada request,
>  y tiene 3 rutas protegidas. Estructura: middleware/auth.js,
>  utils/token.js, routes/protected.js"

# Falta: el edge case de refreshToken() — la razón real de la tarea
```

## Cómo solucionarlo

### **1. Incluir el objetivo, no solo la pregunta**

Cuando delegues trabajo a un subagente, no le pidas qué investigar. Dile POR QUÉ lo investigas:

```
# Malo — solo la query literal:
"Investiga el middleware de auth"

# Bueno — query + objetivo:
"Investiga el middleware de auth. El objetivo es refactorizarlo
porque hay un bug con tokens expirados en refreshToken().
Necesito saber específicamente cómo se manejan los tokens
expirados y si hay edge cases en la renovación."
```

El subagente con contexto objetivo priorizará la información relevante en su resumen.

### **2. Precargar contexto con skills**

Si tu subagente necesita contexto que no está en los archivos, precárgalo en su definición:

```markdown
# .claude/agents/auth-investigator.md
---
name: auth-investigator
description: Investigates auth-related code with security focus.
tools: Read, Grep, Glob
model: sonnet
skills:
  - auth-context
---

You are an auth security investigator. When analyzing auth code:
1. Always check token expiration handling.
2. Look for race conditions in token refresh.
3. Report edge cases explicitly.
```

El campo `skills` inyecta el contenido completo de esas skills en el system prompt del subagente. No es una referencia — es inyección directa.

### **3. Iterative retrieval — no aceptes la primera respuesta**

Este enfoque se conoce como iterative retrieval — un patrón establecido en information retrieval (formalizado en RAG por Iter-RetGen, EMNLP 2023) que aplicado a agentes significa: no aceptes la primera respuesta si está incompleta.

Cuando un subagente devuelve un resumen incompleto, no lances otro desde cero. Pídele a Claude que profundice. Internamente, Claude reanuda el mismo subagente con todo su contexto previo — no arranca uno nuevo:

```
# El subagente devolvió un resumen incompleto.
# Dile a Claude que profundice:

> "El resumen no menciona cómo se manejan los tokens
>  expirados. Pide al subagente que revise refreshToken()
>  en utils/token.js y reporte el flujo de renovación."

# Claude reanuda el mismo subagente internamente.
# El subagente retoma con todo su historial de lecturas
# y razonamiento. No necesita volver a leer los archivos.
```

La clave: tú hablas con Claude en lenguaje natural. Claude gestiona la reanudación del subagente por debajo. No necesitas conocer IDs ni herramientas internas.

### **4. Diseñar subagentes enfocados**

Un subagente que "investiga todo" devuelve resúmenes genéricos. Un subagente con un rol específico sabe qué priorizar:

```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security issues, token handling, and auth vulnerabilities.
tools: Read, Grep, Glob
model: sonnet
---

Focus exclusively on:
1. Token validation and expiration.
2. Auth bypass possibilities.
3. Race conditions in session management.
Ignore: styling, formatting, naming conventions.
```

## Referencia

| Concepto | Detalle |
|---|---|
| Contexto | Independiente — no hereda la conversación principal. |
| Qué recibe | System prompt propio + query de Claude + CLAUDE.md + skills + MCPs configurados. |
| Qué devuelve | Solo el texto final del resumen + metadata de tokens y duración. |
| Follow-up | Pídelo en lenguaje natural. Claude reanuda el mismo subagente internamente. |
| Precargar contexto | Campo `skills` en la definición — inyecta contenido completo en el system prompt. |
| Controlar herramientas | `tools` (allowlist) o `disallowedTools` (denylist) en el frontmatter. |
| Modelo | Configurable por subagente: `sonnet`, `opus`, `haiku` o `inherit`. |
| Límite de turnos | `maxTurns` — limita cuántas iteraciones puede hacer el subagente. |
| Recursión | No soportada — un subagente no puede lanzar otros subagentes. |
| Transcripciones | `~/.claude/projects/{project}/{session}/subagents/agent-{id}.jsonl` |

> Documentación oficial: [Sub-agents](https://code.claude.com/docs/en/sub-agents)
