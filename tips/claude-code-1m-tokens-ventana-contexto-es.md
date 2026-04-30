---
date: 2026-03-16
type: tip
title_es: "Claude Code ahora tiene 1M de tokens de contexto — y no deberías llenarlos"
title_en: "Claude Code Now Has 1M Tokens of Context — and You Shouldn't Fill Them"
---
# Quick Tip: Claude Code ahora tiene 1M de tokens de contexto — y no deberías llenarlos

> **TL;DR** Opus 4.6 incluye 1 millón de tokens de contexto por defecto en planes Max, Team y Enterprise — 5 veces más que antes, sin coste adicional. Pero más contexto no significa mejor resultado. Monitoriza con [`/context`](/es/tips/claude-code-comando-context-uso-tokens), compacta proactivamente, y no dejes que la sesión se degrade.

Desde la versión 2.1.75, Claude Code usa [Opus 4.6](/es/tips/claude-code-elegir-modelo-adecuado) con 1M de tokens como modelo por defecto. La ventana de contexto ha pasado de 200K a 1M — 5 veces más espacio antes de que Claude necesite compactar. Esto significa sesiones más largas, menos interrupciones, y capacidad para trabajar con monorepos completos sin fragmentar el contexto.

Pero hay una trampa: el rendimiento del modelo se degrada con tokens lejanos. Es lo que se conoce como context drift — cuanto más lejos está la información del punto actual de la conversación, menos preciso es el modelo al recuperarla. Que puedas llenar 1M de tokens no significa que debas hacerlo.

## Quién tiene acceso

| Plan | Opus 4.6 1M | Sonnet 4.6 1M |
|---|---|---|
| Max, Team, Enterprise | Incluido | Requiere extra usage |
| Pro | Requiere extra usage | Requiere extra usage |
| API (pay-as-you-go) | Acceso completo | Acceso completo |

No hay surcharge — el precio por token es el mismo en toda la ventana. En planes donde está incluido, no consume créditos adicionales.

Pro aún no lo tiene de serie, pero la tendencia de Anthropic con features premium es clara: primero Enterprise/Max, luego baja.

## Cómo aprovecharlo sin desperdiciar contexto

### **1. Monitoriza con [/context](/es/tips/claude-code-comando-context-uso-tokens)**

Usa el comando `/context` para ver cuánto contexto estás consumiendo en tiempo real. No esperes a que Claude compacte automáticamente — anticípate.

### **2. Compacta antes de que lo haga Claude**

La auto-compactación se dispara al ~95% de capacidad. A ese punto ya has perdido precisión en tokens antiguos. Compacta proactivamente:

```
/compact enfócate en el módulo de autenticación
```

Las instrucciones opcionales le dicen a Claude qué priorizar al resumir.

### **3. No cargues contexto que no necesitas**

Que tengas 1M no significa que debas meter todo el codebase. Carga selectivamente — directorios específicos, archivos relevantes. Claude [lee bajo demanda](/es/tips/claude-code-cuando-se-cargan-features-contexto); no necesitas pre-cargar todo.

### **4. Seleccionar el modelo 1M explícitamente**

Si no lo ves activo, selecciónalo manualmente:

```
/model opus[1m]
/model sonnet[1m]
```

O al lanzar Claude Code:

```bash
claude --model opus[1m]
```

### **5. Controlar cuándo compacta**

Si quieres que compacte antes del 95%, ajusta el umbral:

```bash
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Contexto anterior | 200K tokens |
| Contexto actual | 1M tokens (5x) |
| Modelo con 1M | Opus 4.6 (incluido en Max/Team/Enterprise) |
| Alias de modelo | `opus[1m]`, `sonnet[1m]` |
| Auto-compactación | ~95% por defecto, ajustable con `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` |
| Desactivar 1M | `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` |
| Precio por token | Sin surcharge — mismo precio en toda la ventana |

> Documentación oficial: [Model configuration — Extended context](https://code.claude.com/docs/es/model-config#extended-context)
