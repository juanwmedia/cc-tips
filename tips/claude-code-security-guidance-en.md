---
date: 2026-06-03
type: tip
title_es: "Seguridad en Claude Code: que cace sus propias vulnerabilidades antes de que lleguen a prod"
title_en: "Security in Claude Code: make it catch its own vulnerabilities before they hit prod"
---
> **TL;DR** Install the `security-guidance` plugin (`/plugin install security-guidance@claude-plugins-official`) and Claude reviews its own code for vulnerabilities *as it writes*, in three layers: a per-edit pattern match, an end-of-turn diff review, and a deeper review on every commit. It catches injection, authz bypass, unsafe deserialization, weak crypto, and hands them to Claude to fix in the same session, before the PR. It runs on its own and never blocks: it's one layer of defense, not the only one.

`security-guidance` doesn't ask Claude to grade itself. It runs an **independent** review (a separate instance, fresh context, security-focused prompt) over what Claude just wrote. It's the earliest layer in the chain: it catches the flaw in the editor, before it reaches the PR, the review, and CI. Catch it here and it never ships to prod.

## The three layers

| When | What it does | Cost |
|---|---|---|
| **On each edit** | Pattern match for risky calls: `eval(`, `pickle`, `dangerouslySetInnerHTML`, `.innerHTML =`, edits under `.github/workflows/` | 0, no model call |
| **At end of turn** | Background review of the turn's diff: injection, authz bypass, IDOR, SSRF, weak crypto | Model usage |
| **On each commit/push Claude makes** | Agentic review that reads surrounding code (callers, sanitizers) to cut false positives | Model usage |

If it finds something, it **re-prompts Claude with the finding** and Claude fixes it in the conversation. You see the problem and the fix in your session, not in an after-the-fact report.

## How to turn it on

```bash
# In a Claude Code session:
/plugin install security-guidance@claude-plugins-official
/reload-plugins
```

Pick **user scope** so it loads in every local session. For a shared repo (or [Claude Code on the web](/en/tips/claude-code-cloud-sessions-from-browser), where user plugins don't carry over), declare it in `.claude/settings.json`:

```json
{ "enabledPlugins": { "security-guidance@claude-plugins-official": true } }
```

From there it runs on its own. No command to remember.

## Tune it to your project

- **Natural-language rules** for the model-backed reviews, in `.claude/claude-security-guidance.md`. Your threat model: *"every route under /admin must call `require_role` before any DB read"*.
- **Deterministic patterns** per edit, in `.claude/security-patterns.yaml`: your own regex or substrings, for example catching a hardcoded `sk_live_`.

## Where it fits (and what it isn't)

It's **one layer of defense in depth, not a complete solution**: the reviewer model can miss things, and no layer blocks the commit. The full chain:

1. `security-guidance`, **in session** (this)
2. `/security-review`, **on demand** when you ask
3. [Code Review / `/ultrareview`](/en/tips/claude-code-ultrareview), **on the PR**
4. Your **CI**: static analysis, supply-chain scanners

Each stage catches what the previous one missed. This plugin's value is shrinking what reaches the later ones, not replacing them.

## Watch out for

- **It doesn't block.** Findings arrive as instructions; Claude fixes them, but the final call is yours.
- **It needs git** for the turn and commit reviews. Without a repo, only the pattern match runs.
- **It costs tokens** on the turn and commit layers (the per-edit one is free). Capped at 20 commit reviews per hour.
- It needs **Python 3.8+** on your `PATH`; the first run creates a venv under `~/.claude/security/`.
- The model-backed reviews use a strong model by default, configurable via `SECURITY_REVIEW_MODEL` and `SG_AGENTIC_MODEL`.

## Reference

| Aspect | Detail |
|---|---|
| Install | `/plugin install security-guidance@claude-plugins-official` + `/reload-plugins` |
| Requirements | CLI v2.1.144+, Python 3.8+, git (for turn/commit) |
| Layers | edit (patterns) · turn (diff) · commit (agentic) |
| Custom rules | `.claude/claude-security-guidance.md` · `.claude/security-patterns.yaml` |
| Disable layers | `ENABLE_PATTERN_RULES=0` · `ENABLE_STOP_REVIEW=0` · `ENABLE_COMMIT_REVIEW=0` · `SECURITY_GUIDANCE_DISABLE=1` |
| Built on | hooks (`PostToolUse`, `Stop`…) |

> Official docs: [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance)
