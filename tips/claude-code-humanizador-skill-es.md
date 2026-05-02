---
date: 2026-04-30
type: tip
title_es: "El skill humanizador en Claude Code: para que tu texto deje de oler a IA"
title_en: "The humanizer skill in Claude Code: stop your text from smelling like AI"
---

Si tu texto asistido con IA siempre se siente "demasiado AI" (o detectores como GPTZero lo cazan), el problema no es el tema — son las huellas estadísticas que dejan los LLMs. Em-dashes usados para enfatizar. "Let's dive into". "No solo X, sino Y". Listas triádicas por todas partes. El [skill](/es/tips/claude-code-skills-comandos-personalizados) humanizador caza esos patrones y los reescribe.

## Cómo funciona internamente

El skill vive en `~/.claude/skills/humanizer/SKILL.md`. Cuando lo invocas (o Claude auto-rutea a él vía el campo `description`), pasa tu texto por una checklist de 29 patrones agrupados en 5 categorías. Reescribe los pasajes problemáticos y hace una segunda pasada para cazar lo que se haya colado.

Qué detecta:

| Categoría | Patrones de ejemplo |
|---|---|
| **Content issues** | Inflación de relevancia, name-dropping, atribuciones vagas, retos formulaicos |
| **Language markers** | Vocabulario AI (`testament`, `landscape`, `delve`), cópulas "serves as", listas triádicas, falsos rangos, voz pasiva |
| **Stylistic red flags** | Abuso de em-dashes, negritas excesivas, headers inline, pares de palabras con guión, signposting |
| **Communication artifacts** | "I hope this helps", disclaimers de cutoff, tono sycophant |
| **Filler & hedging** | "In order to", calificadores excesivos, conclusiones genéricas |

## Resultado preview

Antes:

```
Vale la pena destacar que Claude Code no es solo un asistente de código,
sino un completo entorno de desarrollo que sirve como testamento de cómo
la IA puede transformar el panorama del software moderno. Ya seas
principiante o desarrollador experimentado, esta poderosa herramienta
ofrece resultados rápidos, fiables e intuitivos.
```

Después:

```
Claude Code es un entorno de desarrollo construido alrededor de la
asistencia con IA. Tanto si empiezas como si ya envías código a
producción a diario, la herramienta no se interpone.
```

## Configuración

**1. Instala el skill**

```bash
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

Hecho. Claude Code auto-descubre los skills en `~/.claude/skills/` al inicio de cada sesión.

**2. Verifica**

```bash
claude
```

Dentro de la sesión:

```
> /humanizer pega aquí tu párrafo con olor a IA
```

O dispáralo implícitamente: pega un párrafo y di *"limpia esto, suena a IA"*. Claude rutea al skill vía su `description`.

**3. Calibra a tu voz (opcional)**

El skill soporta calibración de voz — puedes editar `SKILL.md` y añadir tus propias preferencias de tono (uso de contracciones, varianza de longitud de frase, set de modismos). Es el mismo mecanismo que usa cualquier [skill personalizado](/es/tips/claude-code-skills-comandos-personalizados).

## Cuándo funciona (y cuándo no)

- **Funciona bien**: copy de marketing, drafts de blog, posts de LinkedIn, prosa de documentación — todo donde los AI tells son patrones estadísticos.
- **No ayuda**: código (deja los bloques de código intactos), respuestas reactivas cortas (los patrones necesitan volumen para detectarse), texto que ya es escueto y humano.

Si el output todavía suena raro, pásalo dos veces — la segunda pasada del skill es buena pero no perfecta.

> Fuente: [blader/humanizer en GitHub](https://github.com/blader/humanizer)
> Construye tu propia variante: [Claude Code skills — comandos personalizados](/es/tips/claude-code-skills-comandos-personalizados)

