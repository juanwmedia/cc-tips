---
date: 2026-06-05
type: tip
title_es: "/compact en Claude Code: las instrucciones que desaparecen sin avisar (y cómo hacerlas sobrevivir)"
title_en: "/compact in Claude Code: the instructions that vanish without warning (and how to make them survive)"
---

> **TL;DR** Cuando la sesión se acerca al límite, Claude Code compacta solo, sin que escribas nada, y resume la conversación. Pero no todo vuelve igual: el system prompt, el CLAUDE.md raíz y la auto memory se re-inyectan del disco; en cambio tus reglas con `paths:`, el CLAUDE.md de subcarpeta y el cuerpo de las skills se pierden o se recortan. Por eso a veces Claude "se olvida" de una regla a media tarea. Regla de oro: lo que tiene que sobrevivir va al CLAUDE.md raíz o al principio del `SKILL.md`.

Lo inquietante no es el `/compact` que lanzas tú. Es el **automático**: cuando el contexto se acerca al límite, Claude Code compacta por su cuenta, a mitad de tarea, sin que toques nada. Y una regla que estaba gobernando tus edits puede dejar de aplicarse justo ahí, en silencio.

## Cómo funciona la compactación

Compactar reemplaza el historial de la conversación por un resumen estructurado. Lo que vuelve después depende de **cómo se cargó** cada instrucción:

- Lo que vive **fuera** del historial (system prompt, output style) queda intacto.
- Lo que se **relee del disco** al arrancar (CLAUDE.md raíz, reglas sin scope, auto memory) se re-inyecta.
- Lo que entró **como mensaje** en el historial (reglas con `paths:`, CLAUDE.md anidado, cuerpos de skill) se resume con el resto y solo vuelve cuando se dispara de nuevo.

El `/compact` manual y el automático funcionan igual. La diferencia es que el automático no lo eliges tú.

## Cómo se ve

```text
# Antes: la regla paths: gobierna tus edits
[Loaded .claude/rules/api-conventions.md]   ← aplica a src/api/**

# Claude compacta solo al acercarse al límite
⏺ Conversation compacted

# Después: la misma edición, sin esa regla
# (vuelve sola en cuanto Claude relee un archivo de src/api/)
```

## Qué sobrevive y qué no

| Mecanismo | Tras la compactación |
|---|---|
| System prompt y output style | Intactos (no son historial) |
| CLAUDE.md raíz y reglas sin scope | Se re-inyectan del disco |
| Auto memory (MEMORY.md) | Se re-inyecta del disco |
| Reglas con `paths:` | **Se pierden hasta que vuelvas a leer un archivo que las dispare** |
| CLAUDE.md anidado en subcarpetas | **Se pierde hasta releer un archivo de esa carpeta** |
| Cuerpos de skills invocadas | **Se re-inyectan, pero topados a 5.000 tokens por skill y 25.000 en total; la más vieja cae primero** |
| Hooks | No aplica (corren como código, no como contexto) |

"Se pierden" no es "se borran para siempre": las reglas `paths:` y el CLAUDE.md anidado vuelven solos en cuanto Claude lee otra vez un archivo que los active. El problema es la ventana entre medias, en la que Claude trabaja sin ellos sin avisarte.

## Cómo hacer que sobrevivan

**1. Reglas que no pueden faltar nunca**

Si una regla tiene que aplicarse pase lo que pase, no la dejes dependiendo de un `paths:`. Quítale el frontmatter de scope o muévela al CLAUDE.md raíz: ese se re-inyecta siempre.

**2. Instrucciones críticas, al principio del SKILL.md**

Cuando una skill se re-inyecta, el truncado **conserva el principio** del archivo y descarta el final. Pon lo que de verdad importa (las reglas duras, los gotchas) en las primeras líneas del `SKILL.md`, no al final.

**3. Compacta tú, con foco, antes de una tarea larga**

En vez de esperar al auto-compact a mitad de tarea, lánzalo tú en una pausa natural y dile qué conservar. El [hábito 3 de cómo ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos) cubre el `/compact` con instrucciones.

Esto es la otra cara de [prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo): allí `/compact` apenas penaliza en **consumo**; aquí el coste es de **fidelidad**, lo que se lleva por delante de tus instrucciones. Y para entender qué se carga al arrancar (antes de cualquier compactación), está [cuándo carga Claude Code cada feature](/es/tips/claude-code-cuando-se-cargan-features-contexto).

> Documentación oficial: [Explore the context window](https://code.claude.com/docs/en/context-window)
