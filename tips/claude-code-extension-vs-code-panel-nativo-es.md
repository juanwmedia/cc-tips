---
date: 2026-06-15
type: tip
title_es: "Claude Code en VS Code: el panel que Anthropic recomienda y casi nadie usa"
title_en: "Claude Code in VS Code: the panel Anthropic recommends and almost nobody uses"
---

> **TL;DR** Instala la extensión (`Cmd+Shift+X` → "Claude Code") y abre el panel con el icono Spark. Ganas revisión de diffs inline, @-mención de rangos de líneas con `Option+K` y varias conversaciones en pestañas. Pierdes el atajo `!` para bash, el tab-completion y parte de los comandos: para eso, `claude` en la terminal integrada sigue ahí.

Casi todo el mundo "usa Claude Code en VS Code" abriendo la terminal integrada y escribiendo `claude`. Funciona, pero te saltas la interfaz que Anthropic marca como recomendada: un panel gráfico nativo dentro del editor. No es la CLI metida en una barra lateral. Es una GUI que sabe dónde tienes el cursor, abre los diffs en el visor nativo de VS Code y maneja varias conversaciones a la vez.

Un detalle que despista: la extensión trae su propia copia de la CLI para el panel. El `claude` de tu terminal (el del PATH) es una instalación aparte. Comparten historial de conversaciones y configuración (`~/.claude/settings.json`), pero son dos binarios distintos. Si no vives dentro de VS Code, el equivalente es la app independiente: [Claude Code Desktop](/es/tips/claude-code-desktop-5-ventajas-sobre-cli).

```
┌── VS Code ──────────────────┐ ┌─ ✱ Claude Code (panel) ──┐
│ auth.ts                     │ │ > arregla el login        │
│  ▸ diff login()      +6 -2  │ │   @auth.ts#10-18          │
│    + const token = sign(u)  │ │                           │
│    - return null            │ │ Plan ▸   ◐ auto-accept    │
│                             │ │ [ Accept ]   [ Reject ]   │
└─────────────────────────────┘ └───────────────────────────┘
```

## Lo que ganas sobre la terminal

**1. Revisas (y editas) el plan antes de que toque nada**

En Plan mode, la extensión abre el plan como un documento markdown completo donde dejas comentarios inline antes de que Claude empiece. No es un párrafo en el chat: es un doc editable. Para el resto del selector de modos del prompt (normal, plan, auto-accept), [los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab); por qué Plan mode merece la pena, [Plan Mode te obliga a entender](/es/tips/claude-code-plan-mode-obliga-entender).

**2. Diffs inline en el visor nativo de VS Code**

Cuando Claude edita, ves una comparación lado a lado y decides: aceptar, rechazar o decirle qué hacer. Si editas la propuesta dentro del diff antes de aceptar, Claude se entera y deja de asumir que el archivo quedó como él lo planteó.

**3. @-mención de rangos exactos de líneas**

Selecciona código y pulsa `Option+K` (macOS) / `Alt+K` (Windows/Linux): inserta una referencia tipo `@auth.ts#5-10`. Claude ya ve tu selección automáticamente y el footer del prompt te dice cuántas líneas. El icono del ojo tachado la oculta si esa selección no debería viajar al contexto.

**4. Varias conversaciones en pestañas, con su historial**

**Open in New Tab** (`Cmd+Shift+Esc`) o **New Window**: cada conversación con su propio contexto. Un punto azul en el icono Spark significa permiso pendiente; naranja, que Claude terminó mientras la pestaña estaba oculta. El botón **Session history** busca sesiones por palabra o fecha, y si usas Claude Code en la web, la pestaña **Remote** trae esas sesiones de claude.ai al editor.

## Lo que todavía te manda a la terminal

El panel es un subconjunto de la CLI. Esto sigue siendo solo de terminal:

- El atajo `!` para bash y el tab-completion no existen en el panel.
- El set completo de comandos y skills: el panel muestra un subconjunto (escribe `/` para ver cuáles).
- Añadir un MCP nuevo se hace con `claude mcp add`; el panel solo gestiona los que ya tienes, con `/mcp`.

Para cualquiera de esos, abre la terminal integrada (`` Cmd+` `` / `` Ctrl+` ``) y escribe `claude`. Comparten historial, así que `claude --resume` continúa una conversación que empezaste en el panel. Ojo: instalar la extensión **no** pone `claude` en tu PATH; para usarlo en la terminal necesitas la [instalación standalone de la CLI](https://code.claude.com/docs/en/setup).

## Referencia

| | Panel (extensión) | `claude` en terminal |
|---|---|---|
| Comandos y skills | Subconjunto | Todos |
| MCP | Gestionar (`/mcp`) | Añadir + gestionar |
| Diffs | Visor nativo de VS Code | En texto |
| `!` bash y tab-completion | No | Sí |
| Checkpoints / rewind | Sí | Sí |

**Instalar**: `Cmd+Shift+X` → busca "Claude Code" → Install. Funciona igual en Cursor y en forks como Kiro vía Open VSX. **Abrir**: el icono Spark (✱) en la esquina del editor con un archivo abierto, en la Activity Bar, o **✱ Claude Code** abajo a la derecha (este último vale aunque no tengas ningún archivo abierto).

> Documentación oficial: [Usar Claude Code en VS Code](https://code.claude.com/docs/en/vs-code)

**Relacionado:** [Claude Code Desktop: 5 ventajas sobre la CLI](/es/tips/claude-code-desktop-5-ventajas-sobre-cli) · [Los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab) · [Plan Mode te obliga a entender](/es/tips/claude-code-plan-mode-obliga-entender)

## Requisitos

- VS Code 1.98 o superior
- Suscripción de pago (Pro, Max, Team o Enterprise) o cuenta de Console; sin API key
