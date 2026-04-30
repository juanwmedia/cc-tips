---
date: 2026-02-21
type: tip
title_es: "Bifurca tus Conversaciones con Fork Session"
title_en: "Branch Your Conversations with Fork Session"
---
> **TL;DR** `claude --continue --fork-session` crea una rama independiente de tu conversación actual. Mismo contexto, nuevo camino. Como `git branch`, pero para tus sesiones con Claude.

Probablemente ya sabes que con `claude --continue` puedes retomar tu última sesión. Eso es de dominio público. Lo que quizás no sabes es que puedes *bifurcarla*. Fork crea una sesión nueva con un ID propio, pero arranca con todo el historial de la sesión original intacto. La sesión original no se toca. Piénsalo como un `git checkout -b` para tu conversación con Claude.

¿Por qué es tan potente? Porque te permite explorar múltiples aproximaciones al mismo problema sin perder el trabajo previo. Estás depurando un bug, Claude sugiere una solución, quieres probar otra vía sin arriesgar lo que ya tienes — fork, prueba, y si no funciona, la sesión original sigue ahí, exactamente donde la dejaste.

Resultado:

```
> claude --continue --fork-session

Resuming session abc123 (forked → new session def456)

> [continúas desde donde lo dejaste, pero en una sesión
  independiente — la original no se modifica]
```

## Cómo usarlo

### **1. Retomar la última sesión (sin fork)**

```bash
claude --continue
```

Esto añade mensajes a la misma sesión. Útil cuando simplemente quieres seguir donde lo dejaste.

### **2. Elegir una sesión concreta**

```bash
claude --resume
```

Muestra una lista de sesiones recientes para elegir. Puedes buscar por nombre o fecha.

### **3. Bifurcar una sesión**

```bash
claude --continue --fork-session
```

Crea una sesión nueva con ID propio. El historial completo se copia, pero a partir de aquí son independientes.

### **4. Bifurcar una sesión específica**

```bash
claude --resume --fork-session
```

Selecciona primero la sesión y luego la bifurca.

## Referencia

| Comando | Qué hace |
|---|---|
| `claude --continue` | Retoma la última sesión (mismo ID) |
| `claude --resume` | Elige una sesión de la lista y la retoma |
| `--fork-session` | Combinar con `--continue` o `--resume` para bifurcar |
| `/resume` | Desde dentro de una sesión, cambia a otra |

| Concepto | Detalle |
|---|---|
| Resume | Mismo session ID, los mensajes se añaden al historial existente |
| Fork | Nuevo session ID, copia el historial hasta ese punto, independiente desde ahí |
| Permisos | Los permisos de sesión no se heredan — hay que re-aprobarlos |
| Múltiples terminales | Sin fork, los mensajes se entremezclan. Con fork, cada terminal tiene su sesión limpia |

> Documentación oficial: [Resume or fork sessions](https://code.claude.com/docs/en/how-claude-code-works#resume-or-fork-sessions)
