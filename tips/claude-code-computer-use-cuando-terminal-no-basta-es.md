---
date: 2026-04-04
type: tip
title_es: "Claude Code ahora controla todo tu ordenador"
title_en: "Claude Code Now Controls Your Entire Computer"
---
# Quick Tip: Claude Code ahora controla todo tu ordenador

> **TL;DR** Claude Code puede abrir apps, hacer click, escribir y hacer screenshots — directamente desde tu terminal. Compila una app Swift, la lanza, verifica que los botones funcionan, y vuelve al código para arreglar lo que falle. Todo en la misma conversación.

Hay tareas que un terminal no puede resolver: verificar que una app nativa funciona visualmente, depurar un layout que solo se rompe en cierto tamaño de ventana, o interactuar con un simulador iOS. Hasta ahora, eso significaba salir de Claude Code y hacerlo a mano.

Computer use cambia eso. Es un MCP server built-in llamado `computer-use` que le da a Claude acceso visual a tu pantalla. Pero no es lo primero que Claude intenta — es lo último.

## Claude solo toca la pantalla cuando nada más sirve

Claude Code tiene una jerarquía clara de herramientas. Siempre usa la más precisa disponible:

1. **MCP server** — si hay un servidor MCP para el servicio, lo usa
2. **Bash** — si la tarea es un comando de terminal, lo ejecuta
3. **[Chrome](/es/tips/claude-code-chrome-depurar-frontend)** — si es trabajo de navegador y tienes Chrome configurado
4. **Computer use** — solo cuando ninguna de las anteriores sirve

El control de pantalla es la opción nuclear: potente pero lenta. Claude la reserva para lo que nada más puede alcanzar: apps nativas, simuladores, herramientas sin API.

## La pieza que faltaba en el agente autónomo

Computer use no es una feature aislada. Es el último eslabón de una cadena que Anthropic lleva meses construyendo — cada pieza reduciendo la distancia entre "yo hago" y "Claude hace por mí":

| Capacidad | Qué resuelve |
|---|---|
| [Headless mode](/es/tips/claude-code-modo-headless-agente-autonomo) | Claude trabaja sin ti delante |
| [Notificaciones](/es/tips/claude-code-notificacion-cuando-termina) | Te avisa cuando termina |
| [Remote Control](/es/tips/claude-code-control-remoto-desde-movil) | Lo controlas desde el móvil |
| [Channels](/es/tips/claude-code-channels-controla-desde-telegram) | Le hablas desde Telegram/Discord |
| [/loop](/es/tips/claude-code-loop-tareas-recurrentes) | Vigila de forma recurrente |
| **Computer use** | **Controla tu pantalla cuando el terminal no basta** |

La combinación de todas: un agente autónomo que trabaja en tu máquina, te contacta por el canal que prefieras, y ahora también puede ver y tocar tu pantalla.

## Cómo activarlo

### **1. Habilitar el MCP server**

```
/mcp
```

Busca `computer-use` en la lista. Selecciónalo y elige **Enable**. Se guarda por proyecto.

### **2. Conceder permisos de macOS**

La primera vez, macOS te pedirá dos permisos:
- **Accesibilidad**: para que Claude haga click, escriba, y haga scroll
- **Grabación de pantalla**: para que Claude vea lo que hay en tu pantalla

### **3. Pedir algo que necesite GUI**

```
Compila el target MenuBarStats, lánzalo, abre preferencias,
y verifica que el slider de intervalo actualiza el label.
Haz screenshot cuando termines.
```

Claude compila, lanza, interactúa con la UI, y te reporta.

## Referencia

| Aspecto | Detalle |
|---|---|
| MCP server | `computer-use` (built-in, desactivado por defecto) |
| Activar | `/mcp` → seleccionar → Enable |
| Plataforma | macOS (CLI). Windows solo en Desktop app |
| Planes | Pro y Max (no Team ni Enterprise) |
| Versión mínima | v2.1.85+ |
| Permisos macOS | Accesibilidad + Grabación de pantalla |
| Aprobación de apps | Por sesión — Claude pide permiso para cada app |
| Parar | `Esc` en cualquier momento o `Ctrl+C` en terminal |
| Jerarquía | MCP → Bash → Chrome → Computer use (último recurso) |

> Documentación oficial: [Computer use — Let Claude use your computer from the CLI](https://code.claude.com/docs/en/computer-use)

## Requisitos

- macOS (no disponible en Linux ni Windows vía CLI)
- Claude Code v2.1.85+
- Plan Pro o Max (no funciona con API key, Bedrock, Vertex ni Foundry)
- Sesión interactiva (no funciona con `-p`)
