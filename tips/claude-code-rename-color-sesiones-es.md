---
date: 2026-03-23
type: tip
title_es: "Distingue tus sesiones de Claude Code de un vistazo"
title_en: "Tell Your Claude Code Sessions Apart at a Glance"
---
# Quick Tip: Distingue tus sesiones de Claude Code de un vistazo

> **TL;DR** Usa `/rename` para dar un nombre a tu sesión y `/color` para cambiar el color de la barra del prompt. Cuando tengas varias sesiones abiertas o quieras encontrar una antigua con `/resume`, nombre + color es la diferencia entre "¿cuál era?" y saberlo al instante.

Gestionar sesiones en Claude Code es una de sus áreas más débiles. Todo se ve igual: misma barra, mismo color, sin título. Si trabajas con varias sesiones en paralelo o necesitas retomar una conversación de hace días, distinguirlas es un ejercicio de memoria.

`/rename` y `/color` no resuelven el problema de raíz, pero lo hacen mucho más llevadero. Con un nombre descriptivo y un color propio, cada sesión tiene identidad visual. Y cuando uses `/resume` para buscar sesiones anteriores, el nombre que le diste aparece como texto buscable.

Resultado:

```
> /rename auth-refactor
> /color blue

# La barra del prompt ahora muestra "auth-refactor" con borde azul.
# Al hacer /resume, la sesión aparece listada como "auth-refactor".
```

## Cómo usarlo

### **1. Nombrar al arrancar (recomendado)**

```bash
claude -n "auth-refactor"
```

El nombre aparece en la barra del prompt y en `/resume`. Puedes retomar la sesión directamente:

```bash
claude -r "auth-refactor"
```

### **2. Renombrar durante la sesión**

```
/rename auth-refactor
```

Sin argumentos, `/rename` genera un nombre automático basado en la conversación. Mi recomendación: ponlo tú. Los nombres auto-generados son genéricos y difíciles de recordar.

### **3. Asignar un color**

```
/color blue
```

Cambia el color del borde de la barra de entrada. Útil cuando tienes varias pestañas de terminal abiertas — cada una con un color distinto.

### **4. Encontrar sesiones con /resume**

```
/resume
```

Abre un selector interactivo. Puedes buscar por nombre, pulsar `R` para renombrar una sesión, o `P` para previsualizarla.

## Referencia

| Comando | Qué hace |
|---|---|
| `claude -n "nombre"` | Nombra la sesión al arrancar |
| `/rename nombre` | Renombra la sesión en curso |
| `/rename` (sin args) | Auto-genera nombre desde el contexto |
| `/color color` | Cambia el color del borde del prompt |
| `/resume` | Selector interactivo de sesiones (`R` = rename, `P` = preview) |
| `claude -r "nombre"` | Retoma una sesión por nombre desde la CLI |

| Limitación | Detalle |
|---|---|
| Directorio | Las sesiones están vinculadas al directorio de trabajo. `/resume` solo muestra sesiones del directorio actual. |
| Persistencia del color | El color se aplica a la sesión actual. No persiste al retomarla. |

> Documentación oficial: [CLI reference — Session flags](https://code.claude.com/docs/en/cli-reference)
