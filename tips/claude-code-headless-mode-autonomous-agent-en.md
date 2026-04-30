---
date: 2026-03-05
type: tip
title_es: "Claude Code puede trabajar mientras duermes"
title_en: "Claude Code Can Work While You Sleep"
---
# Quick Tip: Claude Code Can Work While You Sleep

Claude Code isn't just an interactive assistant. With the `-p` (print) flag, it becomes a headless agent you can launch from scripts, CI/CD pipelines, or — here's where it gets interesting — from a cron job.

The difference from a regular script is that Claude doesn't execute fixed steps: **it reasons about the current context and decides what to do**. Combined with `--allowedTools` to control its permissions, you get a fully autonomous AI agent that works while you sleep.

> **TL;DR** `claude -p "prompt" --allowedTools "Read" "Bash(curl *)"` turns Claude into an autonomous agent you can schedule with cron. It's not a static script — it's an agent that reasons and makes decisions.

Example — cron job that reviews staging logs every night:

```bash
# crontab -e
0 3 * * * cd /home/deploy/app && claude -p "Review logs/staging.log from the last 24h. \
  If you find errors, create a GitHub issue with the stack trace. \
  If clean, post a summary to Slack via curl." \
  --allowedTools "Read" "Bash(curl *)" "Bash(gh issue create *)" \
  --max-turns 10 \
  --max-budget-usd 0.50 \
  --output-format json >> /var/log/claude-review.log 2>&1
```

## How it works

### **1. Basic usage**

```bash
# Direct prompt
claude -p "explain this function"

# Stdin piping
cat error.log | claude -p "explain these errors and suggest fixes"

# Continue a previous session
claude -c -p "check for type errors in the last changes"
```

The `-p` flag disables the interactive interface. Claude processes the prompt, executes the necessary actions, and returns the result to stdout.

### **2. Control permissions**

```bash
# Read-only — risk-free analysis
claude -p "audit this codebase" --allowedTools "Read" "Glob" "Grep"

# Read + HTTP — can notify but not modify
claude -p "check health" --allowedTools "Read" "Bash(curl *)"

# Everything allowed (be careful)
claude -p "fix all lint errors" --dangerously-skip-permissions
```

`--allowedTools` is the key to safe automation. It defines exactly which tools Claude can use, with pattern matching for specific commands.

### **3. Limit cost and execution**

```bash
claude -p "complex analysis" \
  --max-turns 15 \
  --max-budget-usd 1.00
```

`--max-turns` limits how many actions Claude can take. `--max-budget-usd` caps spending. Both are essential for unattended execution.

### **4. Output format for scripts**

```bash
# JSON for programmatic parsing
claude -p "list all TODO comments" --output-format json

# Streaming JSON for real-time processing
claude -p "analyze" --output-format stream-json
```

## Reference

| Flag | What it does | Example |
|---|---|---|
| `-p` / `--print` | Enables headless mode | `claude -p "query"` |
| `--allowedTools` | Permitted tools | `--allowedTools "Read" "Bash(curl *)"` |
| `--max-turns` | Action limit | `--max-turns 10` |
| `--max-budget-usd` | Spending cap | `--max-budget-usd 0.50` |
| `--output-format` | Output format | `--output-format json` |
| `--dangerously-skip-permissions` | Skip all permissions | Use with caution |

> Official docs: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)
