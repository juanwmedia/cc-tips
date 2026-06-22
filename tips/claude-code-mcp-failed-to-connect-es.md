---
date: 2026-06-22
type: tip
title_es: "MCP «Failed to connect» en Claude Code: el árbol de decisión que te ahorra el pánico"
title_en: "MCP \"Failed to connect\" in Claude Code: the decision tree that ends the panic"
---

> **TL;DR** Abre `/mcp` para ver cuál servidor falló. Si es **remoto** (http/sse), el patrón manda: **401/403** es auth caducada (re-autentica desde `/mcp`), **404/405** significa que el servidor está vivo pero la URL está mal, y **5xx o timeout** Claude lo reintenta solo (3 veces al arrancar, 5 a mitad de sesión). Si es **local** (stdio), no se reconecta solo: la app que lo sirve (Figma, Chrome) tiene que estar abierta. Y el truco que cierra el caso: si dice «Connection closed» al instante, **corre el comando del servidor tú mismo en la shell** y lee el error real.

Cada vez conectas más MCPs, y tarde o temprano uno se pone en rojo con un escueto «Failed to connect». El mensaje no te dice nada y acabas tocando la configuración a ciegas. Casi nunca es tu config: es una de tres cosas, y se distingue en treinta segundos.

La clave es que **Claude Code se comporta distinto según el transporte**. Un servidor remoto (HTTP/SSE) se reconecta solo con reintentos; uno local (stdio) es un proceso en tu máquina y **no se reconecta nunca solo**. Y los errores de autenticación o de «no encontrado» no se reintentan: necesitan que cambies algo.

## Lo primero: quién falló y por qué

```
> /mcp

  figma            ✓ connected    8 tools
  notion           ✗ failed       (auth)
  chrome-devtools  ⏸ pending
```

Dentro de la sesión, `/mcp` te muestra el estado de cada servidor y su número de tools. Desde la terminal:

```bash
claude mcp list          # estado de todos
claude mcp get notion    # detalle de uno (incluye ⏸ Pending approval / ✗ Rejected)
```

## El árbol de decisión

**1. ¿Es remoto (http/sse)? Mira el patrón del fallo**

- **401 / 403 → es auth.** El token caducó o nunca te autenticaste. Es lo típico de los MCP de empresa detrás de SSO o IAM: caducan cada cierto tiempo y hay que **re-autenticar desde `/mcp`**. Claude Code **no reintenta** los errores de auth, así que no se arregla solo por esperar.
- **404 / 405 → el servidor está vivo, la URL no.** Llega a responder, o sea que no es un problema de red; revisa la ruta del endpoint que pusiste en `claude mcp add`.
- **5xx, connection refused o timeout → transitorio.** Claude reintenta con backoff: hasta 3 veces al arrancar (desde la v2.1.121) y hasta 5 si se cae a mitad de sesión. Si después sigue en `failed`, el servidor está caído o hay red de por medio; reintenta a mano desde `/mcp`.

**2. ¿Es local (stdio)? El proceso tiene que estar vivo**

Los servidores stdio son procesos en tu máquina y **Claude Code no los reconecta solos**. Dos causas:

- **La app que lo sirve se cerró.** El MCP de Figma o el de Chrome dependen de que su app esté abierta y corriendo. Si la cierras, el MCP muere. Ábrela y reconecta desde `/mcp`.
- **«Connection closed» nada más arrancar.** El comando del servidor ni siquiera llega a ejecutarse.

**3. El truco universal: corre el comando tú mismo**

Coge el comando exacto del servidor (lo ves en `claude mcp get <name>`) y ejecútalo en tu shell. Si falla ahí, ese es tu error de verdad (un binario que falta, un argumento mal, una variable de entorno sin definir), y no tiene nada que ver con Claude Code.

```bash
# si esto peta en tu terminal, ahí está el problema
npx -y @tu/servidor-mcp
```

Dos clásicos de stdio: en **Windows**, `npx` necesita el envoltorio `cmd /c` (`claude mcp add --transport stdio mi-server -- cmd /c npx -y @paquete`); y si el servidor **escribe logs en stdout**, corrompe el protocolo (el log debe ir a stderr).

## Referencia rápida

| Señal en `/mcp` | Qué significa | Qué haces |
|---|---|---|
| `✗ failed` + 401/403 | Auth caducada (típico SSO/IAM de empresa) | Re-autentica desde `/mcp` |
| `✗ failed` + 404/405 | El servidor responde, la URL está mal | Revisa la URL del `claude mcp add` |
| `✗ failed` + 5xx/timeout | Transitorio | Claude reintenta (3 al inicio, 5 a mitad); luego, a mano |
| `⏸ pending` | Reconectando, o esperando aprobación | Espera, o aprueba con `claude` |
| stdio caído | El proceso o app se cerró; no se reconecta solo | Abre la app (Figma, Chrome) y reconecta |
| «Connection closed» al instante | El comando no arranca | Córrelo tú en la shell y lee el error |

| Transporte | ¿Se reconecta solo? |
|---|---|
| HTTP / SSE | Sí, con backoff. La auth y el 404 NO se reintentan |
| stdio (local) | No, nunca: reinícialo a mano |

Para conectar y organizar muchos servidores sin comerte el contexto, mira [MCP en Claude Code](/es/tips/claude-code-mcp-servidores-contexto). Y antes de añadir uno nuevo, conecta solo servidores en los que confíes: un MCP que trae contenido externo puede colarte instrucciones.

> Documentación oficial: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)

## Requisitos

- El reintento de la conexión inicial (3 intentos ante errores transitorios) llega en **Claude Code v2.1.121**. La reconexión a mitad de sesión y el comportamiento por transporte aplican en versiones recientes.
