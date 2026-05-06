---
date: 2026-05-06
type: tip
title_es: "Routines en Claude Code: tu agente sigue trabajando con el portátil cerrado"
title_en: "Routines in Claude Code: your agent keeps working with the laptop closed"
---

> **TL;DR** Una **Routine** es un Claude Code guardado (prompt + repos + connectors MCP) con uno o más **triggers**: cron, GitHub event, o un endpoint HTTP que cualquier sistema puede pegar. Anthropic la ejecuta en su cloud, así que sigue funcionando con tu Mac cerrado. Disponible en planes Pro / Max / Team / Enterprise con Claude Code on the web habilitado.

[`/loop`](/es/tips/claude-code-loop-tareas-recurrentes) hace que Claude vigile algo dentro de tu sesión activa, pero muere cuando cierras el terminal. [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real) reacciona a eventos en stdout, pero también vive y muere con la sesión. **Routines es el escalón de arriba**: lleva ese mismo patrón de "Claude trabaja por mí" al cloud de Anthropic, donde no depende de que tu portátil esté encendido ni de que el terminal esté abierto.

Anthropic la lanzó en `v2.1.105+` (Week 16, abril 2026) y aún está en research preview — el endpoint API ship bajo header beta `experimental-cc-routine-2026-04-01`.

## Qué es exactamente una Routine

Tres piezas + uno o más disparadores:

1. **Prompt**: las instrucciones que Claude ejecuta cada vez que se dispara la routine (autónoma — sin permission prompts en mitad de la run)
2. **Repos**: uno o más repositorios de GitHub que Claude clona en cada run; por defecto solo puede pushear a ramas con prefijo `claude/`
3. **Connectors**: tus MCP conectados (Slack, Linear, Sentry, etc.) — Claude puede usar **cualquier tool** de los connectors incluidos sin pedir permiso
4. **Triggers**: cuándo arranca la routine. Una misma routine puede combinar varios.

Cada disparo crea una **sesión Claude Code completa** en VMs de Anthropic. Te aparece en tu lista de sesiones (web, Desktop, CLI) como una más. Puedes abrirla a posteriori, ver lo que hizo, revisar diffs, abrir PR.

## Los 3 tipos de trigger

### **1. Schedule trigger — cron en el cloud**

```bash
# Desde el CLI:
> /schedule daily PR review at 9am

# O desde web/Desktop: presets (hourly, daily, weekdays, weekly)
# o cron expression custom (mínimo: cada 1 hora)
```

Las horas se interpretan en tu timezone local. Hay un stagger automático de pocos minutos para no saturar la API. **Las one-off runs ("recuérdame en 2 semanas") NO cuentan contra el cap diario** de tu cuenta.

### **2. GitHub event trigger — reacciona a PRs y releases**

Solo se configura desde la web. Eventos soportados: `pull_request.*` y `release.*`. Filtros disponibles: autor, base/head branch, labels, título, regex.

```
# Ejemplo: solo PRs ready-for-review tocando el módulo auth
event: pull_request.opened
filter: is_draft = false AND head_branch contains "auth-"
```

Requiere **instalar la Claude GitHub App** en el repo (no basta `/web-setup`, que solo da permisos para clonar).

### **3. API trigger — webhook único por routine**

Cada routine tiene su `/fire` endpoint con bearer token único. Cualquier sistema externo puede dispararlo:

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01ABC.../fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

El `text` opcional llega a la routine como contexto literal del run. La respuesta devuelve `claude_code_session_id` y URL para seguir la run en el navegador en tiempo real.

## Las 6 plantillas que da Anthropic

| Caso | Trigger | Qué hace |
|---|---|---|
| **Mantenimiento de backlog** | Schedule (entre semana, noches) | Lee issues nuevos, etiqueta, asigna owners, postea resumen en Slack |
| **Triaje de alertas** | API | Sentry/Datadog dispara con stack trace → Claude correla con commits y abre draft PR con fix propuesto |
| **Code review a tu medida** | GitHub `pull_request.opened` | Aplica el checklist de tu equipo, deja comments inline de seguridad/perf/estilo |
| **Verificación de deploy** | API (desde tu CD) | Smoke checks tras cada deploy, escanea logs, postea go/no-go al canal de release |
| **Drift de docs** | Schedule semanal | Escanea PRs mergeados, flagea docs que referencian APIs cambiadas, abre PRs de update |
| **Port entre SDKs** | GitHub `pull_request.closed` (merged) | Cuando se mergea cambio en SDK-A, lo porta a SDK-B y abre PR matching |

## Resultado

```
> /schedule daily PR review at 9am

⏺ Routine creada: pr-review-daily
  Trigger: schedule, daily 09:00 (local)
  Repo: juanwmedia/ai-infra
  Connectors: GitHub, Slack
  Permissions: solo push a claude/*

[Al día siguiente, sin tu Mac encendido]

⏺ Routine ejecutándose en cloud session_01HJK...
  ✓ Cloned juanwmedia/ai-infra
  ✓ 4 PRs abiertos analizados
  ✓ 7 inline comments dejados en PR #421
  ✓ Slack #releases posteado: resumen de revisión

Done in 4m 22s.
```

## Caveats que debes saber antes

- **Research preview**: el endpoint `/fire` y los formats pueden cambiar; dos versiones del beta header conviven a la vez para dar tiempo de migrar
- **Las Routines son personales**, no del equipo: lo que hagan aparece como tú (commits, comments, mensajes de Slack)
- **Daily cap por cuenta** en cuántas runs pueden arrancar; ver consumo en [claude.ai/code/routines](https://claude.ai/code/routines)
- **GitHub triggers tienen cap horario** per-routine y per-account durante la preview
- **Branch safety por defecto**: solo `claude/*`. Para pushear a otras ramas, activa "Allow unrestricted branch pushes" por repo
- **El `/fire` body es texto opaco**: si mandas JSON, llega como string literal al prompt
- **Min interval recurring**: 1 hora. Cron expressions más rápidos se rechazan
- **Solo planes Pro / Max / Team / Enterprise** con Claude Code on the web habilitado

## Referencia

| Aspecto | Detalle |
|---|---|
| Versión mínima | Claude Code `v2.1.105` |
| Crear desde | [claude.ai/code/routines](https://claude.ai/code/routines), Desktop app, o `/schedule` en CLI |
| Triggers | Schedule (cron), GitHub event, API HTTP |
| Beta header | `experimental-cc-routine-2026-04-01` (solo `/fire`) |
| Min interval | 1 hora (recurring); one-off ilimitado |
| Branch safety | Solo `claude/*` por defecto |
| Connectors | Tus MCP conectados, configurables per-routine |
| Pricing | Cuenta contra tu subscription usage normal |
| Pairs con | [`/loop`](/es/tips/claude-code-loop-tareas-recurrentes) (su cousin intra-sesión), [Monitor](/es/tips/claude-code-monitor-eventos-tiempo-real) (eventos dentro de la sesión) |

> Documentación oficial: [Routines guide](https://code.claude.com/docs/en/routines)
