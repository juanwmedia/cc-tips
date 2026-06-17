---
date: 2026-06-17
type: tip
title_es: "/code-review en local: revisa tu diff antes del PR (no es solo el bot de GitHub)"
title_en: "/code-review locally: review your diff before the PR (it's not just the GitHub bot)"
---

> **TL;DR** Ejecuta `/code-review` en cualquier sesión y Claude revisa el diff de tu rama (los commits por delante de tu upstream más lo que tengas sin commitear): bugs de correctness y, además, limpieza de reuse, simplificación y eficiencia. `--fix` aplica los arreglos a tu working tree; `--comment` los postea inline en el PR. Pásale un archivo, un número de PR o un rango `main...rama` para acotar. Cero GitHub App.

Busca "Claude Code code review" y todo apunta al mismo sitio: la GitHub App de Team/Enterprise que comenta tus PRs en la nube. Existe, pero no es lo único. Hay un `/code-review` que corre **en tu terminal, en cualquier sesión**, sin instalar nada, y te revisa el diff **antes** de abrir el PR. Es el shift-left que se pierde casi todo el que trabaja en solitario.

La doc lo dice directo: corre `/code-review` en cualquier sesión de Claude Code y revisa un diff sin instalar la GitHub App.

```
> /code-review

Reviewing: 3 commits ahead of origin/main + 2 uncommitted files
  src/auth/session.ts · src/api/rate-limit.ts

🔴 src/auth/session.ts:142   el refresh de token compite con el logout
🟡 src/api/rate-limit.ts:33  la ventana de rate-limit no se resetea al fallar
🟣 reuse  validateUser duplica la lógica de src/auth/guards.ts

Aplica con --fix · publícalos en el PR con --comment
```

## Cómo se usa

**1. Qué revisa y qué diff coge**

Por defecto revisa el diff de tu rama: los commits que llevas por delante de tu upstream, más lo que tengas sin commitear en el working tree. Busca **bugs de correctness** y, desde la v2.1.151, también **limpieza de reuse, simplificación y eficiencia**. No es un linter de estilo; es un revisor que entiende tu código.

**2. Acótalo con un target**

`/code-review` a secas usa el diff por defecto. Pásale algo para acotar el alcance:

```bash
/code-review src/auth/session.ts      # un archivo
/code-review 1234                      # un PR de GitHub
/code-review main...mi-feature         # el diff que ese PR contendría
```

**3. `--fix` y `--comment`**

- `--fix`: aplica los hallazgos a tu working tree después de revisar. Los repasas como cualquier otro cambio antes de commitear.
- `--comment`: postea los hallazgos como comentarios inline en el PR.

**4. Sube el listón con effort, o vete a la nube**

Un **effort** bajo da menos hallazgos pero más seguros; de `high` a `max`, más cobertura y algún hallazgo incierto. Sin argumento, usa el effort de tu sesión. Si quieres la revisión profunda con flota de agentes en la nube, `/code-review ultra` lanza el [ultrareview](/es/tips/claude-code-ultrareview) y, con `--fix`, aplica sus hallazgos cuando vuelven a tu sesión.

## Si vienes de `/simplify`

Era el nombre de este comando antes de la v2.1.147, cuando aplicaba los arreglos por defecto. Desde la v2.1.154, `/simplify` es otra cosa: una limpieza que aplica fixes **sin cazar bugs**. Si tenías `/simplify` scripteado para encontrar bugs, ahora es `/code-review --fix`.

## Referencia

| Invocación | Qué revisa |
|---|---|
| `/code-review` | Diff por defecto: rama vs upstream + sin commitear |
| `/code-review <archivo>` | Solo ese archivo |
| `/code-review <PR#>` | Un PR de GitHub |
| `/code-review main...rama` | El diff que ese PR contendría |
| `--fix` | Aplica los arreglos al working tree |
| `--comment` | Postea los hallazgos inline en el PR |
| `/code-review ultra` | Ultrareview en la nube (flota de agentes) |

## Dónde encaja

- No lo confundas con [Claude revisando PRs dentro de GitHub](/es/tips/claude-code-github-actions-revisar-prs): eso vive en la nube y se dispara en el PR; esto corre en tu terminal, antes.
- Para un cambio grande, la revisión profunda con verificación es [`/ultrareview` en la nube](/es/tips/claude-code-ultrareview).
- Y la capa más temprana, mientras Claude escribe, es [el plugin de seguridad](/es/tips/claude-code-seguridad-vulnerabilidades): encadena security en sesión → review en el PR → CI.

> Documentación oficial: [Review a diff locally](https://code.claude.com/docs/en/code-review)

## Requisitos

- La limpieza de reuse/simplificación/eficiencia llega en la v2.1.151; el cambio de `/simplify`, en la v2.1.154.
