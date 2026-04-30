---
date: 2026-03-17
type: tip
title_es: "Controla Claude Code desde tu Móvil"
title_en: "Control Claude Code from Your Phone"
---
Remote Control conecta tu sesión local de Claude Code con [claude.ai/code](https://claude.ai/code) o la app de Claude para iOS y Android. Tu proceso sigue ejecutándose en la máquina — el móvil es solo una ventana a esa sesión. Empiezas una tarea en la terminal del portátil, sales de casa, y sigues dando instrucciones a Claude desde el teléfono en el bus. Así de directo.

> **TL;DR** `claude --rc` o `/rc` en sesión activa. Escanea el QR con el móvil. Sigue trabajando desde donde quieras. La terminal original debe quedarse abierta.

Resultado:

```
> claude --rc "Refactor API"
Remote Control session started

Session URL: https://claude.ai/code/session/abc123
Press spacebar to show QR code

╭──────────────────────────────────────╮
│ Remote Control: Refactor API         │
│ Status: Online                       │
│ Connected devices: 1                 │
╰──────────────────────────────────────╯
```

## Cómo usarlo

### **1. Sesión nueva con Remote Control**

```bash
# Sesión interactiva con acceso remoto
claude --rc

# Con nombre personalizado
claude --rc "Refactor API"
```

Abre una sesión normal en la terminal que también es accesible desde el móvil o cualquier navegador.

### **2. Activar en sesión existente**

Si ya estás trabajando con Claude:

```
/rc
```

Lleva toda la conversación actual. Muestra URL y QR para conectar.

### **3. Modo servidor**

```bash
# Sin interacción local, solo sirve conexiones remotas
claude remote-control --name "Backend" --spawn worktree
```

En modo servidor, cada conexión remota puede crear su propio worktree (requiere repositorio git). Acepta hasta 32 sesiones concurrentes.

### **4. Conectar desde otro dispositivo**

- **QR code**: en modo servidor, pulsa espacio para mostrar el QR. Con `/rc`, aparece automáticamente. Escanea con el móvil.
- **URL directa**: copia la URL de sesión en cualquier navegador.
- **Lista de sesiones**: busca por nombre en [claude.ai/code](https://claude.ai/code) o la app (icono de ordenador con punto verde = online).

### **5. Lo que debes saber**

La terminal original **debe quedarse abierta**. Si cierras la terminal o detienes el proceso, la sesión termina. Si el portátil se duerme, la sesión se reconecta automáticamente al despertar — pero si pierde conexión a red por más de ~10 minutos con el equipo encendido, la sesión hace timeout y el proceso se cierra. Tendrás que ejecutar el comando de nuevo.

## Referencia

| Comando | Qué hace |
|---|---|
| `claude --rc` | Sesión interactiva + Remote Control |
| `/rc` | Activa Remote Control en sesión existente |
| `claude remote-control` | Modo servidor (solo conexiones remotas) |
| `--name "Nombre"` | Nombre visible en la lista de sesiones (modo servidor) |
| `--spawn worktree` | Cada sesión remota en su propio worktree (modo servidor) |
| `--capacity <N>` | Máximo de sesiones concurrentes, default: 32 (modo servidor) |

| Detalle | Valor |
|---|---|
| Terminal original | Debe permanecer abierta |
| Laptop dormida | Reconexión automática al despertar |
| Timeout | ~10 min sin red (con equipo encendido). El proceso se cierra. |
| Seguridad | Solo HTTPS saliente, sin puertos abiertos |
| Sincronización | Bidireccional — terminal, navegador y móvil en paralelo |
| Planes | Todos los planes. Admins de Team/Enterprise deben habilitar Claude Code primero. |
| Versión mínima | v2.1.51+ |

> Documentación oficial: [Remote Control](https://code.claude.com/docs/es/remote-control)

## Requisitos

- Disponible en todos los planes (API keys no soportadas). Admins de Team y Enterprise deben habilitar Claude Code en [admin settings](https://claude.ai/admin-settings/claude-code).
- Claude Code v2.1.51 o superior
- App de Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) (opcional — también funciona desde el navegador)
