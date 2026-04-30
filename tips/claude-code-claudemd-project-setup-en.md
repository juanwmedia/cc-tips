---
date: 2026-03-03
type: tip
title_es: "Tu CLAUDE.md está lleno de basura, así es como puedes arreglarlo"
title_en: "Your CLAUDE.md Is Full of Junk — Here's How to Fix It"
---
# Quick Tip: Your CLAUDE.md Is Full of Junk — Here's How to Fix It

CLAUDE.md is the file Claude Code reads at the start of every session to understand your project. It lives at the repo root and is shared with your team via git. The problem: most CLAUDE.md files are packed with information Claude can already infer on its own — dependencies from `package.json`, folder structure, standard language conventions. Every unnecessary line consumes context and dilutes the instructions that actually matter.

The rule: if Claude can figure it out by reading the code, don't put it in CLAUDE.md. Document the why, not the what. Business decisions, team dynamics, the reasoning behind an architecture choice — that's what can't be inferred from a `composer.json`.

> **TL;DR** Run `/init` to generate a base CLAUDE.md, then strip everything that's auto-inferrable. Keep only what Claude can't discover on its own: team decisions, non-standard conventions, and the why behind every rule.

Result:

```markdown
# CLAUDE.md

## Business rules
- All prices must include tax for ES/EU customers — legal requirement since 2024
- Never delete user data; soft-delete only — compliance with our data retention policy

## Architecture decisions
- We chose SQLite over Postgres for the public site — single-server deployment, no need for connection pooling
- API responses are cached 5 min at CDN level — product decision to reduce costs, not a technical limitation

## Team conventions
- PRs require at least 1 review from @frontend-team before merging
- Feature branches use `feat/TICKET-description` format — matches Linear integration

## Non-obvious commands
- `npm run seed:staging` — resets staging DB with anonymized production data
- `./scripts/deploy-preview.sh` — deploys to Vercel preview, needs VERCEL_TOKEN in .env
```

## Setup

### **1. Generate the base file**

```bash
claude
# Inside the session:
/init
```

Claude analyzes the codebase — detects build system, frameworks, tests — and generates an initial CLAUDE.md. If one already exists, it suggests improvements instead of overwriting.

### **2. Strip what's redundant**

Review the generated file and remove:

- Dependencies already in `package.json`, `composer.json`, `Cargo.toml`
- Folder structure (Claude sees it directly)
- Standard language conventions ("use camelCase in JavaScript")
- Public API explanations (link to docs instead of copying them)

### **3. Add what Claude can't infer**

- Business decisions and their reasoning
- Team conventions that differ from the standard
- Internal scripts with usage context
- Legal or compliance constraints
- Workflows not documented in code

### **4. Import external files (optional)**

Use `@path/file` to modularize without bloating the main file:

```markdown
# CLAUDE.md
@docs/architecture-decisions.md
@docs/team-conventions.md
```

Maximum 5 levels of imports. Relative paths resolve from the file containing the import.

## Reference

| File | Scope | Shared with | When to use |
|---|---|---|---|
| `./CLAUDE.md` | Project | Team (via git) | Shared instructions |
| `./.claude/CLAUDE.md` | Project | Team (via git) | Alternative to above |
| `./CLAUDE.local.md` | Project | Just you | Personal project preferences |
| `~/.claude/CLAUDE.md` | Global | Just you | Preferences across all projects |
| `.claude/rules/*.md` | Project | Team (via git) | Modular rules by topic or path |

## Best practices

| Do | Don't |
|---|---|
| Document the why behind every rule | List project dependencies |
| Concrete, verifiable instructions | "Write clean code" |
| Keep under 200 lines | Copy API documentation |
| Review periodically | Leave outdated instructions |
| Use `@imports` to modularize | One 500-line file |

> Official docs: [Memory and CLAUDE.md](https://code.claude.com/docs/en/memory)
