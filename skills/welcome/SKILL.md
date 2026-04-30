---
name: welcome
description: Show the Claude Code Tips welcome message on demand.
disable-model-invocation: true
model: haiku
---

# /cc-tips:welcome

Render the welcome message regardless of `first_seen_at`. Detect the user's working language from recent prompts (Spanish → ES, otherwise EN) and adapt phrasing. Keep technical terms in English.

## Output (English)

> **Welcome to Claude Code Tips.**
>
> This plugin surfaces tips from wmedia.es as you work. When you're exploring a Claude Code feature a tip covers, I'll mention it briefly (max one per day, never the same tip twice).
>
> You can also:
>
> - `/cc-tips:list` — browse all available tips.
> - `/cc-tips:list <topic>` — filter by topic.
> - `/cc-tips:open <N>` — read a specific tip.
> - `/cc-tips:share` — contribute a tip you've discovered.
>
> To get new tips as they're published, enable auto-update for this plugin in `/plugin marketplace`, or run `/plugin marketplace update cc-tips` periodically.

## Output (Spanish)

> **Bienvenido a Claude Code Tips.**
>
> Este plugin te muestra tips de wmedia.es mientras trabajas. Cuando estés explorando una feature de Claude Code que un tip cubre, te lo menciono brevemente (máximo uno por día, nunca el mismo dos veces).
>
> También puedes:
>
> - `/cc-tips:list` — ver todos los tips disponibles.
> - `/cc-tips:list <topic>` — filtrar por topic.
> - `/cc-tips:open <N>` — leer un tip concreto.
> - `/cc-tips:share` — contribuir un tip que hayas descubierto.
>
> Para recibir tips nuevos según se publiquen, activa auto-update para este plugin en `/plugin marketplace`, o ejecuta `/plugin marketplace update cc-tips` periódicamente.

After rendering, do nothing else. Do not modify `progress.json` from this skill — `first_seen_at` is owned by the SessionStart hook.
