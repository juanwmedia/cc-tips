---
date: 2026-04-28
type: tip
title_es: "Allowlist automática en Claude Code: deja que se escriba sola"
title_en: "Automatic allowlist in Claude Code: let it write itself"
---
> **TL;DR** El skill oficial `/fewer-permission-prompts` analiza tu historial de sesiones, detecta qué comandos read-only apruebas una y otra vez, y los añade a `.claude/settings.json` como allowlist priorizada. Sin tocar el JSON a mano.

Si no usas [auto mode](/es/tips/claude-code-auto-mode-alternativa-yolo) pero estás harto de aprobar `npm run typecheck` por enésima vez, este skill es tu atajo. Anthropic lo lanzó justamente para quienes prefieren mantener [los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab) y la fricción manual, pero sin la fatiga de pulsar "y" cada minuto.

## Cómo funciona internamente

Cuando ejecutas `/fewer-permission-prompts`, Claude Code:

1. Localiza tus transcripts en `~/.claude/projects/<dir>/*.jsonl` (cap a las 50 sesiones más recientes).
2. Extrae cada llamada Bash y MCP, agrupa por comando + primer subcomando: `git log`, `gh pr view`, `mcp__slack__read_thread`.
3. Filtra a read-only puro: descarta `rm`, `git push`, `npm install`, builds con efectos secundarios.
4. Descarta los que Claude Code ya auto-aprueba sin allowlist (`cat`, `ls`, `git status`, `gh pr view`, `docker logs`...).
5. Bloquea wildcards peligrosos: `Bash(python3:*)`, `Bash(bun run *)`, `sudo`, intérpretes y shells — todo lo que dé ejecución arbitraria.
6. Rankea por frecuencia, corta lo que aparece menos de 3 veces, te muestra el top 20.

## El resultado

```text
| # | Pattern                          | Count | Notes                |
|---|----------------------------------|-------|----------------------|
| 1 | Bash(npm run typecheck)          | 87    | type-check loops     |
| 2 | Bash(git log *)                  | 54    | history exploration  |
| 3 | mcp__wmedia__get-tip-tool        | 31    | tip lookups          |
```

Y el `.claude/settings.json` del proyecto queda así (preservando lo que ya hubiera):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run typecheck)",
      "Bash(git log *)",
      "mcp__wmedia__get-tip-tool"
    ]
  }
}
```

## Cómo lo invocas

```bash
/fewer-permission-prompts
```

Es un skill built-in en Claude Code (v2.1+). No instala nada, no requiere configuración. Genera la tabla, te explica qué añade y qué descarta, y escribe en el `.claude/settings.json` del proyecto actual — no en el global `~/.claude/settings.json` ni en `.claude/settings.local.json`.

Si el skill parece "no encontrar" comandos que ejecutas a diario (`ls`, `cat`, `git status`, `gh pr view`...) es buena señal: ya están auto-aprobados sin necesidad de entrada en el allowlist.

## Patrones de allowlist que verás

| Forma | Cuándo se usa |
|---|---|
| `Bash(foo)` | Match exacto, una invocación específica |
| `Bash(foo *)` | Prefijo + espacio: matchea `foo`, `foo bar`, `foo --opt` |
| `Bash(foo*)` | Sin espacio: cuidado, `Bash(ls*)` también matchea `lsof` |
| `mcp__server__tool` | Nombre completo de tool MCP, sin wildcards |

> Documentación oficial: [Configure permissions](https://code.claude.com/docs/en/permissions)
