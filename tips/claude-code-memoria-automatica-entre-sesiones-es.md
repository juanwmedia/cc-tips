---
date: 2026-03-04
type: tip
title_es: "¿Sabías que Claude Code recuerda entre conversaciones?"
title_en: "Did You Know Claude Code Remembers Between Conversations?"
---
# Quick Tip: ¿Sabías que Claude Code recuerda entre conversaciones?

Claude Code tiene una feature llamada **auto memory**: mientras trabajas, Claude escribe notas sobre tu proyecto en un directorio local, y las lee al inicio de cada nueva sesión. No es memoria nativa del modelo — es un sistema de ficheros que inyecta contexto automáticamente.

El resultado es sorprendente: Claude "recuerda" los comandos de build de tu proyecto, los patrones de depuración que descubrió, las decisiones de arquitectura que le explicaste. La semana pasada o hace tres semanas.

> **TL;DR** La carpeta `~/.claude/projects/<proyecto>/memory/` es el cerebro persistente de Claude. Cada sesión, lee las primeras 200 líneas de `MEMORY.md`. Lo que anota hoy, lo recuerda en la próxima conversación.

Ejemplo de `~/.claude/projects/<proyecto>/memory/MEMORY.md`:

```markdown
# Memory

## Comandos de build
- `npm run build:staging` carga las vars de staging automáticamente
- El deploy tarda ~4 min porque regenera imágenes responsive

## Patrones de depuración
- Los errores de CORS en local siempre son del proxy de Vite, no del backend
- El test de pagos falla intermitentemente — ticket #892 (race condition conocido)

## Decisiones de arquitectura
- SQLite en producción — servidor único, sin connection pooling
- Traducciones en `/lang/`, no en `/locales/` — legado del proyecto original
```

## Cómo gestionar la memoria

### **1. Ver qué recuerda Claude**

```bash
/memory
```

Lista todos los ficheros cargados en la sesión: `CLAUDE.md`, reglas y ficheros de memoria automática. Permite abrir cualquier fichero directamente en el editor.

### **2. Editar los apuntes**

Los ficheros de memoria son markdown plano. Puedes corregir información incorrecta, añadir contexto que Claude no capturó o borrar entradas obsoletas:

```bash
open ~/.claude/projects/$(basename $(pwd))/memory/MEMORY.md
```

### **3. Desactivar si no la quieres**

```json
{
  "autoMemoryEnabled": false
}
```

También via variable de entorno: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

## Referencia

| | `CLAUDE.md` | Auto memory |
|---|---|---|
| Lo escribe | Tú | Claude |
| Contiene | Instrucciones y reglas | Aprendizajes y patrones |
| Se comparte en git | Sí | No — local, por máquina |
| Límite al cargar | Sin límite | Primeras 200 líneas de `MEMORY.md` |

> Official docs: [Cómo recuerda Claude tu proyecto](https://code.claude.com/docs/es/memory)
