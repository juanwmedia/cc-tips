---
date: 2026-06-08
type: tip
title_es: "CLAUDE.md, settings.json o .mcp.json: ¿en qué archivo de Claude Code va cada cosa?"
title_en: "CLAUDE.md, settings.json, or .mcp.json: which Claude Code file does this go in?"
---

Tienes que configurar algo nuevo en tu proyecto: que Claude no toque la carpeta `dist/`, que use siempre Opus, que todo el equipo tenga el mismo servidor de Notion conectado. ¿Dónde lo escribes? `CLAUDE.md`, `settings.json`, `.mcp.json`, `settings.local.json`... y la mitad de las veces no tienes claro cuál. Es genuinamente confuso saber para qué es cada archivo, y merece la pena parar cinco minutos a entenderlo, porque poner una regla en el sitio equivocado tiene una consecuencia concreta: no se aplica.

La distinción que ordena casi todo es una sola. **CLAUDE.md son instrucciones que Claude lee como guía. settings.json son reglas que se aplican, siga Claude o no.** Una es contexto que Claude puede seguir o ignorar (al final, es un modelo de lenguaje). La otra es una valla que el motor de Claude Code hace cumplir por ti. Si necesitas que algo *no pueda* ocurrir, no va en CLAUDE.md.

> **TL;DR** Dos preguntas deciden el archivo. **¿Qué tipo de cosa es?** Conocimiento que Claude debe tener en cuenta va en `CLAUDE.md` (lo lee como guía). Una regla que debe cumplirse pase lo que pase (permisos, hooks, modelo) va en `settings.json` (se aplica obligatoriamente). Una herramienta externa va en `.mcp.json`. **¿Para quién es?** Si es para el equipo, se commitea (`settings.json`, `.mcp.json`). Si es solo para ti, va a un archivo gitignored (`settings.local.json`).

Result:

```
Tengo que configurar algo nuevo. ¿En qué archivo va?

  ¿Conocimiento o convenciones que Claude debe leer?
    → CLAUDE.md            se lee como guía, no obliga

  ¿Una regla que SIEMPRE debe cumplirse?
    → settings.json        permisos, hooks, modelo, env

  ¿Una herramienta externa (Notion, GitHub, base de datos)?
    → .mcp.json            en la raíz del proyecto, no dentro de .claude/

  ¿Solo para ti, sin commitear?
    → settings.local.json  override personal, va a .gitignore
```

## Guía contra valla

`CLAUDE.md` se carga al empezar la sesión y se queda en el contexto como instrucciones. Claude las lee y hace lo que puede por seguirlas, pero es un modelo: puede malinterpretarlas, olvidarlas a las 50.000 tokens, o decidir que esta vez no aplican. Si escribes "nunca borres la base de datos" en CLAUDE.md, es una sugerencia muy fuerte. No es una garantía.

`settings.json` es otra cosa. No lo "lee" Claude: lo aplica el motor de Claude Code. Pones `dist/**` en `permissions.deny` y Claude no puede tocar `dist/`, decida lo que decida. Los hooks son scripts que se ejecutan en cada evento, quieras o no. El `model` fija el modelo. Nada de esto depende de que Claude coopere.

La documentación oficial lo resume en una frase que vale la pena recordar: *a diferencia de CLAUDE.md, que Claude lee como guía, los settings se aplican siga Claude las instrucciones o no.*

## Equipo o solo tú

La segunda pregunta es de quién es la configuración.

`settings.json` y `.mcp.json` se commitean. Van a git, y todo el que clona el repo los hereda: mismos permisos, mismos hooks, mismos servidores MCP. Es la configuración del proyecto, no la tuya.

`settings.local.json` es tuyo y solo tuyo. Claude Code se encarga de que git lo ignore automáticamente, así que nunca acaba en un commit por accidente. Aquí va lo que no quieres imponerle al equipo: tu modelo preferido, una API key, permisos que solo tú necesitas. Tiene la precedencia más alta que puedes editar a mano, así que es también el sitio para pisar puntualmente un setting del proyecto sin tocar el archivo compartido.

Un nivel más arriba, `~/.claude/settings.json` son tus settings globales: se aplican en todos tus proyectos a la vez.

## La tabla, de un vistazo

| Archivo | Para qué | Cómo actúa | Compartido |
|---|---|---|---|
| `CLAUDE.md` | Instrucciones, contexto, convenciones | Se LEE (guía) | Equipo (git) |
| `settings.json` | Permisos, hooks, modelo, env vars | Se APLICA (obligatorio) | Equipo (git) |
| `settings.local.json` | Tus overrides personales | Se APLICA (obligatorio) | Solo tú (gitignored) |
| `.mcp.json` | Servidores MCP del proyecto | Conecta herramientas | Equipo (git) |

Un detalle que despista a todos: `.mcp.json` va en la **raíz del proyecto**, no dentro de `.claude/`. Es el único de la lista que vive fuera de esa carpeta.

## Dos preguntas que NO responde este tip

**"¿Y si defino lo mismo en dos archivos?"** Eso ya no es *dónde poner* algo nuevo, es *quién gana* cuando dos definiciones chocan. Es un problema distinto, con reglas que no siempre apuntan donde crees, y tiene [su propio tip](/es/tips/claude-code-precedencia-config-quien-gana).

**"Vale, va en CLAUDE.md, ¿pero qué escribo?"** La mayoría de CLAUDE.md están llenos de cosas que Claude ya puede inferir solo. Qué meter y qué borrar está en [tu CLAUDE.md está lleno de basura](/es/tips/claude-code-claudemd-configurar-proyecto).

## Y dos archivos más, para casos concretos

- `.claude/rules/*.md`: trozos de CLAUDE.md modulares. Útiles cuando tu CLAUDE.md se acerca a las 200 líneas, porque puedes activar cada regla solo para las rutas que le indiques.
- `.worktreeinclude`: lista archivos gitignored (tu `.env`, por ejemplo) que quieres copiar automáticamente a cada worktree nuevo.

Y un aviso sobre MCP para cerrar el círculo: `.mcp.json` es el MCP del proyecto, para el equipo. Tu MCP personal no va en un `.mcp.json` tuyo, vive en `~/.claude.json` (lo añade `claude mcp add --scope user`). Son archivos distintos.

> Documentación oficial: [The .claude directory](https://code.claude.com/docs/en/claude-directory)
