---
date: 2026-02-21
type: tip
title_es: "¿Cómo saber qué #@$%! piensa Claude en tiempo real?"
title_en: "What the #@$%! Is Claude Thinking? Watch It Live"
---

# Quick Tip: ¿Cómo saber qué #@$%! piensa Claude en tiempo real?

> **TL;DR** Pulsa `Ctrl+O` para ver a Claude pensar. Detecta problemas pronto. Frena malas decisiones antes de que se conviertan en mal código.

`Ctrl+O` activa la salida verbose en Claude Code. Cuando está activa, ves todo lo que el modelo procesa antes y mientras responde: detalles de las tool calls, trazas de ejecución y — lo más importante — los bloques de extended thinking que revelan el razonamiento interno del modelo.

Este atajo pasa totalmente desapercibido, pero es de los más valiosos cuando trabajas con un modelo con thinking. Poder leer el razonamiento en tiempo real te convierte en un revisor en directo — puedes atrapar alucinaciones, suposiciones erróneas o lógica defectuosa antes de que se materialicen en cambios de código.

Esto importa sobre todo cuando Claude trabaja en algo complejo. La traza de pensamiento te muestra cómo el modelo aborda el problema. Si detectas una suposición incorrecta, una alucinación o un camino que no lleva a ningún sitio, puedes pulsar `Ctrl+C` de inmediato — antes de que Claude escriba archivos, ejecute comandos o queme tokens en un callejón sin salida.

Resultado:

```
> Ctrl+O

Verbose output ON

⏺ Thinking…
  Voy a analizar el flujo de autenticación. El usuario quiere
  añadir refresh tokens con JWT. Primero modifico el middleware,
  luego actualizo el servicio de tokens...

  [el razonamiento se muestra en tiempo real como texto gris en cursiva]
```

## Cómo usarlo

### **1. Activar la salida verbose**

Pulsa `Ctrl+O` en cualquier momento de la sesión. Aparece un mensaje de confirmación y todas las respuestas posteriores incluyen la traza de razonamiento.

### **2. Observar el razonamiento en tiempo real**

Mientras Claude genera su respuesta, verás los bloques de pensamiento renderizados en texto gris cursiva encima de la salida real. Esto es el razonamiento interno del modelo — no un resumen, la cadena de pensamiento real.

### **3. Interrumpir cuando sea necesario**

Si el razonamiento revela una dirección incorrecta, pulsa `Ctrl+C` para detener la generación de inmediato. Redirige con un prompt corregido.

### **4. Desactivar cuando termines**

Pulsa `Ctrl+O` de nuevo para volver a la salida limpia. El modo verbose persiste durante la sesión pero se reinicia al salir.

## Referencia

| Atajo | Acción |
|---|---|
| `Ctrl+O` | Activar/desactivar salida verbose |
| `Ctrl+C` | Detener generación a mitad de respuesta |
| `Alt+T` / `Option+T` | Activar/desactivar extended thinking |

## Cuándo es más útil el modo verbose

| Escenario | Por qué ayuda |
|---|---|
| Refactors complejos | Ver si Claude entiende la cadena de dependencias antes de empezar a editar |
| Sesiones de debugging | Detectar hipótesis erróneas antes de que Claude modifique código funcional |
| Decisiones de arquitectura | Verificar que el razonamiento del modelo coincide con tu modelo mental |
| Codebases desconocidos | Confirmar que Claude lee los archivos correctos y saca conclusiones válidas |

> Documentación oficial: [Interactive mode — Keyboard shortcuts](https://code.claude.com/docs/en/interactive-mode)
