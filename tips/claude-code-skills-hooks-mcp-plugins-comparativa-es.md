---
date: 2026-02-21
type: tip
title_es: "Los 6 mecanismos de extensión de Claude Code que todos confunden"
title_en: "The 6 Extension Points in Claude Code Everyone Confuses"
---
# Quick Tip: Los 6 mecanismos de extensión de Claude Code que todos confunden

Claude Code ofrece seis formas distintas de ampliar su comportamiento: Skills, Hooks, MCP, Sub-agents, Agent Teams y Plugins. Resuelven problemas diferentes, pero sus límites se difuminan rápido. Este tip te da un modelo mental para distinguirlos.

La distinción clave: cada uno responde a una pregunta diferente.

```
¿Qué debe hacer Claude?                            → Skills
¿A qué puede acceder Claude?                       → MCP
¿Quién hace el trabajo?                             → Sub-agents
¿Quién hace el trabajo, en equipo?                  → Agent Teams
¿Cuándo debe pasar algo automáticamente?            → Hooks
¿Cómo empaquetas y compartes todo lo anterior?      → Plugins
```

## Los 6 mecanismos

**1. Skills — Qué debe hacer Claude**

Archivos markdown con instrucciones que Claude ejecuta como slash commands o activa automáticamente cuando son relevantes. Prompts reutilizables con estructura: argumentos, frontmatter, ejecución en subagentes.

```bash
~/.claude/skills/review/SKILL.md → /review src/App.tsx
```

**2. MCP — A qué puede acceder Claude**

Model Context Protocol conecta Claude con herramientas externas: bases de datos, APIs, GitHub, Notion. MCP no le dice a Claude qué hacer — le da manos para llegar fuera de su sandbox.

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**3. Sub-agents — Quién hace el trabajo**

Instancias separadas de Claude que resuelven tareas de forma aislada. Cada una tiene su propia ventana de contexto, herramientas y permisos. Trabajan de forma independiente y devuelven resultados.

```
"Usa el subagente code-reviewer para revisar el módulo de auth"
→ El subagente trabaja aislado → Devuelve resumen
```

**4. Agent Teams — Quién hace el trabajo, en equipo** *(experimental)*

Múltiples instancias de Claude trabajando como equipo coordinado. A diferencia de los sub-agents, los compañeros se envían mensajes entre sí, comparten lista de tareas y cuestionan los hallazgos del otro.

```
"Crea un equipo: uno en seguridad, otro en rendimiento, otro en tests"
→ 3 sesiones independientes → Discusión cruzada → Síntesis
```

**5. Hooks — Cuándo pasan cosas automáticamente**

Comandos shell que se disparan en puntos específicos del ciclo de vida: antes de ejecutar una herramienta, después de editar un archivo, al iniciar sesión. Sin IA — automatización pura.

```json
{ "PostToolUse": [{ "matcher": "Write", "hooks": [{ "type": "command", "command": "npm run lint" }] }] }
```

**6. Plugins — Cómo compartes todo**

Paquetes distribuibles que agrupan skills, agents, hooks y servidores MCP en una unidad instalable. Piensa en paquetes npm pero para extensiones de Claude Code.

```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/        ← skills reutilizables
├── agents/        ← subagentes personalizados
├── hooks/         ← automatización del ciclo de vida
└── .mcp.json      ← conexiones a herramientas externas
```

## Comparativa

| Mecanismo | Pregunta que responde | Se define en | ¿Involucra IA? |
|---|---|---|---|
| Skills | Qué hacer | `SKILL.md` (markdown) | Sí — Claude las sigue |
| MCP | A qué acceder | `.mcp.json` / CLI config | No — puente de protocolo |
| Sub-agents | Quién trabaja | `.claude/agents/` (markdown) | Sí — instancia separada |
| Agent Teams | Quién colabora | Lenguaje natural | Sí — múltiples instancias |
| Hooks | Cuándo automatizar | `settings.json` (JSON) | No — comandos shell |
| Plugins | Cómo distribuir | `.claude-plugin/` (paquete) | No — formato de empaquetado |

> **Tip:** La mayoría de la gente solo necesita Skills y MCP. Añade hooks cuando quieras automatización, sub-agents cuando la ventana de contexto se quede corta, y plugins cuando necesites compartir. Agent Teams es experimental — explóralos cuando los sub-agents no alcancen.

Para una guía completa de Skills con patrones avanzados, consulta el [artículo completo sobre Skills](/es/articulos/claude-code-skills-flujos-trabajo-personalizados).

> Documentación oficial: [Skills](https://code.claude.com/docs/en/skills) · [MCP](https://code.claude.com/docs/en/mcp) · [Sub-agents](https://code.claude.com/docs/en/sub-agents) · [Agent Teams](https://code.claude.com/docs/en/agent-teams) · [Hooks](https://code.claude.com/docs/en/hooks) · [Plugins](https://code.claude.com/docs/en/plugins)
