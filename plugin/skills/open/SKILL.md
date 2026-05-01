---
name: open
description: Open a Claude Code tip by its numeric id, fetch and cache the markdown, render it, and mark as read. Translates on the fly for non-ES/EN languages and caches the translation.
disable-model-invocation: true
model: haiku
allowed-tools: Bash(jq *), Bash(cat *), Bash(curl *), Bash(mkdir *), Bash(test *), Bash(mv *), Bash(mktemp)
argument-hint: "<N>"
---

# /cc-tips:open

Open the tip with numeric id `$ARGUMENTS`, fetch (cache or curl), render to the user, and mark as read.

The session-start hook has already injected the LANGUAGE RULE. It governs both the conversational layer (status messages, attribution, footer) and the tip content (Spanish or English curated; other languages translated on the fly and cached).

Run silently: do not narrate intermediate steps ("I'll fetch...", "Let me verify..."). Output only the final user-visible result.

## Procedure

All JSON parsing goes through `jq`. Cross-platform shell idioms: always quote paths, `mktemp` without flags, `--argjson` for numeric arguments, `--arg` for strings, atomic writes via `tmpfile + mv`.

### 1. Parse argument

`$ARGUMENTS` must be a positive integer. If not, respond (in the working language): `Usage: /cc-tips:open <id>. Run /cc-tips:list to see ids.` Stop.

### 2. Look up the tip

Extract the entry by id with `jq`:

```bash
ENTRY=$(jq -c --argjson n "$ARGUMENTS" '.tips[] | select(.id == $n)' "${CLAUDE_PLUGIN_ROOT}/manifest.json")
```

If `$ENTRY` is empty, the id is not in the manifest. Respond (in the working language): `Tip $ARGUMENTS not found. Run /cc-tips:list to see available tips.` Stop.

Pull the fields you need from `$ENTRY`:

```bash
SLUG=$(printf '%s' "$ENTRY" | jq -r .slug)
TIP_VERSION=$(printf '%s' "$ENTRY" | jq -r .version)
URL_ES=$(printf '%s' "$ENTRY" | jq -r .url_es)
URL_EN=$(printf '%s' "$ENTRY" | jq -r .url_en)
ATTRIB=$(printf '%s' "$ENTRY" | jq -r '.contributed_by_github_username // ""')
```

### 3. Detect language

From recent user prompts, determine the working language. Map it to a lowercase language code:
- Spanish → `es`
- English → `en`
- Italian → `it`, French → `fr`, Portuguese → `pt`, German → `de`, etc. (use the appropriate ISO 639-1 code).

### 4. Determine source URL

- `lang_code == "es"` → source URL = `$URL_ES`
- `lang_code == "en"` → source URL = `$URL_EN`
- otherwise (translation case) → source URL = `$URL_EN` (we always translate from English)

### 5. Cache check

Cache path: `${CLAUDE_PLUGIN_DATA}/tips/<SLUG>-<lang_code>-v<TIP_VERSION>.md`.

Examples for slug `claude-code-skills-custom-slash-commands` v1:
- ES → `…-es-v1.md` (curated Spanish from `url_es`)
- EN → `…-en-v1.md` (curated English from `url_en`)
- IT → `…-it-v1.md` (translated from EN, saved on first open)

Check existence:

```bash
test -f "<cache_path>"
```

If it exists, `cat` it and skip to step 7. Cached content is already in the right language.

### 6. Fetch fresh (cache miss)

Ensure the cache directory exists:

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}/tips"
```

Fetch the source markdown directly to the cache path:

```bash
curl -sLf --max-time 15 "<source_url>" -o "<cache_path>"
```

If `curl` exits non-zero (network failure, 404, timeout), respond (in the working language):
> Couldn't fetch tip $ARGUMENTS. The remote URL is unreachable or the file is missing. Try again in a moment, or run `/plugin marketplace update juanwmedia-cc-tips` to refresh the manifest.

Stop. Do NOT mark as read.

Now branch on language:

- **`lang_code` is `es` or `en`**: `cat` the cache file. The content is the curated tip — proceed to step 7.

- **otherwise (translation case)**: `cat` the cache file (it contains the English source just downloaded). Translate the BODY into the working language following the LANGUAGE RULE's translation rules:
  - Skip the YAML frontmatter (lines from the first `---` through the second `---`). It is metadata, not user-facing content. Do NOT translate or include it.
  - Preserve all code blocks, terminal commands, and configuration snippets verbatim.
  - Preserve "Claude Code" and technical terms in English (hooks, skills, MCP, subagents, plugins).
  - Translate prose, headers, and explanatory text only.

  Save the translated body (no frontmatter) back to the cache path so subsequent opens hit the cache. Use atomic write:

  ```bash
  TMP=$(mktemp)
  printf '%s' "<translated_markdown>" > "$TMP" && mv "$TMP" "<cache_path>"
  ```

### 7. Render

**Strip the YAML frontmatter before rendering.** Tip files start with a frontmatter block (`---` line, several `key: value` lines, another `---` line). This metadata is for the build pipeline, NOT for the user. Drop everything from the first `---` through the second `---` (inclusive) and render only the body that follows. If the content does not start with `---`, render as-is.

Output the (frontmatter-stripped) tip content as your response message. After the markdown body, append (each on its own paragraph):

- **Attribution** (only if `$ATTRIB` is non-empty):
  > _Contributed by [@$ATTRIB](https://github.com/$ATTRIB)_

- **Contribute hint** (always, in the working language):
  > _Discovered a useful pattern? Share it back with `/cc-tips:share`._

- **Update reminder** (always, in the working language):
  > _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update juanwmedia-cc-tips` periodically._

### 8. Mark as read (atomic, jq-driven)

Initialize `progress.json` if missing:

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}"
test -f "${CLAUDE_PLUGIN_DATA}/progress.json" || printf '%s' '{"read_tips":[]}' > "${CLAUDE_PLUGIN_DATA}/progress.json"
```

Append `$ARGUMENTS` to `read_tips` if not already present, atomically:

```bash
TMP=$(mktemp)
jq --argjson n "$ARGUMENTS" 'if (.read_tips // [] | index($n)) == null then (.read_tips = ((.read_tips // []) + [$n])) else . end' "${CLAUDE_PLUGIN_DATA}/progress.json" > "$TMP" && mv "$TMP" "${CLAUDE_PLUGIN_DATA}/progress.json"
```

## Notes

- Cache files are versioned by the manifest entry's `version`. When the manifest gets a newer version (after `/plugin marketplace update`), the cache miss triggers a re-fetch automatically. Old cache files remain on disk until the user clears them (no auto-cleanup in v1).
- For non-ES/EN languages, the cached file IS the translated version after the first open. Subsequent opens are instant (no translation, no network).
- Marking as read happens only after a successful render. Failed fetches do not mark.
