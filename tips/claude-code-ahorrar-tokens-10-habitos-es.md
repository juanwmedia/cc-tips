---
date: 2026-04-08
type: tip
title_es: "Cómo ahorrar tokens en Claude Code: 10 hábitos de la documentación oficial"
title_en: "How to Save Tokens in Claude Code: 10 Habits From the Official Docs"
---
# Quick Tip: Cómo ahorrar tokens en Claude Code: 10 hábitos de la documentación oficial

> **TL;DR** Si tu sesión de Claude Code se acaba antes que hace unos meses, no eres solo tú — hay quejas reales por todos lados. Pero parte de la solución sí depende de ti. Anthropic tiene una página entera en la docs (*"Manage costs effectively"*) con 10 hábitos verificables. Aquí están los 10, con la cita exacta cuando aplica.

Lo curioso de estos 10 hábitos es que ninguno es esotérico. Son sentido común. Y precisamente por eso son los primeros que se pasan por alto: cuando algo es obvio, lo descartas como "ya lo sé" antes de aplicarlo.

## Los 10 hábitos

### **1. Monitoriza dónde se te van los tokens**

`/context` desglosa cada categoría: system prompt, MCP tools, mensajes, free space. Si no lo miras periódicamente, conduces a ciegas. Tip dedicado: [/context para monitorizar el uso de tokens](/es/tips/claude-code-comando-context-uso-tokens).

### **2. Limpia entre tareas**

`/clear` cuando cambies de tarea. Antes, `/rename` para encontrar la sesión después con `/resume`.

> *"Stale context wastes tokens on every subsequent message."*

### **3. Compacta con instrucciones explícitas**

`/compact` no es solo "resume". Le puedes decir exactamente qué preservar:

```bash
/compact Focus on code samples and API usage
```

También puedes meter las instrucciones en `CLAUDE.md` bajo `# Compact instructions`.

### **4. Sonnet por defecto. Opus solo para arquitectura**

`/model` para cambiar al vuelo. Subagents simples con `model: haiku` en su configuración.

> *"Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning."*

Tip dedicado: [Cómo elegir el modelo adecuado en Claude Code](/es/tips/claude-code-elegir-modelo-adecuado).

### **5. Desactiva MCP servers que no uses, prefiere CLI tools nativas**

`/mcp` para ver y desactivar servers. Cada server activo deja sus *tool names* en el contexto, aunque las definiciones estén deferred. Prefiere `gh`, `aws`, `gcloud`, `sentry-cli` antes que MCP servers — las CLI tools no añaden ni siquiera el listing.

### **6. Preprocesa output verboso con hooks**

Un `PreToolUse` hook intercepta el comando antes de ejecutarlo y puede reescribirlo via `updatedInput`. Convierte 10.000 líneas de test output en las 50 que importan. Claude solo ve el output filtrado. Tip dedicado: [Hooks en Claude Code: automatiza tu flujo de trabajo](/es/tips/claude-code-hooks-automatizar-flujo-trabajo).

### **7. Mueve instrucciones de CLAUDE.md a Skills**

`CLAUDE.md` se carga al inicio de la sesión. Esos tokens están en tu contexto desde el primer turno hasta el último. Las Skills cargan **on-demand** solo cuando se invocan. Mueve todo lo específico de un workflow a una Skill. Objetivo de la docs: `CLAUDE.md` por debajo de 200 líneas.

### **8. Baja el thinking en tareas simples**

Los thinking tokens se facturan como output, y el budget por defecto puede ser decenas de miles de tokens por request. `/effort low` cuando no haces razonamiento profundo, o `MAX_THINKING_TOKENS=8000` desde el environment para topar el budget global. Tip dedicado: [Cómo ajustar el effort level en Claude Code](/es/tips/claude-code-effort-level-ajustar-razonamiento).

### **9. Delega operaciones verbosas a subagents**

`npm test`, `gh pr view`, procesar logs: todo eso quema contexto en tu conversación principal. Delegado a un subagent, el output verboso se queda en su contexto — solo vuelve el resumen. Y ojo a los gotchas: [los subagents pierden contexto](/es/tips/claude-code-subagentes-pierden-contexto).

> *"the verbose output stays in the subagent's context while only a summary returns to your main conversation."*

### **10. Plan mode antes de implementar**

`Shift+Tab` entra en plan mode. Claude explora el codebase y propone un approach **antes** de tocar nada. Si la dirección inicial es la equivocada, lo descubres en plan mode (barato) en vez de a mitad de implementación (caro y con re-trabajo).

> *"preventing expensive re-work when the initial direction is wrong."*

## Por qué importa ahora

Hay un volumen creciente de quejas sobre sesiones que se acaban antes. La parte estructural no la controlas — pero la parte de hábitos sí. Y la docs oficial te dice cómo arreglarla en 10 puntos concretos.

Ninguno es magia. Todos son sentido común. Y como son sentido común, son los primeros que se pasan por alto.

> Documentación oficial: [Manage costs effectively](https://code.claude.com/docs/en/costs) · Ver también: [/context](/es/tips/claude-code-comando-context-uso-tokens) · [1M tokens](/es/tips/claude-code-1m-tokens-ventana-contexto) · [Cuándo se cargan las features](/es/tips/claude-code-cuando-se-cargan-features-contexto)
