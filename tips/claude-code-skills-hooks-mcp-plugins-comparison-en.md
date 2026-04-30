---
date: 2026-02-21
type: tip
title_es: "Los 6 mecanismos de extensión de Claude Code que todos confunden"
title_en: "The 6 Extension Points in Claude Code Everyone Confuses"
---
# Quick Tip: The 6 Extension Points in Claude Code Everyone Confuses

Claude Code offers six different ways to extend its behavior: Skills, Hooks, MCP, Sub-agents, Agent Teams, and Plugins. They solve different problems, but their boundaries blur quickly. This tip gives you a mental model to tell them apart.

The core distinction: each one answers a different question.

```
What should Claude do?                              → Skills
What can Claude access?                             → MCP
Who does the work?                                  → Sub-agents
Who does the work, collaboratively?                 → Agent Teams
When should something happen automatically?         → Hooks
How do you package and share all of the above?      → Plugins
```

## The 6 mechanisms

**1. Skills — What Claude should do**

Markdown files with instructions that Claude follows as slash commands or auto-activates when relevant. Reusable prompts with structure: arguments, frontmatter, subagent forking.

```bash
~/.claude/skills/review/SKILL.md → /review src/App.tsx
```

**2. MCP — What Claude can access**

Model Context Protocol connects Claude to external tools: databases, APIs, GitHub, Notion. MCP doesn't tell Claude what to do — it gives Claude hands to reach beyond its sandbox.

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**3. Sub-agents — Who does the work**

Separate Claude instances that handle tasks in isolation. Each gets its own context window, tools, and permissions. They work independently and report results back.

```
"Use the code-reviewer subagent to check the auth module"
→ Subagent works independently → Returns summary
```

**4. Agent Teams — Who does the work, together** *(experimental)*

Multiple Claude instances working as a coordinated team. Unlike sub-agents, teammates message each other, share a task list, and challenge each other's findings.

```
"Create a team: one on security, one on performance, one on tests"
→ 3 independent sessions → Cross-team discussion → Synthesis
```

**5. Hooks — When things happen automatically**

Shell commands triggered at specific lifecycle points: before a tool runs, after a file is edited, when a session starts. No AI involved — pure automation.

```json
{ "PostToolUse": [{ "matcher": "Write", "hooks": [{ "type": "command", "command": "npm run lint" }] }] }
```

**6. Plugins — How you share everything**

Distributable packages that bundle skills, agents, hooks, and MCP servers into an installable unit. Think npm packages for Claude Code extensions.

```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/        ← reusable skills
├── agents/        ← custom subagents
├── hooks/         ← lifecycle automation
└── .mcp.json      ← external tool connections
```

## Comparison

| Mechanism | Question it answers | Defined in | AI involved? |
|---|---|---|---|
| Skills | What to do | `SKILL.md` (markdown) | Yes — Claude follows them |
| MCP | What to access | `.mcp.json` / CLI config | No — protocol bridge |
| Sub-agents | Who works | `.claude/agents/` (markdown) | Yes — separate instance |
| Agent Teams | Who collaborates | Natural language | Yes — multiple instances |
| Hooks | When to automate | `settings.json` (JSON) | No — shell commands |
| Plugins | How to distribute | `.claude-plugin/` (package) | No — packaging format |

> **Tip:** Most people only need Skills and MCP. Add hooks when you want automation, sub-agents when context window pressure hits, and plugins when you need to share. Agent Teams are experimental — explore them when sub-agents aren't enough.

For a deep dive into Skills with advanced patterns, see the [full Skills article](/en/writing/claude-code-skills-custom-workflows).

> Official docs: [Skills](https://code.claude.com/docs/en/skills) · [MCP](https://code.claude.com/docs/en/mcp) · [Sub-agents](https://code.claude.com/docs/en/sub-agents) · [Agent Teams](https://code.claude.com/docs/en/agent-teams) · [Hooks](https://code.claude.com/docs/en/hooks) · [Plugins](https://code.claude.com/docs/en/plugins)
