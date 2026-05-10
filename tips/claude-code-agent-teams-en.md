---
date: 2026-05-09
type: tip
title_es: "Agent Teams en Claude Code: varios Claudes que se hablan entre sí"
title_en: "Agent Teams in Claude Code: multiple Claudes talking to each other"
---

> **TL;DR** Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json` and ask Claude to create a team. It spawns N teammates each with their own context, sharing a **task list** and messaging each other through a **mailbox**. **It's not subagents**: subagents report back to the main; teammates collaborate and challenge each other. Sweet spot: 3-5 teammates with 5-6 tasks each. Available since Claude Code `v2.1.32`.

[Subagents](/en/tips/claude-code-subagent-context-loss) do their work and report to the main. Period. They don't talk to each other, don't share tasks, don't push back. For focused tasks with a single output, perfect. But there's a layer above — and almost nobody is using it because it's been experimental behind a flag since early 2026.

The official docs say it [verbatim](https://code.claude.com/docs/en/agent-teams):

> *"Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."*

## Subagents vs Agent Teams

Same principle (parallelize work in separate contexts), different architecture:

| | [Subagents](/en/tips/claude-code-subagent-context-loss) | Agent Teams |
|---|---|---|
| **Communication** | Only report to main agent | Teammates message each other (mailbox) |
| **Coordination** | Main assigns everything | Shared task list + self-claim |
| **Your access** | Through main only | You can talk to any teammate directly |
| **Best for** | Focused tasks, only the result matters | Work that needs discussion and collaboration |
| **Token cost** | Lower (summaries return to main) | Higher (each teammate is a full Claude session) |

**The detail that changes everything**: with Agent Teams, a frontend teammate can DM the backend teammate directly to coordinate an API contract change, without going through the lead. You can't do that with subagents.

## Enable it

In `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your shell. Verify version: `claude --version` must be ≥ `v2.1.32`.

## The example that explains it best (verbatim from docs)

This prompt is straight from Anthropic's docs — it shows what changes with collaborative teammates better than anything:

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk
to each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

What happens when you launch it?

1. The **lead** creates the team and reasons about dependencies before spawning teammates.
2. Each **teammate** starts as a full Claude Code session (own context window, loads `CLAUDE.md`, MCP servers, skills) with a specific prompt.
3. Teammates **message each other by name** through the mailbox to refute theories. Messages arrive automatically.
4. Theories that survive the debate consolidate in the **shared task list**.
5. When a teammate finishes, it **notifies the lead automatically** (idle notification).
6. The lead **synthesizes** findings.

The debate structure is the key mechanism. A single session suffers from **anchoring**: it finds the first plausible explanation and stops looking. Five teammates with competing hypotheses and an explicit mandate to disprove each other → the theory that survives is much more likely to be the actual root cause.

To see what each teammate is doing from your terminal, use **Shift+Down** to cycle through them (in-process mode), or each teammate opens its own pane if you have tmux/iTerm2 (split-panes mode).

## How to control it

### **1. Ask for a team in plain English**

```
Create a team of 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

Claude decides how many teammates to spawn, or you specify the count. Shared task list and mailbox are created automatically.

### **2. Talk to teammates directly**

- **In-process** (default, works in any terminal): press `Shift+Down` to cycle through teammates. Type to send them a message. `Enter` to enter their session, `Esc` to interrupt.
- **Split panes** (requires tmux or iTerm2): each teammate gets its own pane. Click and type. Auto-detects if you're already in tmux.

### **3. Plan approval for risky tasks**

```
Spawn an architect teammate to refactor the auth module.
Require plan approval before they make any changes.
```

The teammate works in plan mode (read-only) until the lead approves. If rejected with feedback, the teammate revises and resubmits.

### **4. Clean up the team when you're done**

```
Clean up the team
```

The lead checks no teammates are active and cleans up resources. **Always from the lead**, never from a teammate.

## The 4 use cases Anthropic recommends

| Case | Why Agent Teams |
|---|---|
| **Research & review** | Each teammate explores a different angle, then they share and challenge findings |
| **New parallel modules** | Each teammate owns an independent piece without stepping on others |
| **Debugging with competing hypotheses** | Like the example above: 5 theories, debate, the robust one wins |
| **Cross-layer (frontend + backend + tests)** | Each layer in a teammate, coordination through the mailbox |

## Caveats you must know

- **Experimental**: the `EXPERIMENTAL_` flag is literal. The API can change.
- **Tokens × N**: each teammate is a full Claude session. More expensive than a single agent or subagents.
- **`/resume` doesn't restore in-process teammates**: after a resume, the lead may try to message teammates that no longer exist. Fix: ask the lead to spawn new ones.
- **Split panes don't work in VS Code's terminal, Windows Terminal, or Ghostty**. There you stay in-process.
- **One team at a time**: clean up before creating another.
- **No nested teams**: teammates can't spawn their own teams.
- **File conflicts**: two teammates editing the same file overwrite each other. Assign different files to each.

## Reference

| Aspect | Detail |
|---|---|
| Minimum version | Claude Code `v2.1.32` |
| Enable | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (settings.json or env) |
| Sweet spot | 3-5 teammates with 5-6 tasks each |
| Components | Team lead · Teammates · Task list · Mailbox |
| Display modes | `auto` (default), `in-process`, `tmux` (split panes) |
| Storage | `~/.claude/teams/<name>/config.json` · `~/.claude/tasks/<name>/` |
| Hook `TeammateIdle` | exit code 2 → **keeps the teammate working** + feedback (won't let it go idle) |
| Hooks `TaskCreated` / `TaskCompleted` | exit code 2 → **blocks** creation or completion + feedback |
| When NOT to use | Sequential tasks, same file, many dependencies → use [subagents](/en/tips/claude-code-subagent-context-loss) or a single session |

> Official docs: [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
