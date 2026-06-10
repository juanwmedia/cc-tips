---
date: 2026-06-10
type: tip
title_es: "claude -p deja de comerse tus límites en Claude Code: por fin tiene crédito propio"
title_en: "Your claude -p scripts stop eating your Claude Code limits: they finally get their own credit"
---

> **TL;DR** Desde el **15 de junio de 2026**, lo que gastan `claude -p` y el Agent SDK en planes de suscripción sale de un **crédito mensual de Agent SDK aparte**, no de tus límites interactivos. Tu cron, tu CI y tus scripts dejan de comerse la cuota que necesitas para programar en vivo. Pero es un opt-in: hay que **reclamarlo una vez** desde tu cuenta. Vence cada mes y no se acumula.

Montas una automatización con `claude -p`, la dejas en un cron o en CI, y se pasa la noche gastando. Hasta ahora todo salía de la misma bolsa: te sentabas a programar de verdad y te encontrabas el límite agotado por un script que corrió de madrugada. Ese reparto cambia el 15 de junio.

## Qué cambia el 15 de junio

A partir de esa fecha, el uso programático y el interactivo dejan de competir. Son dos bolsas:

```
ANTES                          DESDE EL 15 DE JUNIO

una sola bolsa de uso          bolsa interactiva      crédito Agent SDK
programar + claude -p          terminal, IDE,         claude -p, SDK,
compiten por el límite         web, móvil             CI, cron, scripts
                               (tus límites de        (bolsa propia
                                siempre, intacta)      en dólares)
```

La doc lo repite igual en varias páginas: *"crédito mensual de Agent SDK, separado de tus límites interactivos"*.

## Cuánto crédito te da tu plan

El crédito es una cantidad en dólares, distinta según el plan:

| Plan | Crédito mensual de Agent SDK |
|---|---|
| Pro | **$20** |
| Max 5x | **$100** |
| Max 20x | **$200** |
| Team (Standard) | **$20** |
| Team (Premium) | **$100** |
| Enterprise | de **$20 a $200** según estructura |

Se gasta a tarifas API estándar, así que un CI que corre en cada PR o un `/loop` desatado lo vacían en días, no en semanas. Pon tope de acciones y de gasto con [`--max-turns` y `--max-budget-usd`](/es/tips/claude-code-modo-headless-agente-autonomo) en cada llamada.

## Qué cubre y qué no toca

**Sale del crédito de Agent SDK:**

- `claude -p` (modo headless): scripts, cron, hooks de build.
- El Agent SDK en tus proyectos (Python o TypeScript).
- GitHub Actions (la action de `@claude` que revisa PRs corre sobre el SDK).
- Apps de terceros autenticadas vía Agent SDK.

**Sigue en tus límites de siempre (no cambia nada):**

- Claude Code interactivo en la terminal o el IDE.
- Las conversaciones en web, escritorio y móvil.
- Claude Cowork.

## Tienes que reclamarlo (y vence cada mes)

Es un **opt-in de una sola vez**: reclamas el crédito desde tu cuenta de Claude y queda activo. No se enciende solo, así que si no lo reclamas tu uso programático sigue como hasta ahora. El crédito **no se acumula** de un mes a otro: lo que no gastes se pierde y el siguiente mes empiezas de cero. Y es **por cuenta individual**: en un equipo no se comparte ni se agrupa entre compañeros.

## Qué pasa cuando se agota

Depende de un ajuste tuyo:

- **Con *usage credits* activados:** el uso extra del Agent SDK continúa a tarifas API estándar. Ponle un tope mensual con `/usage-credits` para que no se dispare.
- **Sin *usage credits*:** las peticiones del Agent SDK **se paran** hasta que el crédito se renueve el mes siguiente.

Es decir, por defecto tu automatización se detiene en seco, no te genera una factura sorpresa. Es justo la red que faltaba para dejar `claude -p` corriendo sin vigilarlo.

## Dónde encaja

Esto es el modelo de cobro, no cómo se usa. Las piezas que lo rodean:

- Ya sabes [cómo ejecutar `claude -p`](/es/tips/claude-code-modo-headless-agente-autonomo): cron, `--allowedTools`, topes de gasto. Esto es de qué bolsa sale ahora.
- El [Agent SDK desde tu código](/es/tips/claude-agent-sdk-claude-code-desde-tu-codigo) consume de este mismo crédito.
- Tu lado interactivo no cambia: contrólalo con [`/usage` y `/stats`](/es/tips/claude-code-uso-tokens-usage-stats).
- En el [mapa de las cuatro formas de mandar Claude a background](/es/tips/claude-code-background-agents-mapa), el crédito solo afecta al cuadrante headless/SDK; Agent View, `/loop` y Routines siguen saliendo de tu plan.

> Documentación oficial: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) · [Manage costs](https://code.claude.com/docs/en/costs) · [Use the Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

## Requisitos

Plan de suscripción (Pro, Max, Team o Enterprise). El cambio entra el **15 de junio de 2026**; el crédito hay que reclamarlo una vez desde tu cuenta de Claude.
