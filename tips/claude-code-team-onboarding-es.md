---
date: 2026-06-20
type: tip
title_es: "/team-onboarding en Claude Code: tu setup convertido en guía (aunque no tengas equipo)"
title_en: "/team-onboarding in Claude Code: your setup turned into a guide (even with no team)"
---

> **TL;DR** `/team-onboarding` mira tus **sesiones, comandos y MCP de los últimos 30 días** y escribe una **guía en markdown** que un compañero pega como primer mensaje para ponerse al día en minutos. Con suscripción (Pro, Max, Team o Enterprise) además te da un **share link** para abrirla directa en Claude Code. El truco que casi nadie usa: lánzalo **estando solo**, para documentar tu entorno o preparárselo a tu yo del futuro en una máquina nueva.

Lo ves en la lista de comandos, piensas "esto es para equipos grandes" y pasas de largo. Error. `/team-onboarding` no necesita que tengas equipo: es la forma más rápida de convertir **cómo trabajas tú** en un documento que otra persona (o tu yo de dentro de seis meses) puede replicar.

## Qué hace

Analiza tu **historial de uso de los últimos 30 días** (sesiones, comandos y servidores MCP), lee tu `CLAUDE.md` y genera una **guía en markdown**: cómo se usa Claude en tu proyecto, un checklist de setup y huecos para tus propios tips. La guía está pensada para **pegarse como primer mensaje** de una sesión, de modo que Claude arranca ya sabiendo cómo trabajáis.

```
> /team-onboarding

⠋ Analizando 30 días de uso: sesiones, comandos y MCP…
✓ Guía escrita → team-onboarding.md

  Cómo usamos Claude · Checklist de setup · Tips del equipo
  Pégala como primer mensaje, o comparte el link.
```

## Cómo sacarle partido

**1. El uso obvio: un compañero nuevo.** Lo lanzas tú (que ya tienes el contexto), **editas** la guía para quitar ruido y dejar lo importante, y le pasas el archivo. Tu compañero lo pega como primer mensaje y Claude le acompaña desde ahí, con tu setup como punto de partida en vez de una página en blanco.

**2. El uso que casi nadie ve: tú solo.** No hace falta equipo:

- **Documenta tu entorno** sin escribir un README a mano: qué comandos y MCP usas de verdad, según tus últimos 30 días.
- **Onboarda a tu yo del futuro** cuando montes Claude Code en una máquina nueva.
- **Pásaselo a un colaborador puntual** o freelance para que trabaje como tú desde el minuto uno.

Aunque nunca compartas la guía, leerla es una **auditoría gratis** de cómo trabajas: ahí ves en qué te apoyas de verdad.

## El share link (solo suscripción)

Si entras con una cuenta de **claude.ai** (Pro, Max, Team o Enterprise), además del markdown te devuelve un **enlace** que tu compañero abre directamente en Claude Code, sin pasarse el archivo a mano. Con API key o credencial de cloud te quedas con el markdown, que es lo esencial.

## Referencia

| | Detalle |
|---|---|
| Qué analiza | Sesiones, comandos y MCP de los últimos **30 días** |
| Qué genera | Guía en **markdown** (pégala como primer mensaje) |
| Share link | Solo con suscripción claude.ai (Pro/Max/Team/Enterprise) |
| Uso en solitario | Documentar tu entorno o tu yo futuro en otra máquina |
| Recomendado | **Edítala** antes de pasarla: quita ruido, deja lo útil |

## Dónde encaja

- Es uno más de los [comandos que quizá no conocías](/es/tips/claude-code-slash-commands-cheatsheet); este escanea tu uso por ti.
- La guía complementa tu [`CLAUDE.md`](/es/tips/claude-code-claudemd-configurar-proyecto): el `CLAUDE.md` son las reglas; esto es **cómo las usas** en el día a día.

> Documentación oficial: [Commands](https://code.claude.com/docs/en/commands)

## Requisitos

- El **share link** requiere iniciar sesión con una suscripción de claude.ai (Pro, Max, Team o Enterprise). La guía en markdown se genera en cualquier caso.
