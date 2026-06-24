---
date: 2026-06-24
type: tip
title_es: "Prompts en Claude Code: las 5 reglas que sigue Anthropic"
title_en: "Prompts in Claude Code: the 5 rules Anthropic actually follows"
---
> **TL;DR** Antes de pedirle nada a Claude Code, incluye estas cinco piezas en el prompt: el objetivo en una frase, el archivo concreto con `@`, el porqué de la restricción, la instrucción en positivo, y un ejemplo de entrada y salida. Las cinco salen de la documentación oficial de Anthropic. Valen para vibe coding y para código de producción.

La industria profesional está obsesionada con specs. `/spec`, `spec-driven development`, plantillas markdown de 800 líneas antes de tocar una sola línea. Vale para tu monorepo de producción. No vale cuando estás resolviendo algo en quince minutos, ni cuando empiezas, ni cuando estás haciendo vibe coding y solo quieres avanzar.

Para todo eso queda el prompt. Y un buen prompt sigue siendo la unidad atómica de Claude Code, también en 2026. Anthropic publicó hace meses dos páginas de documentación que casi nadie lee enteras: `best-practices` y `prompt-engineering`. De ellas salen estas cinco reglas.

Resultado:

```
# Mal
> arregla el login

# Bien
> Cambia el flujo de login para que, al validar el email,
  redirija a /dashboard en vez de a /home.

  Archivo: @src/auth/session.ts

  Por qué: /dashboard ya tiene el contexto del usuario cargado.
  /home hace un round-trip extra que se nota como lentitud.

  Cambio mínimo: no refactorices nada alrededor, no toques
  los tests, no añadas comentarios.

  Ejemplo del comportamiento esperado:
    Antes: login OK → router.push('/home') → fetch user → render
    Después: login OK → router.push('/dashboard') → render
```

## Las cinco reglas

### **1. El objetivo en una frase, no la tarea**

La *golden rule* de Anthropic: enseña tu prompt a un compañero que no tenga contexto. Si él se confunde, Claude también. No describas la acción ("arregla"); describe el resultado ("redirige a /dashboard al validar el email"). El verbo importa: di **qué cambia para el usuario o para el código**, no qué tipo de trabajo quieres que haga Claude.

### **2. Apunta el archivo con `@`**

Casi cualquier prompt mejora si lleva un `@ruta/al/archivo` dentro. Claude lo lee desde disco antes de responder y deja de alucinar APIs o nombres de funciones. Es la diferencia entre "explícame cómo se valida el token" y "explícame cómo se valida el token en `@src/auth/session.ts`". Si no sabes qué archivo es, usa `@src/auth/` para que Claude vea el listado del directorio primero.

Combínalo con las [otras cuatro formas de inyectar contexto](/es/tips/claude-code-cinco-formas-contexto-correcto): pipe, imagen, directorio, e import en CLAUDE.md.

### **3. Di el porqué, no solo la regla**

Esta es la que casi nadie aplica. Anthropic lo ilustra con un ejemplo que ya es clásico:

- Regla pelada: `NUNCA uses puntos suspensivos`
- Regla + porqué: `Tu respuesta la va a leer un sintetizador de voz, nunca uses puntos suspensivos porque no sabe pronunciarlos`

La diferencia es enorme. Con el porqué, Claude generaliza correctamente en los casos límite que tú no has previsto. Sin él, sigue la regla literal y rompe en cuanto el escenario cambia un poco.

### **4. Pide en positivo, instruye en imperativo**

Dos sub-reglas que vienen de la misma página de docs:

**Positivo, no negativo.** "No uses markdown" funciona peor que "redacta en párrafos de prosa continua". El cerebro de Claude (igual que el tuyo) se ancla mejor en lo que SÍ debe hacer.

**Imperativo, no consultivo.** "¿Podrías sugerir algunos cambios para mejorar esta función?" hace que Claude solo sugiera. "Modifica esta función para que cachee el resultado" hace que la modifique. Si quieres acción, usa el verbo de acción.

### **5. Pega un ejemplo de entrada y salida**

El *multishot* sigue siendo la palanca más infravalorada. Para vibe coding basta un ejemplo:

```
Entrada: usuario sin email_verified
Salida esperada: redirect /verify-email
```

Para tareas serias, Anthropic recomienda 3 a 5 ejemplos envueltos en etiquetas `<example>`. El ejemplo le da a Claude lo que ninguna descripción consigue: el formato exacto, el tono, la longitud, los casos límite. Si solo puedes hacer una cosa de esta lista, haz esta.

## Cuándo el prompt deja de ser suficiente

Cuando el cambio toca más de tres archivos a la vez, cuando hay decisiones de diseño que afectan a cómo se llamará el código dentro de seis meses, o cuando vas a iterar sobre la misma feature durante varios días. Ahí ya merece la pena el [plan mode](/es/tips/claude-code-modos-permisos-shift-tab) o una spec corta. Para todo lo demás, las cinco reglas de arriba bastan.

## Referencia

| Regla | Pregunta que responde | Coste de saltársela |
|---|---|---|
| Objetivo en una frase | ¿Qué cambia exactamente? | Claude inventa el objetivo |
| Archivo con `@` | ¿De qué código hablamos? | Alucinaciones de APIs |
| El porqué | ¿Por qué esta restricción? | Falla en casos límite |
| Pide en positivo | ¿Qué SÍ quieres? | Output a contracorriente |
| Ejemplo input→output | ¿Cómo es "bien hecho"? | Formato y tono erráticos |

> Documentación oficial: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) y [Prompt engineering — Be clear and direct](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
