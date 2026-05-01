#!/bin/bash
# SessionStart hook for cc-tips.
#
# Emits plain-text additionalContext per Claude Code hooks docs:
# "plain stdout already reaches Claude for this event."
#
# Topics are derived at runtime from manifest.json via `jq`,
# so adding a topic via auto-publish updates the hook output without edits.
#
# Cross-platform contract: bash + jq + cat + mkdir + touch + printf.
# jq is a hard runtime requirement; see README.md.

set -euo pipefail

mkdir -p "${CLAUDE_PLUGIN_DATA}"
FLAG="${CLAUDE_PLUGIN_DATA}/first_seen"

TOPICS=$(jq -r '[.tips[].topic] | unique | join(", ")' "${CLAUDE_PLUGIN_ROOT}/manifest.json")

TOPIC_AWARENESS=$(sed "s|{TOPICS}|${TOPICS}|" "${CLAUDE_PLUGIN_ROOT}/hooks/topic-awareness.md")

cat "${CLAUDE_PLUGIN_ROOT}/hooks/language-rule.md"
printf '\n'

if [ ! -f "$FLAG" ]; then
  touch "$FLAG"
  cat "${CLAUDE_PLUGIN_ROOT}/hooks/welcome-msg.md"
  printf '\n'
fi

printf '%s\n' "$TOPIC_AWARENESS"
