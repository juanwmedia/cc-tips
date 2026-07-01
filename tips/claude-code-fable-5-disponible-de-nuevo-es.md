---
date: 2026-06-30
type: tip
title_es: "Fable 5 disponible de nuevo en Claude Code: esto es todo lo que tienes que saber"
title_en: "Fable 5 is back in Claude Code: everything you need to know"
---

> **TL;DR** Fable 5 vuelve a Claude Code el **1 de julio**, tras suspenderse el 12 de junio por un control de exportación de EE.UU. Regresa con un **clasificador de seguridad más estricto**: bloquea la técnica del incidente en más del 99% de los casos, pero a cambio salta con más falsos positivos en tareas normales de código. Cuando bloquea, tu petición pasa a **Opus 4.8** con aviso. No tienes que hacer nada para recuperarlo.

El 9 de junio salió Fable 5. Tres días después desapareció de tu picker casi sin explicación. La razón: unos investigadores de Amazon encontraron cómo esquivar sus salvaguardas para que identificara vulnerabilidades de software, y el gobierno de EE.UU. aplicó un control de exportación que obligaba a restringir el acceso a extranjeros. Como Anthropic no podía verificar la nacionalidad de cada usuario en tiempo real, cortó el acceso a todos. Ahora vuelve.

## Qué cambia para ti

Vuelve el mismo modelo, pero con la seguridad reforzada. Y ese refuerzo tiene un efecto secundario que sí notarás programando:

- **Un clasificador nuevo, y más sensible.** Anthropic entrenó un clasificador que bloquea la técnica del informe en **>99%** de los casos. El margen es más amplio, así que espera **más falsos positivos en tareas rutinarias de código y debugging**, no solo en seguridad o biología.
- **El reenvío a Opus 4.8 salta más.** Cuando una petición se marca, Claude Code te avisa y la manda a Opus 4.8, y la sesión sigue en Opus. Ya pasaba antes; ahora ocurrirá con más frecuencia.
- **Acceso por plan hasta el 7 de julio.** Durante la primera semana el acceso depende de tu plan; después, de tus créditos de uso.

## Qué hacer (poco)

No hay que instalar ni activar nada: Fable 5 reaparece solo en tu picker el 1 de julio (con `claude update` si tu versión es vieja). Lo útil es saber reaccionar al reenvío:

```bash
# Si una petición se bloquea, estás en Opus 4.8. Para volver a Fable:
/model fable

# Para decidir tú cada vez en vez de que cambie solo:
/config   # → apaga "switch models when a message is flagged"
```

Y si el reenvío te salta ya en el primer mensaje, a menudo lo dispara tu propio contexto (`CLAUDE.md`, nombres de directorio, git status). Para comprobarlo, arranca en [modo seguro](/es/tips/claude-code-modo-seguro) con `claude --safe-mode`.

Todo el detalle de qué es Fable 5, cómo entrar, cuándo merece la pena y cómo funciona ese reenvío está en el tip de fondo: [Fable 5 en Claude Code, el modelo por encima de Opus](/es/tips/claude-code-fable-5-por-encima-de-opus).

## La cronología

| Fecha | Qué pasó |
|---|---|
| 9 jun | Salen Fable 5 y Mythos 5 |
| 12 jun | Control de exportación de EE.UU.; Anthropic suspende el acceso a todos |
| 26 jun | Mythos 5 restaurado |
| 30 jun | Se levanta el control sobre Fable 5 |
| **1 jul** | **Fable 5 disponible de nuevo, global, incluido Claude Code** |

> Documentación oficial: [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5) · [Model configuration](https://code.claude.com/docs/en/model-config)

## Requisitos

- Claude Code v2.1.170+ para ver Fable 5 en el picker (`claude update`). No disponible bajo zero data retention.
