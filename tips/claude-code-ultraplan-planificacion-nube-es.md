---
date: 2026-04-05
type: tip
title_es: "Planifica en la Nube y Ejecuta Donde Quieras con Ultraplan"
title_en: "Plan in the Cloud and Execute Anywhere with Ultraplan"
---

Hay planes que no caben en una terminal. Migraciones de arquitectura, refactors profundos, decisiones que necesitas ver con calma antes de ejecutar. Ultraplan delega la planificación a una sesión de [Claude Code on the web](/es/tips/claude-code-sesiones-en-la-nube) corriendo en plan mode. Claude elabora el plan en la nube mientras tu terminal queda libre. Cuando está listo, lo revisas en el navegador con una interfaz rica — comentarios inline, reacciones, navegación por secciones — y decides dónde se ejecuta: en la web (directo a un PR) o de vuelta en tu terminal.

> **TL;DR** `/ultraplan migrate the auth service from sessions to JWTs` lanza una sesión de planificación en la nube. Revisa el plan en el navegador con comentarios inline. Ejecuta en la web o teletranspórtalo de vuelta a tu terminal.

Resultado:

```
> /ultraplan migrate the auth service from sessions to JWTs

Launching ultraplan session...

◇ ultraplan                      # Claude investiga el codebase
◇ ultraplan needs your input     # Claude tiene una pregunta — abre el enlace
◆ ultraplan ready                # Plan listo para revisar en el navegador
```

## Cómo usarlo

### **1. Lanzar ultraplan desde la CLI**

Tres formas de iniciar una sesión:

```bash
# Opción A: comando directo
/ultraplan migrate the auth service from sessions to JWTs

# Opción B: palabra clave en un prompt normal
Necesito un ultraplan para refactorizar el sistema de pagos

# Opción C: desde un plan local
# Cuando Claude termina un plan local y muestra el diálogo de aprobación,
# elige "No, refine with Ultraplan on Claude Code on the web"
```

Las opciones A y B muestran un diálogo de confirmación antes de lanzar. La opción C salta la confirmación porque la selección ya sirve como tal.

### **2. Monitorizar el progreso**

Tu terminal muestra un indicador de estado mientras la sesión remota trabaja. Ejecuta `/tasks` y selecciona la entrada de ultraplan para ver el enlace a la sesión, la actividad del agente y la opción **Stop ultraplan**.

### **3. Revisar y refinar en el navegador**

Cuando el estado cambia a `◆ ultraplan ready`, abre el enlace. La interfaz de revisión ofrece:

- **Comentarios inline**: selecciona cualquier pasaje y deja un comentario
- **Reacciones con emoji**: aprueba o marca preocupación sin escribir un comentario completo
- **Sidebar de outline**: navega entre secciones del plan

Itera tantas veces como necesites antes de decidir dónde ejecutar.

### **4. Elegir dónde ejecutar**

Desde el navegador tienes dos caminos:

```
Approve Claude's plan and start coding
  → Claude implementa en la misma sesión cloud → PR directo

Approve plan and teleport back to terminal
  → El plan vuelve a tu terminal con 3 opciones:
    • Implement here: inyecta el plan en tu conversación actual
    • Start new session: nueva sesión limpia con solo el plan como contexto
    • Cancel: guarda el plan en un archivo para volver a él después
```

## Referencia

| Estado | Significado |
|---|---|
| `◇ ultraplan` | Claude investiga el codebase y redacta el plan |
| `◇ ultraplan needs your input` | Claude tiene una pregunta; abre el enlace para responder |
| `◆ ultraplan ready` | El plan está listo para revisar en el navegador |

| Método de lanzamiento | Confirmación |
|---|---|
| `/ultraplan <prompt>` | Diálogo de confirmación |
| Palabra `ultraplan` en prompt | Diálogo de confirmación |
| Desde plan local aprobado | Sin confirmación (la selección ya confirma) |

| Opción de teleport | Qué hace |
|---|---|
| Implement here | Inyecta el plan en la conversación actual |
| Start new session | Limpia la conversación, arranca solo con el plan |
| Cancel | Guarda el plan en archivo, Claude imprime la ruta |

> Documentación oficial: [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)

## Requisitos

- Cuenta de [Claude Code on the web](/es/tips/claude-code-sesiones-en-la-nube) (Pro, Max, Team o Enterprise)
- Repositorio en GitHub
- Si Remote Control está activo, se desconecta al iniciar ultraplan (ambos usan la interfaz claude.ai/code)
