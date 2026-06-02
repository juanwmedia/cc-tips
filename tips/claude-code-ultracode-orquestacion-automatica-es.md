---
date: 2026-06-02
type: tip
title_es: "ultracode en Claude Code: que Claude decida solo cuándo desplegar un ejército de agentes"
title_en: "ultracode in Claude Code: let Claude decide on its own when to deploy an army of agents"
---
> **TL;DR** `/effort ultracode` sube tu sesión a `xhigh` y deja que Claude decida solo, en cada tarea de fondo, si merece montar un [workflow de agentes](/es/tips/claude-code-workflows-subagentes-a-escala) (entender → cambiar → verificar). No es un nivel de razonamiento nuevo por encima de `xhigh`: es `xhigh` **más** orquestación automática. Dura la sesión y vuelves con `/effort high`. Enciéndelo para trabajo difícil y multi-paso; apágalo para lo rutinario, porque cuesta más en cada tarea.

Hay dos formas de pedirle agentes a Claude Code. La manual: escribes `workflow` en el prompt o lanzas `/deep-research`, y decides **tú** cuándo paralelizar, una tarea concreta. Y la automática: `/effort ultracode`, donde decide **Claude**, para toda la sesión. Este tip va de la segunda, y de la única pregunta que importa: cuándo encender ese interruptor.

## Qué es exactamente

`ultracode` es una opción del menú `/effort`, no un comando aparte. Hace dos cosas a la vez:

1. **Sube el razonamiento a `xhigh`** (el escalón alto de [effort](/es/tips/claude-code-effort-level-ajustar-razonamiento)).
2. **Le da a Claude autonomía para orquestar.** En lugar de esperar a que tú pidas un workflow, Claude planea uno por su cuenta para cada tarea de fondo de la sesión.

Cuidado con el nombre: no es un razonamiento "más alto que `xhigh`". Es `xhigh` y, encima, la decisión de cuándo desplegar agentes pasa de ti a Claude.

## Qué pasa al encenderlo

```
> /effort ultracode
  Effort: ultracode · Claude planea un workflow para cada tarea de fondo

> refactoriza el módulo de auth y añade tests
  → workflow 1: entender el flujo de auth
  → workflow 2: aplicar el cambio
  → workflow 3: verificar (agentes que se refutan entre sí)
```

Un solo request se convierte en varios workflows en cadena: uno para entender, otro para cambiar, otro para verificar. Y esto aplica a cada tarea de fondo que pidas hasta que lo apagues.

## Cómo usarlo

**1. Enciéndelo.**

```
/effort ultracode
```

Necesita un modelo que soporte `xhigh`. Si el tuyo no lo soporta, `ultracode` ni aparece en el menú `/effort`.

**2. Trabaja normal.** `ultracode` automatiza la *decisión de planear* un workflow, no el lanzarlo a ciegas: en el modo de permisos por defecto, Claude te enseña las fases antes de ejecutar y tú apruebas cada run (puedes abrir el script; no es una caja negra).

**3. Apágalo.**

```
/effort high
```

Dura solo la sesión actual y se resetea al abrir una nueva, pero baja a `high` en cuanto vuelvas a tareas rutinarias.

## Cuándo SÍ y cuándo NO

| Enciéndelo para | No lo enciendas para |
|---|---|
| Migraciones grandes, refactors multi-archivo | Renombrados, fixes de una línea |
| Auditorías de bugs o seguridad en toda la base | Cambios de formato o config |
| Research con fuentes cruzadas | Preguntas rápidas |
| Una sesión entera de trabajo difícil | El día a día rutinario |

La regla: si la tarea no necesita varios agentes verificándose entre sí, `ultracode` te cobra `xhigh` y orquestación para nada.

## Lo que te puede morder

- **Cuesta más en cada tarea de fondo**, no solo en las grandes. Cada request gasta más tokens y tarda más. Por eso es un interruptor que enciendes y apagas, no un default.
- **En Auto mode no hay ese freno.** Con permisos en Auto (o bypass), ultracode no solo planea el workflow: lo lanza sin pedirte aprobación, y las flotas de agentes arrancan solas.
- **Si desactivas los workflows** (`/config`, `disableWorkflows`, o `CLAUDE_CODE_DISABLE_WORKFLOWS=1`), `ultracode` desaparece del menú `/effort`.

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/effort ultracode` |
| Qué es | `xhigh` effort + orquestación automática (no un nivel nuevo) |
| Alcance | Toda la sesión, cada tarea de fondo |
| Comportamiento | 1 request → varios workflows en cadena (entender → cambiar → verificar) |
| Apagar | `/effort high` (o nueva sesión) |
| Requisito | Modelo con `xhigh`; si no, no sale en el menú |
| Auto mode | Se salta el prompt de aprobación del workflow |
| Disponibilidad | Research preview, parte de [dynamic workflows](/es/tips/claude-code-workflows-subagentes-a-escala) (v2.1.154+) |

> Documentación oficial: [Let Claude decide with ultracode](https://code.claude.com/docs/en/workflows#let-claude-decide-with-ultracode)
