---
date: 2026-06-13
type: tip
title_es: "/model en Claude Code: por qué tu modelo se queda pegado o se te resetea sin querer"
title_en: "/model in Claude Code: why your model sticks or resets when you didn't mean to"
---

> **TL;DR** Desde la **v2.1.153**, darle `Enter` en el picker de `/model` **guarda ese modelo como tu default global** para todas las sesiones nuevas; con `s` lo usas solo en esta sesión. Antes era al revés. Si tu modelo "se queda pegado" entre sesiones, es por eso. Y si "se te resetea" al arrancar, es que un settings de proyecto o de empresa manda sobre el tuyo.

Elegiste un modelo una vez, y ahora cada sesión nueva arranca con él aunque no lo pidieras. O al revés: lo cambias y al reiniciar vuelve solo a otro. Dos síntomas opuestos, misma raíz: **dónde se guarda tu elección y quién la pisa**. Y un cambio silencioso de comportamiento que casi nadie vio venir.

Resultado:

```
> /model

  1. Default (recommended)
> 2. Fable 5
  3. Sonnet
  4. Haiku
  5. Opus 4.8 ✓

Enter to set as default · s to use this session only
```

Lee esa última línea. Ahí está todo.

## Qué cambió en la v2.1.153

El picker hace ahora lo contrario que antes:

- **`Enter`**: cambia de modelo **y lo guarda como tu default** (escribe el campo `model` en tu user settings). Persiste en todas tus sesiones nuevas.
- **`s`**: cambia de modelo **solo en esta sesión**.
- Escribir `/model <nombre>` directo se comporta como `Enter` (o sea, también lo guarda).

En las versiones v2.1.144 a v2.1.152 era distinto: `/model` aplicaba solo a la sesión y la tecla `d` guardaba el default. Si tienes la memoria muscular de entonces, ahora estás **reescribiendo tu default sin darte cuenta** cada vez que pulsas `Enter`.

> El picker te pide confirmación cuando la conversación ya tiene output, porque la siguiente respuesta reprocesa toda la historia sin caché (cambiar de modelo a mitad de tarea [rompe el prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo)).

## Las cuatro formas de fijar el modelo (por precedencia)

| Forma | Alcance | Cómo |
|---|---|---|
| `/model` en sesión | Guarda default (con `Enter`) o solo sesión (con `s`) | `/model sonnet` |
| Flag `--model` | **Solo** la sesión que lanzas | `claude --model opus` |
| Variable de entorno | **Solo** esa sesión | `ANTHROPIC_MODEL=opus` |
| Settings (`model`) | Permanente | `{"model": "opus"}` |

`--model` y `ANTHROPIC_MODEL` no tocan tu default guardado: valen solo para esa terminal. Para correr modelos distintos en varias terminales a la vez, lanza cada una con su `--model` en lugar de cambiar con `/model`.

## Por qué se te resetea al arrancar

Aunque guardes tu default, **los settings de proyecto o de empresa (managed) mandan** y se reaplican en cada arranque. Si una sesión arranca con un modelo que no elegiste, la cabecera de inicio te dice qué archivo lo puso. Puedes sobreescribirlo con `/model`, pero el de proyecto o managed volverá en el siguiente arranque. Es la misma lógica de precedencia que cuando [chocan CLAUDE.md, skills y MCP](/es/tips/claude-code-precedencia-config-quien-gana).

Y un caso que confunde: las sesiones que retomas con `claude --resume`, `--continue` o el picker de `/resume` **mantienen el modelo que tenían al guardarse**, ignorando tu setting actual. Es a propósito: evita que el `/model` de otra sesión te cambie el modelo al reanudar.

## Cómo deshacer un default que pusiste sin querer

```bash
# Vuelve al recomendado para tu cuenta y limpia el override:
/model default        # y Enter

# O fija el que quieras de verdad como default:
/model sonnet         # y Enter
```

El alias `default` borra cualquier override y vuelve al modelo recomendado de tu tipo de cuenta. A partir de ahí, recuerda: `Enter` para el default, `s` cuando solo quieras probar algo en esta sesión.

## Dónde encaja

- ¿Qué modelo elegir para qué? [La guía de modelos](/es/tips/claude-code-elegir-modelo-adecuado) (Opus para planificar, Sonnet para ejecutar, `opusplan`).
- El escalón nuevo por encima de Opus: [Fable 5](/es/tips/claude-code-fable-5-por-encima-de-opus), que se activa con `/model fable` y, si le das `Enter`, también se queda de default.
- Por qué un setting de proyecto te pisa el modelo: [quién gana cuando las configs chocan](/es/tips/claude-code-precedencia-config-quien-gana).

> Documentación oficial: [Model configuration — Setting your model](https://code.claude.com/docs/en/model-config)

## Requisitos

El comportamiento `Enter` guarda default es de Claude Code **v2.1.153 o superior**. En v2.1.144–2.1.152 el default se guardaba con `d`.
