---
date: 2026-06-04
type: tip
title_es: "Prompt caching en Claude Code: por qué tu siguiente turno va lento y dispara el consumo (y cómo evitarlo)"
title_en: "Prompt caching in Claude Code: why your next turn is slow and expensive (and how to avoid it)"
---

> **TL;DR** A veces una sesión se vuelve astronómicamente más lenta y dispara el consumo, y al principio no sabes por qué. Casi siempre es la caché. Claude Code cachea el prefijo de cada petición de forma automática; ciertos cambios a mitad de sesión lo invalidan y el siguiente turno reprocesa toda la conversación a precio completo. La regla de oro: elige modelo y effort al arrancar y no los toques a mitad de tarea.

Claude Code gestiona el **prompt caching** por ti, así que no es algo que configures. Es algo que conviene no romper sin querer. Saber qué lo invalida es la diferencia entre una sesión fluida y una que de repente se arrastra.

## Cómo funciona la caché

En cada turno el modelo no recuerda nada del anterior, así que Claude Code reenvía todo el contexto (system prompt, tu CLAUDE.md, todos los mensajes previos) y añade lo nuevo al final. La API cachea **por prefijo**: compara el principio de tu petición con lo que ya procesó. El match es exacto, así que un cambio en cualquier punto del prefijo recomputa todo lo que viene detrás. No hay caché por archivo ni por fragmento.

Para aprovecharlo, Claude Code ordena la petición de lo más estable a lo más cambiante:

| Capa | Contenido | Cambia cuando |
|---|---|---|
| System prompt | Instrucciones base, definiciones de tools, output style | Cambia el set de tools cargadas, o actualizas Claude Code |
| Contexto de proyecto | CLAUDE.md, memoria, reglas | Arranca la sesión, o tras `/clear` o `/compact` |
| Conversación | Tus mensajes, respuestas de Claude, resultados de tools | Cada turno |

Un cambio en la conversación deja intactas las dos capas de arriba. Un cambio en el system prompt invalida **todo**. Y hay dos cosas que ni siquiera son texto pero también forman parte de la clave de caché: el **modelo** y el **effort level**. Cambiar cualquiera de los dos arranca una caché nueva desde cero.

## Cómo se ve

```text
# Caché sana (lo normal)
cache_read_input_tokens:      48.231   ← se reutiliza, ~10% del precio de input
cache_creation_input_tokens:     412   ← solo lo nuevo de este turno

# El turno después de cambiar de modelo a mitad de sesión
cache_read_input_tokens:           0   ← cero aciertos
cache_creation_input_tokens:  48.643   ← reprocesa TODO a precio completo
```

Una lectura cacheada cuesta **~10% del precio de input** (según la doc oficial). Un fallo de caché paga el precio completo: por eso ese turno va lento y consume del orden de 10× más en input.

## Las tres categorías que tienes que distinguir

**1. Lo que rompe la caché (evítalo a mitad de tarea)**

- Cambiar de modelo con `/model` (y el toggle de plan mode con `opusplan`, que es un cambio de modelo encubierto).
- Cambiar el effort con `/effort`. Claude Code te pide confirmación precisamente porque sabe que penaliza.
- Activar fast mode.
- Denegar una herramienta entera (`Bash` o `WebFetch` a secas; las reglas con ámbito como `Bash(rm *)` y todas las de allow/ask no rompen nada).
- Actualizar Claude Code y retomar una sesión larga: el primer turno reprocesa toda la historia, suele ser la petición que más consume de toda la sesión.

**2. Lo que resetea la caché por diseño, pero apenas penaliza (no lo temas)**

- `/compact`: invalida solo la capa de conversación. El resumen se genera leyendo la caché y el turno siguiente reconstruye una historia mucho más corta, así que no es la parte lenta. Lánzalo en pausas naturales entre tareas.
- `/clear`: empiezas de cero a propósito.
- `/rewind`: trunca a un prefijo que ya estaba cacheado, así que abandonas un camino sin reconstruir la caché, a diferencia de `/compact`, que construye una nueva.

**3. Lo que es seguro siempre**

- Editar archivos, invocar skills y comandos, `/recap`, cambiar de modo de permisos, lanzar subagentes.
- Editar CLAUDE.md o el output style a mitad de sesión **no** rompe la caché, pero tampoco se aplica: Claude sigue con la versión que cargó al arrancar hasta el próximo `/clear` o reinicio.

> Sobre MCP y plugins: por defecto, en Opus y Sonnet, las tools de MCP van diferidas y conectar o desconectar un servidor no toca la caché. Solo la rompe cuando las tools se cargan en el prefijo (Haiku, Vertex, un gateway propio, o `alwaysLoad`). En el caso normal, tranquilo.

## Comprueba si tu caché está sana

Los dos números viven en el objeto `current_usage` que la API devuelve en cada respuesta, y lo más cómodo es leerlos desde un [script de statusline](/es/tips/personaliza-tu-status-line-en-claude-code):

- `cache_read_input_tokens`: tokens servidos desde caché (a ~10% del input).
- `cache_creation_input_tokens`: tokens escritos a la caché este turno.

Mucha lectura y poca creación significa que la caché trabaja a tu favor. Si la creación se mantiene alta turno tras turno, algo en tu prefijo está cambiando: repasa la lista de arriba.

## Estira la caché si trabajas a ratos (TTL)

La caché expira tras un rato de inactividad, y cada acierto reinicia el contador:

- Por defecto, 5 minutos.
- Con **suscripción de Claude**: Claude Code pide la TTL de 1 hora automáticamente y sin coste extra (tu uso va incluido en el plan).
- Con API key, Bedrock o Vertex: pagas por token, así que se queda en 5 minutos salvo que pongas `ENABLE_PROMPT_CACHING_1H=1`.
- Forzar 5 minutos para depurar: `FORCE_PROMPT_CACHING_5M=1`.

Esto es la otra cara de [10 hábitos para ahorrar tokens](/es/tips/claude-code-ahorrar-tokens-10-habitos): ahí reduces el tamaño del contexto; aquí evitas pagarlo dos veces. Y si quieres ver el gasto real, [/usage y /stats](/es/tips/claude-code-uso-tokens-usage-stats) te lo cuentan.

> Documentación oficial: [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)

**Requisitos:** mantener la cabecera de fast mode entre toggles necesita Claude Code v2.1.86+. Las variables `ENABLE_PROMPT_CACHING_1H`, `FORCE_PROMPT_CACHING_5M` y `DISABLE_PROMPT_CACHING` van en el bloque `env` de los settings.
