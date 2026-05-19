---
date: 2026-05-19
type: tip
title_es: "Plan Mode en Claude Code: no hace más inteligente a Claude, te obliga a entender tú"
title_en: "Plan Mode in Claude Code: it doesn't make Claude smarter — it forces you to think"
---
> **TL;DR** `Shift+Tab` cicla hasta plan o `/plan <prompt>` para un solo turno. Claude investiga, propone un plan paso a paso, no toca un solo archivo. Yo lo combino con [`/evaluate`](/es/tips/claude-code-evaluator-optimizer-patron) antes de implementar — y a veces después también, para contrastar lo que Claude hizo contra el plan original. Plan mode no le da superpoderes a Claude; te fuerza a ti a entender lo que vas a tocar.

Plan Mode es uno de los primeros pasos para trabajar con un agente AI con un mínimo de estructura. El mito que se repite es que al entrar en Plan Mode activas una especie de superpoderes — que Claude se vuelve más inteligente, más cuidadoso, más "él mismo." La realidad es más mundana y más útil: lo que Plan Mode hace es **obligar a Claude a diseccionar la tarea en acciones lo más atómicas posibles**. Y al forzarlo a hacerlo, te fuerza a ti a entenderlo. Por eso parece mágico cuando no lo es. Es simplemente el poder de planificar antes de actuar — el mismo que en humanos.

Técnicamente, Plan Mode es un modo de permisos read-only: Claude lee archivos, ejecuta comandos de shell read-only (`grep`, `ls`, `find`, `cat`), y escribe un plan. No puede tocar ni un solo archivo hasta que tú apruebes el plan explícitamente.

Resultado:

```
> /plan add rate limiting to the auth endpoints

⠋ Exploring codebase...
⠋ Reading src/auth/*.ts
⠋ Reading src/middleware/*.ts

Here's my plan for adding rate limiting:

1. Install express-rate-limit
2. Create src/middleware/rateLimit.ts with two tiers:
   - Strict: /login, /register, /reset-password (5 req/15min)
   - Standard: /me, /refresh (100 req/15min)
3. Wire into src/app.ts before auth routes
4. Add RATE_LIMIT_WINDOW and RATE_LIMIT_MAX to .env.example
5. Update README.md with the new env vars

Ready to proceed?
  ❯ Approve and start in auto mode
    Approve and accept edits
    Approve and review each edit manually
    Keep planning with feedback
    Refine with Ultraplan
```

## Cuatro formas de entrar en Plan Mode

### **1. Shift+Tab — ciclar a plan en mitad de sesión**

Pulsa `Shift+Tab` para ciclar entre los modos: `default → acceptEdits → plan`. La barra de estado muestra el modo activo. Para los otros tres modos disponibles (`auto`, `dontAsk`, `bypassPermissions`) ver [los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab).

### **2. `/plan <prompt>` — solo este turno**

Prefija un único prompt con `/plan` para entrar en plan solo para esa interacción:

```
> /plan refactoriza la lógica de reintentos de pago con backoff exponencial
```

Útil cuando la mayoría del turno la quieres en `acceptEdits` y solo este cambio concreto necesita planificación.

### **3. `--permission-mode plan` — arrancar la sesión en plan**

```bash
claude --permission-mode plan
```

Toda la sesión arranca en plan mode. Útil cuando vas a explorar un repo nuevo o tienes que tomar una decisión arquitectónica antes de tocar nada.

### **4. `defaultMode` — plan por defecto en este proyecto**

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Cualquier sesión que arranques en este proyecto comienza en plan. Recomendado para repos críticos: producción, sistemas de pagos, código que toca datos de usuarios.

## El workflow que de verdad funciona

Cuando el plan está listo, Claude te ofrece cinco opciones. Las cuatro primeras aprueban; la quinta refina:

| Opción | Qué hace |
|---|---|
| Approve and start in auto mode | Aprueba el plan y cambia a auto mode para implementarlo |
| Approve and accept edits | Aprueba y cambia a `acceptEdits` |
| Approve and review each edit manually | Aprueba y cambia a `default` — revisas cada edición |
| Keep planning with feedback | Pide más iteración sobre el plan |
| Refine with Ultraplan | Escala a [Ultraplan en la nube](/es/tips/claude-code-ultraplan-planificacion-nube) para revisión en navegador |

Antes de aprobar, pulsa `Ctrl+G` para abrir el plan en tu editor por defecto. Puedes anotar pasos, eliminar los que no te convencen, reordenar operaciones, y guardar. Claude usa el plan editado.

Mi flujo personal: en lugar de aprobar directo, paso el plan por [`/evaluate`](/es/tips/claude-code-evaluator-optimizer-patron) antes. El evaluador contrasta cada paso contra el código real — si Claude dice "voy a modificar `src/middleware/auth.ts` línea 42", `/evaluate` verifica que esa línea existe y que el cambio tiene sentido. A veces incluso lo paso por `/evaluate` después de implementar, contra el plan original, para detectar desviaciones silenciosas. Plan → `/evaluate` → Implementar → `/evaluate`. Suena paranoico hasta que evita el primer desastre.

## ¿Hasta para cambiar el color de un botón?

Yo diría que sí. Una pregunta sin filtrar puede acabar tocando archivos que no esperas — un util compartido, un theme global, un test snapshot. Plan mode te muestra qué piensa tocar Claude antes de hacerlo. Cinco segundos de "ah, va a modificar 8 archivos, no 1" te ahorran 20 minutos de revertir cambios.

El coste de planificar es bajo. El coste de no planificar puede ser cualquier cosa.

## Referencia

| Método | Cuándo usarlo |
|---|---|
| `Shift+Tab` | Ciclar mid-sesión |
| `/plan <prompt>` | Un solo turno en plan |
| `claude --permission-mode plan` | Sesión completa en plan |
| `defaultMode: "plan"` en `.claude/settings.json` | Plan por defecto en este proyecto |
| `Ctrl+G` | Editar el plan en tu editor antes de aprobar |

> Documentación oficial: [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
