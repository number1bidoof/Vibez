
# 🚗 Mario Kart-Style Racing Game Deployment Guide

This document provides step-by-step instructions for setting up, running, and deploying the multiplayer Mario Kart-style racing game built with Pygame.

---

## 📦 Requirements

Before running the game, ensure you have the following:

### ✅ Software Dependencies

- **Python 3.8+**
- **Pygame library**

### 📁 Assets Required

Place the following character images in the same directory as the game script:

- `mario.jpg`
- `luigi.png`
- `peach.png`
- `bowser.jpg`
- `toad.jpg`

> 🔔 All images should be sized or will be scaled to fit a standard in-game resolution.

---

## 🧰 Installation

### 1. Install Python

Download and install Python from the [official site](https://www.python.org/downloads/).

To confirm Python is installed:

```bash
python --version
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install Pygame

```bash
pip install pygame
```

---

## 🚀 Running the Game

1. Navigate to the project directory:

```bash
cd path/to/game-directory
```

2. Run the game script:

```bash
python game.py
```

> 💡 Replace `game.py` with the actual name of your script file if different.

---

## 🎮 Gameplay Instructions

### Player Controls

#### Player 1 (WASD):
- `W` - Move Forward
- `S` - Move Backward
- `A` - Turn Left
- `D` - Turn Right

#### Player 2 (Arrow Keys):
- `↑` - Move Forward
- `↓` - Move Backward
- `←` - Turn Left
- `→` - Turn Right

### Objective
- Complete **3 laps** to win.
- Stay inside the **Rainbow Road track boundaries** to avoid losing progress.

---

## 🛠️ Customization Options

Each player can customize:
- Their **character**: Choose from Mario, Luigi, Peach, Bowser, and Toad.
- Their **car color**: Red, Green, or Blue.

Customization is handled at the start of the game in an intuitive menu screen.

---

## 🧪 Testing Tips

- Ensure all character images load successfully. If not, verify the filenames and formats.
- Run the game with different screen sizes if needed and adjust `WIDTH` and `HEIGHT` constants.
- Check boundary collision by attempting to move outside the track.

---

## 📤 Deployment Options

### Local Machine

Best for personal or classroom use. Just clone the repo and run the game using Python locally.

### Packaging with PyInstaller (Optional)

To create an executable for easier sharing:

```bash
pip install pyinstaller
pyinstaller --onefile game.py
```

This creates a standalone `dist/game.exe` (on Windows) or binary for other platforms.

---

## 🔧 Known Issues

- AI character movement is basic; future updates can use pathfinding.
- Ensure all assets are correctly named and present to avoid crashes.

---

## 📬 Support

If you encounter issues:
- Verify all dependencies are installed.
- Check console for Python or image loading errors.
- Ensure Pygame is installed and compatible with your Python version.

Happy racing! 🏁
