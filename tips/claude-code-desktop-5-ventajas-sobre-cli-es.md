---
date: 2026-02-26
type: tip
title_es: "Claude Code Desktop: 5 funcionalidades por las que valdría la pena dejar el terminal"
title_en: "Claude Code Desktop: 5 Features Worth Leaving the Terminal For"
---
# Quick Tip: Claude Code Desktop: 5 funcionalidades por las que valdría la pena dejar el terminal

El terminal siempre va a ganar para trabajo técnico: estás más cerca del código, más cerca de la capa que quieres afectar. Pero no todo el mundo quiere mancharse las manos con la terminal. Product Managers, Project Managers, personas técnicamente capaces pero que no viven en el código — para ellos, Desktop es el punto de entrada perfecto. Mismo motor que la CLI, con cinco capacidades exclusivas encima.

Resultado:

```
┌─────────────────────────────────────────────┐
│  Chat  │  Cowork  │  ● Code                 │
├─────────────────────────────────────────────┤
│ Sessions      │  Diff: app.tsx  +12 -1      │
│ ▸ feature-auth│  - const old = getValue()   │
│ ▸ fix-navbar  │  + const r = compute(input) │
│ + New session │  [Accept] [Reject] [Review] │
└─────────────────────────────────────────────┘
```

## Las 5 funcionalidades exclusivas

**1. Diff visual con comentarios inline**

Claude modifica archivos y aparece un indicador `+12 -1`. Clic para abrir la vista diff. Clic en cualquier línea para dejar un comentario. Claude lee tus comentarios y ajusta el código. `Cmd+Enter` (macOS) o `Ctrl+Enter` (Windows) envía todos los comentarios a la vez.

**2. Sesiones paralelas con worktrees automáticos**

**+ New session** crea un worktree aislado sin flags ni terminales extra. Cada sesión tiene su propia rama, visible en la barra lateral. En la CLI necesitas `claude -w <nombre>` por cada terminal — Desktop lo abstrae por completo.

**3. Preview embebido de tu app**

Un navegador integrado muestra tu app corriendo. Claude arranca el servidor, toma capturas, inspecciona el DOM, rellena formularios y corrige lo que encuentra. Se configura en `.claude/launch.json`:

```json
{
  "configurations": [{
    "name": "web",
    "runtimeExecutable": "npm",
    "runtimeArgs": ["run", "dev"],
    "port": 3000
  }]
}
```

**4. Monitorización de PRs con auto-fix y auto-merge**

Al abrir un PR, una barra de CI aparece en la sesión. **Auto-fix**: Claude lee los fallos y los corrige. **Auto-merge**: Claude hace merge cuando todos los checks pasan. Requiere `gh` CLI instalado.

**5. Conectores integrados**

Botón **+** → **Connectors** para conectar GitHub, Slack, Linear, Notion y más — sin tocar JSON. Son servidores MCP con interfaz gráfica. En la CLI, configurar un MCP requiere editar `~/.claude.json` a mano.

## Referencia

| Funcionalidad | CLI | Desktop |
|---|---|---|
| Diff review | No disponible | Visual con comentarios inline |
| Sesiones paralelas | `claude -w <nombre>` manual | Automático desde sidebar |
| Preview | `--chrome` (beta) | Navegador embebido |
| CI monitoring | No disponible | Barra de estado + auto-fix |
| Conectores | Editar JSON | UI gráfica |

| Concepto | Detalle |
|---|---|
| Motor | Mismo que la CLI — comparten CLAUDE.md, hooks, MCP |
| Plataformas | macOS y Windows (sin Linux) |
| Entornos | Local, Remoto (cloud Anthropic), SSH |
| Modelos | Opus, Sonnet, Haiku — se fija al iniciar sesión |

**Relacionado:** [Las 6 formas de extender Claude Code](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa) · [Worktrees para tareas en paralelo](/es/tips/claude-code-worktrees-tareas-paralelas)

> Documentación oficial: [Primeros pasos con Desktop](https://code.claude.com/docs/en/desktop-quickstart) · [Referencia completa](https://code.claude.com/docs/en/desktop)

## Requisitos

- Suscripción Pro, Max, Teams o Enterprise
- macOS o Windows (Linux no soportado)
- Git instalado (en Windows: [git-scm.com](https://git-scm.com/downloads/win))
