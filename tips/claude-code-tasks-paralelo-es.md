---
date: 2026-04-27
type: tip
title_es: "Tu Claude Code está trabajando en paralelo. ¿Sabes verlo?"
title_en: "Your Claude Code Is Running in Parallel. Do You Know Where to See It?"
---

> **TL;DR** `/tasks` (alias `/bashes`) abre el panel donde convergen todos los trabajos que Claude Code lanza en paralelo: bashes en background con `Ctrl+B`, sesiones cloud con `--remote`, planes con `/ultraplan`, revisiones con `/ultrareview`, consolidaciones de memoria y subagentes. Si nunca lo has abierto, probablemente sea porque aún no has lanzado nada en paralelo.

## Por qué nadie sabe que existe

Probablemente abriste `/tasks` alguna vez, viste **"No tasks currently running"** y cerraste. Yo también. El panel no es interesante por sí solo — es interesante cuando entiendes que es el **dashboard común** de cinco features de Claude Code que probablemente ya estás usando por separado.

Cada una de esas features delega trabajo a algún sitio (tu shell, una VM en la nube, un subagente, el subconsciente de Claude) y reporta de vuelta al mismo panel. `/tasks` es donde se reúnen.

## Las 5 cosas que pueblan tu /tasks

**1. Bashes locales en background (`Ctrl+B`)**

Mientras tienes un comando ejecutándose con `!` ([bash mode](/es/tips/claude-code-bash-mode-ejecutar-comandos)), pulsa `Ctrl+B` para mandarlo al background. Aparece en `/tasks` con su PID y output en vivo. Ideal para builds largos, tests pesados o servidores de desarrollo.

**2. Sesiones cloud con `--remote`**

Cada `claude --remote "tarea"` que lanzas crea una [sesión cloud paralela](/es/tips/claude-code-sesiones-en-la-nube). Puedes disparar 3 o 4 a la vez y verlas todas listadas aquí, con su enlace a `claude.ai/code` para revisar el diff.

**3. `/ultraplan` corriendo en la nube**

[`/ultraplan`](/es/tips/claude-code-ultraplan-planificacion-nube) delega la planificación a una sesión web. Mientras tu terminal queda libre, el plan se teje en background. `/tasks` te muestra el estado (`investigating`, `needs your input`, `ready`) y el enlace para revisar.

**4. `/ultrareview` en paralelo**

[`/ultrareview`](/es/tips/claude-code-ultrareview) lanza una flota de agentes revisores en la nube y tarda 10–20 minutos. Mientras corren, tú sigues programando. `/tasks` te dice cuál es el progreso de cada uno.

**5. Memory consolidation y subagentes**

Cuando Claude pasa la [consolidación de memoria](/es/tips/claude-code-auto-dream-consolidar-memoria) o lanza un subagente con `run_in_background: true`, también aterrizan aquí.

## Cómo se navega

```
↑/↓     Moverte entre tareas en la lista
Enter   Abrir una tarea — ver output, enlace de sesión, opción de Stop
←/Esc   Cerrar el panel y volver a la conversación
```

Una vez dentro de una tarea puedes leer su output completo o detenerla si va por mal camino.

## Cómo se delega trabajo al panel

| Vía | Quién la dispara | Cuándo aparece |
|---|---|---|
| `Ctrl+B` durante un `!` | Tú, manualmente | En cuanto pulsas |
| `claude --remote "..."` | Tú, desde la CLI | Al crear la sesión cloud |
| `/ultraplan` | Tú, comando o palabra clave | Al confirmar el lanzamiento |
| `/ultrareview` | Tú, comando o `/ultrareview <PR>` | Al confirmar el lanzamiento |
| Subagente con `run_in_background` | Claude, autónomamente | Al spawn |
| Memory consolidation | Claude, durante `/auto-dream` | Mientras corre |

## El cambio mental

`/tasks` no se llena porque tú lo abras. Se llena cuando empiezas a delegar. La pregunta correcta no es "¿qué hace `/tasks`?" sino "¿qué trabajo largo estoy ejecutando en serie que podría estar corriendo en paralelo?".

> Documentación oficial: [Interactive mode — Background bash commands](https://code.claude.com/docs/en/interactive-mode) · [Commands reference](https://code.claude.com/docs/en/commands)
