> **TL;DR** Put the word `workflow` in your prompt (or run the bundled `/deep-research`) and Claude writes a **JavaScript script** that orchestrates up to hundreds of subagents in the background — with the plan and intermediate results **outside its context**, and agents that refute each other until they converge before reporting back. It's a research preview, needs **Claude Code v2.1.154+**, ships on all paid plans (on Pro you enable it in `/config`), and burns meaningfully more tokens: start on a scoped task.

Opus 4.8 dropped today (same price as 4.7, ~4× less likely to let code flaws pass unremarked). But the thing that actually changes *how you work* in Claude Code shipped the same day and isn't the model: **dynamic workflows**. It runs on whatever model you've got selected.

The problem it solves: until now, if you wanted to delegate a huge task to many subagents, **Claude was the orchestrator** — it decided turn by turn what to spawn, and *every intermediate result landed in its context*. That's why it didn't scale past a handful of agents.

## The shift: the plan moves into code

|  | Subagents | Skills | Workflows |
|---|---|---|---|
| What it is | A worker Claude spawns | Instructions Claude follows | A script the runtime executes |
| Who decides what runs | Claude, turn by turn | Claude, following the prompt | The script |
| Where results live | Claude's context | Claude's context | Script variables |
| Scale | A few per turn | Same as subagents | Dozens to hundreds per run |

A workflow moves the plan — the loop, the branching, the state — into a JavaScript script Claude writes on the fly. A runtime executes it **in the background, isolated from your conversation**. Your context only gets the final answer. That buys two things: running hundreds of agents without blowing context, and a **repeatable quality pattern** — agents that adversarially review each other's findings before reporting them.

## Try it today without writing anything: `/deep-research`

The zero-cost on-ramp is a workflow that already ships built in:

```text
/deep-research What changed in the Node.js permission model between v20 and v22?
```

It fans out searches across several angles, cross-checks the sources, **votes on each claim**, and returns a cited report with claims that didn't survive the cross-check already filtered out. Your session stays free while it runs. Track progress with `/workflows`.

## The three ways to launch one

```text
# 1. The word "workflow" in your prompt (Claude writes the script)
Run a workflow to audit every endpoint under src/routes/ for missing auth checks

# 2. A bundled workflow
/deep-research <question>

# 3. Let Claude decide (opt-in)
/effort ultracode
```

With `ultracode`, Claude decides on its own whether each task warrants a workflow — opt-in, lasts the session, drop back with `/effort high` for routine work. By default it does **not** spin up agent fleets unless you ask.

**The control:** before anything runs, Claude shows you the planned phases and you can read the raw script (`Ctrl+G`). It's not a black box. And if a run does what you wanted, press `s` in `/workflows` and it's saved as `/your-command` forever — on every branch, for every teammate who pulls. This is the "skills 2.0" feel.

## What it's actually for

Migrations across hundreds of files, security or bug audits across a whole codebase, research with cross-checked sources. The extreme case: Jarred Sumner ported **Bun from Zig to Rust** with workflows — 750,000 lines, 99.8% of the test suite passing, 11 days from first commit to merge, hundreds of agents in parallel with two reviewers per file.

## What to know first (honest)

- **Research preview** · needs **v2.1.154+** · all paid plans (on Pro, enable in `/config`)
- **Limits:** max 16 concurrent agents, 1,000 total per run
- **Cost:** a run burns meaningfully more tokens than doing the task in conversation. Anthropic says it plainly: start on a scoped task to get a feel for it
- Subagents run in `acceptEdits` and inherit your allowlist; file edits are auto-approved

If you came from [parallel worktrees](/en/tips/claude-code-worktrees-parallel-tasks) or the [background agents map](/en/tips/claude-code-background-agents-map), workflows are the next rung: not several of your own sessions, but one that orchestrates hundreds of agents with the plan held in code.

> Official docs: [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
