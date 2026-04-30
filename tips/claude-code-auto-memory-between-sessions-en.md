---
date: 2026-03-04
type: tip
title_es: "¿Sabías que Claude Code recuerda entre conversaciones?"
title_en: "Did You Know Claude Code Remembers Between Conversations?"
---
# Quick Tip: Did You Know Claude Code Remembers Between Conversations?

Claude Code has a feature called **auto memory**: while you work, Claude writes notes about your project to a local directory and reads them at the start of every new session. It's not native model memory — it's a file-based system that automatically injects context.

The effect is surprisingly useful: Claude "remembers" your project's specific build commands, debugging patterns it discovered, architecture decisions you explained to it — from last week or three weeks ago.

> **TL;DR** The `~/.claude/projects/<project>/memory/` folder is Claude's persistent brain. Every session, it reads the first 200 lines of `MEMORY.md`. What it writes today, it knows next time.

Example `~/.claude/projects/<project>/memory/MEMORY.md`:

```markdown
# Memory

## Build commands
- `npm run build:staging` auto-loads staging env vars — no .env.staging needed
- Deploy takes ~4 min because it regenerates responsive images

## Debugging patterns
- CORS errors in local are always the Vite proxy, never the backend
- Payment test fails intermittently — known race condition, ticket #892

## Architecture decisions
- SQLite in production — single server, no connection pooling needed
- Translations live in `/lang/`, not `/locales/` — legacy from the original project
```

## Managing memory

### **1. See what Claude remembers**

```bash
/memory
```

Lists all files loaded into the session: `CLAUDE.md` files, rules, and auto memory files. Lets you open any file directly in your editor.

### **2. Edit the notes**

Memory files are plain markdown. Correct wrong information, add context Claude didn't capture, or delete stale entries:

```bash
open ~/.claude/projects/$(basename $(pwd))/memory/MEMORY.md
```

### **3. Disable it if you don't want it**

```json
{
  "autoMemoryEnabled": false
}
```

Also available as an environment variable: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

## Reference

| | `CLAUDE.md` | Auto memory |
|---|---|---|
| Written by | You | Claude |
| Contains | Instructions and rules | Learnings and patterns |
| Shared via git | Yes | No — local, per machine |
| Load limit | No limit | First 200 lines of `MEMORY.md` |

> Official docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)
