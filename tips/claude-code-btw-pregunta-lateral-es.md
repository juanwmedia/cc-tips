---
date: 2026-03-11
type: tip
title_es: "Pregunta mientras Claude Code trabaja con /btw"
title_en: "Ask Questions While Claude Code Is Working with /btw"
---
# Quick Tip: Pregunta mientras Claude Code trabaja con /btw

> **TL;DR** Escribe `/btw` seguido de tu pregunta para obtener una respuesta rápida sin interrumpir la tarea en curso. No se añade al historial, no tiene acceso a herramientas, y reutiliza la caché del prompt (coste mínimo).

Claude Code ahora tiene un comando para preguntas laterales: `/btw`. Cuando Claude está en mitad de una tarea — editando archivos, ejecutando tests, investigando el codebase — puedes lanzar una pregunta rápida sin interrumpir su trabajo ni contaminar el historial de la conversación.

`/btw` es la inversa de un [subagent](/es/articulos/claude-code-subagents-guia-espanol): ve toda tu conversación pero no tiene herramientas. Un subagent tiene todas las herramientas pero arranca con contexto vacío. Usa `/btw` para preguntar sobre lo que Claude ya sabe; usa un subagent para que descubra algo nuevo.

La pregunta y la respuesta aparecen en un overlay. Cuando lo cierras, desaparecen. El contexto principal queda intacto, Claude sigue trabajando, y tú tienes tu respuesta.

Resultado:

```
> /btw cómo se llamaba el archivo de configuración que leímos antes?

┌─────────────────────────────────────────────┐
│ El archivo era src/config/database.ts,      │
│ lo leímos al analizar la conexión a Redis.  │
└─────────────────────────────────────────────┘

Pulsa Espacio, Enter o Escape para cerrar
```

## Cómo usarlo

### **1. Mientras Claude trabaja**

Cuando Claude está procesando una respuesta (ves el spinner activo), escribe:

```
/btw qué patrón estamos usando para los error handlers?
```

La pregunta se ejecuta de forma independiente. Claude no para lo que está haciendo.

### **2. Entre turnos**

También funciona cuando Claude no está activo. Es útil para consultas rápidas que no quieres que ocupen un turno completo ni añadan ruido al contexto:

```
/btw en qué rama estamos?
```

### **3. Referencia a trabajo previo**

`/btw` tiene visibilidad completa de la conversación actual. Puedes preguntar sobre código que Claude ya leyó, decisiones que tomó, o cualquier cosa del contexto:

```
/btw por qué elegimos SQLite en vez de Postgres?
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando | `/btw <pregunta>` |
| Acceso a herramientas | No — solo responde con lo que ya está en contexto |
| Historial | No se añade a la conversación principal |
| Seguimiento | No hay turnos adicionales — una pregunta, una respuesta |
| Disponibilidad | Funciona mientras Claude está procesando o entre turnos |
| Coste | Mínimo — reutiliza la caché del prompt de la conversación |
| Cerrar | `Espacio`, `Enter` o `Escape` |

> Documentación oficial: [Interactive mode — Side questions](https://code.claude.com/docs/es/interactive-mode#side-questions-with-btw)
