---
date: 2026-03-24
type: tip
title_es: "Programa con la voz: Voice Mode en Claude Code"
title_en: "Code by Voice: Voice Mode in Claude Code"
---

# Quick Tip: Code by Voice: Voice Mode in Claude Code

> **TL;DR** Enable `/voice`, hold the spacebar and speak. Claude Code transcribes in streaming — you see words appearing as you talk. Release and the prompt is ready. Mix voice and typing in the same message.

There's a clear trend in the AI agent world: voice interaction. Typing long, descriptive prompts in a terminal is slow. Dictating them is more natural, faster, and keeps your hands free to browse code or documentation in another window.

Claude Code has incorporated this with streaming transcription — you don't wait until you finish speaking to see text. Words appear in real time as you dictate, optimized for development vocabulary: `regex`, `OAuth`, `JSON`, `localhost` are transcribed correctly. It even picks up your project name and current git branch as recognition hints.

In my experience it still works a bit rough around the edges — sometimes the "hold to record" detection lags, or the transcription doesn't nail very specific terms. But it's good to have as an option, and it will improve.

Result:

```
> /voice
Voice mode enabled. Hold Space to record. Dictation language: en

> [hold Space, speak: "refactor the auth middleware
   to use the new token validation helper"]

> refactor the auth middleware to use the new
  token validation helper▮
```

## Setup

### **1. Enable Voice Mode**

```
/voice
```

Persists across sessions. Run `/voice` again to disable.

### **2. Speak**

Hold `Space` and talk. You'll see `keep holding…` briefly, then a live waveform. Release to finalize.

Text inserts at the cursor position — you can dictate at any point in the prompt and combine with typed text.

### **3. Change the dictation language**

Dictation uses your `language` setting. If not defined, defaults to English:

```json
{
  "language": "es"
}
```

### **4. Rebind the push-to-talk key (recommended)**

`Space` has a warmup because it needs to distinguish between holding and typing. A modifier combination starts instantly:

```json
// ~/.claude/keybindings.json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "meta+k": "voice:pushToTalk",
        "space": null
      }
    }
  ]
}
```

## Reference

| Aspect | Detail |
|---|---|
| Enable | `/voice` (toggle) |
| Default key | `Space` (hold) |
| Transcription | Streaming in real time |
| Vocabulary | Optimized for development (regex, OAuth, JSON, etc.) |
| Auto hints | Project name + current git branch |
| Languages | 20 languages (en, es, fr, de, ja, ko, pt, etc.) |
| Persistence | Stays enabled across sessions |
| Requirements | claude.ai login (not API key), local microphone |
| Minimum version | v2.1.69+ |

> Official docs: [Voice dictation](https://code.claude.com/docs/en/voice-dictation)

## Requirements

- Claude Code v2.1.69+
- claude.ai account (doesn't work with API key, Bedrock, Vertex, or Foundry)
- Local microphone access (doesn't work over SSH or remote environments)
- macOS/Linux/Windows (Linux may need SoX or ALSA utils)
