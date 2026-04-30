---
date: 2026-02-21
type: tip
title_es: "Aplica Reglas Solo a Archivos Específicos con Conditional Rules"
title_en: "Scope Rules to Specific Files with Conditional Rules"
---
# Quick Tip: Aplica Reglas Solo a Archivos Específicos con Conditional Rules

Claude Code carga todos los archivos `.claude/rules/*.md` como memoria de proyecto — pero no todas las reglas aplican a todos los archivos. Las conditional rules usan frontmatter YAML con un campo `paths` para activarse solo cuando Claude trabaja con archivos que coinciden con patrones glob. Tus reglas de API no ocupan contexto cuando editas componentes Vue, y tus convenciones de estilos no se cargan cuando escribes lógica de backend.

Resultado:

```
.claude/rules/
├── api-endpoints.md      # Solo carga para src/api/**/*.ts
├── vue-components.md     # Solo carga para src/components/**/*.vue
├── testing.md            # Solo carga para tests/**/*.test.ts
└── general.md            # Siempre carga (sin frontmatter paths)
```

## Setup

**1. Crea el directorio de rules**

```bash
mkdir -p .claude/rules
```

**2. Crea una regla condicional**

Crea `.claude/rules/api-endpoints.md`:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Rules

- Todos los endpoints deben incluir validación de input
- Usa el formato de error estándar de src/api/errors.ts
- Devuelve códigos HTTP apropiados (201 para creación, 204 para eliminación)
- Incluye comentarios de documentación OpenAPI en cada handler
```

**3. Añade otra para un ámbito distinto**

Crea `.claude/rules/vue-components.md`:

```markdown
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---

# Vue Component Rules

- Usa Composition API con <script setup lang="ts">
- Los props deben tiparse con defineProps<T>()
- Emite eventos con defineEmits<T>()
- Mantén los templates por debajo de 80 líneas — extrae componentes hijos
```

**4. Añade una regla incondicional**

Crea `.claude/rules/general.md` (sin frontmatter):

```markdown
# General Rules

- Indentación de 2 espacios
- Sin console.log en código de producción
- Todas las funciones públicas deben tener comentarios JSDoc
```

## Referencia

| Característica | Detalles |
|---|---|
| Ubicación | `.claude/rules/*.md` (proyecto) o `~/.claude/rules/*.md` (personal) |
| Carga | Las reglas condicionales solo cargan cuando Claude toca archivos que coinciden |
| Incondicional | Las reglas sin frontmatter `paths` cargan siempre |
| Patrones glob | `**/*.ts`, `src/**/*`, `*.{ts,tsx}`, `{src,lib}/**/*.ts` |
| Brace expansion | `*.{ts,tsx}` coincide con archivos `.ts` y `.tsx` |
| Subdirectorios | `.claude/rules/frontend/react.md` funciona — la búsqueda es recursiva |
| Symlinks | Soportados — comparte reglas entre proyectos con `ln -s` |
| Múltiples paths | Lista varios patrones bajo `paths:` para ámbitos más amplios |

> Documentación oficial: [Manage Claude's memory](https://code.claude.com/docs/en/memory)
