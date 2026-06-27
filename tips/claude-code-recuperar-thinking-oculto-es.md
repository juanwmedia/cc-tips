---
date: 2026-06-26
type: tip
title_es: "Claude Code te oculta su thinking: cómo recuperarlo de verdad (y los trucos que no funcionan)"
title_en: "Claude Code hides its thinking now: what actually brings it back (and the fixes that don't)"
---

> **TL;DR** En Claude Code con suscripción, desde una actualización reciente el razonamiento viene **redactado** por defecto: el modelo piensa igual (y lo pagas), pero no lo ves. Para recuperarlo hacen falta dos cosas en `~/.claude/settings.json`: `"showThinkingSummaries": true` (lo des-redacta) y `"verbose": true` (lo muestra, o pulsa `Ctrl+O` por sesión). Probado en la v2.1.195. Los otros "trucos" que circulan no hacen esto.

Soy de los que mira el razonamiento del modelo. Me gusta ver pensar a un modelo frontera como Opus: dónde duda, qué descarta, por qué decide una cosa y no otra. Un día dejó de aparecer. Sin aviso, sin changelog claro, con la excusa de ganar velocidad. Si no lees la documentación y los issues de GitHub, ni te enteras de que lo apagaron.

Y hay mucha confusión alrededor. Mi lectura: Anthropic es opaco a propósito, porque la confusión le beneficia. Así que, para nuestra versión de Claude Code (la **2.1.195**), esta es la forma de traerlo de vuelta.

## Por qué no lo ves

Claude Code envía por defecto un header (`redact-thinking-2026-02-12`) que **redacta** los bloques de thinking en la terminal. El razonamiento ocurre y se factura igual, pero no llega a tu pantalla. Recuperarlo son dos palancas distintas, y ahí está el error de casi todos: tocan una sola.

- **Des-redactar:** que el servidor te devuelva el razonamiento.
- **Mostrar:** que la terminal lo enseñe en vez de colapsarlo.

Resultado, una vez activado:

```
> Hey Claude, how are you doing?

∴ The user is just saying hello, so I'll respond warmly
  and offer to help with whatever they need.
```

El razonamiento, en gris, antes de la respuesta.

## Cómo recuperarlo

### **1. Des-redacta con `showThinkingSummaries`**

En `~/.claude/settings.json`:

```json
{ "showThinkingSummaries": true }
```

Sin esto, en suscripción el bloque de thinking llega **vacío**. Es la pieza que casi nadie configura, y la que de verdad trae el razonamiento.

### **2. Muéstralo con `verbose` (o `Ctrl+O`)**

```json
{ "verbose": true }
```

`verbose: true` lo deja siempre expandido. Si lo prefieres por sesión, pulsa `Ctrl+O`. Pero `verbose` solo, sin el paso 1, no enseña nada: expande una caja vacía.

### **3. Lo que probamos (no es de oídas)**

| `verbose` | `showThinkingSummaries` | ¿Se ve el razonamiento? |
|---|---|---|
| `false` | `false` | No (redactado por defecto) |
| `true` | `false` | **No** (verbose solo no basta) |
| `true` | `true` | **Sí** |

Lo que probamos a mano: `showThinkingSummaries` es **imprescindible** (sin él no sale nada). Y según la documentación, `verbose`/`Ctrl+O` es el interruptor que lo muestra. La receta segura es poner los dos.

## Lo que NO funciona (aunque lo leas por ahí)

| Lo que se dice | La realidad |
|---|---|
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` lo recupera | Controla el *presupuesto* de razonamiento, no si se muestra. Y no tiene efecto en Opus 4.7+ |
| `/effort high` lo recupera | Sube la *profundidad* del razonamiento, no el display |
| `think` / `think hard` en el prompt | Ya no son keywords; solo `ultrathink` se reconoce, y también es profundidad, no display |

## Ojo: esto es una foto de hoy

Esto cambia rápido. La redacción llegó con el header `redact-thinking-2026-02-12`, el setting está apenas documentado, y hay [issues reportando](https://github.com/anthropics/claude-code/issues/52376) que en suscripción no funcionaba. En la **2.1.195** (la nuestra), con la combinación de arriba, funciona. Si actualizas y deja de funcionar, vuelve a la documentación y a los issues.

Cuando lo tengas visible, leerlo en directo da para mucho: [el modo verbose te convierte en revisor en tiempo real](/es/tips/claude-code-verbose-output-ver-razonamiento), capaz de cortar una alucinación antes de que se convierta en código.

> Documentación oficial: [Model configuration — extended thinking](https://code.claude.com/docs/en/model-config)

## Requisitos

- Claude Code v2.1.x (probado en la 2.1.195), plan con suscripción (Pro/Max).
- Te cobran los tokens de thinking aunque estén redactados, así que no ahorras ocultándolo.
