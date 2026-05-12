---
date: 2026-05-12
type: tip
title_es: "Claude Code en tu GitHub: revisa PRs, arregla issues y crea código sin abrir la terminal"
title_en: "Claude Code on GitHub: review PRs, fix issues, ship code without opening your terminal"
---

> **TL;DR** Ejecutas `/install-github-app`, el wizard instala la GitHub App de Anthropic, añade `ANTHROPIC_API_KEY` a los secrets del repo y copia un workflow YAML. A partir de ahí, cada vez que menciones `@claude` en un PR o un issue, Claude lee el contexto, propone cambios, abre commits en la rama y responde en el hilo. Por debajo es el Claude Agent SDK corriendo en un runner de GitHub Actions.

Lo que normalmente harías en local — pedirle a Claude que revise el diff de un PR, que arregle el TypeError del dashboard, que implemente lo que pide un issue — pasa ahora dentro de GitHub. Sin clonar, sin abrir la terminal. Una mención `@claude` en un comentario dispara el workflow.

Bajo el capó: la [GitHub App de Anthropic](https://github.com/apps/claude) escucha eventos (`issue_comment`, `pull_request_review_comment`, `issues`) y, si el comentario contiene la trigger phrase, lanza un job en `ubuntu-latest` que ejecuta `anthropics/claude-code-action@v1` con tu API key. Es Claude Code corriendo en cloud con todos sus permisos sobre el repo.

## Lo que ves cuando funciona

En un PR cualquiera escribes:

```
@claude el test SearchBar.spec.tsx está fallando con "Cannot read 'value' of null".
¿Puedes mirar?
```

A los pocos segundos Claude responde con un análisis del fallo, propone una corrección a `SearchBar.vue`, empuja un commit a la rama del PR, y comenta el resumen. Sin que toques nada en local.

## Setup en 5 minutos

**1. Instala la GitHub App.** Desde tu terminal:

```bash
claude
/install-github-app
```

El wizard te guía por: elegir el repo, instalar la App, añadir `ANTHROPIC_API_KEY` como secret, y copiar el workflow YAML por defecto. Necesitas ser **admin del repo**. La App pide permisos de Contents, Issues y Pull requests (read & write).

> El wizard solo cubre cuentas directas de Claude API. Para Bedrock o Vertex AI hay setup OIDC adicional — link a docs al final.

**2. Workflow básico (el que copia el wizard):**

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Eso solo: responde a menciones `@claude` en comentarios. La action auto-detecta si tiene que correr en modo interactivo (responde a la mención) o en modo automation (corre con un prompt prefijado).

**3. Auto-review de cada PR sin mencionar a nadie.** Añade un workflow paralelo:

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Revisa este PR (calidad, correctness, seguridad). Postea los hallazgos como comentarios de review."
          claude_args: "--max-turns 5"
```

`claude_args` admite cualquier flag del CLI de Claude Code (`--model`, `--max-turns`, `--allowedTools`, `--mcp-config`, etc.).

## Los 3 settings que vas a querer tocar

| Parámetro | Para | Cuándo |
|---|---|---|
| `claude_args: --model claude-opus-4-7` | Usar Opus 4.7 en lugar del Sonnet por defecto | PRs complejos donde quieras más razonamiento |
| `claude_args: --max-turns 5` | Limitar iteraciones del agente | Controlar coste — sin esto puede iterar hasta agotar tokens |
| `trigger_phrase: "@bot-review"` | Cambiar la trigger phrase | Para no colisionar con menciones humanas o tener varios workflows |

## CLAUDE.md sigue mandando

El `CLAUDE.md` de la raíz del repo se aplica también a las sesiones de GitHub Actions. Si lo tienes con tus convenciones, estándares de testing y guidelines de review, Claude las aplica en CI igual que en local. Eso convierte el setup en *"Claude que entiende tu codebase"* y no en *"un linter genérico"*. Para repasar [cómo configurar CLAUDE.md](/es/tips/claude-code-claudemd-configurar-proyecto), hay tip propio.

## Coste

Dos vectores. **Tokens API** — facturados a tu cuenta de Anthropic — y **minutos de GitHub Actions** (gratis hasta el límite del plan, pagas si lo excedes). Para controlar el primero: `--max-turns`, prompts específicos, y no disparar workflows en cada `synchronize` si no lo necesitas.

## Combina con

- [Plugins](/es/tips/claude-code-marketplace-plugins-distribucion) — la action puede cargar plugins via `--mcp-config`.
- [Skills](/es/tips/claude-code-skills-comandos-personalizados) — invocables desde el `prompt` del workflow.
- [Subagents](/es/tips/claude-code-crear-agentes-personalizados) — funcionan igual en cloud que en local.
- [Cheat sheet de slash commands](/es/tips/claude-code-slash-commands-cheatsheet) — `/install-github-app` está ahí, junto con los otros 79.

> Documentación oficial: [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
