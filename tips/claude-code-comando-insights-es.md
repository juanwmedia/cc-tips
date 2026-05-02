---
date: 2026-05-02
type: tip
title_es: "/insights en Claude Code: tu radiografía de uso (con reglas CLAUDE.md de regalo)"
title_en: "/insights in Claude Code: your usage X-ray (with CLAUDE.md rules as a bonus)"
---

Si llevas semanas o meses con Claude Code, hay un comando built-in que te genera un informe HTML interactivo de los últimos 30 días. Friction points rankeados por frecuencia. Charts de tools, lenguajes y patrones por hora. Y — lo mejor — sugerencias de reglas CLAUDE.md sacadas literal de las instrucciones que más repites.

Se llama `/insights`. Casi nadie lo ha ejecutado todavía, y la comunidad ya lo bautizó como *"el comando que te roastea las costumbres"*.

## Cómo funciona internamente

Cuando ejecutas `/insights`, Claude Code:

1. Escanea tus últimos 30 días de sesiones guardadas en `~/.claude/projects/<dir>/*.jsonl` (los mismos archivos que lee [`/fewer-permission-prompts`](/es/tips/claude-code-allowlist-automatica)).
2. Analiza patrones: qué tools llamas, qué archivos tocas, cuándo Claude no te entiende, dónde re-promptas.
3. Genera un informe HTML interactivo en `~/.claude/usage-data/report.html` y lo abre en tu navegador.
4. **Tu código fuente nunca sale de tu máquina** — solo se procesan los transcripts de sesión.

## Qué contiene el informe

| Sección | Qué te da |
|---|---|
| **At a glance** | Qué está funcionando, friction points actuales, quick wins, workflows ambiciosos |
| **Stats dashboard** | Mensajes, líneas de código cambiadas, archivos tocados, días activos |
| **Usage charts** | Tools llamadas, tipos de request, lenguajes, categorías de sesión |
| **Análisis narrativo** | Resumen de tu estilo de trabajo y patrones |
| **Time-of-day** | Cuándo programas con Claude (con selector de timezone) |
| **Friction analysis** | Breakdowns del workflow rankeados por frecuencia, con ejemplos citados de tus sesiones |
| **Sugerencias de reglas CLAUDE.md** | Reglas listas para pegar, sacadas de las instrucciones que más repites — el regalo |

## Cómo usarlo

```bash
/insights
```

Ese es el comando entero. Esperas ~30 segundos, el navegador se abre.

La friction analysis es la parte que escuece. Cosas como *"Claude no entendió la petición al primer intento en el 47% de las sesiones"* con ejemplos citados sacados literal de tus conversaciones. Doloroso, útil.

Las sugerencias de CLAUDE.md son la parte que paga. En lugar de [curar tu CLAUDE.md a mano](/es/tips/claude-code-claudemd-configurar-proyecto), recibes reglas generadas a partir de tu uso real. Mueve las buenas a tu CLAUDE.md del proyecto y la fricción baja en la siguiente ejecución.

## Cuándo ejecutarlo

- **Cadencia semanal**: track si tu fricción está bajando entre ejecuciones.
- **Después de una sesión autónoma larga**: descubre qué tropiezó a Claude antes de olvidarlo.
- **Onboarding de proyecto nuevo**: ten una baseline antes de tocar CLAUDE.md.
- **Cuando algo se siente raro**: si Claude lleva días "sin pillarlo", la friction analysis te dice por qué.

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/insights` (sin argumentos) |
| Rango de tiempo | Últimos 30 días de transcripts |
| Output | `~/.claude/usage-data/report.html` (se abre en el navegador automáticamente) |
| Fuente | `~/.claude/projects/<dir>/*.jsonl` |
| Privacidad | Procesamiento local — el código fuente no se sube |

> Documentación oficial: [Claude Code commands reference](https://code.claude.com/docs/en/commands) (busca `/insights`)

> Comando hermano sobre los mismos datos: [`/fewer-permission-prompts`](/es/tips/claude-code-allowlist-automatica) lee los mismos transcripts para armarte la allowlist.

