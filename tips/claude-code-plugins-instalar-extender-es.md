---
date: 2026-03-22
type: tip
title_es: "Plugins en Claude Code: no es nada nuevo, es empaquetar lo que ya sabes"
title_en: "Claude Code Plugins: Nothing New — Just Packaging What You Already Know"
---
# Quick Tip: Plugins en Claude Code: no es nada nuevo, es empaquetar lo que ya sabes

> **TL;DR** Un plugin de Claude Code no es una nueva tecnología. Es un directorio que empaqueta [skills](/es/articulos/claude-code-skills-flujos-trabajo-personalizados), [subagents](/es/articulos/claude-code-subagents-guia-espanol), [hooks](/es/articulos/claude-code-hooks-guia-practica), MCP servers y configuraciones — todo lo que ya conoces — en un formato instalable y compartible con un solo comando.

Si ves "plugins" y piensas "otra cosa más que aprender", tranquilo. No hay API nueva, ni sintaxis nueva, ni concepto nuevo. Un plugin es literalmente tu directorio `.claude/` empaquetado: las mismas skills, los mismos agentes, los mismos hooks. La diferencia es que ahora puedes compartirlo con tu equipo o con la comunidad con `/plugin install`.

Es como un `package.json` para configuración de Claude Code: un manifiesto que declara qué contiene y una estructura de directorios que Claude Code sabe leer.

Resultado — la estructura de un plugin:

```
mi-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifiesto: nombre, versión, descripción
├── skills/
│   └── code-review/
│       └── SKILL.md          # Skill con su prompt
├── agents/
│   └── reviewer.md           # Subagent personalizado
├── hooks/
│   └── hooks.json            # Hooks de ciclo de vida
├── .mcp.json                 # Servidores MCP
└── settings.json             # Configuración por defecto
```

## Cómo usarlo

### **1. Instalar un plugin existente**

```
/plugin install code-review@claude-plugins-official
```

El marketplace oficial de Anthropic es `claude-plugins-official`. Los equipos pueden crear los suyos propios.

### **2. Crear un plugin desde cero**

```bash
mkdir -p mi-plugin/.claude-plugin
```

```json
// mi-plugin/.claude-plugin/plugin.json
{
  "name": "mi-plugin",
  "description": "Mis workflows de equipo empaquetados",
  "version": "1.0.0"
}
```

Añade skills en `skills/`, agentes en `agents/`, hooks en `hooks/hooks.json`. La misma sintaxis que usas en `.claude/`.

### **3. Probar en local**

```bash
claude --plugin-dir ./mi-plugin
```

Las skills aparecen con namespace: `/mi-plugin:skill-name`.

### **4. Convertir configuración existente a plugin**

Si ya tienes skills y hooks en `.claude/`, es copiar y pegar:

```bash
cp -r .claude/commands mi-plugin/
cp -r .claude/agents mi-plugin/
cp -r .claude/skills mi-plugin/
```

## Referencia

| Componente | Ubicación en plugin | Equivalente standalone |
|---|---|---|
| Skills | `skills/` | `.claude/skills/` |
| Subagents | `agents/` | `.claude/agents/` |
| Hooks | `hooks/hooks.json` | `settings.json` → `hooks` |
| MCP servers | `.mcp.json` | `.mcp.json` del proyecto |
| Settings | `settings.json` | `.claude/settings.json` |
| Manifiesto | `.claude-plugin/plugin.json` | No existe — es lo nuevo |

| Aspecto | Detalle |
|---|---|
| Instalar | `/plugin install nombre@marketplace` |
| Probar local | `claude --plugin-dir ./ruta` |
| Recargar | `/reload-plugins` (sin reiniciar) |
| Namespace | `/nombre-plugin:skill` |
| Versiones | Semver en `plugin.json` |

> Documentación oficial: [Create plugins](https://code.claude.com/docs/en/plugins)
