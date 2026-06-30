---
date: 2026-06-30
type: tip
title_es: "Sonnet 5 en Claude Code: casi Opus 4.8, a precio de Sonnet"
title_en: "Sonnet 5 in Claude Code: near-Opus quality, at Sonnet prices"
---

> **TL;DR** Sonnet 5 ya está en Claude Code. El alias `sonnet` ahora resuelve a él (la vía universal: `/model sonnet`), y es el **Default** en Pro, Team Standard y Enterprise por asiento. Trae **ventana nativa de 1M de tokens**, calidad *cercana a Opus 4.8* a precio bastante menor (intro $2/$10 por MTok hasta el 31 ago), y hace que `opusplan` (Opus planifica, Sonnet ejecuta) sea un gran combo calidad/precio. Necesitas **Claude Code v2.1.197+**: `claude update`.

Trabajando con Kimi 2.7 o con Composer 2.5 (que por debajo es Kimi), echas de menos una cosa frente a Opus: la velocidad. Se nota muchísimo. Pruebas Sonnet 4.6 y sí, es más rápido, pero pierde adherencia: en tareas que piden razonamiento, se queda corto.

Sonnet 5 parece la respuesta de Anthropic a ese hueco. Un modelo frontera que no intenta ser el más potente de su rango, sino el más equilibrado. Buena noticia para cuando no necesitas toda la adherencia, el poder (y el precio) de Opus 4.8, pero sigues queriendo agentic AI de calidad.

## Qué cambia en Claude Code

La doc oficial es clara: en la API de Anthropic, `sonnet` resuelve ahora a **Sonnet 5** y `opus` a Opus 4.8. Por eso la vía universal para usarlo es `/model sonnet`, sea cual sea tu plan.

Ojo con el Default, que no es lo que parece: **Sonnet 5 es el Default en Pro, Team Standard y Enterprise por asiento**. Pero en **Max, Team Premium, Enterprise pay-as-you-go y la propia API de Anthropic, el Default sigue siendo Opus 4.8**. Si vas en Max y no tocas nada, sigues en Opus, no en Sonnet 5.

Tres cosas que importan al programar:

- **1M de contexto nativo.** Sonnet 5 trae ventana de 1 millón de tokens de serie; el viejo truco `sonnet[1m]` ya es redundante.
- **`opusplan` sube de nivel.** Opus 4.8 para planificar, Sonnet 5 para ejecutar. Planificación de máxima calidad, ejecución rápida y económica.
- **Es el Sonnet más agéntico.** Según Anthropic, termina tareas complejas donde los Sonnet anteriores se paraban, y verifica su propio output sin pedírselo.

## Cómo confirmarlo o cambiar

### **1. Actualiza (si no, ni aparece)**

```bash
claude update
```

Sonnet 5 **requiere Claude Code v2.1.197 o posterior**. En versiones viejas no sale en el picker.

### **2. Comprueba o fija el modelo**

```bash
/model            # abre el picker y ves tu modelo actual
/model sonnet     # fija Sonnet 5 como default para nuevas sesiones
```

Desde la v2.1.153, `/model <alias>` guarda tu elección como default escribiendo el campo `model` en tus settings. Para el combo plan+ejecución:

```bash
/model opusplan   # Opus 4.8 planifica, Sonnet 5 implementa
```

### **3. Cuándo seguir en Opus 4.8**

Opus sigue siendo *"the model of choice for higher accuracy"*. Para refactors críticos, arquitectura delicada o cuando la adherencia importa más que la velocidad, `/model opus`. Para el día a día agéntico, Sonnet 5.

## Referencia

| Alias / ajuste | Resuelve a (suscripción) |
|---|---|
| `sonnet` | Sonnet 5 |
| `opus` | Opus 4.8 |
| `opusplan` | Opus 4.8 (plan) + Sonnet 5 (ejecución) |
| `default` en Pro / Team Standard / Enterprise (asiento) | Sonnet 5 |
| `default` en Max / Team Premium / Enterprise pay-as-you-go / API | Opus 4.8 |

| Precio Sonnet 5 (por MTok) | Input | Output |
|---|---|---|
| Intro (hasta 31 ago 2026) | $2 | $10 |
| Estándar | $3 | $15 |

> Nota: en Bedrock, Vertex y Foundry `sonnet` aún resuelve a Sonnet 4.5; allí selecciona el nombre completo o usa `ANTHROPIC_DEFAULT_SONNET_MODEL`.

> Documentación oficial: [Model configuration](https://code.claude.com/docs/en/model-config)

Para entender la precedencia de qué modelo manda (y por qué a veces se te resetea), mira [/model en Claude Code](/es/tips/claude-code-cambiar-modelo-default). Para decidir cuándo Sonnet y cuándo Opus, [cómo elegir el modelo adecuado](/es/tips/claude-code-elegir-modelo-adecuado). Y por encima de Opus, [Fable 5](/es/tips/claude-code-fable-5-por-encima-de-opus).

## Requisitos

- Claude Code **v2.1.197+** (`claude update`). El alias `sonnet` resuelve a Sonnet 5 en la API; es el `default` solo en Pro, Team Standard y Enterprise por asiento.
