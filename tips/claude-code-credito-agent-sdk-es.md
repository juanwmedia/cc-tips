---
date: 2026-06-10
type: tip
title_es: "El crédito aparte del Agent SDK no llega (de momento): tu claude -p sigue saliendo de tu suscripción"
title_en: "The separate Agent SDK credit isn't happening (yet): your claude -p still runs on your subscription"
---

> **TL;DR · Actualización 16 jun 2026:** Anthropic ha dado marcha atrás. El cambio que iba a mover `claude -p`, el Agent SDK, GitHub Actions y las apps de terceros a un crédito mensual propio **no entra en vigor**. Todo sigue saliendo de los límites de tu suscripción igual que antes, y **no hay ningún crédito que reclamar**. Anthropic dice que está rehaciendo el plan y avisará con antelación antes de aplicar nada.

En mayo, Anthropic anunció que desde el 15 de junio de 2026 el uso programático (`claude -p`, el Agent SDK, GitHub Actions y las apps de terceros) dejaría de tirar de los límites de tu suscripción y pasaría a un crédito mensual propio. Medio internet, este tip incluido, te dijo que te prepararas. No va a pasar, al menos por ahora: el mismo día en que iba a entrar, Anthropic mandó un correo cancelándolo.

## Qué dice Anthropic ahora

Del aviso a los usuarios, sin paráfrasis:

> "No vamos a hacer este cambio hoy. Estamos trabajando para actualizar el plan y dar mejor soporte a cómo construye la gente con las suscripciones de Claude. No cambia nada por ahora. El Agent SDK, `claude -p` y el uso de apps de terceros siguen funcionando con tu suscripción exactamente igual que antes, y **no hay ningún crédito que reclamar**. Tus límites de suscripción no cambian. Cuando tengamos una actualización, la compartiremos con antelación antes de que entre en vigor."

Traducción práctica: si montaste prisas para reclamar un crédito o reorganizar tus crons antes del día 15, puedes deshacerlas. No hay nada que hacer.

## Qué se llegó a anunciar (y hoy no aplica)

Para dejar el registro de lo que estuvo sobre la mesa, y que podría volver reformulado:

- Una **bolsa mensual de Agent SDK aparte**, separada de tus límites interactivos, para `claude -p`, el SDK, CI/cron, GitHub Actions y apps de terceros.
- Un importe en dólares por plan: **$20** (Pro), **$100** (Max 5x), **$200** (Max 20x), con variantes en Team y Enterprise.
- Gasto a tarifas API estándar, **sin rollover**, y un **opt-in** de una sola vez para activarlo.

Nada de esto está vigente. Tu uso programático sigue contando contra los límites de tu suscripción, como siempre.

## Por qué no es una sorpresa

Es la segunda vez en 2026 que Anthropic anuncia un cambio de facturación sobre el uso programático y lo revierte tras el revuelo. En enero bloqueó los tokens OAuth de suscripción para herramientas de terceros y dio marcha atrás en días. El patrón se repite: anuncio, reacción de la comunidad, vuelta atrás.

La lectura útil: cuando llegue el próximo "tu crédito de Agent SDK cambia el día X", **no corras**. Anthropic se ha comprometido a avisar con antelación, y esta vez ese plazo se quedó en nada.

## Lo que sí puedes controlar mientras tanto

El reparto del gasto no ha cambiado, pero las herramientas para no vaciar tu cuota desatendido siguen ahí:

- Pon topes por llamada con `--max-turns` y `--max-budget-usd` en tus `claude -p`.
- Vigila tu consumo real con `/usage` y `/stats`.
- Si llamas al SDK desde tu propio código, de momento cuenta igual que el resto de tu uso de suscripción.

> Documentación oficial: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) · [Manage costs](https://code.claude.com/docs/en/costs) · [Use the Agent SDK with your plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)

## Requisitos

Nada que hacer. Si reclamaste algo o reorganizaste crons esperando el cambio, puedes revertirlo: tus límites de suscripción están intactos.
