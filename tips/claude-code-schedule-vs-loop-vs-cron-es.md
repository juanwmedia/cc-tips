---
date: 2026-04-08
type: tip
title_es: "Deja de confundir /schedule, /loop y cron en Claude Code"
title_en: "Stop Confusing /schedule, /loop, and Cron in Claude Code"
---
# Quick Tip: Deja de confundir /schedule, /loop y cron en Claude Code

> **TL;DR** Claude Code tiene tres formas nativas de programar trabajo recurrente — `/loop`, Desktop tasks y Cloud tasks — más la opción de toda la vida: cron del sistema con `claude -p`. La diferencia clave en una línea: `/loop` necesita la sesión abierta, las Desktop tasks necesitan la máquina encendida, y las Cloud tasks corren en infraestructura de Anthropic aunque tu portátil esté apagado.

"Tarea recurrente", "cron", "programada" y "schedule" se usan para cosas distintas dentro de Claude Code. `/loop` no es `/schedule`, y ninguno de los dos es lo mismo que montar un cron del sistema. Si los has estado mezclando, aquí está la diferencia en una tabla y la regla para elegir.

Resultado:

```
# /loop — vigila algo mientras sigues trabajando
> /loop 5m check if the staging deploy finished
Loop started (every 5m). Task ID: loop-a1b2c3

# /schedule — crea una tarea Cloud
> /schedule daily PR review at 9am
Setting up a scheduled task. Which repo? Which environment?...
```

## Las tres opciones nativas

| | `/loop` | Desktop task | Cloud task |
|---|---|---|---|
| Se ejecuta en | Tu máquina | Tu máquina | Cloud de Anthropic |
| Necesita sesión abierta | Sí | No | No |
| Necesita la máquina encendida | Sí | Sí | No |
| Sobrevive reinicios | No | Sí | Sí |
| Acceso a archivos locales | Sí | Sí | No (clon fresco del repo) |
| Intervalo mínimo | 1 min | 1 min | 1 hora |
| Expiración automática | 7 días | No | No |
| Cómo se crea | CLI: `/loop <prompt>` | Desktop app → **Schedule** → **New task** → **New local task** | CLI: `/schedule`, o web [claude.ai/code/scheduled](https://claude.ai/code/scheduled), o Desktop app → **New remote task** |

Para reaccionar a eventos en vez de sondear, ninguno de estos es la respuesta correcta — eso son [Channels](/es/tips/claude-code-channels-controlar-desde-telegram).

## Cómo elegir (regla de una línea)

- **Vigilando algo mientras trabajas en tu sesión actual** → `/loop`
- **Tarea diaria con acceso a tu código local** → Desktop task (desde la Desktop app)
- **Tarea que debe correr aunque tu portátil esté apagado** → Cloud task (desde `/schedule` en la CLI o desde la web)
- **Cron del sistema + `claude -p`** → reserva solo para casos raros donde las tres opciones nativas no te encajan

## Setup

### **1. /loop — durante la sesión actual**

```
/loop 15m check open PRs for new comments
```

Corre en segundo plano mientras la sesión esté abierta. Se cancela al cerrar la terminal y expira a los 7 días. El detalle completo, en el tip dedicado a [/loop](/es/tips/claude-code-loop-tareas-recurrentes).

### **2. Desktop task — persistente en tu máquina**

Solo se crean desde la Desktop app: **Schedule** en la sidebar → **New task** → **New local task**. Defines nombre, prompt, frecuencia, permisos y carpeta de trabajo. También puedes pedírselo a Claude en lenguaje natural dentro de cualquier sesión de la Desktop app: *"configura una revisión de código diaria cada mañana a las 9"*.

Corre en tu máquina con acceso a tus archivos locales (incluidos los cambios sin commit) y sobrevive reinicios, pero necesita que el ordenador esté despierto a la hora programada. Si tu portátil duerme a las 9, la tarea se salta (con catch-up al despertar).

### **3. Cloud task — persistente sin tu máquina**

```
/schedule daily code review at 9am
```

Claude te guía conversacionalmente: eliges **repo de GitHub**, **prompt**, **horario**, **environment** (network access, variables de entorno, setup script) y **connectors MCP**. La tarea corre en infraestructura de Anthropic aunque tu portátil esté apagado, pero parte de un clon fresco del repo — no ve tus cambios sin commit. Intervalo mínimo: 1 hora.

También puedes crearlas desde [claude.ai/code/scheduled](https://claude.ai/code/scheduled) o desde la Desktop app eligiendo **New remote task**.

### **4. Cron del sistema (la forma de antes)**

```bash
0 9 * * * claude -p "review my PRs" --allowedTools "Bash(gh *)"
```

Sobrevive a todo. Sin contexto entre ejecuciones. Úsalo solo si las tres opciones nativas no te encajan — que hoy es raro. Ver el tip sobre [headless mode](/es/tips/claude-code-modo-headless-agente-autonomo).

## Por qué existen las tres

`/loop` nació para **vigilar dentro de la sesión**: cada iteración ve tu contexto, los archivos que cambiaste, la conversación entera. Eso es imposible con un cron del sistema, que arranca desde cero cada vez.

**Desktop tasks** y **Cloud tasks** nacieron para **trabajo desatendido y persistente**: cosas que quieres que pasen aunque cierres Claude Code. La diferencia entre ambas es dónde corren y qué ven: Desktop usa tu máquina y tus archivos reales (incluidos cambios sin commit); Cloud usa infraestructura de Anthropic y un clon fresco del repo.

El cron del sistema sigue ahí por **compatibilidad histórica** y casos exóticos, pero hoy las tres opciones nativas cubren el 90% de los casos sin tocar crontab.

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando sesión | `/loop [intervalo] <prompt>` |
| Comando Cloud task | `/schedule <descripción en lenguaje natural>` |
| Desktop tasks | Solo desde la Desktop app (sin comando CLI equivalente) |
| Herramientas internas (session-scoped) | `CronCreate`, `CronList`, `CronDelete` |
| Expresión cron (5 campos) | `minuto hora día-mes mes día-semana` |
| Zona horaria | Local, no UTC |
| Deshabilitar `/loop` + cron de sesión | `CLAUDE_CODE_DISABLE_CRON=1` |

> Documentación oficial: [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) · [Cloud scheduled tasks](https://code.claude.com/docs/en/web-scheduled-tasks) · [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
