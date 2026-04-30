---
date: 2026-02-21
type: tip
title_es: "Cómo ajustar el effort level en Claude Code"
title_en: "How to Adjust the Effort Level in Claude Code"
---
# Quick Tip: Cómo ajustar el effort level en Claude Code

Cuando usas `/model` para cambiar de modelo, es fácil pasar por alto el slider que aparece debajo: con las flechas izquierda/derecha puedes ajustar el effort level de Opus 4.6. Ese slider controla cuánto razonamiento invierte Claude antes de responder. No es un límite estricto de tokens — es una señal de comportamiento. En `low`, Claude piensa menos y responde más rápido. En `high` (por defecto), dedica más tokens de razonamiento a problemas complejos.

No confundas effort level con [fast mode](/es/tips/claude-code-fast-mode-respuestas-rapidas). Fast mode acelera la generación de tokens sin reducir la calidad del razonamiento. Bajar el effort sí reduce el razonamiento a cambio de velocidad y coste.

> **TL;DR** Usa `/model` + flechas para ajustar effort sobre la marcha. O configúralo permanentemente con `effortLevel` en settings o la variable de entorno `CLAUDE_CODE_EFFORT_LEVEL`.

Result:

```
> /model

  ● opus
    sonnet
    haiku

  Effort: ◄ ██████░░░░ medium ►
```

## 3 formas de configurar el effort level

### 1. Desde `/model` (interactivo)

Escribe `/model`, selecciona un modelo compatible (actualmente Opus 4.6) y usa las flechas izquierda/derecha para mover el slider de effort:

```
/model
```

El cambio aplica inmediatamente a la sesión actual.

### 2. Variable de entorno

```bash
export CLAUDE_CODE_EFFORT_LEVEL=low
```

Útil para scripts, CI/CD o tareas batch donde sabes de antemano que las operaciones son simples.

### 3. Archivo de configuración

Añade `effortLevel` a tu `settings.json` (usuario o proyecto):

```json
{
  "model": "opus",
  "effortLevel": "medium"
}
```

## Referencia

| Nivel | Razonamiento | Cuándo usarlo |
|---|---|---|
| `low` | Mínimo — respuestas rápidas y baratas | Tareas simples, renombramientos, formateo |
| `medium` | Moderado — equilibrio velocidad/calidad | Desarrollo diario, implementaciones directas |
| `high` | Máximo (por defecto) — razonamiento profundo | Arquitectura, debugging complejo, lógica difícil |

## Cómo monitorizarlo

El effort level no aparece en el JSON que recibe el [status line](/es/tips/personaliza-tu-status-line-en-claude-code) por defecto. Pero puedes leer la variable de entorno directamente desde tu script:

```bash
EFFORT=${CLAUDE_CODE_EFFORT_LEVEL:-high}
```

Y añadirlo a tu status line junto al modelo:

```
╸ my-project  main │ Opus (medium) │ ██░░░ 35%
```

También puedes ver el modelo activo (aunque no el effort) con `/status`.

> Documentación oficial: [Model configuration — Adjust effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level)
