---
date: 2026-04-14
type: tip
title_es: "Controla cuánta autonomía le das a Claude Code con los 6 modos de permisos"
title_en: "Control How Much Autonomy Claude Code Gets with 6 Permission Modes"
---
> **TL;DR** Press `Shift+Tab` to cycle between default, acceptEdits, and plan. Enable auto or bypassPermissions (YOLO mode) with flags. Combine with `/permissions` to pre-allow specific tools. Most people only know two of the six modes — and confuse what acceptEdits actually approves.

This is one of those essential features that gets overlooked because it looks simple — a keyboard shortcut that cycles modes. But the decision of which mode to use when changes how you work with Claude Code fundamentally. And there's a common misconception: acceptEdits does NOT approve everything. It approves file edits and basic filesystem commands. All other Bash commands still prompt.

Six modes, from most restrictive to most autonomous. Each one is a different tradeoff between oversight and flow.

Result:

```
> Shift+Tab

default  →  acceptEdits  →  plan  →  [auto]  →  [bypassPermissions]
                                        ↑              ↑
                                  auto-opts-in    --dangerously-skip
                                  (Max/Team+)    (containers only)
```

## The six modes

### **1. default — Review everything**

```
default — ask before every edit
```

Claude reads files freely but asks before every edit and every command. Use this when you're starting out, working on sensitive code, or don't trust the direction yet.

### **2. acceptEdits — Trust the edits, review the commands**

```
acceptEdits — edit freely, ask for commands
```

Claude creates and edits files without prompting. Also auto-approves common filesystem commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`. All other Bash commands still ask.

**The misconception**: many people think acceptEdits means "approve everything." It doesn't. `npm test`, `git push`, `curl` — all still prompt. If you want to skip those prompts for specific commands without going full auto, you can [set up deny rules and allow wildcards to fine-tune what Claude can touch](/en/tips/claude-code-permissions-3-key-concepts).

### **3. plan — Look but don't touch**

```
plan — research and propose, never touch files
```

Claude explores the codebase and proposes a plan. No source edits. Permission prompts still apply for commands. Enter with `Shift+Tab` or prefix a single prompt with `/plan`.

When the plan is ready, Claude asks how to proceed: approve and switch to auto, approve and accept edits, approve and review manually, or keep refining.

### **4. auto — Claude decides what's safe**

```
auto — background classifier checks every action
```

A separate Sonnet 4.6 classifier evaluates each action before it runs. Safe operations execute silently. Risky ones (deploys, mass deletion, force push, `curl | bash`) are blocked.

**Requirements**: Max, Team, Enterprise, or API plan. Sonnet 4.6, Opus 4.6, or Opus 4.7 — on Max only Opus 4.7 works. Anthropic API only (not on Bedrock, Vertex, or Foundry).

Once your account meets the requirements, Auto appears in the `Shift+Tab` cycle automatically. The first time you cycle to it you'll see a one-time opt-in prompt.

For the classifier internals, conversational boundaries, and dropped allow rules, see [Escape Claude Code's permission fatigue without going YOLO](/en/tips/claude-code-auto-mode-vs-yolo).

### **5. dontAsk — Only pre-approved tools**

```
dontAsk — everything denied unless explicitly allowed
```

Only tools matching your `permissions.allow` rules execute. Everything else is denied without prompting. Designed for CI pipelines and locked-down scripts. If you're building skills that need to [pre-approve their own tools without user intervention](/en/tips/claude-code-allowed-tools-skill-permissions), `allowed-tools` in the skill frontmatter does the same per-skill.

```bash
claude --permission-mode dontAsk
```

Never appears in the Shift+Tab cycle — set it at startup only.

### **6. bypassPermissions — YOLO mode**

```
bypassPermissions — everything runs, no safety net
```

Disables all permission prompts and safety checks. Only writes to protected paths (`.git`, `.zshrc`, `.claude`) still prompt.

```bash
claude --dangerously-skip-permissions
# or equivalently:
claude --permission-mode bypassPermissions
```

**Use only in containers, VMs, or sandboxed environments.** No protection against prompt injection. No classifier. No guardrails. If you run this on your host machine, Claude can `rm -rf ~/` and it will execute.

To add YOLO to the Shift+Tab cycle without activating it immediately:

```bash
claude --allow-dangerously-skip-permissions
```

I switched from YOLO to auto mode the day Auto shipped — most of YOLO's flow with a real safety net. See [Escape Claude Code's permission fatigue without going YOLO](/en/tips/claude-code-auto-mode-vs-yolo) for the full story.

## Combine modes with /permissions

Modes set the baseline. `/permissions` lets you layer specific exceptions on top — pre-approve tools you run constantly so they never prompt, regardless of mode.

```bash
> /permissions
# Add allow rules like:
Bash(npm test)
Bash(git add *)
Bash(git commit *)
```

This is how you stay in default mode for safety but skip the prompt for your most common commands. The rules [carry over between sessions](/en/tips/claude-code-permissions-3-key-concepts) and apply in every mode except bypassPermissions (which skips the permission layer entirely).

## Reference

| Mode | Shift+Tab | Auto-approves | Best for |
|---|---|---|---|
| `default` | Yes (default) | Reads only | Sensitive work, getting started |
| `acceptEdits` | Yes | Reads + file edits + filesystem commands | Code iteration |
| `plan` | Yes | Reads only (no edits) | Exploration, architecture |
| `auto` | After opt-in | Everything (with classifier) | Long tasks (Team+ only) |
| `dontAsk` | Never | Only pre-approved tools | CI, scripts |
| `bypassPermissions` | After opt-in | Everything (no classifier) | Containers, VMs only |

## How to enter each mode

| Method | Example |
|---|---|
| Keyboard | `Shift+Tab` to cycle |
| CLI flag | `claude --permission-mode plan` |
| Default setting | `"permissions": {"defaultMode": "acceptEdits"}` in settings.json |
| Single prompt | `/plan describe the auth flow` |

> Official docs: [Permission modes](https://code.claude.com/docs/en/permission-modes) | [Permissions reference](https://code.claude.com/docs/en/permissions)
