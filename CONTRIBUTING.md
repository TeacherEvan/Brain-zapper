# Contributing to Brain Zapper 🐍✨

Thanks for your interest in the Enhanced Wild Worm Game! This project is a
small single-file pygame demo plus a pytest suite. This document explains
how to set up a development environment, run the tests, and add new ones.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local environment setup](#local-environment-setup)
3. [Running the game](#running-the-game)
4. [Running the tests](#running-the-tests)
5. [Adding a new test](#adding-a-new-test)
6. [Code style](#code-style)
7. [Submitting changes](#submitting-changes)

---

## Prerequisites

- **Python 3.11+** recommended (CI runs on Python 3.11).
- **pygame 2.6+** (the runtime library).
- **Pillow 10+** (used by some optional rendering paths).
- **pytest 7+** for the test suite.
- On headless servers (CI, no display), pygame requires
  `SDL_VIDEODRIVER=dummy`. The test suite sets this automatically.
- Git for version control.

## Local environment setup

Pinned versions live in `requirements.txt`:

```text
pygame>=2.6,<3
pillow>=10,<13
```

### Option A: system Python (Debian / Ubuntu)

```bash
sudo -S -p '' apt-get install python3-pygame python3-pil python3-pytest
```

…or, when PEP-668 allows it:

```bash
pip install -r requirements.txt pytest
```

### Option B: a venv (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
python -m pytest -q
```

### Local env quirk (read this if `pytest` fails)

If your shell's `pytest` resolves to a system-installed pytest whose shebang
points to a Python that does **not** have pygame (a common case on Ubuntu,
where `/usr/bin/python3` ships without pygame and is PEP-668 locked), the
test suite will fail with `ModuleNotFoundError: No module named 'pygame'`.
Two fixes, in order of preference:

1. Run tests via the venv Python: `python -m pytest -q` — this resolves
   `pytest` inside the venv, which has pygame installed.
2. Install pygame in the system Python via your package manager:
   `sudo apt-get install python3-pygame`. Avoid `pip install --break-system-packages`
   unless you fully understand the risk to system Python.

CI on GitHub Actions is unaffected — it installs deps from scratch in a fresh
`ubuntu-latest` runner via `pip install -r requirements.txt`.

## Running the game

```bash
python Enhanced_Wild_Worm_Visual_Demo.py
```

Controls:

- **Click** — interact with game elements.
- **SPACE** — toggle Project Approach (rainbow) mode.
- **G** — cycle gradient background.
- **S** — toggle sound.
- **ESC** — quit.

## Running the tests

```bash
# from the repo root, with a Python that has pygame:
python -m pytest -q
```

Expected result: `57 passed in ~0.3s` on a modern machine.

### Headless / CI

```bash
SDL_VIDEODRIVER=dummy PYGAME_HIDE_SUPPORT_PROMPT=1 python -m pytest -q
```

`SDL_VIDEODRIVER=dummy` is the documented pygame recipe for running on a
machine with no display. The test files set it via
`os.environ.setdefault("SDL_VIDEODRIVER", "dummy")`, but exporting it
explicitly in CI is fine and matches the workflow at
`.github/workflows/python-tests.yml`.

### Running a subset

```bash
# by keyword (substring match against test name)
python -m pytest -q -k levels
python -m pytest -q -k update_game

# one file at a time
python -m pytest -q tests/test_game_logic_ext.py
```

## Adding a new test

The repo keeps tests **pure-logic** wherever possible — the source file
initialises pygame.display at import time, so any test that touches a
display surface needs `SDL_VIDEODRIVER=dummy`. The existing tests work
around this by importing the game module via `importlib.util`.

### Template

```python
# tests/test_my_feature.py
import importlib.util
import os
from pathlib import Path

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_PATH = REPO_ROOT / "Enhanced_Wild_Worm_Visual_Demo.py"


def _load_game_module():
    spec = importlib.util.spec_from_file_location(
        "game_under_test", GAME_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_my_feature():
    game = _load_game_module()
    # …assert on pure-logic globals or pure functions…
```

### Rules

- Tests **must not modify `Enhanced_Wild_Worm_Visual_Demo.py`** — exercise
  it as-is. If you find a bug, fix it in a separate change.
- Tests **must be deterministic** — use fixed inputs, or seed `random.seed()`
  if you must rely on randomness.
- For functions that mutate module globals (`update_particles`,
  `toggle_sound`, `update_game`), always `save → mutate → restore` (use
  try/finally) so subsequent tests start from a known state.
- For functions that call `play_*_sound` or `pygame.mixer` methods,
  stub the side-effect callback (`game.play_life_lost_sound = lambda: None`)
  before invoking the function.
- Use `pytest.approx` for any floating-point comparison.

## Code style

- **Black** formatting (88 columns). Not enforced in CI yet — keep PR diffs
  consistent with surrounding code.
- **Type hints** are welcome but not required. The source file currently has
  none; matching the surrounding style is fine.
- One-line module docstring at the top of every new file.
- Imports: stdlib first, third-party second, local last (PEP 8).

## Submitting changes

1. Fork or branch.
2. Make your change.
3. Run the full suite — `python -m pytest -q` must stay green.
4. Commit with a conventional message (`feat: …`, `test: …`, `fix: …`).
5. Open a PR against `main`. CI will run on Python 3.11 headless.

---

Questions? Open an issue on GitHub.
