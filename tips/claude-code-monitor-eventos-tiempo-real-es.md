---
date: 2026-05-04
type: tip
title_es: "Monitor en Claude Code: tu agente reacciona cuando algo pasa, no cada 30 segundos"
title_en: "Monitor in Claude Code: your agent reacts when something happens, not every 30 seconds"
---

> **TL;DR** El tool `Monitor` lanza un script en background y convierte cada línea de stdout en una notificación. Claude reacciona solo cuando hay un evento — un error en el log, un test que falla, un PR aprobado. Sin polling, sin gastar tokens en preguntar "¿ya está?".

Tienes el dev server arrancando, una suite de tests corriendo, o un PR esperando CI. Con [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes) cada 2 minutos durante 10 minutos pagas **5 llamadas completas a la API** preguntando lo mismo: "¿ya está?". Monitor invierte esa lógica. Claude se engancha al stdout de un comando — `tail -f`, un script que comprueba CI, un `while true` — y solo despierta cuando llega una línea que importa.

Anthropic lo lanzó en `v2.1.98` (Week 15 de abril 2026). El `/loop` que ya conoces ahora también lo invoca solo cuando puede ahorrarte el polling.

## Cómo funciona por dentro

`Monitor` toma 4 parámetros:

| Parámetro | Detalle |
|---|---|
| `description` | Etiqueta que verás en cada notificación |
| `command` | El script cuyo stdout se convierte en stream de eventos |
| `timeout_ms` | Tiempo máximo (default 5 min, máx 1 h) |
| `persistent` | Si vive durante toda la sesión (`true`) o se autodestruye al timeout |

Cada línea de stdout es una notificación que despierta la sesión principal. Si llegan varias líneas en menos de 200 ms se agrupan en una sola — útil para outputs multilínea de un mismo evento. El stderr no se streamea, va al archivo de salida.

Si el script empieza a vomitar cientos de líneas por segundo, Claude lo para automáticamente. La selección de filtros es tu responsabilidad.

## Resultado

```
> Tail server.log y avísame cuando aparezca un 5xx

⏺ Monitor iniciado
   command: tail -f server.log | grep --line-buffered -E " 5[0-9]{2} "
   description: server-5xx-watcher

[12:14:03] 192.168.1.4 - "GET /api/users" 503 0.124s
⏺ Detectado un 503 en /api/users. Investigo el handler...
```

Claude no preguntó nada en 12 minutos. Solo reaccionó cuando había algo a lo que reaccionar.

## Cómo usarlo

### **1. Stream filter — vigila logs sin parar**

```
> Monitorea app.log y dime cuando aparezca un ERROR o Traceback

# Equivale internamente a:
tail -f app.log | grep --line-buffered -E "ERROR|Traceback|FAILED"
```

`grep --line-buffered` es **obligatorio** en cualquier pipe. Sin él, el buffering retrasa los eventos varios minutos.

### **2. Poll-and-if — vigila CI o un PR**

```
> Cada 30 segundos comprueba el CI del PR #421 y avísame cuando pase a green o red
```

Para fuentes remotas usa intervalos de **30 s o más**; para chequeos locales `0.5–1 s` está bien. Maneja fallos transitorios con `|| true` para que un timeout puntual no termine el monitor.

### **3. Wait-once — espera a que el dev server arranque**

```
> Espera hasta que el dev server diga "Ready in" y entonces ejecuta los tests E2E
```

Patrón clásico: `until grep -q "Ready in" dev.log; do sleep 0.5; done`. Para esto a veces basta con `Bash` y `run_in_background`, pero Monitor te da la notificación bonita en el transcript.

## Cobertura esencial

> "Si este proceso se cayera ahora mismo, ¿mi filtro emitiría algo?"

Un filtro que solo busca `elapsed_steps=` falla en silencio si el script revienta. Filtra siempre los **estados terminales** (éxito **Y** fallo): `elapsed_steps=|Traceback|Error|FAILED`.

## /loop vs Monitor

| Caso | Usa | Por qué |
|---|---|---|
| "Avísame cuando el test #23 falle" | Monitor | Silencio = 0 tokens; solo la línea del fallo entra a la sesión |
| "Cada 5 min hazme un check completo del estado" | `/loop` | Cada tick necesita razonamiento, no solo una línea |
| "Tail del log buscando 5xx" | Monitor | Eventos asíncronos de baja frecuencia |
| "Resumen periódico que compara iteraciones" | `/loop` | Necesita memoria del tick anterior |

## Referencia

| Aspecto | Detalle |
|---|---|
| Versión mínima | Claude Code `v2.1.98` |
| Tipo | Built-in tool (no requiere setup) |
| Stream | stdout — cada línea es una notificación |
| Batching | Líneas en ≤ 200 ms se agrupan |
| Stderr | Va al archivo de salida, no streamea |
| Auto-stop | Tras un volumen excesivo de eventos |
| Pairs con | `/loop` (lo invoca cuando puede saltarse el polling) |

> Documentación oficial: [Monitor tool reference](https://code.claude.com/docs/en/tools-reference#monitor-tool)
