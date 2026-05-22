---
date: 2026-05-22
type: tip
title_es: "Claude Code Router: el truco que abarata Claude Code (con el trade-off que nadie cuenta)"
title_en: "Claude Code Router: the trick to cheaper Claude Code (with the trade-off nobody mentions)"
---
> **TL;DR** `npm install -g @musistudio/claude-code-router` mete un proxy local entre Claude Code y el modelo, y te deja enrutar las peticiones a DeepSeek, Qwen, Ollama, OpenRouter o lo que quieras. Configuras `~/.claude-code-router/config.json` con tus providers y reglas (por escenario: `default`, `background`, `think`, `longContext`, `webSearch`), arrancas con `ccr code`, y switcheas modelo al vuelo con `/model`. **El trade-off honesto que nadie te cuenta**: te llevas el UX de Claude Code, pero no a Claude. DeepSeek dentro de Claude Code sigue siendo DeepSeek — mejor que ChatGPT en muchas tareas, pero peor que Sonnet 4.6 en agentic y razonamiento.

Cada vez más gente busca "claude code gratis", "claude code ollama", "claude code unlimited". Detrás de todas esas búsquedas está la misma pregunta: ¿puedo seguir programando con esta CLI cuando agoto el plan o cuando el código no debería salir de mi máquina? La respuesta de la comunidad — no de Anthropic — es [Claude Code Router](https://github.com/musistudio/claude-code-router), un proyecto open source con 26k+ estrellas que intercepta las llamadas de Claude Code y las traduce a casi cualquier proveedor.

No es magia. Es un proxy que cambia `ANTHROPIC_BASE_URL` para apuntar a tu máquina, y reescribe las requests al formato del proveedor que elijas. Lo que te llevas: la CLI, los slash commands, los hooks, las skills, los plugins. Lo que NO te llevas: a Claude.

Resultado:

```
> ccr code

Claude Code Router running on localhost:3456
Default model: deepseek,deepseek-chat

> /model openrouter,anthropic/claude-sonnet-4-6

Switched to claude-sonnet-4-6 via OpenRouter for this turn

> /model ollama,qwen2.5-coder:14b

Switched to qwen2.5-coder:14b (local) for this turn
```

## Instalación

```bash
# 1. Claude Code (si no lo tienes ya)
npm install -g @anthropic-ai/claude-code

# 2. El router
npm install -g @musistudio/claude-code-router

# 3. Verifica
ccr --version
```

## Configuración mínima (DeepSeek + Ollama)

Crea `~/.claude-code-router/config.json`:

```json
{
  "Providers": [
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/chat/completions",
      "api_key": "sk-...",
      "models": ["deepseek-chat", "deepseek-reasoner"]
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": ["qwen2.5-coder:14b", "llama3.1:8b"]
    }
  ],
  "Router": {
    "default": "deepseek,deepseek-chat",
    "background": "ollama,qwen2.5-coder:14b",
    "think": "deepseek,deepseek-reasoner",
    "longContext": "deepseek,deepseek-chat",
    "webSearch": "deepseek,deepseek-chat"
  }
}
```

Las cinco claves de `Router` no son decoración — son **escenarios distintos** que Claude Code dispara según el tipo de operación:

| Escenario | Cuándo se usa | Modelo recomendado |
|---|---|---|
| `default` | Conversación normal | El más barato útil (DeepSeek Chat) |
| `background` | Subagents, tareas paralelas | Local (Ollama) — son baratas y muchas |
| `think` | `/think`, planning, razonamiento | El mejor que tengas (reasoner / Sonnet vía OpenRouter) |
| `longContext` | Ventanas largas (>32k tokens) | Modelo con context window grande |
| `webSearch` | Tool web search | El más capaz para parsear resultados |

Arranca con `ccr code` (en vez de `claude`). Para recargar config sin reiniciar: `ccr restart`. Hay UI: `ccr ui`. Para cambiar de modelo en mitad de conversación: `/model <provider>,<modelo>`.

## El trade-off honesto

Esto es lo que **no encuentras** en los blogs de "Claude Code unlimited":

- **Te llevas el UX, no a Claude.** DeepSeek-Chat dentro de Claude Code sigue siendo DeepSeek — bueno para refactors y boilerplate, peor en agentic, tool use complejo y razonamiento de varios pasos.
- **Algunas features [requieren Claude](/es/tips/claude-code-elegir-modelo-adecuado).** Auto mode necesita el classifier de Anthropic. [`/advisor`](/es/tips/claude-code-advisor-opus-sonnet) llama a Opus específicamente. El [combo Figma + Chrome MCP con `/goal`](/es/tips/claude-code-figma-chrome-mcp-pixel-perfect) funciona porque Claude maneja el bucle agentic — con un modelo más débil se rompe a los 3-4 turnos.
- **Es proyecto comunitario.** Cuando Claude Code cambia su API (pasa cada semanas), el router puede romperse hasta que `musistudio` parchee. No es production-critical infrastructure.
- **Privacy: depende del provider.** Ollama → tu máquina, 100% local. DeepSeek/Qwen → servidores del proveedor (China en estos dos casos). Decide en función del repo.

## Cuándo SÍ vale la pena

- **Te agotaste el plan Pro/Max** y necesitas seguir el día → switch a DeepSeek por unas horas
- **Código sensible que no puede salir de tu máquina** → ruta a Ollama local
- **Tareas masivas y baratas** (renombrar 200 archivos, generar boilerplate) → background a un modelo cheap
- **Vives en una región sin facturación directa de Anthropic** → OpenRouter via router
- **Quieres comparar modelos** dentro del mismo flow → switch al vuelo con `/model`

## Cuándo NO usarlo

- **Cuando trabajas con agentic complejo** — [auto mode](/es/tips/claude-code-auto-mode-alternativa-yolo), [agent teams](/es/tips/claude-code-agent-teams-equipos), [subagents](/es/tips/claude-code-subagentes-pierden-contexto). Esos flujos asumen capacidades específicas de Claude.
- **Cuando tu cuello de botella es razonamiento**, no coste. Pagar Sonnet 4.6 y planificar bien sale más barato que ahorrar en tokens y reescribir mal.
- **Cuando ahorras tokens, no presupuesto.** Si el problema es que se te llena el contexto, son [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos), no cambiar de modelo.

## Referencia

| Comando | Qué hace |
|---|---|
| `ccr code` | Lanza Claude Code apuntando al router |
| `ccr restart` | Recarga config sin matar la sesión |
| `ccr ui` | Abre la interfaz web del router |
| `ccr model` | Lista modelos / cambia el default desde CLI |
| `/model <provider>,<modelo>` | Cambia modelo dentro de Claude Code, al vuelo |

| Provider soportado | Mejor para |
|---|---|
| DeepSeek | Chat barato (`deepseek-chat`) y reasoner (`deepseek-reasoner`) |
| Qwen 3 / Qwen Coder | Coder fuerte vía Alibaba (DashScope) o Ollama local |
| Ollama / LM Studio / vLLM | Local, privacidad total, sin coste por token |
| OpenRouter | Gateway a cientos de modelos (incluido el propio Claude) |
| GLM (Zhipu) | Bilingüe EN/ZH, barato |

> Documentación oficial: [musistudio/claude-code-router (GitHub)](https://github.com/musistudio/claude-code-router) · [Routing scenarios docs](https://musistudio.github.io/claude-code-router/)

## Requisitos

- Node.js 18+
- Claude Code v2.0+
- API key del provider que elijas (DeepSeek, OpenRouter…) o Ollama corriendo en local
