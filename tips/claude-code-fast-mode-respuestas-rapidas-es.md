---
date: 2026-02-21
type: tip
title_es: "Acelera las Respuestas de Claude Code con Fast Mode"
title_en: "Speed Up Claude Code Responses with Fast Mode"
---
# Quick Tip: Acelera las Respuestas de Claude Code con Fast Mode

Fast mode es una configuración de Opus 4.6 que prioriza la velocidad de generación de tokens sobre el coste. No es un modelo distinto ni una versión con menos capacidad de razonamiento -- es el mismo Opus 4.6 con la misma inteligencia, solo que con respuestas hasta 2.5x más rápidas. La contrapartida: un coste por token significativamente mayor.

Es importante no confundir fast mode con el ajuste de effort level. Bajar el effort level sí reduce la calidad de razonamiento a cambio de velocidad. Fast mode no sacrifica nada en calidad -- solo en coste.

Resultado:

```
> /fast

Fast mode ON · $15/$75 per Mtok (50% off through Feb 16)
```

## Setup

**1. Activa fast mode**

Escribe `/fast` en cualquier momento de tu sesión:

```bash
/fast
```

Un icono `↯` aparece junto al prompt mientras fast mode esté activo.

**2. Desactiva cuando no lo necesites**

```bash
/fast
```

El mismo comando lo desactiva. Al desactivarlo, sigues en Opus 4.6 (no vuelve al modelo anterior).

**3. Activa por defecto (opcional)**

Para tenerlo siempre activo, añade a tu configuración de usuario:

```json
{
  "fastMode": true
}
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/fast` (toggle on/off) |
| Modelo | Opus 4.6 (el mismo, sin cambios en calidad) |
| Velocidad | Hasta 2.5x más rápido en output tokens |
| Coste (< 200K) | $30 / $150 por MTok (input / output) |
| Coste (> 200K) | $60 / $225 por MTok (input / output) |
| Descuento | 50% hasta el 16 de febrero de 2026 |
| Rate limits | Separados de Opus estándar; al agotarse, cae a velocidad normal |
| Persistencia | Se mantiene entre sesiones |
| Disponibilidad | Planes Pro/Max/Team/Enterprise con extra usage habilitado |

## Cuando usarlo

- **Iteración rápida**: cambios de código donde esperar 30 segundos importa.
- **Debugging en vivo**: sesiones interactivas donde cada segundo cuenta.
- **Trabajo con deadline**: cuando la velocidad justifica el coste extra.

Para tareas autónomas largas, batch processing o CI/CD, el modo estándar es más eficiente en coste.

> **Nota personal:** Fast mode acaba de lanzarse a fecha de publicación de este tip. En las tareas medianas con las que he podido probarlo, la diferencia de velocidad se nota, pero no tengo claro todavía si justifica pagar el doble (2x) respecto a Opus estándar. Durante el periodo de descuento del 50% (hasta el 16 de febrero de 2026), fast mode cuesta lo mismo que el modo estándar -- ahí no hay debate.

> Documentación oficial: [Speed up responses with fast mode](https://code.claude.com/docs/en/fast-mode)
