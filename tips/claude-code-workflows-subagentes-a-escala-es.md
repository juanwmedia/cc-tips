> **TL;DR** Escribe la palabra `workflow` en tu prompt (o lanza el bundled `/deep-research`) y Claude escribe un **script de JavaScript** que orquesta hasta cientos de subagentes en background — con el plan y los resultados intermedios **fuera de su contexto**, y agentes que se refutan entre sí hasta converger antes de contestarte. Es research preview, requiere **Claude Code v2.1.154+**, está en todos los planes de pago (en Pro se activa en `/config`), y gasta bastantes más tokens: empieza por una tarea acotada.

Hoy salió Opus 4.8 (mismo precio que 4.7, ~4× menos probable que deje pasar fallos de código sin avisar). Pero lo que de verdad cambia *cómo trabajas* en Claude Code salió el mismo día y no es el modelo: **dynamic workflows**. Funciona con el modelo que tengas puesto.

El problema que resuelve: hasta ahora, si querías delegar una tarea enorme a muchos subagentes, **Claude era el orquestador** — decidía turno a turno qué lanzar, y *cada resultado intermedio le llenaba el contexto*. Por eso no escalaba más allá de un puñado de agentes.

## El cambio: el plan se mueve a código

|  | Subagentes | Skills | Workflows |
|---|---|---|---|
| Qué es | Un worker que Claude lanza | Instrucciones que Claude sigue | Un script que ejecuta el runtime |
| Quién decide qué corre | Claude, turno a turno | Claude, siguiendo el prompt | El script |
| Dónde viven los resultados | Contexto de Claude | Contexto de Claude | Variables del script |
| Escala | Unos pocos por turno | Igual que subagentes | Decenas a cientos por run |

Un workflow mueve el plan (el bucle, las ramas, el estado) a un script de JavaScript que Claude escribe sobre la marcha. Un runtime lo ejecuta **en background, aislado de tu conversación**. Tu contexto solo recibe la respuesta final. Eso permite dos cosas: correr cientos de agentes sin reventar el contexto, y aplicar un **patrón de calidad repetible** — agentes que revisan adversarialmente los hallazgos de otros antes de reportarlos.

## Pruébalo hoy sin escribir nada: `/deep-research`

La rampa de entrada a coste cero es un workflow que ya viene de serie:

```text
/deep-research ¿Qué cambió en el permission model de Node.js entre v20 y v22?
```

Lanza búsquedas en paralelo desde varios ángulos, cruza las fuentes, **vota cada claim**, y te devuelve un informe citado con lo que no sobrevivió al cross-check ya filtrado. Mientras corre, tu sesión sigue libre. Sigue el progreso con `/workflows`.

## Las tres formas de lanzar uno

```text
# 1. La palabra "workflow" en tu prompt (Claude escribe el script)
Lanza un workflow que audite cada endpoint bajo src/routes/ sin auth check

# 2. Un workflow bundled
/deep-research <pregunta>

# 3. Que Claude decida solo (opt-in)
/effort ultracode
```

Con `ultracode`, Claude decide por su cuenta si cada tarea merece un workflow — opt-in, dura la sesión, vuelve a `/effort high` para trabajo rutinario. Por defecto **no** monta flotas de agentes a menos que se lo pidas.

**El control:** antes de ejecutar nada, Claude te muestra las fases planeadas y puedes leer el script crudo (`Ctrl+G`). No es una caja negra. Y si un run te sirve, pulsas `s` en `/workflows` y queda guardado como `/tu-comando` para siempre, en cada branch y para todo el equipo que haga pull. Es el "skills 2.0".

## Para qué sirve de verdad

Migraciones de cientos de archivos, auditorías de seguridad o de bugs en toda la base de código, research con fuentes cruzadas. El caso extremo: Jarred Sumner portó **Bun de Zig a Rust** con workflows — 750.000 líneas, 99,8% del test suite pasando, 11 días del primer commit al merge, cientos de agentes en paralelo con dos revisores por archivo.

## Lo que tienes que saber antes (honesto)

- **Research preview** · requiere **v2.1.154+** · todos los planes de pago (en Pro lo activas en `/config`)
- **Límites:** máx. 16 agentes concurrentes, 1.000 en total por run
- **Coste:** un run gasta bastantes más tokens que hacer la tarea en conversación. Anthropic lo dice claro: empieza por una tarea acotada para coger el feel
- Los subagentes corren en `acceptEdits` y heredan tu allowlist; los edits de archivos se auto-aprueban

Si vienes de [worktrees paralelos](/es/tips/claude-code-worktrees-tareas-paralelas) o del [mapa de background agents](/es/tips/claude-code-background-agents-mapa), los workflows son el siguiente escalón: no varias sesiones tuyas, sino una que orquesta cientos de agentes con el plan en código.

> Documentación oficial: [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
