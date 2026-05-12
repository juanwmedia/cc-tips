---
date: 2026-05-12
type: tip
title_es: "Claude Code en tu GitHub: revisa PRs, arregla issues y crea código sin abrir la terminal"
title_en: "Claude Code on GitHub: review PRs, fix issues, ship code without opening your terminal"
---

> **TL;DR** Run `/install-github-app`, the wizard installs Anthropic's GitHub App, adds `ANTHROPIC_API_KEY` to your repo secrets and drops in a workflow YAML. From there on, every time you mention `@claude` in a PR or issue, Claude reads the context, proposes changes, pushes commits to the branch and replies in-thread. Under the hood it's the Claude Agent SDK running on a GitHub Actions runner.

What you'd normally do locally — ask Claude to review a PR diff, fix a TypeError in the dashboard, implement what an issue asks for — now happens inside GitHub. No cloning, no terminal. A `@claude` mention in a comment fires the workflow.

Under the hood: [Anthropic's GitHub App](https://github.com/apps/claude) listens to events (`issue_comment`, `pull_request_review_comment`, `issues`) and, if the comment contains the trigger phrase, kicks off a job on `ubuntu-latest` that runs `anthropics/claude-code-action@v1` with your API key. It's Claude Code running in the cloud with full permissions over your repo.

## What you see when it works

On any PR you write:

```
@claude the SearchBar.spec.tsx test is failing with "Cannot read 'value' of null".
Can you look at it?
```

A few seconds later Claude replies with an analysis of the failure, proposes a fix to `SearchBar.vue`, pushes a commit to the PR's branch, and posts a summary. Without you touching a thing locally.

## 5-minute setup

**1. Install the GitHub App.** From your terminal:

```bash
claude
/install-github-app
```

The wizard walks you through: picking the repo, installing the App, adding `ANTHROPIC_API_KEY` as a secret, and copying the default workflow YAML. You need to be a **repo admin**. The App requests Contents, Issues, and Pull requests permissions (read & write).

> The wizard only covers direct Claude API accounts. For Bedrock or Vertex AI there's extra OIDC setup — see the docs link below.

**2. The basic workflow** (what the wizard drops in):

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

That's it: responds to `@claude` mentions in comments. The action auto-detects whether to run in interactive mode (responds to mentions) or automation mode (runs with a pre-set prompt).

**3. Auto-review every PR without anyone mentioning Claude.** Add a parallel workflow:

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
          prompt: "Review this PR for code quality, correctness, and security. Post findings as review comments."
          claude_args: "--max-turns 5"
```

`claude_args` accepts any Claude Code CLI flag (`--model`, `--max-turns`, `--allowedTools`, `--mcp-config`, etc.).

## The 3 settings you'll want to tune

| Parameter | For | When |
|---|---|---|
| `claude_args: --model claude-opus-4-7` | Use Opus 4.7 instead of the default Sonnet | Complex PRs where you want more reasoning |
| `claude_args: --max-turns 5` | Cap agent iterations | Cost control — without it Claude can keep iterating until tokens run out |
| `trigger_phrase: "@bot-review"` | Change the trigger phrase | Avoid colliding with human `@claude` mentions, or run multiple workflows |

## CLAUDE.md still rules

The `CLAUDE.md` at your repo root applies to GitHub Actions sessions too. If it has your conventions, testing standards, and review guidelines, Claude applies them in CI the same way it does locally. That's what turns the setup into *"Claude who understands your codebase"* instead of *"a generic linter"*. For a refresher on [configuring CLAUDE.md](/en/tips/claude-code-claudemd-project-setup), there's a dedicated tip.

## Cost

Two vectors. **API tokens** — billed to your Anthropic account — and **GitHub Actions minutes** (free up to your plan limit, paid above). To keep the first in check: `--max-turns`, specific prompts, and don't fire workflows on every `synchronize` if you don't need to.

## Pairs well with

- [Plugins](/en/tips/claude-code-plugin-marketplace-distribution) — the action can load plugins via `--mcp-config`.
- [Skills](/en/tips/claude-code-skills-custom-slash-commands) — invokable from the workflow `prompt`.
- [Subagents](/en/tips/claude-code-create-custom-agents) — work the same in cloud as locally.
- [Slash commands cheat sheet](/en/tips/claude-code-slash-commands-cheat-sheet) — `/install-github-app` lives there along with the other 79.

> Official docs: [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
