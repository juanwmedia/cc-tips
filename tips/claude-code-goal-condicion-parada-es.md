---
date: 2026-05-03
type: tip
title_es: "/goal en Claude Code: define la condición de parada y vete a otra cosa"
title_en: "/goal in Claude Code: set the stop condition and walk away"
---

> **TL;DR** `/goal <condición>` deja una nota persistente: "no me devuelvas el control hasta que esto se cumpla". Tras cada turno, Haiku lee la transcripción y decide sí o no contra tu condición. Si no → Claude lanza otro turno automáticamente. Si sí → vuelves al prompt. Sirve para refactors masivos, migraciones o vaciar colas de issues — cualquier cosa con un "done" verificable.

Hay tareas que sabes que terminarán, pero te obligan a escribir "sigue" cada dos turnos. Migrar un import por todo el repo. Hacer que pase un test suite legacy. Vaciar una cola de issues etiquetados. Tras cada turno Claude para y espera tu OK. `/goal` rompe ese ciclo: defines la condición de parada y dejas de hacer de cron humano.

## Cómo funciona

`/goal` envuelve un [Stop hook](/es/tips/claude-code-hooks-automatizar-flujo-trabajo) prompt-based con vida útil de sesión. Cada vez que Claude termina un turno:

1. La condición y la transcripción se mandan al modelo rápido (Haiku por defecto).
2. El evaluador devuelve sí/no más una razón corta.
3. "No" → Claude continúa, con la razón inyectada como guía del siguiente turno.
4. "Sí" → el goal se borra solo y vuelves al control.

El evaluador NO ejecuta herramientas — solo lee lo que Claude ya ha escrito en la conversación. Por eso las condiciones tienen que ser verificables desde la transcripción.

## Vista previa

```text
> /goal todos los tests en test/auth pasan y el lint queda limpio

◎ /goal active · 0m

# Claude ejecuta npm test → 3 fallos
# Evaluador: condición no cumplida — 3 tests fallan en test/auth/*
# Claude arregla el primer test → siguiente turno
# Claude arregla los otros dos → siguiente turno
# npm test verde, npm run lint limpio
# Evaluador: condición cumplida

◎ /goal cleared — logrado en 4m 12s, 6 turnos
```

## Cómo usarlo

**1. Define la condición**

```text
/goal todos los tests en test/auth pasan y el lint queda limpio
```

Al setear el goal arranca un turno inmediatamente con la condición como directiva — no hace falta prompt adicional. Hasta 4000 caracteres por condición.

**2. Escribe condiciones verificables desde la transcripción**

El evaluador solo lee lo que Claude ha surfaceado en la conversación:

- "`npm test` exit code 0" → Claude ejecuta el comando, la salida queda en la transcripción
- "todos los call sites de `getUser` ahora son `fetchUser`" → Claude lo grepa, la salida queda visible
- "el app está listo para producción" → no es verificable, no lo uses

Añade constraints ("sin tocar migrations") y un tope ("o para tras 20 turnos") cuando el riesgo de bucle sea real.

**3. Estado y cancelación**

```text
/goal         # estado: condición, turnos, tiempo, tokens, última razón
/goal clear   # cancela (alias: stop, off, reset, none, cancel)
```

`/clear` también borra el goal activo.

**4. Resume entre sesiones**

Si la sesión acaba con un goal activo, `claude --resume` o `--continue` lo restaura. La condición persiste; el contador de turnos y el tiempo se resetean.

**5. Headless (CI / cron / scripts)**

```bash
claude -p "/goal CHANGELOG.md tiene una entrada por cada PR mergeado esta semana"
```

Una sola invocación, corre hasta cumplir la condición o hasta Ctrl+C.

## /goal vs /loop vs Stop hook propio

| Cuándo | Mecanismo |
|---|---|
| **`/goal`** | Hay un *done* verificable: migración, refactor, vaciar issue queue |
| **[`/loop`](/es/tips/claude-code-loop-tareas-recurrentes)** | Vigilar algo en intervalos: deploys, logs, PRs nuevos |
| **Stop hook propio** | Lógica determinista en script bash, o regla reutilizada en cada sesión |

`/goal` es lo más cercano a "Claude, no vuelvas a por mí hasta que esto esté hecho".

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/goal <condición>` · `/goal` (estado) · `/goal clear` |
| Goals activos | 1 por sesión |
| Tamaño máximo | 4000 caracteres |
| Evaluador | Modelo rápido configurado (Haiku por defecto), sin acceso a herramientas |
| Coste | Tokens del evaluador, despreciables vs el turno principal |
| Requisitos | Workspace de confianza, hooks habilitados (`disableAllHooks` lo deshabilita) |
| Persistencia | Sobrevive a `--resume` / `--continue` (resetea contadores) |
| Headless | `claude -p "/goal ..."` corre hasta cumplir o Ctrl+C |

> Documentación oficial: [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal)
