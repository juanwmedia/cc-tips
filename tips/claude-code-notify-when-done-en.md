---
date: 2026-03-06
type: tip
title_es: "Haz que Claude Code te avise cuando termine (sin molestar)"
title_en: "Get Notified When Claude Code Finishes (Only When You're Not Looking)"
---
# Quick Tip: Get Notified When Claude Code Finishes (Only When You're Not Looking)

Claude Code has an event called `Stop` that fires every time it finishes responding. You can [hook](/en/writing/claude-code-hooks-practical-guide) it to any system command — including playing a sound. The trick is making it sound only when you're not looking at the terminal, so you don't go crazy with every short response.

The hook uses `osascript` to ask macOS which app is in focus. If it's not your terminal, it plays a system sound. If you're staring at the terminal, silence.

> **TL;DR** A `Stop` hook + a script that checks the focused app = sound only when you're in another app. Zero annoying notifications.

Result — the complete script:

```bash
#!/bin/bash
# ~/.claude/notify-stop.sh
# Notify when Claude finishes — only if the terminal is not in focus

FRONTMOST=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)

# Warp identifies as "stable", not "Warp"
if [ "$FRONTMOST" != "Warp" ] && [ "$FRONTMOST" != "stable" ]; then
  afplay /System/Library/Sounds/Glass.aiff &
fi
```

## Setup

### **1. Create the script**

```bash
cat > ~/.claude/notify-stop.sh << 'EOF'
#!/bin/bash
FRONTMOST=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)

if [ "$FRONTMOST" != "Warp" ] && [ "$FRONTMOST" != "stable" ]; then
  afplay /System/Library/Sounds/Glass.aiff &
fi
EOF
chmod +x ~/.claude/notify-stop.sh
```

If you use a different terminal, replace `"Warp"` and `"stable"` with your app's name. To find out how your terminal identifies itself, run:

```bash
osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'
```

### **2. Register the hook**

Add this to your `~/.claude/settings.json` (global, for all projects):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/notify-stop.sh"
          }
        ]
      }
    ]
  }
}
```

### **3. Pick a different sound (optional)**

macOS includes several sounds in `/System/Library/Sounds/`. Some options:

```bash
# Listen to the options
afplay /System/Library/Sounds/Ping.aiff
afplay /System/Library/Sounds/Pop.aiff
afplay /System/Library/Sounds/Purr.aiff
afplay /System/Library/Sounds/Hero.aiff
afplay /System/Library/Sounds/Submarine.aiff
```

## Reference

| Concept | Detail |
|---|---|
| `Stop` event | Fires when Claude finishes responding. Does not fire on user interrupt. |
| `osascript` | Queries macOS for the frontmost app via AppleScript. |
| `afplay` | Native macOS audio player. The trailing `&` prevents blocking Claude. |
| Warp = "stable" | Warp identifies as "stable" in System Events, not "Warp". Common gotcha. |
| Hook location | `~/.claude/settings.json` for global, `.claude/settings.json` for a single project. |

> Official docs: [Hooks practical guide](https://code.claude.com/docs/en/hooks-guide)

## Requirements

- macOS (the script uses `osascript` and `afplay`)
- For Linux: replace `osascript` with `xdotool` and `afplay` with `paplay`
