---
name: open
description: Open a Claude Code tip by its numeric id, fetch and cache the markdown, render it, and mark as read. Translates on the fly for non-ES/EN languages and caches the translation.
disable-model-invocation: true
model: haiku
allowed-tools: Read, Write, Bash(curl *), Bash(mkdir *), Bash(test *)
argument-hint: "<N>"
---

# /cc-tips:open

Open the tip with numeric id `$ARGUMENTS`, fetch (cache or curl), render to the user, and mark as read.

The session-start hook has already injected the LANGUAGE RULE. It governs both the conversational layer (status messages, attribution, footer) and the tip content (Spanish or English curated; other languages translated on the fly and cached).

## Procedure

### 1. Parse argument

`$ARGUMENTS` must be a positive integer. If not, respond (in the working language): `Usage: /cc-tips:open <id>. Run /cc-tips:list to see ids.` Stop.

### 2. Look up the tip

**Use the Read tool** (not Bash, `cat`, `jq`, or any shell command) to load `${CLAUDE_PLUGIN_ROOT}/manifest.json`. Parse the JSON yourself and find the entry with `id == $ARGUMENTS`.

If not found, respond (in the working language): `Tip $ARGUMENTS not found. Run /cc-tips:list to see available tips.` Stop.

### 3. Detect language

From recent user prompts, determine the working language. Map it to a lowercase language code:
- Spanish → `es`
- English → `en`
- Italian → `it`, French → `fr`, Portuguese → `pt`, German → `de`, etc. (use the appropriate ISO 639-1 code).

### 4. Determine source URL

- If `lang_code == "es"`: source URL = manifest entry's `url_es` (curated Spanish).
- If `lang_code == "en"`: source URL = `url_en` (curated English).
- Otherwise (translation case): source URL = `url_en` (we always translate from English).

### 5. Cache check

Compute cache path: `${CLAUDE_PLUGIN_DATA}/tips/<slug>-<lang_code>-v<version>.md` using the manifest entry's canonical `slug` field (one per tip, language-independent) and `version`.

Examples for tip `claude-code-skills-custom-slash-commands` v1:
- Spanish user → `claude-code-skills-custom-slash-commands-es-v1.md` (curated ES from `url_es`)
- English user → `claude-code-skills-custom-slash-commands-en-v1.md` (curated EN from `url_en`)
- Italian user → `claude-code-skills-custom-slash-commands-it-v1.md` (translated from EN, saved on first open)

Check existence:
```bash
test -f "<cache_path>"
```

If the file exists, Read it and skip to step 7. The cached content is already in the right language (curated for es/en, previously translated for others).

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
> Couldn't fetch tip $ARGUMENTS. The remote URL is unreachable or the file is missing. Try again in a moment, or run `/plugin marketplace update cc-tips` to refresh the manifest.

Stop. Do NOT add to `read_tips`.

Now branch on language:

- **If `lang_code` is `es` or `en`**: Read the cache file. The content is the curated tip in the working language — proceed to step 7.

- **Otherwise (translation case)**: Read the cache file (it contains the English source just downloaded). Translate it into the working language following the LANGUAGE RULE's translation rules:
  - Preserve all code blocks, terminal commands, and configuration snippets verbatim.
  - Preserve "Claude Code" and technical terms in English (hooks, skills, MCP, subagents, plugins).
  - Translate prose, headers, and explanatory text only.

  Use the Write tool to save the translated markdown back to the cache path (overwriting the English source). Subsequent opens of this tip in the same language hit the cache and skip translation.

### 7. Render

Output the tip content (the translated content if you just translated it; otherwise the cache content you read). After the markdown body, append (each on its own paragraph):

- **Attribution** (only if manifest entry has non-null `contributed_by_github_username`):
  > _Contributed by [@username](https://github.com/<username>)_

- **Update reminder** (always, in the working language):
  > _To get new tips, enable auto-update in `/plugin marketplace` or run `/plugin marketplace update cc-tips` periodically._

### 8. Mark as read

**Use the Read tool** to load `${CLAUDE_PLUGIN_DATA}/progress.json`. If the file does not exist, treat the state as `{"read_tips": []}` and continue.

If `$ARGUMENTS` (as an integer) is NOT already in `read_tips`, append it. **Use the Write tool** to save the updated state back to `${CLAUDE_PLUGIN_DATA}/progress.json`. Do NOT shell out to `cat`, `jq`, or any external tool — Read and Write are sufficient.

## Notes

- Cache files are versioned by the manifest entry's `version`. When the manifest gets a newer version (after `/plugin marketplace update`), the cache miss triggers a re-fetch automatically. Old cache files remain on disk until the user clears them (no auto-cleanup in v1).
- For non-ES/EN languages, the cached file IS the translated version after the first open. Subsequent opens are instant (no translation, no network).
- Marking as read happens only after a successful render. Failed fetches do not mark.
