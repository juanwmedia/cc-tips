---
date: 2026-05-16
type: tip
title_es: "Claude Agent SDK: Claude Code, pero llamado desde tu código"
title_en: "Claude Agent SDK: Claude Code, but called from your code"
---

> **TL;DR** `pip install claude-agent-sdk` (o `npm install @anthropic-ai/claude-agent-sdk`), importas `query`, pasas un prompt y la lista de tools permitidas, y obtienes el mismo agente que corre en tu terminal — programable. CI/CD, cron, API, lo que quieras. Por dentro: el agent loop, las built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch...), las skills de `~/.claude/`, los hooks, los subagents, MCP, sessions con resume/fork. **No es el Client SDK** (donde implementas tú el tool loop). Es el agente completo corriendo en tu proceso. La nota importante: a partir del **15 de junio de 2026**, el uso del SDK en planes de suscripción consume un **crédito mensual de Agent SDK** separado de tus límites interactivos.

Si llevas tiempo con Claude Code en la terminal, lo que sigue te ahorra el rato de confusión: **Claude Agent SDK** y **Claude Code SDK** son el mismo SDK. Anthropic lo renombró durante 2026 — la PAA de Google sigue llena de gente preguntando *"What is the difference between Claude Code and Claude Agent SDK?"*. La diferencia real es la interfaz: en tu terminal lo llamas `claude`, en tu código lo llamas con la librería.

Bajo el capó es el **mismo agent loop** que corre cuando escribes `claude` en tu terminal: lee archivos, ejecuta comandos, edita código, gestiona contexto. La librería expone los primitivos que ya conoces (skills, hooks, subagents, MCP, permisos) como argumentos de la función `query`.

## Hello world

Python, leer + editar + bash permitidos:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Encuentra y arregla el bug en auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)  # Claude lee el archivo, encuentra el bug, lo edita

asyncio.run(main())
```

TypeScript equivalente:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Encuentra y arregla el bug en auth.ts",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

Eso es todo. No implementas el tool loop. No serializas tool_use ni tool_result. Claude lo gestiona dentro de la librería.

## Setup

**1. Instala el SDK.**

```bash
pip install claude-agent-sdk                      # Python
npm install @anthropic-ai/claude-agent-sdk        # TypeScript
```

> El SDK de TypeScript trae el binario nativo de Claude Code empaquetado, así que no necesitas instalar Claude Code aparte.

**2. Configura tu API key.**

```bash
export ANTHROPIC_API_KEY=tu-api-key
```

Otras vías de auth soportadas: Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google Vertex AI (`CLAUDE_CODE_USE_VERTEX=1`), Azure AI Foundry (`CLAUDE_CODE_USE_FOUNDRY=1`), Claude Platform on AWS (`CLAUDE_CODE_USE_ANTHROPIC_AWS=1`).

## Claude Code (CLI) vs Agent SDK: cuándo cada uno

Mismas capacidades, distinta superficie. La tabla oficial:

| Caso de uso | Mejor opción |
|---|---|
| Desarrollo interactivo en local | CLI |
| Pipelines CI/CD | SDK |
| Aplicaciones custom | SDK |
| Tareas one-off | CLI |
| Automatización en producción | SDK |

> *"Many teams use both: CLI for daily development, SDK for production."* — docs.

## Lo que enchufas como en local

| Primitivo | Cómo se pasa al `query` | Para |
|---|---|---|
| **Built-in tools** | `allowed_tools=["Read", "Edit", "Bash", ...]` | Restringir qué puede tocar el agente |
| **[Hooks](/es/tips/claude-code-hooks-automatizar-flujo-trabajo)** | `hooks={"PostToolUse": [...]}` | Validar, loggear, bloquear o transformar acciones del agente |
| **[Subagents](/es/tips/claude-code-crear-agentes-personalizados)** | `agents={"code-reviewer": AgentDefinition(...)}` | Spawn de agentes especializados con tools acotadas |
| **[MCP servers](/es/tips/claude-code-mcp-configuracion-rapida)** | `mcp_servers={"playwright": {...}}` | Conectar bases de datos, navegadores, APIs externas |
| **[Permisos](/es/tips/claude-code-permisos-3-conceptos-clave)** | `allowed_tools` + `permission_mode` | Allow / ask / deny granular |
| **[Sessions](/es/tips/claude-code-session-recap-resumen-sesion)** | `resume=session_id` | Reanudar conversaciones (incluso forkearlas) |
| **[Skills](/es/tips/claude-code-skills-comandos-personalizados)** | Auto-loaded desde `.claude/skills/*/SKILL.md` | Reutilizar tus comandos custom |
| **CLAUDE.md** | Auto-loaded desde el cwd | Las mismas instrucciones que en local |

Las skills, slash commands y `CLAUDE.md` se cargan por defecto desde `.claude/` y `~/.claude/`. Si quieres restringir orígenes, pasa `setting_sources` en las opciones.

## El SDK ≠ Client SDK

La trampa típica. El [Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks) te da acceso directo a la API: tú envías prompts y **tú implementas el tool loop**. El Agent SDK ya lo trae:

```python
# Client SDK — tú escribes el loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK — Claude gestiona las tools
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

Si te encuentras escribiendo un `while response.stop_reason == "tool_use"`, estás en el SDK equivocado.

## Coste a partir del 15 de junio de 2026

Anthropic introduce un **crédito mensual de Agent SDK** en los planes de suscripción, separado del uso interactivo de Claude Code. El uso del SDK (y de `claude -p`, modo headless) cuenta contra ese crédito, no contra tus límites interactivos. Detalle oficial en el [aviso de pricing](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan).

Antes del 15 de junio, todo el uso del SDK cuenta como API normal (tokens facturados a tu cuenta).

## Combina con

- [GitHub Actions](/es/tips/claude-code-github-actions-revisar-prs) — la action de `@claude` que revisa PRs corre encima del Agent SDK. Saber esto te permite extenderla.
- [Subagents](/es/tips/claude-code-crear-agentes-personalizados) — el patrón que ya usabas en local, vía `agents={}`.
- [Plugins](/es/tips/claude-code-marketplace-plugins-distribucion) — cargables programáticamente via la opción `plugins`.
- [Cheat sheet de slash commands](/es/tips/claude-code-slash-commands-cheatsheet) — todo lo que invocas con `/` también es invocable desde el SDK.

> Documentación oficial: [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Python SDK](https://code.claude.com/docs/en/agent-sdk/python) · [TypeScript SDK](https://code.claude.com/docs/en/agent-sdk/typescript)
