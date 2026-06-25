---
date: 2026-06-25
type: tip
title_es: "Deja de hacer de niñera de tus PRs: Claude Code arregla el CI en rojo por ti"
title_en: "Stop babysitting your PRs: let Claude Code fix the failing CI for you"
---

> **TL;DR** En la rama de tu PR, ejecuta `/autofix-pr`. Claude detecta el PR con `gh`, abre una sesión en la nube y se queda vigilándolo: cuando el CI falla o alguien deja un comentario de review, investiga y **empuja el arreglo si está claro**. Necesitas la Claude GitHub App instalada y Claude Code on the web (en research preview para Pro, Max, Team y Enterprise).

Subes el PR y te quedas refrescando GitHub a ver si pasa el CI. Cuando falla, lees el log, arreglas, vuelves a empujar, y otra vez a esperar. Ese bucle es trabajo muerto. `/autofix-pr` lo mueve a la nube y te lo quita de encima.

No lo confundas con la GitHub App de Actions (esa responde cuando mencionas `@claude` en un comentario). Aquí, desde la misma terminal donde ya trabajas, lanzas un **vigilante**: Claude se suscribe a los eventos del PR y reacciona solo, sin que toques nada.

Resultado:

```
> /autofix-pr

Detectando el PR de la rama actual con gh… PR #214
Abriendo sesión en la nube y activando auto-fix…

⏺ Vigilando PR #214 · CI + comentarios de review
⎿  CI en rojo (test:unit) → investigando → fix empujado ✓
```

## Cómo se usa

### **1. Instala la Claude GitHub App** (requisito)

Desde [github.com/apps/claude](https://github.com/apps/claude), o cuando el setup te lo pida. Sin ella, el auto-fix no funciona.

### **2. En la rama del PR, ejecuta `/autofix-pr`**

Claude detecta el PR abierto con `gh pr view`, abre una sesión web y activa el auto-fix de un tirón. No hace falta pegar la URL ni configurar nada: basta con estar en la rama correcta. Acepta un prompt opcional para acotarlo: `/autofix-pr arregla solo lint y errores de tipos`. Otras vías:

- **PR creado en Claude Code on the web:** abre la barra de estado de CI y pulsa **Auto-fix**.
- **Desde el móvil:** "vigila este PR y arregla los fallos de CI o los comentarios de review".
- **Cualquier PR existente:** pega la URL en una sesión y pídele que lo arregle.

### **3. Qué hace ante cada evento**

Con el auto-fix activo, Claude recibe los eventos del PR y decide:

- **Fix claro:** si está seguro y no choca con instrucciones previas, hace el cambio, lo empuja y lo explica en la sesión.
- **Ambiguo o arquitectónico:** si el comentario admite varias lecturas o toca algo importante, te pregunta antes de actuar.
- **Duplicado o sin acción:** lo anota y sigue.

### **4. Pararlo**

Es un toggle por PR. Abre la barra de estado de CI en la sesión web y quita **Auto-fix**, o dile a Claude que deje de vigilar el PR.

## Tres avisos para no llevarte sorpresas

- **Los conflictos de merge no los caza solo.** GitHub no emite webhook cuando la base avanza y crea un conflicto, así que el auto-fix no se entera. Abre la sesión y pídele un rebase.
- **Responde con tu cuenta.** Claude puede contestar a los hilos de review en GitHub; los mensajes salen bajo tu usuario (etiquetados como Claude Code, para que se sepa que los escribió el agente).
- **Aviso de seguridad.** Si tu repo tiene automatización disparada por comentarios (Atlantis, Terraform Cloud, Actions sobre `issue_comment`), las respuestas de Claude pueden activarla. Desactiva el auto-fix en repos donde un comentario en un PR pueda desplegar infraestructura.

## Referencia

| Vía | Cómo se activa |
|---|---|
| Terminal | `/autofix-pr` en la rama del PR |
| Claude Code on the web | Barra de estado de CI → **Auto-fix** |
| Móvil | "vigila este PR y arregla el CI / los comentarios" |
| PR existente | Pega la URL en una sesión y pídeselo |
| Parar | Quita el toggle **Auto-fix** o "deja de vigilar el PR" |

## Dónde encaja

- No es [Claude revisando PRs con GitHub Actions](/es/tips/claude-code-github-actions-revisar-prs): eso responde a `@claude` en un comentario vía workflow con tu API key; esto vigila el PR solo y empuja fixes desde una sesión en la nube.
- Para revisar tu diff en local **antes** de abrir el PR: [`/code-review`](/es/tips/claude-code-code-review-antes-del-pr).
- Vive sobre [Claude Code en la nube](/es/tips/claude-code-sesiones-en-la-nube), que es la infraestructura donde corre la sesión.

> Documentación oficial: [Auto-fix pull requests](https://code.claude.com/docs/en/claude-code-on-the-web#auto-fix-pull-requests)

## Requisitos

- La Claude GitHub App instalada en el repo.
- El `gh` CLI instalado y autenticado (lo usa para detectar el PR de la rama).
- Claude Code on the web (en research preview) en Pro, Max, Team o Enterprise (asientos premium o Chat + Claude Code).
