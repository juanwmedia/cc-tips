> **TL;DR** Claude Code tiene una herramienta `LSP` integrada que le da navegación de código con precisión de compilador: `goToDefinition`, `findReferences`, diagnósticos de tipos automáticos tras cada edición. Pero viene **apagada**: necesitas (1) instalar el binario del language server (`npm install -g typescript-language-server typescript`), (2) instalar el plugin de code intelligence (`/plugin install typescript-lsp@claude-plugins-official`) y (3) `/reload-plugins`. El error nº1: instalar solo el plugin. **El plugin no instala el binario — es solo el adaptador.** Lo confirma su propio README oficial.

Soy heavy user de Claude Code y descubrí esto hace literalmente una hora. Al probar la herramienta LSP sobre un archivo `.ts` me devolvía `No LSP server available for file type: .ts`: la navegación con precisión de IDE estaba ahí, integrada, pero apagada. La encendimos para TypeScript en tres pasos — y hay plugins oficiales para Rust, Python, Go y ocho lenguajes más.

Sin LSP, cuando le pides a Claude "¿dónde se define `greet` y quién la llama?", la respuesta sale de `grep`: te devuelve *todas* las coincidencias textuales — comentarios, strings, `greeting`, `greetUser`, la definición y las llamadas, todo mezclado. Claude tiene que abrir varios archivos para desambiguar, cargando contexto que no necesita. Con LSP, `goToDefinition` devuelve **una** ubicación exacta, resuelta semánticamente. Cero falsos positivos, cero lecturas de desambiguación.

## Lo que gana Claude

| Capacidad | Qué hace |
|---|---|
| `goToDefinition` | Salta a la definición exacta de un símbolo (no la primera coincidencia de texto) |
| `findReferences` | Lista las referencias reales, resueltas por scope — no `grep` |
| `hover` | Firma de tipos e info al vuelo: `function greet(user: User): string` |
| Diagnósticos automáticos | Tras cada edición, el server reporta errores de tipo en el mismo turno |

El beneficio más infravalorado son los **diagnósticos automáticos**. Sin LSP, el bucle para validar un cambio es: edito → corro `tsc` (que vuelca muchísimo output a contexto) → leo errores → re-edito. Con LSP, si introduzco un import roto o un tipo incorrecto, Claude lo ve y lo arregla en el mismo turno, sin el volcado del compilador.

## El malentendido que te va a morder

El plugin **no instala** el language server. Su README oficial lo deja claro — su sección de instalación es literalmente `npm install -g typescript-language-server typescript`. Hay dos piezas distintas:

| Pieza | Qué es | Quién la instala |
|---|---|---|
| El binario (`typescript-language-server`) | El motor que entiende los tipos | **Tú**, vía `npm install -g` |
| El plugin (`typescript-lsp`) | El adaptador: ~15 líneas que dicen "para `.ts`, lanza este binario" | `/plugin install` |

Si instalas solo el plugin, verás `Executable not found in $PATH` en la pestaña **Errors** de `/plugin`. El plugin es el cable, no el aparato.

## Encenderlo (TypeScript, 3 pasos)

```bash
# 1. El motor (lo instalas tú, prerequisito)
npm install -g typescript-language-server typescript

# 2. El adaptador (plugin oficial de Anthropic)
/plugin install typescript-lsp@claude-plugins-official

# 3. Activar en la sesión actual
/reload-plugins
```

A partir de ahí, abre cualquier `.ts/.tsx/.js/.jsx` y Claude navega con precisión de compilador y ve los errores de tipo al instante. Pulsa **Ctrl+O** cuando aparezca el indicador "diagnostics found" para verlos inline.

## Lenguajes con plugin oficial

Cada uno necesita su binario instalado aparte:

| Lenguaje | Plugin | Binario |
|---|---|---|
| TypeScript | `typescript-lsp` | `typescript-language-server` |
| Python | `pyright-lsp` | `pyright-langserver` |
| Rust | `rust-analyzer-lsp` | `rust-analyzer` |
| Go | `gopls-lsp` | `gopls` |
| C/C++ | `clangd-lsp` | `clangd` |
| C# | `csharp-lsp` | `csharp-ls` |
| Java | `jdtls-lsp` | `jdtls` |
| PHP | `php-lsp` | `intelephense` |
| Lua, Kotlin, Swift | `lua-lsp`, `kotlin-lsp`, `swift-lsp` | (ver docs) |

## El matiz "semi-automático"

Si Claude Code detecta que **ya tienes el binario en el PATH** al abrir un proyecto, te *ofrece* instalar el plugin correspondiente. No se instala solo en silencio — tú apruebas. Pero el binario sigue siendo prerequisito tuyo: Claude Code nunca lo instala por ti.

Aviso honesto: los language servers consumen memoria (`rust-analyzer` y `pyright` notablemente en monorepos grandes). Si te da problemas, `/plugin disable <plugin>` y Claude vuelve a sus herramientas de búsqueda. El ahorro es de tokens y precisión, no de RAM.

Combina esto con [`/run-skill-generator`](/es/tips/claude-code-run-verify-ejecutar-app) para cerrar el bucle: navegación semántica + ejecución real de la app.

> Documentación oficial: [Code intelligence — Claude Code Docs](https://code.claude.com/docs/en/discover-plugins#code-intelligence) · Catálogo: [claude.com/plugins](https://claude.com/plugins)
