---
date: 2026-05-09
type: tip
title_es: "Agent Teams en Claude Code: varios Claudes que se hablan entre sí"
title_en: "Agent Teams in Claude Code: multiple Claudes talking to each other"
---

> **TL;DR** Activa `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` en `settings.json` y pídele a Claude que cree un equipo. Él spawnea N teammates en sus propios contextos, comparten una **task list**, y se mensajean entre sí vía **mailbox**. **No es lo mismo que subagents**: los subagents reportan al main; los teammates colaboran y se desafían entre ellos. Sweet spot: 3-5 teammates con 5-6 tareas cada uno. Disponible desde Claude Code `v2.1.32`.

[Los subagents](/es/tips/claude-code-subagentes-pierden-contexto) hacen su trabajo y reportan al main. Punto. No se hablan entre ellos, no comparten tareas, no se cuestionan. Para tareas focalizadas con un único output, perfecto. Pero hay un escalón superior — y casi nadie lo está usando porque está experimental detrás de un flag desde principios de 2026.

Lo dice [la doc oficial](https://code.claude.com/docs/en/agent-teams) literal:

> *"Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."*

## Subagents vs Agent Teams

Mismo principio (paralelizar trabajo en contextos separados) pero arquitectura distinta:

| | [Subagents](/es/tips/claude-code-subagentes-pierden-contexto) | Agent Teams |
|---|---|---|
| **Comunicación** | Solo reportan al main agent | Teammates se mensajean entre sí (mailbox) |
| **Coordinación** | El main asigna todo | Task list compartida + self-claim |
| **Tu acceso** | Solo a través del main | Puedes hablar con cualquier teammate directamente |
| **Cuándo encaja** | Tareas focalizadas, solo importa el resultado | Trabajo que requiere discusión y colaboración |
| **Coste tokens** | Menor (resúmenes vuelven al main) | Mayor (cada teammate es una sesión Claude completa) |

**El detalle que cambia todo**: con Agent Teams, una teammate de frontend puede mandarle un mensaje DIRECTAMENTE a la de backend para coordinar un cambio en el contrato de la API, sin pasar por el lead. Eso con subagents no se puede.

## Cómo activarlo

En `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

O `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` en tu shell. Verifica versión: `claude --version` debe ser ≥ `v2.1.32`.

## El ejemplo que mejor lo explica (verbatim de docs oficial)

Este prompt está sacado tal cual de la doc de Anthropic — ilustra mejor que ningún otro qué cambia con teammates colaborativos:

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk
to each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

¿Qué pasa cuando lo lanzas?

1. El **lead** crea el equipo y razona sobre las dependencias antes de spawnear teammates.
2. Cada **teammate** arranca como una sesión Claude Code completa (su propio context window, lee `CLAUDE.md`, MCP servers, skills) con un prompt específico.
3. Los teammates **se mensajean entre sí por nombre** vía mailbox para refutar teorías. Los mensajes llegan automáticamente a quien los reciba.
4. Las teorías que sobreviven al debate se consolidan en la **task list compartida**.
5. Cuando un teammate termina, **notifica al lead automáticamente** (idle notification).
6. El lead **sintetiza** los hallazgos.

La estructura del debate es lo que importa. Una sola sesión sufre de **anchoring**: encuentra la primera explicación plausible y deja de buscar. Cinco teammates con hipótesis competing y mandato de refutarse → la teoría que sobrevive es mucho más probablemente la correcta.

Para ver lo que está pasando en cada teammate desde tu terminal, usa **Shift+Down** para ir ciclando entre ellos (modo in-process), o cada teammate abre su propio panel si tienes tmux/iTerm2 (modo split panes).

## Cómo controlarlo

### **1. Pides un equipo en lenguaje natural**

```
Crea un equipo de 4 teammates para refactorizar estos módulos en paralelo.
Usa Sonnet para cada teammate.
```

Claude decide cuántos teammates spawnea, o le dices el número. La tabla compartida y el mailbox se crean automáticamente.

### **2. Hablas con teammates directamente**

- **In-process** (por defecto, funciona en cualquier terminal): pulsa `Shift+Down` para ir ciclando entre teammates. Escribes y mandas mensaje directo. `Enter` para entrar en su sesión, `Esc` para interrumpir.
- **Split panes** (requiere tmux o iTerm2): cada teammate en su panel propio. Click y escribes. Auto-detecta si ya estás en tmux.

### **3. Plan approval para tareas arriesgadas**

```
Spawn an architect teammate to refactor the auth module.
Require plan approval before they make any changes.
```

El teammate trabaja en plan mode (read-only) hasta que el lead aprueba. Si rechaza con feedback, el teammate revisa y resubmite.

### **4. Cierras el equipo cuando acabas**

```
Clean up the team
```

El lead chequea que no hay teammates activos y limpia los resources. **Siempre desde el lead**, no desde un teammate.

## Los 4 use cases que recomienda Anthropic

| Caso | Por qué Agent Teams |
|---|---|
| **Research & review** | Cada teammate investiga un ángulo distinto, luego comparten y se cuestionan |
| **Módulos nuevos en paralelo** | Cada teammate posee una pieza independiente sin pisarse |
| **Debugging con hipótesis competing** | Como el ejemplo de arriba: 5 teorías, debate, gana la robusta |
| **Cross-layer (frontend + backend + tests)** | Cada capa en un teammate, coordinación vía mailbox |

## Caveats que tienes que saber

- **Experimental**: el flag `EXPERIMENTAL_` es literal. La API puede cambiar.
- **Tokens × N**: cada teammate es una sesión Claude completa. Más caro que un solo agente o subagents.
- **`/resume` no restaura teammates in-process**: tras un resume, el lead puede mandar mensajes a teammates que ya no existen. Solución: pedirle al lead que spawnee nuevos.
- **Split panes no funciona en VS Code terminal, Windows Terminal ni Ghostty**. En esos, queda in-process.
- **Un solo equipo a la vez**: cleanup antes de crear otro.
- **Sin equipos anidados**: los teammates no pueden crear sus propios teams.
- **Conflictos de archivo**: dos teammates editando el mismo archivo se sobrescriben. Asigna files distintos a cada uno.

## Referencia

| Aspecto | Detalle |
|---|---|
| Versión mínima | Claude Code `v2.1.32` |
| Activar | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (settings.json o env) |
| Sweet spot | 3-5 teammates con 5-6 tareas cada uno |
| Componentes | Team lead · Teammates · Task list · Mailbox |
| Display modes | `auto` (default), `in-process`, `tmux` (split panes) |
| Storage | `~/.claude/teams/<name>/config.json` · `~/.claude/tasks/<name>/` |
| Hooks `TeammateIdle` | exit code 2 → **mantiene al teammate trabajando** + feedback (no le deja irse a idle) |
| Hooks `TaskCreated` / `TaskCompleted` | exit code 2 → **bloquea** la creación o completion + feedback |
| Cuándo NO usar | Tareas secuenciales, mismo archivo, muchas dependencias → mejor [subagents](/es/tips/claude-code-subagentes-pierden-contexto) o sesión única |

> Documentación oficial: [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
