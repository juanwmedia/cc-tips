---
date: 2026-06-12
type: tip
title_es: "MCP en Claude Code: conecta 20 servidores sin comerte el contexto"
title_en: "MCP in Claude Code: connect 20 servers without eating your context"
---

> **TL;DR** Las tools de tus MCP ya **no cargan al arrancar**: van diferidas y Claude las busca con una herramienta interna (`ToolSearch`) solo cuando las necesita. Al inicio entran únicamente los nombres y una instrucción por servidor. Es el mismo truco que ya conoces de las skills, aplicado a MCP. Viene activado por defecto, y se afina con `ENABLE_TOOL_SEARCH` si quieres otro comportamiento.

Durante meses la regla fue [cinco servidores bastan, cincuenta estorban](/es/tips/claude-code-mejores-servidores-mcp): cada MCP volcaba las definiciones completas de todas sus tools en el contexto al arrancar, y conectar GitHub + Notion + Chrome DevTools te costaba decenas de miles de tokens antes de escribir tu primera palabra. Tool Search cambió esa matemática en silencio, y casi nadie se ha enterado porque, desde fuera, todo funciona igual.

## El truco que ya conoces (de las skills)

Las [skills](/es/tips/claude-code-skills-comandos-personalizados) siempre han funcionado así: en contexto vive solo el nombre y una descripción de una línea; el cuerpo entero carga cuando se invocan. Divulgación progresiva: índice barato siempre visible, contenido caro solo cuando hace falta.

Tool Search aplica ese mismo patrón a tus MCP, y la doc hace la comparación tal cual: *"server instructions help Claude understand when to search for your tools, similar to how skills work"*.

| | Skills | Tools MCP (con Tool Search) |
|---|---|---|
| Siempre en contexto | nombre + descripción | nombres de tools + instrucciones del servidor |
| Carga bajo demanda | el cuerpo del SKILL.md | el esquema completo, vía `ToolSearch` |

## Cómo funciona

Al arrancar la sesión solo entran los **nombres** de las tools y las **instrucciones de cada servidor** (truncadas a 2KB). Cuando Claude necesita una tool concreta, llama a `ToolSearch` (admite búsqueda por keywords, no hace falta el nombre exacto), el esquema completo entra en contexto en ese momento, y la usa. Solo pagan contexto las tools que de verdad se usan.

Lo veo cada día: en la sesión donde escribo esto hay unos 90 nombres de tools diferidas (Notion, Canva, Chrome DevTools...) y Claude solo cargó los esquemas de las tres que tocó para publicar. Antes, esos 90 esquemas habrían entrado enteros al arrancar.

Compruébalo tú con [`/context`](/es/tips/claude-code-comando-context-uso-tokens): la categoría de MCP tools que antes dominaba la ventana ahora es una fracción.

## Los mandos

Viene activado por defecto. Si quieres otro comportamiento, la variable `ENABLE_TOOL_SEARCH` (en el bloque `env` de tus settings o al lanzar):

| Valor | Qué hace |
|---|---|
| *(sin tocar)* | Todo diferido, descubrimiento bajo demanda. El default |
| `auto` | Híbrido: si todas las tools caben en el 10% del contexto, cargan al inicio; el resto se difiere |
| `auto:N` | Igual, con umbral propio (0-100), p. ej. `auto:5` |
| `false` | Comportamiento antiguo: todo al inicio, sin deferral |
| `true` | Fuerza el deferral incluso en Vertex o detrás de un proxy |

Y por servidor: si uno debe estar siempre visible sin paso de búsqueda (porque lo usas en cada turno), exímelo con `alwaysLoad` en su configuración:

```json
{
  "mcpServers": {
    "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/", "alwaysLoad": true }
  }
}
```

## La letra pequeña

- **Haiku no lo soporta** (requiere modelos con `tool_reference`).
- **En Vertex AI viene desactivado** por defecto (soportado desde Sonnet 4.5 y Opus 4.5; fuerza con `ENABLE_TOOL_SEARCH=true`).
- **Se apaga solo** si tu `ANTHROPIC_BASE_URL` apunta a un proxy no first-party.
- Si publicas tu propio servidor MCP, las **server instructions** son ahora tu escaparate: dilas como la `description` de una skill (qué tareas cubren tus tools y cuándo buscarlas).

## ¿Entonces la regla de los cinco ya no vale?

La mitad de contexto de [aquella regla](/es/tips/claude-code-mejores-servidores-mcp), no. Pero la curación sigue ganando por otras dos razones: cada servidor conectado sigue metiendo sus nombres e instrucciones, y un menú gigante de opciones sigue costando decisiones por turno. Conecta los que uses; ahora el precio de equivocarte es mucho más bajo. Bonus de [caché](/es/tips/claude-code-prompt-caching-turno-lento-consumo): con las tools diferidas, conectar o desconectar un servidor a mitad de sesión ya no invalida el prefijo.

> Documentación oficial: [Scale with MCP Tool Search](https://code.claude.com/docs/en/mcp)

## Requisitos

Activado por defecto en la API de Anthropic con Sonnet y Opus. Ver la letra pequeña para Haiku, Vertex AI y proxies.
