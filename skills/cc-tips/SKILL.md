---
name: cc-tips
description: Surface a relevant Claude Code tip when the user is exploring or using Claude Code features (hooks, skills, MCP, subagents, plugins, memory, models, sessions).
model: haiku
allowed-tools: Read, Bash(curl *), Bash(jq *), Bash(date *), Bash(mkdir *), Bash(mv *), Bash(cat *), Bash(test *), Bash(echo *), Bash(mktemp)
---

# cc-tips — contextual tip surface

Decide whether a tip is relevant to the user's current work and surface it briefly. The user does the actual reading via `/cc-tips:open <N>`.

## When to use this skill

Activate when the user's recent prompts are about Claude Code features or workflows. The 11 covered topics: `skills`, `mcp`, `hooks`, `subagents`, `plugins`, `memory-context`, `models-cost`, `permissions`, `sessions`, `autonomous`, `fundamentals`.

Examples that match: "how do I write a Claude Code hook?", "what's the difference between agents and subagents?", "show me how to use MCP", "I'm setting up plugin marketplaces", "I want Claude to remember things across sessions", "how do I limit which tools Claude can run?".

Do NOT surface a tip if the user is working on something unrelated to Claude Code, or if you would be interrupting a tool result, code rendering, or a multi-step procedure mid-flow.

## Procedure

### 1. Read state

Read these files (use defaults when missing):

- `${CLAUDE_PLUGIN_ROOT}/manifest.json` — list of all available tips with id, slug, topic, summaries, URLs.
- `${CLAUDE_PLUGIN_DATA}/progress.json` — user state. Schema: `{"first_seen_at": ISO|null, "last_organic_surface_at": "YYYY-MM-DD"|null, "read_tips": [int...], "language_preference": "es"|"en"|null}`.

If `progress.json` does not exist, create it:

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}"
echo '{"first_seen_at": null, "last_organic_surface_at": null, "read_tips": [], "language_preference": null}' > "${CLAUDE_PLUGIN_DATA}/progress.json"
```

### 2. Apply gating rules (in order; skip surfacing if any holds)

- `last_organic_surface_at` equals today (UTC). One organic mention per day across all sessions.
- After filtering manifest tips by topic relevance AND excluding ids in `read_tips`, the candidate set is empty.
- The current message context is mid-tool-result or mid-code-render where an aside would interrupt.

### 3. Pick one tip

From candidates remaining after gating:
- Score by topic relevance to the recent conversation. The most directly relevant topic wins.
- Tie-break: prefer the most recent tip (highest id).
- Pick exactly ONE. Never surface multiple at once.

### 4. Detect language

Read the user's recent prompts. Spanish → conversational language is Spanish. Any other language → English. Persist the choice into `progress.json` `language_preference` if it was null.

### 5. Render the surface

One short paragraph in the user's working language. Mention the tip's id, topic, and one-line summary (`summary_es` or `summary_en` from manifest). End with the open command. Keep technical terms in English (hooks, skills, MCP, subagents, plugins, checkpoints).

Example (English):
> By the way — there's a tip about Claude Code checkpoints that might help here. Tip #3 (sessions): _"Recover earlier code state with Esc Esc and the /checkpoints command."_ Open it with `/cc-tips:open 3`.

Example (Spanish):
> Por cierto — hay un tip sobre checkpoints en Claude Code que te puede servir aquí. Tip #3 (sessions): _"Recupera estados anteriores del código con Esc Esc y el comando /checkpoints."_ Ábrelo con `/cc-tips:open 3`.

### 6. Update state

After successfully rendering the surface, update `progress.json` atomically:

```bash
TODAY=$(date -u +%Y-%m-%d)
TMP=$(mktemp)
jq --arg today "$TODAY" '.last_organic_surface_at = $today' "${CLAUDE_PLUGIN_DATA}/progress.json" > "$TMP" && mv "$TMP" "${CLAUDE_PLUGIN_DATA}/progress.json"
```

Do NOT add the tip's id to `read_tips`. The tip is only marked read when the user runs `/cc-tips:open <N>`.

### 7. Continue

After the surface line, continue answering the user's actual question normally. The surface is one short paragraph, not a takeover.

## Constraints

- Maximum one organic surface per day. Never two, even if topics shift mid-day.
- Never surface during a tool-result render or a code-only response.
- Never list multiple candidate tips. Pick one or none.
- Conversational layer follows user language; technical terms stay in English.
- The user's GitHub username, machine state, and any private context are never sent anywhere — this skill only reads local files and emits text.
