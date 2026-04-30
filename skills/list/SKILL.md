---
name: list
description: List all Claude Code tips grouped by topic with read/unread markers. Optional topic filter.
disable-model-invocation: true
model: haiku
allowed-tools: Read, Bash(jq *), Bash(test *)
argument-hint: "[topic]"
---

# /cc-tips:list

Render the tip manifest as a table for the user. Optional topic filter via `$ARGUMENTS`.

## Procedure

1. Read `${CLAUDE_PLUGIN_ROOT}/manifest.json`.
2. Read `${CLAUDE_PLUGIN_DATA}/progress.json` to get `read_tips`. If missing, treat as empty array.
3. If `$ARGUMENTS` is non-empty, treat it as a topic filter:
   - Validate against the 11 known topics: `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.
   - If invalid, respond: `Unknown topic '$ARGUMENTS'. Valid topics: skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals.` Stop.
   - Otherwise, filter manifest entries to that topic.
4. Detect the user's working language from recent prompts. Pick `lang = "es"` (Spanish) or `lang = "en"` (otherwise).
5. Group entries by topic. For each non-empty topic, render a markdown section in the canonical topic order: `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.

Format per topic:

```
## <Topic title>

| ID | Title | Status |
|---|---|---|
| 3 | Recover earlier code state with /checkpoints | ✓ read |
| 7 | Resume long-running sessions across machines | unread |
```

- Use `title_es` if `lang = "es"`, else `title_en`.
- Tips whose id is in `read_tips`: `✓ read`. Otherwise: `unread`.
- Keep technical terms in English regardless of `lang`.

6. Append a one-line update reminder (in the user's language):

> _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update cc-tips` periodically._

## Notes

- This skill is read-only. It does NOT mark anything as read. Users must run `/cc-tips:open <N>` to mark a tip read.
- If the manifest is empty (shouldn't happen post-install), respond with `No tips available yet. Check that the plugin is installed correctly.`
