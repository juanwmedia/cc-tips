---
date: 2026-03-03
type: tip
title_es: "Tu CLAUDE.md está lleno de basura, así es como puedes arreglarlo"
title_en: "Your CLAUDE.md Is Full of Junk — Here's How to Fix It"
---
# Quick Tip: Tu CLAUDE.md está lleno de basura, así es como puedes arreglarlo

CLAUDE.md es el archivo que Claude Code lee al inicio de cada sesión para entender tu proyecto. Vive en la raíz del repositorio y se comparte con el equipo via git. El problema: la mayoría de CLAUDE.md están llenos de información que Claude puede inferir solo — dependencias del `package.json`, estructura de carpetas, convenciones estándar del lenguaje. Cada línea innecesaria consume contexto y diluye las instrucciones que realmente importan.

La regla: si Claude puede descubrirlo leyendo el código, no lo pongas en CLAUDE.md. Documenta el por qué, no el qué. Las decisiones de negocio, las dinámicas de equipo, los motivos detrás de una arquitectura — eso sí que no se infiere de un `composer.json`.

> **TL;DR** Ejecuta `/init` para generar un CLAUDE.md base, luego elimina todo lo que sea auto-inferible. Quédate solo con lo que Claude no puede descubrir por sí mismo: decisiones de equipo, convenciones no estándar y el por qué detrás de cada regla.

Resultado:

```markdown
# CLAUDE.md

## Business rules
- All prices must include tax for ES/EU customers — legal requirement since 2024
- Never delete user data; soft-delete only — compliance with our data retention policy

## Architecture decisions
- We chose SQLite over Postgres for the public site — single-server deployment, no need for connection pooling
- API responses are cached 5 min at CDN level — product decision to reduce costs, not a technical limitation

## Team conventions
- PRs require at least 1 review from @frontend-team before merging
- Feature branches use `feat/TICKET-description` format — matches Linear integration

## Non-obvious commands
- `npm run seed:staging` — resets staging DB with anonymized production data
- `./scripts/deploy-preview.sh` — deploys to Vercel preview, needs VERCEL_TOKEN in .env
```

## Configuración

### **1. Generar el archivo base**

```bash
claude
# Dentro de la sesión:
/init
```

Claude analiza el codebase — detecta build system, frameworks, tests — y genera un CLAUDE.md inicial. Si ya existe uno, sugiere mejoras en lugar de sobreescribirlo.

### **2. Limpiar lo que sobra**

Revisa el archivo generado y elimina:

- Dependencias que aparecen en `package.json`, `composer.json`, `Cargo.toml`
- Estructura de carpetas (Claude la ve directamente)
- Convenciones estándar del lenguaje ("usar camelCase en JavaScript")
- Explicaciones de APIs públicas (enlaza a la documentación en lugar de copiarla)

### **3. Añadir lo que Claude no puede inferir**

- Decisiones de negocio y sus razones
- Convenciones de equipo que difieren del estándar
- Scripts internos con contexto de uso
- Restricciones legales o de compliance
- Flujos de trabajo no documentados en código

### **4. Importar archivos externos (opcional)**

Usa `@ruta/archivo` para modularizar sin sobrecargar el archivo principal:

```markdown
# CLAUDE.md
@docs/architecture-decisions.md
@docs/team-conventions.md
```

Máximo 5 niveles de importación. Las rutas relativas se resuelven desde el archivo que contiene el import.

## Referencia

| Archivo | Alcance | Compartido | Cuándo usarlo |
|---|---|---|---|
| `./CLAUDE.md` | Proyecto | Equipo (via git) | Instrucciones compartidas |
| `./.claude/CLAUDE.md` | Proyecto | Equipo (via git) | Alternativa al anterior |
| `./CLAUDE.local.md` | Proyecto | Solo tú | Preferencias personales del proyecto |
| `~/.claude/CLAUDE.md` | Global | Solo tú | Preferencias en todos los proyectos |
| `.claude/rules/*.md` | Proyecto | Equipo (via git) | Reglas modulares por tema o ruta |

## Buenas prácticas

| Hacer | No hacer |
|---|---|
| Documentar el por qué detrás de cada regla | Listar dependencias del proyecto |
| Instrucciones concretas y verificables | "Escribir código limpio" |
| Mantener bajo 200 líneas | Copiar documentación de APIs |
| Revisar periódicamente | Dejar instrucciones obsoletas |
| Usar `@imports` para modularizar | Un solo archivo de 500 líneas |

> Documentación oficial: [Memory and CLAUDE.md](https://code.claude.com/docs/es/memory)
