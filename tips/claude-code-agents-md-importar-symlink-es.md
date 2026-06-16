---
date: 2026-06-16
type: tip
title_es: "AGENTS.md: el estándar que leen Cursor, Codex y Copilot, pero no Claude Code"
title_en: "AGENTS.md: the standard Cursor, Codex and Copilot read, but Claude Code doesn't"
---

> **TL;DR** Claude Code no lee `AGENTS.md`, solo `CLAUDE.md`. Crea un `CLAUDE.md` con `@AGENTS.md` en la primera línea (importa tu AGENTS.md y debajo añades reglas solo-Claude) o, si no necesitas nada propio de Claude, un symlink: `ln -s AGENTS.md CLAUDE.md`. En Windows usa el `@import`, que los symlinks piden permisos de administrador. Un archivo, todos tus agentes.

`AGENTS.md` se ha convertido en el estándar para darle instrucciones a un agente de IA: lo leen de forma nativa Cursor, Codex, Copilot, Gemini CLI y unos cuantos más. Claude Code es la excepción. Lee `CLAUDE.md`, y solo `CLAUDE.md`. Si tu repo ya tiene un `AGENTS.md`, Claude Code lo ignora.

Lo dice la propia documentación, sin rodeos: *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`"*. Así que la opción mala es mantener dos archivos casi idénticos y sincronizarlos a mano. La buena: que tu `CLAUDE.md` **importe** al `AGENTS.md`, y mantienes uno solo.

```markdown
# CLAUDE.md
@AGENTS.md

## Claude Code
Usa plan mode para cambios en src/billing/.
```

Claude carga el `AGENTS.md` importado al arrancar la sesión y luego añade lo que pongas debajo. Tu equipo edita `AGENTS.md` para todas las herramientas; tú le reservas a Claude lo que solo le toca a él.

## Las tres formas

**1. `@AGENTS.md` import (la recomendada)**

Pon `@AGENTS.md` en la primera línea de tu `CLAUDE.md`. La sintaxis `@ruta` importa cualquier archivo al contexto al arrancar; admite rutas relativas y absolutas, es recursiva (hasta **4 saltos**) y, lo importante, **funciona en Windows**. La primera vez que Claude encuentre imports externos te muestra un diálogo de aprobación con la lista de archivos; si lo aceptas, no vuelve a preguntar. Esta vía te deja añadir reglas solo-Claude debajo del import.

**2. Symlink (la mínima)**

Si no necesitas nada específico de Claude, enlaza un archivo al otro:

```bash
ln -s AGENTS.md CLAUDE.md
```

Un único archivo en disco, dos nombres. **En Windows** crear un symlink exige permisos de administrador o el Modo Desarrollador, así que ahí quédate con el `@import`.

**3. `/init` si arrancas de cero**

Si tu repo ya tiene `AGENTS.md` (o `.cursorrules`, `.devin/rules/`, `.windsurfrules`), ejecuta `/init` y Claude los lee e incorpora lo relevante al `CLAUDE.md` que genera. Es la vía para migrar sin copiar y pegar a mano.

## Referencia

| Detalle | Valor |
|---|---|
| Qué lee Claude Code | `CLAUDE.md` y `.claude/CLAUDE.md`, nunca `AGENTS.md` directo |
| Sintaxis de import | `@ruta` (relativa o absoluta) |
| Recursividad | Sí, hasta 4 saltos |
| Windows | `@import` sí; symlink necesita admin / Modo Desarrollador |
| Primer import externo | Diálogo de aprobación una sola vez |
| `/init` con `AGENTS.md` presente | Lo lee e incorpora (también `.cursorrules`, `.devin/rules/`, `.windsurfrules`) |

## Dónde encaja

- Lo que de verdad debe ir dentro de ese archivo (y lo que sobra) está en [tu CLAUDE.md está lleno de basura](/es/tips/claude-code-claudemd-configurar-proyecto). El `@AGENTS.md` es solo la primera línea.
- ¿El archivo combinado crece demasiado? Saca las normas por ámbito a [reglas condicionales en `.claude/rules/`](/es/tips/claude-code-reglas-condicionales): cargan solo cuando Claude toca los archivos que casan.

> Documentación oficial: [How Claude remembers your project · AGENTS.md](https://code.claude.com/docs/en/memory)

## Requisitos

- Para el symlink en Windows: permisos de administrador o Modo Desarrollador (o usa el `@import`, sin requisitos).
