> **TL;DR** Creas un worktree con `claude -w`, tu app no arranca, pierdes 5 minutos hasta que descubres que el `.env` no está. Git worktree solo copia archivos tracked — todo lo que tienes en `.gitignore` (`.env`, `.env.local`, `config/secrets.json`) se queda fuera. La solución es un archivo llamado **`.worktreeinclude`** en la raíz del proyecto. Usa sintaxis `.gitignore`, y Claude Code copia automáticamente los archivos que listen **solo si también están gitignored**. Es una invención de Claude Code — git no lo soporta — y se merece estar commiteado en el repo para que todo el equipo lo aproveche.

Soy heavy user de Claude Code y no sabía que existía. Llevo meses usando una skill custom para crear worktrees, y cada vez le pedía a Claude que copiara manualmente los archivos de entorno. Hasta que descubrí que Claude Code resuelve esto con un archivo de una línea que lleva ahí desde que el Desktop lo soporta.

El problema es universal: un worktree es un checkout limpio. Solo tiene lo que git trackea. Todo lo que vive en `.gitignore` — que es exactamente donde están tus secretos, tus variables de entorno y tu configuración local — no existe en el nuevo directorio. Tu app falla, y Claude gasta tokens debuggeando algo que no es un bug.

## El archivo

Crea `.worktreeinclude` en la raíz del proyecto:

```text
# .worktreeinclude
.env
.env.local
config/secrets.json
```

Eso es todo. La próxima vez que ejecutes `claude -w feature-auth`, Claude Code copiará esos archivos al worktree automáticamente. Funciona con:

- `--worktree` desde la CLI
- Worktrees de subagents (`isolation: worktree`)
- Sesiones paralelas en la Desktop app

## Reglas

| Regla | Qué significa |
|---|---|
| Sintaxis `.gitignore` | Soporta `*`, `**`, `!` para negar, `#` para comentarios |
| Solo copia gitignored | Si el archivo está tracked por git, no lo duplica |
| Preserva estructura | `config/secrets.json` crea `config/` en el worktree |
| No recursivo por defecto | `*.env` solo en raíz; `**/*.env` en todo el árbol |

## Ejemplo real: monorepo con múltiples `.env`

```text
# .worktreeinclude
.env
.env.local
apps/web/.env.local
apps/api/.env.local
packages/db/.env
config/master.key
config/credentials/development.key
```

## El patrón que uso: créalo con los hallazgos de la primera sesión

Si trabajas en un proyecto que no tiene `.worktreeinclude`, pídele a Claude que lo cree:

```text
Crea un .worktreeinclude con todos los archivos gitignored
que necesita la app para arrancar. Revisa .gitignore,
los scripts de setup y el README.
```

Claude escanea el proyecto, identifica qué archivos gitignored son necesarios para que la app funcione (`.env`, claves, configs locales), y genera el archivo. Lo subo al repo y todo el equipo se beneficia desde la siguiente sesión.

## No lo gitignores — compártelo

`.worktreeinclude` **no contiene secretos** — contiene *nombres* de archivos que son secretos. Es metadatos, no datos. Commitéalo al repo como commiteas `.gitignore`:

```bash
git add .worktreeinclude
git commit -m "Add .worktreeinclude for worktree env setup"
```

Cualquier compañero que haga `claude -w` después de un `git pull` tendrá su `.env` copiado automáticamente.

## Qué NO hace

- **No crea archivos** — si tu `.env` no existe en el directorio principal, no puede copiarlo
- **No funciona con hooks custom** — si usas un `WorktreeCreate` hook, `.worktreeinclude` se ignora; copia los archivos dentro del hook
- **No es git nativo** — es una invención de Claude Code (otros AI tools como Roo Code y CodeBuddy lo están adoptando, pero git no lo soporta)

Si ya tienes worktrees funcionando, este archivo es el detalle que convierte "funciona para mí" en "funciona para el equipo". Una línea, cero tokens desperdiciados.

Combina con [worktrees paralelos](/es/tips/claude-code-worktrees-tareas-paralelas) si aún no los usas, y con [`/run-skill-generator`](/es/tips/claude-code-run-verify-ejecutar-app) si quieres que Claude también sepa levantar la app en cada worktree sin adivinar.

> Documentación oficial: [Copy gitignored files into worktrees — Claude Code Docs](https://code.claude.com/docs/en/worktrees#copy-gitignored-files-into-worktrees)
