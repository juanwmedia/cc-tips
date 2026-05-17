---
date: 2026-05-17
type: tip
title_es: "Cómo actualizar Claude Code (depende de cómo lo instalaste)"
title_en: "How to update Claude Code (depends on how you installed it)"
---

> **TL;DR** Check your version with `claude --version`. If you installed via the native installer (`curl … | bash`), it auto-updates in the background. Force an update now with `claude update`. For Homebrew, WinGet, apt, dnf, apk or npm: use the package manager's own upgrade command — or set `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` and let Claude run it for you (Homebrew/WinGet). Pick a release channel with `autoUpdatesChannel: "latest"` (default, new features immediately) or `"stable"` (~1 week behind, skips releases with major regressions).

Claude Code updates itself... sometimes. It depends on how you installed it, and that confuses more people than you'd think: the official docs don't have a dedicated "how to update" page, so the answer lives scattered across different sections of the advanced setup. Here it is in one table.

If you haven't seen a new feature in months, you're probably in the second group: package-manager install that doesn't auto-update.

## Do you have to update? Yes

New features ship every couple of weeks — skills, subagents, agent teams, `/goal`, GitHub Actions, the Agent SDK. The native binary keeps backwards compatibility with your `CLAUDE.md` and your settings across versions, so the cost of updating is basically zero. The cost of not updating is missing features that probably already have their own tips on this site.

## Check your version

```bash
claude --version
# claude-code/2.1.103
```

Compare against the latest published version, or from inside Claude run `/release-notes` (interactive changelog picker).

## How to update (by install method)

| How you installed | Auto-update | Manual update command |
|---|---|---|
| **Native installer** (`curl … \| bash`) | ✅ Background | `claude update` |
| **Homebrew** (`brew install --cask claude-code`) | ❌ | `brew upgrade claude-code` |
| **WinGet** (Windows) | ❌ | `winget upgrade Anthropic.ClaudeCode` |
| **apt** (Debian, Ubuntu) | ❌ | `sudo apt update && sudo apt upgrade claude-code` |
| **dnf** (Fedora, RHEL) | ❌ | `sudo dnf upgrade claude-code` |
| **apk** (Alpine) | ❌ | `apk update && apk upgrade claude-code` |
| **npm** (global) | ❌ | `npm install -g @anthropic-ai/claude-code@latest` |

> Important for npm: do NOT use `npm update -g`. It respects the semver range from the original install and may not move you to the newest release.

## Install a specific version (or downgrade)

Sometimes you don't want the latest — you want a specific version, for CI or because a recent update broke something. The native installer accepts either an exact version or a channel name:

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89

# Windows PowerShell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
```

Whatever channel you pick at install time (`latest`, `stable`, or an exact number) becomes the default for future auto-updates.

## The package-manager trick

If you installed via Homebrew or WinGet but want Claude Code to auto-update anyway, drop this into your `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE": "1"
  }
}
```

From then on, when a new version is available Claude runs the upgrade in the background and shows a restart prompt on success. apt, dnf, and apk still require manual updates because their commands need elevated privileges.

## Channel: latest vs stable

By default you're on `"latest"` — new features as soon as they ship. If a recent regression bit you and you'd rather be conservative:

```json
{
  "autoUpdatesChannel": "stable"
}
```

`"stable"` runs ~1 week behind and skips releases with major regressions. Switch the channel via `/config → Auto-update channel`, or by editing `settings.json` directly. For teams: [managed settings](https://code.claude.com/docs/en/permissions#managed-settings) enforce a channel and `minimumVersion` org-wide.

## Pin a minimum version

To make sure you don't accidentally downgrade past a specific version (for example when switching from `"latest"` to `"stable"`):

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

Useful in CI or teams that want a common floor.

## Disable auto-updates

If your network, internal policy, or paranoia doesn't allow Claude to update itself:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

`DISABLE_AUTOUPDATER` only stops the background check — `claude update` still works. To block everything (including manual updates), use [`DISABLE_UPDATES`](https://code.claude.com/docs/en/env-vars).

## Reference: env vars and settings

| Variable / setting | For |
|---|---|
| `claude --version` | Show installed version |
| `claude update` | Force update now (any install method) |
| `autoUpdatesChannel` | `"latest"` or `"stable"` |
| `minimumVersion` | Version floor (refuses downgrades) |
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` | Auto-update through Homebrew/WinGet |
| `DISABLE_AUTOUPDATER=1` | Turn off the background check |
| `DISABLE_UPDATES=1` | Block every update path |

## Pairs well with

- [`/doctor`](/en/tips/claude-code-doctor-diagnostic) — audits install, version, MCP, and skills when something feels off.
- [Slash commands cheat sheet](/en/tips/claude-code-slash-commands-cheat-sheet) — includes `/release-notes` and `/config`.

> Official docs: [Update Claude Code](https://code.claude.com/docs/en/setup#update-claude-code)
