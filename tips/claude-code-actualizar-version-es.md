---
date: 2026-05-17
type: tip
title_es: "Cómo actualizar Claude Code (depende de cómo lo instalaste)"
title_en: "How to update Claude Code (depends on how you installed it)"
---

> **TL;DR** Comprueba tu versión con `claude --version`. Si lo instalaste con el installer nativo (`curl … | bash`), se actualiza solo en segundo plano. Para forzarlo ahora: `claude update`. Para Homebrew, WinGet, apt, dnf, apk o npm: usa el comando del package manager — o pon `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` y deja que Claude lo haga por ti en Homebrew/WinGet. Configura el canal con `autoUpdatesChannel: "latest"` (default, novedades al día) o `"stable"` (~1 semana de retraso, salta releases con regressions).

Claude Code se actualiza... a veces. Depende de cómo lo instalaste, y eso confunde a más gente de la que parece: la docs oficial no tiene una página "cómo actualizar" dedicada, así que la respuesta vive escondida en distintas secciones del setup avanzado. Aquí está en una sola tabla.

Si llevas meses sin ver una novedad, probablemente estás en el segundo grupo: instalado vía package manager que no se auto-actualiza.

## ¿Tienes que actualizar? Sí

Las novedades llegan cada par de semanas — skills, subagents, agent teams, `/goal`, GitHub Actions, el Agent SDK. El binario nativo mantiene compatibilidad con tu `CLAUDE.md` y tus settings entre versiones, así que el coste de actualizar es básicamente cero. El de no hacerlo es perderte features que probablemente ya están en otros tips de este sitio.

## Comprueba tu versión

```bash
claude --version
# claude-code/2.1.103
```

Compáralo con la última versión publicada o, desde dentro de Claude, usa `/release-notes` (picker interactivo del changelog).

## Cómo actualizar según tu instalación

| Cómo lo instalaste | Auto-update | Cómo actualizar a mano |
|---|---|---|
| **Installer nativo** (`curl … \| bash`) | ✅ En segundo plano | `claude update` |
| **Homebrew** (`brew install --cask claude-code`) | ❌ | `brew upgrade claude-code` |
| **WinGet** (Windows) | ❌ | `winget upgrade Anthropic.ClaudeCode` |
| **apt** (Debian, Ubuntu) | ❌ | `sudo apt update && sudo apt upgrade claude-code` |
| **dnf** (Fedora, RHEL) | ❌ | `sudo dnf upgrade claude-code` |
| **apk** (Alpine) | ❌ | `apk update && apk upgrade claude-code` |
| **npm** (global) | ❌ | `npm install -g @anthropic-ai/claude-code@latest` |

> Importante para npm: NO uses `npm update -g`. Respeta el rango semver del install original y puede no moverte a la última versión.

## Instalar una versión específica (o hacer downgrade)

A veces no quieres la última — quieres una versión concreta, por CI o porque una update reciente rompió algo. El installer nativo acepta versión exacta o canal:

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89

# Windows PowerShell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
```

El canal que elijas al instalar (`latest`, `stable`, o un número exacto) queda como default para futuros auto-updates.

## El truco para los package managers

Si instalaste con Homebrew o WinGet pero quieres que Claude Code se actualice solo, pon esto en tu `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE": "1"
  }
}
```

A partir de ahí, cuando haya nueva versión Claude la instala en segundo plano y te muestra un prompt para reiniciar. apt, dnf y apk siguen requiriendo actualización manual porque necesitan permisos elevados.

## Canal: latest vs stable

Por defecto vas en `"latest"` — novedades al instante. Si alguna regression reciente te ha mordido y prefieres ir más conservador:

```json
{
  "autoUpdatesChannel": "stable"
}
```

`"stable"` va ~1 semana por detrás y salta releases con regressions importantes. Cambias el canal con `/config → Auto-update channel`, o editando el `settings.json` directamente. Para equipos: las [managed settings](https://code.claude.com/docs/en/permissions#managed-settings) imponen canal y `minimumVersion` en toda la organización.

## Pin de versión mínima

Para garantizar que no bajes accidentalmente de una versión concreta (por ejemplo al cambiar de `"latest"` a `"stable"`):

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

Útil en CI o en equipos donde quieres garantizar un piso común.

## Desactivar auto-updates

Si tu red, política interna o paranoia no permite que Claude se actualice solo:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

`DISABLE_AUTOUPDATER` solo apaga el background check — `claude update` sigue funcionando. Para bloquear TODO (incluido el update manual), usa [`DISABLE_UPDATES`](https://code.claude.com/docs/en/env-vars).

## Referencia: env vars y settings

| Variable / setting | Para |
|---|---|
| `claude --version` | Ver versión instalada |
| `claude update` | Forzar update ahora (cualquier install) |
| `autoUpdatesChannel` | `"latest"` o `"stable"` |
| `minimumVersion` | Piso de versión (no permite downgrade) |
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` | Auto-update vía Homebrew/WinGet |
| `DISABLE_AUTOUPDATER=1` | Apaga el background check |
| `DISABLE_UPDATES=1` | Bloquea todos los caminos de update |

## Combina con

- [`/doctor`](/es/tips/claude-code-doctor-diagnostico) — chequea install, versión, MCP y skills cuando algo va raro.
- [Cheat sheet de slash commands](/es/tips/claude-code-slash-commands-cheatsheet) — incluye `/release-notes` y `/config`.

> Documentación oficial: [Update Claude Code](https://code.claude.com/docs/en/setup#update-claude-code)
