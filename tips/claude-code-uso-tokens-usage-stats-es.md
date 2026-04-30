---
date: 2026-04-13
type: tip
title_es: "Visualiza tu consumo real de tokens en Claude Code con /usage y /stats"
title_en: "Visualize Your Actual Token Consumption in Claude Code with /usage and /stats"
---

> **TL;DR** `/usage` muestra los límites de tu plan y el estado del rate limit. `/stats` abre un dashboard completo con heatmap de actividad, recuento de sesiones, total de tokens, desglose por modelo y rachas. Juntos responden a la pregunta que todo el mundo se hace ahora mismo: ¿dónde se me están yendo los tokens?

En el momento de escribir esto, el consumo de tokens y los límites de sesión son un tema más candente que nunca. Los developers se topan con límites, las sesiones parecen más cortas, y la reacción por defecto es culpar a la herramienta. Pero antes de optimizar nada, necesitas ver qué está pasando realmente. Dos comandos integrados te dan esa visibilidad — y la mayoría no sabe que existen.

`/usage` es la comprobación rápida: ¿estoy cerca del límite de mi plan? ¿Hay un rate limit activo ahora mismo? Responde a la pregunta inmediata de "¿puedo seguir trabajando?".

`/stats` es la vista a largo plazo: cuántas sesiones has ejecutado, cuántos tokens en total, qué modelos estás quemando, y cómo es tu patrón de actividad a lo largo de semanas y meses.

Ninguno de los dos comandos consume tokens. Ninguno modifica nada. Son diagnósticos de solo lectura.

Resultado:

```
> /usage

Status    Config    Usage    Stats

Plan: Max
Rate limit: 1,247 / 2,000 requests remaining
Resets in: 3h 42m
```

```
> /stats

              Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic  Ene  Feb  Mar  Abr
Lun           ░░   ██   ░░   ██   ██   ██   ██   ░░   ░░   ██   ██   ██   ██
Mié           ░░   ██   ██   ██   ██   ██   ░░   ░░   ██   ██   ██   ██   ██
Vie           ░░   ░░   ██   ██   ░░   ██   ██   ██   ██   ██   ██   ██   ░░

All time · Last 7 days · Last 30 days

Modelo favorito: Opus 4.6      Total tokens: 10.5m
Sesiones: 92                   Sesión más larga: 40d 22h 54m
Días activos: 66/99            Racha más larga: 56 días
Día más activo: 28 Mar         Racha actual: 8 días

↓ stats · r para cambiar rango · ctrl+s para copiar
```

## Cómo usarlos

### **1. Comprueba los límites de tu plan con /usage**

```bash
> /usage
```

Muestra cuatro pestañas: **Status**, **Config**, **Usage** y **Stats**. La pestaña Usage muestra tu consumo actual contra los límites del plan. Si estás en Pro o Max, aquí es donde ves cuánto te queda antes de tocar el rate limit.

### **2. Explora tu historial con /stats**

```bash
> /stats
```

La pestaña Stats abre un dashboard visual con:

- **Heatmap de actividad**: cuadrícula estilo GitHub mostrando qué días usaste Claude Code y con qué intensidad
- **Métricas de sesión**: total de sesiones, sesión más larga, días activos, datos de rachas
- **Desglose de tokens por modelo**: cuántos tokens consumió cada modelo (Opus, Sonnet, Haiku)
- **Gráfico de tokens por día**: consumo diario a lo largo del tiempo

Usa los atajos del teclado que aparecen abajo para navegar: `r` para cambiar entre rangos de tiempo (todo, 7 días, 30 días), flechas para moverte entre pestañas, `Ctrl+S` para copiar.

### **3. Combina con /context para visibilidad completa**

`/usage` y `/stats` muestran datos históricos y a nivel de plan. Para el desglose del contexto de la sesión actual, usa [`/context`](/es/tips/claude-code-comando-context-uso-tokens) — muestra exactamente cómo el system prompt, herramientas, MCP servers y mensajes consumen la ventana de 200k ahora mismo.

Los tres juntos te dan visibilidad completa: `/context` para la sesión actual, `/stats` para la tendencia a largo plazo, `/usage` para los límites del plan.

## Referencia

| Comando | Qué muestra | Alcance | ¿Consume tokens? |
|---|---|---|---|
| `/usage` | Límites del plan, estado del rate limit | Nivel de cuenta | No |
| `/stats` | Heatmap, sesiones, tokens, modelos, rachas | Historial completo | No |
| `/context` | Desglose de la ventana de contexto por categoría | Sesión actual | No |
| `/cost` | Coste en USD de la sesión actual | Sesión actual (usuarios API) | No |

## Cuándo usar cuál

| Situación | Comando |
|---|---|
| "¿Estoy a punto de tocar el límite?" | `/usage` |
| "¿Qué modelo estoy quemando más?" | `/stats` |
| "¿Qué se está comiendo mi contexto ahora mismo?" | `/context` |
| "¿Cuánto ha costado esta sesión en dólares?" | `/cost` |

> Documentación oficial: [Referencia de comandos](https://code.claude.com/docs/en/commands) | [Gestionar costes](https://code.claude.com/docs/en/costs)

Tips relacionados: [Monitoriza el uso de tokens con /context](/es/tips/claude-code-comando-context-uso-tokens) | [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos) | [Cómo elegir el modelo adecuado](/es/tips/claude-code-elegir-modelo-adecuado)
