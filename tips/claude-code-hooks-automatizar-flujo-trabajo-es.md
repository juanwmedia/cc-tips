---
date: 2026-02-23
type: tip
title_es: "Hooks en Claude Code — Automatiza Tu Flujo de Trabajo"
title_en: "Claude Code Hooks — Automate Your Workflow"
---
# Quick Tip: Hooks en Claude Code — Automatiza Tu Flujo de Trabajo

Hooks son comandos que se ejecutan automáticamente en puntos concretos del ciclo de vida de Claude Code. A diferencia de las instrucciones en CLAUDE.md (que Claude puede ignorar), los hooks son **deterministas**: si se cumple la condición, se ejecutan siempre. Tres tipos cubren desde validaciones simples hasta verificaciones con IA.

Para una guía completa con 5 hooks esenciales y patrones avanzados, consulta el [artículo completo sobre hooks](/es/articulos/claude-code-hooks-guia-practica).

Resultado:

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\""
      }]
    }]
  }
}
```

## Los 3 tipos de hook

**1. Command — Ejecuta un script**

El más común. Recibe contexto vía stdin como JSON, y el exit code decide el resultado: `0` pasa, `2` bloquea.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo $CLAUDE_TOOL_INPUT | jq -e '.command | test(\"rm -rf|--force|DROP TABLE\") | not'"
      }]
    }]
  }
}
```

Este hook bloquea comandos destructivos como `rm -rf`, `--force` o `DROP TABLE` antes de que se ejecuten.

**2. Prompt — El LLM evalúa**

Para decisiones subjetivas que un script no puede resolver. Claude evalúa el contexto con un prompt en una sola pasada.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "prompt",
        "prompt": "Check that the code follows the project style guide. Block if it introduces console.log statements in production code. $ARGUMENTS"
      }]
    }]
  }
}
```

**3. Agent — Subagente con herramientas**

Para verificaciones complejas. Lanza un subagente con acceso a Read, Grep y Glob que puede inspeccionar archivos antes de decidir.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "agent",
        "prompt": "Verify that every new function has a corresponding test file. Check the test directory for matching test files. Block if tests are missing. $ARGUMENTS"
      }]
    }]
  }
}
```

## Referencia rápida

| Evento | Cuándo se dispara | Uso típico |
|---|---|---|
| `PreToolUse` | Antes de ejecutar una herramienta | Bloquear acciones peligrosas |
| `PostToolUse` | Después de una herramienta exitosa | Formatear, lint, type-check |
| `Notification` | Cuando Claude envía una notificación | Alertas de escritorio personalizadas |
| `Stop` | Cuando Claude termina su respuesta | Validación final, auto-commit |
| `PreCompact` | Antes de comprimir contexto | Re-inyectar instrucciones críticas |
| `SessionStart` | Al iniciar una sesión | Configurar entorno |

| Tipo | IA involucrada | Mejor para |
|---|---|---|
| `command` | No | Validaciones binarias (pasa/falla) |
| `prompt` | Sí (1 pasada) | Decisiones subjetivas |
| `agent` | Sí (multi-turn) | Verificaciones complejas con herramientas |

## Configuración

Los hooks se definen en `settings.json`. Tres niveles de alcance:

- `~/.claude/settings.json` — Todos los proyectos
- `.claude/settings.json` — Proyecto (compartible con el equipo)
- `.claude/settings.local.json` — Proyecto (privado)

La forma más rápida de crear uno: escribe `/hooks` en Claude Code.

**Relacionado:** [Los 6 mecanismos de extensión](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa) · [Skills: comandos personalizados](/es/tips/claude-code-skills-comandos-personalizados) · [Sistema de permisos](/es/tips/claude-code-permisos-3-conceptos-clave)

> Documentación oficial: [Hooks](https://code.claude.com/docs/en/hooks) · [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
