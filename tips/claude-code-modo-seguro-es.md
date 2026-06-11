---
date: 2026-06-11
type: tip
title_es: "El modo a prueba de fallos de Claude Code: para cuando /doctor no encuentra nada"
title_en: "Claude Code's safe mode: for when /doctor comes up empty"
---

> **TL;DR** Algo va raro, `/doctor` sale verde y sigues sin saber qué pasa. Arranca con `claude --safe-mode`: Claude Code carga **sin ninguna de tus customizaciones** (CLAUDE.md, skills, plugins, hooks, MCP...). Si el problema desaparece, el culpable era tu config, no Claude. Es el Modo a prueba de fallos de Windows, pero para Claude Code. Necesitas v2.1.169 o superior.

Cuando algo no funciona, lo primero es [`/doctor`](/es/tips/claude-code-doctor-diagnostico): te audita instalación, settings, MCP y contexto. Pero `/doctor` te dice si las cosas *parecen* sanas, no si **tú** las has roto. A veces sale todo verde y sigues atascado, sin saber lo único que importa: ¿es Claude Code, o es mi setup?

`--safe-mode` responde esa pregunta de la única forma fiable: quitando tu setup de la ecuación. Arranca con lo mínimo, sin tus extras, igual que el Modo a prueba de fallos de Windows o el modo seguro del móvil. Si el problema sigue ahí en limpio, no eras tú.

El bisect, en tres pasos:

```bash
# 1. Reproduce el problema en una sesión normal.
# 2. Arranca sin tus customizaciones:
claude --safe-mode
# 3. ¿Desapareció? El culpable está en tu config.
#    ¿Sigue igual? El problema está más arriba (instalación, red, el modelo).
```

## Qué apaga (y qué no)

Con `--safe-mode`, **no se carga ninguna customización**: CLAUDE.md, skills, plugins, hooks, MCP servers, comandos y agentes propios, output styles, workflows, temas, keybindings, status line, LSP servers y auto-memory.

Lo que **sí sigue funcionando**: autenticación, selección de modelo, las herramientas nativas y los permisos. Por eso puedes trabajar en modo seguro con normalidad. Aquí está la diferencia con [`--bare`](https://code.claude.com/docs/en/headless), que va mucho más pelado.

> Las políticas de managed settings siguen aplicándose (hooks, status line y file-suggestion configurados por política). Lo que no carga es lo tuyo.

## Encuentra al culpable

Si en modo seguro el problema desaparece, ya sabes que está en tu config. Ahora toca aislar **cuál**: vuelve a una sesión normal y reactiva tus customizaciones de una en una (o por bloques) hasta que el fallo reaparezca. La que lo despierte es la culpable. Demo de 2 minutos: rompe un hook a propósito, arranca normal (falla), arranca con `--safe-mode` (limpio), y ya tienes el sospechoso.

## Cuándo tirar de él

**1. Fable te reenruta a Opus y no sabes por qué.** [Fable 5](/es/tips/claude-code-fable-5-por-encima-de-opus) salta a Opus cuando su clasificador marca tu petición, a veces en el primer mensaje, por el contexto que arrastra tu CLAUDE.md o el repo. Arranca con `--safe-mode` para ver si el detonante eran tus customizaciones.

**2. Claude se cuelga o se come la RAM.** Antes de pelearte con el proceso, descarta tu config: si en modo seguro va fino, el problema es un plugin, un MCP o un hook. Si sigue pesado, [los arreglos de rendimiento están aquí](/es/tips/claude-code-lento-cuelgues-memoria).

**3. Algo se rompió tras un cambio.** Instalaste un plugin, tocaste un hook, añadiste un MCP, y de repente algo falla. `--safe-mode` te confirma en un arranque si fue eso.

## /doctor vs --safe-mode

No compiten, son dos preguntas distintas:

| | `/doctor` | `claude --safe-mode` |
|---|---|---|
| Qué hace | **Audita** tu setup y reporta verde/amarillo/rojo | **Arranca sin** tu setup |
| Pregunta que responde | ¿Está algo mal configurado? | ¿El problema es mi config o no? |
| Cuándo | Primer chequeo, busca lo roto evidente | Cuando /doctor no encuentra nada y sigues atascado |

## Referencia

| | |
|---|---|
| Comando | `claude --safe-mode` |
| Variable de entorno | `CLAUDE_CODE_SAFE_MODE` (la pone el flag) |
| Versión mínima | Claude Code v2.1.169 |
| Apaga | Todas tus customizaciones (CLAUDE.md, skills, plugins, hooks, MCP, comandos, agentes, output styles, workflows, temas, keybindings, status line, LSP, auto-memory) |
| Mantiene | Auth, modelo, tools nativas, permisos |
| Alcance | Solo esa sesión |

> Documentación oficial: [CLI reference](https://code.claude.com/docs/en/cli-reference) · [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) · [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)

## Requisitos

Claude Code v2.1.169 o superior (`claude update` si no lo tienes).
