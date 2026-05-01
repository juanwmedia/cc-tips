---
name: list
description: List all Claude Code tips grouped by topic with read/unread markers. Optional topic filter.
disable-model-invocation: true
model: haiku
allowed-tools: Read
argument-hint: "[topic]"
---

# /cc-tips:list

Render the tip manifest as a table for the user. Optional topic filter via `$ARGUMENTS`.

The session-start hook has already injected the LANGUAGE RULE. Apply it for the conversational layer (table headers, status labels, footer, error messages). Tip titles come from the manifest as-is.

## Procedure

1. **Use the Read tool** (not Bash, `cat`, `jq`, or any shell command) to load `${CLAUDE_PLUGIN_ROOT}/manifest.json`. Parse the JSON yourself.
2. **Use the Read tool** to load `${CLAUDE_PLUGIN_DATA}/progress.json` and extract `read_tips`. If the file does not exist or has no `read_tips` key, treat it as an empty list. Do not shell out.
3. If `$ARGUMENTS` is non-empty, treat it as a topic filter:
   - Validate against the topics present in the manifest. To enumerate them, derive the unique set of `topic` values from the entries you just read.
   - If the argument is not in that set, respond (in the working language): `Unknown topic '$ARGUMENTS'. Valid topics: <comma-separated list of topics from the manifest>.` Stop.
   - Otherwise, filter manifest entries to that topic.
4. Group entries by topic. For each non-empty topic, render a markdown section in the canonical topic order: `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.

Format per topic:

```
## <Topic title>

| ID | Title | Status |
|---|---|---|
| 3 | Recover earlier code state with /checkpoints | ✓ read |
| 7 | Resume long-running sessions across machines | unread |
```

- Use `title_es` if the working language is Spanish, else `title_en`.
- Tips whose id is in `read_tips`: `✓ read`. Otherwise: `unread`.
- Translate the column headers (`ID`, `Title`, `Status`) and the status word `unread` to the working language. Keep tip titles as authored in the manifest.

5. Append two one-line footers, in the working language:

> Run `/cc-tips:open <ID>` to read a tip.
>
> _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update cc-tips` periodically._

Translate the first line to the working language (e.g., Spanish: "Ejecuta `/cc-tips:open <ID>` para leer un tip."). Keep the slash command and the literal placeholder `<ID>`.

## Notes

- This skill is read-only. It does NOT mark anything as read. Users must run `/cc-tips:open <N>` to mark a tip read.
- If the manifest is empty (shouldn't happen post-install), respond: `No tips available yet. Check that the plugin is installed correctly.` (translated to working language).
