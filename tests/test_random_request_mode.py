"""Pure-logic tests for Random Request Mode (OBJ-001..OBJ-008).

Loads Enhanced_Wild_Worm_Visual_Demo.py via importlib.util to avoid
touching pygame.display. The new mode toggles `RANDOM_REQUEST_MODE`,
and `pick_random_request()` reads from SHAPE_NAMES+FRUITS+VEGETABLES.
"""
import importlib.util
import os
import random
from pathlib import Path

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_PATH = REPO_ROOT / "Enhanced_Wild_Worm_Visual_Demo.py"


def _load_game_module():
    spec = importlib.util.spec_from_file_location(
        "game_random_request_mode", GAME_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# OBJ-001 -- RANDOM_REQUEST_MODE defaults to False -----------------------------

def test_random_mode_default_false():
    game = _load_game_module()
    original = game.RANDOM_REQUEST_MODE
    try:
        game.RANDOM_REQUEST_MODE = False  # force-set to test default contract
        assert isinstance(game.RANDOM_REQUEST_MODE, bool)
        assert game.RANDOM_REQUEST_MODE is False
        # The default value when the module is freshly loaded is False.
        # Reload to confirm the source-level default.
        spec = importlib.util.spec_from_file_location(
            "game_random_default", GAME_PATH
        )
        fresh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fresh)
        assert fresh.RANDOM_REQUEST_MODE is False
    finally:
        game.RANDOM_REQUEST_MODE = original


# OBJ-002 -- pick_random_request returns in-pool string -----------------------

def test_pick_random_request_in_pool():
    game = _load_game_module()
    pool = set(game.RANDOM_REQUEST_POOL)
    expected_pool = set(game.SHAPE_NAMES) | set(game.FRUITS) | set(game.VEGETABLES)
    assert pool == expected_pool
    for _ in range(50):
        v = game.pick_random_request()
        assert isinstance(v, str) and v, f"empty/non-str result: {v!r}"
        assert v in pool, f"{v!r} not in pool {pool}"


def test_pick_random_request_deterministic_with_seed():
    game = _load_game_module()
    rng1 = random.Random(0)
    rng2 = random.Random(0)
    a = game.pick_random_request(rng1)
    b = game.pick_random_request(rng2)
    assert a == b
    # Different seeds → potentially different first picks (just sanity check
    # that the rng arg is actually used, not ignored).
    seen = {game.pick_random_request(random.Random(s)) for s in range(10)}
    assert len(seen) >= 2, "rng arg appears to be ignored"


# OBJ-003 -- random_mode_label reflects the flag ------------------------------

def test_random_mode_label_strings():
    game = _load_game_module()
    original = game.RANDOM_REQUEST_MODE
    try:
        game.RANDOM_REQUEST_MODE = False
        assert game.random_mode_label() == "Random: OFF"
        game.RANDOM_REQUEST_MODE = True
        assert game.random_mode_label() == "Random: ON"
    finally:
        game.RANDOM_REQUEST_MODE = original


# OBJ-004/005 -- reset_game branches ------------------------------------------

def test_reset_game_randomizes_when_enabled():
    game = _load_game_module()
    original = game.RANDOM_REQUEST_MODE
    original_req = game.snake_request
    try:
        game.RANDOM_REQUEST_MODE = True
        random.seed(42)
        # Pre-set a known request value; reset should overwrite it.
        game.snake_request = "ZZZ_Never_Picked"
        game.reset_game()
        # The new request must be a string from the pool.
        assert game.snake_request in game.RANDOM_REQUEST_POOL
        # And it must be a different string from our pre-set value
        # (the seeded RNG will not pick "ZZZ_Never_Picked" since it's not in pool).
    finally:
        game.RANDOM_REQUEST_MODE = original
        game.snake_request = original_req


def test_reset_game_preserves_when_disabled():
    game = _load_game_module()
    original = game.RANDOM_REQUEST_MODE
    original_req = game.snake_request
    try:
        game.RANDOM_REQUEST_MODE = False
        sentinel = "PRESERVE_ME"
        game.snake_request = sentinel
        game.reset_game()
        assert game.snake_request == sentinel, (
            "reset_game must not touch snake_request when mode is off"
        )
    finally:
        game.RANDOM_REQUEST_MODE = original
        game.snake_request = original_req


# OBJ-006 -- update_game re-randomizes on timer expiry when mode is on --------

def test_update_game_randomizes_on_expiry():
    game = _load_game_module()
    original_state = game.game_state
    original_lives = game.lives
    original_timer = game.request_timer
    original_mode = game.RANDOM_REQUEST_MODE
    original_req = game.snake_request
    original_life_sound = game.play_life_lost_sound
    game.play_life_lost_sound = lambda: None
    try:
        game.RANDOM_REQUEST_MODE = True
        random.seed(7)
        game.game_state = game.STATE_PLAYING
        game.lives = 3
        game.request_timer = 0.1
        sentinel = "NOT_IN_POOL"
        game.snake_request = sentinel
        game.update_game(0.5)
        # Lives must drain (existing behaviour preserved).
        assert game.lives == 2
        # Still playing (3→2 doesn't end the game).
        assert game.game_state == game.STATE_PLAYING
        # And snake_request MUST be re-picked from the pool.
        assert game.snake_request != sentinel
        assert game.snake_request in game.RANDOM_REQUEST_POOL
    finally:
        game.play_life_lost_sound = original_life_sound
        game.RANDOM_REQUEST_MODE = original_mode
        game.game_state = original_state
        game.lives = original_lives
        game.request_timer = original_timer
        game.snake_request = original_req


def test_update_game_does_not_change_request_when_mode_off():
    """Regression guard: timer-expiry must NOT touch snake_request when off."""
    game = _load_game_module()
    original_state = game.game_state
    original_lives = game.lives
    original_timer = game.request_timer
    original_mode = game.RANDOM_REQUEST_MODE
    original_req = game.snake_request
    original_life_sound = game.play_life_lost_sound
    game.play_life_lost_sound = lambda: None
    try:
        game.RANDOM_REQUEST_MODE = False
        game.game_state = game.STATE_PLAYING
        game.lives = 3
        game.request_timer = 0.1
        sentinel = "Circle"
        game.snake_request = sentinel
        game.update_game(0.5)
        assert game.lives == 2
        assert game.snake_request == sentinel
    finally:
        game.play_life_lost_sound = original_life_sound
        game.RANDOM_REQUEST_MODE = original_mode
        game.game_state = original_state
        game.lives = original_lives
        game.request_timer = original_timer
        game.snake_request = original_req
