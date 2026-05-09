---
date: 2026-05-08
type: tip
title_es: "/doctor en Claude Code: deja de buscar tu error en Reddit"
title_en: "/doctor in Claude Code: stop searching for your error on Reddit"
---

> **TL;DR** Ejecuta `/doctor` dentro de Claude Code. Audita en una sola pasada **instalación, settings, MCP servers y uso de contexto**. Cada check sale en verde, amarillo o rojo. Pulsa `f` y Claude arregla los issues reportados solo. Si Claude ni siquiera arranca: `claude doctor` desde tu shell.

Algo va raro en Claude Code: el search no encuentra archivos, un MCP no conecta, las respuestas se ralentizan, una skill que ayer iba bien hoy no aparece. La reacción típica: abrir Reddit, buscar el síntoma, perderse 40 minutos en threads. La reacción que casi nadie tiene: ejecutar `/doctor` y dejar que Claude se audite solo.

## Cómo funciona por dentro

`/doctor` corre una batería de checks en paralelo y devuelve un report con **status icons**:

- 🟢 verde — pasa
- 🟡 amarillo — warning (algo no es óptimo, pero funciona)
- 🔴 rojo — error (esto está roto)

Y la pieza que poca gente conoce: tras el report, **pulsa `f` y Claude arregla los issues reportados** sin que tengas que copiar-pegar el fix de ningún sitio.

Si Claude no arranca y no puedes ejecutar slash commands, hay versión shell: `claude doctor` desde el terminal te da el mismo report fuera del CLI.

## Resultado

```
> /doctor

Running diagnostics...

🟢 Installation       npm global · Claude Code v2.1.119
🟢 Settings           ~/.claude/settings.json valid
🟢 API connectivity   reachable, auth OK
🟡 Context usage      72% — consider /compact
🔴 MCP: github        connection refused (port 3000)
🟢 ripgrep            built-in OK
🟢 Skills             14 loaded

1 error · 1 warning · 5 OK

Press [f] to have Claude fix the reported issues, or [Enter] to dismiss.
```

Pulsas `f`. Claude detecta que el MCP de GitHub está apuntando a un puerto no expuesto, lee tu `~/.claude/mcp.json`, propone el fix, lo aplica, reintenta el connect. Verde.

## Cuándo ejecutarlo

### **1. Cuando algo va raro**

Antes de Reddit, antes de StackOverflow. Es el primer paso. Si algo sale rojo, ya sabes dónde mirar. Si todo sale verde, el problema no está en tu setup — es algo más arriba.

### **2. Tras un install o upgrade**

Acabas de instalar Claude Code o de hacer `claude update`. Lanza `/doctor` para verificar que todo quedó bien antes de empezar a trabajar y pillar un error 20 minutos después.

### **3. Tras cambiar de método de instalación**

Migraste de npm a installer nativo, o entre Pro y Bedrock. Quedan restos de la configuración anterior. `/doctor` los detecta.

### **4. Si Claude no arranca**

Cuando ni siquiera puedes meterte en una sesión, la versión shell:

```bash
claude doctor
```

Mismo report, fuera del CLI. Útil cuando el binario está roto o el `PATH` no lo encuentra.

## Lo que detecta

| Categoría | Qué chequea |
|---|---|
| **Instalación** | Tipo (npm global / native / local), versión, integridad del binario |
| **Settings** | `~/.claude/settings.json` válido, sin keys inválidas |
| **API connectivity** | Llega al endpoint, auth funciona, no hay 5xx |
| **MCP servers** | Cada servidor configurado responde |
| **Skills** | Las skills del directorio cargan sin errores |
| **Context usage** | % usado del context window — sugiere `/compact` si está alto |
| **ripgrep** | Funciona el bundled o necesitas instalar el del sistema |
| **PATH** | El binario `claude` está accesible |

## Referencia

| Aspecto | Detalle |
|---|---|
| Comando dentro del CLI | `/doctor` |
| Versión shell | `claude doctor` |
| Tecla de fix | `f` (después del report) |
| Status icons | 🟢 OK · 🟡 warning · 🔴 error |
| Cobertura | Install, settings, API, MCP, skills, context, ripgrep, PATH |
| Tiempo medio | ~30 segundos |

> Documentación oficial: [Troubleshooting — Claude Code Docs](https://code.claude.com/docs/en/troubleshooting)
