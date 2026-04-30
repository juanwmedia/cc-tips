---
date: 2026-02-21
type: tip
title_es: "Depura tu Frontend con Claude Code y Chrome"
title_en: "Debug Your Frontend with Claude Code and Chrome"
---
> **TL;DR** `claude --chrome` or `/chrome` connects Claude Code to your browser. From there, Claude opens tabs, navigates, clicks, reads the console, and debugs your frontend — all without leaving the terminal.

Claude Code integrates with the Claude in Chrome extension to give you browser automation directly from the CLI. Launch your app, ask Claude to test it, and it opens Chrome, navigates to your localhost, interacts with forms, reads console errors, and tells you what's broken — with access to the real DOM and your browser's login state.

It's fascinating to watch it work: opening tabs, scrolling, launching modals, typing search terms, and compiling results. It's still sometimes slow. It still sometimes fails. But the key word is *still*. This improves with every release, and the direction is clear.

Result:

```
> claude --chrome

Chrome integration enabled

> Open localhost:3000, fill out the registration form
  with invalid data and tell me if the error messages
  appear correctly

⏺ Opening new tab → localhost:3000
  Clicking "Sign up"...
  Typing invalid email...
  Form submitted — 3 validation errors detected:
  - Email format invalid
  - Password too short
  - Terms not accepted
```

## How to set it up

### **1. Prerequisites**

- Google Chrome or Microsoft Edge
- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+
- Claude Code v2.0.73+
- Direct Anthropic plan (Pro, Max, Teams, or Enterprise)

### **2. Launch with Chrome**

```bash
claude --chrome
```

Or within an existing session:

```bash
/chrome
```

### **3. Enable by default (optional)**

Run `/chrome` and select "Enabled by default" to skip passing `--chrome` each session. Note this increases context usage since browser tools are always loaded.

## Reference

| Capability | What it does |
|---|---|
| Live debugging | Read console errors and DOM state, then fix the code |
| Design verification | Build UI and visually compare in the browser |
| Web app testing | Test forms, user flows, and visual regressions |
| Authenticated apps | Interact with Google Docs, Gmail, Notion — uses your active session |
| Data extraction | Pull structured data from web pages and save locally |
| Task automation | Automate data entry, forms, and multi-site workflows |
| Session recording | Record interactions as GIFs to document or share |

| Command | Action |
|---|---|
| `claude --chrome` | Launch Claude Code with Chrome enabled |
| `/chrome` | Enable/manage Chrome within a session |

> Official docs: [Use Claude Code with Chrome (beta)](https://code.claude.com/docs/en/chrome)
