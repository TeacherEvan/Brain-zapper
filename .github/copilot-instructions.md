# Brain-zapper - Enhanced Wild Worm Game

Brain-zapper is a Python-based pygame visual game featuring spectacular visual effects, neon colors, and enhanced animations. The game is a snake-like experience with modern visual enhancements including gradient backgrounds, particle effects, and interactive elements.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Initial Setup and Dependencies
- Install Python 3.6+ (tested with Python 3.12.3)
- Install required Python packages:
  ```bash
  pip install pygame pillow
  ```
  - **TIMING**: Installation takes 15-30 seconds with good network connection. NEVER CANCEL - network timeouts may occur, be patient.
  - **DEPENDENCIES**: pygame 2.0+ and Pillow 8.0+ are required
  - **NETWORK ISSUES**: If `pip install` times out, retry the command - this is normal in restricted network environments

### Building and Testing
- **NO BUILD STEP REQUIRED**: This is pure Python - no compilation needed
- Validate Python syntax:
  ```bash
  python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py
  ```
  - **TIMING**: <1 second for syntax validation
- Test imports and basic functionality:
  ```bash
  python3 -c "import os; os.environ['SDL_VIDEODRIVER'] = 'dummy'; import Enhanced_Wild_Worm_Visual_Demo; print('Import successful')"
  ```
  - **TIMING**: <2 seconds for import test

### Running the Game
- **Standard run** (requires display):
  ```bash
  python3 Enhanced_Wild_Worm_Visual_Demo.py
  ```
- **Headless testing** (for validation without display):
  ```bash
  SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 Enhanced_Wild_Worm_Visual_Demo.py
  ```
  - **TIMING**: Game starts in <2 seconds
  - **NEVER CANCEL**: Let the game window appear - it may take a moment to initialize pygame

## Validation

### Manual Testing Requirements
**CRITICAL**: After making any changes, ALWAYS run through these complete user scenarios:

1. **Basic Game Launch**:
   - Run `python3 Enhanced_Wild_Worm_Visual_Demo.py`
   - Verify game window opens with welcome screen
   - Verify background gradient and visual effects display correctly

2. **Core Game Interactions**:
   - Click to start the game from welcome screen
   - Use mouse to interact with game elements
   - Verify particle effects trigger on mouse clicks
   - Test ESC key to exit game

3. **Special Features**:
   - Press SPACE key to toggle Project Approach mode (rainbow snake effect)
   - Press G key to cycle through gradient backgrounds (6 different themes)
   - Verify visual effects change accordingly

4. **Game Controls Validation**:
   - Mouse clicks: Should create particle effects
   - SPACE key: Toggles rainbow snake mode with visual feedback
   - G key: Cycles background gradients (sunset, ocean, forest, cosmic, fire, electric)
   - ESC key: Exits the game cleanly

### Automated Validation
- **Python Syntax**: `python3 -m py_compile *.py`
- **Import Test**: `python3 -c "import Enhanced_Wild_Worm_Visual_Demo"`
- **NO UNIT TESTS**: This repository does not have automated tests - rely on manual validation

### Code Quality
- **NO LINTERS CONFIGURED**: Repository has no pylint, flake8, or other linting tools
- **SYNTAX ONLY**: Use Python's built-in syntax checking for validation
- Run syntax validation before making changes: `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py`

## Repository Structure

### Key Files and Locations
```
project-root/
├── Enhanced_Wild_Worm_Visual_Demo.py          # MAIN GAME FILE - Core executable
├── Wild_Worm_Game_(Enhanced).ipynb            # Jupyter notebook version
├── README.md                                  # Basic project description  
├── README_Enhanced_Wild_Worm.md               # Detailed game documentation
├── Wild_Worm_Game_Enhanced_Visuals.md         # Visual effects documentation
└── .github/
    └── copilot-instructions.md                # This file
```

### Most Important Files
1. **Enhanced_Wild_Worm_Visual_Demo.py**: The complete game implementation
   - All game logic, visual effects, and user interaction
   - ~700+ lines of Python/pygame code
   - Contains particle system, gradient backgrounds, and game mechanics

2. **README_Enhanced_Wild_Worm.md**: Comprehensive game documentation
   - Installation instructions
   - Feature descriptions  
   - Control schemes and gameplay modes

3. **Wild_Worm_Game_Enhanced_Visuals.md**: Technical visual effects documentation
   - Implementation details for visual enhancements
   - Color palettes and effect systems

## Common Development Tasks

### Making Code Changes
1. **ALWAYS** validate syntax first: `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py`
2. **ALWAYS** test imports after changes: `python3 -c "import Enhanced_Wild_Worm_Visual_Demo"`
3. **ALWAYS** run manual validation scenarios (see Validation section above)
4. **NEVER SKIP** the complete user scenario testing - visual bugs are not caught by syntax checking

### Troubleshooting Common Issues
- **ImportError for pygame/PIL**: Run `pip install pygame pillow`
- **SDL Video/Audio warnings**: Normal in headless environments, can be ignored
- **ALSA audio warnings**: Normal in containerized environments, can be ignored  
- **Game window not appearing**: Check display environment, try headless mode for testing

### Key Game Components
- **Particle System**: Lines 300-400 in main file - creates visual effects
- **Game States**: Welcome screen, playing, game over - controlled by state machine
- **Visual Effects**: Gradient backgrounds, neon colors, animations throughout
- **Input Handling**: Mouse and keyboard event processing in handle_events() function

## Performance and Timing Expectations

### Timing Guidelines
- **Dependency Installation**: 15-30 seconds (NEVER CANCEL - network dependent)
- **Game Startup**: <2 seconds
- **Syntax Validation**: <1 second  
- **Import Testing**: <2 seconds
- **Manual Testing**: 2-3 minutes for complete scenario validation

### NO BUILD TIMEOUTS NEEDED
- This is a pure Python project with no compilation step
- All "build" operations complete in seconds
- The longest operation is dependency installation via pip

## Development Environment Notes

### System Requirements  
- **Python**: 3.6+ (tested with 3.12.3)
- **Display**: Required for full game functionality (can run headless for basic testing)
- **Audio**: Optional (game works without audio)
- **Network**: Required only for initial pip dependency installation

### Environment Variables for Testing
```bash
export SDL_VIDEODRIVER=dummy    # For headless testing
export SDL_AUDIODRIVER=dummy    # Suppress audio warnings
```

### No Complex Tooling
- **NO**: webpack, npm, make, cmake, docker, or other build tools
- **NO**: CI/CD pipelines or GitHub Actions configured
- **NO**: Database, server components, or external services
- **YES**: Simple Python execution with pygame for graphics

## Validation Checklist

Before completing any changes, verify:
- [ ] Python syntax validation passes
- [ ] Game imports successfully  
- [ ] Game launches and displays welcome screen
- [ ] Mouse clicks create particle effects
- [ ] SPACE key toggles rainbow mode
- [ ] G key cycles background gradients
- [ ] ESC key exits cleanly
- [ ] Visual effects display properly
- [ ] No Python exceptions in console

## Common Error Messages and Solutions

### ImportError: No module named 'pygame'
```bash
pip install pygame pillow
```
This error means the required dependencies are not installed.

### ImportError: No module named 'PIL'
```bash
pip install pillow
```
PIL is provided by the Pillow package.

### SDL Video/Audio Driver Warnings
```
ALSA lib confmisc.c:855:(parse_card) cannot find card '0'
```
These warnings are normal in containerized or headless environments and can be safely ignored.

## Emergency Procedures

### If Game Won't Start
1. Check Python version: `python3 --version` (must be 3.6+)
2. Reinstall dependencies: `pip install --force-reinstall pygame pillow`
3. Test import: `python3 -c "import pygame, PIL; print('Dependencies OK')"`
4. Try headless mode: `SDL_VIDEODRIVER=dummy python3 Enhanced_Wild_Worm_Visual_Demo.py`

### If Syntax Errors Occur  
1. Run: `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py`
2. Check for global variable declarations before usage
3. Verify proper indentation (Python is whitespace sensitive)
4. Look for missing colons, parentheses, or quotes

### If Game Runs But No Visual Effects
1. Check if running in headless mode (SDL_VIDEODRIVER=dummy)
2. Verify display environment is available
3. Test with: `python3 Enhanced_Wild_Worm_Visual_Demo.py` (no environment variables)

**Remember**: This is a visual game - automated testing cannot replace manual validation of the user experience and visual effects.