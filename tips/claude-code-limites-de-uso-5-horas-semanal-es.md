---
date: 2026-06-19
type: tip
title_es: "Límites de uso en Claude Code, sin mitos: la franja de 5 horas y el tope semanal"
title_en: "Claude Code usage limits, demystified: the 5-hour window and the weekly cap"
---

> **TL;DR** No es un límite, son tres barras a la vez. La **franja de 5 horas** arranca con tu primer mensaje y se renueva 5 horas después (ventana móvil). Por encima corren **dos límites semanales**: uno para **todos los modelos** y otro **solo para Sonnet**, ambos con reset a una hora **fija** asignada a tu cuenta. Lo que lo vacía más rápido: el modelo (Opus pesa mucho más que Sonnet), el effort y las sesiones largas. Mira tus barras en `/usage` (`d`/`w` para 24 h / 7 días). Cualquiera de las tres te corta hasta que resetee.

Llevo muchísimas horas al día con Claude Code y, con sinceridad, nunca entendí del todo por qué a veces me cortaba a media tarde. La culpa es que no es un contador, son **varios relojes corriendo a la vez** con reglas distintas. Una vez los separas, deja de parecer aleatorio.

```
> /usage

Current session       ████░░░░░░  18% · resetea 3:50pm
Current week (all)    █░░░░░░░░░   3% · resetea Jun 25, 8pm
Current week (Sonnet) ░░░░░░░░░░   0%
```

## Los relojes

**1. La franja de 5 horas (la "sesión")**

Es una **ventana móvil**: empieza a contar con tu **primer mensaje** y se renueva 5 horas después de ese arranque. No es de reloj de pared (no es "a las 0:00"), es "5 horas desde que empezaste". `/usage` te muestra cuánto llevas gastado y a qué hora resetea la sesión actual. Es el tope que más gente toca en un día intenso.

**2. Los límites semanales (son dos)**

Por encima de la franja corren **dos** topes semanales, y aquí está la diferencia clave: **resetean a una hora fija asignada a tu cuenta**, no es móvil. Te enseña hasta la fecha del próximo reset (p. ej. *Resets Jun 25 at 8pm*). Tu día y hora no cambian hagas lo que hagas, y cada ciclo recibes la cuota entera.

Las dos barras son **`Current week (all models)`** y **`Current week (Sonnet only)`**: una cuenta todo tu uso y la otra solo el de Sonnet. Así aparece en un plan Max; mira tus propias barras para tu plan.

> Excepción: en un asiento **Enterprise** el pool resetea en ventana móvil, no a hora fija. Lo de arriba es para Pro y Max.

## Qué lo vacía más rápido

No todos los turnos cuestan igual. Pesa más:

- **El modelo.** Opus consume mucho más que Sonnet por el mismo trabajo. [Elegir bien el modelo](/es/tips/claude-code-cambiar-modelo-default) es la palanca número uno.
- **Las sesiones largas.** El propio `/usage` te avisa: por encima de ~150k de contexto cada turno cuesta más **aunque haya caché**. `/compact` entre tareas y `/clear` al cambiar de tema.
- **Romper la caché.** Un fallo de caché reprocesa todo el prefijo a precio completo: cambiar de modelo a mitad de tarea te puede costar 10× ese turno. Lo explico en [prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo).
- El **effort level**, los **adjuntos** y las herramientas (web search) también suman. Para gastar menos, los [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos).

## El matiz que descuadra los números

Tu plan es **un solo pool compartido**: lo que gastas en claude.ai, en la app de escritorio y en Claude Code va al mismo sitio. Pero el `/usage` del CLI **se calcula en local**, y lo avisa él mismo: *"based on local sessions on this machine, does not include other devices or claude.ai"*. Por eso a veces "te corta" antes de lo que parece por el `/usage`: el contador real del servidor va por delante del que ves en la terminal.

## Referencia

| | Franja de 5 horas | Límites semanales |
|---|---|---|
| Tipo | Ventana móvil | Reset a hora fija asignada |
| Empieza | Con tu primer mensaje | Día/hora fijos de tu cuenta |
| Cuántos | Uno | Dos: todos los modelos + Sonnet only |
| Dónde se ve | `/usage` · Settings > Usage | `/usage` (`w`) · Settings > Usage |

## Dónde encaja

- Para ver tus barras y el desglose por skill, subagente, plugin y MCP: [`/usage` y `/stats`](/es/tips/claude-code-uso-tokens-usage-stats).
- Por qué un turno se dispara de golpe: [prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo).
- Cómo gastar menos: [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos).

> Documentación oficial: [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices) · [Models, usage, and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)

## Requisitos

- Las barras de plan en `/usage` (sesión + semanales) requieren un plan de suscripción (Pro, Max, Team o Enterprise). Los números exactos los suben de vez en cuando, así que mira siempre los tuyos.
