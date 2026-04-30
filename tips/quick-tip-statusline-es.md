---
date: 2026-02-21
type: tip
title_es: "Personaliza tu Status Line en Claude Code"
title_en: "Customize Your Claude Code Status Line"
---

# Quick Tip: Personaliza tu Status Line en Claude Code

Claude Code te permite personalizar la barra de estado inferior con un script de shell — como el PS1 de tu terminal, pero para tu sesión de IA.

Con ~50 líneas de bash tienes: modelo, directorio, rama git, diff stats, coste de sesión y una barra de uso de ventana de contexto — todo con colores ANSI.

Resultado:

```
╸ mi-proyecto  main │ Opus │ +156 -23 │ $0.12 │ ██░░░ 35%
```

## Setup

**1. Crea el script**

```bash
#!/bin/bash
input=$(cat)

# --- Extraer datos ---
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir' | xargs basename)
ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
CTX_PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Rama git
BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    B=$(git branch --show-current 2>/dev/null)
    [ -n "$B" ] && BRANCH="$B"
fi

# --- Colores ANSI ---
RST="\033[0m"
DIM="\033[2m"
BOLD="\033[1m"
CYAN="\033[36m"
GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
MAGENTA="\033[35m"
BLUE="\033[34m"

# --- Barra de contexto (5 bloques) ---
filled=$((CTX_PCT / 20))
empty=$((5 - filled))
BAR=""
for ((i=0; i<filled; i++)); do BAR+="█"; done
for ((i=0; i<empty; i++)); do BAR+="░"; done

if [ "$CTX_PCT" -ge 80 ]; then
    BAR_COLOR="$RED"
elif [ "$CTX_PCT" -ge 50 ]; then
    BAR_COLOR="$YELLOW"
else
    BAR_COLOR="$GREEN"
fi

# --- Construir línea ---
OUT=""
OUT+="${DIM}╸${RST} "
OUT+="${BOLD}${CYAN}${DIR}${RST}"
[ -n "$BRANCH" ] && OUT+=" ${MAGENTA} ${BRANCH}${RST}"
OUT+=" ${DIM}│${RST} ${BLUE}${MODEL}${RST}"
OUT+=" ${DIM}│${RST} ${GREEN}+${ADDED}${RST} ${RED}-${REMOVED}${RST}"
OUT+=" ${DIM}│${RST} ${DIM}\$${RST}${COST}"
OUT+=" ${DIM}│${RST} ${BAR_COLOR}${BAR}${RST} ${DIM}${CTX_PCT}%${RST}"

echo -e "$OUT"
```

Guárdalo como `~/.claude/statusline.sh` y dale permisos:

```bash
chmod +x ~/.claude/statusline.sh
```

**2. Actívalo en settings**

Añade a `.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

Reinicia Claude Code.

## Qué muestra cada segmento

| Segmento | Qué es |
|---|---|
| `╸ mi-proyecto` | Directorio actual (cyan, bold) |
| ` main` | Rama git (magenta, solo dentro de un repo) |
| `Opus` | Modelo activo (azul) |
| `+156 -23` | Líneas añadidas/eliminadas en la sesión (verde/rojo) |
| `$0.12` | Coste de la sesión en USD |
| `██░░░ 35%` | Uso de ventana de contexto (verde < 50%, amarillo 50-80%, rojo > 80%) |

## Requisitos

- `jq` instalado (`brew install jq` / `apt install jq`)
- Terminal con soporte ANSI (básicamente todas)

## Cómo funciona

Claude Code envía un JSON con metadatos de la sesión al stdin de tu script cada vez que la conversación se actualiza (máximo cada 300ms). Tu script lo lee, extrae lo que necesita, e imprime una línea por stdout. Esa línea se convierte en la barra de estado. Los códigos ANSI están soportados.

El esquema JSON completo está documentado en [Status line configuration](https://code.claude.com/docs/en/statusline) — incluye info del modelo, rutas del workspace, tracking de costes y uso de ventana de contexto.
