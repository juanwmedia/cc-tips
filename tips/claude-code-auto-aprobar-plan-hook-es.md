---
date: 2026-06-28
type: tip
title_es: "Deja de aprobar cada plan en Claude Code (sin auto-aprobar nada más)"
title_en: "Stop approving every plan in Claude Code (without opening the floodgates)"
---

> **TL;DR** Un hook `PermissionRequest` con `"matcher": "ExitPlanMode"` que devuelve `{"behavior":"allow"}` aprueba solo el "¿procedo con el plan?". Bash, edits y MCP siguen preguntando igual. La clave es el matcher estrecho: automatizas un permiso, no todos. Funciona en interactivo: como actúa sobre el diálogo de permiso, en headless (`-p`) no aplica; ahí el evento sería `PreToolUse` con `permissionDecision: "allow"`.

Lanzas un plan grande. Te levantas a por un café, o te pones con otra cosa. Vuelves diez minutos después y Claude no ha tocado nada: lleva todo ese rato parado, esperando que apruebes el "sí, procede". Tiempo muerto, y encima por un permiso que ibas a dar igual.

La parte buena: ese permiso concreto se puede automatizar. Y solo ese.

## Cómo funciona

Cuando Claude sale de plan mode llama a una tool, `ExitPlanMode`, que requiere permiso. El evento `PermissionRequest` se dispara justo cuando aparecería el diálogo de aprobación. Un hook puede responderlo por ti con `behavior: allow`. Acotado con `"matcher": "ExitPlanMode"`, solo toca ese permiso, ninguno más.

Resultado:

```
Here's my plan:
  1. ...
  2. ...

✓ Allowed by PermissionRequest hook
```

Sin esperar tu clic.

## Cómo montarlo

### **1. El hook en `settings.json`**

En `~/.claude/settings.json` (o el `.claude/settings.json` del proyecto):

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

El comando escribe la decisión en stdout. Nada más: el plan se aprueba solo.

### **2. El matcher estrecho es la seguridad**

`"matcher": "ExitPlanMode"` hace que el hook responda **solo** a ese permiso. Un `rm`, una edición, una llamada MCP te siguen pidiendo permiso como siempre. Automatizas una cosa concreta, no bajas la guardia en el resto.

### **3. Solo en interactivo**

`PermissionRequest` actúa sobre el diálogo de aprobación, así que en headless (`claude -p`) no aplica. Si lo necesitas ahí, el evento es `PreToolUse` con `permissionDecision: "allow"`. Al aprobar, Claude Code restaura el modo de permisos que tenías antes de entrar en plan.

## Lo que NO hacer

Circula una variante que, además de aprobar el plan, salta a `bypassPermissions` para que **nada** vuelva a preguntar. Eso es lo contrario de la idea: abre la mano con todo. Si quieres seguir revisando bash y edits, evítala. El valor está, justamente, en el matcher estrecho.

## Referencia

| Pieza | Valor |
|---|---|
| Evento | `PermissionRequest` (interactivo) · `PreToolUse` (headless) |
| Matcher | `ExitPlanMode` (nombre pelado, sin specifier) |
| Salida | `{"hookSpecificOutput":{...,"decision":{"behavior":"allow"}}}` |
| Alcance | Solo el permiso de salir de plan mode |

> Documentación oficial: [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)

Encaja con [plan mode](/es/tips/claude-code-plan-mode-obliga-entender), de donde sale el permiso, y con [el sistema de permisos de `/permissions`](/es/tips/claude-code-permisos-3-conceptos-clave) (deny/allow/ask), del que este hook es la capa programable.

## Requisitos

- Claude Code v2.1.x. El hook `PermissionRequest` actúa en sesiones interactivas.
- `ExitPlanMode` requiere permiso, y por eso se puede interceptar.
