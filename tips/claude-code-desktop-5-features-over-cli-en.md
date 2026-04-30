---
date: 2026-02-26
type: tip
title_es: "Claude Code Desktop: 5 funcionalidades por las que valdría la pena dejar el terminal"
title_en: "Claude Code Desktop: 5 Features Worth Leaving the Terminal For"
---
# Quick Tip: Claude Code Desktop: 5 Features Worth Leaving the Terminal For

The terminal will always win for technical work: you're closer to the code, closer to the layer you want to affect. But not everyone wants to get their hands dirty with the terminal. Product Managers, Project Managers, technically capable people who don't live in code — for them, Desktop is the perfect entry point. Same engine as the CLI, with five exclusive capabilities on top.

Result:

```
┌─────────────────────────────────────────────┐
│  Chat  │  Cowork  │  ● Code                 │
├─────────────────────────────────────────────┤
│ Sessions      │  Diff: app.tsx  +12 -1      │
│ ▸ feature-auth│  - const old = getValue()   │
│ ▸ fix-navbar  │  + const r = compute(input) │
│ + New session │  [Accept] [Reject] [Review] │
└─────────────────────────────────────────────┘
```

## The 5 exclusive features

**1. Visual diff review with inline comments**

Claude edits files and a `+12 -1` indicator appears. Click to open the diff view. Click any line to leave a comment. Claude reads your feedback and adjusts the code. `Cmd+Enter` (macOS) or `Ctrl+Enter` (Windows) sends all comments at once.

**2. Parallel sessions with automatic worktrees**

**+ New session** creates an isolated worktree with no flags, no extra terminals. Each session gets its own branch, visible in the sidebar. The CLI requires `claude -w <name>` per terminal — Desktop abstracts it entirely.

**3. Embedded app preview**

A built-in browser shows your running app. Claude starts the dev server, takes screenshots, inspects the DOM, fills out forms, and fixes issues it finds. Configuration lives in `.claude/launch.json`:

```json
{
  "configurations": [{
    "name": "web",
    "runtimeExecutable": "npm",
    "runtimeArgs": ["run", "dev"],
    "port": 3000
  }]
}
```

**4. PR monitoring with auto-fix and auto-merge**

After opening a PR, a CI status bar appears in the session. **Auto-fix**: Claude reads failures and patches them. **Auto-merge**: Claude merges when all checks pass. Requires `gh` CLI installed.

**5. Built-in connectors**

**+** button → **Connectors** to hook up GitHub, Slack, Linear, Notion, and more — no JSON editing. These are MCP servers with a graphical setup flow. In the CLI, configuring an MCP server means editing `~/.claude.json` by hand.

## Reference

| Feature | CLI | Desktop |
|---|---|---|
| Diff review | Not available | Visual with inline comments |
| Parallel sessions | `claude -w <name>` manual | Automatic from sidebar |
| App preview | `--chrome` (beta) | Embedded browser |
| CI monitoring | Not available | Status bar + auto-fix |
| Connectors | Edit JSON manually | Graphical UI |

| Concept | Detail |
|---|---|
| Engine | Same as the CLI — shares CLAUDE.md, hooks, MCP |
| Platforms | macOS and Windows (no Linux) |
| Environments | Local, Remote (Anthropic cloud), SSH |
| Models | Opus, Sonnet, Haiku — locked at session start |

**Related:** [The 6 ways to extend Claude Code](/en/tips/claude-code-skills-hooks-mcp-plugins-comparison) · [Worktrees for parallel tasks](/en/tips/claude-code-worktrees-parallel-tasks)

> Official docs: [Get started with Desktop](https://code.claude.com/docs/en/desktop-quickstart) · [Full reference](https://code.claude.com/docs/en/desktop)

## Requirements

- Pro, Max, Teams, or Enterprise subscription
- macOS or Windows (Linux not supported)
- Git installed (on Windows: [git-scm.com](https://git-scm.com/downloads/win))
