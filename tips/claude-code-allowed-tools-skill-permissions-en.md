---
date: 2026-02-21
type: tip
title_es: "Automatiza los permisos de tus skills con allowed-tools"
title_en: "Automate Skill Permissions with allowed-tools"
---
# Quick Tip: Automate Skill Permissions with allowed-tools

When a skill orchestrates multiple tools — SSH connections, web searches, external APIs, Git — Claude Code asks for approval on each one. For content creation skills, that means dozens of confirmation prompts per run. The `allowed-tools` field in the frontmatter grants automatic approval only for the tools you specify: selective freedom, not blanket access.

The most practical approach is to discover it backwards: run the skill manually a few times, approve each tool by hand, note the pattern. After 2-3 runs you'll know exactly what it needs. That's when you formalize it in the frontmatter.

Result:

```yaml
---
name: publish-content
description: Generate and publish content to production
allowed-tools: Read, Write, Bash(ssh *), Bash(git *), mcp__notion__notion-fetch
---
```

## Setup

**1. Run the skill without allowed-tools**

Each time Claude asks for permission, note two things: the tool name and the exact command. After a few runs you'll have the complete list.

**2. Add allowed-tools to the frontmatter**

```yaml
---
name: publish-article
description: Generate and publish a blog article
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(ssh *), Bash(mv *), Bash(git *), mcp__notion__notion-create-pages, mcp__notion__notion-fetch
---
```

The syntax follows three patterns:

- **Native tools**: direct name — `Read`, `Write`, `WebSearch`
- **Bash commands**: `Bash(pattern *)` — the `*` accepts any argument after the pattern
- **MCP tools**: full tool name — `mcp__server__tool-name`

**3. Verify**

Invoke the skill. Listed tools run without confirmation. Anything not in the list still requires approval — that's the control you keep.

## Reference

| Pattern | Allows |
|---|---|
| `Read` | Read any file |
| `Bash(ssh *)` | Any SSH command |
| `Bash(git *)` | Any Git operation |
| `Bash(npm run *)` | Only npm scripts |
| `WebSearch` | Web searches |
| `mcp__notion__notion-fetch` | Only Notion fetch tool |

> Official docs: [Extend Claude with skills](https://code.claude.com/docs/en/skills#restrict-tool-access)
