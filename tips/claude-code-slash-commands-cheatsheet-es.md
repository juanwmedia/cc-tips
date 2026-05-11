---
date: 2026-05-11
type: tip
title_es: "Slash commands en Claude Code: la cheat sheet que las docs no te dan"
title_en: "Slash commands in Claude Code: the cheat sheet the docs don't give you"
---

> **TL;DR** Claude Code tiene casi 80 slash commands. Las docs los listan **en orden alfabético**; aquí los tienes agrupados **por lo que quieres hacer**. Empezar una sesión, ahorrar contexto, dejar a Claude trabajando solo, revisar antes de mergear, debug cuando algo va raro. Si en tu sesión escribes `/`, Claude te muestra los compatibles con tu plan y plataforma — pero saber dónde mirar es lo que te ahorra los 5 minutos de scroll.

Si llegas aquí desde Google buscando "claude code slash commands" probablemente ya viste la docs oficial: 80 entradas alfabéticas, una al lado de otra. Útil si ya sabes qué buscas. Inútil cuando lo que sabes es "quiero que Claude vigile algo mientras yo sigo programando" pero no recuerdas si era `/loop`, `/schedule`, `/monitor` o `/batch`.

Aquí los tienes por intent. Cada entrada con el comando, qué hace en una línea, y enlace al tip propio si profundizamos en él.

## 1. Cuando arrancas un proyecto

| Comando | Para |
|---|---|
| `/init` | Generar un `CLAUDE.md` inicial. Activa el flujo interactivo con `CLAUDE_CODE_NEW_INIT=1` ([tip](/es/tips/claude-code-init-flujo-interactivo)) |
| `/login` · `/logout` | Sesión con tu cuenta Anthropic |
| `/web-setup` | Conectar tu GitHub para [Claude Code on the web](/es/tips/claude-code-sesiones-en-la-nube) |
| `/install-github-app` | Configurar Claude GitHub Actions para un repo |
| `/team-onboarding` | Generar una guía de ramp-up de tu setup para un compañero nuevo |
| `/setup-bedrock` · `/setup-vertex` | Wizards para AWS Bedrock y Google Vertex AI |
| `/terminal-setup` | Configurar Shift+Enter y atajos en VS Code, Cursor, Windsurf, Alacritty, Zed |

## 2. Mientras estás trabajando en una tarea

| Comando | Para |
|---|---|
| `/model [model]` | Cambiar de modelo sin perder el prompt ([tip](/es/tips/claude-code-elegir-modelo-adecuado)) |
| `/effort [level]` | Subir o bajar el razonamiento. `xhigh` es el sweet spot en Opus 4.7 ([tip](/es/tips/claude-code-effort-level-ajustar-razonamiento)) |
| `/fast` | Toggle del [fast mode](/es/tips/claude-code-fast-mode-respuestas-rapidas) |
| `/plan [descripción]` | Plan mode directo, opcionalmente con la tarea ya escrita |
| `/branch [nombre]` | Bifurcar la conversación aquí, preservar la original ([tip](/es/tips/claude-code-fork-session-bifurcar-sesiones)) |
| `/btw <pregunta>` | Side question sin contaminar el historial ([tip](/es/tips/claude-code-btw-pregunta-lateral)) |
| `/copy [N]` | Copiar la última respuesta de Claude al portapapeles |
| `/diff` | Visor interactivo de diffs uncommitted + per-turn |
| `/add-dir <path>` | Añadir un directorio extra a la sesión |
| `/sandbox` | Toggle del [sandbox mode](https://code.claude.com/docs/en/sandboxing) |

## 3. Cuando el contexto se llena

| Comando | Para |
|---|---|
| `/context` | Ver dónde se está yendo tu context window ([tip](/es/tips/claude-code-comando-context-uso-tokens)) |
| `/compact [instrucciones]` | Comprimir la conversación; opcionalmente con foco ("conserva el plan y el diff") |
| `/clear [nombre]` | Empezar conversación nueva, la anterior queda accesible vía `/resume` |
| `/recap` | Resumen de una línea de la sesión actual ([tip](/es/tips/claude-code-session-recap-resumen-sesion)) |
| `/memory` | Editar `CLAUDE.md` y revisar las entradas de auto-memory ([tip](/es/tips/claude-code-memoria-automatica-entre-sesiones)) |

## 4. Cuando quieres que Claude trabaje sin ti

| Comando | Para |
|---|---|
| `/loop [intervalo] [prompt]` | Recurring intra-sesión. Sin intervalo, Claude se autopaca ([tip](/es/tips/claude-code-loop-tareas-recurrentes)) |
| `/schedule [descripción]` | Crear una [Routine](/es/tips/claude-code-routines-cloud-agents) en cloud. Alias `/routines` |
| `/batch <instrucción>` | Decomponer un refactor en 5-30 PRs paralelos ([tip](/es/tips/claude-code-batch-refactor-paralelo)) |
| `/ultraplan <prompt>` | Drafting de plan en cloud para revisar en el navegador ([tip](/es/tips/claude-code-ultraplan-planificacion-nube)) |
| `/autofix-pr [prompt]` | Web session que vigila tu PR y empuja fixes cuando CI falla |
| `/tasks` | Panel de todo lo que tienes corriendo en paralelo. Alias `/bashes` ([tip](/es/tips/claude-code-tasks-paralelo)) |

Y para entender cómo encajan unos con otros: [el mapa completo de las primitivas autonomous](/es/tips/claude-code-loop-routines-monitor-mapa).

## 5. Antes de mergear

| Comando | Para |
|---|---|
| `/review [PR]` | Revisión local en la sesión |
| `/ultrareview [PR]` | Revisión en cloud con flota de agentes paralelos ([tip](/es/tips/claude-code-ultrareview)) |
| `/security-review` | Analiza diffs pendientes buscando vulnerabilidades |
| `/simplify [foco]` | 3 agentes en paralelo revisan archivos recientes y aplican fixes de calidad/eficiencia |

## 6. Cuando algo va raro

| Comando | Para |
|---|---|
| `/doctor` | Audita install, settings, MCP, skills, contexto. Pulsa `f` y Claude arregla los errores ([tip](/es/tips/claude-code-doctor-diagnostico)) |
| `/debug [descripción]` | Activa debug logging y analiza el log de la sesión |
| `/heapdump` | Snapshot de memoria a `~/Desktop` cuando el consumo se dispara |
| `/feedback [report]` | Reportar un bug a Anthropic con el contexto de la sesión adjunto. Alias `/bug` |

## 7. Entre sesiones

| Comando | Para |
|---|---|
| `/resume [session]` | Abrir picker de sesiones. Acepta pegar la URL de un PR para encontrar la que lo creó. Alias `/continue` |
| `/rename [nombre]` | Renombrar la sesión actual ([tip](/es/tips/claude-code-rename-color-sesiones)) |
| `/teleport` | Traer una sesión de [Claude Code on the web](/es/tips/claude-code-sesiones-en-la-nube) a tu terminal. Alias `/tp` |
| `/desktop` | Continuar en la Desktop app. Alias `/app` |
| `/remote-control` | Hacer la sesión accesible desde claude.ai para controlarla en remoto ([tip](/es/tips/claude-code-control-remoto-desde-movil)) |
| `/export [archivo]` | Exportar la conversación como texto plano |

## 8. Métricas y uso

| Comando | Para |
|---|---|
| `/usage` | Coste, plan limits, stats. Aliases `/cost`, `/stats` ([tip](/es/tips/claude-code-uso-tokens-usage-stats)) |
| `/insights` | Análisis de tus sesiones: tipos de requests, lenguajes, patrones, fricción ([tip](/es/tips/claude-code-comando-insights)) |
| `/release-notes` | Picker interactivo del changelog |
| `/extra-usage` | Activar usage extra cuando llegas al rate limit |

## 9. Personalizar Claude Code

| Comando | Para |
|---|---|
| `/config` | UI de settings: tema, modelo, output style, editor mode, etc. Alias `/settings` |
| `/theme` | Cambiar tema. Incluye [crear uno custom](/es/tips/claude-code-custom-themes-paleta) |
| `/color` | Cambiar color de la prompt bar |
| `/statusline` | Configurar la status line |
| `/keybindings` | Editar bindings personalizados |
| `/agents` | Gestionar [subagents](/es/tips/claude-code-crear-agentes-personalizados) |
| `/hooks` | Ver hooks configurados ([tip](/es/tips/claude-code-hooks-automatizar-flujo-trabajo)) |
| `/mcp` | Gestionar MCP servers ([tip](/es/tips/claude-code-mcp-configuracion-rapida)) |
| `/permissions` | Reglas allow/ask/deny ([tip](/es/tips/claude-code-permisos-3-conceptos-clave)). Alias `/allowed-tools` |
| `/skills` | Listar skills. Press `t` para ordenar por tokens, `Space` para ocultar |
| `/plugin` | Gestionar [plugins](/es/tips/claude-code-marketplace-plugins-distribucion) |
| `/reload-plugins` | Recargar plugins sin reiniciar |

## Slash commands ≠ Skills (la confusión típica)

Las **skills** son archivos markdown en `~/.claude/skills/<nombre>/SKILL.md` que Claude ejecuta o auto-activa. Aparecen en el menú `/` como cualquier otro slash command, pero las escribes tú o las instalas vía plugin. Los **slash commands** built-in (los de las tablas de arriba) son código nativo de Claude Code, no editables.

Algunos commands están marcados como bundled skills en docs (`/batch`, `/loop`, `/simplify`, `/debug`, `/fewer-permission-prompts`, `/claude-api`): vienen de serie, pero técnicamente son skills, lo que significa que puedes ver su markdown si te interesa hackearlas. Para el modelo mental completo: [los 6 mecanismos de extensión](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa).

## Comandos retirados (por si los buscas)

- `/pr-comments` — retirado en `v2.1.91`. Sustituido: pídele a Claude que lea los comentarios del PR directamente.
- `/vim` — retirado en `v2.1.92`. Sustituido: `/config` → Editor mode.

## El comando que ya conoces sin saberlo

`/` solo, sin texto. Te muestra el listado completo filtrado por lo que tengas instalado y tu plan. Si encima escribes letras después de `/`, filtra en tiempo real. Si no recuerdas el nombre exacto, esa es la forma más rápida — sin tener que volver a esta cheat sheet.

> Documentación oficial: [Commands reference](https://code.claude.com/docs/en/commands)
