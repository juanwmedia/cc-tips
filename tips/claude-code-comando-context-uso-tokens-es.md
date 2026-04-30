---
date: 2026-02-21
type: tip
title_es: "Monitoriza el Uso de Tokens con el Comando /context"
title_en: "Monitor Token Usage with the /context Command"
---
# Quick Tip: Monitoriza el Uso de Tokens con el Comando /context

Claude Code opera dentro de una ventana de contexto de 200k tokens. Todo lo que Claude necesita para funcionar — system prompt, herramientas, MCP servers, agentes, archivos de memoria, skills y tu conversación — compite por ese espacio. El comando `/context` desglosa exactamente cuántos tokens consume cada componente, dándote visibilidad total sobre un recurso que se agota en silencio.

Es algo que se pasa fácilmente por alto al principio. Empiezas a agregar MCP servers, agentes custom, rules... y cuando quieres darte cuenta, gran parte de la ventana de contexto ya está preconsumida antes de que escribas tu primer mensaje. `/context` te mantiene alerta.

Resultado:

```
/context

Context Usage
claude-opus-4-5-20251101 · 51k/200k tokens (26%)

Estimated usage by category
  System prompt:     2.6k tokens  (1.3%)
  System tools:     17.6k tokens  (8.8%)
  MCP tools:          907 tokens  (0.5%)
  Custom agents:      935 tokens  (0.5%)
  Memory files:       302 tokens  (0.2%)
  Skills:              61 tokens  (0.0%)
  Messages:         30.5k tokens (15.3%)
  Free space:        114k        (57.0%)
  Autocompact buffer: 33k tokens (16.5%)
```

## Setup

No requiere configuración. El comando está disponible en cualquier sesión.

**1. Ejecuta el comando**

Escribe `/context` en cualquier momento de tu sesión:

```bash
/context
```

**2. Analiza el desglose**

El output muestra el consumo de cada categoría. Presta especial atención a:

- **System tools** y **MCP tools**: las herramientas se cargan en cada request. Pocos MCP servers pueden consumir un porcentaje considerable.
- **Free space**: tu espacio real de trabajo. Es lo que queda para mensajes, lectura de archivos y resultados de comandos.
- **Autocompact buffer**: reserva que Claude usa para compactar automáticamente cuando el contexto se llena.

**3. Actúa sobre lo que ves**

Si MCP tools consume demasiado, ejecuta `/mcp` para ver el coste por servidor y desactiva los que no necesites en esta sesión. Si el espacio libre baja del 30%, considera usar `/compact` o iniciar una sesión nueva.

## Referencia

| Categoría | Qué incluye |
|---|---|
| System prompt | Instrucciones internas de Claude Code |
| System tools | Herramientas integradas (Read, Edit, Bash, Grep, Glob, etc.) |
| MCP tools | Definiciones de herramientas de MCP servers conectados |
| Custom agents | Agentes personalizados definidos en `.claude/agents/` |
| Memory files | CLAUDE.md y archivos de memoria automática |
| Skills | Descripciones de skills registrados |
| Messages | Tu conversación: prompts, respuestas y resultados de herramientas |
| Free space | Tokens disponibles para seguir trabajando |
| Autocompact buffer | Reserva para compactación automática (~16.5%) |

> Documentación oficial: [The context window](https://code.claude.com/docs/en/how-claude-code-works#the-context-window)
