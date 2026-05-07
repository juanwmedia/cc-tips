---
date: 2026-05-07
type: tip
title_es: "Loop, Routines, Monitor en Claude Code: el mapa para no equivocarte de herramienta"
title_en: "Loop, Routines, Monitor in Claude Code: the map so you don't pick the wrong one"
---

> **TL;DR** Todas las primitivas de Claude Code para "que el agente trabaje cuando tú no estás" caben en una matriz 2×3. Eje horizontal: qué lo despierta — un **reloj** (cron) o un **evento** (una línea, un PR, un webhook). Eje vertical: dónde corre — tu **sesión** activa, tu **Mac** persistente, o el **cloud** de Anthropic. Una celda, una primitiva. Si conoces la celda, el nombre da igual.

Anthropic ha apilado seis primitivas distintas en menos de un año: `/loop`, [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real), Desktop scheduled tasks, [Routines](/es/tips/claude-code-routines-cloud-agents), [Channels](/es/tips/claude-code-channels-controla-desde-telegram), y el viejo `cron + claude -p` ([headless mode](/es/tips/claude-code-modo-headless-agente-autonomo)). Cada una se llama distinto en CLI, Web y Desktop app. Y elegir mal te cuesta tokens, sesiones perdidas, o un agente que muere cuando cierras la tapa.

Hay un mapa.

## Las dos dimensiones que lo explican todo

**Dimensión 1 — qué despierta a Claude:**

- **Time-driven**: un reloj. "Cada 5 minutos", "todos los días a las 9". Útil para checks periódicos donde el momento es lo que importa.
- **Event-driven**: algo que pasa. Una línea en un log, un PR que se abre, un webhook que llega. Útil cuando el silencio cuesta cero y solo quieres reaccionar a *eso*.

**Dimensión 2 — dónde corre Claude:**

- **Intra-sesión**: tu terminal abierto ahora. Si la cierras, se acabó. Acceso a archivos locales y al contexto de la conversación.
- **Local persistente**: tu Mac, gestionado por la Desktop app. Sobrevive reinicios, pero necesita que la máquina esté despierta.
- **Cloud**: VMs de Anthropic. Sigue funcionando con el portátil cerrado. Parte de un clon fresco del repo.

## La matriz 2×3 (todas las primitivas en una celda)

| | **Time-driven** (reloj) | **Event-driven** (evento) |
|---|---|---|
| **Intra-sesión** | `/loop` | [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real) |
| **Local persistente** | Desktop scheduled task | [Channels](/es/tips/claude-code-channels-controla-desde-telegram) (push externo) |
| **Cloud (Anthropic)** | [Routine](/es/tips/claude-code-routines-cloud-agents) con trigger Schedule | [Routine](/es/tips/claude-code-routines-cloud-agents) con trigger GitHub o API |

Cada celda contesta dos preguntas: *qué despierta a Claude* y *dónde corre*. Eso es todo.

## Cómo elegir en 3 preguntas

1. **¿Lo necesito mientras estoy trabajando ahora, en esta sesión?** → fila *Intra-sesión*. Si el disparador es tiempo, [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes). Si es evento (una línea de log, salida de stdout), [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real).
2. **¿Lo necesito recurrente, pero solo cuando mi Mac está encendido?** → fila *Local persistente*. Tarea programada → Desktop scheduled task. Notificación push (Telegram, Discord) → [Channels](/es/tips/claude-code-channels-controla-desde-telegram).
3. **¿Tiene que correr de forma fiable aunque cierre el portátil?** → fila *Cloud*. Schedule, GitHub event o API webhook, todo cae en una [Routine](/es/tips/claude-code-routines-cloud-agents).

Si tu pregunta es "¿qué tengo corriendo ahora mismo?" — eso es el [panel `/tasks`](/es/tips/claude-code-tasks-paralelo). Es el dashboard, no una primitiva.

## La jungla de nombres (lo mismo se llama distinto en cada superficie)

| Concepto | CLI | Web (claude.ai/code) | Desktop app |
|---|---|---|---|
| Cloud agent | `/schedule` (alias `/routines`) | Routines | sidebar **Routines** → **New routine** → **Remote** |
| Local scheduled task | (no hay equivalente CLI) | (no hay) | sidebar **Routines** → **New routine** → **Local** |
| Intra-session loop | `/loop` (alias `/proactive`) | (no hay — necesita CLI vivo) | (no hay) |
| Stop polling, watch events | Monitor tool (built-in) | (no hay) | (no hay) |

**El lío más caro**: `/schedule` en el CLI **NO** crea una scheduled task local en tu Mac — crea una Routine en cloud. Si quieres tareas locales del Desktop, abre la Desktop app y elige **Local**.

## El detalle que poca gente conoce

`/loop` y Monitor están integrados a propósito. Si lanzas `/loop check si pasó el CI` **sin intervalo**, Claude se autopaca — y puede decidir bajarse a Monitor por debajo si polling es la forma cara. Lo dice [la doc oficial](https://code.claude.com/docs/en/scheduled-tasks#let-claude-choose-the-interval) literal:

> *"When you ask for a dynamic `/loop` schedule, Claude may use the Monitor tool directly. Monitor [...] avoids polling altogether and is often more token-efficient."*

Tú pides "vigila esto"; Claude elige el mecanismo.

## Referencia rápida

| Primitiva | Persistencia | Min interval | Mejor para |
|---|---|---|---|
| [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes) | Solo sesión activa (auto-expira a 7d) | 1 min | Vigilar mientras trabajas |
| [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real) | Solo sesión activa | Eventos asíncronos | Tail de logs, esperar señales |
| Desktop scheduled task | Mac despierta | 1 min | Tareas con archivos locales |
| [Channels](/es/tips/claude-code-channels-controla-desde-telegram) | Mientras tu CLI esté listening | Push externo | Recibir órdenes desde Telegram/Discord |
| [Routine schedule](/es/tips/claude-code-routines-cloud-agents) | Cloud, siempre | 1 hora | Cron desatendido sin tu Mac |
| [Routine event](/es/tips/claude-code-routines-cloud-agents) | Cloud, siempre | Webhook / GitHub event | PR review automático, alert triage |

> Documentación oficial: [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) · [Routines](https://code.claude.com/docs/en/routines) · [Monitor tool reference](https://code.claude.com/docs/en/tools-reference#monitor-tool)
