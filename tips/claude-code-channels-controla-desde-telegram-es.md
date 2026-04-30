---
date: 2026-03-21
type: tip
title_es: "Controla Claude Code desde Telegram o Discord con Channels"
title_en: "Control Claude Code from Telegram or Discord with Channels"
---
# Quick Tip: Controla Claude Code desde Telegram o Discord con Channels

> **TL;DR** Claude Code ahora acepta mensajes desde Telegram y Discord mientras trabaja en tu terminal. Le escribes desde el móvil, él ejecuta, y te responde por el mismo canal. Es bidireccional, seguro (allowlist de remitentes), y se activa con `--channels`.

Channels es un sistema que empuja eventos externos a tu sesión de Claude Code a través de un MCP server. Telegram, Discord, o cualquier servicio que implementes. Claude lee el mensaje, actúa con todas sus herramientas (bash, edición, lectura, subagents), y responde por el mismo canal.

Si te suena a lo que hace [OpenClaw](https://openclaw.ai/) — un asistente AI que vive en tus apps de chat y ejecuta tareas en tu máquina — no es coincidencia. Anthropic está construyendo esa misma visión, pero integrada nativamente en Claude Code: con acceso a [hooks](/es/articulos/claude-code-hooks-guia-practica), [skills](/es/articulos/claude-code-skills-flujos-trabajo-personalizados), [subagents](/es/articulos/claude-code-subagents-guia-espanol) y MCP.

Resultado — le escribes a tu bot de Telegram:

```
Tú (Telegram): ¿Hay tests fallando en el proyecto?

Claude Code (terminal): ejecuta npm test, analiza resultados

Claude Code (Telegram): 2 tests fallando en auth.test.ts:
  - testLoginExpiredToken: expected 401, got 500
  - testRefreshToken: timeout después de 5s
```

## Configuración (Telegram)

### **1. Crear un bot en Telegram**

Abre [BotFather](https://t.me/BotFather) en Telegram, envía `/newbot`, dale un nombre y copia el token.

### **2. Instalar el plugin**

```
/plugin install telegram@claude-plugins-official
```

### **3. Configurar el token**

```
/telegram:configure <tu-token>
```

### **4. Reiniciar con channels activo**

```bash
claude --channels plugin:telegram@claude-plugins-official
```

### **5. Vincular tu cuenta**

Envía cualquier mensaje a tu bot en Telegram. Te responderá con un código de emparejamiento. En Claude Code:

```
/telegram:access pair <código>
/telegram:access policy allowlist
```

La segunda línea bloquea a cualquiera que no seas tú.

## Referencia

| Aspecto | Detalle |
|---|---|
| Qué es | MCP server que empuja eventos a tu sesión |
| Canales soportados | Telegram, Discord, fakechat (demo localhost) |
| Dirección | Bidireccional — Claude lee y responde por el mismo canal |
| Seguridad | Allowlist de remitentes + código de emparejamiento |
| Flag de activación | `--channels plugin:<nombre>@claude-plugins-official` |
| Sesión requerida | Claude Code debe estar corriendo (no es un servicio persistente) |
| Permisos | Los prompts de permisos pausan la sesión hasta que apruebes localmente |
| Estado | Research preview (v2.1.80+) |
| Autenticación | Solo claude.ai login (no API key ni Console) |
| Enterprise | Desactivado por defecto — el admin debe habilitar `channelsEnabled` |

> Documentación oficial: [Channels — Push events into a running session](https://code.claude.com/docs/en/channels)

## Requisitos

- Claude Code v2.1.80+
- [Bun](https://bun.sh) instalado (`bun --version` para verificar)
- Login con claude.ai (no funciona con API key)
- Team/Enterprise: el admin debe habilitar channels en managed settings
