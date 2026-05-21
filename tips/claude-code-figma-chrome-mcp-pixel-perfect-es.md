---
date: 2026-05-20
type: tip
title_es: "Figma + Chrome MCP en Claude Code: el agente que busca el pixel perfect"
title_en: "Figma + Chrome MCP in Claude Code: the agent chasing pixel perfect"
---
> **TL;DR** Dos MCPs locales — `figma-desktop` (en `http://127.0.0.1:3845/mcp`) y `chrome-devtools-mcp` — más [`/goal`](/es/tips/claude-code-goal-condicion-parada) como condición de parada montan un loop cerrado: Claude lee specs y captura screenshots de Figma, implementa el código, abre Chrome real, verifica visual y funcional, y ajusta hasta llegar al pixel perfect. Mete el `/goal` dentro de [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes) y tienes una pipeline E2E que corre sola. Lo uso cada vez más — el overhead de memoria por tener ambos MCPs locales merece la pena con creces.

Llevamos meses oyendo que el feedback loop entre diseño e implementación es el cuello de botella del frontend con AI. Claude Code lo cierra cuando le das dos cosas locales: ojos en Figma (para leer la spec real, no tu descripción de ella) y ojos en Chrome (para verificar lo que escribió, no asumirlo). Ambos servidores corren en tu máquina, lo que importa por dos razones — latencia de localhost vs HTTPS con OAuth, y los **writes en Figma están exentos del rate limit** (los reads heredan el tier-1 de tu plan Figma).

Los MCPs que mueven la aguja no son siempre los remotos con catálogo de 200 tools. A veces los dos que cierran el bucle son los que viven en tu propio puerto local.

Resultado:

```
> claude mcp list

  ● figma-desktop    (http,  connected) → 127.0.0.1:3845
  ● chrome-devtools  (stdio, connected) → npx chrome-devtools-mcp

> /goal Implementa el componente Pricing card del frame
  "/Marketing/Pricing v2" exactamente como en Figma — pixel
  perfect, animación de hover incluida — y verifica en
  http://localhost:3000/pricing

[Loop autónomo]
  ✓ figma_get_frame "/Marketing/Pricing v2"
  ✓ figma_export_screenshot → guardado
  ✓ Edit src/components/PricingCard.tsx
  ✓ chrome_navigate http://localhost:3000/pricing
  ✓ chrome_screenshot → comparar
  ⚠ Diff visual: spacing-3 ≠ Figma (8px vs 12px)
  ✓ Edit src/components/PricingCard.tsx
  ✓ chrome_screenshot → match
  ✓ chrome_click [data-test="pricing-card"] → hover state OK
  ✓ Goal alcanzado
```

## Instalación (dos comandos)

```bash
# 1. Figma Desktop MCP — abre Figma Desktop primero,
#    activa "MCP Server" en Dev Mode (sidebar derecho)
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp

# 2. Chrome DevTools MCP — del equipo oficial de Chrome
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest

# Verifica
claude mcp list
```

Requisitos: Figma Desktop abierto con el archivo del proyecto, Chrome instalado, plan Figma con Dev o Full seat (Starter está capado a 6 calls/mes — efectivamente bloqueante para este flujo).

## Por qué el loop funciona tan bien

El patrón es un **Evaluator-Optimizer** ([cinco patrones de Agentic AI](/es/tips/claude-code-agentic-ai-cinco-patrones)) montado con dos sensores reales. Figma da la verdad de diseño. Chrome da la verdad del render. Claude itera entre ambos hasta que cuadran.

El truco para que no se cuelgue iterando sutilezas: dale [`/goal`](/es/tips/claude-code-goal-condicion-parada) con la condición exacta — "pixel perfect contra el frame X, hover state funcional, sin errores en consola". Sin goal claro, el agente sigue afinando para siempre. Con goal, sabe cuándo parar.

Para rutinas recurrentes — revisión nocturna de un set de componentes, regression visual antes de release — envuelve el `/goal` en [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes):

```bash
/loop 1h /goal Verifica que los componentes en
  /design-system/* siguen pixel-perfect contra el último
  Figma export y avísame si alguno divergió.
```

## El overhead de memoria

Dos MCPs locales suman ~150-300 MB extra de RAM (Figma Desktop ya está abierto si lo usas; `chrome-devtools-mcp` arranca un Chrome headless solo cuando se invoca). En mi máquina merece la pena con creces — el tiempo que ahorras en el ping-pong manual de "captura, pega, ¿se ve igual?" lo paga el primer día.

## Cuándo NO usarlo

- **Cuando no usas Figma.** Obvio, pero hay que decirlo — el MCP de Figma solo se gana el slot si abres el archivo a menudo. Para más opciones, ver [los cinco MCPs que sí se ganan el slot](/es/tips/claude-code-mejores-servidores-mcp).
- **Cuando estás en un repo backend puro.** Quita Chrome DevTools MCP del scope `user` y déjalo en `project` solo donde aporta.
- **Cuando el sitio detrás requiere tu sesión autenticada.** Chrome MCP arranca un Chrome limpio sin tus cookies. Para eso usa [`--chrome`](/es/tips/claude-code-chrome-depurar-frontend) (la extensión Claude in Chrome), que reusa tu sesión activa — son mecanismos distintos, no compiten.

## Referencia

| MCP | Local en | Rate limit | Best for |
|---|---|---|---|
| Figma Desktop | `127.0.0.1:3845/mcp` | Writes exentos · reads tier-1 Figma | Leer specs, exportar frames, tokens, components |
| Chrome DevTools | stdio (npx) | Ninguno (es tu Chrome) | Render real, eval JS, console, screenshots, click flows E2E |

| Comando | Qué hace |
|---|---|
| `claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp` | Conecta el MCP local de Figma Desktop |
| `claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest` | Instala el MCP oficial de Chrome DevTools |
| `claude mcp list` | Verifica que ambos están `connected` |
| `claude mcp remove <name>` | Lo quitas si no lo necesitas en este proyecto |

> Documentación oficial: [Figma MCP server guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) · [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) · [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
