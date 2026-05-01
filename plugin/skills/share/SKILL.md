---
name: share
description: Draft a tip contribution from the recent conversation and submit it as a GitHub issue (gh CLI primary, browser URL fallback).
disable-model-invocation: true
model: haiku
allowed-tools: Bash(gh *), Bash(test *)
---

# /cc-tips:share

Draft a Claude Code tip from the recent conversation, present for review, and submit as a GitHub issue against `juanwmedia/cc-tips` with the `contribution` label.

The session-start hook has already injected the LANGUAGE RULE. Apply it for the conversational layer (drafts shown to the user, prompts, confirmation messages). The issue title and body submitted to GitHub are always in English (so the maintainer can curate uniformly).

## Procedure

### 1. Mine the conversation

Read the last ~20 turns. Identify a CONCRETE, ACTIONABLE pattern the user discovered or worked through. Examples of good material:

- A non-obvious flag or option combination that solved a real problem.
- A workflow shortcut that saved time.
- A gotcha and its workaround.

If the conversation has nothing concrete worth sharing, tell the user honestly (in the working language):

> I don't see a specific Claude Code pattern in our recent conversation that would make a useful tip. Try `/cc-tips:share` after we work through something concrete together.

Stop.

### 2. Draft the proposal (always in English for submission)

Construct:

- **Title**: short, action-oriented, lowercase first word (e.g., `Use /loop to poll until a build finishes`).
- **Suggested topic**: one of `skills, mcp, hooks, subagents, plugins, memory-context, models-cost, permissions, sessions, autonomous, fundamentals`.
- **Body** (markdown):

```markdown
## Suggested topic
<topic>

## What the tip is about
<2-3 sentences describing the pattern>

## How to use it
<concrete example, code blocks if relevant>

## Why it matters
<1-2 sentences on the benefit>
```

### 3. Present for review

Show the draft to the user, in the working language, but include the English title and body verbatim so the user sees what will actually be submitted. Ask plainly: edit, approve, or cancel? Iterate until approved.

### 4. Submit

Try `gh` first:

```bash
gh auth status >/dev/null 2>&1
```

If exit code is 0 (`gh` is installed and authenticated):

```bash
GH_USER=$(gh api user --jq .login 2>/dev/null)
```

If `GH_USER` is non-empty, append a final line `Contributed by @<GH_USER>` to the body.

```bash
gh issue create \
  --repo juanwmedia/cc-tips \
  --title "<title>" \
  --body "<body>" \
  --label contribution
```

The command prints the issue URL on success. Show it to the user (in the working language).

### 5. Browser fallback (if gh is missing or unauthenticated)

Build the GitHub issue URL yourself. Construct it with proper percent-encoding of the title and body:

```
https://github.com/juanwmedia/cc-tips/issues/new?title=<URL_ENCODED_TITLE>&body=<URL_ENCODED_BODY>&labels=contribution
```

Apply standard percent-encoding rules:
- Spaces → `%20`
- `\n` → `%0A`
- `&` → `%26`, `=` → `%3D`, `?` → `%3F`, `#` → `%23`, `+` → `%2B`
- `<` → `%3C`, `>` → `%3E`, `"` → `%22`
- Other reserved characters per RFC 3986

Print the URL to the user (do NOT shell out to `open`/`xdg-open`/`start` — terminals handle clickable URLs natively across platforms). Tell the user (in the working language):

> Click the URL below to open the pre-filled issue in your browser. If you want attribution, add your GitHub handle to the body before submitting.
>
> <URL>

## Constraints

- Always show the draft to the user BEFORE submitting. Never submit without approval.
- If the user revises, redraft and re-present.
- Keep the draft concise — the maintainer expands and refines later.
- Never submit without the `contribution` label.
- Title and body submitted are always in English.
