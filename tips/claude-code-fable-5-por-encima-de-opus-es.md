---
date: 2026-06-09
type: tip
title_es: "Fable 5 en Claude Code: el modelo nuevo que está por encima de Opus"
title_en: "Fable 5 in Claude Code: the new model that sits above Opus"
---

> **TL;DR** Fable 5 es el nuevo techo de Claude Code, por encima de Opus: para tus tareas más largas y difíciles. Lo activas con `/model fable` (necesitas v2.1.170 o superior). Consume tus límites ~2× más rápido que Opus, así que no es para todo. Y trae un clasificador de seguridad que puede reenrutarte a Opus solo, a veces ya en el primer mensaje.

El picker de modelos acaba de pasar de cuatro opciones a cinco. Fable 5 se sienta por encima de Opus 4.8 como el modelo más capaz: pensado para tareas que no caben en una sola sentada. Investiga antes de actuar y verifica su propio trabajo más que los modelos pequeños. No es el modelo por defecto: tu cuenta sigue arrancando en Opus 4.8 (o Sonnet, según tu plan), y a Fable entras a propósito.

Resultado:

```
Select model

  1. Default (recommended)   Opus 4.8 with 1M context
> 2. Fable 5                 Most capable for your hardest and longest-running tasks
                             Uses your limits ~2× faster than Opus
  3. Sonnet                  Sonnet 4.6 · Efficient for routine tasks
  4. Haiku                   Haiku 4.5 · Fastest for quick answers
  5. Opus 4.8 ✓              Best for everyday, complex tasks (claude-opus-4-8)

Enter to set as default · s to use this session only
```

## **1. Cómo entrar**

`/model fable`, o elige la opción 2 en el picker (`/model` sin argumentos). En el picker, `Enter` lo deja como tu default para nuevas sesiones y `s` lo usa solo en esta. El alias `best` apunta a Fable 5 donde tu cuenta lo tenga.

## **2. El requisito (acaba de salir)**

Fable 5 necesita Claude Code **v2.1.170 o superior**. Si tu picker no lo muestra, `claude update`. No está disponible bajo zero data retention: ahí el picker lo oculta o lo deshabilita.

## **3. Cuándo merece la pena**

La doc es explícita sobre cómo sacarle partido, y casi todo va contra tus reflejos con modelos pequeños:

- **Describe el resultado, no los pasos.** Dale el objetivo y deja que planifique el camino. Combínalo con [`/goal`](/es/tips/claude-code-goal-condicion-parada) para que siga hasta cumplirlo.
- **Dale problemas ambiguos:** root-cause, debugging de caídas, decisiones de arquitectura. Ahí es donde su investigación extra paga.
- **Deja de recordarle que teste:** se autoverifica con menos prompting, así que los "acuérdate de probarlo" sobran.
- **Súbele tareas grandes:** trabajo que normalmente partirías en trozos. Aguanta sesiones largas sin perder el hilo.

Effort `high` por defecto, hasta `max`. En Fable 5 el thinking no se puede apagar: siempre razona de forma adaptativa.

## **4. El reenrutado automático que nadie te cuenta**

Esto es lo más práctico y casi nadie lo verá venir. Fable 5 corre con clasificadores de seguridad en **ciberseguridad y biología**. Cuando uno marca tu petición, Claude Code la **reejecuta en Opus** (4.8 en la API de Anthropic) con un aviso, y la sesión continúa en Opus. Para volver: `/model fable`.

Lo sorprendente: puede saltar en el **primer mensaje**, antes de que escribas nada raro, porque esa primera petición arrastra tu `CLAUDE.md` y el git status del repo. Un repositorio con material de seguridad o biología puede dispararlo solo con ese contexto.

- Para ver si el culpable son tus customizaciones, arranca con `claude --safe-mode`: desactiva CLAUDE.md, skills, MCP y hooks. El git status y los nombres de directorio siguen contando.
- Para decidir tú cada vez en lugar de que cambie solo, ve a `/config` y apaga "switch models when a message is flagged".

Si trabajas en pentesting, CTF o código cercano a biología, cuenta con que lo dispare a menudo.

## Fable 5 de un vistazo

| | |
|---|---|
| Cómo entrar | `/model fable` · picker opción 2 · alias `best` |
| Default | No (sigues en Opus 4.8 o Sonnet) |
| Versión mínima | Claude Code v2.1.170 |
| Límites | los consume ~2× más rápido que Opus |
| Effort | `high` por defecto, hasta `max` · thinking siempre activo |
| Contexto | 1M de tokens en la API de Anthropic |
| Fallback de seguridad | ciberseguridad y biología → Opus, con aviso |

## Dónde encaja

Fable 5 es el escalón nuevo por encima de [Opus 4.7](/es/tips/claude-code-opus-4-7) y Opus 4.8. Si dudas qué usar para qué, [la guía de elegir modelo](/es/tips/claude-code-elegir-modelo-adecuado) sigue aplicando: Fable para lo más difícil y largo, Opus para el día a día, Sonnet para lo rutinario, Haiku para lo rápido.

> Documentación oficial: [Model configuration](https://code.claude.com/docs/en/model-config) | [Anuncio de Claude Fable 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)

## Requisitos

Claude Code v2.1.170 o superior (`claude update`). No disponible bajo zero data retention.
