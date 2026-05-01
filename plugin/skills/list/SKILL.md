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

All JSON parsing goes through `jq`. **Use one Bash invocation, not several** — shell variables do NOT persist between Bash tool calls, so combine everything into a single command. Cross-platform shell idioms: always quote paths, `--argjson` for numeric arguments, `--arg` for strings.

### 1. (Optional) Validate topic argument

If `$ARGUMENTS` is non-empty and is NOT one of the canonical topics (`skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`), respond (in the working language): `Unknown topic '$ARGUMENTS'. Valid topics: skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals.` Stop. (No Bash needed for this check — the canonical list is fixed.)

### 2. Pull all the data with ONE bash call

This single command reads `read_tips` (defaulting to `[]` if missing) and outputs one tab-separated line per tip with the read flag baked in:

For the FULL list (no `$ARGUMENTS`):

```bash
READ_TIPS=$(test -f "${CLAUDE_PLUGIN_DATA}/progress.json" && jq -c '.read_tips // []' "${CLAUDE_PLUGIN_DATA}/progress.json" || printf '%s' '[]') ; jq -r --argjson p "$READ_TIPS" '.tips[] | [.id, .topic, .title_es, .title_en, (.id | IN($p[]) | tostring)] | @tsv' "${CLAUDE_PLUGIN_ROOT}/manifest.json"
```

For a TOPIC FILTER:

```bash
READ_TIPS=$(test -f "${CLAUDE_PLUGIN_DATA}/progress.json" && jq -c '.read_tips // []' "${CLAUDE_PLUGIN_DATA}/progress.json" || printf '%s' '[]') ; jq -r --arg t "$ARGUMENTS" --argjson p "$READ_TIPS" '.tips[] | select(.topic == $t) | [.id, .topic, .title_es, .title_en, (.id | IN($p[]) | tostring)] | @tsv' "${CLAUDE_PLUGIN_ROOT}/manifest.json"
```

Output schema per line: `id<TAB>topic<TAB>title_es<TAB>title_en<TAB>read` where `read` is the literal string `true` or `false`.

**The Bash command must output ONLY TSV** — exactly the jq command above, no extra formatting, no `printf` of markdown, no echo of headers. Step 3 (your response) handles all rendering.

### 3. Render the table — THIS IS YOUR FINAL RESPONSE TO THE USER

**Critical**: the Bash output from step 2 is RAW DATA (TSV) for your eyes only. The user does NOT see it as the answer — they see your response message. **You MUST write the rendered markdown table as your response text after the Bash call returns.** Do not end your turn without it. Do not assume the Bash result is "the answer". You are the renderer; the TSV is your input.

Group entries by topic in this canonical order: `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.

For each non-empty topic, write a markdown section to the user as your response:

```
## <Topic title>

| ID | Title | Status |
|---|---|---|
| 3 | Recover earlier code state with /checkpoints | ✓ read |
| 7 | Resume long-running sessions across machines | unread |
```

- Use `title_es` if the working language is Spanish, else `title_en`.
- Status: if the read flag is `true` → `✓ read`; otherwise `unread`.
- Translate the column headers (`ID`, `Title`, `Status`) and the `unread` word to the working language. Keep tip titles verbatim from the manifest.

### 4. Append two one-line footers, in the working language

> Run `/cc-tips:open <ID>` to read a tip.
>
> _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update juanwmedia-cc-tips` periodically._

Translate the first line to the working language (e.g., Spanish: "Ejecuta `/cc-tips:open <ID>` para leer un tip."). Keep the slash command and the literal placeholder `<ID>`.

## Notes

- This skill is read-only. It does NOT mark anything as read. Users must run `/cc-tips:open <N>` to mark a tip read.
- If the manifest yields no tips (shouldn't happen post-install), respond: `No tips available yet. Check that the plugin is installed correctly.` (translated to working language).
