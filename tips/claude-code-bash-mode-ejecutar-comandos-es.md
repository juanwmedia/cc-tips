---
date: 2026-02-21
type: tip
title_es: "Ejecuta comandos en el terminal sin salir de Claude Code"
title_en: "Run Shell Commands Without Leaving Claude Code"
---
# Quick Tip: Ejecuta comandos en el terminal sin salir de Claude Code

Claude Code tiene un modo bash integrado: escribe `!` seguido de cualquier comando y se ejecuta directamente en tu shell, sin que Claude lo interprete ni lo apruebe. El output aparece en tiempo real y se añade al contexto de la conversación — Claude ve el resultado y puede actuar sobre él.

No es un detalle obvio, pero una vez que lo descubres cambia cómo trabajas. No necesitas abrir otro terminal ni otro panel. Escribes, ejecutas, sigues hablando.

> **TL;DR** Prefija cualquier comando con `!` para ejecutarlo directamente. Usa `Ctrl+B` para enviar procesos largos al background. Claude ve el output de ambos.

Resultado:

```
> ! git status

On branch feature/auth
Changes not staged for commit:
  modified:   src/auth/login.ts
  modified:   src/auth/session.ts
```

## Cómo usarlo

### 1. Ejecutar un comando rápido

Escribe `!` seguido del comando:

```bash
! npm test
! git diff --stat
! ls -la src/
```

Claude no interviene — el comando va directo a tu shell. Pero el resultado se añade a la conversación, así que puedes preguntar "¿qué ha fallado?" inmediatamente después.

### 2. Enviar un proceso largo al background

Si un comando tarda (builds, tests, servidores de desarrollo), pulsa `Ctrl+B` mientras se ejecuta:

```bash
! npm run build
# tarda demasiado → pulsa Ctrl+B
# Claude sigue disponible mientras el build termina en background
```

También puedes pedirle a Claude directamente que ejecute algo en background.

### 3. Autocompletado con historial

Escribe `!` seguido de las primeras letras y pulsa `Tab`. Claude Code autocompleta basándose en comandos `!` anteriores del mismo proyecto.

```bash
! np  → Tab → ! npm test
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Prefijo | `!` al inicio del input |
| Ejecución | Directa en tu shell, sin interpretación de Claude |
| Output | Se muestra en tiempo real y se añade al contexto |
| Background | `Ctrl+B` durante la ejecución (tmux: pulsar dos veces) |
| Autocompletado | `Tab` completa desde historial de comandos `!` del proyecto |
| Permisos | No requiere aprobación — es tu terminal |

> **Nota personal:** Es de esas funciones que no descubres leyendo la doc, sino viendo a alguien usarlo. Estás depurando, necesitas un `git log` rápido o un `cat` de un archivo, y en lugar de saltar a otra pestaña simplemente escribes `! git log --oneline -5`. Parece menor, pero elimina el cambio de contexto constante.

> Documentación oficial: [Interactive mode — Bash mode](https://code.claude.com/docs/en/interactive-mode#bash-mode-with-prefix)
