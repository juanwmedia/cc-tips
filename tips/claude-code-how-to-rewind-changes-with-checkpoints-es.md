---
date: 2026-02-21
type: tip
title_es: "Deshaz Cambios al Instante con Checkpoints"
title_en: "Rewind Changes Instantly with Checkpoints"
---
# Quick Tip: Deshaz Cambios al Instante con Checkpoints

Claude Code hace un snapshot automático de tu código antes de cada edición. Cada vez que envías un prompt, se crea un checkpoint. Si Claude toma un camino equivocado — rompe una feature, se desvía, o sobreingeniería una solución — puedes rebobinar a cualquier estado anterior en segundos. Los checkpoints persisten entre sesiones y se limpian automáticamente tras 30 días.

Resultado:

```
> Esc Esc  (pulsa Escape dos veces)

┌─ Rebobinar a ────────────────────────┐
│ ● Mensaje 5: "Añadir auth middleware"│
│ ○ Mensaje 4: "Crear modelo usuario"  │
│ ○ Mensaje 3: "Configurar base datos" │
│                                      │
│ Restaurar: ◉ Ambos  ○ Código  ○ Chat│
└──────────────────────────────────────┘
```

## Setup

No requiere configuración. Checkpointing está activado por defecto.

**1. Trabaja normalmente con Claude**

Cada prompt que envías crea un checkpoint automáticamente.

**2. Rebobina cuando lo necesites**

Pulsa `Esc` dos veces rápidamente, o escribe `/rewind`. Selecciona el checkpoint y qué restaurar:

```
Esc + Esc     → Abre el menú de rewind
/rewind       → Lo mismo, por comando
```

**3. Elige qué restaurar**

| Opción | Qué hace |
|---|---|
| **Código y conversación** | Restaura los archivos y rebobina el chat a ese punto |
| **Solo código** | Revierte los cambios en archivos, mantiene la conversación |
| **Solo conversación** | Rebobina el chat, mantiene el estado actual de los archivos |

## Referencia

| Característica | Detalles |
|---|---|
| Activación | `Esc` + `Esc` o `/rewind` |
| Creación de checkpoints | Automática en cada prompt del usuario |
| Persistencia | Sobrevive a reinicios de sesión y `/resume` |
| Retención | 30 días (configurable con `cleanupPeriodDays`) |
| Rastrea | Ediciones de archivos hechas por las herramientas de Claude |
| NO rastrea | Comandos bash (`rm`, `mv`, `cp`), ediciones externas |

## Limitaciones

- Los archivos modificados por comandos bash (ej. `rm file.txt`) no se rastrean
- Las ediciones manuales que hagas fuera de Claude Code no se capturan
- Los checkpoints son recuperación a nivel de sesión, no sustituyen a Git

> Documentación oficial: [Checkpointing](https://code.claude.com/docs/en/checkpointing)
