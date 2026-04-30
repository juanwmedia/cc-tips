---
date: 2026-03-22
type: tip
title_es: "Plugins en Claude Code: no es nada nuevo, es empaquetar lo que ya sabes"
title_en: "Claude Code Plugins: Nothing New — Just Packaging What You Already Know"
---
# Quick Tip: Claude Code Plugins: Nothing New — Just Packaging What You Already Know

> **TL;DR** A Claude Code plugin isn't a new technology. It's a directory that bundles [skills](/en/writing/claude-code-skills-custom-workflows), [subagents](/en/writing/claude-code-subagents-guide-ai), [hooks](/en/writing/claude-code-hooks-practical-guide), MCP servers, and settings — everything you already know — into an installable, shareable format with a single command.

If you see "plugins" and think "another thing to learn," relax. There's no new API, no new syntax, no new concept. A plugin is literally your `.claude/` directory packaged up: the same skills, the same agents, the same hooks. The difference is you can now share it with your team or the community via `/plugin install`.

Think of it as a `package.json` for Claude Code configuration: a manifest declaring what's inside and a directory structure that Claude Code knows how to read.

Result — a plugin's structure:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest: name, version, description
├── skills/
│   └── code-review/
│       └── SKILL.md          # Skill with its prompt
├── agents/
│   └── reviewer.md           # Custom subagent
├── hooks/
│   └── hooks.json            # Lifecycle hooks
├── .mcp.json                 # MCP servers
└── settings.json             # Default settings
```

## How to use it

### **1. Install an existing plugin**

```
/plugin install code-review@claude-plugins-official
```

Anthropic's official marketplace is `claude-plugins-official`. Teams can create their own.

### **2. Create a plugin from scratch**

```bash
mkdir -p my-plugin/.claude-plugin
```

```json
// my-plugin/.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "My team workflows packaged up",
  "version": "1.0.0"
}
```

Add skills in `skills/`, agents in `agents/`, hooks in `hooks/hooks.json`. Same syntax you already use in `.claude/`.

### **3. Test locally**

```bash
claude --plugin-dir ./my-plugin
```

Skills appear namespaced: `/my-plugin:skill-name`.

### **4. Convert existing configuration to a plugin**

If you already have skills and hooks in `.claude/`, it's copy and paste:

```bash
cp -r .claude/commands my-plugin/
cp -r .claude/agents my-plugin/
cp -r .claude/skills my-plugin/
```

## Reference

| Component | Plugin location | Standalone equivalent |
|---|---|---|
| Skills | `skills/` | `.claude/skills/` |
| Subagents | `agents/` | `.claude/agents/` |
| Hooks | `hooks/hooks.json` | `settings.json` → `hooks` |
| MCP servers | `.mcp.json` | Project `.mcp.json` |
| Settings | `settings.json` | `.claude/settings.json` |
| Manifest | `.claude-plugin/plugin.json` | Doesn't exist — this is the new part |

| Aspect | Detail |
|---|---|
| Install | `/plugin install name@marketplace` |
| Test locally | `claude --plugin-dir ./path` |
| Reload | `/reload-plugins` (no restart needed) |
| Namespace | `/plugin-name:skill` |
| Versioning | Semver in `plugin.json` |

> Official docs: [Create plugins](https://code.claude.com/docs/en/plugins)
