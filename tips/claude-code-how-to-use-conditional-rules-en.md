---
date: 2026-02-21
type: tip
title_es: "Aplica Reglas Solo a Archivos Específicos con Conditional Rules"
title_en: "Scope Rules to Specific Files with Conditional Rules"
---
# Quick Tip: Scope Rules to Specific Files with Conditional Rules

Claude Code loads all `.claude/rules/*.md` files as project memory — but not every rule applies to every file. Conditional rules use YAML frontmatter with a `paths` field to activate only when Claude works with files matching specific glob patterns. Your API rules stay out of context when you're editing Vue components, and your styling conventions don't load when you're writing backend logic.

Result:

```
.claude/rules/
├── api-endpoints.md      # Only loads for src/api/**/*.ts
├── vue-components.md     # Only loads for src/components/**/*.vue
├── testing.md            # Only loads for tests/**/*.test.ts
└── general.md            # Always loads (no paths frontmatter)
```

## Setup

**1. Create the rules directory**

```bash
mkdir -p .claude/rules
```

**2. Add a conditional rule**

Create `.claude/rules/api-endpoints.md`:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Rules

- All endpoints must include input validation
- Use the standard error response format from src/api/errors.ts
- Return proper HTTP status codes (201 for creation, 204 for deletion)
- Include OpenAPI documentation comments on every handler
```

**3. Add another for a different scope**

Create `.claude/rules/vue-components.md`:

```markdown
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---

# Vue Component Rules

- Use Composition API with <script setup lang="ts">
- Props must be typed with defineProps<T>()
- Emit events with defineEmits<T>()
- Keep templates under 80 lines — extract child components
```

**4. Add an unconditional rule**

Create `.claude/rules/general.md` (no frontmatter):

```markdown
# General Rules

- Use 2-space indentation
- No console.log in production code
- All public functions must have JSDoc comments
```

## Reference

| Feature | Details |
|---|---|
| Location | `.claude/rules/*.md` (project) or `~/.claude/rules/*.md` (personal) |
| Loading | Conditional rules load only when Claude touches matching files |
| Unconditional | Rules without `paths` frontmatter always load |
| Glob patterns | `**/*.ts`, `src/**/*`, `*.{ts,tsx}`, `{src,lib}/**/*.ts` |
| Brace expansion | `*.{ts,tsx}` matches both `.ts` and `.tsx` files |
| Subdirectories | `.claude/rules/frontend/react.md` works — discovery is recursive |
| Symlinks | Supported — share rules across projects with `ln -s` |
| Multiple paths | List multiple patterns under `paths:` to match broader scopes |

> Official docs: [Manage Claude's memory](https://code.claude.com/docs/en/memory)
