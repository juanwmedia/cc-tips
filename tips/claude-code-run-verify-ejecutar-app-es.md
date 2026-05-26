> **TL;DR** Claude Code v2.1.145 introduce tres skills bundled que cambian cómo Claude dice "hecho": **`/run`** lanza tu app y la maneja como lo haría un usuario, **`/verify`** compila, ejecuta y observa si el cambio se refleja en la app real (no en los tests), y **`/run-skill-generator`** graba la receta de build+launch de tu proyecto para que `/run` y `/verify` nunca más tengan que adivinar. La doctrina detrás: *"Verification is runtime observation. Don't run tests. Don't typecheck."* — literal del propio skill `/verify`.

El problema: le dices a Claude "verifica que funciona" y Claude ejecuta `npm test`. Los tests pasan. Claude dice "hecho". Pero la app no levanta, o el botón no hace nada, o la ruta devuelve 500 en el navegador. Los tests verifican que **el código hace lo que el código dice**, no que **la app funciona como espera el usuario**.

Anthropic decidió cortar esa inercia. Las instrucciones del skill bundled `/verify` son explícitas:

> *"Don't run tests. Don't typecheck. Running them here proves you can run CI — not that the change works."*

Resultado:

```
> /verify

Finding change scope...
  git diff origin/HEAD... --stat → 3 files changed

Building and launching...
  npm run build ✓
  npm run dev → localhost:3000

Driving to the surface...
  curl localhost:3000/api/payments/retry -d '{"id":"pay_123"}'
  → 200 {"status":"retried","next_attempt":"2026-05-26T13:00:00Z"}

Capturing evidence...
  Response matches expected retry behavior ✓
  Screenshot: payment dashboard shows "Retry scheduled" ✓

PASS — change verified at runtime surface
```

## Los tres skills

### **1. `/run` — lanza y maneja tu app**

```bash
/run
```

Detecta el tipo de proyecto (CLI, servidor, TUI, Electron, browser, library) y lo lanza. No como `node index.js` y ya — **interactúa** hasta un punto donde un usuario vería algo:

| Tipo de proyecto | Qué hace `/run` |
|---|---|
| CLI | Ejecuta un comando representativo, comprueba exit code y stdout |
| Servidor / API | Levanta en background + `curl` al endpoint tocado |
| TUI | tmux `send-keys` + `capture-pane` del resultado |
| Desktop GUI (Electron) | Playwright `_electron` REPL bajo xvfb + screenshot |
| Browser | Dev server + `chromium-cli` script |
| Library / SDK | Import desde la interfaz pública del paquete, no desde `./src/` |

Si en tu repo existe un skill de proyecto en `.claude/skills/run-<nombre>/`, `/run` lo sigue literalmente en vez de adivinar. Si no existe, aplica el patrón por tipo.

### **2. `/verify` — la prueba de que el cambio funciona**

```bash
/verify
```

`/verify` va más allá de `/run`: primero lee el diff (`git diff origin/HEAD...`), identifica qué cambió, y luego ejecuta la app **hasta la superficie donde ese cambio se manifiesta**. La superficie es el punto donde un usuario — humano o programático — encuentra el cambio.

Reglas que sigue el skill:

- **Función interna que no es superficie** → sigue la cadena de llamadas hasta la CLI, el socket o la ventana
- **Solo cambios en tests** → `SKIP — no runtime surface`, no intenta rellenar el hueco corriendo tests
- **PR mixto (src + tests)** → verifica el src, ignora los tests (CI los corre)
- **Sin superficie runtime** (docs, type declarations) → `SKIP — no runtime surface: (reason)`

### **3. `/run-skill-generator` — graba la receta una vez**

```bash
/run-skill-generator
```

`/run` y `/verify` infieren cómo levantar tu proyecto desde `README`, `package.json` o `Makefile`. Eso funciona para proyectos estándar. Pero si necesitas una base de datos, un `.env`, variables de entorno específicas o un build multi-paso, la inferencia falla.

`/run-skill-generator` **arranca tu proyecto desde cero en un entorno limpio**, captura todo lo que funcionó (los `apt-get install` exactos, las variables de entorno, los parches, el script de driver), y lo commitea como un skill de proyecto:

```
mi-proyecto/.claude/skills/run-mi-proyecto/
├── SKILL.md          # instrucciones cortas + referencia al driver
└── driver.mjs        # harness programático para interactuar con la app
```

A partir de ahí, `/run`, `/verify` y **cualquier otro agente en el repo** siguen la receta grabada en vez de redescubrirla. Ejecútalo una vez por proyecto, y otra vez si cambia el proceso de build o launch.

Lo que el generator exige antes de dar por terminado (su propia "Definition of Done"):

1. **La app se ejecutó de verdad** — no basta con que compile
2. **El harness de interacción está commiteado** — un driver (JS, Python, shell) o smoke test vive junto al SKILL.md
3. **El SKILL.md documenta el harness** — la ruta del agente describe el driver primero, no comandos genéricos de setup
4. **Cada code block se ejecutó y validó** — todos los comandos del skill se corrieron en la sesión

## Cuándo usar cada uno

| Situación | Skill |
|---|---|
| "Quiero ver si la app funciona después de mi cambio" | `/verify` |
| "Levanta la app para que pueda probarla" | `/run` |
| "Enséñale a Claude cómo se levanta este proyecto" | `/run-skill-generator` |
| "Los tests pasan pero la app no funciona" | `/verify` (ese es exactamente su caso de uso) |

## Requisitos

- Claude Code **v2.1.145+** (los tres skills se introdujeron en esta versión)
- Para GUI: `xvfb` disponible (el skill lo detecta automáticamente)
- Para proyectos complejos: ejecutar `/run-skill-generator` una vez antes de confiar en `/run` y `/verify`

Los tres son skills bundled — viven dentro de Claude Code, no hay nada que instalar. Si ya tienes skills de proyecto que cubren el build/launch (creadas con [`/run-skill-generator`](/es/tips/claude-code-run-verify-ejecutar-app) o manualmente siguiendo las [5 reglas de Anthropic para crear skills](/es/tips/claude-code-crear-skills-5-reglas-anthropic)), `/run` y `/verify` las prefieren sobre la inferencia automática. Si quieres entender la diferencia entre skills, hooks, MCP y plugins, revisa la [comparativa completa](/es/tips/claude-code-skills-hooks-mcp-plugins-comparativa).

> Documentación oficial: [Run and verify your app — Claude Code Docs](https://code.claude.com/docs/en/skills#run-and-verify-your-app) · [Commands reference](https://code.claude.com/docs/en/commands)
