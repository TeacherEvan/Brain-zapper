# Brain-zapper: Enhanced Wild Worm Game 🧠⚡🐍

Enhanced Wild Worm Game is a Python-based visual brain training game featuring spectacular graphics effects, designed to provide mental stimulation and cognitive exercise through engaging gameplay.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Run the Game
- **Install Python dependencies**: `pip3 install pygame pillow` -- takes ~1-2 seconds. Dependencies are pygame 2.6+ and pillow 11.0+.
- **Run the game**: `python3 Enhanced_Wild_Worm_Visual_Demo.py`
- **Expected audio warnings**: ALSA audio warnings are NORMAL and expected in headless environments. Game automatically falls back to silent mode.
- **Game startup time**: ~2-3 seconds in normal environments, ~10 seconds with virtual display drivers. NEVER CANCEL - this is normal behavior.

### Environment Setup
- **Python requirement**: Python 3.6+ (tested on 3.12.3)
- **Platform support**: Windows, macOS, Linux
- **Display requirements**: Game requires display access. Use `export SDL_VIDEODRIVER=dummy` for headless testing.
- **Audio fallback**: Game gracefully handles missing audio hardware and displays "Audio Status: Not Available (Silent Mode)"

### No Build Process Required
- **Direct execution**: This is a single-file Python script - NO compilation or build steps needed
- **No dependencies file**: No requirements.txt, package.json, or similar - just install pygame and pillow directly
- **No test infrastructure**: No existing test files or framework - manual validation required

## Validation

### ALWAYS Validate Changes With These Steps
1. **Syntax check**: `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py` -- completes instantly
2. **Dependency check**: `python3 -c "import pygame, PIL; print('Dependencies OK')"` -- takes 1-2 seconds, ignore pygame welcome messages
3. **Game startup test**: `export SDL_VIDEODRIVER=dummy && timeout 5 python3 Enhanced_Wild_Worm_Visual_Demo.py 2>&1 | grep "Starting Enhanced Wild Worm Game"` -- NEVER CANCEL before 5 seconds
4. **Visual validation** (if display available): `timeout 10 xvfb-run -a -s "-screen 0 1024x768x24" python3 Enhanced_Wild_Worm_Visual_Demo.py` -- NEVER CANCEL, set timeout to 30+ seconds minimum

### Required User Scenario Testing
After making ANY changes to the game code, ALWAYS manually test these scenarios:
- **Game starts**: Verify welcome screen appears with all visual elements
- **Controls work**: Test keyboard controls (SPACE, G, S, ESC) and mouse clicks
- **Visual effects**: Confirm particle effects, gradient backgrounds, and animations function
- **Audio handling**: Verify graceful audio fallback in headless environments
- **Game loop**: Ensure game runs continuously without crashes for at least 30 seconds

### Audio Warnings Are Expected
```
ALSA lib confmisc.c:855:(parse_card) cannot find card '0'
ALSA lib conf.c:5204:(_snd_config_evaluate) function snd_func_card_inum returned error: No such file or directory
```
These warnings are NORMAL in headless/container environments. Game correctly falls back to silent mode.

## Common Tasks

### Repository Structure
```
/
├── .github/
│   └── copilot-instructions.md          # This file
├── .gitignore                           # Python cache exclusions
├── Enhanced_Wild_Worm_Visual_Demo.py    # Main game file (791 lines)
├── README.md                            # Main project documentation
├── README_Enhanced_Wild_Worm.md         # Detailed feature documentation
├── Wild_Worm_Game_(Enhanced).ipynb      # Jupyter notebook version
└── Wild_Worm_Game_Enhanced_Visuals.md   # Visual effects documentation
```

### Key Game Features (For Testing)
- **Gradient backgrounds**: 6 themes (cosmic, sunset, ocean, forest, fire, electric)
- **Particle effects**: Sparkle animations with neon colors
- **Rainbow snake mode**: Activated with SPACE key
- **Audio system**: Dynamic sound effects with graceful fallback
- **60 FPS animations**: Smooth visual transitions and effects

### Game Controls (For Manual Testing)
- **Click**: Interact with game elements
- **SPACE**: Toggle Project Approach mode (rainbow snake effect)
- **G**: Cycle through gradient backgrounds  
- **S**: Toggle sound effects on/off
- **ESC**: Exit game

### Expected Game Output
When game starts successfully, you should see:
```
pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
Audio not available in this environment - running in silent mode
🐍✨ Starting Enhanced Wild Worm Game ✨🐍
Features:
- Spectacular gradient backgrounds
- Enhanced particle effects with sparkles
[... feature list continues ...]

Controls:
- Click to interact
- SPACE: Toggle Project Approach mode
[... controls list continues ...]

Audio Status: Not Available (Silent Mode)
Enjoy the enhanced visuals and audio! 🎮✨🔊
```

### Complete Validation Workflow
For any code changes, run this complete validation sequence:
```bash
# 1. Syntax validation (instant)
python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py

# 2. Dependencies test (1-2 seconds) 
python3 -c "import pygame, PIL; print('Dependencies OK')" 2>&1 | grep "Dependencies OK"

# 3. Headless startup test (2-5 seconds) -- NEVER CANCEL
export SDL_VIDEODRIVER=dummy
timeout 5 python3 Enhanced_Wild_Worm_Visual_Demo.py 2>&1 | grep -E "(Starting Enhanced|Audio Status)"
# Expected output: "🐍✨ Starting Enhanced Wild Worm Game ✨🐍" and "Audio Status: Not Available"
# timeout command will terminate with exit code 143 - this is EXPECTED
```

## Installation Commands Reference

### Python and Dependencies
```bash
# Verify Python version (3.6+ required)
python3 --version

# Install game dependencies (takes ~1-2 seconds)
pip3 install pygame pillow

# Verify installation
python3 -c "import pygame, PIL; print(f'pygame {pygame.version.ver}, PIL {PIL.__version__}')"
```

### Running the Game
```bash
# Standard run (requires display)
python3 Enhanced_Wild_Worm_Visual_Demo.py

# Headless testing (dummy video driver)
export SDL_VIDEODRIVER=dummy
python3 Enhanced_Wild_Worm_Visual_Demo.py

# Visual testing with virtual display
xvfb-run -a -s "-screen 0 1024x768x24" python3 Enhanced_Wild_Worm_Visual_Demo.py
```

## Timing Expectations

- **Dependency installation**: 1-2 seconds for already cached packages, 30-60 seconds for fresh installation -- NEVER CANCEL pip commands
- **Game startup**: 2-3 seconds normal, up to 10 seconds with virtual display drivers -- NEVER CANCEL, set timeout to 15+ seconds minimum
- **Syntax validation**: Instant (<1 second)
- **Import testing**: 1-2 seconds (includes pygame initialization messages)
- **Full visual testing with xvfb**: 5-10 seconds startup -- NEVER CANCEL, set timeout to 30+ seconds

## Troubleshooting

### Common Issues
- **"No module named 'pygame'"**: Run `pip3 install pygame pillow`
- **ALSA audio warnings**: EXPECTED - game runs in silent mode, this is normal
- **"pygame.error: No available video device"**: Set `export SDL_VIDEODRIVER=dummy` for headless environments
- **Game appears to hang on startup**: Wait at least 10 seconds - initialization with virtual displays is slow but normal

### Development Workflow
1. Make minimal changes to `Enhanced_Wild_Worm_Visual_Demo.py`
2. Run syntax check: `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py`
3. Test game startup with dummy driver for quick validation
4. If possible, test with visual display for full validation
5. Manually test changed functionality through game controls

**Remember: This is a single-file game with no build system - changes take effect immediately upon running the Python file.**