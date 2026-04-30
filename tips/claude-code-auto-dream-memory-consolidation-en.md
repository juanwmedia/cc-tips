---
date: 2026-04-05
type: tip
title_es: "Auto Dream: Claude Code Consolida tu Memoria Mientras Descansas"
title_en: "Auto Dream: Claude Code Consolidates Your Memory While You Rest"
---
Auto memory writes notes. Auto Dream cleans them up. After enough sessions, your memory files accumulate contradictions, stale entries, duplicate observations, and relative dates that no longer make sense. Auto Dream is a background sub-agent that reviews recent session transcripts, extracts what matters, and reorganizes your memory files into something coherent. It runs between sessions without blocking your work.

> **TL;DR** Auto Dream consolidates your memory files automatically. Check `/memory` to see if it's enabled. If you need it on demand, say "consolidate my memory files" in any session. The `/dream` command exists but is still rolling out.

Result:

```
Memory consolidation
51s · reviewing 3 sessions

Status: running

Starting memory consolidation. Let me orient first.

Now let me read all existing memory files and search
recent sessions for new signals.

Let me search for key signals in these sessions
— user corrections, preferences, new projects,
and feedback.
```

## How it works

Auto Dream follows four phases, each with a specific purpose:

### **1. Orient**

Claude scans the memory directory, reads MEMORY.md, and skims existing topic files. This builds a map of everything currently stored before making any changes.

### **2. Gather signal**

The sub-agent searches recent session transcripts (JSONL files) for high-value patterns: user corrections, explicit save requests, recurring themes, and key decisions. It uses narrow search terms rather than reading entire transcripts.

### **3. Consolidate**

New information merges into existing topic files. Critical maintenance happens here:

- Contradicted facts get deleted at their source
- Relative dates convert to absolute ("yesterday" becomes "2026-04-04")
- Overlapping entries merge into one clean note

### **4. Prune and index**

MEMORY.md is updated to stay under 200 lines (~25KB) — the startup load limit. Stale pointers are removed, verbose entries shortened, and contradictions between files resolved.

## Using it

### **Check if auto-dream is enabled**

```
/memory
```

Look for `Auto-dream: on` in the selector. If you see it, consolidation is already running between sessions.

### **Trigger manually**

The `/dream` command is intended as the manual trigger, but it's still rolling out and may return "Unknown skill" on some versions. As a workaround:

```
> Consolidate my memory files
```

This achieves the same result within your current session.

### **When to trigger manually**

After major changes — framework migrations, large refactors, renamed directories — your memory files will contain outdated references. A manual consolidation cleans those up immediately instead of waiting for the next automatic cycle.

## Reference

| Phase | What it does |
|---|---|
| Orient | Reads memory directory, builds map of existing state |
| Gather signal | Searches session transcripts for corrections, decisions, patterns |
| Consolidate | Merges new info, removes contradictions, fixes dates |
| Prune and index | Keeps MEMORY.md under 200 lines, cleans stale pointers |

| Detail | Value |
|---|---|
| Scope | Only writes to memory files — never touches source code |
| Runs | Automatically between sessions; manually via prompt |
| `/dream` | Manual trigger, still rolling out (may not work on all versions) |
| Visibility | Shows as "Memory consolidation" in `/tasks` while running |

**Related:** [Auto memory between sessions](/en/tips/claude-code-auto-memory-between-sessions)

> Official docs: [How Claude remembers your project](https://code.claude.com/docs/en/memory)
