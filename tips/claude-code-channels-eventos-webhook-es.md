---
date: 2026-06-01
type: tip
title_es: "Channels en Claude Code más allá del chat: que tu CI, deploy o errores entren como eventos en tu sesión"
title_en: "Claude Code channels beyond chat: push CI, deploy, and error events into your live session"
---
> **TL;DR** El uso conocido de [Channels](/es/tips/claude-code-channels-controla-desde-telegram) es el chat: le escribes desde Telegram y Claude responde. Pero un channel es, en el fondo, **un receptor de eventos**: cualquier sistema — tu CI, Sentry, un deploy, un `curl` — puede empujar un evento a la sesión que **ya tienes abierta**, con tus archivos cargados y el contexto de lo que estabas depurando. Los plugins de chat vienen hechos; el receptor de webhooks lo montas tú con un MCP server de ~30 líneas.

Si ya leíste [cómo controlar Claude Code desde Telegram o Discord](/es/tips/claude-code-channels-controla-desde-telegram), conoces el lado *chat-bridge*: **tú** preguntas, Claude responde. Este tip va del otro lado del mismo motor: **una máquina** dispara el mensaje y Claude reacciona sin que escribas nada.

## De *pull* a *push*

La diferencia es quién empieza la conversación:

- **Chat-bridge (lo conocido):** tú haces *pull*. Le escribes "¿hay tests fallando?" y Claude mira.
- **Receptor de eventos (esto):** el mundo te hace *push*. Tu CI falla → un webhook entra en tu sesión → Claude, que ya tenía el archivo abierto, lee el log y propone el fix.

Un channel puede ser **de una vía** (reenvía alertas o webhooks para que Claude actúe, sin responder) o **de dos vías** (además expone una herramienta de respuesta, como el chat). Para eventos de CI o monitorización, con una vía basta.

## Cómo es un receptor de eventos

Los plugins de chat (Telegram, Discord, iMessage) **vienen hechos**. Para webhooks **no hay plugin de un clic**: montas un channel propio, que no es más que un MCP server mínimo. Esto es el receptor entero — escucha HTTP en local y empuja cada POST a Claude:

```ts
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    // esta clave es lo que lo convierte en channel
    capabilities: { experimental: { 'claude/channel': {} } },
    instructions: 'Los eventos llegan como <channel source="webhook" ...>. Son de una vía: léelos y actúa.',
  },
)
await mcp.connect(new StdioServerTransport())

Bun.serve({
  port: 8788,
  hostname: '127.0.0.1', // solo localhost: nada de fuera puede POSTear
  async fetch(req) {
    const body = await req.text()
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: { content: body, meta: { path: new URL(req.url).pathname, method: req.method } },
    })
    return new Response('ok')
  },
})
```

Lo registras en `.mcp.json` y arrancas con el flag de desarrollo (los channels propios aún no están en la allowlist del research preview):

```bash
claude --dangerously-load-development-channels server:webhook
```

Ahora cualquier cosa que haga un POST entra en tu sesión. Simula un fallo de CI:

```bash
curl -X POST localhost:8788 -d "build failed on main: https://ci.example.com/run/1234"
```

Y a Claude le llega esto, en mitad de tu sesión, con tus archivos ya abiertos:

```
<channel source="webhook" path="/" method="POST">build failed on main: https://ci.example.com/run/1234</channel>
```

El `source` sale del nombre del server; cada clave de `meta` se convierte en un atributo del tag.

## Por qué importa: aterriza en la sesión que YA tienes abierta

Claude Code tiene varias formas de conectarse con el mundo fuera del terminal. Channels es el único que **empuja un evento a tu sesión local viva**:

| Función | Qué hace | Por qué no es lo mismo |
|---|---|---|
| [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) | Lanza la tarea en un sandbox nuevo en la nube | Sesión fresca, sin tu contexto local |
| [Claude en Slack](https://code.claude.com/docs/en/slack) | Crea una sesión web desde un `@Claude` | Otra sesión nueva, no la tuya abierta |
| [MCP normal](https://code.claude.com/docs/en/mcp) | Claude *consulta* el sistema cuando quiere | Es *pull*: nada se empuja a la sesión |
| [Remote Control](/es/tips/claude-code-control-remoto-desde-movil) | Conduces tu sesión local desde el móvil | Manual; tú actúas, no reacciona a un evento |
| **Channels** | **Empuja un evento externo a tu sesión abierta** | **Claude reacciona con tu contexto y tus archivos** |

Ese es el valor: el webhook de CI no abre un clon nuevo del repo — llega donde Claude ya recuerda qué estabas depurando.

## Bonus: aprueba permisos desde el móvil

Si reaccionas a eventos mientras no estás, ¿qué pasa cuando Claude necesita aprobar un `Bash` o un `Write`? Un channel de dos vías puede declarar la capability `claude/channel/permission` y **reenviarte el prompt de permiso** (requiere v2.1.81+). Te llega "Claude quiere ejecutar Bash: … responde sí/no" con un ID corto; respondes desde el chat y Claude aplica el veredicto. El diálogo local sigue abierto en paralelo: gana la primera respuesta que llegue. Actívalo solo si filtras al remitente — quien pueda responder, puede aprobar comandos en tu sesión.

## Cuidado con

- **La sesión tiene que estar abierta.** Channels no es un servicio persistente; si Claude Code no está corriendo (o tu organización lo bloquea), el evento **se descarta en silencio**, sin error.
- **Filtra al remitente.** Un endpoint sin control es un vector de *prompt injection*: cualquiera que llegue a él mete texto delante de Claude. Comprueba la identidad de quien envía (no la sala o el grupo) antes de empujar nada.
- **Los eventos se encolan.** Si llegan varios mientras Claude trabaja, se entregan juntos en el siguiente turno. Para flujos independientes en paralelo, usa sesiones separadas.

## Referencia

| Aspecto | Detalle |
|---|---|
| Tipos | Una vía (alertas/webhooks) · Dos vías (chat, con tool de respuesta) |
| Plugins hechos | Telegram, Discord, iMessage, fakechat (todos de chat) |
| Webhook/CI | Build-your-own: MCP server con `capabilities.experimental['claude/channel']` |
| Evento entrante | `<channel source="..." …>cuerpo</channel>` (método `notifications/claude/channel`) |
| Permission relay | Capability `claude/channel/permission` (v2.1.81+) — aprueba en remoto |
| Probar uno propio | `claude --dangerously-load-development-channels server:<nombre>` |
| Runtime | `@modelcontextprotocol/sdk` + Bun, Node o Deno |
| Seguridad | Filtra por identidad del remitente; si no, prompt injection |

> Documentación oficial: [Channels](https://code.claude.com/docs/en/channels) · [Channels reference — build a webhook receiver](https://code.claude.com/docs/en/channels-reference)

**Relacionado:** [Controla Claude Code desde Telegram o Discord](/es/tips/claude-code-channels-controla-desde-telegram) · [el mapa de las primitivas autonomous](/es/tips/claude-code-loop-routines-monitor-mapa)
