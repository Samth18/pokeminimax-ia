import os

# Carpetas a crear en la raíz del repositorio
folders = [
    "game",
    "ui",
    "docs"
]

# Archivos base con contenido inicial (puedes personalizarlos luego)
files = {
    "main.py": "",
    "game/__init__.py": "",
    "game/battle.py": "",
    "game/minimax.py": "",
    "game/player.py": "",
    "game/pokemon.py": "",
    "game/type_chart.py": "",
    "ui/__init__.py": "",
    "ui/console_ui.py": "",
    "docs/documentacion.md": "# Documentación del Proyecto\n\nAquí se explican decisiones técnicas, estructura del código y ejemplos de uso.",
    "README.md": "# Pokeminmax\n\nSimulador de combate Pokémon con IA usando Minimax con poda alfa-beta.",
    ".gitignore": "__pycache__/\n*.pyc\n.env"
}

# Crear carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Crear archivos
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Estructura del proyecto creada correctamente (incluye carpeta docs/).")

