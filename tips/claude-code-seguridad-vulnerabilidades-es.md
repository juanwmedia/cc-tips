---
date: 2026-06-03
type: tip
title_es: "Seguridad en Claude Code: que cace sus propias vulnerabilidades antes de que lleguen a prod"
title_en: "Security in Claude Code: make it catch its own vulnerabilities before they hit prod"
---
> **TL;DR** Instala el plugin `security-guidance` (`/plugin install security-guidance@claude-plugins-official`) y Claude revisa su propio código en busca de vulnerabilidades *mientras lo escribe*, en tres capas: match de patrones por edición, review del diff al final de cada turno, y review más profunda en cada commit. Caza injection, authz bypass, deserialización insegura o cripto débil, y se los pasa a Claude para arreglarlos en la misma sesión, antes del PR. Corre solo y no bloquea: es una capa de defensa, no la única.

`security-guidance` no le pide a Claude que se autoevalúe. Lanza un review **independiente** (otra instancia, contexto fresco, prompt centrado en seguridad) sobre lo que Claude acaba de escribir. Es la capa más temprana de la cadena: pilla el fallo en el editor, antes de que llegue al PR, a la revisión y a CI. Si lo pillas aquí, no llega a prod.

## Las tres capas

| Cuándo | Qué hace | Coste |
|---|---|---|
| **En cada edición** | Match de patrones de riesgo: `eval(`, `pickle`, `dangerouslySetInnerHTML`, `.innerHTML =`, edits bajo `.github/workflows/` | 0, sin llamada al modelo |
| **Al final de cada turno** | Review en background del diff del turno: injection, authz bypass, IDOR, SSRF, cripto débil | Uso de modelo |
| **En cada commit/push de Claude** | Review agéntica que lee el código de alrededor (callers, sanitizers) para bajar falsos positivos | Uso de modelo |

Si encuentra algo, **re-promptea a Claude con el hallazgo** y lo arregla en la conversación. Ves el problema y el fix en tu sesión, no en un informe a posteriori.

## Cómo activarlo

```bash
# En una sesión de Claude Code:
/plugin install security-guidance@claude-plugins-official
/reload-plugins
```

Elige **user scope** para que cargue en cada sesión local. Para un repo compartido (o para [Claude Code en la web](/es/tips/claude-code-sesiones-en-la-nube), donde los plugins de usuario no entran), decláralo en `.claude/settings.json`:

```json
{ "enabledPlugins": { "security-guidance@claude-plugins-official": true } }
```

A partir de ahí corre solo. No hay comando que recordar.

## Afínalo a tu proyecto

- **Reglas en lenguaje natural** para los reviews de modelo, en `.claude/claude-security-guidance.md`. Tu threat model: *"toda ruta bajo /admin debe llamar a `require_role` antes de leer la BD"*.
- **Patrones deterministas** por edición, en `.claude/security-patterns.yaml`: regex o substrings propios, por ejemplo cazar un `sk_live_` hardcodeado.

## Dónde encaja (y qué NO es)

Es **una capa de defense-in-depth, no una solución completa**: el modelo revisor puede dejar pasar cosas, y ninguna capa bloquea el commit. La cadena entera:

1. `security-guidance`, **en sesión** (esto)
2. `/security-review`, **on-demand** cuando lo pides
3. [Code Review / `/ultrareview`](/es/tips/claude-code-ultrareview), **en el PR**
4. Tu **CI**: scanners estáticos, supply-chain

Cada etapa caza lo que la anterior dejó pasar. El valor de este plugin es reducir lo que llega a las siguientes, no sustituirlas.

## Cuidado con

- **No bloquea.** Los hallazgos llegan como instrucciones; Claude los arregla, pero la última palabra es tuya.
- **Necesita git** para los reviews de turno y commit. Sin repo, solo corre el match de patrones.
- **Cuesta tokens** en las capas de turno y commit (la de edición es gratis). Tope de 20 reviews de commit por hora.
- Requiere **Python 3.8+** en el `PATH`; en el primer arranque crea un venv en `~/.claude/security/`.
- Los reviews de modelo usan un modelo potente por defecto, configurable con `SECURITY_REVIEW_MODEL` y `SG_AGENTIC_MODEL`.

## Referencia

| Aspecto | Detalle |
|---|---|
| Instalar | `/plugin install security-guidance@claude-plugins-official` + `/reload-plugins` |
| Requisitos | CLI v2.1.144+, Python 3.8+, git (para turno/commit) |
| Capas | edición (patrones) · turno (diff) · commit (agéntica) |
| Reglas propias | `.claude/claude-security-guidance.md` · `.claude/security-patterns.yaml` |
| Desactivar capas | `ENABLE_PATTERN_RULES=0` · `ENABLE_STOP_REVIEW=0` · `ENABLE_COMMIT_REVIEW=0` · `SECURITY_GUIDANCE_DISABLE=1` |
| Construido sobre | hooks (`PostToolUse`, `Stop`…) |

> Documentación oficial: [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance)
