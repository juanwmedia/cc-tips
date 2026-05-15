---
date: 2026-05-15
type: tip
title_es: "Servidores MCP en Claude Code: cinco bastan, cincuenta estorban"
title_en: "MCP Servers in Claude Code: five is enough, fifty just slows the agent down"
---

> **TL;DR** Más MCPs no es mejor Claude Code. Cada servidor inyecta su set de herramientas en el contexto y obliga al agente a elegir entre más opciones cada turno. Cinco bien escogidos baten cualquier ranking de cincuenta. Mi curación: **GitHub** (issues y PRs), **Context7** (docs versionadas, sin alucinaciones), **Figma Desktop** + **Chrome DevTools** (el bucle de feedback frontend autónomo), **DBHub** (Postgres, MySQL, SQLite). Lo demás se instala cuando duele su ausencia, no antes.

Cada blog y cada hilo de Reddit ofrece su "top 50 servidores MCP para Claude Code". La verdad incómoda es que más conectores penalizan: el contexto se llena de definiciones de herramientas que el agente nunca usará, la lista de decisiones por turno se duplica, y los servidores remotos añaden latencia que se nota cuando encadenas tres llamadas. Anthropic mete su propio mecanismo (Tool Search) para mitigarlo, pero el principio no cambia: la curación gana al catálogo.

## Resultado

```bash
> claude mcp list

  ● github          (http,  connected)
  ● context7        (http,  connected)
  ● figma-desktop   (http,  connected)
  ● chrome-devtools (stdio, connected)
  ● db              (stdio, connected)
```

Cinco. Bastan para el 95% del trabajo real.

## La curación

**1. GitHub MCP — entras en el flujo de tu repo**

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Issues, PRs, commits, code search, revisiones. Convierte a Claude Code de "generador de código" en "participante en tu workflow". Sin él, ves archivos pero no entiendes el contexto del PR donde estás. Con él, le pides "implementa el issue ENG-4521 y abre el PR" y lo hace de punta a punta.

**2. Context7 — documentación real, no alucinada**

```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
```

El servidor con mejor ROI por línea de configuración. Cuando el agente trabaja con una librería, Context7 le sirve la documentación versionada de esa librería — no el snapshot de hace ocho meses que vive en sus pesos. Adiós a "esa función no existe en esa versión". Mi `CLAUDE.md` tiene una regla durable: si dudas de una API, consulta Context7 antes de inventar.

**3. Figma Desktop MCP — diseño a código sin rate limit**

```bash
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```

El servidor vive dentro de tu Figma de escritorio, no en la nube — por eso **no tiene rate limit**. Abres un archivo de Figma, activas Dev Mode, enciendes "MCP Server" en el sidebar, y Claude lee tokens, spacing, componentes y variables directamente. La ventaja frente al MCP remoto de Figma: no compite con tu cuota, lo que importa cuando el agente itera veinte veces sobre un componente.

**4. Chrome DevTools MCP — el ojo que cierra el bucle**

```bash
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest
```

El compañero natural de Figma Desktop. Claude implementa los specs que extrajo de Figma, abre Chrome, inspecciona el render real, ajusta. Bucle autónomo: leer diseño → implementar → verificar → corregir. Sin ti en medio para "espera que abro el navegador". Cualquier modelo frontera (Opus 4.7, Sonnet 4.6) lo usa intensivamente en cuanto lo tiene a mano — es la herramienta que más me ha movido la aguja en trabajo de frontend.

**5. DBHub — Postgres, MySQL, SQLite con un solo conector**

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

Cuando Claude puede consultar tu base en lugar de pedirte exports, "¿cuántos usuarios tienen X?" pasa de cinco minutos a cinco segundos. DBHub habla con Postgres, MySQL, SQLite y más; si solo usas Postgres, el servidor oficial también vale.

## La regla que pesa más que la lista

Cinco es la mediana razonable. Tu cinco no es mi cinco — depende de tu stack. Si trabajas con Cloudflare Workers, el MCP de Cloudflare entra. Si tu equipo vive en Notion o Linear, ese MCP gana un slot por encima de DBHub. Si haces tests E2E pesados, Playwright MCP entra antes que Chrome DevTools. La heurística sana:

- **Añade un MCP solo cuando notes su ausencia.** Pedirle al agente que copies y pegues lo mismo tres veces = momento de instalar el conector.
- **Quita los que no usas.** `claude mcp remove <name>` libera contexto.
- **Scope correcto.** Servidores de tu workflow personal → `--scope user`. Servidores del equipo con credenciales del proyecto → `--scope project` (van a `.mcp.json`, compartidos en git).

Para todo lo demás, mira el [setup básico de MCP](/es/tips/claude-code-mcp-configuracion-rapida) y la [diferencia entre skills, hooks, MCP y plugins](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa).

## Referencia rápida

| Servidor | Para qué | Transporte | Comando |
|---|---|---|---|
| GitHub | Issues, PRs, code search | HTTP | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| Context7 | Docs versionadas | HTTP | `claude mcp add --transport http context7 https://mcp.context7.com/mcp` |
| Figma Desktop | Specs sin rate limit (local) | HTTP | `claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp` |
| Chrome DevTools | Render + inspección | stdio | `claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest` |
| DBHub | Multi-DB queries | stdio | `claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn …` |

> Documentación oficial: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
