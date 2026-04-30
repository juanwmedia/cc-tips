---
date: 2026-04-16
type: tip
title_es: "/ultrareview en Claude Code: la revisión que no quieres pero vas a necesitar"
title_en: "/ultrareview in Claude Code: The Review You Don't Want but Definitely Need"
---

> **TL;DR** `/ultrareview` es un comando nuevo de Claude Code que lanza una **flota de agentes revisores en la nube** para cazar bugs antes de mergear. Cada hallazgo se reproduce y verifica de forma independiente — nada de "podrías considerar usar const". Tres pases gratis en Pro y Max, y todo corre en segundo plano mientras tú sigues trabajando.

## Cómo funciona

`/ultrareview` aterrizó en Claude Code el 16 de abril de 2026 junto con [Opus 4.7](/es/tips/claude-code-opus-4-7) — es uno de los cambios grandes de ese lanzamiento.

Cuando lo ejecutas, Claude Code sube el estado de tu rama (o clona tu PR de GitHub si pasas un número) a [la misma infraestructura en la nube](/es/tips/claude-code-sesiones-en-la-nube) que ya usa para sesiones remotas, y orquesta **múltiples agentes revisores en paralelo**. Cada uno explora el cambio desde un ángulo distinto: lógica, edge cases, seguridad, performance. Lo que distingue a `/ultrareview` del [`/review` local](https://code.claude.com/docs/en/commands) es que **cada hallazgo se reproduce de forma independiente antes de reportarlo**. Si el bug no se puede verificar, no aparece.

Es el equivalente a poner a un senior paranoico durante 15 minutos solo a leer tu diff.

## Qué verás cuando arranque

```bash
$ /ultrareview 1234

Ultrareview scope:
  PR #1234 — feat: add rate limiting middleware
  Files changed: 8 · Lines: +342 / -56

Free runs remaining: 2/3
Estimated cost: 0 credits (within free runs)

[Confirm to launch review in background? y/n]

✔ Review started. Track with /tasks
```

## Cómo usarlo

**1. Actualiza Claude Code a 2.1.86 o superior** y autentícate con tu cuenta Claude.ai (no funciona con API key sola):

```bash
claude update
/login
```

**2. Revisa los cambios de tu rama actual** vs la rama por defecto — incluye uncommitted y staged:

```bash
/ultrareview
```

**3. Revisa un PR concreto de GitHub** (requiere un remote `github.com`):

```bash
/ultrareview 1234
```

**4. Sigue la revisión en segundo plano**. Tarda 10–20 minutos y no bloquea la sesión. Puedes cerrar Claude Code y volver después — la tarea sigue corriendo:

```bash
/tasks   # ver revisiones en curso y completadas
```

**5. Cuando termine**, te llegan los hallazgos verificados con archivo, línea y explicación. Pide a Claude que los arregle directamente desde los resultados.

## /review vs /ultrareview

La comparativa a tener clara antes de elegir uno u otro:

| Criterio | `/review` | `/ultrareview` |
|---|---|---|
| Ejecución | Local, en tu sesión | Sandbox en la nube |
| Profundidad | Una pasada | Múltiples agentes en paralelo con verificación independiente |
| Duración | Segundos a minutos | 10–20 minutos |
| Coste | Cuenta como uso normal | 3 pases gratis, después [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Ideal para | Feedback rápido mientras iteras | Confianza antes de mergear cambios grandes |

## Referencia

| Campo | Valor |
|---|---|
| Comando | `/ultrareview [PR]` |
| Versión mínima | Claude Code 2.1.86 |
| Autenticación | Claude.ai (no funciona solo con API key) |
| Planes con pases gratis | Pro y Max · 3 pases **one-time** |
| Team y Enterprise | Sin pases gratis, se factura como extra usage |
| No disponible en | Bedrock, Vertex AI, Foundry, organizaciones con Zero Data Retention |
| Seguimiento | `/tasks` |
| Modo sin argumentos | Compara el branch actual vs el branch por defecto (incluye uncommitted) |
| Modo con argumento | Clona el PR directamente desde GitHub |

## Cuándo vale cada pase

Los tres pases gratis son **one-time** — no se renuevan cada mes. Gástalos con cabeza: no los uses para PRs triviales. El valor está en cambios grandes, refactors amplios, o código de negocio crítico (pagos, auth, migrations) donde un bug en producción cuesta más que los 10 minutos que tarda la revisión.

Si ya agotaste los tres, el coste sigue siendo mucho menor que el de una incidencia en producción — y [trackear el uso](/es/tips/claude-code-uso-tokens-usage-stats) con `/usage` te deja controlar el gasto.

Y si lo que quieres es la fase opuesta — razonar un cambio grande **antes** de escribir una sola línea — `/ultrareview` tiene [su contrapartida de planificación en la nube](/es/tips/claude-code-ultraplan-planificacion-nube): `/ultraplan`.

> Docs oficiales: [Find bugs with ultrareview](https://code.claude.com/docs/en/ultrareview) · [Commands reference](https://code.claude.com/docs/en/commands)
