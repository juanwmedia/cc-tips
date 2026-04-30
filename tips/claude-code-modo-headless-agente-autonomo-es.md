---
date: 2026-03-05
type: tip
title_es: "Claude Code puede trabajar mientras duermes"
title_en: "Claude Code Can Work While You Sleep"
---
# Quick Tip: Claude Code puede trabajar mientras duermes

Claude Code no es solo un asistente interactivo. Con el flag `-p` (print), se convierte en un agente headless que puedes lanzar desde scripts, pipelines de CI/CD, o — y aquí viene lo interesante — desde un cron job.

La diferencia con un script normal es que Claude no ejecuta pasos fijos: **razona sobre el contexto en el momento y decide qué hacer**. Combinado con `--allowedTools` para controlar sus permisos, tienes un agente AI completamente autónomo que trabaja mientras duermes.

> **TL;DR** `claude -p "prompt" --allowedTools "Read" "Bash(curl *)"` convierte a Claude en un agente autónomo que puedes programar con cron. No es un script estático — es un agente que razona y toma decisiones.

Ejemplo — cron job que revisa logs de staging cada noche:

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

## Cómo funciona

### **1. Uso básico**

```bash
# Prompt directo
claude -p "explain this function"

# Piping de stdin
cat error.log | claude -p "explain these errors and suggest fixes"

# Continuar una sesión anterior
claude -c -p "check for type errors in the last changes"
```

El flag `-p` desactiva la interfaz interactiva. Claude procesa el prompt, ejecuta las acciones necesarias y devuelve el resultado a stdout.

### **2. Controlar los permisos**

```bash
# Solo lectura — análisis sin riesgo
claude -p "audit this codebase" --allowedTools "Read" "Glob" "Grep"

# Lectura + HTTP — puede notificar pero no modificar
claude -p "check health" --allowedTools "Read" "Bash(curl *)"

# Todo permitido (cuidado)
claude -p "fix all lint errors" --dangerously-skip-permissions
```

`--allowedTools` es la clave de la automatización segura. Define exactamente qué herramientas puede usar Claude, con pattern matching para comandos específicos.

### **3. Limitar coste y ejecución**

```bash
claude -p "complex analysis" \
  --max-turns 15 \
  --max-budget-usd 1.00
```

`--max-turns` limita cuántas acciones puede tomar. `--max-budget-usd` pone un tope de gasto. Ambos son esenciales para ejecución desatendida.

### **4. Formato de salida para scripts**

```bash
# JSON para parsear programáticamente
claude -p "list all TODO comments" --output-format json

# Streaming JSON para procesamiento en tiempo real
claude -p "analyze" --output-format stream-json
```

## Referencia

| Flag | Qué hace | Ejemplo |
|---|---|---|
| `-p` / `--print` | Activa el modo headless | `claude -p "query"` |
| `--allowedTools` | Herramientas permitidas | `--allowedTools "Read" "Bash(curl *)"` |
| `--max-turns` | Límite de acciones | `--max-turns 10` |
| `--max-budget-usd` | Tope de gasto | `--max-budget-usd 0.50` |
| `--output-format` | Formato de salida | `--output-format json` |
| `--dangerously-skip-permissions` | Salta todos los permisos | Usar con precaución |

> Official docs: [Ejecutar Claude Code programáticamente](https://code.claude.com/docs/es/headless)
