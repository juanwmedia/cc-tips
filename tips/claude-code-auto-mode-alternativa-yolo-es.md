---
date: 2026-04-25
type: tip
title_es: "Olvídate de los permisos en Claude Code sin caer en modo YOLO"
title_en: "Escape Claude Code's permission fatigue without going YOLO"
---

> **TL;DR** Auto mode pone un clasificador entre Claude y tu máquina: las acciones seguras se ejecutan sin preguntar, las arriesgadas se bloquean. Es lo que `--dangerously-skip-permissions` debería haber sido. Yo retiré mi alias YOLO el día que lo probé.

Auto mode salió como research preview hace unas semanas y la mayoría de la gente que vivía con `--dangerously-skip-permissions` (el famoso modo YOLO) sigue sin moverse. Es un error: hace casi todo lo que hace YOLO, pero con un modelo separado vigilando cada tool call antes de que se ejecute.

Imagínalo como un guardia de seguridad. YOLO no tiene guardia, todo entra. Auto mode tiene un clasificador (un Sonnet 4.6 corriendo aparte) que revisa cada acción y solo deja pasar las que considera seguras.

Resultado:

```
> Shift+Tab → modo: ⚡ auto

✓ Edit src/auth.ts
✓ Run npm test
✓ Run git commit -m "fix login"
✗ Run git push origin main         (bloqueado: push directo a main)
↪ Claude probará: git push origin feature/login
✓ Run git push origin feature/login
```

Cero "(y)es" pulsados durante toda la sesión, y aún así no se te va a colar un `rm -rf` ni un push a producción.

## **1. Activación**

Si tu cuenta cumple los requisitos, Auto aparece automáticamente en el ciclo de `Shift+Tab`. La primera vez que cicles hasta él te pide un opt-in:

```
default → acceptEdits → plan → auto

⚡ auto mode (research preview)
   [Yes, enable]  [No, don't ask again]
```

Sin flag `--enable-auto-mode` (ese flag ya no existe en versiones recientes). Cumples requisitos y aparece.

**Requisitos exactos:**

| Tipo | Qué necesitas |
|---|---|
| Versión | Claude Code 2.1.83 o superior |
| Plan | Max, Team, Enterprise o API. Pro queda fuera. |
| Modelo | Sonnet 4.6, Opus 4.6 u Opus 4.7. En Max **solo Opus 4.7** funciona. |
| Provider | Anthropic API. No funciona en Bedrock, Vertex ni Foundry. |
| Admin (Team/Enterprise) | El admin debe activarlo en el panel antes de que tú puedas. |

Si Auto te dice "no disponible" y crees cumplir todo, no es un fallo transitorio: es que falta uno de los requisitos.

## **2. Lo que el clasificador deja pasar y lo que bloquea**

**Pasa sin preguntar:**
- Edits y reads dentro de tu working directory
- Instalar dependencias declaradas en lockfiles o manifests
- Leer `.env` y mandar credenciales a su API correspondiente
- HTTP read-only
- Push a la rama en la que empezaste o una que Claude creó

**Bloquea por defecto:**
- `curl | bash` y patrones download-and-execute
- Mandar datos sensibles a endpoints externos
- Deploys y migraciones de producción
- Borrado masivo en cloud storage
- Conceder permisos IAM o de repo
- Force push o push directo a `main`
- Borrar archivos que existían antes de la sesión

Para ver las reglas completas: `claude auto-mode defaults`.

## **3. La feature oculta: barreras en conversación**

Esto no aparece en el release note y es lo más útil de Auto mode después del clasificador.

Si en cualquier momento dices "no hagas push" o "espera a que revise antes de deployar", el clasificador trata esa frase como una **deny rule** durante el resto de la sesión. Re-lee el transcript en cada check.

```
Tú: estamos a viernes, no me toques producción esta tarde
Claude: entendido.

[horas después, Claude propone un deploy]
✗ Run aws ecs update-service ... (bloqueado: usuario pidió no tocar prod)
```

**Cuidado con el context compaction**: las barreras viven en el transcript. Si compactas y se pierde el mensaje, la barrera desaparece. Para una garantía dura, escribe un `deny rule` en `.claude/settings.json`.

## **4. La feature oculta 2: drop automático de allow rules amplias**

Si tienes en tu `settings.json` reglas tipo `Bash(*)` o `Bash(python*)` —el atajo perezoso clásico— al entrar en Auto mode Claude **las descarta automáticamente**. Las restaura cuando sales.

```
allow:
  Bash(*)              # ⚠️ se descarta al entrar en Auto
  Bash(npm test)       # ✓ esta sí se mantiene (es específica)
  Agent(my-agent)      # ⚠️ también se descarta
```

Lo hace porque una regla `Bash(*)` deshabilitaría al clasificador de facto. Las reglas estrechas (`Bash(npm test)`, `Bash(git commit *)`) sí se mantienen — esas son intencionales.

## **5. Cuándo Auto se rinde**

Si el clasificador bloquea **3 acciones seguidas o 20 totales**, Auto pausa y vuelves al flujo manual. No es configurable. Si te pasa con frecuencia, suele ser señal de que tu admin necesita declarar tu infra como confiable en `autoMode.environment`.

## **6. Cuándo aún tiene sentido YOLO**

`--dangerously-skip-permissions` sigue teniendo un nicho:
- Containers efímeros sin internet
- VMs aisladas / sandboxes
- CI con scope acotado donde quieres velocidad pura

En tu máquina principal, no hay razón para seguir en YOLO si tienes acceso a Auto. Auto te da el 95% del flow sin el riesgo.

## Auto vs YOLO

| | `auto` | `bypassPermissions` (YOLO) |
|---|---|---|
| Prompts | No | No |
| Clasificador antes de cada acción | ✓ | ✗ |
| Bloquea force push, mass delete, prod deploys | ✓ | ✗ |
| Honra "no hagas push" en chat | ✓ | ✗ |
| Drop de allow rules amplias | ✓ | ✗ |
| Coste por sesión | Ligeramente más alto | Igual al normal |
| Recomendado en máquina host | ✓ | ✗ (solo containers) |

Yo usaba YOLO con un alias `claude-yolo` desde hace meses. Cuando salió Auto lo probé pensando que el clasificador me iba a cortar el ritmo. Apenas se nota: en tareas largas se mete una vez cada veinte acciones, y cuando lo hace casi siempre tiene razón. El alias sigue ahí. Ya no lo uso.

> **Para el desglose completo de los 6 modos**, ver [Controla cuánta autonomía le das a Claude Code con los 6 modos de permisos](/es/tips/claude-code-modos-permisos-shift-tab). Para entender cómo se combinan modos con `/permissions`, ver [3 cosas que debes saber sobre /permissions en Claude Code](/es/tips/claude-code-permisos-3-conceptos-clave).

> Docs oficiales: [Permission modes](https://code.claude.com/docs/en/permission-modes) | [Auto mode engineering blog (Anthropic)](https://www.anthropic.com/engineering/claude-code-auto-mode)
