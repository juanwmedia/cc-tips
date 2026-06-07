---
date: 2026-06-06
type: tip
title_es: "Claude Code va lento, se cuelga o se come la RAM: la lista de fixes que no sabías que existían"
title_en: "Claude Code slow, hanging, or eating your RAM: the fix list you didn't know existed"
---

> **TL;DR** Antes de pelearte: ¿es una caída o "Claude está más tonto"? Eso es [otro diagnóstico](/es/tips/claude-code-caido-diagnostico). Lanza [`/doctor`](/es/tips/claude-code-doctor-diagnostico) primero. Si no es ni lo uno ni lo otro y es Claude Code en sí (CPU/RAM disparada, cuelgue, terminal con texto corrupto, búsqueda que no encuentra archivos), cada síntoma tiene su arreglo: `/heapdump` para ver la memoria, `Ctrl+C` + `claude --resume` para cuelgues, `/terminal-setup` para el texto corrupto, e instalar `ripgrep` + `USE_BUILTIN_RIPGREP=0` para la búsqueda rota.

"Claude Code va lento" puede ser tres cosas distintas, y cada una se arregla en otro sitio. Antes de tocar nada, descarta las dos fáciles: si sospechas una **caída** o que "el modelo está más tonto hoy", eso casi siempre es presión de contexto y lo cubre [¿está caído o eres tú?](/es/tips/claude-code-caido-diagnostico). Y `/doctor` te audita el setup en una pasada. Este tip es la **tercera** rama: cuando el problema es el proceso en sí.

## Cómo se ve

```text
> /heapdump

Wrote heap snapshot + memory breakdown to ~/Desktop:
  claude-heap-<ts>.heapsnapshot
  claude-memory-<ts>.txt

  RSS (resident)          1.842 MB
  JS heap                   612 MB
  Array buffers             340 MB
  Native (sin contabilizar) 890 MB   ← si esto domina, el leak es nativo, no JS
```

## Los arreglos, por síntoma

**1. CPU o RAM disparada**

Claude Code es un proceso de Node; con codebases grandes se hincha. En orden:

- `/compact` cada cierto tiempo para reducir el contexto.
- Cierra y reinicia entre tareas grandes (no pierdes la conversación: `claude --resume`).
- Mete los directorios de build pesados en tu `.gitignore`.

Si la memoria sigue alta, `/heapdump` escribe un snapshot **y un desglose de memoria** en `~/Desktop` (en Linux sin carpeta Desktop, en tu home). El desglose separa RSS, JS heap, array buffers y memoria nativa sin contabilizar, así sabes si el crecimiento es de objetos JS o de código nativo. Abre el `.heapsnapshot` en Chrome DevTools → Memory → Load para ver los retainers, y adjunta ambos archivos si reportas el problema en GitHub.

**2. Se cuelga o no responde**

```bash
# 1. Cancela la operación en curso
Ctrl+C

# 2. Si sigue muerto, cierra el terminal y reinicia.
#    No pierdes la conversación:
claude --resume
```

**3. Texto corrupto en el terminal integrado del editor**

Si en el terminal de VS Code, Cursor o Devin ves cajas, manchas o glifos raros, suele ser el render por GPU. Dentro de Claude Code:

```bash
/terminal-setup
```

Pone `terminal.integrated.gpuAcceleration` en `"off"` por ti.

**4. La búsqueda no encuentra archivos**

Si el Search, las menciones `@archivo` o las skills no encuentran nada, el `ripgrep` que trae Claude Code no corre en tu sistema. Instala el del sistema y dile que lo use:

```bash
brew install ripgrep      # macOS (apt / pacman / winget en otros SO)
export USE_BUILTIN_RIPGREP=0
```

**5. Búsqueda lenta o incompleta en WSL**

Cruzar entre el sistema de archivos de Windows y el de Linux penaliza la lectura, así que en WSL la búsqueda devuelve menos resultados de los esperados. Sé específico ("busca la validación JWT en el paquete auth"), o mueve el proyecto al FS de Linux (`/home/`). El detalle que importa: **`/doctor` te marcará Search como OK igual**. Es el único fallo de esta lista que no caza.

## Referencia

| Síntoma | Arreglo |
|---|---|
| RAM/CPU alta | `/compact`, reiniciar entre tareas, build dirs al `.gitignore`, `/heapdump` para diagnosticar |
| Cuelgue | `Ctrl+C`; si no, reinicia y `claude --resume` |
| Texto corrupto en terminal del editor | `/terminal-setup` (apaga la GPU del terminal) |
| Search no encuentra archivos | Instala `ripgrep` del sistema + `USE_BUILTIN_RIPGREP=0` |
| Search lento/incompleto en WSL | Búsquedas específicas o proyecto en `/home/` (y ojo: `/doctor` lo da por bueno) |

¿El "lento" es en realidad un turno que se reprocesa entero? Eso es la caché, no el proceso: lo cubre [prompt caching](/es/tips/claude-code-prompt-caching-turno-lento-consumo).

> Documentación oficial: [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
