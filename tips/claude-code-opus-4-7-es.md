---
date: 2026-04-16
type: tip
title_es: "Opus 4.7 ha llegado a Claude Code: deja de supervisar, empieza a delegar"
title_en: "Opus 4.7 Is in Claude Code: Stop Supervising, Start Delegating"
---
> **TL;DR** Opus 4.7 aterrizó esta mañana (16 de abril de 2026) en Claude Code y cambia el juego: esfuerzo `xhigh` por defecto, 1M de tokens de contexto, razonamiento adaptativo y nuevo comando `/ultrareview`. Si estás en Max ya es tu default; si estás en Pro tienes que pasarte tú con `/model opus`. Es el primer modelo al que de verdad puedes dejarle una tarea de horas sin volver cada diez minutos a corregirlo.

## Cómo funciona

Opus 4.7 sustituye a Opus 4.6 como el modelo más capaz de Anthropic. En Claude Code introduce tres cambios visibles desde el primer prompt: nivel de [esfuerzo](/es/tips/claude-code-effort-level-ajustar-razonamiento) `xhigh` por defecto (un escalón nuevo entre `high` y `max`), razonamiento adaptativo (el modelo decide cuánto pensar por sí solo) y contexto de 1M de tokens incluido sin configurar nada si estás en Max, Team o Enterprise.

El salto agente es lo que importa: Anthropic reporta 3× más tareas resueltas en SWE-bench Verified frente a Opus 4.6, 70 % en CursorBench (vs 58 %), y un tercio menos de errores de tool en benchmarks de Notion Agent. En visión, 98,5 % vs 54,5 % — no es una mejora, es otro modelo.

También reporta mejor memoria entre sesiones: si arrancas una tarea larga, cierras la sesión y vuelves mañana, retoma donde lo dejaste sin que tengas que reexplicarle nada. Complementa [la memoria automática que Claude Code ya tenía entre conversaciones](/es/tips/claude-code-memoria-automatica-entre-sesiones) llevándola a tareas de varias horas.

## Qué vas a ver al iniciar sesión

```bash
$ claude --version
2.1.111

$ /model
> opus   ─ Claude Opus 4.7 (xhigh)
  sonnet ─ Claude Sonnet 4.6 (high)
  haiku  ─ Claude Haiku 4.5

✔ opus selected. Effort: xhigh
```

## Cómo empezar a usarlo

**1. Actualiza a 2.1.111 o superior**. Opus 4.7 no aparece en versiones anteriores:

```bash
claude update
claude --version   # debe mostrar 2.1.111+
```

**2. Selecciona el modelo**. Si estás en Max o Team Premium, Opus 4.7 ya es tu default. En Pro, API y Enterprise sigue siendo Sonnet 4.6 hasta el 23 de abril de 2026 — hasta entonces, cámbialo tú:

```bash
/model opus
```

**3. Deja el esfuerzo en `xhigh`**. Es el nuevo default en Opus 4.7 para todos los planes y es el que Anthropic recomienda para [tareas de código agente](/es/tips/claude-code-modo-headless-agente-autonomo). Solo baja a `high` si quieres más velocidad y menos tokens; sube a `max` únicamente para problemas puntuales donde la profundidad de razonamiento compense (cuidado: `max` es propenso a sobre-pensar).

**4. Aprovecha el 1M de contexto**. En Max, Team o Enterprise, el [millón de tokens](/es/tips/claude-code-1m-tokens-ventana-contexto) viene activado sin hacer nada. Para forzarlo explícitamente:

```bash
/model opus[1m]
```

**5. Revisa antes de merge con [`/ultrareview`](/es/tips/claude-code-ultrareview)**. El comando nuevo que corre una flota de agentes revisores en la nube para verificar bugs reales — no sugerencias de estilo. Tres pases gratis si estás en Pro o Max. Y si quieres delegación completa sin confirmar cada paso, combínalo con [los modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab) en `acceptEdits` o `auto`.

## Referencia

| Campo | Valor |
|---|---|
| Model ID | `claude-opus-4-7` |
| Alias en Claude Code | `opus` |
| Versión mínima de Claude Code | 2.1.111 |
| Contexto | 1M tokens |
| Output máximo | 128k tokens |
| Precio | 5 $/MTok input · 25 $/MTok output |
| Thinking | Adaptativo (no Extended) |
| Esfuerzo por defecto | `xhigh` |
| Niveles de esfuerzo | `low`, `medium`, `high`, `xhigh`, `max` |
| Training cutoff | Enero 2026 |
| Default en | Max, Team Premium |

## Cuándo sigue teniendo sentido Sonnet

Opus 4.7 no es siempre la respuesta. Sonnet 4.6 hace el 80 % del trabajo diario más barato y más rápido — y el [modelo adecuado](/es/tips/claude-code-elegir-modelo-adecuado) depende de la tarea. Reserva Opus 4.7 para: debugging profundo, refactors grandes, sesiones largas con mucho contexto, y cualquier cosa que antes te obligase a abrir y corregir cada 15 minutos. Para CRUD y boilerplate, sigue Sonnet.

> Docs oficiales: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) · [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) · [Model configuration](https://code.claude.com/docs/en/model-config)
