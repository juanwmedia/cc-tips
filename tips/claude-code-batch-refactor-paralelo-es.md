---
date: 2026-05-03
type: tip
title_es: "/batch en Claude Code: parte un refactor masivo en 30 agentes paralelos, uno por PR"
title_en: "/batch in Claude Code: split a massive refactor across 30 parallel agents, one PR each"
---

> **TL;DR** `/batch <instrucción>` lanza un agente orquestador que (1) explora tu codebase y descompone el cambio en 5-30 unidades independientes, (2) te presenta el plan para que apruebes, (3) ejecuta cada unidad en paralelo en su propio git worktree, y (4) abre un PR por cada agente. Hasta 10x más rápido que el mismo refactor secuencial.

Tienes un cambio masivo — renombrar `getUser` a `fetchUser` en 200 archivos, migrar de `axios` a `fetch`, sustituir un componente deprecated por su sucesor en todas las pantallas. Secuencialmente es una tarde de `find/replace` y una hora arreglando los tests. `/batch` lo resuelve en 5 minutos lanzando agentes en paralelo, cada uno en un [git worktree](/es/tips/claude-code-worktrees-tareas-paralelas) aislado.

## Cómo funciona internamente

`/batch` corre en tres fases:

**Fase 1 — Plan.** El orquestador entra en plan mode y lanza agentes Explore para investigar todo lo que toca tu instrucción: cada archivo, cada call site, cada test relacionado. Luego descompone el trabajo en **5 a 30 unidades autocontenidas** según el tamaño del codebase y la complejidad del cambio. Ves el plan antes de que nada mute.

**Fase 2 — Ejecución paralela.** Cuando apruebas, el orquestador dispara un agente background por unidad — todos en un único message block para que corran en **paralelo real**. Cada agente recibe isolation: un `git worktree` limpio con su propia rama. Sin interferencias, sin merge conflicts a mitad de vuelo.

**Fase 3 — Cierre.** Cada worker, tras aplicar sus cambios:

1. Ejecuta `/simplify` sobre su propio diff (comando hermano de cleanup).
2. Corre el test suite de su unidad.
3. Commit, push, y abre un PR con `gh pr create`.

Te despiertas con una cola de N PRs, cada uno con un alcance independiente, cada uno verde en CI.

## Resultado preview

```bash
> /batch renombra `getUser` a `fetchUser` en todo el codebase

⏺ Orquestador (Plan mode)

Explorando archivos afectados...
Encontrados 47 archivos en 4 paquetes.

Descompuesto en 6 unidades:
  1. core/auth/* (8 archivos)
  2. core/api/* (12 archivos)
  3. apps/web/* (11 archivos)
  4. apps/mobile/* (9 archivos)
  5. packages/sdk/* (4 archivos)
  6. tests/integration/* (3 archivos)

¿Aprobar plan? [y/N]
> y

⏺ Lanzando 6 agentes en paralelo...

[agent-1] worktree: ../proy-batch-1  rama: batch/rename-getuser-1
[agent-2] worktree: ../proy-batch-2  rama: batch/rename-getuser-2
[...]

[agent-1] ✓ /simplify ✓ tests pasan ✓ PR #421 abierto
[agent-3] ✓ /simplify ✓ tests pasan ✓ PR #422 abierto
[agent-2] ✓ /simplify ✓ tests pasan ✓ PR #423 abierto
[agent-5] ✓ /simplify ✓ tests pasan ✓ PR #424 abierto
[agent-4] ✓ /simplify ✗ test fail   ⚠ PR #425 abierto (draft)
[agent-6] ✓ /simplify ✓ tests pasan ✓ PR #426 abierto

Hecho en 4m 12s. 6 PRs abiertos. 1 necesita revisión.
```

## Cuándo usarlo (y cuándo no)

| Usa `/batch` para | Salta `/batch` para |
|---|---|
| Renombrados en masa por muchos archivos | Cambios fuertemente acoplados (un concern transversal) |
| Migraciones de librería (`axios` → `fetch`) | Trabajo que requiere decisiones secuenciales |
| Actualizar cada componente a una nueva API | Edits de un solo archivo — overkill |
| Añadir la misma instrumentación en todas partes | Cambios donde el output de una unidad alimenta a la siguiente |
| Limpieza masiva de código deprecated | Refactors donde aún no sabes la forma final |

La prueba mental: *¿se puede descomponer el trabajo en unidades independientes?* Si la unidad B depende del resultado de la A, `/batch` es la herramienta equivocada — usa una sesión normal con el [patrón Explore subagent](/es/tips/claude-code-agentic-ai-cinco-patrones).

## Referencia

| Aspecto | Detalle |
|---|---|
| Invocación | `/batch <instrucción>` (instrucción requerida) |
| Descomposición | 5-30 unidades independientes, dimensionadas por el orquestador |
| Aislamiento por agente | Un `git worktree` por agente |
| Gate de aprobación | Plan presentado antes de cualquier ejecución |
| Post-step por agente | `/simplify` → tests → commit → push → `gh pr create` |
| Velocidad | Hasta 10x más rápido que secuencial |

## Requisitos

- Repositorio Git con remote
- `gh` (GitHub CLI) instalado y autenticado
- Espacio en disco para N worktrees (cada uno es un checkout completo)

> Documentación oficial: [Claude Code commands reference](https://code.claude.com/docs/en/commands) (busca `/batch`)

> Mecánica hermana: [`/batch` corre cada agente en su propio git worktree — el mismo patrón de aislamiento que puedes pilotar manualmente](/es/tips/claude-code-worktrees-tareas-paralelas).
