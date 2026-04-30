---
date: 2026-03-31
type: tip
title_es: "Haz que Claude Code vigile tu código mientras trabajas"
title_en: "Make Claude Code Watch Your Code While You Work"
---
# Quick Tip: Haz que Claude Code vigile tu código mientras trabajas

> **TL;DR** `/loop 5m <prompt>` ejecuta un prompt de forma recurrente dentro de tu sesión activa. A diferencia de un cron con `claude -p`, cada iteración tiene acceso al contexto completo de tu conversación: archivos leídos, decisiones tomadas, cambios en curso. Es un vigilante con cerebro, no un script ciego.

Podrías montar un cron que lance `claude -p "check deploy status"` cada 5 minutos. Funciona. Pero cada ejecución arranca desde cero — sin saber qué pasó antes, sin contexto de tu sesión, sin capacidad de actuar sobre lo que encuentra.

`/loop` es diferente: corre dentro de tu sesión abierta. Claude sabe qué archivos cambiaste, qué intentabas hacer, y puede comparar con la iteración anterior. Si algo cambia, puede actuar en el momento con todas tus herramientas.

La limitación: necesitas la sesión abierta. Si cierras la terminal, se pierde. Y las tareas expiran automáticamente a los 3 días. Para monitoring que sobreviva al cierre, usa [headless mode con cron](/es/tips/claude-code-modo-headless-agente-autonomo).

Resultado:

```
> /loop 5m check if the staging deploy at localhost:3000 is responding

Loop started (every 5m). Task ID: loop-a1b2c3
Next run: 12:05:00

# 12:05 — localhost:3000 returns 503. Deploy still in progress.
# 12:10 — localhost:3000 returns 200. Deploy complete. All health checks pass.
```

## Cómo usarlo

### **1. Sintaxis básica**

```
/loop [intervalo] <prompt>
```

El intervalo por defecto es 10 minutos. Formatos: `5m` (minutos), `2h` (horas), `1d` (días).

### **2. Ejemplos prácticos**

```
# Vigilar un deploy
/loop 5m check if the staging deploy finished and tests pass

# Monitorizar PRs
/loop 15m check open PRs for new comments, summarize responses needed

# Detectar conflictos de merge
/loop 30m detect merge conflicts between current branch and main

# Escanear logs en busca de errores
/loop 5m scan app.log for FATAL/ERROR entries in the last 5 minutes
```

### **3. Buenas prácticas**

- Define condiciones de alerta — no quieres ruido en cada iteración, solo anomalías
- Limita el scope — `src/` en vez de todo el proyecto
- Pon reglas de terminación — "stop after 3 consecutive passes"

## /loop vs cron + claude -p

| Aspecto | `/loop` | `cron + claude -p` |
|---|---|---|
| Contexto | Sesión completa (archivos, historial, decisiones) | Ninguno — cada ejecución es nueva |
| Puede actuar | Sí — edita, ejecuta, usa herramientas | Sí, pero sin contexto previo |
| Acumula conocimiento | Sí — compara con iteraciones anteriores | No |
| Persistencia | Solo mientras la sesión esté abierta | Sobrevive reinicios |
| Expiración | 3 días automáticamente | Sin límite |
| Concurrencia | Max 50 tareas por sesión | Sin límite |
| Caso de uso | Vigilar mientras trabajas | Monitoring real / tareas programadas |

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/loop [intervalo] <prompt>` |
| Intervalo por defecto | 10 minutos |
| Formatos | `5m`, `2h`, `1d` |
| Max tareas | 50 por sesión |
| Expiración | 3 días |
| Persistencia | No sobrevive al cierre del terminal |
| Tipo | Bundled skill (incluido de serie) |

> Documentación oficial: [Skills — Bundled skills](https://code.claude.com/docs/en/skills#bundled-skills)
