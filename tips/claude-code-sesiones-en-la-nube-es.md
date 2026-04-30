---
date: 2026-04-05
type: tip
title_es: "Claude Code en la Nube: Sesiones Paralelas desde el Navegador"
title_en: "Claude Code on the Web: Parallel Cloud Sessions from Your Browser"
---
Renunciar a tu entorno local suena intimidante. Tu editor, tu terminal, tus dotfiles — hay cierta comodidad en tener todo a mano. Pero para tareas rutinarias — una review, un scan de seguridad, una exploración rápida — no necesitas todo eso. Claude Code on the web ejecuta esas tareas en infraestructura cloud gestionada por Anthropic, directamente desde [claude.ai/code](https://claude.ai/code). Cada sesión corre en una VM aislada con tu repositorio clonado, un entorno preconfigurado y acceso de red limitado por defecto. Tu terminal queda libre. Y puedes lanzar varias tareas en paralelo.

> **TL;DR** Visita [claude.ai/code](https://claude.ai/code), conecta GitHub, describe la tarea. Claude clona, ejecuta, testea y te prepara un PR. También desde la terminal con `claude --remote "tarea"`. Requiere Pro, Max, Team o Enterprise.

Resultado:

```bash
> claude --remote "Fix the flaky test in auth.spec.ts"
# Sesión creada en claude.ai/code

> claude --remote "Update the API documentation"
# Segunda sesión en paralelo

> claude --remote "Refactor the logger to use structured output"
# Tercera sesión en paralelo
```

## Cómo usarlo

### **1. Desde el navegador**

1. Ve a [claude.ai/code](https://claude.ai/code)
2. Conecta tu cuenta de GitHub e instala la Claude GitHub App
3. Selecciona un entorno (o usa el default)
4. Describe la tarea en lenguaje natural
5. Revisa los cambios en la vista diff, itera con comentarios y crea un PR

### **2. Desde la terminal**

```bash
# Configuración inicial (usa credenciales de gh CLI)
/web-setup

# Lanzar tarea en la nube
claude --remote "Add input validation to the signup form"

# Lanzar varias en paralelo
claude --remote "Fix auth bug"
claude --remote "Add pagination to /api/users"
```

Cada `--remote` crea su propia sesión cloud. Monitoriza todas con `/tasks`.

### **3. Traer una sesión a tu terminal (teleport)**

```bash
# Selector interactivo de sesiones web
claude --teleport

# Sesión específica
claude --teleport <session-id>

# Desde dentro de Claude Code
/teleport
```

Teleport verifica que estés en el repositorio correcto, descarga la rama y carga el historial completo de la conversación.

## Referencia

| Comando / Acción | Qué hace |
|---|---|
| `claude --remote "tarea"` | Lanza una sesión cloud desde la terminal |
| `/web-setup` | Conecta GitHub con credenciales de `gh` CLI |
| `claude --teleport` | Trae una sesión web a la terminal local |
| `/teleport` o `/tp` | Igual, desde dentro de Claude Code |
| `/tasks` | Lista sesiones en background |

| Detalle | Valor |
|---|---|
| VM | Aislada por sesión, gestionada por Anthropic |
| Imagen base | Ubuntu 24.04 con Node, Python, Go, Rust, Java, Ruby, PHP, PostgreSQL 16, Redis 7 |
| Red | Limitada por defecto (registros de paquetes + GitHub). Configurable. |
| Sesiones paralelas | Sin límite fijo; comparten rate limits de tu plan |
| Plataformas de código | Solo GitHub (GitHub Enterprise Server para Team/Enterprise) |
| Planes | Pro, Max, Team, Enterprise |

**Relacionado:** [Controla Claude Code desde tu Móvil](/es/tips/claude-code-control-remoto-desde-movil) · [Worktrees para tareas en paralelo](/es/tips/claude-code-worktrees-tareas-paralelas)

> Documentación oficial: [Claude Code en la web](https://code.claude.com/docs/en/claude-code-on-the-web)

## Requisitos

- Suscripción Pro, Max, Team o Enterprise (API keys no soportadas)
- Cuenta de GitHub conectada
- `gh` CLI instalado y autenticado (para setup desde terminal; opcional desde el navegador)
