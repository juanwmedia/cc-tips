---
date: 2026-02-21
type: tip
title_es: "3 cosas que debes saber sobre /permissions en Claude Code"
title_en: "3 Things You Must Know About /permissions in Claude Code"
---
# Quick Tip: 3 cosas que debes saber sobre /permissions en Claude Code

El comando `/permissions` parece un menú más. En realidad es la puerta de entrada a un sistema de control de acceso con modos, reglas granulares y orden de evaluación propio. No necesitas dominarlo entero, pero hay tres conceptos que si no conoces te van a morder.

> **TL;DR** Los deny siempre ganan. Los modos cambian el comportamiento de todo. Y la sintaxis `Tool(specifier)` acepta wildcards y patrones gitignore. Con eso, controlas el 90%.

Result:

```bash
/permissions

Allow rules:
  Bash(npm run *)         # from .claude/settings.json
  Bash(git commit *)      # from .claude/settings.json
  Edit(/src/**)           # from .claude/settings.json

Deny rules:
  Bash(git push *)        # from .claude/settings.json
  Read(.env)              # from .claude/settings.json
```

## Los 3 conceptos clave

### 1. El orden de evaluación: deny siempre gana

Las reglas se evalúan en este orden: **deny → ask → allow**. La primera coincidencia gana. Si un deny coincide, no importa cuántos allow tengas — la operación se bloquea.

```json
{
  "permissions": {
    "allow": ["Bash(git *)"],
    "deny": ["Bash(git push *)"]
  }
}
```

En este ejemplo, `git commit -m "fix"` pasa. `git push origin main` se bloquea. El deny para `git push *` coincide antes de que el allow para `git *` tenga oportunidad.

### 2. Los modos cambian todo el comportamiento

Claude Code tiene 5 modos de permisos. Puedes ciclar entre los tres principales con **Shift+Tab** durante la sesión:

| Modo | Qué hace |
|---|---|
| `default` | Pide permiso en cada herramienta nueva |
| `acceptEdits` | Acepta automáticamente ediciones de archivos |
| `plan` | Solo lectura — Claude analiza pero no modifica nada |
| `dontAsk` | Deniega todo lo que no esté explícitamente en allow |
| `bypassPermissions` | Salta todas las comprobaciones (solo en entornos aislados) |

El modo `dontAsk` es el que más confusión genera: no es "acepta todo sin preguntar" sino exactamente lo contrario. Deniega todo excepto lo que hayas pre-aprobado con `/permissions` o en `permissions.allow`.

### 3. La sintaxis acepta más de lo que parece

Las reglas siguen el formato `Tool(specifier)` con wildcards:

| Regla | Qué permite |
|---|---|
| `Bash(npm run *)` | Cualquier script npm |
| `Bash(* --version)` | Cualquier comando con `--version` |
| `Edit(/src/**)` | Editar cualquier archivo bajo `src/` (recursivo) |
| `Read(.env)` | Leer `.env` en el directorio actual |
| `Read(~/.ssh/*)` | Leer archivos en tu directorio `.ssh` |
| `mcp__notion__*` | Cualquier herramienta del servidor MCP Notion |

Para Read y Edit, los patrones siguen la especificación gitignore: `*` coincide en un directorio, `**` es recursivo.

## Dónde se guardan las reglas

| Archivo | Ámbito |
|---|---|
| `~/.claude/settings.json` | Personal — todos tus proyectos |
| `.claude/settings.json` | Proyecto — compartido con el equipo |
| `.claude/settings.local.json` | Proyecto — solo tú (gitignore) |

Las reglas de proyecto tienen precedencia sobre las personales. Si un proyecto deniega algo que tú permites, gana el proyecto.

> Documentación oficial: [Configure permissions](https://code.claude.com/docs/en/permissions)
