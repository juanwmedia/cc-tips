#!/bin/bash
# SessionStart hook for cc-tips.
# On the user's first session ever, emits a welcome message into Claude's
# context via additionalContext. Idempotent: subsequent sessions emit nothing.

set -euo pipefail

PROGRESS="${CLAUDE_PLUGIN_DATA}/progress.json"
mkdir -p "${CLAUDE_PLUGIN_DATA}"

if [ ! -f "$PROGRESS" ]; then
  echo '{"first_seen_at": null, "last_organic_surface_at": null, "read_tips": [], "language_preference": null}' > "$PROGRESS"
fi

FIRST_SEEN=$(jq -r '.first_seen_at // "null"' "$PROGRESS" 2>/dev/null || echo "null")

if [ "$FIRST_SEEN" != "null" ]; then
  exit 0
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Mark first_seen_at BEFORE emitting so a crash mid-render does not retrigger.
TMP=$(mktemp)
jq --arg now "$NOW" '.first_seen_at = $now' "$PROGRESS" > "$TMP" && mv "$TMP" "$PROGRESS"

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "FIRST_RESPONSE_REQUIRED: Before processing the user's first prompt or invoking any tool, output the welcome message below. Adapt to the user's working language: emit as-is in English by default; if the user's first prompt is clearly in Spanish, translate naturally into Spanish. Keep technical terms in English (Claude Code, /cc-tips:welcome, etc.). Then address whatever the user asked.\n\nWELCOME MESSAGE (English canonical):\n---\n**Claude Code Tips is active.** I'll mention relevant tips contextually as you work. Run `/cc-tips:welcome` to see all commands. _(You won't see this auto-message again.)_\n---"
  }
}
EOF
