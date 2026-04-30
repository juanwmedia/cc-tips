---
date: 2026-04-09
type: tip
title_es: "Cinco formas de darle a Claude Code el contexto correcto (no solo @)"
title_en: "Five Ways to Give Claude Code the Right Context (Not Just @)"
---
> **TL;DR** La mayoría conoce `@archivo`. Pero hay cinco formas distintas de inyectar contexto en Claude Code — archivos, directorios, imágenes, datos por pipe, e imports en CLAUDE.md. La última es la que casi nadie usa, y cambia cómo arquitecturas toda tu configuración.

La referencia `@` es una de esas features tan básicas que dejas de pensar en ella. Escribes `@`, seleccionas un archivo, listo. Pero precisamente porque parece simple, la mayoría de developers nunca exploran la sintaxis completa — y hay más de lo que parece.

Claude Code tiene cinco métodos de input distintos para proporcionar contexto. Cada uno sirve para algo diferente. Saber cuándo usar cuál es la diferencia entre que Claude adivine y que Claude entienda.

Resultado:

```
> @src/auth/session.ts explica la lógica de token refresh alrededor de la línea 47

Claude lee session.ts desde disco, se enfoca en la línea 47,
y explica el flujo exacto de expiración — sin divagar, sin suponer.
```

## Los cinco métodos

### **1. Referencia @ a archivo**

El movimiento básico. Escribe `@` seguido de una ruta y Claude lee el archivo desde disco antes de responder.

```bash
> @src/api/payments.ts qué expone este módulo?
```

El autocompletado se activa después de `@` — el índice se precalienta al iniciar la sesión con caché basado en sesión, así que las sugerencias aparecen rápido. No necesitas escribir rutas completas.

Dos detalles que la gente pasa por alto:

- **Case-sensitive** en Linux y macOS. `@Auth.ts` y `@auth.ts` son archivos distintos.
- **Matching difuso**: escribir `@Button` puede mostrar tanto `Button.tsx` como `Button.test.tsx`, para que elijas de una lista filtrada.

Combínalo con referencias de línea en lenguaje natural para precisión quirúrgica:

```bash
# Enfoca en un área específica
> @src/auth/session.ts explica la lógica alrededor de la línea 47

# Compara entre archivos
> @src/models/user.ts línea 23 vs @src/models/admin.ts línea 18 — qué diferencia hay?
```

### **2. Referencia @ a directorio**

Apunta a un directorio en vez de un archivo:

```bash
> @src/api/ qué endpoints tenemos?
```

Claude recibe un listado del directorio — nombres de archivo, no su contenido completo. Útil para orientarte antes de entrar en archivos concretos. Ahorra contexto comparado con leer cada archivo individualmente.

### **3. Pegar imágenes**

Pulsa `Ctrl+V` (o `Cmd+V` en iTerm2) con una imagen en el portapapeles:

```
[Image #1] arregla el problema de spacing que se ve en este screenshot
```

Claude recibe la imagen como input visual. El chip `[Image #N]` se inserta en la posición del cursor, así puedes referenciarlo por número en tu prompt. También puedes arrastrar y soltar archivos de imagen directamente en la ventana del terminal.

Funciona con screenshots de bugs de UI, mockups de diseño, diálogos de error, o output del terminal que es difícil de copiar como texto.

### **4. Datos por pipe desde stdin**

```bash
cat error.log | claude "qué está causando esto?"
npm test 2>&1 | claude "qué tests están fallando y por qué?"
git diff HEAD~3 | claude "resume qué cambió"
```

Los datos del pipe entran al contexto igual que una referencia de archivo. La diferencia: funciona con cualquier output de comando, no solo archivos en disco. Útil para logs, output de build, respuestas de API, o diffs que no quieres guardar primero.

### **5. @imports en CLAUDE.md (el patrón avanzado)**

Este es el que casi nadie conoce. Dentro de cualquier CLAUDE.md, `@ruta/al/archivo` importa el contenido de ese archivo al contexto de inicio de sesión:

```markdown
# CLAUDE.md
Ver @README.md para overview del proyecto y @package.json para scripts.

# Workflow
- Convenciones de Git: @docs/git-instructions.md
- Overrides personales: @~/.claude/my-project-instructions.md
```

Esto convierte `@` de una feature del prompt en una **herramienta de arquitectura de configuración**:

- **Imports recursivos**: los archivos importados pueden importar otros, hasta 5 niveles de profundidad
- **Rutas relativas**: se resuelven desde el archivo que importa, no desde el directorio de trabajo
- **Diálogo de aprobación**: la primera vez que Claude encuentra imports externos en un proyecto, pide confirmación
- **Seguro en bloques de código**: `@algun-paquete` dentro de un code block o inline code no dispara un import — puedes documentar nombres de paquetes sin efectos secundarios

El patrón práctico: mantén tu CLAUDE.md principal por debajo de 200 líneas (la recomendación oficial), y haz `@import` de todo lo demás. Arquitectura del proyecto en un archivo, convenciones de testing en otro, estándares de API en un tercero. Cada uno se carga al inicio, pero son lo suficientemente modulares para mantenerlos por separado.

## Referencia

| Método | Sintaxis | Qué recibe Claude |
|---|---|---|
| Referencia a archivo | `@ruta/al/archivo.ts` | Contenido completo leído desde disco |
| Foco por línea | `@archivo.ts` + "línea 47" | Archivo completo, enfocado en esa área |
| Referencia a directorio | `@ruta/al/dir/` | Listado del directorio (solo nombres) |
| Imagen pegada | `Ctrl+V` o arrastrar y soltar | Input visual como chip `[Image #N]` |
| Input por pipe | `cat archivo \| claude "..."` | Stdout del comando como contexto |
| @import en CLAUDE.md | `@ruta` dentro de CLAUDE.md | Contenido cargado al inicio de sesión |

> Documentación oficial: [Best Practices — Provide rich content](https://code.claude.com/docs/en/best-practices) | [CLAUDE.md imports](https://code.claude.com/docs/en/memory)
