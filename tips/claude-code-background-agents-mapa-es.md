---
date: 2026-05-23
type: tip
title_es: "Background agents en Claude Code: el mapa de las cuatro formas de dejar de mirar la terminal"
title_en: "Background agents in Claude Code: the map of four ways to stop watching the terminal"
---
> **TL;DR** Hay cuatro mecanismos en Claude Code para que Claude siga trabajando sin que mires: **Agent View** (`claude agents` o `claude --bg` — sesiones locales persistentes en un supervisor independiente del terminal), **headless mode** (`claude -p` — single-shot, ideal para CI/CD y scripts), **`/loop`** (in-session, repite un prompt a intervalos en una sesión activa) y **Routines** (cloud en claude.ai, recurrentes o disparadas por schedule/API/GitHub). La regla de decisión: ¿corre en tu máquina o en la nube? ¿Una vez o recurrente? ¿Inicio interactivo o disparado por evento externo? Confundirlos es la fuente principal de pérdida de tiempo en setups "autónomos".

"Background agent" no es una sola feature de Claude Code — es **una categoría con cuatro herramientas que se solapan en propósito y divergen en mecanismo**. La gente busca "claude code background agent" y aterriza en el blog de Anthropic sobre autonomía, pero esa página no compara: solo presenta. La pregunta práctica — *cuál de las cuatro necesito hoy* — se queda sin responder.

Lo que comparten: todas dejan a Claude trabajando sin tu input continuo. Lo que las separa: dónde corren, cuánto duran, qué las dispara y qué quota consumen.

Resultado:

```
> claude agents

Pinned
  ✽ payment-retry-fix      Edit src/payments/retry.ts            3m

Ready for review
  ∙ stripe-webhook         github.com/acme/api/pull/2048      ●  2h

Needs input
  ✻ feature-flag-cleanup   needs input: rollout 50% or 100%?     1m

Working
  ✽ flaky-test-investig    run 12 · all checkpoints cleared      4m
  ✢ nightly-deps-check     /loop · next run in 18m
```

Cada fila es una sesión completa de Claude Code corriendo en segundo plano. Cierras el terminal, vuelves mañana, siguen ahí.

## Los cuatro mecanismos

### **1. Agent View (`claude agents`) — sesiones locales persistentes**

```bash
claude agents
# o crear una sin abrir la vista:
claude --bg "investiga el flaky test SettingsChangeDetector"
# o backgroundear la sesión actual:
/bg
```

Un **supervisor local** mantiene N sesiones vivas independientemente del terminal. Cada sesión es una conversación completa de Claude Code con sus skills, hooks, MCPs, permisos. Cierras tu shell — siguen. Reinicia la máquina — fallan, pero las recuperas con un `attach`.

Es la entrada canónica al concepto "background". Cubierto a fondo en [Agent View: una pantalla para todos los agentes que has lanzado](/es/tips/claude-code-agent-view-sesiones-paralelas). Si lo que necesitas es ver qué hay vivo dentro de UNA sesión (subagents, monitores, comandos en background), eso lo gestiona [el panel de Tasks](/es/tips/claude-code-tasks-paralelo) — los dos se complementan: Agent View muestra sesiones; Tasks muestra los tasks dentro de cada sesión.

**Cuándo:** trabajos paralelos en tu máquina (PR review + bug fix + investigación + refactor). Edits aislados en worktrees `.claude/worktrees/` automáticamente — si combinas esto con [worktrees para tareas paralelas](/es/tips/claude-code-worktrees-tareas-paralelas), tienes aislamiento por sesión sin pisar tu rama principal.

### **2. Headless mode (`claude -p`) — single-shot para CI/scripts**

```bash
claude -p "explica el root cause de este error" --bare < build.log
```

No-interactivo, una sola "vuelta" del agente. Lee stdin, escribe stdout, exit code. Es la base del [Agent SDK](/es/tips/claude-agent-sdk-claude-code-desde-tu-codigo) y de [Claude Code en GitHub Actions](/es/tips/claude-code-github-actions-revisar-prs). Cubierto en [headless mode como agente autónomo](/es/tips/claude-code-modo-headless-agente-autonomo).

⚠️ **Caveat de pricing crítico**: a partir del **15 de junio 2026**, `claude -p` en planes de suscripción drena de un **crédito Agent SDK mensual separado** del de uso interactivo. Si tu CI corre mucho, prepárate.

**Cuándo:** CI/CD, scripts de build, hooks de `package.json`, lint con Claude, pipes desde tooling externo.

### **3. `/loop` — recurrencia in-session**

```
> /loop 1h /goal Verifica que el design system sigue pixel-perfect
  contra el último export de Figma y avisa si algo divergió.
```

Repite un prompt cada intervalo (m/h/d) **dentro de una sesión activa**. Se contabiliza como un "Working/sleeping" en Agent View. Útil para monitoring continuo, chequeos periódicos durante una sesión larga. Cubierto en [/loop para tareas recurrentes](/es/tips/claude-code-loop-tareas-recurrentes). El combo más común — `/loop` con [`/goal`](/es/tips/claude-code-goal-condicion-parada) como condición de parada en cada iteración — vive ejemplificado en el [pipeline de pixel-perfect Figma + Chrome MCP](/es/tips/claude-code-figma-chrome-mcp-pixel-perfect). Si lo que quieres es ver los eventos en tiempo real mientras se ejecuta, [el comando Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real) es el complemento natural.

**Cuándo:** chequeos durante una sesión larga (smoke tests durante un refactor, monitoreo de un dev server, polling de un CI lejano). Local, no persiste si cierras la sesión.

### **4. Routines — cloud con triggers**

```
> /schedule daily PR review at 9am
```

Routines corren en **claude.ai/code** (cloud, no tu máquina). Se disparan por:
- **Schedule** (cron, hourly/daily/weekly o one-off natural language)
- **API** (HTTP POST con bearer token, ideal para alertas y deploys)
- **GitHub events** (PR opened, release, etc.)

Tu portátil no necesita estar encendido. Cubierto en [Routines: agentes en la nube con triggers](/es/tips/claude-code-routines-cloud-agents). El mapa completo `/schedule` vs `/loop` vs cron vive en [Schedule vs Loop vs Cron](/es/tips/claude-code-schedule-vs-loop-vs-cron). Si necesitas que la routine te avise por chat sin abrir la web, conéctala con [Channels y Telegram](/es/tips/claude-code-channels-controla-desde-telegram) o [el control remoto desde móvil](/es/tips/claude-code-control-remoto-desde-movil) — son los caminos canónicos para notificación + intervención sin terminal.

**Cuándo:** automation recurrente que debe ejecutarse aunque no estés (nightly PR review, alert triage, docs drift), o triggers de sistemas externos (Sentry → routine, deploy → routine).

## La tabla de decisión

| Pregunta | Agent View | Headless `-p` | `/loop` | Routines |
|---|---|---|---|---|
| ¿Dónde corre? | Local (supervisor) | Local (single-shot) | Local (in-session) | Cloud (claude.ai) |
| ¿Persiste sin terminal? | ✅ Sí | ❌ Acaba al exit | ❌ Solo si la sesión vive | ✅ Sí, siempre |
| ¿Recurrente? | ❌ No nativo | ❌ Llámalo desde cron | ✅ Sí, intervalo fijo | ✅ Sí, cron/eventos |
| ¿Multi-sesión paralela? | ✅ Sí, decenas | Manualmente | ✅ Dentro de una sesión | ✅ Sí |
| ¿Triggers externos? | ❌ No | Stdin / pipe | ❌ No | ✅ API + GitHub webhooks |
| ¿Mi máquina apagada? | ❌ Muere | ❌ N/A | ❌ Muere | ✅ Sigue corriendo |
| ¿Quota? | Tu plan | Hasta jun 2026 plan, después crédito Agent SDK separado | Tu plan | Tu plan + daily routine cap |

## El error más común

> *"Le metí `/loop` para que revisara los PRs cada hora pero al cerrar el portátil dejó de funcionar."*

`/loop` es local in-session. Cierras la sesión → muere. Lo que querías era una **Routine** (cloud + schedule trigger). Patrón inverso: meter en Routine algo que solo tarda 10 segundos y se ejecuta una vez al día — overkill. Para eso `claude --bg` con un nombre claro y listo.

La regla de oro: **¿necesitas que esto sobreviva apagar la máquina?** Si sí, Routine. Si no, las otras tres según el resto del flowchart.

## Referencia rápida

| Necesito | Mecanismo | Comando de entrada |
|---|---|---|
| Lanzar 5 trabajos en paralelo local | Agent View | `claude agents` + `Enter` 5 veces |
| Una tarea en background YA, sin abrir la vista | `--bg` | `claude --bg "<prompt>"` |
| Mover la conversación actual al background | `/bg` | `/bg` dentro de la sesión |
| Lint con Claude en CI | Headless | `claude -p --bare "<prompt>"` |
| Chequeo cada hora mientras programo | `/loop` | `/loop 1h <prompt>` |
| Nightly PR review aunque duerma | Routine | `/schedule daily PR review at 9am` |
| Trigger desde Sentry/deploy | Routine + API | claude.ai/code/routines |

> Documentación oficial: [Agent View](https://code.claude.com/docs/en/agent-view) · [Run Claude Code programmatically (headless)](https://code.claude.com/docs/en/headless) · [Routines](https://code.claude.com/docs/en/routines) · [`/loop` and in-session scheduling](https://code.claude.com/docs/en/scheduled-tasks)

## Requisitos

- **Agent View**: Claude Code v2.1.139+
- **`--permission-mode`/`--effort` en `claude agents`**: v2.1.142+
- **Routines**: plan Pro/Max/Team/Enterprise con Claude Code on the web habilitado
- **Headless con crédito Agent SDK separado**: a partir del 15 de junio 2026
