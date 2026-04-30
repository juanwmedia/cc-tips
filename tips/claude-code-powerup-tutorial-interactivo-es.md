---
date: 2026-04-02
type: tip
title_es: "Claude Code tiene un tutorial interactivo oculto: /powerup"
title_en: "Claude Code Has a Hidden Interactive Tutorial: /powerup"
---
# Quick Tip: Claude Code tiene un tutorial interactivo oculto: /powerup

> **TL;DR** Escribe `/powerup` y accede a 18 lecciones interactivas con demos animadas dentro de tu terminal. Cada una enseña una feature que la mayoría no conoce. Incluso si eres usuario avanzado, vas a descubrir algo.

Desde la versión 2.1.90, Claude Code incluye un sistema de lecciones integrado. No es documentación estática — son tutoriales interactivos con snippets de código, demos animadas y progreso gamificado. Cada "power-up" cubre una feature concreta que puedes probar en el momento.

Lo interesante: no es solo para principiantes. Siendo usuario avanzado, descubrí que puedes añadir `&` al final de un comando bash para que Claude lo ejecute en background y lo supervise — algo que no había visto en ninguna documentación.

Resultado:

```
> /powerup

Power-ups 0/18 unlocked ████░░░░░░░░░░░

Each power-up teaches one thing Claude Code can do
that most people miss. Open one, read it, try it, mark it done.

  o Talk to your codebase      @ files, line refs
  o Steer with modes           shift+tab, plan, auto
  o Undo anything              /rewind, Esc-Esc
  o Run in the background      tasks, /tasks
  o Teach Claude your rules    CLAUDE.md, /memory
  o Extend with tools          MCP, /mcp
  o Automate your workflow     skills, hooks
  o Multiply yourself          subagents, /agents
  o Code from anywhere         /remote-control, /teleport
  o Dial the model             /model, /effort
```

## Cómo usarlo

### **1. Abrir el menú de power-ups**

```
/powerup
```

Verás la lista completa con tu progreso. Selecciona cualquiera para abrirlo.

### **2. Leer, probar, marcar como hecho**

Cada power-up tiene texto explicativo, snippets de código, y una demo animada. Cuando lo hayas probado, márcalo como completado. Tu progreso se guarda.

### **3. Descubrir lo que no sabías**

Algunos power-ups que sorprenden incluso a usuarios avanzados:

- **Run in the background**: `! npm run build &` — el `&` al final hace que Claude ejecute el comando en background y lo supervise. Puedes seguir trabajando.
- **Steer with modes**: `Shift+Tab` cicla entre default, plan, y auto mode sin abrir ningún menú.
- **Undo anything**: `Esc+Esc` abre el rewind directamente, sin escribir `/rewind`.

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/powerup` |
| Lecciones | 18 power-ups |
| Formato | Texto + snippets + demos animadas |
| Progreso | Se guarda entre sesiones |
| Versión mínima | v2.1.90+ |
| Nivel | Principiante a avanzado |

> Documentación oficial: [Changelog — v2.1.90](https://code.claude.com/docs/en/changelog)
