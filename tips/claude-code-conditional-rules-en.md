---
date: 2026-06-14
type: tip
title_es: "Reglas condicionales en Claude Code: que tu CLAUDE.md no cargue entero en cada sesión"
title_en: "Conditional rules in Claude Code: stop loading your whole CLAUDE.md every session"
---

> **TL;DR** Split your CLAUDE.md into files inside `.claude/rules/` and give them a `paths:` frontmatter with globs. Each rule **only enters context when Claude touches files matching** its pattern. Your API rules don't take up space when you're editing Vue components, and vice versa. Rules without `paths` always load. It's the same principle as skills: the expensive part only when it's needed.

Your CLAUDE.md grows, and all of it loads every session, no matter how much of each part you actually use. Your endpoint rules ride along in context even when you spend the afternoon in the frontend. There's a way to make each rule show up **only when it matters**, and it lives in a folder a lot of people don't know exists.

Result:

```
.claude/rules/
├── api-endpoints.md      # only loads for src/api/**/*.ts
├── vue-components.md     # only loads for src/components/**/*.vue
├── testing.md            # only loads for tests/**/*.test.ts
└── general.md            # always loads (no paths frontmatter)
```

## How it works

Claude Code discovers every `.md` inside `.claude/rules/` (recursively, so you can nest them in subfolders) and loads them as project memory, with the same priority as `.claude/CLAUDE.md`. The frontmatter is what makes the difference:

- **With `paths:`** (a list of globs): the rule is **conditional**. It only applies when Claude works with files matching the pattern. It doesn't load every turn, but when Claude reads a matching file.
- **Without `paths:`**: it always loads, like another chunk of your CLAUDE.md.

## Setup

**1. Create a conditional rule**

`.claude/rules/api-endpoints.md`:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API rules

- Every endpoint validates input before processing.
- Use the error format from src/api/errors.ts.
- Correct HTTP status codes (201 on create, 204 on delete).
```

**2. Another for a different scope**

`.claude/rules/vue-components.md`:

```markdown
---
paths:
  - "src/components/**/*.vue"
  - "src/pages/**/*.vue"
---

# Vue component rules

- Composition API with <script setup lang="ts">.
- Props typed with defineProps<T>().
- Keep templates under 80 lines; extract children.
```

**3. An unconditional one, for everything**

`.claude/rules/general.md` (no frontmatter): 2-space indentation, no console.log in production, JSDoc on public functions.

## Glob patterns you can use

| Pattern | Matches |
|---|---|
| `**/*.ts` | Every `.ts` in any folder |
| `src/**/*` | Everything under `src/` |
| `src/components/*.tsx` | Components in one specific folder |
| `**/*.{ts,tsx}` | `.ts` and `.tsx` (brace expansion) |

You can list several patterns under `paths:` to widen the scope.

## Details that help

- **Symlinks supported.** Keep a shared rule set and link it into multiple projects: `ln -s ~/shared-rules .claude/rules/shared`.
- **User-level rules.** `~/.claude/rules/*.md` apply to all your projects; project rules take higher priority.
- **Rule or skill?** If the instruction is for a specific task you don't need in context all the time, prefer a [skill](/en/tips/claude-code-skills-custom-slash-commands): it loads only when you invoke it. Conditional rules load when you touch matching files.

## Where it fits

- It's the surgical version of your [project CLAUDE.md](/en/tips/claude-code-claudemd-project-setup): instead of one file that keeps growing, rules scoped by area.
- Same "load only what's needed" idea as [Tool Search for MCP](/en/tips/claude-code-mcp-tool-search): the expensive part is deferred.
- How much each thing weighs in your window: [when each feature loads](/en/tips/claude-code-when-features-load-context).

> Official docs: [Manage Claude's memory — Organize rules with `.claude/rules/`](https://code.claude.com/docs/en/memory)
