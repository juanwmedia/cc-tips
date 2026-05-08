---
date: 2026-05-08
type: tip
title_es: "Crea y distribuye temas personalizados con Claude Code"
title_en: "Create and distribute custom themes with Claude Code"
---

> **TL;DR** Run `/theme` and pick **New custom theme...** at the end of the list. You choose a base preset (`dark` or `light`) and override only the tokens you care about. It lives in `~/.claude/themes/<slug>.json`. Hot-reload: edit the JSON and the active session updates without restarting. And if you ship it inside a [plugin](/en/tips/claude-code-plugin-marketplace-distribution), the whole team inherits it with one install.

Until April, Claude Code shipped with four or five themes and that was it. If you worked with a specific palette — your company's corporate scheme, Dracula, Solarized, a mix of your own — you took whatever the repo gave you. Anthropic packaged the fix in `v2.1.118` (Week 17, April 2026): **custom themes**. And the most under-discussed piece is the last one — themes are shippable as plugins.

## How it works internally

Each custom theme is a JSON file in `~/.claude/themes/<slug>.json` with three fields:

| Field | Detail |
|---|---|
| `name` | The name that shows up in the `/theme` picker |
| `base` | The preset to inherit from: `dark`, `light`, or any built-in |
| `overrides` | Dictionary of semantic tokens to colors |

You only override what you care about. The rest inherits from the base preset. When you select it, Claude stores `custom:<slug>` as your theme preference. And it watches the folder — if you edit the JSON in your code editor, changes take effect in the live session without a restart.

Color values accept any of these formats:

```
#bd93f9       (#rrggbb)
#bdf          (#rgb)
rgb(189, 147, 249)
ansi256(141)  (256-color palette)
ansi:cyan     (16 standard ANSI)
```

## Result preview

```json
// ~/.claude/themes/dracula.json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error":  "#ff5555",
    "success": "#50fa7b"
  }
}
```

Save the file. Run `/theme`, see "Dracula" in the list, pick it. Change `#bd93f9` to `#ff79c6` in your editor, save. Switch back to the terminal: already applied. No restart.

## How to use it

### **1. Interactive picker (no JSON)**

```
> /theme
[built-in themes]
[custom themes you've created]
[themes contributed by installed plugins]
> New custom theme...
```

Name it, pick a base preset, override tokens one by one. Claude creates the JSON for you in `~/.claude/themes/`.

### **2. Hand-edit the JSON**

Faster when you already know the hex values you want. Create the file, drop in the `overrides` you need, switch back to the terminal and pick it from `/theme`.

```bash
mkdir -p ~/.claude/themes
cat > ~/.claude/themes/corporate.json <<'EOF'
{
  "name": "Corporate",
  "base": "light",
  "overrides": {
    "claude": "#1a73e8",
    "syntax.string": "#0f9d58",
    "syntax.keyword": "#d93025"
  }
}
EOF
```

### **3. Ship the theme to your team as a plugin**

Here's the edge. Instead of asking 12 people to copy your JSON, you drop it inside a [Claude Code plugin](/en/tips/claude-code-plugin-marketplace-distribution):

```
my-plugin/
├── plugin.json
└── themes/
    └── corporate.json
```

`plugin install` does the rest: the theme shows up in every teammate's `/theme` automatically. When you bump the plugin version (corporate colors changed, you added a dark variant), a `/plugin marketplace update` propagates it.

## Reference

| Aspect | Detail |
|---|---|
| Minimum version | Claude Code `v2.1.118` |
| Command | `/theme` (alias of what you already knew) |
| Path | `~/.claude/themes/<slug>.json` |
| Slug | Filename without `.json` |
| Hot-reload | Yes — edit the JSON and the live session updates |
| Color formats | `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, `ansi:<name>` |
| Distribution | Any plugin can ship themes inside its `themes/` folder |
| Persistence | The selected theme lives in `~/.claude/settings.json` as `custom:<slug>` |

> Official docs: [Terminal config — Create a custom theme](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme)
