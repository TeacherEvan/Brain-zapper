"""Regression tests for the K_s sound-toggle dead-code fix (OBJ-01..03).

Before the fix, `K_s` was bound to BOTH the DOWN movement branch and the
sound-toggle branch inside an `if/elif` chain, so the movement branch always
won and pressing S moved the snake down while never toggling sound. These
tests assert the post-fix behaviour and fail on the pre-fix source.
"""
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
        "game_under_test_sound_toggle", GAME_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_keydown(key):
    import pygame
    return pygame.event.Event(pygame.KEYDOWN, {"key": key})


def test_s_key_toggles_sound_not_direction():
    """Pressing S must toggle SOUND_ENABLED and must NOT change snake_direction."""
    game = _load_game_module()
    import pygame
    original_dir = game.snake_direction
    original_sound = game.SOUND_ENABLED
    try:
        game.pygame.event.get = lambda: [_fake_keydown(pygame.K_s)]
        game.handle_events()
        assert game.SOUND_ENABLED is (not original_sound), \
            "S should toggle SOUND_ENABLED"
        assert game.snake_direction == original_dir, \
            "S should not change snake_direction"
    finally:
        game.snake_direction = original_dir
        game.SOUND_ENABLED = original_sound


def test_s_key_no_longer_moves_down():
    """S must not be treated as a DOWN movement key."""
    game = _load_game_module()
    import pygame
    original_dir = game.snake_direction
    try:
        game.pygame.event.get = lambda: [_fake_keydown(pygame.K_s)]
        game.handle_events()
        assert game.snake_direction != (0, 1), \
            "S must not move the snake down"
    finally:
        game.snake_direction = original_dir


def test_down_key_still_moves_down():
    """The DOWN arrow key must still move the snake down after the fix."""
    game = _load_game_module()
    import pygame
    original_dir = game.snake_direction
    try:
        game.pygame.event.get = lambda: [_fake_keydown(pygame.K_DOWN)]
        game.handle_events()
        assert game.snake_direction == (0, 1)
    finally:
        game.snake_direction = original_dir
