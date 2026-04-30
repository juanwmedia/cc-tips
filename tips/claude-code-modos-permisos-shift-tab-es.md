---
date: 2026-04-14
type: tip
title_es: "Controla cuánta autonomía le das a Claude Code con los 6 modos de permisos"
title_en: "Control How Much Autonomy Claude Code Gets with 6 Permission Modes"
---
> **TL;DR** Pulsa `Shift+Tab` para ciclar entre default, acceptEdits y plan. Activa auto o bypassPermissions (modo YOLO) con flags. Combina con `/permissions` para pre-aprobar herramientas específicas. La mayoría solo conoce dos de los seis modos — y confunde lo que acceptEdits realmente aprueba.

Esta es una de esas características esenciales que se pasan por alto porque parecen simples — un atajo de teclado que cicla modos. Pero la decisión de qué modo usar cuándo cambia fundamentalmente cómo trabajas con Claude Code. Y hay una confusión habitual: acceptEdits NO aprueba todo. Aprueba ediciones de archivos y comandos básicos del sistema de archivos. Todos los demás comandos Bash siguen pidiendo permiso.

Seis modos, del más restrictivo al más autónomo. Cada uno es un equilibrio diferente entre supervisión y fluidez.

Resultado:

```
> Shift+Tab

default  →  acceptEdits  →  plan  →  [auto]  →  [bypassPermissions]
                                        ↑              ↑
                                  auto-opts-in    --dangerously-skip
                                  (Max/Team+)    (solo contenedores)
```

## Los seis modos

### **1. default — Revisar todo**

```
default — pregunta antes de cada edición
```

Claude lee archivos libremente pero pide permiso antes de cada edición y cada comando. Úsalo cuando estés empezando, trabajando en código sensible, o no confíes en la dirección todavía.

### **2. acceptEdits — Confía en las ediciones, revisa los comandos**

```
acceptEdits — edita libremente, pregunta para comandos
```

Claude crea y edita archivos sin pedir permiso. También auto-aprueba comandos comunes del sistema de archivos: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`. Todos los demás comandos Bash siguen pidiendo permiso.

**La confusión**: mucha gente piensa que acceptEdits significa "aprobar todo." No es así. `npm test`, `git push`, `curl` — todos siguen preguntando. Si quieres saltarte esos prompts para comandos específicos sin activar el modo completo, puedes [configurar deny rules y wildcards para controlar exactamente qué puede tocar Claude](/es/tips/claude-code-permisos-3-conceptos-clave).

### **3. plan — Mirar pero no tocar**

```
plan — investiga y propone, nunca toca archivos
```

Claude explora el codebase y propone un plan. Sin ediciones de código fuente. Los permisos para comandos siguen aplicando igual que en default. Entra con `Shift+Tab` o añade `/plan` antes de un prompt individual.

Cuando el plan está listo, Claude pregunta cómo proceder: aprobar y cambiar a auto, aprobar y aceptar ediciones, aprobar y revisar manualmente, o seguir refinando.

### **4. auto — Claude decide qué es seguro**

```
auto — un clasificador revisa cada acción en segundo plano
```

Un clasificador separado (Sonnet 4.6) evalúa cada acción antes de ejecutarla. Las operaciones seguras se ejecutan en silencio. Las peligrosas (deploys, borrados masivos, force push, `curl | bash`) se bloquean.

**Requisitos**: plan Max, Team, Enterprise o API. Sonnet 4.6, Opus 4.6 u Opus 4.7 — en Max solo funciona Opus 4.7. Solo Anthropic API (no Bedrock, Vertex ni Foundry).

Cuando tu cuenta cumple los requisitos, Auto aparece automáticamente en el ciclo de `Shift+Tab`. La primera vez que cicles hasta él verás un opt-in único.

Para los detalles del clasificador, las barreras en conversación y el drop automático de allow rules, ver [Olvídate de los permisos en Claude Code sin caer en modo YOLO](/es/tips/claude-code-auto-mode-alternativa-yolo).

### **5. dontAsk — Solo herramientas pre-aprobadas**

```
dontAsk — todo denegado salvo lo explícitamente permitido
```

Solo las herramientas que coinciden con tus reglas `permissions.allow` se ejecutan. Todo lo demás se deniega sin preguntar. Diseñado para pipelines de CI y scripts bloqueados. Si estás creando skills que necesitan [pre-aprobar sus propias herramientas sin intervención del usuario](/es/tips/claude-code-allowed-tools-permisos-skills), `allowed-tools` en el frontmatter de la skill hace lo mismo por skill.

```bash
claude --permission-mode dontAsk
```

Nunca aparece en el ciclo de Shift+Tab — solo se configura al arrancar.

### **6. bypassPermissions — Modo YOLO**

```
bypassPermissions — todo se ejecuta, sin red de seguridad
```

Desactiva todos los prompts de permisos y las comprobaciones de seguridad. Solo las escrituras en rutas protegidas (`.git`, `.zshrc`, `.claude`) siguen pidiendo permiso.

```bash
claude --dangerously-skip-permissions
# o equivalentemente:
claude --permission-mode bypassPermissions
```

**Usar solo en contenedores, VMs o entornos aislados.** Sin protección contra prompt injection. Sin clasificador. Sin barreras. Si lo ejecutas en tu máquina, Claude puede hacer `rm -rf ~/` y se ejecutará.

Para añadir YOLO al ciclo de Shift+Tab sin activarlo inmediatamente:

```bash
claude --allow-dangerously-skip-permissions
```

El día que salió Auto cambié del modo YOLO a auto mode — casi toda la fluidez de YOLO con una red de seguridad real. Para el desglose completo, ver [Olvídate de los permisos en Claude Code sin caer en modo YOLO](/es/tips/claude-code-auto-mode-alternativa-yolo).

## Combinar modos con /permissions

Los modos establecen la línea base. `/permissions` te permite añadir excepciones específicas por encima — pre-aprobar herramientas que ejecutas constantemente para que nunca pidan permiso, independientemente del modo.

```bash
> /permissions
# Añade reglas como:
Bash(npm test)
Bash(git add *)
Bash(git commit *)
```

Así te mantienes en default para seguridad pero te saltas el prompt para tus comandos más habituales. Las reglas [se mantienen entre sesiones](/es/tips/claude-code-permisos-3-conceptos-clave) y aplican en todos los modos excepto bypassPermissions (que ignora la capa de permisos por completo).

## Referencia

| Modo | Shift+Tab | Auto-aprueba | Mejor para |
|---|---|---|---|
| `default` | Sí (defecto) | Solo lecturas | Trabajo sensible, empezar |
| `acceptEdits` | Sí | Lecturas + ediciones + comandos filesystem | Iteración de código |
| `plan` | Sí | Solo lecturas (sin ediciones) | Exploración, arquitectura |
| `auto` | Tras opt-in | Todo (con clasificador) | Tareas largas (Team+ solo) |
| `dontAsk` | Nunca | Solo herramientas pre-aprobadas | CI, scripts |
| `bypassPermissions` | Tras opt-in | Todo (sin clasificador) | Solo contenedores, VMs |

## Cómo entrar en cada modo

| Método | Ejemplo |
|---|---|
| Teclado | `Shift+Tab` para ciclar |
| Flag CLI | `claude --permission-mode plan` |
| Configuración por defecto | `"permissions": {"defaultMode": "acceptEdits"}` en settings.json |
| Prompt individual | `/plan describe el flujo de auth` |

> Documentación oficial: [Modos de permisos](https://code.claude.com/docs/en/permission-modes) | [Referencia de permisos](https://code.claude.com/docs/en/permissions)
