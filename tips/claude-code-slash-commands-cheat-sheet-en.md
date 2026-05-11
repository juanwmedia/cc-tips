---
date: 2026-05-11
type: tip
title_es: "Slash commands en Claude Code: la cheat sheet que las docs no te dan"
title_en: "Slash commands in Claude Code: the cheat sheet the docs don't give you"
---

> **TL;DR** Claude Code has nearly 80 slash commands. The official docs list them **alphabetically**; here they are grouped **by what you want to do**. Starting a session, freeing context, letting Claude work without you, reviewing before merge, debugging when something's off. Typing `/` shows you the ones available to your plan — but knowing where to look saves the 5-minute scroll.

If you landed here from a "claude code slash commands" search, you've probably already seen the official docs: 80 alphabetical entries, one after another. Useful when you know what you want. Useless when what you know is "I want Claude to watch something while I keep coding" but can't remember whether that's `/loop`, `/schedule`, `/monitor`, or `/batch`.

Here they are by intent. Each entry: the command, what it does in one line, and a link to the dedicated tip when we have one.

## 1. When you start a project

| Command | For |
|---|---|
| `/init` | Generate a starter `CLAUDE.md`. `CLAUDE_CODE_NEW_INIT=1` unlocks the interactive flow ([tip](/en/tips/claude-code-init-interactive-flow)) |
| `/login` · `/logout` | Sign in/out of your Anthropic account |
| `/web-setup` | Connect GitHub for [Claude Code on the web](/en/tips/claude-code-cloud-sessions-from-browser) |
| `/install-github-app` | Set up Claude GitHub Actions for a repo |
| `/team-onboarding` | Generate a ramp-up guide of your setup for a new teammate |
| `/setup-bedrock` · `/setup-vertex` | Wizards for AWS Bedrock and Google Vertex AI |
| `/terminal-setup` | Configure Shift+Enter and shortcuts in VS Code, Cursor, Windsurf, Alacritty, Zed |

## 2. While you're working on a task

| Command | For |
|---|---|
| `/model [model]` | Switch model without losing your prompt ([tip](/en/tips/claude-code-choose-right-model)) |
| `/effort [level]` | Dial reasoning up or down. `xhigh` is the sweet spot on Opus 4.7 ([tip](/en/tips/claude-code-effort-level-adjust-reasoning)) |
| `/fast` | Toggle [fast mode](/en/tips/claude-code-fast-mode-faster-responses) |
| `/plan [description]` | Plan mode directly, optionally with the task already written |
| `/branch [name]` | Fork the conversation here, preserve the original ([tip](/en/tips/claude-code-fork-session-branch-conversations)) |
| `/btw <question>` | Side question without polluting history ([tip](/en/tips/claude-code-btw-side-question)) |
| `/copy [N]` | Copy Claude's last reply to clipboard |
| `/diff` | Interactive diff viewer: uncommitted + per-turn |
| `/add-dir <path>` | Add an extra directory to the session |
| `/sandbox` | Toggle [sandbox mode](https://code.claude.com/docs/en/sandboxing) |

## 3. When context fills up

| Command | For |
|---|---|
| `/context` | See where your context window is going ([tip](/en/tips/claude-code-context-command-token-usage)) |
| `/compact [instructions]` | Compress the conversation; optionally with focus ("keep only the plan and the diff") |
| `/clear [name]` | Start a new conversation, the previous one stays in `/resume` |
| `/recap` | One-line summary of the current session ([tip](/en/tips/claude-code-session-recap-resume-context)) |
| `/memory` | Edit `CLAUDE.md` and review auto-memory entries ([tip](/en/tips/claude-code-auto-memory-between-sessions)) |

## 4. When you want Claude to work without you

| Command | For |
|---|---|
| `/loop [interval] [prompt]` | Recurring intra-session. Omit the interval, Claude self-paces ([tip](/en/tips/claude-code-loop-recurring-tasks)) |
| `/schedule [description]` | Create a [Routine](/en/tips/claude-code-routines-cloud-agents) in cloud. Alias `/routines` |
| `/batch <instruction>` | Decompose a refactor into 5-30 parallel PRs ([tip](/en/tips/claude-code-batch-parallel-refactor)) |
| `/ultraplan <prompt>` | Draft a plan in cloud, review in browser ([tip](/en/tips/claude-code-ultraplan-cloud-planning)) |
| `/autofix-pr [prompt]` | Web session that watches your PR and pushes fixes when CI fails |
| `/tasks` | Panel of everything running in parallel. Alias `/bashes` ([tip](/en/tips/claude-code-tasks-panel)) |

To see how they all fit together: [the full map of autonomous primitives](/en/tips/claude-code-loop-routines-monitor-map).

## 5. Before you merge

| Command | For |
|---|---|
| `/review [PR]` | Local review in the session |
| `/ultrareview [PR]` | Cloud review with a parallel fleet of agents ([tip](/en/tips/claude-code-ultrareview)) |
| `/security-review` | Scans the diff for vulnerabilities |
| `/simplify [focus]` | 3 parallel agents review recent files and apply quality/efficiency fixes |

## 6. When something feels off

| Command | For |
|---|---|
| `/doctor` | Audits install, settings, MCP, skills, context. Press `f` and Claude fixes the issues ([tip](/en/tips/claude-code-doctor-diagnostic)) |
| `/debug [description]` | Enables debug logging and analyzes the session log |
| `/heapdump` | Memory snapshot to `~/Desktop` when usage spikes |
| `/feedback [report]` | Report a bug to Anthropic with session context attached. Alias `/bug` |

## 7. Between sessions

| Command | For |
|---|---|
| `/resume [session]` | Open the session picker. Accepts pasting a PR URL to find the session that created it. Alias `/continue` |
| `/rename [name]` | Rename the current session ([tip](/en/tips/claude-code-rename-color-sessions)) |
| `/teleport` | Pull a [Claude Code on the web](/en/tips/claude-code-cloud-sessions-from-browser) session into your terminal. Alias `/tp` |
| `/desktop` | Continue in the Desktop app. Alias `/app` |
| `/remote-control` | Make the session reachable from claude.ai for remote control ([tip](/en/tips/claude-code-remote-control-from-phone)) |
| `/export [file]` | Export the conversation as plain text |

## 8. Metrics and usage

| Command | For |
|---|---|
| `/usage` | Cost, plan limits, stats. Aliases `/cost`, `/stats` ([tip](/en/tips/claude-code-track-usage-stats-dashboard)) |
| `/insights` | Analysis of your sessions: request types, languages, patterns, friction ([tip](/en/tips/claude-code-insights-command)) |
| `/release-notes` | Interactive changelog picker |
| `/extra-usage` | Enable extra usage when you hit the rate limit |

## 9. Customize Claude Code

| Command | For |
|---|---|
| `/config` | Settings UI: theme, model, output style, editor mode, etc. Alias `/settings` |
| `/theme` | Change theme. Includes [creating a custom one](/en/tips/claude-code-custom-themes) |
| `/color` | Change the prompt bar color |
| `/statusline` | Configure the status line |
| `/keybindings` | Edit custom bindings |
| `/agents` | Manage [subagents](/en/tips/claude-code-create-custom-agents) |
| `/hooks` | View configured hooks ([tip](/en/tips/claude-code-hooks-automate-workflow)) |
| `/mcp` | Manage MCP servers ([tip](/en/tips/claude-code-mcp-quick-setup)) |
| `/permissions` | Allow/ask/deny rules ([tip](/en/tips/claude-code-permissions-3-key-concepts)). Alias `/allowed-tools` |
| `/skills` | List skills. Press `t` to sort by tokens, `Space` to hide one |
| `/plugin` | Manage [plugins](/en/tips/claude-code-plugin-marketplace-distribution) |
| `/reload-plugins` | Reload plugins without restarting |

## Slash commands ≠ Skills (the classic mix-up)

**Skills** are markdown files at `~/.claude/skills/<name>/SKILL.md` that Claude runs or auto-activates. They show up in the `/` menu like any other slash command, but you write or install them. **Built-in slash commands** (the tables above) are native Claude Code code, not editable.

A few commands are labeled as bundled skills in docs (`/batch`, `/loop`, `/simplify`, `/debug`, `/fewer-permission-prompts`, `/claude-api`): they ship with Claude Code, but technically they're skills — meaning you can look at their markdown if you want to hack them. For the full mental model: [the 6 extension points](/en/tips/claude-code-skills-hooks-mcp-plugins-comparison).

## Removed commands (in case you're looking for them)

- `/pr-comments` — removed in `v2.1.91`. Replacement: ask Claude to read the PR comments directly.
- `/vim` — removed in `v2.1.92`. Replacement: `/config` → Editor mode.

## The command you already know without knowing it

`/` alone, no text. Shows you the full menu filtered by what you have installed and your plan. Type letters after `/` to filter in real time. If you can't remember the exact name, that's the fastest way — without having to come back to this cheat sheet.

> Official docs: [Commands reference](https://code.claude.com/docs/en/commands)
