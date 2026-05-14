---
date: 2026-05-13
type: tip
title_es: "Agent View en Claude Code: una sola pantalla para todos los agentes que has lanzado"
title_en: "Agent View in Claude Code: one screen for every agent you've dispatched"
---

> **TL;DR** `claude agents` abre un panel donde cada fila es una sesión de Claude Code en segundo plano. Ves en un vistazo cuál te pregunta algo, cuál sigue trabajando, cuál terminó. Las sesiones siguen vivas aunque cierres la terminal — un supervisor por usuario las hospeda. Tres formas de despachar: desde la propia vista, `/bg` dentro de una sesión, o `claude --bg "tarea"` desde el shell. Peek con `Space` para responder sin attach. Enter para entrar en la conversación completa. Es el [panel `/tasks`](/es/tips/claude-code-tasks-paralelo) pero a nivel sesión, no de tarea intra-sesión.

Lanzas un bug fix en una terminal. Una revisión de PR en otra. Un agente que investiga un test flaky en una tercera. A los 20 minutos tienes siete pestañas abiertas, no recuerdas cuál estaba esperando respuesta tuya, y dos han muerto porque cerraste la tab sin querer. Agent View elimina el malabar: una pantalla, una fila por sesión, y un proceso supervisor que mantiene las sesiones vivas con o sin terminal.

## Cómo funciona

Cada sesión en background es un proceso completo de Claude Code hospedado por un **supervisor por usuario** — un demonio que arranca solo la primera vez que mandas algo al fondo. El supervisor sobrevive a auto-updates, mantiene las sesiones aunque cierres todas tus terminales, y se apaga solo cuando no queda nada activo. El estado vive en `~/.claude/jobs/<id>/state.json`; los logs en `~/.claude/daemon.log`.

Las filas se agrupan automáticamente: **Needs input** y **Ready for review** arriba, **Working** en medio, **Completed** abajo. Cada fila lleva un icono cuyo color codifica estado (animado = trabajando, amarillo = espera tuya, verde = OK, rojo = falló) y cuya forma indica si el proceso está vivo (`✻` activo, `∙` durmiendo).

## Vista previa

```text
Pinned
  ✽ clawd walk cycle          Write assets/sprites/clawd-walk.png         3m

Ready for review
  ∙ jump physics              github.com/example/game/pull/2048        ●  2h

Needs input
  ✻ power-up design           needs input: double jump or wall climb?     1m

Working
  ✽ collision detection       Edit src/physics/CollisionSystem.ts         2m
  ✢ playtest level 3          run 12 · all checkpoints cleared          in 4m

Completed
  ✻ title screen              result: menu, options, and credits done     9m
```

## Cómo usarlo

**1. Abrir Agent View**

```bash
claude agents
```

Sale en pantalla completa, con un input al fondo y la lista arriba. `Esc` te devuelve al shell sin matar nada.

**2. Despachar una sesión nueva (3 vías)**

```bash
# Desde Agent View: escribe en el input y Enter
> investigar el test flaky de SettingsChangeDetector

# Desde dentro de una sesión interactiva
/bg

# Directamente desde el shell, sin pasar por Agent View
claude --bg "address review comments on PR 1234"
```

`@<subagente>` al principio del prompt lanza esa sesión con un [subagente custom](/es/tips/claude-code-crear-agentes-personalizados-es) como agente principal. `@<repo>` te permite dirigir la sesión a otro directorio.

**3. Peek y respuesta inline**

Selecciona una fila con flechas, `Space` abre el panel de peek: ves el último output o la pregunta concreta que bloquea la sesión. Escribes la respuesta y `Enter` — sin necesidad de attach. Si es una pregunta multi-opción, las teclas numéricas las eligen.

**4. Attach y detach**

`Enter` o `→` te mete en la conversación completa, como si hubieras lanzado `claude` en ese directorio. `←` con el prompt vacío te saca y vuelves al panel. Detach NUNCA mata la sesión — `/stop` desde dentro es lo único que termina una.

**5. Gestión desde el shell (sin abrir Agent View)**

```bash
claude attach <id>     # entrar en la sesión
claude logs <id>       # ver output reciente
claude stop <id>       # parar (alias: claude kill)
claude respawn <id>    # reanudar una parada, contexto intacto
claude rm <id>         # borrar de la lista + limpiar worktree
```

Cada sesión vive en su propio [git worktree](/es/tips/claude-code-worktrees-tareas-paralelas) bajo `.claude/worktrees/` — incluyendo las que mandas al fondo con `/bg` desde una sesión interactiva. Me pasó: dos terminales abiertas en el mismo repo (poco común, pero ocurre), `/bg` en una, y antes de tocar un solo archivo Claude la movió a su propio worktree. Dos sesiones no se pisan ni queriendo — pagas el precio de tener que mergear o pushear si quieres conservar los cambios antes de borrar la sesión.

## Dónde encaja con el resto del paralelismo

| Si quieres ver… | Mira… |
|---|---|
| Tareas en background de **esta** sesión | [panel `/tasks`](/es/tips/claude-code-tasks-paralelo) |
| Todas tus **sesiones** en paralelo | **Agent View** (`claude agents`) |
| Subagentes que se hablan entre sí | [Agent Teams](/es/tips/claude-code-agent-teams-equipos) |
| Reloj y eventos que despiertan agentes | [mapa de primitivas autonomous](/es/tips/claude-code-loop-routines-monitor-mapa) |

Agent View no sustituye a `/tasks` — son cosas distintas: `/tasks` te muestra las tareas DENTRO de una sesión; Agent View te muestra las sesiones ENTRE sí.

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `claude agents` · `claude --bg "<tarea>"` · `/bg` dentro de una sesión |
| Atajos clave | `Space` peek · `Enter`/`→` attach · `←` detach · `Ctrl+X` stop (2x = delete) · `Ctrl+T` pin · `?` ayuda |
| Estados | working · needs input · idle · completed · failed · stopped |
| Persistencia | Supervisor por usuario, sobrevive auto-updates y cierre de terminales. Sleep/shutdown de la máquina sí mata sesiones (`claude respawn --all` las reanima) |
| Aislamiento | Cada sesión en su propio git worktree bajo `.claude/worktrees/` |
| Requisitos | Claude Code v2.1.139+. Research preview |
| Planes | Pro, Max, Team, Enterprise, Claude API |
| Apagar | `disableAgentView: true` en settings · `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` |
| Cuota | Cada sesión consume rate limit independiente — 10 agentes en paralelo gastan 10× |

> Documentación oficial: [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
