---
date: 2026-03-02
type: tip
title_es: "Cómo elegir el modelo adecuado en Claude Code"
title_en: "How to Choose the Right Model in Claude Code"
---
# Quick Tip: Cómo elegir el modelo adecuado en Claude Code

No todas las tareas necesitan el modelo frontera. Un modelo frontera es el más avanzado y potente disponible en cada momento — ahora mismo, Opus 4.6. Es tentador usarlo para todo: si tienes acceso al mejor, ¿por qué conformarte con menos? Pero hacerlo desperdicia tokens, tiempo de espera y recursos. La mayoría de tareas de desarrollo diario no requieren razonamiento profundo.

Claude Code ya aplica esta lógica internamente. Su agente Explore funciona con Haiku para búsquedas rápidas en el codebase. El alias `opusplan` automatiza la estrategia completa: Opus razona durante la planificación, Sonnet ejecuta la implementación.

> **TL;DR** Usa `opusplan` para planificar con Opus y ejecutar con Sonnet. Cambia a Haiku para exploración rápida. No uses el modelo frontera para todo — asigna potencia donde realmente importa.

Resultado:

```
> /model

    default
  ● opusplan   ← Plan: Opus 4.6 · Ejecución: Sonnet 4.6
    opus
    sonnet
    haiku
```

## La estrategia: planificar, ejecutar, explorar

**1. Planificar con el modelo frontera**

El razonamiento profundo solo se justifica cuando diseñas arquitectura, evalúas trade-offs o tomas decisiones que afectan al proyecto entero. Aquí es donde Opus marca la diferencia.

```bash
claude --model opus
# O cambiar durante la sesión:
/model opus
```

**2. Ejecutar con Sonnet**

Escribir funciones, tests, refactorizar — no necesita el mismo nivel de razonamiento. Sonnet 4.6 ofrece inteligencia comparable a menor coste y mayor velocidad.

```bash
/model sonnet
```

**3. Explorar con Haiku**

Búsquedas en el codebase, lectura de archivos, análisis de estructura. Tareas de solo lectura donde la velocidad importa más que la profundidad.

```bash
/model haiku
```

**4. El atajo: `opusplan`**

Si no quieres cambiar manualmente, `opusplan` automatiza la estrategia:

```bash
claude --model opusplan
# O durante la sesión:
/model opusplan
```

Opus se activa en modo planificación. Cuando Claude pasa a ejecutar, cambia a Sonnet automáticamente. Es exactamente lo que hacen los agentes nativos de Claude Code — cada tarea recibe el modelo justo que necesita.

## Referencia

| Modelo | Alias | Coste relativo | Ideal para |
|---|---|---|---|
| Opus 4.6 | `opus` | $$$ | Arquitectura, debugging complejo, decisiones de diseño |
| Sonnet 4.6 | `sonnet` | $$ | Desarrollo diario, implementación, tests |
| Haiku 4.5 | `haiku` | $ | Exploraciones, búsquedas, tareas simples |
| Opus → Sonnet | `opusplan` | Mixto | Flujo completo: planificar + ejecutar |

## Configuración permanente

Añade el modelo a tu `settings.json` para no tener que elegir en cada sesión:

```json
{
  "model": "opusplan"
}
```

O via variable de entorno:

```bash
export ANTHROPIC_MODEL=opusplan
```

Si además quieres afinar el razonamiento de Opus dentro de la fase de planificación, combina esta estrategia con el [ajuste de effort level en Claude Code](/es/tips/claude-code-effort-level-ajustar-razonamiento): baja el esfuerzo para decisiones rápidas y reserva `high` para las arquitectónicas.

> Documentación oficial: [Model configuration](https://code.claude.com/docs/es/model-config)
