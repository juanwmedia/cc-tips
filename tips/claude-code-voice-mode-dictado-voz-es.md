---
date: 2026-03-24
type: tip
title_es: "Programa con la voz: Voice Mode en Claude Code"
title_en: "Code by Voice: Voice Mode in Claude Code"
---

# Quick Tip: Programa con la voz: Voice Mode en Claude Code

> **TL;DR** Activa `/voice`, mantén pulsada la barra espaciadora y habla. Claude Code transcribe en streaming — ves las palabras aparecer mientras hablas. Sueltas y el prompt está listo. Mezcla voz y teclado en el mismo mensaje.

Hay una tendencia clara en el mundo de agentes AI: la interacción por voz. Escribir prompts largos y descriptivos en un terminal es lento. Dictarlos es más natural, más rápido, y mantiene las manos libres para consultar código o documentación en otra ventana.

Claude Code lo ha incorporado con transcripción en streaming — no esperas a terminar de hablar para ver el texto. Las palabras aparecen en tiempo real mientras dictas, optimizadas para vocabulario de desarrollo: `regex`, `OAuth`, `JSON`, `localhost` se transcriben correctamente. Incluso detecta el nombre de tu proyecto y tu rama de git actual como hints de reconocimiento.

En mi experiencia todavía funciona un poco irregular — a veces la detección de "mantener pulsado" tarda, o la transcripción no clava términos muy específicos. Pero es bueno tenerlo como opción, y mejorará.

Resultado:

```
> /voice
Voice mode enabled. Hold Space to record. Dictation language: es

> [mantén Space, habla: "refactoriza el middleware de auth
   para usar el nuevo helper de validación de tokens"]

> refactoriza el middleware de auth para usar el nuevo
  helper de validación de tokens▮
```

## Configuración

### **1. Activar Voice Mode**

```
/voice
```

Persiste entre sesiones. Para desactivarlo, ejecuta `/voice` de nuevo.

### **2. Hablar**

Mantén `Space` pulsada y habla. Verás `keep holding…` brevemente, luego una onda de audio en vivo. Suelta para finalizar.

El texto se inserta en la posición del cursor — puedes dictar en cualquier punto del prompt y combinar con texto escrito.

### **3. Cambiar el idioma**

El dictado usa el mismo `language` de tu configuración. Si no está definido, usa inglés por defecto:

```json
{
  "language": "es"
}
```

### **4. Cambiar la tecla push-to-talk (recomendado)**

`Space` tiene un warmup porque necesita distinguir entre pulsación y escritura. Con una combinación de modificador arrancas al instante:

```json
// ~/.claude/keybindings.json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "meta+k": "voice:pushToTalk",
        "space": null
      }
    }
  ]
}
```

## Referencia

| Aspecto | Detalle |
|---|---|
| Activar | `/voice` (toggle) |
| Tecla por defecto | `Space` (mantener pulsada) |
| Transcripción | Streaming en tiempo real |
| Vocabulario | Optimizado para desarrollo (regex, OAuth, JSON, etc.) |
| Hints automáticos | Nombre del proyecto + rama git actual |
| Idiomas | 20 idiomas (en, es, fr, de, ja, ko, pt, etc.) |
| Persistencia | Se mantiene activo entre sesiones |
| Requisitos | claude.ai login (no API key), micrófono local |
| Versión mínima | v2.1.69+ |

> Documentación oficial: [Voice dictation](https://code.claude.com/docs/en/voice-dictation)

## Requisitos

- Claude Code v2.1.69+
- Cuenta claude.ai (no funciona con API key, Bedrock, Vertex ni Foundry)
- Acceso al micrófono local (no funciona en SSH ni entornos remotos)
- macOS/Linux/Windows (en Linux puede necesitar SoX o ALSA utils)
