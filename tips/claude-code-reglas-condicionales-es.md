---
date: 2026-06-14
type: tip
title_es: "Reglas condicionales en Claude Code: que tu CLAUDE.md no cargue entero en cada sesión"
title_en: "Conditional rules in Claude Code: stop loading your whole CLAUDE.md every session"
---

> **TL;DR** Parte tu CLAUDE.md en archivos dentro de `.claude/rules/` y ponles un frontmatter `paths:` con globs. Cada regla **solo entra en contexto cuando Claude toca archivos que casan** con su patrón. Tus normas de API no ocupan sitio cuando editas componentes Vue, y al revés. Las reglas sin `paths` se cargan siempre. Es el mismo principio que las skills: lo caro solo cuando hace falta.

Tu CLAUDE.md crece, y todo él se carga en cada sesión, gastes lo que gastes de cada parte. Las normas de tus endpoints viajan en el contexto aunque te pases la tarde en el frontend. Hay una forma de que cada regla aparezca **solo cuando importa**, y vive en una carpeta que mucha gente no sabe que existe.

Resultado:

```
.claude/rules/
├── api-endpoints.md      # solo carga para src/api/**/*.ts
├── vue-components.md     # solo carga para src/components/**/*.vue
├── testing.md            # solo carga para tests/**/*.test.ts
└── general.md            # siempre carga (sin frontmatter paths)
```

## Cómo funciona

Claude Code descubre todos los `.md` dentro de `.claude/rules/` (de forma recursiva, así que puedes meterlos en subcarpetas) y los carga como memoria de proyecto, con la misma prioridad que `.claude/CLAUDE.md`. La diferencia la marca el frontmatter:

- **Con `paths:`** (lista de globs): la regla es **condicional**. Solo se aplica cuando Claude trabaja con archivos que casan con el patrón. No se carga en cada turno, sino cuando lee un archivo que encaja.
- **Sin `paths:`**: se carga siempre, como un trozo más de tu CLAUDE.md.

## Setup

**1. Crea una regla condicional**

`.claude/rules/api-endpoints.md`:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Reglas de API

- Todo endpoint valida el input antes de procesar.
- Usa el formato de error de src/api/errors.ts.
- Códigos HTTP correctos (201 al crear, 204 al borrar).
```

**2. Otra para un ámbito distinto**

`.claude/rules/vue-components.md`:

```markdown
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---

# Reglas de componentes Vue

- Composition API con <script setup lang="ts">.
- Props tipadas con defineProps<T>().
- Templates por debajo de 80 líneas; extrae hijos.
```

**3. Una incondicional, para todo**

`.claude/rules/general.md` (sin frontmatter): indentación de 2 espacios, nada de console.log en producción, JSDoc en funciones públicas.

## Patrones glob que puedes usar

| Patrón | Casa con |
|---|---|
| `**/*.ts` | Todos los `.ts` en cualquier carpeta |
| `src/**/*` | Todo lo que cuelga de `src/` |
| `src/components/*.tsx` | Componentes en una carpeta concreta |
| `**/*.{ts,tsx}` | `.ts` y `.tsx` (brace expansion) |

Puedes listar varios patrones bajo `paths:` para ampliar el ámbito.

## Detalles que ayudan

- **Symlinks soportados.** Mantén un set de reglas compartido y enlázalo en varios proyectos: `ln -s ~/reglas-compartidas .claude/rules/shared`.
- **Reglas de usuario.** `~/.claude/rules/*.md` aplican a todos tus proyectos; las de proyecto tienen más prioridad.
- **¿Regla o skill?** Si la instrucción es de una tarea concreta que no necesitas en contexto siempre, mejor una [skill](/es/tips/claude-code-skills-comandos-personalizados): carga solo cuando la invocas. Las reglas condicionales cargan cuando tocas archivos que casan.

## Dónde encaja

- Es la versión quirúrgica de tu [CLAUDE.md de proyecto](/es/tips/claude-code-claudemd-configurar-proyecto): en vez de un archivo que crece, normas por ámbito.
- Misma idea de "cargar solo lo que hace falta" que [Tool Search en los MCP](/es/tips/claude-code-mcp-servidores-contexto): lo caro va diferido.
- Cuánto pesa cada cosa en tu ventana: [cuándo se carga cada feature](/es/tips/claude-code-cuando-se-cargan-features-contexto).

> Documentación oficial: [Manage Claude's memory — Organize rules with `.claude/rules/`](https://code.claude.com/docs/en/memory)
