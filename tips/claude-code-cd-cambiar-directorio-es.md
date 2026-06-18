---
date: 2026-06-18
type: tip
title_es: "/cd en Claude Code: cámbiate de repo a mitad de sesión sin perder el contexto"
title_en: "/cd in Claude Code: jump to another repo mid-session without losing your context"
---

> **TL;DR** `/cd <ruta>` mueve tu sesión a otra carpeta sin reiniciar: la caché del prompt **se conserva** (el `CLAUDE.md` de la nueva carpeta se añade como mensaje, no reescribe el system prompt), y la sesión pasa al storage de la nueva carpeta, así que `--resume` y `--continue` la encuentran allí. Si solo quieres dar acceso a otra carpeta sin mover la sesión, usa `/add-dir`. Requiere v2.1.169+.

Cambiar de repo a mitad de sesión era un fastidio: salías, relanzabas `claude` en la otra carpeta y perdías toda la conversación. Y hacer `cd` en bash no vale, la sesión vuelve a su raíz: no coge el `CLAUDE.md` de la nueva carpeta ni actualiza las rutas de Glob, Grep y Bash. Desde la v2.1.169 hay un comando para esto: `/cd`.

Lo bueno no es solo que se mueva. Es que **se mueve sin reconstruir la caché del prompt**: en vez de reescribir el system prompt con el contexto de la nueva carpeta, añade su `CLAUDE.md` como un mensaje más. El siguiente turno no reprocesa toda la conversación a precio completo.

```
> /cd ../api-service

¿Confiar en ../api-service? (primera vez aquí)  [y/n] y
Sesión movida a ~/work/api-service
  · CLAUDE.md de api-service añadido al contexto
  · Glob, Grep y Bash trabajan ahora aquí
  · /resume y /continue la encuentran desde esta carpeta
```

## Qué hace, punto por punto

**1. Mueve la sesión y conserva la caché**

El `CLAUDE.md` de la carpeta destino se **añade como mensaje** en vez de reescribir el system prompt, que es justo lo que [rompería la caché del prompt](/es/tips/claude-code-prompt-caching-turno-lento-consumo). Por eso `/cd` no te penaliza el turno siguiente.

**2. La sesión se reubica en el storage de la nueva carpeta**

Pasa al project storage de la carpeta destino, así que `--resume` y `--continue` la encuentran **desde allí**, no desde donde arrancaste.

**3. Te pide confianza si la carpeta es nueva**

Si nunca has trabajado en esa carpeta, `/cd` te pide aprobarla antes de moverse. La misma puerta de confianza que el resto de Claude Code.

**4. `/cd` (mover) vs `/add-dir` (solo dar acceso)**

No son lo mismo. `/cd` **mueve** la sesión entera a la nueva carpeta. `/add-dir` solo **añade** una carpeta para acceso a archivos, sin mover la sesión ni cambiar de proyecto.

**5. Restringe a dónde puede saltar**

Con reglas de permiso `Cd` acotas o deshabilitas los destinos de `/cd`. Útil si no quieres que una sesión se pasee por todo el disco.

## Referencia

| Aspecto | Detalle |
|---|---|
| Invocación | `/cd <ruta>` (relativa o absoluta) |
| Caché del prompt | Se conserva (el `CLAUDE.md` nuevo entra como mensaje) |
| Storage de sesión | Pasa a la nueva carpeta; `--resume` / `--continue` la encuentran allí |
| Carpeta nueva | Pide confianza la primera vez |
| Solo dar acceso | `/add-dir` (no mueve la sesión) |
| Restringir destinos | Reglas de permiso `Cd` |
| Versión | v2.1.169+ (antes: `Unknown command: /cd`) |

## Dónde encaja

- El motivo de fondo por el que importa que no reescriba el system prompt: [prompt caching en Claude Code](/es/tips/claude-code-prompt-caching-turno-lento-consumo). Un cambio de carpeta a lo bruto te rompería el prefijo; `/cd` no.
- La carpeta destino aporta su propio `CLAUDE.md`: lo que de verdad debe ir ahí (y lo que sobra), en [tu CLAUDE.md está lleno de basura](/es/tips/claude-code-claudemd-configurar-proyecto).

> Documentación oficial: [Commands reference](https://code.claude.com/docs/en/commands)

## Requisitos

- Claude Code **v2.1.169** o superior. En versiones anteriores responde `Unknown command: /cd`.
