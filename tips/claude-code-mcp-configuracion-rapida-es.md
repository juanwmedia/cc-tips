---
date: 2026-02-21
type: tip
title_es: "Qué es MCP en Claude Code y cómo conectarlo en 2 minutos"
title_en: "What Is MCP in Claude Code and How to Set It Up in 2 Minutes"
---
# Quick Tip: Qué es MCP en Claude Code y cómo conectarlo en 2 minutos

MCP (Model Context Protocol) no es un plugin. No es una skill. No es una API. Es un **protocolo** — un estándar abierto que define cómo un agente de IA se comunica con herramientas externas. Piensa en USB, pero para conectar Claude con tus servicios: Notion, GitHub, Sentry, bases de datos, lo que sea.

La diferencia clave: una skill es un prompt que le das a Claude. Una API es algo que tú consumes desde tu código. MCP es algo que Claude consume directamente — le da herramientas nuevas que puede usar sin que tú escribas código.

> **TL;DR** `claude mcp add` + URL o comando local. Con eso tienes Claude conectado a cualquier servicio.

Result:

```bash
> /mcp

  MCP Servers:
  ● notion (http, connected)
  ● db (stdio, connected)
```

## Los dos tipos de servidor

### 1. Remoto (HTTP) — servicios en la nube

Un servidor HTTP vive en internet. Alguien lo mantiene, tú solo lo conectas:

```bash
# Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# GitHub
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Algunos requieren autenticación OAuth. Después de añadirlo, ejecuta `/mcp` dentro de Claude Code y sigue el flujo en el navegador.

### 2. Local (stdio) — procesos en tu máquina

Un servidor stdio es un proceso que corre localmente. Ideal para bases de datos, herramientas de sistema o scripts propios:

```bash
# PostgreSQL
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"

# Servidor personalizado
claude mcp add --transport stdio my-tool -- node ./my-mcp-server.js
```

## Referencia rápida

| Comando | Qué hace |
|---|---|
| `claude mcp add` | Añade un servidor |
| `claude mcp list` | Lista servidores configurados |
| `claude mcp remove <name>` | Elimina un servidor |
| `/mcp` | Estado y autenticación (dentro de Claude Code) |

| Scope | Dónde se guarda | Para qué |
|---|---|---|
| `--scope local` | `~/.claude.json` (por defecto) | Solo tú, solo este proyecto |
| `--scope project` | `.mcp.json` en la raíz | Compartido con el equipo (va a git) |
| `--scope user` | `~/.claude.json` | Solo tú, todos tus proyectos |

> Documentación oficial: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
