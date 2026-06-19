---
date: 2026-06-19
type: tip
title_es: "Artifacts en Claude Code: tu sesión deja de estar atrapada en el terminal"
title_en: "Artifacts in Claude Code: your session stops being trapped in the terminal"
---

> **TL;DR** Pídele a Claude Code *"haz un artifact de…"* y publica una **página HTML autocontenida** en una URL privada de claude.ai que tu equipo abre en el navegador y ve actualizarse en vivo. Requisitos: beta, plan **Team o Enterprise**, login en claude.ai y **solo Anthropic API** (nada de Bedrock/Vertex). Es estático por diseño: sin backend, una CSP que bloquea `fetch` y recursos externos, todo va *baked in*. ¿No tienes acceso? La técnica de fondo (pedir HTML en vez de Markdown y abrirlo en local) funciona en cualquier plan.

Hay una verdad incómoda que Anthropic puso por escrito en [un artículo sobre la eficacia del HTML](https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html): un Markdown de más de 100 líneas no se lee, se ojea en diagonal. Y el output de un agente vivía atrapado en tu terminal, visible solo para ti. La comunidad ya lo intentaba a mano (en Reddit alguien montó un "HTML Drive" casero para guardar y compartir estas páginas). Artifacts es esa idea, oficial.

## Cómo funciona

Un artifact es una **página web viva** que Claude Code publica desde tu sesión a una URL privada en claude.ai. La abres en el navegador y se actualiza en su sitio según avanza la sesión. Claude escribe un fichero HTML (o Markdown) en tu proyecto y lo publica; te pide permiso la primera vez.

```
> Haz un artifact que recorra este PR con el diff anotado al margen.

⠋ Escribiendo pr-walkthrough.html...
Claude wants to publish "PR walkthrough" (pr-walkthrough.html)
  to a private page on claude.ai  [y/n] y

✓ https://claude.ai/code/artifact/5fbea6f3-...
  (tu navegador se abre solo · Ctrl+] para reabrir el último)
```

Cada publicación es una **versión**. Compartes desde la cabecera de la página: a personas concretas o a toda tu organización (nunca fuera de ella). Para actualizarlo desde otra sesión, le pasas la URL.

## Qué puedes construir

Una sola página HTML, así que cabe todo lo que expreses con HTML, CSS y JS inline:

- **Recorrer un cambio**: el diff de un PR con anotaciones al margen y findings por color de severidad.
- **Comparar alternativas**: cuatro layouts del mismo panel, en rejilla, con su trade-off debajo.
- **Controles interactivos**: sliders para una curva de easing y ver la animación en vivo.
- **Devolver el resultado a la sesión**: un board de triaje con un botón *"Copy as prompt"* que te da el orden final para pegarlo de vuelta.
- **Seguir trabajo en curso**: un checklist que se va marcando solo mientras una tarea larga corre.

## Estático por diseño (y por qué importa)

Aquí está la limitación que más confunde, y es **a propósito, por seguridad**. Claude envuelve tu fichero en una CSP estricta:

| Restricción | Qué implica |
|---|---|
| Sin peticiones externas | La CSP bloquea `fetch`, XHR, WebSocket y cualquier script, fuente o imagen de otro host. Claude mete el CSS/JS inline y las imágenes como data URI |
| Sin backend | No guarda lo que metes en un formulario, no autentica ni llama a una API al verse |
| Una sola página | Los enlaces relativos no resuelven; usa anclas dentro de la página |
| Tipos de fichero | `.html`, `.htm` o `.md` · Tamaño renderizado ≤ 16 MiB |

Por eso un esquema de "JSON para el estado" no funciona: no hay servidor que lo sirva. Si quieres estado real, despliegas en tu infra. Un artifact es **una foto del trabajo, no una app**.

## El coste en tokens vale la pena (con design system)

Una página con estilo gasta más tokens que el mismo texto en el terminal: el CSS/JS inline y las imágenes en data URI son lo caro. Pero la ganancia visual es de calle. Para no pagarlo dos veces: prefiere SVG o HTML+CSS antes que imágenes raster, y deja registrado tu design system donde Claude lo lea (en tu `CLAUDE.md` o un theme), porque reutilizar colores, espacios y tipografías es lo que abarata y unifica. Claude carga un skill integrado, `artifact-design`, al construirlo:

```
Skill(artifact-design)
  └ Successfully loaded skill
```

Tu prompt y tu design system mandan sobre él. Para que tus UIs dejen de parecer hechas por IA en general, el [frontend-design skill](/es/tips/claude-code-skill-frontend-design) empuja en la misma dirección. Y si los tokens te preocupan, mira [cómo funcionan tus límites de uso](/es/tips/claude-code-limites-de-uso-5-horas-semanal).

## ¿No estás en Team/Enterprise? La técnica funciona igual

El botón de publicar es solo para Team/Enterprise, pero lo de fondo lo puedes hacer hoy en cualquier plan: pídele a Claude Code una **página HTML autocontenida** y ábrela en local con `open informe.html`. Pierdes el compartir y el live-update, pero ganas lo importante: dejar de leer Markdown en diagonal.

## Requisitos

- **Beta**, plan **Team o Enterprise** (en Team va por defecto; en Enterprise lo activa un admin).
- Login en claude.ai con `/login`. Con API key, gateway o credencial de cloud **no** publica.
- **Solo Anthropic API**: no en Amazon Bedrock, Google Vertex AI ni Microsoft Foundry.
- CLI de Claude Code, o app de escritorio v1.13576.0+. Desactívalo con `"disableArtifact": true`.

> Documentación oficial: [Share session output as artifacts](https://code.claude.com/docs/en/artifacts) · [Artifacts in Claude Code (blog)](https://claude.com/blog/artifacts-in-claude-code)
