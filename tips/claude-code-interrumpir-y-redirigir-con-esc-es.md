---
date: 2026-06-23
type: tip
title_es: "Cómo parar y reconducir a Claude Code mientras trabaja sin perder lo que ya hizo"
title_en: "How to stop or redirect Claude Code mid-task without losing its work"
---

> **TL;DR** Dos teclas, dos intenciones. `Esc` corta la herramienta en marcha y para en seco: conservas lo ya hecho y rediriges con un prompt nuevo, pero pierdes la acción en curso. Escribir una corrección y pulsar `Enter` no interrumpe nada: la herramienta actual termina y Claude lee tu nota en el siguiente paso. Pulsa `Esc` cuando va por mal camino; escribe y `Enter` cuando solo quieres ajustar el rumbo.

Claude Code trabaja en un bucle: reúne contexto, actúa con herramientas y verifica, encadenando decisiones hasta terminar. Tú formas parte de ese bucle y puedes intervenir sin reiniciar la sesión ni perder el contexto. Hay dos formas de hacerlo, y la diferencia entre ellas es una sola: qué pasa con la acción que está corriendo ahora mismo.

Resultado:

```
> Refactoriza el módulo de pagos          (Claude está editando archivos…)

⏺ Edit  src/payments/checkout.ts
  ↳ Ejecutando…            [pulsas Esc]

⎿  Interrumpido · Claude conserva lo hecho y espera tu instrucción
```

## El freno y el volante

### **1. `Esc` — el freno de emergencia**

Pulsa `Esc` una vez para cortar la respuesta o la herramienta en mitad del turno. Claude cancela la acción en curso, conserva todo lo que ya había hecho y espera tu siguiente instrucción. A partir de ahí rediriges con un prompt nuevo.

Úsalo cuando Claude va claramente por mal camino: edita el archivo equivocado, enfila una solución que no quieres, o se enrolla con una explicación que no necesitas. Cortas, mantienes el trabajo previo y reconduces.

### **2. Escribe y `Enter` — el volante**

Si en lugar de `Esc` escribes una corrección y pulsas `Enter`, no interrumpes nada. La herramienta en marcha termina su trabajo y tu mensaje entra en el siguiente punto de decisión: Claude lo lee y ajusta su próximo paso antes de seguir.

Úsalo cuando vas bien pero quieres matizar sobre la marcha — "usa zod en vez de yup", "no toques los tests todavía" — sin tirar a la basura la acción que ya está corriendo.

### **3. La decisión: ¿te sirve lo que está haciendo ahora?**

Esa es toda la regla:

- Si la acción en curso **no** te sirve (va a romper algo, va al sitio equivocado) → `Esc`. Para en seco y redirige.
- Si la acción en curso **sí** te sirve y solo quieres ajustar lo siguiente → escribe y `Enter`. Deja que termine y dale el nuevo rumbo.

## Dos avisos para no llevarte sorpresas

Escribir y `Enter` **encola**, no aborta. No esperes que tu mensaje detenga la herramienta actual: se aplica en el siguiente paso, no en este. Si necesitas un corte inmediato, es `Esc`.

`Esc` no siempre corta al instante. En mitad de una cadena larga de herramientas, o controlando a Claude por Remote Control, puede tardar o no responder al primer toque; insiste. Y ojo con la doble pulsación: si el prompt tiene texto, `Esc` `Esc` borra el borrador; con el prompt vacío, `Esc` `Esc` abre el menú de [rewind](/es/tips/deshaz-cambios-al-instante-con-checkpoints) para deshacer cambios, que es otra cosa.

¿Solo quieres preguntar algo sin tocar la tarea? Para eso está [`/btw`](/es/tips/claude-code-btw-pregunta-lateral): responde en un overlay y Claude sigue trabajando sin enterarse.

## Referencia

| Acción | Qué hace | Qué pasa con el trabajo | Cuándo |
|---|---|---|---|
| `Esc` | Corta la herramienta o respuesta en marcha | Conserva lo ya hecho; la acción en curso se cancela | Va por mal camino y quieres redirigir |
| Escribe + `Enter` | Envía una corrección sin interrumpir | La acción actual termina; tu nota entra en el siguiente paso | Vas bien y solo quieres matizar |
| `Esc` `Esc` (prompt vacío) | Abre el menú de rewind | Deshace ediciones a un checkpoint anterior | Quieres deshacer, no redirigir |
| `/btw <pregunta>` | Pregunta lateral en un overlay | No toca la tarea; Claude sigue | Solo quieres consultar algo |

> Documentación oficial: [How Claude Code works — Interrupt and steer](https://code.claude.com/docs/en/how-claude-code-works#interrupt-and-steer)
