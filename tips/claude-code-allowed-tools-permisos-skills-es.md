---
date: 2026-02-21
type: tip
title_es: "Automatiza los permisos de tus skills con allowed-tools"
title_en: "Automate Skill Permissions with allowed-tools"
---
# Quick Tip: Automatiza los permisos de tus skills con allowed-tools

Cuando una skill orquesta varias herramientas — conexiones SSH, búsquedas web, APIs externas, Git — Claude Code pide confirmación para cada una. En skills de creación de contenido, eso se traduce en docenas de aprobaciones por ejecución. El campo `allowed-tools` en el frontmatter concede aprobación automática solo a las herramientas que especifiques: libertad selectiva, no acceso total.

Lo más práctico es descubrirlo al revés: ejecuta la skill manualmente varias veces, aprueba cada herramienta a mano, toma nota del patrón. Después de 2-3 ejecuciones sabrás exactamente qué necesita. Ahí es cuando lo formalizas en el frontmatter.

Result:

```yaml
---
name: publish-content
description: Generate and publish content to production
allowed-tools: Read, Write, Bash(ssh *), Bash(git *), mcp__notion__notion-fetch
---
```

## Configuracion

**1. Ejecuta la skill sin allowed-tools**

Cada vez que Claude pida permiso, anota dos cosas: el nombre de la herramienta y el comando exacto. Tras varias ejecuciones tendrás la lista completa.

**2. Añade allowed-tools al frontmatter**

```yaml
---
name: publish-article
description: Generate and publish a blog article
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(ssh *), Bash(mv *), Bash(git *), mcp__notion__notion-create-pages, mcp__notion__notion-fetch
---
```

La sintaxis sigue tres patrones:

- **Herramientas nativas**: nombre directo — `Read`, `Write`, `WebSearch`
- **Comandos Bash**: `Bash(patron *)` — el `*` acepta cualquier argumento tras el patrón
- **Herramientas MCP**: nombre completo — `mcp__servidor__nombre-herramienta`

**3. Verifica**

Invoca la skill. Las herramientas listadas se ejecutan sin confirmación. Las que no estén en la lista siguen pidiendo aprobación — ese es el control que mantienes.

## Referencia

| Patrón | Permite |
|---|---|
| `Read` | Leer cualquier archivo |
| `Bash(ssh *)` | Cualquier comando SSH |
| `Bash(git *)` | Cualquier operación Git |
| `Bash(npm run *)` | Solo scripts npm |
| `WebSearch` | Búsquedas web |
| `mcp__notion__notion-fetch` | Solo fetch del servidor Notion |

> Official docs: [Extend Claude with skills](https://code.claude.com/docs/en/skills#restrict-tool-access)
