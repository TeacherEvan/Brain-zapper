# Brain Zapper - Enhanced Wild Worm Game 🧠⚡🐍

A spectacular visual and audio-enhanced Wild Worm game designed to stimulate the mind and provide engaging mental exercise.

## 🎯 Purpose
*5 minutes a day keeps the mind fog away.*

This game promotes:
- Mental clarity and focus
- Quick reaction times  
- Visual-spatial processing
- Mindful gaming experiences

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- Required packages:
```bash
pip install pygame pillow  # or, for pinned versions:
pip install -r requirements.txt
```

### Run the Game
```bash
python Enhanced_Wild_Worm_Visual_Demo.py
```

## ✅ Tests

The repo ships with a `pytest` suite (44 tests) covering the data tables,
RGB palettes, gradient themes, particle + star factories, audio gates,
and `reset_game`. CI runs it on every push via
`.github/workflows/python-tests.yml`.

Local run (headless, no display required):

```bash
pip install -r requirements.txt pytest
SDL_VIDEODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 pytest -q
```

`SDL_VIDEODRIVER=dummy` lets pytest import the pygame module without
opening a window, and `PYGAME_HIDE_SUPPORT_PROMPT=1` suppresses the
pygame community banner. Both env vars are already set by the CI
workflow; they are documented here for local + container runs.

Quick syntax-only check:

```bash
python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py
```

## 🎮 Features

### 🌈 Enhanced Visuals
- **Gradient backgrounds** with 6 stunning themes
- **Neon particle effects** with sparkle animations
- **Rainbow snake mode** with wobble animations
- **Twinkling starfield** background
- **60 FPS** smooth animations

### 🔊 Audio System
- **Dynamic sound effects** for all interactions
- **Procedurally generated tones** for game events
- **Toggle audio** on/off (Press S)
- **Graceful fallback** for systems without audio

### 🎯 Controls
- **Click**: Interact with game elements
- **SPACE**: Toggle Project Approach mode (rainbow effect)
- **G**: Cycle through gradient backgrounds
- **S**: Toggle sound on/off
- **ESC**: Exit game

## 📁 File Structure
```
Enhanced_Wild_Worm_Visual_Demo.py    # Main game file
README.md                           # This file
README_Enhanced_Wild_Worm.md        # Detailed feature documentation
Wild_Worm_Game_Enhanced_Visuals.md  # Visual effects documentation
```

## 🧠 Brain Training Benefits
- **Empty your mind** through focused gameplay
- **Meditation** in motion with smooth visuals
- **Cognitive stimulation** through rapid decision making
- **Stress relief** via immersive audiovisual experience

## 🎨 Visual Themes
1. **Cosmic** - Deep space purples and blues
2. **Sunset** - Warm oranges and yellows  
3. **Ocean** - Cool blues and teals
4. **Forest** - Natural greens
5. **Fire** - Intense reds and oranges
6. **Electric** - Bright cyans and blues

## 🔧 Technical Requirements
- **Platform**: Windows, macOS, Linux
- **Python**: 3.6 or higher
- **Memory**: Minimal requirements
- **Graphics**: Any system with basic graphics support

## 🎵 Audio Features
- **Click sounds** for UI feedback
- **Particle sounds** for visual effects
- **Life lost alerts** for game events
- **Game over sequences** with tonal progressions
- **Silent mode** for audio-free environments

Enjoy the enhanced Brain Zapper experience! 🎮✨🧠
