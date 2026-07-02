---
date: 2026-07-02
type: tip
title_es: "Claude Code en JetBrains: IntelliJ y PyCharm sin cambiarte a VS Code"
title_en: "Claude Code in JetBrains: IntelliJ and PyCharm without switching to VS Code"
---

> **TL;DR** There's an official Anthropic plugin on the JetBrains Marketplace: **Claude Code [Beta]**. Install two pieces (the `claude` CLI yourself and the plugin) and run `claude` in the integrated terminal. You gain diffs in the JetBrains viewer, your selection shared automatically, `Cmd+Option+K` to reference `@file#L1-99`, and IDE errors sent to Claude. And heads up: this is not the "Claude Agent" in JetBrains' AI Assistant, they're different things.

If you code in IntelliJ or PyCharm, "using Claude Code" usually means opening the integrated terminal and typing `claude`. It works, but you miss the integration almost everyone associates only with VS Code. You don't have to switch editors: there's an official plugin that connects your JetBrains IDE to the CLI.

## How it works (not ACP, not a panel)

Here's the part that trips people up. The plugin does **not** ship a graphical panel like the VS Code extension, and it does **not** use ACP. What it does, per the docs, is run `claude` in the IDE's integrated terminal and connect to it over a local bridge. It's the same mechanism the VS Code extension uses (there that bridge is a local MCP server named `ide`), not ACP. Your interface stays the terminal; what changes is that the IDE lights up around it: diffs, selection, and diagnostics.

Important detail: **the plugin does not bundle its own copy of the CLI**. That's why you install two things (the CLI and the plugin), unlike VS Code, where the extension carries its own.

## What you actually see

```
IntelliJ IDEA ── integrated terminal
> claude
  ⧉ Selected 12 lines from auth.kt        ← your selection travels on its own
> fix the token that expires

  ▸ diff  UserService.kt        +6 -2      ← opens in the JetBrains viewer
  Cmd+Option+K → @auth.kt#L1-99            ← exact reference on the fly
```

## Getting started

**1. Install the CLI (the plugin doesn't carry it)**

Follow the [quickstart](https://code.claude.com/docs/en/quickstart) so `claude` is on your PATH. If it's missing, the plugin warns you with a "Cannot launch Claude Code".

**2. Install the plugin and restart**

In the IDE: **Settings → Plugins → Marketplace**, search "Claude Code", and install **Claude Code [Beta]**. Restart the IDE completely (sometimes more than once).

**3. Run it**

Open the integrated terminal and type `claude`: that alone activates the IDE features. From an external terminal, connect it with `/ide`. Quick launch: `Cmd+Esc` (Mac) / `Ctrl+Esc` (Win/Linux) opens Claude Code straight from the editor.

**4. Diffs in the IDE**

Inside Claude Code, `/config` → set the diff tool to `auto` to see them in the JetBrains viewer, or `terminal` to keep them as text.

## Don't confuse it with JetBrains' AI Assistant

Search for it and two similarly named things show up — it's the most repeated question:

- **Claude Code [Beta]** → the **Anthropic** plugin. It's your CLI connected to the IDE, on your Claude subscription.
- **"Claude Agent" / AI Assistant** → a **JetBrains** product that uses Claude as one of its models. Different company, different subscription, different thing.

This tip is about the first one.

## Reference

| Feature | How | Shortcut |
|---|---|---|
| Launch Claude Code | from the editor | `Cmd+Esc` / `Ctrl+Esc` |
| Diffs in the IDE | `/config` → diff tool `auto` | — |
| Shared selection | automatic (current tab/selection) | — |
| File reference | inserts `@src/auth.ts#L1-99` | `Cmd+Option+K` / `Alt+Ctrl+K` |
| Diagnostics | IDE lint and errors go to Claude | automatic |

**Real gotchas:**
- **`ESC` doesn't interrupt** in the JetBrains terminal: in **Settings → Tools → Terminal**, uncheck "Move focus to the editor with Escape" (or delete that keybinding).
- **Remote Development**: install the plugin on the **remote host** (Settings → Plugin (Host)), not on your local machine.
- **In `acceptEdits`** Claude can modify IDE config files that the IDE runs on its own. In repos you don't control, review by hand instead of auto-accepting. Revisit [the 6 permission modes](/en/tips/claude-code-permission-modes-shift-tab).

If you work in VS Code instead of JetBrains, the story is different (there you do get a graphical panel): [Claude Code in VS Code, the panel almost nobody uses](/en/tips/claude-code-vs-code-extension-native-panel).

> Official docs: [Claude Code in JetBrains IDEs](https://code.claude.com/docs/en/jetbrains)

**Related:** [Claude Code in VS Code](/en/tips/claude-code-vs-code-extension-native-panel) · [The 6 permission modes](/en/tips/claude-code-permission-modes-shift-tab)

## Requirements

- The **Claude Code [Beta]** plugin from the Marketplace + the CLI installed separately
- Works with IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, GoLand, and Android Studio
- A paid subscription (Pro, Max, Team, or Enterprise) or a Console account; no API key
