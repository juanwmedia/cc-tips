LANGUAGE RULE — applies to all plugin output that follows.

The plugin has two distinct layers, with two different rules.

## Conversational layer

Anything written by the plugin in conversation: welcome message, topic-awareness mentions, list/open/share UI text, any prose Claude produces on behalf of the plugin: render in the user's working language. 

Detect from their first prompt.

Only the English source of plugin messages is provided. Translate it naturally to the working language when needed. 

Do NOT output the English source verbatim when the working language is not English.

## Tip content

Tips are authored in two languages: Spanish and English. Both versions are canonical (Spanish is the original; English is the human-authored translation).

When opening or rendering a tip:
- If the working language is Spanish → serve the curated Spanish version.
- If the working language is English → serve the curated English version.
- For any other working language (Italian, French, Portuguese, German, …) → fetch the English version, translate naturally to the working language while rendering, and cache the translation as `<slug>-<lang>-v<version>.md` so subsequent opens hit the cache.

Translation rules for non-curated languages:
- Preserve "Claude Code" and technical terms in English (hooks, skills, MCP, subagents, plugins).
- Preserve all code blocks, terminal commands, and configuration snippets verbatim.
- Translate prose, headers, and explanatory text only.

## Brand and commands

Keep "Claude Code Tips" (plugin name) and slash commands (`/cc-tips:list`, `/cc-tips:open`, `/cc-tips:share`, `/cc-tips:welcome`) in English regardless of working language.
