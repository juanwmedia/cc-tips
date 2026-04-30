---
name: share
description: Draft a tip contribution from the recent conversation and submit it as a GitHub issue (gh CLI primary, browser URL fallback).
disable-model-invocation: true
model: haiku
allowed-tools: Bash(gh *), Bash(open *), Bash(echo *), Bash(test *), Bash(printf *)
---

# /cc-tips:share

Draft a Claude Code tip from the recent conversation, present for review, and submit as a GitHub issue against `juanwmedia/cc-tips` with the `contribution` label.

## Procedure

### 1. Mine the conversation

Read the last ~20 turns. Identify a CONCRETE, ACTIONABLE pattern the user discovered or worked through. Examples of good material:

- A non-obvious flag or option combination that solved a real problem.
- A workflow shortcut that saved time.
- A gotcha and its workaround.

If the conversation has nothing concrete worth sharing, tell the user honestly:

> I don't see a specific Claude Code pattern in our recent conversation that would make a useful tip. Try `/cc-tips:share` after we work through something concrete together.

Stop.

### 2. Draft the proposal

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

Show the draft to the user in their working language. Ask plainly: edit, approve, or cancel? Iterate until approved.

### 4. Submit

Try `gh` first:

```bash
gh auth status >/dev/null 2>&1
```

If exit code is 0 (`gh` is installed and authenticated):

```bash
GH_USER=$(gh api user --jq .login 2>/dev/null)
```

Append a final body line: `Contributed by @<GH_USER>` (only if `GH_USER` is non-empty).

```bash
gh issue create \
  --repo juanwmedia/cc-tips \
  --title "<title>" \
  --body "<body>" \
  --label contribution
```

The command prints the issue URL on success. Show it to the user.

If `gh auth status` fails OR `gh` command is not found, fall back to browser:

```bash
TITLE_ENC=$(printf '%s' "<title>" | jq -sRr @uri)
BODY_ENC=$(printf '%s' "<body>" | jq -sRr @uri)
URL="https://github.com/juanwmedia/cc-tips/issues/new?title=${TITLE_ENC}&body=${BODY_ENC}&labels=contribution"
open "$URL"
```

Tell the user (in their working language):

> Browser opened with your draft pre-filled. Submit there. If you want attribution, add your GitHub handle to the body before submitting.

## Constraints

- Always show the draft to the user BEFORE submitting. Never submit without approval.
- If the user revises, redraft and re-present.
- Keep the draft concise — the maintainer expands and refines later.
- Never submit without the `contribution` label.
