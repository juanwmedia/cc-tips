---
date: 2026-04-14
type: tip
title_es: "Plugins en Claude Code: instala funciones con un solo comando"
title_en: "Plugins in Claude Code: Install Features with One Command"
---
> **TL;DR** Claude Code acaba de tener su propia app store. Añades una "tienda" (un marketplace) una vez, exploras lo que hay dentro, e instalas funciones con un solo comando. Skills, hooks, agentes, servidores MCP — todo empaquetado como plugins que instalas y desinstalas como apps en tu móvil.

Esta es la tercera vez que Anthropic aplica este patrón. Primero vino [MCP](/es/tips/claude-code-mcp-configuracion-rapida) a finales de 2024 — un estándar universal para conectar IA con herramientas y datos. Después [Agent Skills](/es/tips/claude-code-captura-patron-skill-en-caliente) en octubre de 2025 — módulos de capacidades empaquetados que cualquier plataforma de IA puede cargar. Ahora los plugin marketplaces — la capa de distribución que une todo.

Antes de los marketplaces, compartir una skill significaba copiar y pegar un archivo `SKILL.md`. Compartir un [subagente personalizado](/es/tips/claude-code-crear-agentes-personalizados) significaba mandar un `.md` por Slack. Compartir [configuración de un servidor MCP](/es/tips/claude-code-mcp-configuracion-rapida) significaba rezar para que todo el mundo tuviera las mismas rutas. Compartir [hooks](/es/tips/claude-code-hooks-automatizar-flujo-trabajo) significaba documentarlos en un README que nadie leía.

Un plugin empaqueta todo eso — skills, agentes, hooks, servidores MCP, servidores LSP — en una unidad instalable. Un marketplace es un catálogo de esos plugins, hospedado donde sea (GitHub, git, local, URL), que los usuarios añaden una vez y exploran.

Resultado:

```
> /plugin marketplace add anthropics/claude-code
> /plugin install commit-commands@anthropics-claude-code
> /commit-commands:commit
```

Tres comandos. De "he oído hablar de esta skill" a "está corriendo en mi terminal."

## Cómo funciona

### **1. El marketplace oficial ya está ahí**

`claude-plugins-official` está disponible automáticamente en el momento que abres Claude Code. No hace falta añadirlo. Abre el browser para ver qué contiene:

```
> /plugin
```

Cuatro pestañas: **Discover** (todos los plugins de todos tus marketplaces), **Installed** (lo que tienes), **Marketplaces** (fuentes de catálogo), **Errors** (si algo se rompió). Pulsa `Tab` para ciclar.

El marketplace oficial tiene integraciones con GitHub, GitLab, Atlassian, Linear, Notion, Figma, Vercel, Supabase, Slack, Sentry, y language servers para C/C++, Go, Java, Python, Rust, Swift, TypeScript, y más.

### **2. Añadir otro marketplace**

Cuatro tipos de fuente, cada una una sola línea:

```bash
# GitHub shorthand (lo más común)
/plugin marketplace add anthropics/claude-code

# URL git completa (GitLab, Bitbucket, self-hosted)
/plugin marketplace add https://gitlab.com/team/plugins.git

# Fijar a una rama o tag específico
/plugin marketplace add anthropics/claude-code#v2.0

# Directorio local (para probar el tuyo)
/plugin marketplace add ./my-marketplace

# URL remota a marketplace.json
/plugin marketplace add https://example.com/marketplace.json
```

Añadir registra el catálogo. Todavía no hay plugins instalados — ese es el siguiente paso.

### **3. Instalar un plugin**

Desde la pestaña Discover del `/plugin`, o directamente:

```bash
/plugin install plugin-name@marketplace-name
```

Los plugins se instalan al scope de usuario por defecto. A través de la UI también puedes instalar a scope de proyecto (compartido con tu equipo vía `.claude/settings.json`) o scope local (solo este repo, no compartido).

Después de instalar, ejecuta `/reload-plugins` para activar sin reiniciar.

### **4. Gestionar marketplaces**

```bash
/plugin marketplace list        # Ver los que tienes
/plugin marketplace update      # Refrescar todos, o nombre para refrescar uno
/plugin marketplace remove name # También desinstala sus plugins
```

Atajo: `/plugin market` funciona en lugar de `/plugin marketplace`. Y `rm` funciona como alias de `remove`.

### **5. Crear tu propio marketplace**

Un marketplace es un repo de git (o directorio local) con un solo archivo: `.claude-plugin/marketplace.json`.

```json
{
  "name": "my-team-tools",
  "owner": { "name": "Team Platform" },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Auto-formato al guardar"
    },
    {
      "name": "deploy-tools",
      "source": { "source": "github", "repo": "team/deploy-plugin" }
    }
  ]
}
```

Push a GitHub. Comparte el nombre del repo. Cualquiera de tu equipo ejecuta `/plugin marketplace add your-org/your-repo` y tiene acceso a todo al instante. Sin copiar y pegar, sin instrucciones de README, sin "asegúrate de que tus rutas coinciden."

## FAQ

**¿Los plugins reemplazan a mis skills manuales en `.claude/skills/`?**

No. Coexisten. Las skills manuales en `.claude/skills/` siguen funcionando exactamente igual. Las skills de plugin viven en `~/.claude/plugins/cache/` y están namespaced: `/my-plugin:my-skill`. Tus personalizaciones locales no se tocan nunca.

**¿Y si ya tengo skills/hooks/agentes configurados a mano?**

Puedes convertirlos en un plugin copiándolos a una estructura de directorio de plugin y publicando a un marketplace — ver [la guía conceptual sobre plugins](/es/tips/claude-code-plugins-instalar-extender) para el layout de carpetas. O mantenlos manuales para siempre. Ambas opciones funcionan.

**¿Puedo usar marketplaces privados?**

Sí. Claude Code usa tus credenciales git existentes para instalaciones manuales. Para auto-updates en background con repos privados, configura `GITHUB_TOKEN`, `GITLAB_TOKEN`, o `BITBUCKET_TOKEN` en tu entorno.

**¿Son seguros?**

Los plugins pueden ejecutar código arbitrario con los privilegios de tu usuario. Trata un marketplace como tratarías instalar un paquete npm — confía en la fuente, revisa qué hay dentro si importa. Las empresas pueden restringir qué marketplaces pueden añadir los usuarios vía managed settings (`strictKnownMarketplaces`).

## Referencia

| Comando | Qué hace |
|---|---|
| `/plugin` | Abre el browser con pestañas (Discover/Installed/Marketplaces/Errors) |
| `/plugin marketplace add <source>` | Añade un catálogo (4 tipos de fuente soportados) |
| `/plugin marketplace list` | Lista los marketplaces configurados |
| `/plugin marketplace update [name]` | Refresca listados de plugins |
| `/plugin marketplace remove <name>` | Elimina un marketplace (desinstala sus plugins) |
| `/plugin install <plugin>@<marketplace>` | Instala un plugin al scope de usuario |
| `/plugin uninstall <plugin>@<marketplace>` | Elimina un plugin |
| `/reload-plugins` | Aplica cambios sin reiniciar |

| Tipo de fuente | Sintaxis |
|---|---|
| GitHub | `owner/repo` o `owner/repo#rama` |
| URL git | `https://gitlab.com/...git` |
| Local | `./ruta/a/marketplace` |
| JSON remoto | `https://example.com/marketplace.json` |

> Documentación oficial: [Descubrir plugins](https://code.claude.com/docs/en/discover-plugins) | [Crear un marketplace](https://code.claude.com/docs/en/plugin-marketplaces) | [Enviar plugin](https://platform.claude.com/plugins/submit)
