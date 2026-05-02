---
date: 2026-04-29
type: tip
title_es: "/init en Claude Code: mucho más que un CLAUDE.md de plantilla"
title_en: "/init in Claude Code: way more than a CLAUDE.md template"
---

`/init` is one of those built-in commands almost everyone runs once on day one and never again. And they're stuck with the poor mode: a generic CLAUDE.md that Anthropic itself considers deprecated under its current philosophy (*"CLAUDE.md is loaded into every Claude Code session, so it must be concise — only include what Claude would get wrong without it"*).

The new flow goes further: it can also generate the project's first [skills](/en/tips/claude-code-skills-custom-slash-commands) and [hooks](/en/tips/claude-code-hooks-automate-workflow). More importantly, it applies discipline on CLAUDE.md from day one. If your CLAUDE.md is already [full of junk](/en/tips/claude-code-claudemd-project-setup), re-running `/init` with the new flow is the cleanest way to start over.

## How it works internally

When you run `/init`, Claude Code loads one of two prompts depending on `CLAUDE_CODE_NEW_INIT`:

| Mode | Variable | Description | What it generates |
|---|---|---|---|
| Default | (unset) | *"Initialize a new CLAUDE.md file with codebase documentation"* | Basic CLAUDE.md + note about `/plugin` |
| New | `CLAUDE_CODE_NEW_INIT=1` | *"Initialize new CLAUDE.md file(s) and optional skills/hooks with codebase documentation"* | **Minimal** CLAUDE.md + skills (optional) + hooks (optional) |

The new mode is governed by a literal rule in the prompt: *"CLAUDE.md is loaded into every Claude Code session, so it must be concise — only include what Claude would get wrong without it."* That means: don't list `package.json` dependencies, folder structure, or language conventions — Claude infers those.

## How to enable it

For a single session:

```bash
CLAUDE_CODE_NEW_INIT=1 claude
```

Then inside the session:

```bash
/init
```

Permanently in your shell:

```bash
echo 'export CLAUDE_CODE_NEW_INIT=1' >> ~/.zshrc
```

## When to re-run it

`/init` is not "once and forget":

- **Major refactor**: if you moved code to a monorepo, switched frameworks, or introduced new skills, re-init so CLAUDE.md and the hooks reflect the new state.
- **After removing deprecated code**: if your CLAUDE.md describes a module that no longer exists, regenerating is cleaner than patching.
- **Before onboarding**: a clean CLAUDE.md on day one shortens the ramp for new developers.

## Bonus: /init-verifiers

There's a sibling command almost nobody knows about:

```bash
/init-verifiers
```

Generates skills specifically for **automated verification of code changes**. Useful when you want certain checks (linter, specific tests, type validation) to run consistently as auto-invocable skills after each edit.

## Reference

| Command | Use it for |
|---|---|
| `/init` (default) | Basic CLAUDE.md generated from automatic analysis |
| `CLAUDE_CODE_NEW_INIT=1` + `/init` | Minimal CLAUDE.md + skills + hooks |
| `/init-verifiers` | Post-edit verification skills |

> Official docs: [Claude Code commands](https://code.claude.com/docs/en/commands)

