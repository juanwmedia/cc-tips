---
date: 2026-06-29
type: tip
title_es: "Tu límite de uso de Claude Code, siempre a la vista en la status line"
title_en: "Your Claude Code usage limit, always in sight in the status line"
---

> **TL;DR** El JSON que recibe tu status line trae `rate_limits` con dos ventanas, `five_hour` y `seven_day`, cada una con `used_percentage` y `resets_at`. Léelas con `jq` y pinta el porcentaje en la barra. Solo aparece en suscripción (Pro/Max) y tras la primera respuesta de la sesión, así que maneja la ausencia con `// empty`.

Trabajas con Pro o Max. En mitad de una tarea larga, el límite de 5 horas se agota y Claude se detiene. Sin aviso previo. Existe `/usage`, pero tienes que parar, escribirlo y leerlo. El dato ya viene en cada respuesta de la sesión: ponlo en la status line y lo ves sin levantar la vista del código.

## Cómo funciona

Claude Code envía a tu script de status line un JSON por stdin. Desde hace poco incluye `rate_limits`, con dos ventanas:

```json
"rate_limits": {
  "five_hour":  { "used_percentage": 23.5, "resets_at": 1738425600 },
  "seven_day":  { "used_percentage": 41.2, "resets_at": 1738857600 }
}
```

`used_percentage` va de 0 a 100. `resets_at` es epoch en segundos (cuándo se reinicia la ventana).

Resultado:

```
my-project  main ✦   5h 24% · 7d 41%
```

En verde mientras vas holgado, en rojo cuando te acercas al muro.

## Cómo montarlo

### **1. Apunta la status line a tu script**

En `~/.claude/settings.json`:

```json
{
  "statusLine": { "type": "command", "command": "~/.claude/statusline.sh" }
}
```

### **2. Lee las dos ventanas en el script**

```bash
#!/usr/bin/env bash
in=$(cat)
fh=$(jq -r '.rate_limits.five_hour.used_percentage // empty' <<<"$in")
sd=$(jq -r '.rate_limits.seven_day.used_percentage // empty' <<<"$in")

# Solo Pro/Max, y solo tras la primera respuesta: si no está, no pintes nada
[ -z "$fh" ] && exit 0

bar() {                       # $1 = porcentaje
  local p=${1%.*} c
  if   [ "$p" -ge 80 ]; then c=31   # rojo
  elif [ "$p" -ge 50 ]; then c=33   # amarillo
  else                       c=32   # verde
  fi
  printf '\033[%sm%s%%\033[0m' "$c" "$p"
}

printf '5h %s · 7d %s' "$(bar "$fh")" "$(bar "${sd:-0}")"
```

### **3. El `// empty` no es opcional**

`rate_limits` solo existe en suscripción Claude.ai (Pro/Max) y aparece **tras la primera respuesta** de la sesión. Cada ventana puede faltar por separado. Sin el `// empty` y el `exit 0`, al arrancar verías una status line rota hasta el primer mensaje.

## Referencia

| Campo | Qué es |
|---|---|
| `rate_limits.five_hour.used_percentage` | % consumido de la ventana de 5 horas (0–100) |
| `rate_limits.seven_day.used_percentage` | % consumido de la ventana de 7 días |
| `rate_limits.five_hour.resets_at` | Epoch (s) en que se reinicia la ventana de 5h |
| `rate_limits.seven_day.resets_at` | Epoch (s) en que se reinicia la de 7 días |

Para una cuenta atrás, resta `resets_at` de la hora actual: `jq -r '.rate_limits.five_hour.resets_at'` y formatéalo con `date`.

> Documentación oficial: [Status line — rate limit usage](https://code.claude.com/docs/en/statusline)

Esto extiende el [script de status line](/es/tips/personaliza-tu-status-line-en-claude-code) con los campos que casi nadie usa. Si lo que quieres es el desglose de qué se come tu límite, eso es trabajo de `/usage`; esto es el vistazo permanente.

## Requisitos

- Claude Code v2.1.x, `jq`, y plan con suscripción (Pro/Max). En cuenta de API no hay `rate_limits`.
