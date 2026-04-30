---
date: 2026-04-07
type: tip
title_es: "Cómo usar más de un perfil de Claude Code en la misma máquina"
title_en: "How to Use More Than One Claude Code Profile on the Same Machine"
---
# Quick Tip: Cómo usar más de un perfil de Claude Code en la misma máquina

> **TL;DR** Define `CLAUDE_CONFIG_DIR` apuntando a un directorio distinto y tienes un Claude Code completamente aislado: credenciales, settings, historial, plugins, agents, hooks. Crea un alias en tu shell y cambias entre perfiles con un comando.

Si usas Claude Code para trabajo y para proyectos personales, mezclar contextos es un problema real. Tu MEMORY.md de proyectos personales aparece en sesiones de trabajo. Los plugins de tu empresa contaminan tu setup personal. Y si usas dos cuentas distintas, hacer logout/login constantemente es ridículo.

La solución oficial: `CLAUDE_CONFIG_DIR`. Una variable de entorno que le dice a Claude Code dónde guardar TODA su configuración. Apunta a un directorio distinto y tienes una instalación paralela completamente aislada.

## Cómo se aísla cada perfil

Cada `CLAUDE_CONFIG_DIR` guarda independientemente:

- Credenciales de cuenta (claude.ai login)
- `settings.json` (modelo, permisos, hooks globales)
- `CLAUDE.md` global
- Historial de sesiones (`/resume`)
- Plugins instalados
- Skills personales (`~/.claude/skills/`)
- Subagents personales (`~/.claude/agents/`)
- Auto-memory (`projects/<repo>/memory/`)

Es una instalación de Claude Code completa por cada directorio. Nada se comparte.

## Configuración

### **1. Crear el segundo directorio**

```bash
mkdir -p ~/.claude-work
```

No necesitas copiar nada. La primera vez que arranques Claude Code apuntando a ese directorio, te pedirá login y empezará desde cero.

### **2. Crear aliases en tu shell**

Añade a `~/.zshrc` o `~/.bashrc`:

```bash
# Perfil personal (default)
alias claude-personal='CLAUDE_CONFIG_DIR=~/.claude claude'

# Perfil de trabajo
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

Recarga la shell:

```bash
source ~/.zshrc
```

### **3. Usar cada perfil**

```bash
# Arranca con tu cuenta personal
claude-personal

# Arranca con tu cuenta de trabajo (otra cuenta, otros plugins, otro historial)
claude-work
```

La primera vez que ejecutes `claude-work`, te pedirá hacer login. A partir de ahí, cada perfil mantiene su sesión.

### **4. Auto-cargar un perfil por proyecto (opcional)**

Si un proyecto siempre usa una cuenta concreta, añade un `.env` en su raíz:

```
CLAUDE_CONFIG_DIR=~/.claude-work
```

Y carga las variables al entrar al directorio (con [direnv](https://direnv.net/) o similar). Cualquier `claude` que ejecutes desde ese proyecto usará automáticamente el perfil correcto.

## Referencia

| Aspecto | Detalle |
|---|---|
| Variable | `CLAUDE_CONFIG_DIR` |
| Default | `~/.claude` |
| Qué aísla | Credenciales, settings, historial, plugins, skills, agents, auto-memory |
| Setup típico | Aliases en `.zshrc` / `.bashrc` |
| Por proyecto | `.env` con `direnv` u otra herramienta similar |
| Logout/login | Innecesario — cada perfil mantiene su sesión |

> Documentación oficial: [Environment variables — CLAUDE_CONFIG_DIR](https://code.claude.com/docs/en/env-vars)
