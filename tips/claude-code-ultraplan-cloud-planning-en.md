---
date: 2026-04-05
type: tip
title_es: "Planifica en la Nube y Ejecuta Donde Quieras con Ultraplan"
title_en: "Plan in the Cloud and Execute Anywhere with Ultraplan"
---

Some plans don't fit in a terminal. Architecture migrations, deep refactors, decisions that need more than a scrollback buffer to review properly. Ultraplan delegates planning to a [Claude Code on the web](/en/tips/claude-code-cloud-sessions-from-browser) session running in plan mode. Claude drafts the plan in the cloud while your terminal stays free. When it's ready, you review it in a rich browser interface — inline comments, reactions, section navigation — and then choose where to execute: on the web (straight to a PR) or back in your terminal.

> **TL;DR** `/ultraplan migrate the auth service from sessions to JWTs` launches a cloud planning session. Review the plan in your browser with inline comments. Execute on the web or teleport it back to your terminal.

Result:

```
> /ultraplan migrate the auth service from sessions to JWTs

Launching ultraplan session...

◇ ultraplan                      # Claude is researching your codebase
◇ ultraplan needs your input     # Claude has a question — open the link
◆ ultraplan ready                # Plan ready for review in browser
```

## How to use it

### **1. Launch ultraplan from the CLI**

Three ways to start a session:

```bash
# Option A: direct command
/ultraplan migrate the auth service from sessions to JWTs

# Option B: keyword in a normal prompt
I need an ultraplan to refactor the payments system

# Option C: from a local plan
# When Claude finishes a local plan and shows the approval dialog,
# choose "No, refine with Ultraplan on Claude Code on the web"
```

Options A and B show a confirmation dialog before launching. Option C skips it because the selection itself serves as confirmation.

### **2. Monitor progress**

Your terminal shows a status indicator while the remote session works. Run `/tasks` and select the ultraplan entry to see the session link, agent activity, and a **Stop ultraplan** action.

### **3. Review and refine in the browser**

When the status changes to `◆ ultraplan ready`, open the link. The review interface provides:

- **Inline comments**: highlight any passage and leave a comment
- **Emoji reactions**: signal approval or concern without a full comment
- **Outline sidebar**: jump between sections

Iterate as many times as needed before deciding where to execute.

### **4. Choose where to execute**

From the browser you have two paths:

```
Approve Claude's plan and start coding
  → Claude implements in the same cloud session → direct PR

Approve plan and teleport back to terminal
  → The plan returns to your terminal with 3 options:
    • Implement here: inject the plan into your current conversation
    • Start new session: clean conversation with only the plan
    • Cancel: save the plan to a file to return to later
```

## Reference

| Status | Meaning |
|---|---|
| `◇ ultraplan` | Claude is researching the codebase and drafting the plan |
| `◇ ultraplan needs your input` | Claude has a question; open the link to respond |
| `◆ ultraplan ready` | The plan is ready for review in the browser |

| Launch method | Confirmation |
|---|---|
| `/ultraplan <prompt>` | Confirmation dialog |
| `ultraplan` keyword in prompt | Confirmation dialog |
| From approved local plan | No confirmation (selection already confirms) |

| Teleport option | What it does |
|---|---|
| Implement here | Injects the plan into the current conversation |
| Start new session | Clears the conversation, starts fresh with only the plan |
| Cancel | Saves the plan to a file, Claude prints the path |

> Official docs: [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)

## Requirements

- A [Claude Code on the web](/en/tips/claude-code-cloud-sessions-from-browser) account (Pro, Max, Team, or Enterprise)
- GitHub repository
- If Remote Control is active, it disconnects when ultraplan starts (both use the claude.ai/code interface)
