---
date: 2026-02-21
type: tip
title_es: "Depura tu Frontend con Claude Code y Chrome"
title_en: "Debug Your Frontend with Claude Code and Chrome"
---
> **TL;DR** `claude --chrome` o `/chrome` conecta Claude Code con tu navegador. Desde ahí, Claude abre pestañas, navega, hace click, lee la consola y depura tu frontend — todo sin salir de la terminal.

Claude Code se integra con la extensión Claude in Chrome para darte automatización del navegador directamente desde la CLI. Lanzas tu app, le pides que la pruebe, y Claude abre Chrome, navega a tu localhost, interactúa con formularios, lee errores de consola y te dice qué está roto — con acceso al DOM real y al estado de login de tu navegador.

Es fascinante verlo trabajar: abre pestañas, hace scroll, lanza modales, escribe términos de búsqueda y compila el resultado. Todavía a veces es lento. Todavía a veces falla. Pero la palabra clave es *todavía*. Esto mejora con cada versión, y la dirección es clara.

Resultado:

```
> claude --chrome

Chrome integration enabled

> Abre localhost:3000, rellena el formulario de registro
  con datos inválidos y dime si los mensajes de error
  aparecen correctamente

⏺ Opening new tab → localhost:3000
  Clicking "Sign up"...
  Typing invalid email...
  Form submitted — 3 validation errors detected:
  - Email format invalid
  - Password too short
  - Terms not accepted
```

## Cómo configurarlo

### **1. Requisitos previos**

- Google Chrome o Microsoft Edge
- [Extensión Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+
- Claude Code v2.0.73+
- Plan directo de Anthropic (Pro, Max, Teams o Enterprise)

### **2. Lanzar con Chrome**

```bash
claude --chrome
```

O dentro de una sesión existente:

```bash
/chrome
```

### **3. Activar por defecto (opcional)**

Ejecuta `/chrome` y selecciona "Enabled by default" para no pasar `--chrome` en cada sesión. Ten en cuenta que esto aumenta el consumo de contexto al cargar siempre las herramientas del navegador.

## Referencia

| Capacidad | Qué hace |
|---|---|
| Live debugging | Lee errores de consola y estado del DOM, luego arregla el código |
| Design verification | Construye UI y la compara visualmente en el navegador |
| Web app testing | Prueba formularios, flujos de usuario y regresiones visuales |
| Authenticated apps | Interactúa con Google Docs, Gmail, Notion — usa tu sesión activa |
| Data extraction | Extrae datos estructurados de webs y los guarda localmente |
| Task automation | Automatiza entrada de datos, formularios y workflows multi-site |
| Session recording | Graba interacciones como GIF para documentar o compartir |

| Comando | Acción |
|---|---|
| `claude --chrome` | Lanza Claude Code con Chrome habilitado |
| `/chrome` | Activa/gestiona Chrome dentro de una sesión |

> Documentación oficial: [Use Claude Code with Chrome (beta)](https://code.claude.com/docs/en/chrome)
