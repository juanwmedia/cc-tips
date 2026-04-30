---
name: open
description: Open a Claude Code tip by its numeric id, fetch and cache the markdown, render it, and mark as read.
disable-model-invocation: true
model: haiku
allowed-tools: Read, Bash(curl *), Bash(jq *), Bash(mkdir *), Bash(mv *), Bash(cat *), Bash(test *), Bash(mktemp)
argument-hint: "<N>"
---

# /cc-tips:open

Open the tip with numeric id `$ARGUMENTS`, fetch (cache or curl), render to the user, and mark as read.

## Procedure

### 1. Parse argument

`$ARGUMENTS` must be a positive integer. If not, respond: `Usage: /cc-tips:open <id>. Run /cc-tips:list to see ids.` Stop.

### 2. Look up the tip

Read `${CLAUDE_PLUGIN_ROOT}/manifest.json`. Find the entry with `id == $ARGUMENTS`.

If not found:
> Tip $ARGUMENTS not found. Run `/cc-tips:list` to see available tips.

Stop.

### 3. Detect language

From recent user prompts, pick `lang = "es"` (Spanish) or `lang = "en"` (any other).

### 4. Cache check

Compute cache path: `${CLAUDE_PLUGIN_DATA}/tips/<slug>-<lang>-v<version>.md` using `slug` and `version` from the manifest entry, where `<slug>` is the language-specific slug (`slug_es` or `slug_en` if present, else `slug`).

If the cache file exists, read it and skip to step 6.

### 5. Fetch fresh

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}/tips"
TMP=$(mktemp)
curl -sLf --max-time 15 "<url_es or url_en from manifest>" -o "$TMP"
```

If `curl` exits non-zero (network failure, 404, timeout):
> Couldn't fetch tip $ARGUMENTS. The remote URL is unreachable or the file is missing. Try again in a moment, or run `/plugin marketplace update cc-tips` to refresh the manifest.

Stop. Do NOT add to `read_tips`.

On success, atomically move into place:
```bash
mv "$TMP" "${CLAUDE_PLUGIN_DATA}/tips/<slug>-<lang>-v<version>.md"
```

### 6. Render to user

Output the markdown content as-is. After the content, append (each on its own paragraph):

- **Attribution** (only if manifest entry has non-null `contributed_by_github_username`):
  > _Contributed by [@username](https://github.com/<username>)_

- **Update reminder** (always, in user's working language):
  > _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update cc-tips` periodically._

### 7. Mark as read

Append `$ARGUMENTS` (as integer) to `read_tips` in `progress.json` if not already present. Atomic update:

```bash
TMP=$(mktemp)
jq --argjson n $ARGUMENTS '
  if (.read_tips | index($n)) == null
  then .read_tips += [$n]
  else .
  end
' "${CLAUDE_PLUGIN_DATA}/progress.json" > "$TMP" && mv "$TMP" "${CLAUDE_PLUGIN_DATA}/progress.json"
```

## Notes

- Cache files are versioned by manifest entry's `version`. When the manifest gets a newer version (after `/plugin marketplace update`), the cache miss triggers a re-fetch automatically. Old cache files remain on disk until the user clears them (no auto-cleanup in v1).
- Marking as read happens only after a successful render. Failed fetches do not mark.
- The conversational wrapper (any text you say to the user OUTSIDE the tip's markdown content) is in the user's working language. The tip content itself is the markdown as fetched.
