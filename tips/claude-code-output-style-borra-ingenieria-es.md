---
date: 2026-06-29
type: tip
title_es: "Tu output style en Claude Code borra el comportamiento de ingeniería sin avisar"
title_en: "Your Claude Code output style is silently deleting its engineering behavior"
---

> **TL;DR** Un output style custom **reemplaza** las instrucciones de ingeniería de Claude Code por defecto, no las suma. Si creas un estilo "persona" sin más, pierdes cómo acota cambios, escribe comentarios y verifica el trabajo. Una línea de frontmatter lo arregla: `keep-coding-instructions: true` superpone tu estilo en vez de borrar la base.

Creas tu primer output style. Le das una voz, un formato, una persona. Y de repente Claude empieza a programar peor: deja cambios a medias, no verifica, mete comentarios donde no toca. No es el modelo: es que tu output style ha **borrado** las instrucciones de ingeniería que traía de serie, y nadie te avisó.

## Por qué pasa

Un output style modifica el system prompt. La doc oficial lo dice sin rodeos: *"Custom output styles leave out Claude Code's built-in software engineering instructions, such as how to scope changes, write comments, and verify work, unless `keep-coding-instructions` is set to `true`."* Y ese flag, por defecto, es **`false`**.

Es decir: cuando defines un estilo propio, Claude Code asume que ya no estás programando (un asistente de escritura, un analista de datos) y quita la capa de ingeniería. Útil si de verdad no programas. Un disparo en el pie si solo querías cambiar el tono.

## El arreglo: una línea

En tu archivo de output style (`~/.claude/output-styles/mi-estilo.md` para todos los proyectos, o `.claude/output-styles/` para uno):

```markdown
---
name: Diagramas primero
description: Empieza cada explicación con un diagrama
keep-coding-instructions: true
---

Al explicar código o arquitectura, empieza con un diagrama Mermaid
de la estructura y luego explícalo en prosa.
```

Con `keep-coding-instructions: true`, tu instrucción se **añade encima** del comportamiento de ingeniería. Sin esa línea, lo sustituye.

## Cuándo cada uno

| Quieres… | `keep-coding-instructions` |
|---|---|
| Cambiar el tono/formato, pero sigues programando | `true` |
| Que Claude deje de ser ingeniero (escritura, análisis) | déjalo fuera (`false`) |

## Cómo cambiar de estilo (ojo, esto cambió)

El comando `/output-style` **se deprecó en la v2.1.73 y se eliminó en la v2.1.91**. Si lo buscas, no está. Ahora:

- `/config` → **Output style** para elegir del menú (se guarda en `.claude/settings.local.json`).
- O fija el campo directamente:

```json
{ "outputStyle": "Explanatory" }
```

El output style es parte del system prompt, que Claude Code lee **una vez al arrancar**. Los cambios aplican tras `/clear` o en una sesión nueva.

## Referencia

| Campo (frontmatter) | Qué hace | Por defecto |
|---|---|---|
| `name` | Nombre del estilo (si no, el del archivo) | nombre de archivo |
| `description` | Texto en el picker de `/config` | ninguno |
| `keep-coding-instructions` | Mantiene las instrucciones de ingeniería | `false` |

Esto NO es lo mismo que [CLAUDE.md](/es/tips/claude-code-claudemd-configurar-proyecto): el output style cambia el system prompt (rol, tono, formato); CLAUDE.md añade un mensaje con el contexto de tu proyecto **sin tocar** la base. Para una adición puntual de una sola invocación, usa `--append-system-prompt`.

> Documentación oficial: [Output styles](https://code.claude.com/docs/en/output-styles)

## Requisitos

- Claude Code v2.1.x (el campo `keep-coding-instructions` y `/config`; el viejo `/output-style` ya no existe).
