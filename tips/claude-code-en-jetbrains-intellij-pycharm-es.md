---
date: 2026-07-02
type: tip
title_es: "Claude Code en JetBrains: IntelliJ y PyCharm sin cambiarte a VS Code"
title_en: "Claude Code in JetBrains: IntelliJ and PyCharm without switching to VS Code"
---

> **TL;DR** Hay un plugin oficial de Anthropic en el Marketplace de JetBrains: **Claude Code [Beta]**. Instala dos piezas (el CLI `claude` por tu cuenta y el plugin) y ejecuta `claude` en la terminal integrada. Ganas diffs en el visor de JetBrains, tu selección compartida sola, `Cmd+Option+K` para referenciar `@archivo#L1-99` y los errores del IDE enviados a Claude. Y ojo: no es el "Claude Agent" del AI Assistant de JetBrains, son cosas distintas.

Si programas en IntelliJ o PyCharm, "usar Claude Code" suele reducirse a abrir la terminal integrada y escribir `claude`. Funciona, pero te pierdes la integración que casi todo el mundo asocia solo a VS Code. No hace falta cambiarse de editor: hay un plugin oficial que conecta tu IDE de JetBrains con el CLI.

## Cómo funciona (no es ACP ni un panel)

Aquí está el matiz que despista. El plugin **no** trae un panel gráfico como la extensión de VS Code, y **no** usa ACP. Lo que hace, según la doc, es lanzar `claude` en la terminal integrada del IDE y conectarse a él por un puente local. Es el mismo mecanismo que usa la extensión de VS Code (allí ese puente es un servidor MCP local llamado `ide`), no ACP. Tu interfaz sigue siendo la terminal; lo que cambia es que el IDE se "enciende" a su alrededor: diffs, selección y diagnósticos.

Detalle importante: **el plugin no incluye su propia copia del CLI**. Por eso instalas dos cosas (el CLI y el plugin), al revés que en VS Code, donde la extensión trae la suya.

## Lo que ves al usarlo

```
IntelliJ IDEA ── terminal integrada
> claude
  ⧉ Selected 12 lines from auth.kt        ← tu selección viaja sola
> arregla el token que expira

  ▸ diff  UserService.kt        +6 -2      ← se abre en el visor de JetBrains
  Cmd+Option+K → @auth.kt#L1-99            ← referencia exacta al vuelo
```

## Puesta en marcha

**1. Instala el CLI (el plugin no lo trae)**

Sigue el [quickstart](https://code.claude.com/docs/en/quickstart) para tener `claude` en tu PATH. Si falta, el plugin avisa con un "Cannot launch Claude Code".

**2. Instala el plugin y reinicia**

En el IDE: **Settings → Plugins → Marketplace**, busca "Claude Code" e instala **Claude Code [Beta]**. Reinicia el IDE por completo (a veces hace falta más de una vez).

**3. Ejecútalo**

Abre la terminal integrada y escribe `claude`: con eso los features del IDE ya están activos. Desde una terminal externa, conéctalo con `/ide`. Atajo rápido: `Cmd+Esc` (Mac) / `Ctrl+Esc` (Win/Linux) lanza Claude Code desde el editor.

**4. Diffs en el IDE**

En Claude Code, `/config` → pon el diff tool en `auto` para verlos en el visor de JetBrains, o `terminal` para dejarlos en texto.

## No lo confundas con el AI Assistant de JetBrains

Al buscar salen dos cosas con nombre parecido, y es la duda más repetida:

- **Claude Code [Beta]** → el plugin de **Anthropic**. Es tu CLI conectado al IDE, con tu suscripción de Claude.
- **"Claude Agent" / AI Assistant** → producto de **JetBrains** que usa Claude como uno de sus modelos. Otra empresa, otra suscripción, otra cosa.

Este tip va del primero.

## Referencia

| Feature | Cómo | Atajo |
|---|---|---|
| Lanzar Claude Code | desde el editor | `Cmd+Esc` / `Ctrl+Esc` |
| Diffs en el IDE | `/config` → diff tool `auto` | — |
| Selección compartida | automática (tab/selección actual) | — |
| Referencia a archivo | inserta `@src/auth.ts#L1-99` | `Cmd+Option+K` / `Alt+Ctrl+K` |
| Diagnósticos | lint y errores del IDE van a Claude | automático |

**Gotchas reales:**
- **El `ESC` no interrumpe** en la terminal de JetBrains: en **Settings → Tools → Terminal** desmarca "Move focus to the editor with Escape" (o borra ese atajo).
- **Remote Development**: instala el plugin en el **host remoto** (Settings → Plugin (Host)), no en tu máquina local.
- **En `acceptEdits`** Claude puede modificar archivos de config del IDE que este ejecuta solo. En repos que no controlas, revisa a mano en vez de auto-aceptar. Repasa [los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab).

Si trabajas en VS Code en vez de JetBrains, la historia es otra (ahí sí hay panel gráfico): [Claude Code en VS Code, el panel que casi nadie usa](/es/tips/claude-code-extension-vs-code-panel-nativo).

> Documentación oficial: [Claude Code en JetBrains IDEs](https://code.claude.com/docs/en/jetbrains)

**Relacionado:** [Claude Code en VS Code](/es/tips/claude-code-extension-vs-code-panel-nativo) · [Los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab)

## Requisitos

- El plugin **Claude Code [Beta]** del Marketplace + el CLI instalado aparte
- Funciona en IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, GoLand y Android Studio
- Suscripción de pago (Pro, Max, Team o Enterprise) o cuenta de Console; sin API key
