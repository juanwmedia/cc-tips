---
date: 2026-05-29
type: tip
title_es: "Ctrl+R en Claude Code: recupera cualquier prompt que ya hayas escrito"
title_en: "Ctrl+R in Claude Code: bring back any prompt you've already written"
---
> **TL;DR** Pulsa `Ctrl+R`, escribe dos palabras y Claude Code busca entre los prompts que ya enviaste. Lo que casi nadie sabe: por defecto rebusca en **todos tus proyectos**, así que ese prompt largo que clavaste la semana pasada en otro repo lo recuperas aquí. `Tab` para editarlo, `Enter` para lanzarlo.

¿Ese pantallazo con "Search prompts · everywhere" y una lista de prompts antiguos? Es la búsqueda inversa del historial. `Ctrl+R` es la misma tecla que ya conoces de bash, pero con un giro que bash no tiene: Claude Code guarda tu historial de prompts **por directorio y entre sesiones**, y la búsqueda arranca con el alcance en *todos los proyectos*. Por eso en la captura aparecen prompts de otros repos (SlopSimulator, "frontend de 2a"…): no los escribiste en esta sesión, los está rescatando de tu historial global.

Resultado:

```
Search prompts · everywhere          ← alcance actual (Ctrl+S lo cambia)
↑ 14h ago  Sigue con el SlopSimulator y los comandos   ┐
  13h ago  Commitea T2.5 y arranca Fase 2               │ prompts de
  13h ago  Sigue con el frontend de 2a                  ┘ OTROS proyectos
  ⌕ refactor▮                          ← escribes y filtra al vuelo
```

## Cómo funciona

`Ctrl+R` abre una búsqueda incremental sobre tu historial: escribes, y resalta las coincidencias entre tus prompts anteriores. No es el visor de transcripción (eso es `Ctrl+O`, otra cosa): aquí buscas y reutilizas lo que ya escribiste.

**1. Abre la búsqueda.** Pulsa `Ctrl+R` en el prompt vacío.

**2. Escribe para filtrar.** Teclea unas letras; el término se resalta en cada coincidencia.

**3. Recorre coincidencias.** Pulsa `Ctrl+R` de nuevo para saltar a coincidencias más antiguas.

**4. Cambia el alcance con `Ctrl+S`.** Arranca en *todos los proyectos* (el "everywhere" del pantallazo). `Ctrl+S` cicla el alcance: **esta sesión → este proyecto → todos los proyectos**. Úsalo para acotar cuando hay demasiado ruido.

**5. Acepta o cancela.**
- `Tab` o `Esc`: mete el prompt en el input para **editarlo** antes de enviar.
- `Enter`: lo **ejecuta** tal cual, al instante.
- `Ctrl+C`: cancela y te **devuelve** lo que tenías escrito.

## Referencia rápida

| Tecla | Qué hace |
|---|---|
| `Ctrl+R` | Abre la búsqueda inversa / salta a la siguiente coincidencia (más antigua) |
| escribir | Filtra el historial en vivo, resaltando el término |
| `Ctrl+S` | Cambia el alcance: esta sesión / este proyecto / todos los proyectos |
| `Tab` o `Esc` | Acepta y deja el prompt en el input para editarlo |
| `Enter` | Acepta y ejecuta el prompt de inmediato |
| `Ctrl+C` | Cancela y restaura tu texto original |

## Detalles que evitan sustos

- **Si la pantalla se "congela" al pulsar `Ctrl+S`**, tu terminal lo está interpretando como flow-control (XOFF): pulsa `Ctrl+Q` para descongelar, y desactívalo con `stty -ixon` si te molesta.
- **`Ctrl+R` ≠ `Ctrl+O`.** `Ctrl+O` abre el visor de transcripción; la búsqueda de prompts es `Ctrl+R`. En versiones recientes están bien separados; si `Ctrl+R` no busca, actualiza con `claude update`.
- Esto se lleva de maravilla con [el modo bash (`Ctrl+B`)](/es/tips/claude-code-bash-mode-ejecutar-comandos): recuperas un comando largo del historial y lo reejecutas sin reescribirlo.

> Docs oficiales: [Reverse search with Ctrl+R](https://code.claude.com/docs/en/interactive-mode#reverse-search-with-ctrl-r)
