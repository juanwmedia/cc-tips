---
date: 2026-05-01
type: tip
title_es: "¿Claude Code gratis? La trampa del 'plan free' y las 2 vías reales"
title_en: "Claude Code free? The 'free plan' trap and 2 real paths"
---

Si has buscado "Claude Code gratis" en Google y has aterrizado en un post que promete un "plan free", ese post está mal. La página oficial de pricing de Anthropic es taxativa: **el plan Free NO incluye Claude Code**. El entry point real es Pro a $17 al mes (anual).

Pero sí hay dos formas legítimas de usar Claude Code sin pagar — una es un crédito pequeño para empezar, la otra vale 1.200 dólares. Y la segunda esconde una puerta que casi nadie ve.

## La trampa: claude.ai Free ≠ Claude Code

Sacado directamente de [claude.com/pricing](https://claude.com/pricing):

| Plan | Precio | Claude Code |
|---|---|---|
| Free | $0/mes | ❌ No incluido |
| Pro | $17/mes (anual) o $20/mes | ✅ Incluido |
| Max 5x | $100/mes | ✅ Incluido |
| Max 20x | $200/mes | ✅ Incluido |

El Free te da Claude chat en el navegador (Sonnet 4.6, uso limitado al día). **No** te da el comando `claude` en terminal. Cualquier post que diga lo contrario está desactualizado o equivocado.

## Vía 1 — API de Anthropic con tu propia clave

Crea una cuenta en [console.anthropic.com](https://console.anthropic.com), genera una API key, y conéctala a Claude Code:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
claude
```

La factura es **pay-as-you-go** — pagas exactamente los tokens que consumes, sin suscripción mensual. Es la entrada más barata para uso esporádico de Claude Code completo (todos los modelos disponibles).

¿Y los créditos gratis que mencionan algunos blogs? Anthropic ha dado históricamente un crédito pequeño de bienvenida al verificar tu teléfono al registrarte. **La documentación oficial de Anthropic no lo menciona explícitamente**, así que verifica el importe actual en console.anthropic.com al crear la cuenta — puede haber cambiado o desactivado. Si está activo, te da unas horas para probar antes de empezar a pagar.

## Vía 2 — Claude for Open Source (1.200 USD de valor, 6 meses)

Anthropic lanzó [Claude for Open Source](https://claude.com/contact-sales/claude-for-oss) a principios de 2026: **6 meses de Claude Max 20x — el plan de $200/mes — a coste cero** para mantenedores que cualifican. Son 1.200 USD de valor con acceso completo al tier Max 20x (Claude Code incluido).

Elegibilidad estándar:

- Mantenedor principal o miembro del core team de un repo público con **5.000+ stars en GitHub** o **1M+ descargas mensuales en NPM**
- Activo en los últimos 3 meses (commits, releases o reviews de PR)

La puerta escondida, sacada literal de la página del programa: *"Si mantienes algo de lo que el ecosistema depende silenciosamente, aplica igualmente y cuéntanoslo"*. Traducción: una librería de infraestructura crítica que vuele por debajo del radar de stars puede entrar también.

Aceptan hasta 10.000 contribuidores. Aplicaciones en rolling.

## Referencia

| Vía | Coste | ¿Claude Code? | Cuándo elegirla |
|---|---|---|---|
| **claude.ai Free** | $0 | ❌ No (la trampa) | Si quieres Claude Code, esta no |
| **API + tu propia clave** | Pay-as-you-go (crédito de bienvenida si activo) | ✅ Sí, todos los modelos | Probar Claude Code o uso esporádico |
| **Claude for Open Source** | $0 durante 6 meses | ✅ Sí (Max 20x) | Mantienes un repo OSS sustancial |
| **Pro (de pago)** | $17-20/mes | ✅ Sí | Uso personal normal |

## Qué hacer hoy

Si no cualificas para el programa OSS, el camino legítimo más barato es Pro a $17/mes en anual. Dos tips complementarios para que rinda más: [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos) y [seguir tu consumo con /stats](/es/tips/claude-code-uso-tokens-usage-stats).

> Fuente oficial de precios: [claude.com/pricing](https://claude.com/pricing)
> Programa OSS: [claude.com/contact-sales/claude-for-oss](https://claude.com/contact-sales/claude-for-oss)

