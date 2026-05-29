---
date: 2026-05-29
type: tip
title_es: "Cuando CLAUDE.md, skills y MCP chocan en Claude Code: ¿cuál gana?"
title_en: "When CLAUDE.md, skills, and MCP collide in Claude Code: which one wins?"
---
> **TL;DR** Tienes una skill `/deploy` en `~/.claude/skills/` y otra con el mismo nombre en el `.claude/skills/` del proyecto. ¿Cuál se ejecuta? La tuya personal: en skills, el nivel de **usuario gana al de proyecto**. Pero crea un subagente o un servidor MCP con ese mismo nombre y es al revés: gana el **proyecto**. Cuatro tipos de extensión, tres reglas de conflicto distintas.

Cuando defines la misma feature en dos sitios —tu carpeta personal `~/.claude/`, el repo del proyecto, un plugin o una política de empresa— Claude Code tiene que decidir qué hacer con el choque. Lo intuitivo sería "siempre gana lo más específico", es decir, el proyecto. No es así. Cada tipo de extensión resuelve el conflicto a su manera, y para skills la dirección está **invertida** respecto a subagentes y MCP. Saberlo te ahorra el rato de "pero si yo configuré esto en el proyecto, ¿por qué no se aplica?".

Esto es el complemento de [cuándo se carga cada feature en el contexto](/es/tips/claude-code-cuando-se-cargan-features-contexto): aquello explica el *cuándo* y el coste; esto, el *quién gana* cuando dos definiciones colisionan.

Resultado:

```
Misma skill /deploy en dos niveles:

  ~/.claude/skills/deploy/      (usuario)   ─┐
  .claude/skills/deploy/        (proyecto)  ─┤  mismo nombre → colisión
                                             │
  Skill      → gana USUARIO  ───────────────┘   (managed > usuario > proyecto)
  Subagente  → gana PROYECTO                     (managed > --agents > proyecto > usuario)
  MCP        → gana PROYECTO                      (local > proyecto > usuario)
  CLAUDE.md  → se SUMAN las dos                   (additivo, sin ganador)
  Hooks      → se disparan TODOS                  (merge, sin ganador)
```

## Cómo lo resuelve Claude Code

No hay una regla única. Hay tres comportamientos:

**1. CLAUDE.md: se suman.** Todos los niveles (managed, usuario, proyecto, `CLAUDE.local.md`) se concatenan en el contexto, no se pisan. El orden va de la raíz del sistema de archivos hacia tu directorio de trabajo, así que la instrucción **más cercana a tu cwd se lee la última**. Si dos se contradicen, Claude reconcilia con criterio y tiende a priorizar la más específica. No hay "ganador" duro: todo entra.

**2. Skills: override por nombre, y gana el usuario.** Si la misma skill existe en varios niveles, una sustituye a las demás con esta prioridad: **managed > usuario > proyecto**. Aquí está la trampa: tu skill personal en `~/.claude/skills/` **tapa** la del proyecto con el mismo nombre. Las skills de plugin usan namespace (`plugin:skill`), así que nunca chocan con las tuyas.

**3. Subagentes: override por nombre, pero gana el proyecto.** Misma idea, dirección opuesta: **managed > flag `--agents` > proyecto > usuario > plugin**. Aquí el proyecto sí gana a tu definición personal.

**4. MCP: override por nombre, entrada entera.** Prioridad **local > proyecto > usuario > plugin > conectores de claude.ai**. Importante: no se fusionan campos. Si el mismo servidor existe en dos scopes, se usa la entrada **completa** del de mayor prioridad, no una mezcla de ambas.

**5. Hooks: se fusionan.** Todos los hooks registrados se disparan en su evento, da igual de dónde vengan. No hay sustitución.

## Referencia rápida

| Feature | Al colisionar | Mismo nombre → quién gana |
|---|---|---|
| **CLAUDE.md** | Se suman (aditivo) | Nadie; entran todas, la más cercana al cwd se lee al final |
| **Skills** | Override por nombre | managed > **usuario > proyecto** (plugin con namespace) |
| **Subagentes** | Override por nombre | managed > `--agents` > **proyecto > usuario** > plugin |
| **MCP** | Override por nombre (entrada entera) | **local > proyecto > usuario** > plugin > claude.ai |
| **Hooks** | Se fusionan | Todos se disparan, sin importar el origen |

## Por qué te importa

- **Una skill del proyecto no se dispara y no sabes por qué.** Busca una con el mismo nombre en `~/.claude/skills/`: la está tapando. Abre `/skills` para ver el origen de cada una.
- **Reglas que DEBEN cumplirse siempre** van en el nivel `managed` (gana a todo) y, si es una prohibición dura, como [un hook](/es/tips/claude-code-hooks-automatizar-flujo-trabajo) —porque CLAUDE.md es contexto, no garantía.
- **Plugins siempre al final** en skills, subagentes y MCP: la menor prioridad. Por eso las skills de plugin van con namespace y no compiten con las tuyas. Si dudas entre las features, mira [skills vs hooks vs MCP vs plugins](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa).

> Docs oficiales: [Extend Claude Code — Understand how features layer](https://code.claude.com/docs/en/features-overview#understand-how-features-layer)
