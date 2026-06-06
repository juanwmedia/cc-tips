---
date: 2026-06-06
type: tip
title_es: "Reanudar sesiones en Claude Code: todas las formas de volver a una conversación que no conocías"
title_en: "Resume sessions in Claude Code: every door back into a conversation (even across worktrees)"
---

> **TL;DR** Claude Code guarda cada conversación, así que ninguna se pierde. `claude --continue` retoma la más reciente de este directorio; `claude --resume` abre el picker; `claude --resume <nombre>` va directa a una sesión con nombre; y `claude --from-pr <número>` reabre la sesión local que hay detrás de un PR. Dentro del picker, `Ctrl+W` y `Ctrl+A` buscan sesiones en otros worktrees y proyectos, no solo en el directorio donde lanzaste el comando.

Para mí, resume ha pasado de casi inusable a una de las cosas que más uso. Hoy tiro casi siempre de la [vista de agentes](/es/tips/claude-code-agent-view-sesiones-paralelas) para lo paralelo, pero resume ganó un truco que lo cambió todo: ahora busca tus sesiones en **todos** los directorios, no solo en el que invocas el comando, y te lleva a esa conversación sin que tengas que encontrar la carpeta tú.

## Cómo funciona

Cada sesión se guarda en local mientras trabajas. El picker (`/resume`, o `claude --resume`) lee esas sesiones y, por defecto, te muestra las del worktree actual. Con un par de teclas amplías la búsqueda al resto del repo o a toda la máquina, y eliges sin tener que recordar dónde vivía cada conversación.

## Cómo se ve

```text
> /resume        reanuda una conversación · Ctrl+W worktrees · Ctrl+A todo

  auth-refactor       fix token refresh 401          hace 2h   · 84 msgs   main
▸ flaky-test (3)      investiga SettingsChange…       hace 1d   · 51 msgs   test
  pago-stripe         github.com/acme/app/pull/2048   hace 3d   · 120 msgs  feat/pay

  ↑↓ navegar · Space preview · Ctrl+R renombrar · Enter reanudar
```

## Las cinco puertas de vuelta

**1. La última, sin pensar**

```bash
claude --continue
```

Retoma la sesión más reciente **de este directorio**. Por eso importa el picker: cuando la que buscas está en otra carpeta, `--continue` no la ve.

**2. Elige del picker**

```bash
claude --resume      # o /resume desde dentro de una sesión
```

Cada fila lleva nombre o resumen, tiempo desde la última actividad, número de mensajes y branch. Las sesiones bifurcadas se agrupan bajo su raíz: pulsa `→` para expandirlas.

**3. Directa, por nombre**

```bash
claude --resume auth-refactor
```

Resuelve entre worktrees: si hay coincidencia exacta, entra aunque la sesión viva en otro worktree. [Nombra y colorea tus sesiones](/es/tips/claude-code-rename-color-sesiones) primero, o el picker es una sopa de IDs.

**4. Desde un PR**

```bash
claude --from-pr 2048
```

Reabre la sesión local que generó ese PR. Y dentro del picker puedes **pegar la URL** de un PR o MR (GitHub, GitLab, Bitbucket) y te encuentra la sesión que lo creó.

**5. Los atajos del picker que casi nadie usa**

- `Ctrl+W`: amplía a todos los worktrees del repo.
- `Ctrl+A`: amplía a todos los proyectos de la máquina.
- `Ctrl+B`: filtra a la branch actual (aquí `Ctrl+B` es del picker, no el background mode).
- `Space`: preview de la conversación sin entrar.
- `Ctrl+R`: renombra la sesión al vuelo.

Cuando eliges una sesión de **otro worktree del mismo repo**, la reanuda ahí mismo. Si es de un **proyecto sin relación**, te copia al portapapeles el `cd <dir> && claude --resume <id>` listo para pegar. En ningún caso tienes que acordarte de la ruta.

## Referencia

| Entrada | Qué hace |
|---|---|
| `claude --continue` | La sesión más reciente de este directorio |
| `claude --resume` | Abre el picker |
| `claude --resume <nombre>` | Va directa a la sesión con ese nombre (resuelve entre worktrees) |
| `claude --from-pr <número>` | Reabre la sesión local detrás de ese PR |
| `claude --resume <session-id>` | Reanuda una sesión de `claude -p` o el SDK (no salen en el picker) |
| `/resume` | Cambia de conversación desde dentro de una sesión |

| Atajo del picker | Acción |
|---|---|
| `Ctrl+W` | Todos los worktrees del repo |
| `Ctrl+A` | Todos los proyectos de la máquina |
| `Ctrl+B` | Filtra a la branch actual |
| `Space` | Preview sin entrar |
| `Ctrl+R` | Renombrar |

Para **bifurcar** en vez de retomar (probar otra vía sin tocar la original), está [ramifica tus conversaciones](/es/tips/claude-code-fork-session-bifurcar-sesiones). Y si lo que quieres es que la sesión te resuma sola por dónde ibas al volver, eso es [session recap](/es/tips/claude-code-session-recap-resumen-sesion).

> Documentación oficial: [Manage sessions](https://code.claude.com/docs/en/sessions)
