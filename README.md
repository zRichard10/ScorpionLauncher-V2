# 🦂 Scorpion Launcher

Premium Minecraft Java Launcher con interfaz moderna y oscura.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-Personal-orange)

## Características

- 🎮 **Lanzador de Minecraft Java** con soporte para todas las versiones (1.7.10 - última)
- 🎨 **Interfaz premium** con tema oscuro y acentos ámbar/dorado
- 📦 **Gestión de versiones** - instala cualquier versión con barra de progreso
- 🔄 **Auto-actualización** - detecta nuevas versiones de Minecraft automáticamente
- 👥 **Perfiles de usuario** - guarda y cambia entre usuarios
- ⚙️ **Configuración** - RAM, directorio de Minecraft, ruta de Java
- 🚀 **Sin consola** - se ejecuta limpio, sin ventana CMD

## Instalación rápida

### Requisitos previos
- **Python 3.8+** instalado ([descargar](https://python.org/downloads/))
  - ⚠️ Marca **"Add Python to PATH"** durante la instalación

### Pasos

1. **Clona o descarga** el repositorio
2. **Ejecuta `setup.bat`** (doble clic)
   - Instala las dependencias automáticamente
   - Crea el acceso directo en el escritorio
3. **Listo!** Abre desde el acceso directo en el escritorio

### Instalación manual

```bash
pip install customtkinter minecraft-launcher-lib Pillow
python main.py
```

## Estructura

```
ScorpionLauncher/
├── main.py              # Interfaz principal
├── config.py            # Configuración y colores
├── mc_manager.py        # Lógica de Minecraft
├── create_shortcut.py   # Genera acceso directo
├── ScorpionLauncher.vbs # Lanzador silencioso (sin CMD)
├── setup.bat            # Instalador automático
├── requirements.txt     # Dependencias
└── assets/
    ├── banner.png       # Banner del launcher
    ├── icon.png         # Ícono PNG
    └── icon.ico         # Ícono Windows
```

## Uso

1. Abre el launcher (acceso directo o `ScorpionLauncher.vbs`)
2. Ve a **Versiones** → selecciona una versión → **Descargar**
3. En **Inicio**, elige versión y usuario → **JUGAR**
4. Configura RAM y preferencias en **Ajustes**
