---
date: 2026-05-18
type: tip
title_es: "Claude Code está caído (o eres tú): cómo saberlo en 30 segundos"
title_en: "Is Claude Code down (or is it you)? How to tell in 30 seconds"
---

> **TL;DR** Tres comprobaciones en orden, 30 segundos cada una. **1) status.claude.com** — Anthropic publica el uptime de Claude Code como componente separado (99,14% en los últimos 90 días) con Atom/RSS, email, SMS, Slack y webhooks. **2) DownDetector** — si el status page va lento en reflejar el incidente, esta página recoge reportes de usuarios en tiempo real. **3) `/doctor`** — descarta que el problema sea local (MCP roto, ripgrep, settings inválidas). Si todo está verde y aún así "Claude parece más tonto hoy", el culpable casi siempre es presión de contexto (autocompact thrashing), no el modelo.

Hay un meme recurrente en Reddit y X: *"Claude Code is getting dumber"*. A veces es real (incidente o degradación). Casi siempre es uno de tres errores de percepción: tu context window al 80%, un MCP que metió 30k tokens de basura, o anchoring de una conversación demasiado larga. Aquí cómo distinguirlo.

## 1. status.claude.com — primer sitio donde mirar

Anthropic publica un status page con uptime por componente. Claude Code está **separado** de Claude API, Claude.ai y Claude Cowork:

| Componente | Significado |
|---|---|
| **Claude Code** | El CLI directamente |
| **Claude API** (`api.anthropic.com`) | El backend al que van tus prompts. Si esto cae, Claude Code también |
| **Claude.ai** | El chat web. No afecta a Claude Code |
| **Claude Console** | `platform.claude.com` (gestión de API keys) |

Pulsa "Subscribe" arriba a la derecha para enterarte de los incidentes por email, SMS, Slack, Microsoft Teams, webhook o Atom/RSS antes de que te toquen.

## 2. DownDetector — para corroborar

A veces el status page de Anthropic tarda 15-30 minutos en reflejar un incidente porque el equipo necesita confirmarlo internamente. DownDetector recoge reportes de usuarios en tiempo real:

```
https://downdetector.com/status/claude-ai/
```

Si en DownDetector ves un pico de reportes y `status.claude.com` sigue en verde, espera 10 minutos y vuelve a comprobar. Pico real → está cayendo aunque oficialmente no lo hayan reconocido todavía.

## 3. `/doctor` — descarta problemas locales

Si los dos pasos anteriores salen limpios, el problema no es Anthropic. Es tu setup. Lanza:

```bash
/doctor
```

Audita instalación, settings, MCP servers y uso de contexto en una pasada. Si Claude Code ni siquiera arranca para correr `/doctor`:

```bash
claude doctor
```

Mismo report fuera del CLI. Hay [tip dedicado a `/doctor`](/es/tips/claude-code-doctor-diagnostico) si quieres profundizar.

## "Claude está más tonto hoy" — qué pasa de verdad

El modelo no cambia entre sesiones. Anthropic publica releases con semver y `/release-notes` te dice si algo cambió en tu CLI. Lo que sí cambia es **tu contexto**. Tres síntomas que se confunden con degradación del modelo:

**Autocompact thrashing**. Tu context window se llena, autocompact lo reduce, y el siguiente tool result lo vuelve a llenar. Claude Code para de reintentar para no quemar tokens. Síntoma: respuestas cortas, lentas, parecen "perezosas". Fix:

```bash
/compact "conserva solo el plan y el diff"
# o, si lo anterior ya no hace falta:
/clear
```

**MCP basura**. Un MCP server devuelve un blob enorme (un schema, un dump de DB, un resultado de Playwright) y se come la mitad de tu contexto. Síntoma: la sesión se enlentece tras llamar a un tool. Fix: deshabilita ese MCP con `/mcp` o cierra esa rama de la conversación con [`/branch`](/es/tips/claude-code-fork-session-bifurcar-sesiones).

**Anchoring**. Llevas 200 turnos y la primera mala interpretación contaminó todo lo que vino después. Síntoma: Claude repite errores incluso cuando le señalas el correcto. Fix: `/clear`, empieza limpio. Para no perder lo bueno, dile a Claude que escriba un `/recap` antes.

Si hiciste los tres pasos y nada cambia: probablemente es Claude. Reporta con `/feedback` (adjunta el contexto de la sesión automáticamente).

## Suscríbete antes de que te pille la siguiente caída

Si tu trabajo depende de Claude Code, no esperes a abrir el status page cuando algo va mal:

| Canal | Para |
|---|---|
| Email / SMS | Caídas críticas, fuera del navegador |
| Slack / Microsoft Teams | Si tu equipo trabaja allí, notificación al canal |
| Webhook | Integrar en tu dashboard interno o tu propio bot |
| Atom / RSS | Si llevas todo en un reader |

Te suscribes una vez y te enteras antes que tu equipo.

## Combina con

- [`/doctor`](/es/tips/claude-code-doctor-diagnostico) — herramienta de diagnóstico local.
- [Comando `/context`](/es/tips/claude-code-comando-context-uso-tokens) — ver dónde se va tu context window.
- [Cómo actualizar Claude Code](/es/tips/claude-code-actualizar-version) — una versión vieja a veces se comporta raro y el meme del "getting dumber" se confunde con eso.
- [Cheat sheet de slash commands](/es/tips/claude-code-slash-commands-cheatsheet) — incluye `/compact`, `/clear`, `/recap`, `/feedback`.

> Documentación oficial: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) · [Status page](https://status.claude.com/)
