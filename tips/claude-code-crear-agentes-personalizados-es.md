---
date: 2026-03-10
type: tip
title_es: "Crea agentes personalizados en Claude Code con --agent"
title_en: "Create Custom Agents in Claude Code with --agent"
---
# Quick Tip: Crea agentes personalizados en Claude Code con --agent

Claude Code permite crear agentes especializados como archivos Markdown con frontmatter YAML. Cada agente tiene su propio system prompt, herramientas restringidas y modelo. Cuando lanzas una sesión con `claude --agent <nombre>`, toda la conversación se transforma — no es un [subagent delegado](/es/articulos/claude-code-subagents-guia-espanol), es tu sesión principal operando con una personalidad y reglas diferentes.

Es como tener múltiples versiones de Claude Code, cada una diseñada para un rol concreto: reviewer, debugger, deployer, o lo que necesites.

> **TL;DR** Crea un archivo `.md` en `~/.claude/agents/`, define el rol en el frontmatter YAML, y lánzalo con `claude --agent nombre`. Tu sesión entera se convierte en ese agente especializado.

Resultado — un agente de revisión de código listo para usar:

```markdown
# ~/.claude/agents/reviewer.md
---
name: reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Glob, Grep, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Provide feedback organized by priority:
   - Critical (must fix)
   - Warnings (should fix)
   - Suggestions (consider improving)

Include specific examples of how to fix each issue.
```

## Configuración

### **1. Crear el archivo del agente**

Crea un archivo `.md` en una de estas ubicaciones:

```bash
# Global — disponible en todos tus proyectos
~/.claude/agents/reviewer.md

# Proyecto — compartido con el equipo via git
.claude/agents/reviewer.md
```

### **2. Lanzar la sesión como agente**

```bash
claude --agent reviewer
```

Claude Code arranca con el system prompt, las herramientas y el modelo que definiste. No verás el prompt habitual — estás dentro del agente.

### **3. Usar el asistente interactivo**

Si prefieres no escribir el archivo a mano:

```bash
claude
# Dentro de la sesión:
/agents
```

Selecciona "Create new agent", elige el scope (user o project), y Claude te guía paso a paso — incluso puede generar el system prompt por ti.

### **4. Definir agentes efímeros desde la CLI (opcional)**

Para probar sin crear archivo, usa `--agents` (plural) con JSON inline:

```bash
claude --agents '{
  "reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer. Focus on quality and security.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Nota: `--agent` (singular) transforma tu sesión principal en un agente existente. `--agents` (plural) define subagents efímeros que Claude puede delegar durante la sesión.

## Referencia

| Campo | Requerido | Descripción |
|---|---|---|
| `name` | Sí | Identificador único (letras minúsculas y guiones) |
| `description` | Sí | Cuándo debe usarse este agente |
| `tools` | No | Herramientas permitidas. Si se omite, hereda todas |
| `disallowedTools` | No | Herramientas explícitamente denegadas |
| `model` | No | `sonnet`, `opus`, `haiku` o `inherit` (por defecto) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `plan`, `bypassPermissions` |
| `hooks` | No | [Hooks](/es/articulos/claude-code-hooks-guia-practica) del ciclo de vida del agente |
| `memory` | No | `user`, `project` o `local` — memoria persistente entre sesiones |
| `skills` | No | [Skills](/es/articulos/claude-code-skills-flujos-trabajo-personalizados) precargadas en el contexto del agente |
| `mcpServers` | No | Servidores MCP disponibles para el agente |

| Ubicación | Alcance | Prioridad |
|---|---|---|
| `--agents` (CLI flag) | Sesión actual | 1 (máxima) |
| `.claude/agents/` | Proyecto | 2 |
| `~/.claude/agents/` | Global (personal) | 3 |
| Directorio de plugins | Donde el plugin esté activo | 4 (mínima) |

> Documentación oficial: [Crear subagentes personalizados](https://code.claude.com/docs/es/sub-agents)
