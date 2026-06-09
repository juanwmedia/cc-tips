---
date: 2026-06-09
type: tip
title_es: "/sandbox en Claude Code: ejecuta comandos sin pedir permiso y sin poder salirse de tu proyecto"
title_en: "/sandbox in Claude Code: run commands without prompts, locked to your project"
---

> **TL;DR** Activa `/sandbox` en modo auto-allow y Claude ejecuta comandos sin pedirte permiso, pero el sistema operativo le impide escribir fuera de tu proyecto o llamar a dominios que no autorizaste. No es el clasificador de auto mode: aquí no hay un modelo decidiendo, hay una valla que pone el SO. Si vives en `--dangerously-skip-permissions`, esta es la red que te faltaba.

Por defecto, Claude te pide permiso antes de cada comando de Bash. Para evitarlo tienes [el modo auto o el modo YOLO](/es/tips/claude-code-auto-mode-alternativa-yolo). El sandbox ataca el problema por otro lado: en vez de decidir *si* un comando se ejecuta, define *qué puede tocar* una vez que corre, y lo impone el sistema operativo (Seatbelt en macOS, bubblewrap en Linux/WSL2) sobre cada comando y sus procesos hijos.

Esa es la diferencia que casi nadie ve. [Auto mode](/es/tips/claude-code-auto-mode-alternativa-yolo) pone un clasificador a juzgar cada acción antes de ejecutarla. El sandbox no juzga nada: levanta una valla física. No hay modelo en medio, es determinista, y funciona en cualquier plan o modelo, porque el límite lo pone el SO y no tu cuenta. Y se pueden combinar.

Resultado:

```
> /sandbox

Sandbox  Mode  Overrides  Config

Configure mode
  1. Sandbox BashTool, with auto-allow
  2. Sandbox BashTool, with regular permissions
  3. No Sandbox ✓

Auto-allow mode: Commands will try to run in the sandbox automatically,
and attempts to run outside of the sandbox fallback to regular permissions.
Explicit ask/deny rules are always respected.
```

## La caja por defecto

Antes de tocar nada, de fábrica el sandbox permite lo siguiente:

- **Escritura:** solo tu directorio de trabajo y sus subcarpetas. Nada de `~/.bashrc`, `/bin` ni rutas fuera del proyecto.
- **Lectura:** casi todo el disco. Ojo: por defecto eso incluye `~/.ssh` y `~/.aws/credentials`. Si te importa, bloquéalas con `denyRead`.
- **Red:** ningún dominio permitido. La primera vez que un comando necesita uno nuevo, te pregunta.

## **1. Enciéndelo en un proyecto**

Ejecuta `/sandbox` y elige la opción 1 (auto-allow). La elección se guarda en `.claude/settings.local.json`, así que aplica a ese proyecto y no se va a git.

## **2. Actívalo en todos tus proyectos**

Ponlo en tu `~/.claude/settings.json` y deja de tocarlo proyecto a proyecto:

```json
{
  "sandbox": { "enabled": true }
}
```

## **3. Los comandos que se escapan**

Algunos no funcionan dentro del sandbox. En vez de apagarlo, los sacas con `excludedCommands`:

```json
{
  "sandbox": {
    "enabled": true,
    "excludedCommands": ["docker *"]
  }
}
```

Los clásicos: `docker` es incompatible, `jest` se cuelga (usa `jest --no-watchman`), y las CLIs en Go (`gh`, `gcloud`, `terraform`) fallan la verificación TLS bajo Seatbelt en macOS.

## **4. Modo estricto (sin puerta de escape)**

Por defecto, un comando que falla dentro del sandbox puede reintentarse *fuera*, pidiéndote permiso. Para cerrar esa puerta y obligar a que todo corra contenido:

```json
{
  "sandbox": { "enabled": true, "allowUnsandboxedCommands": false }
}
```

## Referencia

| Modo del panel | Qué hace |
|---|---|
| Sandbox BashTool, auto-allow | Ejecuta dentro del sandbox sin preguntar; lo que no cabe cae a permisos normales |
| Sandbox BashTool, regular permissions | Ejecuta dentro del sandbox pero sigue pidiendo permiso (más control) |
| No Sandbox | Apagado (por defecto) |

| Ajuste en `settings.json` | Para qué |
|---|---|
| `sandbox.enabled` | Enciéndelo en todos tus proyectos |
| `sandbox.excludedCommands` | Comandos que corren fuera (`docker`, `gh`...) |
| `sandbox.filesystem.allowWrite` | Dar escritura a rutas externas (`~/.kube`, `/tmp/build`) |
| `sandbox.filesystem.denyRead` | Bloquear lecturas sensibles (`~/.ssh`, `~/.aws`) |
| `sandbox.allowedDomains` | Pre-permitir dominios de red |
| `sandbox.allowUnsandboxedCommands` | `false` = modo estricto, sin escape |

## No es una cárcel perfecta

El sandbox reduce el riesgo, no lo elimina. No inspecciona el tráfico TLS, así que permitir un dominio amplio como `github.com` puede convertirse en una vía de fuga de datos. Y recuerda: por defecto sigue pudiendo leer tus credenciales. Trátalo como una valla muy alta, no como una bóveda.

## Dónde encaja

- [Los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab) deciden *si* un comando se ejecuta.
- [Auto mode](/es/tips/claude-code-auto-mode-alternativa-yolo) pone un clasificador a vigilar esa decisión.
- El sandbox decide *qué puede tocar* lo que ya se está ejecutando, y lo impone el SO.

Son capas, no rivales. Lo potente es combinarlas: auto-allow del sandbox más auto mode te da el flujo sin prompts con doble red.

## Requisitos

macOS, Linux o WSL2 (Windows nativo no). En Linux y WSL2 necesitas `bubblewrap` y `socat` (`sudo apt-get install bubblewrap socat`). En macOS no instalas nada: usa el Seatbelt del sistema.

> Documentación oficial: [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
