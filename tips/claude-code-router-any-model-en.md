---
date: 2026-05-22
type: tip
title_es: "Claude Code Router: el truco que abarata Claude Code (con el trade-off que nadie cuenta)"
title_en: "Claude Code Router: the trick to cheaper Claude Code (with the trade-off nobody mentions)"
---
> **TL;DR** `npm install -g @musistudio/claude-code-router` puts a local proxy between Claude Code and the model, letting you route requests to DeepSeek, Qwen, Ollama, OpenRouter, or whatever. Configure `~/.claude-code-router/config.json` with your providers and rules (per scenario: `default`, `background`, `think`, `longContext`, `webSearch`), launch with `ccr code`, and switch models on the fly with `/model`. **The honest trade-off nobody mentions**: you keep Claude Code's UX, not Claude. DeepSeek inside Claude Code is still DeepSeek — better than ChatGPT at many tasks, but worse than Sonnet 4.6 at agentic work and reasoning.

More and more searches lead to "claude code free", "claude code ollama", "claude code unlimited". Behind all of them is the same question: can I keep coding with this CLI when my plan runs out, or when the code shouldn't leave my machine? The community's answer — not Anthropic's — is [Claude Code Router](https://github.com/musistudio/claude-code-router), an open-source project with 26k+ stars that intercepts Claude Code's calls and translates them to almost any provider.

It's not magic. It's a proxy that changes `ANTHROPIC_BASE_URL` to point at your machine and rewrites requests to the format of whichever provider you pick. What you keep: the CLI, slash commands, hooks, skills, plugins. What you don't keep: Claude itself.

Result:

```
> ccr code

Claude Code Router running on localhost:3456
Default model: deepseek,deepseek-chat

> /model openrouter,anthropic/claude-sonnet-4-6

Switched to claude-sonnet-4-6 via OpenRouter for this turn

> /model ollama,qwen2.5-coder:14b

Switched to qwen2.5-coder:14b (local) for this turn
```

## Install

```bash
# 1. Claude Code (if you don't have it)
npm install -g @anthropic-ai/claude-code

# 2. The router
npm install -g @musistudio/claude-code-router

# 3. Verify
ccr --version
```

## Minimal config (DeepSeek + Ollama)

Create `~/.claude-code-router/config.json`:

```json
{
  "Providers": [
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/chat/completions",
      "api_key": "sk-...",
      "models": ["deepseek-chat", "deepseek-reasoner"]
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": ["qwen2.5-coder:14b", "llama3.1:8b"]
    }
  ],
  "Router": {
    "default": "deepseek,deepseek-chat",
    "background": "ollama,qwen2.5-coder:14b",
    "think": "deepseek,deepseek-reasoner",
    "longContext": "deepseek,deepseek-chat",
    "webSearch": "deepseek,deepseek-chat"
  }
}
```

The five `Router` keys aren't decoration — they're **distinct scenarios** Claude Code triggers based on the kind of operation:

| Scenario | When it triggers | Recommended model |
|---|---|---|
| `default` | Normal conversation | The cheapest useful one (DeepSeek Chat) |
| `background` | Subagents, parallel tasks | Local (Ollama) — they're cheap and many |
| `think` | `/think`, planning, deep reasoning | The best you have (reasoner / Sonnet via OpenRouter) |
| `longContext` | Long windows (>32k tokens) | A model with a large context window |
| `webSearch` | Web search tool | The most capable for parsing results |

Launch with `ccr code` (instead of `claude`). Hot-reload config: `ccr restart`. There's a UI: `ccr ui`. To swap models mid-conversation: `/model <provider>,<model>`.

## The honest trade-off

What you **won't find** in "Claude Code unlimited" blogs:

- **You keep the UX, not Claude.** DeepSeek-Chat inside Claude Code is still DeepSeek — good for refactors and boilerplate, worse at agentic work, complex tool use, and multi-step reasoning.
- **Some features [need Claude](/en/tips/claude-code-choose-right-model).** Auto mode needs Anthropic's classifier. [`/advisor`](/en/tips/claude-code-advisor-opus-sonnet) calls Opus specifically. The [Figma + Chrome MCP combo with `/goal`](/en/tips/claude-code-figma-chrome-mcp-pixel-perfect) works because Claude handles the agentic loop — swap in a weaker model and it breaks within 3-4 turns.
- **It's a community project.** When Claude Code's API changes (it does, every few weeks), the router can break until `musistudio` patches. This isn't production-critical infrastructure.
- **Privacy depends on the provider.** Ollama → your machine, 100% local. DeepSeek/Qwen → the provider's servers (Chinese in both cases). Decide based on the repo.

## When it IS worth it

- **You ran out of Pro/Max plan** and need to keep going today → switch to DeepSeek for a few hours
- **Sensitive code that can't leave your machine** → route to local Ollama
- **Massive cheap tasks** (rename 200 files, generate boilerplate) → background to a cheap model
- **You live in a region without direct Anthropic billing** → OpenRouter via the router
- **You want to compare models** inside the same flow → swap on the fly with `/model`

## When NOT to use it

- **When you're doing complex agentic work** — [auto mode](/en/tips/claude-code-auto-mode-vs-yolo), [agent teams](/en/tips/claude-code-agent-teams), [subagents](/en/tips/claude-code-subagent-context-loss). Those flows assume Claude-specific capabilities.
- **When your bottleneck is reasoning, not cost.** Paying for Sonnet 4.6 and planning well is cheaper than saving on tokens and rewriting badly.
- **When you're saving tokens, not budget.** If the problem is your context filling up, the answer is [10 habits to save tokens](/en/tips/claude-code-save-tokens-10-habits), not switching models.

## Reference

| Command | What it does |
|---|---|
| `ccr code` | Launches Claude Code pointing at the router |
| `ccr restart` | Reloads config without killing the session |
| `ccr ui` | Opens the router's web UI |
| `ccr model` | Lists models / changes default from the CLI |
| `/model <provider>,<model>` | Swaps model inside Claude Code, on the fly |

| Supported provider | Best for |
|---|---|
| DeepSeek | Cheap chat (`deepseek-chat`) and reasoner (`deepseek-reasoner`) |
| Qwen 3 / Qwen Coder | Strong coder via Alibaba (DashScope) or local Ollama |
| Ollama / LM Studio / vLLM | Local, full privacy, no per-token cost |
| OpenRouter | Gateway to hundreds of models (Claude itself included) |
| GLM (Zhipu) | Bilingual EN/ZH, cheap |

> Official docs: [musistudio/claude-code-router (GitHub)](https://github.com/musistudio/claude-code-router) · [Routing scenarios docs](https://musistudio.github.io/claude-code-router/)

## Requirements

- Node.js 18+
- Claude Code v2.0+
- An API key from your chosen provider (DeepSeek, OpenRouter…) or Ollama running locally
