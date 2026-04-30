---
date: 2026-02-21
type: tip
title_es: "Ejecuta Tareas en Paralelo con Git Worktrees"
title_en: "Run Parallel Tasks with Git Worktrees"
---

> **TL;DR** `claude -w feature-auth` crea un worktree, abre una nueva rama y arranca una instancia de Claude en ella. Hazlo tres veces en tres terminales y tienes tres Claudes trabajando en tres tareas distintas — en paralelo, en el mismo repo, sin conflictos.

Sí, los worktrees parecen complicados. Y sí, son de esas cosas que solo usas cuando la necesidad realmente lo requiere. Pero los beneficios son tan desproporcionados que quizás este es el momento de empezar. En vez de esperar a que Claude termine una tarea para empezar la siguiente, lanzas múltiples instancias que trabajan simultáneamente en ramas separadas. Mismo repo, diferentes directorios de trabajo, cero conflictos. Aquí es donde Claude Code deja de ser una herramienta y empieza a ser un equipo.

Un worktree es un directorio de trabajo adicional vinculado al mismo repositorio git. Cada uno tiene su propia rama y su propio estado de archivos, pero comparten el mismo `.git`. Claude Code lo integra con un solo flag: `-w`.

Resultado:

```
# Terminal 1
> claude -w feature-auth
Creating worktree at .claude/worktrees/feature-auth (branch: feature-auth)
╭──────────────────────────────────╮
│ Session in worktree feature-auth │
╰──────────────────────────────────╯

# Terminal 2
> claude -w fix-navbar
Creating worktree at .claude/worktrees/fix-navbar (branch: fix-navbar)

# Terminal 3
> claude -w refactor-api
Creating worktree at .claude/worktrees/refactor-api (branch: refactor-api)

# 3 Claudes. 3 tareas. En paralelo.
```

## Cómo usarlo

### **1. Lanzar un worktree**

```bash
claude -w feature-auth
```

Claude crea el worktree en `.claude/worktrees/feature-auth`, crea una rama basada en HEAD y arranca una sesión en ese directorio. Todo en un solo comando.

### **2. Abrir más worktrees en paralelo**

Abre una nueva terminal y lanza otro:

```bash
claude -w fix-navbar
```

Cada worktree es independiente. Cada Claude trabaja en su propia rama sin pisar al otro.

### **3. Desde dentro de una sesión**

Si ya estás en una sesión y quieres moverte a un worktree:

```bash
/worktree
```

Claude crea el worktree y cambia el directorio de trabajo de la sesión actual.

### **4. Limpiar cuando termines**

Al salir de una sesión en worktree, Claude te pregunta si quieres mantenerlo o eliminarlo. Los cambios de cada rama se mergean como cualquier otra rama git.

## Referencia

| Comando | Qué hace |
|---|---|
| `claude -w <nombre>` | Crea worktree + rama + sesión en un solo paso |
| `/worktree` | Crea worktree desde una sesión existente |
| `/worktree <nombre>` | Crea worktree con nombre específico |

| Concepto | Detalle |
|---|---|
| Ubicación | `.claude/worktrees/<nombre>` dentro del repo |
| Rama | Nueva rama basada en HEAD del momento de creación |
| Independencia | Cada worktree tiene su propio directorio de trabajo y staging area |
| Limpieza | Al salir, Claude pregunta si mantener o eliminar el worktree |
| VS Code | Cada worktree se abre en su propia ventana de VS Code |

> Documentación oficial: [Use git worktrees for parallel tasks](https://code.claude.com/docs/en/vs-code#use-git-worktrees-for-parallel-tasks)
