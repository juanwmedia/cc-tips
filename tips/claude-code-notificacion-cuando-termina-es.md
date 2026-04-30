---
date: 2026-03-06
type: tip
title_es: "Haz que Claude Code te avise cuando termine (sin molestar)"
title_en: "Get Notified When Claude Code Finishes (Only When You're Not Looking)"
---
# Quick Tip: Haz que Claude Code te avise cuando termine (sin molestar)

Claude Code tiene un evento llamado `Stop` que se dispara cada vez que termina de responder. Puedes conectarle un [hook](/es/articulos/claude-code-hooks-guia-practica) que ejecute cualquier comando del sistema — incluido un sonido. El truco está en que solo suene cuando no estás mirando la terminal, para no volverse loco con cada respuesta corta.

El hook usa `osascript` para preguntar a macOS qué app tiene el foco. Si no es tu terminal, reproduce un sonido del sistema. Si estás en la terminal, silencio.

> **TL;DR** Un hook `Stop` + un script que comprueba la app en foco = sonido solo cuando estás en otra app. Cero notificaciones molestas.

Resultado — el script completo:

```bash
#!/bin/bash
# ~/.claude/notify-stop.sh
# Notify when Claude finishes — only if the terminal is not in focus

FRONTMOST=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)

# Warp se identifica como "stable", no como "Warp"
if [ "$FRONTMOST" != "Warp" ] && [ "$FRONTMOST" != "stable" ]; then
  afplay /System/Library/Sounds/Glass.aiff &
fi
```

## Configuración

### **1. Crear el script**

```bash
cat > ~/.claude/notify-stop.sh << 'EOF'
#!/bin/bash
FRONTMOST=$(osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' 2>/dev/null)

if [ "$FRONTMOST" != "Warp" ] && [ "$FRONTMOST" != "stable" ]; then
  afplay /System/Library/Sounds/Glass.aiff &
fi
EOF
chmod +x ~/.claude/notify-stop.sh
```

Si usas otra terminal, cambia `"Warp"` y `"stable"` por el nombre de tu app. Para descubrir cómo se identifica, ejecuta:

```bash
osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'
```

### **2. Registrar el hook**

Añade esto a tu `~/.claude/settings.json` (global, para todos los proyectos):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/notify-stop.sh"
          }
        ]
      }
    ]
  }
}
```

### **3. Elegir otro sonido (opcional)**

macOS incluye varios sonidos en `/System/Library/Sounds/`. Algunos:

```bash
# Escuchar las opciones
afplay /System/Library/Sounds/Ping.aiff
afplay /System/Library/Sounds/Pop.aiff
afplay /System/Library/Sounds/Purr.aiff
afplay /System/Library/Sounds/Hero.aiff
afplay /System/Library/Sounds/Submarine.aiff
```

## Referencia

| Concepto | Detalle |
|---|---|
| Evento `Stop` | Se dispara cuando Claude termina de responder. No se dispara si el usuario interrumpe. |
| `osascript` | Permite consultar a macOS qué app tiene el foco via AppleScript. |
| `afplay` | Reproductor de audio nativo de macOS. El `&` al final evita bloquear a Claude. |
| Warp = "stable" | Warp se identifica como "stable" en System Events, no como "Warp". Gotcha común. |
| Ubicación del hook | `~/.claude/settings.json` para global, `.claude/settings.json` para un proyecto. |

> Official docs: [Guía práctica de hooks](https://code.claude.com/docs/es/hooks-guide)

## Requisitos

- macOS (el script usa `osascript` y `afplay`)
- Para Linux: sustituir `osascript` por `xdotool` y `afplay` por `paplay`
