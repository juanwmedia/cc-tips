---
date: 2026-06-20
type: tip
title_es: "/fork en Claude Code: delega una tarea en segundo plano sin re-explicar tu contexto"
title_en: "/fork in Claude Code: delegate a background task without re-explaining your context"
---

> **TL;DR** `/branch` **te cambia a una copia** de la conversación (el original se queda, vuelves con `/resume`): es el `git checkout -b` de tu chat. `/fork <directiva>` **no te mueve**: lanza un **subagente en background que hereda toda tu conversación**, trabaja la directiva mientras tú sigues, y solo su **resultado final** vuelve al chat. Antes de la v2.1.161 `/fork` era un alias de `/branch`; desde 2.1.161 va por defecto. Y como hereda tu mismo prefijo, reusa la caché del padre: sale más barato que un subagente normal.

Si aprendiste `/fork` hace unos meses, tienes el modelo mental equivocado. Hasta la v2.1.161 `/fork` era literalmente un alias de `/branch`. Ahora son **dos mecanismos distintos**, y confundirlos es lo que hace que la gente use el que no toca.

## `/branch`: te clonas y te cambias

`/branch [nombre]` crea una rama de la conversación en este punto, **te cambia a ella** y preserva la original (vuelves con `/resume`). Es para explorar otra dirección sin perder lo que tienes. ¿La quieres como sesión nueva e independiente desde fuera? `claude --continue --fork-session` hace justo eso, y lo cuento en [bifurcar sesiones con fork-session](/es/tips/claude-code-fork-session-bifurcar-sesiones).

## `/fork`: delegas y sigues a lo tuyo

`/fork <directiva>` **no te mueve de sitio**. Lanza un **subagente en background que hereda toda la conversación** (mismo system prompt, tools, modelo e historial), trabaja la directiva mientras tú sigues en el hilo principal, y cuando termina **solo su resultado final** vuelve como un mensaje. Sus llamadas a herramientas no ensucian tu contexto.

El caso típico: estás a media implementación y, sin parar, lanzas `/fork redacta los tests de este cambio` o `/fork averigua por qué falla el build`. El fork arranca con tu mismo contexto (no le re-explicas nada), trabaja en paralelo y te deja el resultado cuando tú terminas lo tuyo. Ideal también para probar dos enfoques a la vez desde el mismo punto de partida.

```
> /fork redacta los unit tests del parser con los cambios de hasta ahora

  ┌─ main                                   trabajando…
  └─ redacta los unit tests del parser ⠋   (fork, en background)
     Enter: abrir y dirigir · x: descartar
```

El fork aparece en un **panel bajo el prompt**: `Enter` abre su transcript y le mandas mensajes, `x` lo descarta o lo para. Puedes lanzar varios y compararlos.

## Por qué no es un subagente normal

Un subagente normal **arranca en limpio**: no ve tu historial ni los ficheros que ya leíste; Claude le compone un mensaje-resumen y trabaja desde ahí (por eso a veces [pierden contexto](/es/tips/claude-code-subagentes-pierden-contexto)). El fork es la excepción: **hereda todo**, así que no le re-explicas nada. Y como su system prompt y sus tools son idénticos a los del padre, su primera petición **reusa la caché del padre** ([prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo)): por eso forkar es más barato que abrir un subagente desde cero.

## Referencia

| | `/branch [nombre]` | `/fork <directiva>` |
|---|---|---|
| Qué hace | Una rama de la conversación | Un subagente en background |
| ¿Te cambias? | Sí, pasas a la copia | No, sigues en el hilo |
| Contexto | Es tu conversación | Hereda toda tu conversación |
| Qué vuelve | Nada (eres tú) | Solo el resultado final |
| Dónde corre | Tu sesión | En background (panel abajo) |
| El original | Preservado (`/resume`) | Intacto, sigues en él |

## Detalles que conviene saber

- **Versión:** por defecto desde **v2.1.161**. En v2.1.117–2.1.160 necesitas `CLAUDE_CODE_FORK_SUBAGENT=1`. Antes de 2.1.117 no existe.
- **Forzar el modo:** `CLAUDE_CODE_FORK_SUBAGENT=1` lo activa, `=0` lo desactiva (en interactivo, SDK y `claude -p`).
- **Un fork no puede lanzar otro fork** (sí otros tipos de subagente).

> Documentación oficial: [Fork the current conversation](https://code.claude.com/docs/en/sub-agents#fork-the-current-conversation) · [Commands](https://code.claude.com/docs/en/commands)

## Requisitos

- Claude Code **v2.1.161+** para `/fork` por defecto; **v2.1.117+** activándolo con `CLAUDE_CODE_FORK_SUBAGENT=1`.
