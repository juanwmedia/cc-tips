---
date: 2026-02-27
type: tip
title_es: "Cuándo se carga cada feature en el contexto (y lo que cuesta)"
title_en: "When Each Feature Loads Into Context (and What It Costs)"
---

# Quick Tip: Cuándo se carga cada feature en el contexto (y lo que cuesta)

> **TL;DR** CLAUDE.md y los MCP servers se cargan al inicio de cada sesión y consumen contexto en cada petición. Skills cargan solo su descripción al inicio (contenido completo al usarlas). Subagents trabajan en contexto aislado. Hooks se ejecutan externamente con coste cero. Saber esto te permite diseñar un setup que ahorre tokens desde el minuto cero.

El comando `/context` te muestra qué consume tu contexto en este momento. Pero hay un paso previo: entender *cuándo* se carga cada cosa. No todas las features pesan igual ni cargan al mismo tiempo. Unas ocupan contexto desde que arrancas la sesión, otras solo cuando las usas, y otras no tocan la ventana de contexto en absoluto. Esa distinción marca la diferencia entre un setup eficiente y uno que quema tokens antes de que escribas tu primer prompt.

Resultado:

```
  Al inicio              Al usar           Aislado
┌──────────────────────────────────┐
│       Ventana de contexto        │
│                                  │
│  CLAUDE.md            Skills     │   ┌──────────────┐
│  Contenido completo,  Contenido  │   │ Ctx separado │
│  cada petición        completo   │   │              │
│                       al usarlas │   │  Subagents   │
│  MCP servers                     │   │  Frescos,    │
│  Definiciones de                 │   │  aislados    │
│  herramientas,                   │   └──────────────┘
│  cada petición                   │
│                                  │   Hooks
│  Skills*                         │   Ejecución externa,
│  Solo descripciones              │   coste cero
│  (por defecto)                   │
└──────────────────────────────────┘

■ Siempre en contexto  ■ Se carga al usar  □ Fuera del contexto
```

*Skills con `disable-model-invocation: true` no cargan nada hasta que las invocas.

## Las 3 fases de carga

### 1. Al inicio de sesión (siempre en contexto)

Se cargan cuando arrancas Claude Code y permanecen en cada petición:

- **CLAUDE.md**: contenido completo de todos los niveles (managed, user, project). Los archivos desde tu directorio actual hacia arriba se cargan al inicio; los de subdirectorios se descubren conforme accedes a ellos.
- **MCP servers**: todas las definiciones de herramientas y schemas JSON. Con Tool Search activado (por defecto), se cargan hasta un 10% del contexto y el resto se difiere.
- **Skills**: solo nombres y descripciones (~100 tokens por skill). El contenido completo no se carga aún.

```bash
# Comprueba qué consume tu contexto ahora mismo
/context
```

### 2. Al usar (carga bajo demanda)

Las skills cargan su contenido completo cuando las invocas con `/<nombre>` o Claude decide que son relevantes. Hasta entonces, solo consumen los tokens de su descripción.

```bash
# Esto carga el contenido completo de la skill en el contexto
/deploy
```

Skills con `disable-model-invocation: true` no cargan absolutamente nada hasta que las invocas manualmente. Coste cero por defecto — ideal para skills con efectos secundarios o que solo activas tú.

### 3. Aislado (fuera del contexto principal)

Subagents trabajan en su propia ventana de contexto. No heredan tu historial ni las skills invocadas — solo CLAUDE.md, las skills que les asignes, y lo que el agente principal les pase. Hooks se ejecutan como scripts externos sin tocar el contexto en absoluto.

## Referencia

| Feature | Cuándo carga | Qué carga | Coste en contexto |
|---|---|---|---|
| CLAUDE.md | Inicio de sesión | Contenido completo | Cada petición |
| MCP servers | Inicio de sesión | Definiciones + schemas | Cada petición* |
| Skills | Inicio + al usar | Descripciones al inicio, contenido al usar | Bajo hasta invocar** |
| Subagents | Al lanzarlos | Contexto fresco + skills asignados | Aislado |
| Hooks | Al dispararse | Nada (ejecución externa) | Cero |

*Con Tool Search activado, las herramientas que excedan el 10% del contexto se difieren.
**Skills con `disable-model-invocation: true` tienen coste cero hasta invocarse.

**Relacionado:** [Monitoriza tu consumo con /context](/es/tips/claude-code-comando-context-uso-tokens) · [Las 6 formas de extender Claude Code](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa)

> Documentación oficial: [Extend Claude Code](https://code.claude.com/docs/en/features-overview#understand-how-features-load)
