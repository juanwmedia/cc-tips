---
date: 2026-04-17
type: tip
title_es: "Consigue Opus al precio de Sonnet en Claude Code"
title_en: "Get Opus Performance at Sonnet Prices in Claude Code"
---

> **TL;DR** Claude Code acaba de meter un ajuste nuevo (`/advisor`) que te deja usar Sonnet como motor principal y consultar a Opus solo cuando Sonnet no llega. Anthropic midió el combo: **−11,9 % de coste y +2,7 % de accuracy en SWE-bench** frente a Sonnet solo. Con Haiku + Opus asesor el salto es todavía más brutal: **41,2 % vs 19,7 %** en BrowseComp. Pagas precio-Sonnet el 90 % del tiempo y Opus solo aparece cuando hace falta.

## Cómo funciona

No es un swap de modelo ni un orchestration clásico. Es un patrón *player + coach*:

- **El executor** (Sonnet o Haiku) hace TODO el trabajo real — lee archivos, escribe código, llama tools, responde al usuario
- **El advisor** ([Opus 4.7](/es/tips/claude-code-opus-4-7) o Sonnet 4.6) se queda en el banquillo como una **herramienta más** dentro del toolbox del executor
- Cuando el executor llega a una decisión que no sabe resolver (un bug ambiguo, un refactor complejo, o simplemente está "circling without progress"), **llama al advisor** igual que llamaría a Bash
- El advisor lee **todo el contexto compartido** y devuelve un plan o corrección de **400–700 tokens** — ni código ni tool calls, solo guía
- El executor retoma con esa guía y sigue ejecutando

La analogía es un junior con el senior en marcación rápida: el junior escribe todo, solo llama cuando está atascado, el senior nunca toca el teclado.

## Qué vas a ver al escribir `/advisor`

```text
Advisor Tool

When Claude needs stronger judgment — a complex decision, an
ambiguous failure, a problem it's circling without progress — it
escalates to the advisor model for guidance, then resumes. The
advisor runs server-side and uses additional tokens.

For certain workloads, pairing Sonnet as the main model with Opus
as the advisor gives you near-Opus performance with reduced token
usage.

  1. Opus 4.7
  2. Sonnet 4.6
> 3. No advisor ✓

Enter to confirm · Esc to cancel
```

## Cómo activarlo

**1. Escribe `/advisor`** en cualquier sesión de Claude Code. Por defecto está en `No advisor` — activarlo es opt-in.

**2. Elige el advisor**:

- **Opus 4.7** si tu executor es Sonnet 4.6 — el combo mainstream que Anthropic recomienda
- **Sonnet 4.6** si tu executor es Haiku 4.5 — duplica la capacidad de Haiku con un extra de coste mínimo
- **No advisor** para desactivarlo

**3. Enter**. El advisor queda activado para la sesión. Sonnet seguirá haciendo TODO — solo escala cuando lo necesite.

**4. No tienes que invocar nada manualmente**. El executor decide cuándo consultar basándose en su propia incertidumbre. Puedes influir vía prompt ("si ves algo raro, consulta al advisor antes de tocar código").

## Cuándo merece la pena (y cuándo no)

**Activa el advisor cuando**:

- Trabajas en una tarea larga con muchas decisiones (refactor, migración, feature compleja)
- Sonnet te está fallando en algo específico y llevas ya varios intentos fallidos
- Vas a ejecutar algo crítico (pagos, auth, migrations) y quieres segunda opinión en caliente

**No actives el advisor cuando**:

- Haces CRUD, boilerplate o renames — pagas tokens extra sin retorno
- Ya usas [Opus 4.7](/es/tips/claude-code-opus-4-7) como executor — no tiene sentido que se consulte a sí mismo
- Estás en `/plan` puro — para eso usa [`opusplan`](/es/tips/claude-code-elegir-modelo-adecuado), que es una estrategia distinta

## Combos recomendados

| Executor | Advisor | Cuándo usarlo |
|---|---|---|
| Sonnet 4.6 | **Opus 4.7** | El default práctico — calidad Opus con coste Sonnet |
| Haiku 4.5 | **Opus 4.7** | Para [exploraciones largas](/es/tips/claude-code-modo-headless-agente-autonomo) y lecturas masivas de código |
| Haiku 4.5 | Sonnet 4.6 | Más barato aún, útil cuando solo necesitas un empujón puntual |
| Opus 4.7 | *(cualquiera)* | No tiene sentido — Opus ya es el modelo más capaz |

## Los números que publicó Anthropic

| Métrica | Cifra |
|---|---|
| Reducción de coste (Sonnet + Opus advisor vs Sonnet solo) | **−11,9 %** |
| Accuracy SWE-bench Multilingual (delta) | **+2,7 pp** |
| Haiku + Opus advisor en BrowseComp | **41,2 %** (Haiku solo: 19,7 %) |
| Tokens del advisor por consulta | **400–700** (1.400–1.800 con thinking) |

La cifra más llamativa: **Haiku con Opus como asesor dobla su nota en BrowseComp**. No es una mejora marginal — es consultar al modelo grande en el momento exacto y no el resto del tiempo.

## Referencia

| Campo | Valor |
|---|---|
| Comando | `/advisor` |
| Advisors disponibles | Opus 4.7, Sonnet 4.6 |
| Default | No advisor (opt-in) |
| Ejecución | Server-side |
| Tokens extra por consulta | 400–700 (plan) · 1.400–1.800 (con thinking) |
| Invocación | El executor decide cuándo consultar |
| API beta header | `advisor-tool-2026-03-01` |
| Origen | [Anthropic Advisor Strategy](https://claude.com/blog/the-advisor-strategy) (9 abril 2026) |

Es el tercer cambio grande de abril en Claude Code, después de [Opus 4.7](/es/tips/claude-code-opus-4-7) y [`/ultrareview`](/es/tips/claude-code-ultrareview). Los tres van en la misma dirección: delegar más, supervisar menos, pagar solo la potencia que realmente usas.

> Docs oficiales: [The advisor strategy — Anthropic](https://claude.com/blog/the-advisor-strategy) · [Advisor tool (API)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)
