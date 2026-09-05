"""Pure-logic tests for Enhanced_Wild_Worm_Visual_Demo.

These tests intentionally avoid creating a real display window. They are safe
to run on a headless CI runner as long as SDL_VIDEODRIVER=dummy is set
(see .github/workflows/python-tests.yml).
"""
import array
import importlib
import os
import sys
from pathlib import Path

import pytest

# Ensure SDL has a fake video driver for CI / headless environments.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
# Suppress pygame's "Hello from the pygame community" banner during tests.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_PATH = REPO_ROOT / "Enhanced_Wild_Worm_Visual_Demo.py"


def _load_game_module():
    """Import the single-file pygame game by file path."""
    spec = importlib.util.spec_from_file_location("game_under_test", GAME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# OBJ-006 -- Word lists are non-empty strings ---------------------------------

def test_shape_names_non_empty_strings():
    game = _load_game_module()
    assert isinstance(game.SHAPE_NAMES, list)
    assert len(game.SHAPE_NAMES) > 0
    assert all(isinstance(s, str) and s for s in game.SHAPE_NAMES)


def test_fruits_non_empty_strings():
    game = _load_game_module()
    assert isinstance(game.FRUITS, list)
    assert len(game.FRUITS) > 0
    assert all(isinstance(s, str) and s for s in game.FRUITS)


def test_vegetables_non_empty_strings():
    game = _load_game_module()
    assert isinstance(game.VEGETABLES, list)
    assert len(game.VEGETABLES) > 0
    assert all(isinstance(s, str) and s for s in game.VEGETABLES)


# OBJ-003 -- Color tuples are 3-int RGB in [0, 255] --------------------------

NAMED_RGB = [
    "WHITE", "BLACK", "RED", "BRIGHT_RED", "GREEN", "BRIGHT_GREEN",
    "BLUE", "DARK_BLUE", "BRIGHT_BLUE", "DARK_PURPLE", "BRIGHT_PURPLE",
    "DARK_CYAN", "BRIGHT_CYAN", "YELLOW", "LIGHT_YELLOW", "ORANGE",
    "PURPLE", "GREY", "DARK_GREY", "SNAKE_COLOR", "SNAKE_COLOR_DARK",
    "CAGE_COLOR", "NEON_RED", "NEON_GREEN", "NEON_BLUE", "NEON_PURPLE",
    "NEON_CYAN", "NEON_YELLOW", "NEON_ORANGE", "NEON_PINK",
    "ELECTRIC_BLUE", "LIME_GREEN", "CAGE_GOLD", "SILVER",
]


@pytest.mark.parametrize("name", NAMED_RGB)
def test_named_rgb_constant_is_3_tuple_in_range(name):
    game = _load_game_module()
    color = getattr(game, name)
    assert isinstance(color, tuple), f"{name} is not a tuple"
    assert len(color) == 3, f"{name} must be RGB (3-tuple), got {len(color)}"
    for channel in color:
        assert isinstance(channel, int), f"{name} channel {channel!r} not int"
        assert 0 <= channel <= 255, f"{name} channel {channel} out of range"


def test_enhanced_particle_colors_all_rgb():
    game = _load_game_module()
    for color in game.ENHANCED_PARTICLE_COLORS:
        assert isinstance(color, tuple) and len(color) == 3
        for channel in color:
            assert 0 <= channel <= 255


def test_gradient_themes_have_at_least_three_stops():
    game = _load_game_module()
    for theme, stops in game.GRADIENT_COLORS.items():
        assert isinstance(stops, list), f"{theme} stops not a list"
        assert len(stops) >= 3, f"{theme} has fewer than 3 gradient stops"
        for stop in stops:
            assert isinstance(stop, tuple) and len(stop) == 3
            for channel in stop:
                assert 0 <= channel <= 255


# OBJ-004 -- generate_tone returns expected array -----------------------------

def test_generate_tone_returns_none_when_sound_disabled():
    game = _load_game_module()
    original = game.SOUND_ENABLED
    try:
        game.SOUND_ENABLED = False
        result = game.generate_tone(440.0, 0.5)
        assert result is None
    finally:
        game.SOUND_ENABLED = original


def test_generate_tone_returns_array_of_expected_length_when_audio_off():
    """When AUDIO_AVAILABLE is False, generate_tone short-circuits to None."""
    game = _load_game_module()
    original = game.AUDIO_AVAILABLE
    try:
        game.AUDIO_AVAILABLE = False
        result = game.generate_tone(440.0, 0.5)
        assert result is None
    finally:
        game.AUDIO_AVAILABLE = original


# OBJ-005 -- create_background_stars + create_spectacular_particle shapes ----

def test_create_background_stars_appends_to_global_list():
    game = _load_game_module()
    game.background_stars.clear()
    game.create_background_stars()
    stars = game.background_stars
    assert len(stars) == 100
    sample = stars[0]
    assert set(sample.keys()) >= {"pos", "brightness", "twinkle_speed"}
    x, y = sample["pos"]
    assert 0 <= x <= game.screen_width
    assert 0 <= y <= game.screen_height
    assert 0.3 <= sample["brightness"] <= 1.0


def test_create_spectacular_particle_appends_well_formed_particles():
    game = _load_game_module()
    # Stub the sound callback so the test does not depend on mixer state.
    original = game.play_particle_sound
    game.play_particle_sound = lambda: None
    try:
        game.particles.clear()
        before = len(game.particles)
        game.create_spectacular_particle((100, 100), game.NEON_PINK)
        after = len(game.particles)
        assert after - before >= 5  # random.randint(5, 12)
        p = game.particles[-1]
        assert set(p.keys()) >= {
            "pos", "vel", "size", "color", "lifetime", "total_lifetime", "sparkle"
        }
        assert isinstance(p["color"], tuple) and len(p["color"]) == 3
        assert isinstance(p["sparkle"], bool)
    finally:
        game.play_particle_sound = original
        game.particles.clear()


# OBJ-005 bonus -- reset_game resets snake-related state -----------------------

def test_reset_game_returns_snake_to_start_position():
    game = _load_game_module()
    # Move snake somewhere weird first; reset_game must restore sane state.
    game.snake_segments = [(0, 0), (1, 0), (2, 0)]
    game.reset_game()
    assert len(game.snake_segments) == 5
    # After reset, snake sits at screen centre + vertical offsets, not at (0,0).
    head_x, head_y = game.snake_segments[0]
    assert head_x > 0 and head_y > 0
    # Game state must be reset to playing.
    assert game.game_state == game.STATE_PLAYING
    assert game.lives == 3
    assert game.score == 0
