---
date: 2026-05-30
type: tip
title_es: "/diff en Claude Code: mira qué tocó Claude en cada turno, sin salir del terminal"
title_en: "/diff in Claude Code: inspect what Claude touched on every turn, without leaving the terminal"
---
> **TL;DR** `/diff` abre un visor interactivo en el terminal. Con ←/→ saltas entre **Current** (`git diff HEAD`, todo lo no commiteado) y los **turnos** (T1, T2…): lo que Claude cambió en cada turno. Lo bueno: la vista por turno se reconstruye de la conversación, **no de git** — sobrevive a tus ediciones manuales y a `git add`. Con ↑/↓ navegas archivos, y ya se hace scroll del detalle con teclado.

Vengo de [lazygit](https://github.com/jesseduffield/lazygit) y acabo de empezar a usar `/diff`. Todavía lo noto un poco *clunky* — acaba de salir —, pero tener un visor de cambios **nativo** dentro de Claude Code, donde ves lo que tocó en *cada turno*, es una pasada. Y no es "una vista trapera más" sobre `git diff`: la pestaña por turno mira otra cosa.

## Cómo funciona

`/diff` tiene **dos fuentes**, y ahí está el truco:

- **Current** = `git diff HEAD`: todos los cambios sin commitear de tu working tree. Lo de siempre, pero sin abrir otra pestaña.
- **Por turno** (T1, T2, T3…) = lo que Claude editó en *ese* turno concreto. **No sale de git**: Claude lo reconstruye de los `FileEdit`/`FileWrite` de los registros de la conversación. Por eso sigue siendo exacto aunque hayas tocado archivos a mano o hecho `git add` entremedias, y cada turno lleva un trozo de tu prompt para que recuerdes de qué iba.

Resultado:

```
> /diff

 Current   T2   T1            ← ←/→ cambia de fuente · ↑/↓ navega archivos
 ─────────────────────────────
 src/auth/login.ts     +12 −3
 src/auth/session.ts    +4 −1

 ▸ Current  = git diff HEAD (todo lo no commiteado)
 ▸ T2       = "arregla el logout" → lo que Claude tocó en ESE turno
```

## Cómo usarlo

**1. Ábrelo.** Escribe `/diff` (sin argumentos). Se abre el visor al instante.

**2. Cambia de fuente con ←/→.** Salta entre `Current` (git) y cada turno de Claude (`T1`, `T2`…, los más recientes primero).

**3. Navega archivos con ↑/↓.** Recorre los archivos tocados en la fuente seleccionada.

**4. Haz scroll del detalle con teclado.** En la vista de detalle de un diff largo: flechas, `j`/`k`, `PgUp`/`PgDn`, `Space`, `Home`/`End`. (Esto es lo que se acaba de añadir.)

## Referencia rápida

| Tecla / fuente | Qué hace |
|---|---|
| `/diff` | Abre el visor interactivo de cambios |
| `Current` | `git diff HEAD`: todo lo no commiteado del working tree |
| `T1`, `T2`, … | Cambios que hizo Claude **en cada turno** (de la conversación, no de git) |
| `←` / `→` | Cambia entre `Current` y los turnos |
| `↑` / `↓` | Navega entre archivos |
| flechas · `j`/`k` · `PgUp`/`PgDn` · `Space` · `Home`/`End` | Scroll del detalle |

## Por qué te importa

- **"¿Qué turno me rompió esto?"** La vista por turno ata cada cambio a su prompt: encuentras el culpable sin bisecar a mano.
- **Sobrevive a git.** Como la vista por turno no depende del estado de git, sigues viendo lo que tocó Claude aunque ya hayas hecho `git add` o editado a mano.
- **Primero mira, luego audita.** `/diff` solo *enseña* (read-only). Cuando ya lo has ojeado y quieres que la IA cace bugs, pásalo por [`/code-review` o la revisión en la nube](/es/tips/claude-code-ultrareview). ¿Un turno entero que no te gusta? Eso es [rebobinar con checkpoints](/es/tips/deshaz-cambios-al-instante-con-checkpoints).

> Docs oficiales: [Commands — /diff](https://code.claude.com/docs/en/commands)
