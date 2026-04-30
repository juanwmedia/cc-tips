---
date: 2026-04-25
type: tip
title_es: "Olvídate de los permisos en Claude Code sin caer en modo YOLO"
title_en: "Escape Claude Code's permission fatigue without going YOLO"
---

> **TL;DR** Auto mode puts a classifier between Claude and your machine: safe actions execute without prompting, risky ones get blocked. It's what `--dangerously-skip-permissions` should have been. I retired my YOLO alias the day I tried it.

Auto mode shipped as a research preview a few weeks ago and most people still living on `--dangerously-skip-permissions` (the famous YOLO mode) haven't moved. That's a mistake: it does almost everything YOLO does, with a separate model checking each tool call before it runs.

Think of it as a security guard. YOLO has no guard, everything walks through. Auto mode has a classifier (a Sonnet 4.6 running on the side) that reviews each action and only lets the safe ones pass.

Result:

```
> Shift+Tab → mode: ⚡ auto

✓ Edit src/auth.ts
✓ Run npm test
✓ Run git commit -m "fix login"
✗ Run git push origin main         (blocked: pushing directly to main)
↪ Claude will try: git push origin feature/login
✓ Run git push origin feature/login
```

Zero "(y)es" pressed for the entire session, and you still won't get an `rm -rf` slipped past or a push to production.

## **1. Turning it on**

If your account meets the requirements, Auto shows up in the `Shift+Tab` cycle automatically. The first time you cycle to it you get an opt-in prompt:

```
default → acceptEdits → plan → auto

⚡ auto mode (research preview)
   [Yes, enable]  [No, don't ask again]
```

There's no `--enable-auto-mode` flag (that flag is gone in recent versions). Meet the requirements and it's just there.

**Exact requirements:**

| Type | What you need |
|---|---|
| Version | Claude Code 2.1.83 or later |
| Plan | Max, Team, Enterprise, or API. Pro is out. |
| Model | Sonnet 4.6, Opus 4.6, or Opus 4.7. On Max **only Opus 4.7** works. |
| Provider | Anthropic API. Doesn't work on Bedrock, Vertex, or Foundry. |
| Admin (Team/Enterprise) | An admin must enable it in the panel before users can turn it on. |

If Auto says "unavailable" while you believe you meet everything, it's not a transient outage — one of the requirements is missing.

## **2. What the classifier lets through and what it blocks**

**Passes silently:**
- Edits and reads inside your working directory
- Installing dependencies declared in lockfiles or manifests
- Reading `.env` and sending credentials to their matching API
- Read-only HTTP requests
- Pushing to the branch you started on or one Claude created

**Blocked by default:**
- `curl | bash` and download-and-execute patterns
- Sending sensitive data to external endpoints
- Production deploys and migrations
- Mass deletion on cloud storage
- Granting IAM or repo permissions
- Force push, or pushing directly to `main`
- Irreversibly destroying files that existed before the session

To see the full rule lists: `claude auto-mode defaults`.

## **3. The hidden feature: conversational boundaries**

This isn't in the release note and it's the most useful thing about Auto mode after the classifier itself.

If at any point you tell Claude "don't push" or "wait until I review before deploying", the classifier treats that sentence as a **deny rule** for the rest of the session. It re-reads the transcript on each check.

```
You: it's Friday, don't touch production this afternoon
Claude: understood.

[hours later, Claude proposes a deploy]
✗ Run aws ecs update-service ... (blocked: user asked to skip prod)
```

**Watch out for context compaction**: boundaries live in the transcript. If you compact and the message goes, the boundary goes too. For a real hard guarantee, write a `deny rule` in `.claude/settings.json` instead.

## **4. The other hidden feature: broad allow rules dropped automatically**

If your `settings.json` has rules like `Bash(*)` or `Bash(python*)` — the lazy shortcut — when you enter Auto mode Claude **drops them automatically**. They come back when you leave.

```
allow:
  Bash(*)              # ⚠️ dropped on entering Auto
  Bash(npm test)       # ✓ this carries over (it's narrow)
  Agent(my-agent)      # ⚠️ also dropped
```

It does this because `Bash(*)` would effectively disable the classifier. Narrow rules (`Bash(npm test)`, `Bash(git commit *)`) stay — those are intentional.

## **5. When Auto gives up**

If the classifier blocks **3 actions in a row or 20 total**, Auto pauses and you're back to manual prompts. Not configurable. If it happens often, usually it means your admin needs to declare your infra as trusted in `autoMode.environment`.

## **6. When YOLO still makes sense**

`--dangerously-skip-permissions` still has a niche:
- Ephemeral containers without internet
- Isolated VMs / sandboxes
- CI runs with tight scope where you want raw speed

On your daily-driver machine, there's no reason to keep using YOLO if Auto is available. Auto gives you 95% of the flow without the risk.

## Auto vs YOLO

| | `auto` | `bypassPermissions` (YOLO) |
|---|---|---|
| Prompts | No | No |
| Classifier before every action | ✓ | ✗ |
| Blocks force push, mass delete, prod deploys | ✓ | ✗ |
| Honors "don't push" in chat | ✓ | ✗ |
| Drops broad allow rules | ✓ | ✗ |
| Cost per session | Slightly higher | Same as normal |
| Safe on host machine | ✓ | ✗ (containers only) |

I used YOLO via a `claude-yolo` alias for months. When Auto shipped I tried it expecting the classifier to slow me down. You barely notice it: on long tasks it intervenes once every twenty actions, and when it does, it's almost always right. The alias is still there. I don't use it anymore.

> **For the full 6-mode rundown**, see [Control How Much Autonomy Claude Code Gets with 6 Permission Modes](/en/tips/claude-code-permission-modes-shift-tab). To understand how modes combine with `/permissions`, see [3 Things You Must Know About /permissions in Claude Code](/en/tips/claude-code-permissions-3-key-concepts).

> Official docs: [Permission modes](https://code.claude.com/docs/en/permission-modes) | [Auto mode engineering blog (Anthropic)](https://www.anthropic.com/engineering/claude-code-auto-mode)
