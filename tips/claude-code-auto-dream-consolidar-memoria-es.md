---
date: 2026-04-05
type: tip
title_es: "Auto Dream: Claude Code Consolida tu Memoria Mientras Descansas"
title_en: "Auto Dream: Claude Code Consolidates Your Memory While You Rest"
---
Auto memory escribe notas. Auto Dream las limpia. Después de suficientes sesiones, tus archivos de memoria acumulan contradicciones, entradas obsoletas, observaciones duplicadas y fechas relativas que ya no tienen sentido. Auto Dream es un sub-agente en background que revisa las transcripciones de sesiones recientes, extrae lo relevante y reorganiza tus archivos de memoria en algo coherente. Se ejecuta entre sesiones sin bloquear tu trabajo.

> **TL;DR** Auto Dream consolida tus archivos de memoria automáticamente. Revisa `/memory` para ver si está habilitado. Si lo necesitas bajo demanda, di "consolida mis archivos de memoria" en cualquier sesión. El comando `/dream` existe pero aún se está desplegando.

Resultado:

```
Memory consolidation
51s · reviewing 3 sessions

Status: running

Starting memory consolidation. Let me orient first.

Now let me read all existing memory files and search
recent sessions for new signals.

Let me search for key signals in these sessions
— user corrections, preferences, new projects,
and feedback.
```

## Cómo funciona

Auto Dream sigue cuatro fases, cada una con un propósito específico:

### **1. Orientarse**

Claude escanea el directorio de memoria, lee MEMORY.md y revisa los archivos de temas existentes. Esto construye un mapa de todo lo almacenado antes de hacer cambios.

### **2. Recoger señales**

El sub-agente busca en las transcripciones de sesiones recientes (archivos JSONL) patrones de alto valor: correcciones del usuario, peticiones explícitas de guardar, temas recurrentes y decisiones clave. Usa términos de búsqueda específicos en vez de leer transcripciones enteras.

### **3. Consolidar**

La información nueva se integra en los archivos de temas existentes. Aquí ocurre el mantenimiento crítico:

- Los hechos contradichos se eliminan en su origen
- Las fechas relativas se convierten a absolutas ("ayer" pasa a ser "2026-04-04")
- Las entradas duplicadas se fusionan en una sola nota limpia

### **4. Podar e indexar**

MEMORY.md se actualiza para mantenerse bajo 200 líneas (~25KB) — el límite de carga al iniciar sesión. Se eliminan punteros obsoletos, se acortan entradas verbosas y se resuelven contradicciones entre archivos.

## Cómo usarlo

### **Comprobar si auto-dream está habilitado**

```
/memory
```

Busca `Auto-dream: on` en el selector. Si lo ves, la consolidación ya se ejecuta entre sesiones.

### **Ejecutar manualmente**

El comando `/dream` es el trigger manual previsto, pero aún se está desplegando y puede devolver "Unknown skill" en algunas versiones. Como alternativa:

```
> Consolida mis archivos de memoria
```

Esto consigue el mismo resultado dentro de tu sesión actual.

### **Cuándo ejecutar manualmente**

Después de cambios grandes — migraciones de framework, refactors amplios, directorios renombrados — tus archivos de memoria contendrán referencias obsoletas. Una consolidación manual las limpia de inmediato en vez de esperar al siguiente ciclo automático.

## Referencia

| Fase | Qué hace |
|---|---|
| Orientarse | Lee el directorio de memoria, construye mapa del estado actual |
| Recoger señales | Busca en transcripciones: correcciones, decisiones, patrones |
| Consolidar | Integra nueva info, elimina contradicciones, corrige fechas |
| Podar e indexar | Mantiene MEMORY.md bajo 200 líneas, limpia punteros obsoletos |

| Detalle | Valor |
|---|---|
| Alcance | Solo escribe en archivos de memoria — nunca toca código fuente |
| Se ejecuta | Automáticamente entre sesiones; manualmente via prompt |
| `/dream` | Trigger manual, aún en despliegue (puede no funcionar en todas las versiones) |
| Visibilidad | Aparece como "Memory consolidation" en `/tasks` mientras corre |

**Relacionado:** [Memoria automática entre sesiones](/es/tips/claude-code-memoria-automatica-entre-sesiones)

> Documentación oficial: [Cómo Claude recuerda tu proyecto](https://code.claude.com/docs/en/memory)
