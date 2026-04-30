---
date: 2026-04-03
type: tip
title_es: "Haz que Claude Code recuerde lo que importa"
title_en: "Make Claude Code Remember What Matters"
---
# Quick Tip: Haz que Claude Code recuerde lo que importa

> **TL;DR** Acabas de resolver algo no trivial. El contexto está fresco. En vez de esperar a que auto-memory decida qué guardar, dile a Claude: "extrae lo que acabamos de hacer como skill". En 30 segundos tienes un workflow reutilizable en `.claude/skills/`.

Auto-memory guarda lo que Claude considera relevante. Pero no captura workflows completos — los pasos, las decisiones, los gotchas que descubriste por el camino. Eso se pierde cuando cierras la sesión.

El truco es simple: justo después de resolver algo difícil, pídele a Claude que lo convierta en una [skill](/es/articulos/claude-code-skills-flujos-trabajo-personalizados) reutilizable. No necesitas un comando especial. Claude ya sabe crear skills. Solo necesitas el hábito de pedírselo en el momento adecuado.

Resultado:

```
Tú: extrae lo que acabamos de hacer para arreglar el memory leak
    en una skill reutilizable en .claude/skills/

Claude: crea ~/.claude/skills/fix-memory-leak/SKILL.md con:
  - Los pasos de diagnóstico que seguimos
  - Los patrones que buscamos (event listeners sin cleanup)
  - El fix estándar
  - El comando de verificación

Tú: /fix-memory-leak
# La próxima vez, el workflow completo está a un comando de distancia.
```

## Cómo hacerlo

### **1. Identifica el momento**

Acabas de resolver algo que:
- Te llevó más de 10 minutos
- Involucró pasos que no son obvios
- Podría repetirse en el futuro

### **2. Pídelo en caliente**

```
Extrae lo que acabamos de hacer como skill en .claude/skills/<nombre>/SKILL.md.
Incluye los pasos, los patrones que buscamos, y cómo verificar que funciona.
```

Claude tiene todo el contexto de la conversación — los archivos que leyó, los errores que encontró, la solución final. Es el mejor momento para capturarlo.

### **3. Afina el resultado**

Claude genera un `SKILL.md` con frontmatter y los pasos. Revísalo: recorta lo que sobra, añade lo que falta. La skill es tuya — un archivo markdown que puedes editar.

### **4. Úsalo la próxima vez**

```
/fix-memory-leak
```

O deja que Claude lo invoque automáticamente cuando detecte un problema similar (si la `description` del frontmatter es buena).

## Cuándo capturar

| Señal | Ejemplo |
|---|---|
| Debugging no trivial | Memory leaks, race conditions, auth edge cases |
| Setup complejo | Configurar MCP server, desplegar a un entorno nuevo |
| Patrón que se repite | Migrar un componente, actualizar dependencias |
| Workflow multi-paso | Deploy + verificación + rollback |

## Referencia

| Aspecto | Detalle |
|---|---|
| Qué pedir | "Extrae esto como skill en `.claude/skills/`" |
| Cuándo | Justo después de resolver algo no trivial — el contexto está fresco |
| Resultado | Un `SKILL.md` con frontmatter, pasos, y verificación |
| Invocación | `/nombre-skill` o automática si la description es buena |
| Ubicación | `~/.claude/skills/<nombre>/SKILL.md` (personal) o `.claude/skills/` (proyecto) |

> Documentación oficial: [Skills — Create your first skill](https://code.claude.com/docs/en/skills#create-your-first-skill)
