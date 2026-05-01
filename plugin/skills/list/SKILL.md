---
name: list
description: List all Claude Code tips grouped by topic with read/unread markers. Optional topic filter.
disable-model-invocation: true
model: haiku
allowed-tools: Bash(jq *), Bash(cat *), Bash(test *)
argument-hint: "[topic]"
---

# /cc-tips:list

Render the tip manifest as a table for the user. Optional topic filter via `$ARGUMENTS`.

The session-start hook has already injected the LANGUAGE RULE. Apply it for the conversational layer (table headers, status labels, footer, error messages). Tip titles come from the manifest as-is.

Run silently: do not narrate intermediate steps ("I'll read...", "Let me check..."). Output only the final user-visible result.

## Procedure

All JSON parsing goes through `jq`. Cross-platform shell idioms: always quote paths, no `echo` for literal strings, `mktemp` without flags, `--argjson` for numeric arguments, `--arg` for strings.

### 1. Validate topic argument (if any)

If `$ARGUMENTS` is non-empty, it's a topic filter. Get the unique topic set from the manifest:

```bash
VALID=$(jq -r '[.tips[].topic] | unique | join(",")' "${CLAUDE_PLUGIN_ROOT}/manifest.json")
```

If `$ARGUMENTS` is not a substring of `$VALID`, respond (in the working language): `Unknown topic '$ARGUMENTS'. Valid topics: <VALID with ", " separators>.` Stop.

### 2. Read state

```bash
test -f "${CLAUDE_PLUGIN_DATA}/progress.json" \
  && READ_TIPS=$(jq -r '.read_tips // [] | join(",")' "${CLAUDE_PLUGIN_DATA}/progress.json") \
  || READ_TIPS=""
```

`READ_TIPS` is now a comma-separated list of read ids (possibly empty).

### 3. Pull entries from the manifest

For the FULL list (no `$ARGUMENTS`):

```bash
jq -r '.tips[] | [.id, .topic, .title_es, .title_en] | @tsv' "${CLAUDE_PLUGIN_ROOT}/manifest.json"
```

For a TOPIC FILTER:

```bash
jq -r --arg t "$ARGUMENTS" '.tips[] | select(.topic == $t) | [.id, .topic, .title_es, .title_en] | @tsv' "${CLAUDE_PLUGIN_ROOT}/manifest.json"
```

The output is one tab-separated line per tip: `id<TAB>topic<TAB>title_es<TAB>title_en`.

### 4. Render the table

Group entries by topic in this canonical order: `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.

For each non-empty topic, render a markdown section:

```
## <Topic title>

| ID | Title | Status |
|---|---|---|
| 3 | Recover earlier code state with /checkpoints | ✓ read |
| 7 | Resume long-running sessions across machines | unread |
```

- Use `title_es` if the working language is Spanish, else `title_en`.
- Status: tips whose id appears in `READ_TIPS` show `✓ read`; otherwise `unread`.
- Translate the column headers (`ID`, `Title`, `Status`) and the `unread` word to the working language. Keep tip titles verbatim from the manifest.

### 5. Append two one-line footers, in the working language

> Run `/cc-tips:open <ID>` to read a tip.
>
> _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update juanwmedia-cc-tips` periodically._

Translate the first line to the working language (e.g., Spanish: "Ejecuta `/cc-tips:open <ID>` para leer un tip."). Keep the slash command and the literal placeholder `<ID>`.

## Notes

- This skill is read-only. It does NOT mark anything as read. Users must run `/cc-tips:open <N>` to mark a tip read.
- If the manifest yields no tips (shouldn't happen post-install), respond: `No tips available yet. Check that the plugin is installed correctly.` (translated to working language).
