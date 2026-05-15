---
date: 2026-05-15
type: tip
title_es: "Servidores MCP en Claude Code: cinco bastan, cincuenta estorban"
title_en: "MCP Servers in Claude Code: five is enough, fifty just slows the agent down"
---

> **TL;DR** More MCPs is not better Claude Code. Every server injects its tool surface into the context and forces the agent to pick from a wider menu each turn. Five well-chosen servers beat any top-fifty ranking. My pick: **GitHub** (issues and PRs), **Context7** (versioned docs, no hallucinations), **Figma Desktop** + **Chrome DevTools** (the autonomous frontend feedback loop), **DBHub** (Postgres, MySQL, SQLite). The rest you install when their absence starts to hurt, not before.

Every blog and Reddit thread offers its "top 50 MCP servers for Claude Code". The uncomfortable truth is that more connectors actively penalize: context fills with tool definitions the agent will never use, the per-turn decision space doubles, and remote servers add latency that compounds when you chain three calls. Anthropic ships Tool Search to mitigate it, but the principle still holds — curation beats catalog.

## The result

```bash
> claude mcp list

  ● github          (http,  connected)
  ● context7        (http,  connected)
  ● figma-desktop   (http,  connected)
  ● chrome-devtools (stdio, connected)
  ● db              (stdio, connected)
```

Five. Enough for 95% of real work.

## The curation

**1. GitHub MCP — step into your repo's workflow**

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Issues, PRs, commits, code search, reviews. Turns Claude Code from "code generator" into "participant in your workflow". Without it, the agent sees files but misses the PR context you're in. With it, you say "implement issue ENG-4521 and open the PR" and it does it end-to-end.

**2. Context7 — real documentation, not hallucinated**

```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
```

The single highest-ROI server per line of config. When the agent is working with a library, Context7 hands it the versioned docs for that library — not the eight-month-old snapshot baked into its weights. Goodbye to "that function doesn't exist in that version". My `CLAUDE.md` has a durable rule: if you're unsure about an API, check Context7 before inventing.

**3. Figma Desktop MCP — design to code with no rate limit**

```bash
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```

The server runs inside your Figma desktop app, not in the cloud — which is why **it has no rate limit**. Open a Figma file, switch to Dev Mode, flip "MCP Server" on in the sidebar, and Claude reads tokens, spacing, components, and variables directly. The advantage over Figma's remote MCP: it doesn't compete with your quota, which matters when the agent iterates twenty times on a single component.

**4. Chrome DevTools MCP — the eye that closes the loop**

```bash
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest
```

The natural partner to Figma Desktop. Claude implements the specs it pulled from Figma, opens Chrome, inspects the actual render, adjusts. Autonomous loop: read design → implement → verify → fix. No "wait while I open the browser" with you in the middle. Any frontier model (Opus 4.7, Sonnet 4.6) uses this combo extensively once it has it on hand — it's the tool that moves the needle most on frontend work.

**5. DBHub — Postgres, MySQL, SQLite, all in one connector**

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

When Claude can query your database instead of asking you for exports, "how many users have X?" goes from five minutes to five seconds. DBHub speaks Postgres, MySQL, SQLite, and more; if you only use Postgres, the official Postgres server is equally fine.

## The rule that matters more than the list

Five is the sane median. Your five isn't my five — it depends on your stack. If you ship to Cloudflare Workers, the Cloudflare MCP earns a slot. If your team lives in Notion or Linear, that MCP outranks DBHub. If you run heavy E2E test suites, Playwright MCP wins over Chrome DevTools. The honest heuristic:

- **Add an MCP only when its absence starts to hurt.** If you've manually copy-pasted the same thing into chat three times, that's the install signal.
- **Drop the ones you don't use.** `claude mcp remove <name>` frees context.
- **Pick the right scope.** Personal workflow servers → `--scope user`. Team servers with project credentials → `--scope project` (lands in `.mcp.json`, committed to git).

For everything else, see the [MCP quick setup](/en/tips/claude-code-mcp-quick-setup) and the [difference between skills, hooks, MCP and plugins](/en/tips/claude-code-skills-hooks-mcp-plugins-comparison).

## Quick reference

| Server | What for | Transport | Command |
|---|---|---|---|
| GitHub | Issues, PRs, code search | HTTP | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| Context7 | Versioned docs | HTTP | `claude mcp add --transport http context7 https://mcp.context7.com/mcp` |
| Figma Desktop | Specs, no rate limit (local) | HTTP | `claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp` |
| Chrome DevTools | Render + inspection | stdio | `claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest` |
| DBHub | Multi-DB queries | stdio | `claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn …` |

> Official docs: [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
