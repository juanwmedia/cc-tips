---
date: 2026-02-21
type: tip
title_es: "Qué es MCP en Claude Code y cómo conectarlo en 2 minutos"
title_en: "What Is MCP in Claude Code and How to Set It Up in 2 Minutes"
---
# Quick Tip: What Is MCP in Claude Code and How to Set It Up in 2 Minutes

MCP (Model Context Protocol) is not a plugin. Not a skill. Not an API. It's a **protocol** — an open standard that defines how an AI agent communicates with external tools. Think USB, but for connecting Claude to your services: Notion, GitHub, Sentry, databases, whatever you need.

The key distinction: a skill is a prompt you give Claude. An API is something you consume from your code. MCP is something Claude consumes directly — it gives Claude new tools it can use without you writing any code.

> **TL;DR** `claude mcp add` + URL or local command. That's all it takes to connect Claude to any service.

Result:

```bash
> /mcp

  MCP Servers:
  ● notion (http, connected)
  ● db (stdio, connected)
```

## The two types of servers

### 1. Remote (HTTP) — cloud services

An HTTP server lives on the internet. Someone else maintains it, you just connect:

```bash
# Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# GitHub
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Some require OAuth authentication. After adding, run `/mcp` inside Claude Code and follow the browser flow.

### 2. Local (stdio) — processes on your machine

A stdio server is a process running locally. Ideal for databases, system tools, or custom scripts:

```bash
# PostgreSQL
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"

# Custom server
claude mcp add --transport stdio my-tool -- node ./my-mcp-server.js
```

## Quick reference

| Command | What it does |
|---|---|
| `claude mcp add` | Add a server |
| `claude mcp list` | List configured servers |
| `claude mcp remove <name>` | Remove a server |
| `/mcp` | Status and authentication (inside Claude Code) |

| Scope | Where it's stored | Use case |
|---|---|---|
| `--scope local` | `~/.claude.json` (default) | Just you, just this project |
| `--scope project` | `.mcp.json` at project root | Shared with team (goes to git) |
| `--scope user` | `~/.claude.json` | Just you, all your projects |

> Official docs: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
