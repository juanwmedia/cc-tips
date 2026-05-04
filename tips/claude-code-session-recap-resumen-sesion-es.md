---
date: 2026-05-04
type: tip
title_es: "Session recap en Claude Code: vuelve a tu terminal y la sesión ya sabe por dónde ibas"
title_en: "Session recap in Claude Code: come back to your terminal and your session remembers where you left off"
---

> **TL;DR** Si dejas el terminal sin foco más de 3 minutos, Claude Code prepara un resumen de la sesión en segundo plano y te lo muestra al volver. También funciona a demanda con `/recap`. Activado por defecto en todos los planes y providers.

Vuelves al portátil después de una reunión de cuarenta minutos. Tu sesión de Claude Code sigue abierta, pero el "¿por dónde iba?" se cuela antes que cualquier otra cosa. Lees los últimos mensajes para reconstruir el contexto. Tres minutos perdidos antes de cada bloque de trabajo, varias veces al día.

Anthropic empaquetó eso en una sola feature en la versión `v2.1.114` (Week 17 de abril 2026): **session recap**. Si te alejas más de tres minutos del terminal, Claude Code genera un resumen en background. Cuando vuelves, ahí está, en una línea, listo. Es el mismo principio que [`/btw`](/es/tips/claude-code-btw-pregunta-lateral) — información disponible en el momento exacto en que la necesitas, sin contaminar el contexto principal.

## Cómo funciona por dentro

Claude Code dispara el recap automático bajo tres condiciones simultáneas:

1. **Terminal sin foco** durante al menos 3 minutos desde el último turno completado.
2. **Sesión con al menos 3 turnos** previos (sesiones cortas no lo activan).
3. **Nunca dos veces seguidas** — si ya viste un recap, el siguiente se genera tras nueva actividad.

El resumen se calcula en segundo plano mientras tú estás en otra app, así que aparece sin latencia cuando vuelves. En modo no-interactivo (`claude -p`, hooks, headless) el recap se omite siempre.

## Resultado

```
[volviendo al terminal después de una reunión]

⏺ Recap: estabas migrando el módulo `auth/` a JWT.
   Editaste 4 archivos, faltan los tests de expiración.

>
```

Una línea. Sigue exactamente donde estabas — sin scroll, sin releer.

## Cómo usarlo

### **1. No hagas nada (modo automático)**

Ya está activado por defecto. Solo aleja el cursor del terminal más de 3 minutos y vuelve. Si llevas al menos 3 turnos, verás el recap.

### **2. A demanda con `/recap`**

Cuando lo necesites en mitad de una sesión larga — antes de cambiar de subtarea, antes de un commit, antes de pedirle un plan a Claude:

```
> /recap
```

Útil tras una sesión de 2 horas para auditar lo hecho antes del PR.

### **3. Desactivarlo si te molesta**

Dos formas:

```bash
# A. Desde dentro de Claude Code:
> /config
# Navega a "Session recap" y desactiva

# B. Mediante variable de entorno (en .zshrc / .bashrc):
export CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Trigger automático | Terminal sin foco ≥ 3 min + sesión con ≥ 3 turnos |
| Comando manual | `/recap` |
| Coste | Mínimo — corre en background reutilizando la caché del prompt |
| Frecuencia | Nunca dos veces seguidas sin nueva actividad |
| Modo no-interactivo | Siempre omitido |
| Desactivar | `/config` → Session recap, o `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` |
| Disponibilidad | Todos los planes y providers (Bedrock, Vertex, Foundry incluidos) |

## Requisitos

- Claude Code `v2.1.114` o posterior

> Documentación oficial: [Interactive mode — Session recap](https://code.claude.com/docs/es/interactive-mode#session-recap)
