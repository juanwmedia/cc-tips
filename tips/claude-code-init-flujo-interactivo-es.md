---
date: 2026-04-29
type: tip
title_es: "/init en Claude Code: mucho más que un CLAUDE.md de plantilla"
title_en: "/init in Claude Code: way more than a CLAUDE.md template"
---

`/init` es uno de esos comandos built-in que casi todo el mundo ejecuta una vez el primer día y nunca más. Y se quedan con el modo pobre: un CLAUDE.md genérico que Anthropic ya considera deprecated en su filosofía actual ("CLAUDE.md is loaded into every Claude Code session, so it must be concise — only include what Claude would get wrong without it").

El flujo nuevo va más allá: te puede generar también las primeras [skills](/es/tips/claude-code-skills-comandos-personalizados) del proyecto y [hooks](/es/tips/claude-code-hooks-automatizar-flujo-trabajo) básicos. Y lo importante: aplica disciplina en CLAUDE.md desde el primer momento. Si ya tienes uno y [está lleno de basura](/es/tips/claude-code-claudemd-configurar-proyecto), re-ejecutar `/init` con el flujo nuevo es la forma más limpia de empezar de cero.

## Cómo funciona internamente

Cuando ejecutas `/init`, Claude Code carga uno de dos prompts según la variable `CLAUDE_CODE_NEW_INIT`:

| Modo | Variable | Descripción | Qué genera |
|---|---|---|---|
| Default | (no definida) | *"Initialize a new CLAUDE.md file with codebase documentation"* | CLAUDE.md básico + nota sobre `/plugin` |
| Nuevo | `CLAUDE_CODE_NEW_INIT=1` | *"Initialize new CLAUDE.md file(s) and optional skills/hooks with codebase documentation"* | CLAUDE.md **mínimo** + skills (opcional) + hooks (opcional) |

El modo nuevo se gobierna por la regla literal del prompt: *"CLAUDE.md is loaded into every Claude Code session, so it must be concise — only include what Claude would get wrong without it."* Es decir: nada de listar dependencias del `package.json`, estructura de carpetas, o convenciones del lenguaje — Claude las infiere solo.

## Cómo lo activas

Solo para una sesión:

```bash
CLAUDE_CODE_NEW_INIT=1 claude
```

Y dentro de la sesión:

```bash
/init
```

Permanentemente en tu shell:

```bash
echo 'export CLAUDE_CODE_NEW_INIT=1' >> ~/.zshrc
```

## Cuándo re-ejecutarlo

`/init` no es "una vez y olvidar":

- **Refactor mayor**: si moviste código a un monorepo, cambiaste de framework o introdujiste skills nuevas, re-init para que CLAUDE.md y los hooks reflejen el nuevo estado.
- **Tras eliminar deprecated**: si tu CLAUDE.md describe un módulo que ya no existe, mejor regenerar que parchear.
- **Antes de onboarding**: el primer día de un nuevo developer, un CLAUDE.md limpio acelera la curva.

## Bonus: /init-verifiers

Existe un comando hermano que casi nadie conoce:

```bash
/init-verifiers
```

Genera skills específicos para **verificación automatizada de cambios de código**. Útil si quieres que ciertas comprobaciones (linter, tests específicos, validación de tipos) se ejecuten consistentemente como skills auto-invocables después de cada edit.

## Referencia

| Comando | Para qué |
|---|---|
| `/init` (default) | CLAUDE.md básico generado por análisis automático |
| `CLAUDE_CODE_NEW_INIT=1` + `/init` | CLAUDE.md mínimo + skills + hooks |
| `/init-verifiers` | Skills de verificación post-edit |

> Documentación oficial: [Comandos de Claude Code](https://code.claude.com/docs/en/commands)

