---
date: 2026-06-26
type: tip
title_es: "Tus propias reglas de seguridad en Claude Code: caza secretos hardcodeados en cada edición, gratis"
title_en: "Your own security rules in Claude Code: catch hardcoded secrets on every edit, for free"
---

> **TL;DR** Crea `.claude/security-patterns.yaml` con tus reglas (substrings o regex) y el plugin `security-guidance` salta en cada edición de Claude si aparece uno de tus patrones: un `sk_live_` hardcodeado, una query multi-tenant sin filtrar. Es determinista, **cero llamadas al modelo** y cero coste. Lo pones una vez y vigila solo.

El plugin [`security-guidance`](/es/tips/claude-code-seguridad-vulnerabilidades) revisa el código de Claude en tres capas. Dos usan el modelo y gastan tokens; la tercera, la de **cada edición**, es un match de patrones determinista que no llama al modelo: coste cero. Esa capa trae patrones de fábrica (`eval(`, `pickle`, `dangerouslySetInnerHTML`…), pero lo que casi nadie configura es **añadir los tuyos**.

Para eso está `.claude/security-patterns.yaml`. Tú defines qué texto, en qué archivos, y con qué aviso. Cada vez que Claude escribe, si el patrón aparece, el aviso entra en su contexto para el siguiente paso.

Resultado:

```
⏺ Edit  src/config/stripe.ts
⚠ internal_api_key · Clave de API hardcodeada. Carga las credenciales del secret manager.
```

## Cómo se usa

### **1. Requisito: el plugin `security-guidance`**

La capa de patrones vive dentro del plugin. Si no lo tienes:

```bash
/plugin install security-guidance@claude-plugins-official
/reload-plugins
```

El [tip del plugin](/es/tips/claude-code-seguridad-vulnerabilidades) cubre las tres capas; aquí vamos a la gratis.

### **2. Crea `.claude/security-patterns.yaml`**

```yaml
patterns:
  - rule_name: internal_api_key
    substrings: ["sk_live_", "AKIA"]
    reminder: "Clave de API hardcodeada. Carga las credenciales del secret manager."
  - rule_name: tenant_unfiltered_query
    regex: "\\.objects\\.all\\(\\)"
    paths: ["**/src/tenants/**"]
    reminder: "El código multi-tenant debe filtrar por org_id."
```

Dos reglas: una caza el prefijo de un secreto en cualquier archivo; la otra, una query sin filtrar solo bajo `src/tenants/`.

### **3. Los campos**

| Campo | Qué es |
|---|---|
| `rule_name` | Identificador que sale en el aviso |
| `substrings` | Lista de textos literales (esto **o** `regex`) |
| `regex` | Regex de Python contra el contenido editado |
| `paths` | Globs: la regla solo aplica a esos archivos (prefija con `**/`) |
| `exclude_paths` | Globs a saltar |
| `reminder` | El aviso que se le mete a Claude (máx. 1 KB) |

### **4. Dónde lo busca**

Carga y concatena todas las que existan:

- Usuario: `~/.claude/security-patterns.yaml` (todos tus proyectos)
- Proyecto: `.claude/security-patterns.yaml` (versionado con el repo)
- Proyecto local: `.claude/security-patterns.local.yaml` (gitignored, tus overrides)

## Cuidado con

- **El `.yaml` necesita PyYAML importable.** Si no lo tienes, el archivo se ignora **en silencio**. Usa `.json` (mismo schema), que funciona en cualquier Python.
- **Tope de 50 reglas**, y descarta las regex con riesgo de backtracking catastrófico.
- **Es aditivo y no bloquea.** Suma patrones a los de fábrica (no los quita), y el aviso es una instrucción para Claude, no un muro. Para bloqueo duro, un hook que corte la edición o un check en CI.
- Cada aviso salta **una vez por patrón, archivo y sesión**: no te inunda.

## Dónde encaja

- Es la capa más barata del plugin [`security-guidance`](/es/tips/claude-code-seguridad-vulnerabilidades): las otras dos (turno y commit) usan el modelo; esta es gratis.
- Para reglas que necesitan criterio y no un patrón fijo, está el archivo en lenguaje natural `.claude/claude-security-guidance.md` (mismas ubicaciones), que sí pasa por el modelo.

> Documentación oficial: [Add custom per-edit patterns](https://code.claude.com/docs/en/security-guidance#add-custom-per-edit-patterns)

## Requisitos

- El plugin `security-guidance` instalado (CLI v2.1.144+).
- Python 3.8+ en el `PATH` (lo necesita el plugin).
- Para `.yaml`: PyYAML importable. Si no, usa `.json` (sin dependencias).
