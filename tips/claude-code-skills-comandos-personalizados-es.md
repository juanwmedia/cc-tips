---
date: 2026-02-09
type: tip
title_es: "Crea Comandos Reutilizables con Skills en Claude Code"
title_en: "Create Reusable Commands with Skills in Claude Code"
---
# Quick Tip: Crea Comandos Reutilizables con Skills en Claude Code

Las skills son archivos markdown con instrucciones que Claude Code ejecuta como slash commands. Creas un archivo `SKILL.md` en una carpeta, y lo invocas con `/nombre-skill`. El proceso sigue siendo conversacional: puedes intervenir, corregir y redirigir mientras Claude ejecuta los pasos.

No es un script ciego. Es una conversación guiada con pasos predecibles. Este mismo tip se ha generado con una skill.

Resultado:

```
/review-component src/components/SearchBar.vue

Reviewing SearchBar.vue against 5 criteria...

| Criterio        | Severidad | Hallazgo                          |
|-----------------|-----------|-----------------------------------|
| Estructura      | Baja      | Lógica y template bien separados  |
| Props           | Media     | Falta valor por defecto en query  |
| Accesibilidad   | Alta      | Sin role="search" en el form      |
```

## Setup

**1. Crea el directorio de la skill**

```bash
mkdir -p ~/.claude/skills/review-component
```

**2. Escribe el SKILL.md**

```yaml
---
name: review-component
description: Revisa un componente frontend contra criterios de calidad.
argument-hint: [ruta-al-componente]
---

Revisa el componente en $ARGUMENTS contra estos criterios:

1. **Estructura**: ¿Separación clara de lógica, template y estilos?
2. **Props**: ¿Tipadas correctamente? ¿Valores por defecto?
3. **Accesibilidad**: ¿Roles ARIA, labels, navegación por teclado?

Presenta hallazgos en tabla con columna de severidad.
```

**3. Invócalo**

```bash
/review-component src/components/SearchBar.vue
```

Claude aplica siempre los mismos criterios, en el mismo orden, con el mismo formato de output.

## Referencia

| Campo | Qué hace |
|---|---|
| `name` | Nombre del slash command (solo minúsculas, números, guiones) |
| `description` | Cuándo usar la skill. Claude lo usa para decidir si cargarla automáticamente |
| `argument-hint` | Pista en el autocompletado (`[issue-number]`, `[ruta]`) |
| `disable-model-invocation` | `true` para que solo tú puedas invocarla |
| `context` | `fork` para ejecutar en un subagente aislado |
| `$ARGUMENTS` | Se reemplaza por lo que escribas después del comando |

## Dónde guardar las skills

| Ubicación | Ruta | Alcance |
|---|---|---|
| Personal | `~/.claude/skills/<nombre>/SKILL.md` | Todos tus proyectos |
| Proyecto | `.claude/skills/<nombre>/SKILL.md` | Solo este proyecto |

Skills personales son las más prácticas para empezar. Funcionan en cualquier proyecto sin configuración adicional.

> **Consejo:** Empieza con las instrucciones que copias y pegas siempre. Mételas en un `SKILL.md`. Eso es tu primera skill. Después puedes añadir argumentos, fork a subagentes, contexto dinámico — pero el primer paso es ese archivo markdown.

Para una guía completa con patrones avanzados, argumentos posicionales, fork a subagentes e inyección de contexto dinámico, consulta el [artículo completo sobre skills](/es/articulos/claude-code-skills-flujos-trabajo-personalizados).

> Documentación oficial: [Extender Claude con skills](https://code.claude.com/docs/es/skills)
