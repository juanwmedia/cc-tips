---
date: 2026-05-08
type: tip
title_es: "Crea y distribuye temas personalizados con Claude Code"
title_en: "Create and distribute custom themes with Claude Code"
---

> **TL;DR** Ejecuta `/theme` y elige **New custom theme...** al final del listado. Eliges un base preset (`dark` o `light`) y sobrescribes solo los tokens que te importan. Vive en `~/.claude/themes/<slug>.json`. Hot-reload: editas el JSON y la sesión se actualiza sin reiniciar. Y si lo empaquetas en un [plugin](/es/tips/claude-code-marketplace-plugins-distribucion), todo tu equipo lo hereda con un solo install.

Hasta abril, Claude Code traía cuatro o cinco themes y se acabó. Si trabajas con una paleta concreta — la corporate de tu empresa, Dracula, Solarized, una mezcla tuya — tocaba aceptar la del repo. Anthropic empaquetó la solución en `v2.1.118` (Week 17, abril 2026): **custom themes**. Y la pieza menos comentada es la última — los themes son distribuibles como plugin.

## Cómo funciona por dentro

Cada custom theme es un JSON en `~/.claude/themes/<slug>.json` con tres campos:

| Campo | Detalle |
|---|---|
| `name` | El nombre que aparece en el picker de `/theme` |
| `base` | El preset del que parte: `dark`, `light`, o cualquier built-in |
| `overrides` | Diccionario de tokens semánticos a colores |

Solo sobrescribes lo que te importa. El resto hereda del base preset. Cuando lo seleccionas, Claude guarda `custom:<slug>` como tu preferencia de theme. Y vigila la carpeta — si editas el JSON con tu editor de código, los cambios entran en la sesión activa sin reiniciar.

Los color values aceptan cualquiera de estos formatos:

```
#bd93f9       (#rrggbb)
#bdf          (#rgb)
rgb(189, 147, 249)
ansi256(141)  (256-color palette)
ansi:cyan     (16 ANSI estándar)
```

## Resultado

```json
// ~/.claude/themes/dracula.json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error":  "#ff5555",
    "success": "#50fa7b"
  }
}
```

Lo guardas. Ejecutas `/theme`, ves "Dracula" en el listado, lo seleccionas. Cambias `#bd93f9` por `#ff79c6` en el editor, guardas. Vuelves al terminal: ya está aplicado. Sin reiniciar.

## Cómo usarlo

### **1. Picker interactivo (sin tocar JSON)**

```
> /theme
[lista de built-in themes]
[lista de custom themes que ya tienes]
[lista de themes contribuidos por plugins instalados]
> New custom theme...
```

Le pones nombre, eliges un base preset y sobrescribes los tokens uno a uno. Claude crea el JSON por ti en `~/.claude/themes/`.

### **2. Editar el JSON a mano**

Más rápido si ya sabes los hex que quieres. Crea el archivo, mete los `overrides` que necesites, vuelve al terminal y selecciónalo en `/theme`.

```bash
mkdir -p ~/.claude/themes
cat > ~/.claude/themes/corporate.json <<'EOF'
{
  "name": "Corporate",
  "base": "light",
  "overrides": {
    "claude": "#1a73e8",
    "syntax.string": "#0f9d58",
    "syntax.keyword": "#d93025"
  }
}
EOF
```

### **3. Distribuir el theme a tu equipo como plugin**

Aquí está el filo. En vez de pedirle a 12 personas que se copien tu JSON, lo metes en un [plugin de Claude Code](/es/tips/claude-code-marketplace-plugins-distribucion):

```
mi-plugin/
├── plugin.json
└── themes/
    └── corporate.json
```

`plugin install` hace el resto: el theme aparece en `/theme` de cada miembro del equipo automáticamente. Cuando bumpas la versión del plugin (cambias colores corporativos, añades una variante dark), un `/plugin marketplace update` lo propaga.

## Referencia

| Aspecto | Detalle |
|---|---|
| Versión mínima | Claude Code `v2.1.118` |
| Comando | `/theme` (alias del que ya conocías) |
| Path | `~/.claude/themes/<slug>.json` |
| Slug | El nombre del archivo sin `.json` |
| Hot-reload | Sí — edita el JSON y la sesión se actualiza |
| Color formats | `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, `ansi:<name>` |
| Distribución | Cualquier plugin puede shippear themes en su carpeta `themes/` |
| Persistencia | El theme seleccionado vive en `~/.claude/settings.json` como `custom:<slug>` |

> Documentación oficial: [Terminal config — Create a custom theme](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme)
