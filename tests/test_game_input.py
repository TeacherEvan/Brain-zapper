"""Input & reset tests for Enhanced_Wild_Worm_Visual_Demo (OBJ-001..OBJ-004).

Headless-safe: mirrors the importlib pattern used by the existing suites.
Exercises handle_events(), create_background_stars(), and reset_game()
without modifying the source file.
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
    spec = importlib.util.spec_from_file_location("game_under_test_input", GAME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_keydown(key):
    import pygame
    return pygame.event.Event(pygame.KEYDOWN, {"key": key})


def _fake_quit():
    import pygame
    return pygame.event.Event(pygame.QUIT)


# --- OBJ-001 -- keyboard movement changes snake_direction -------------------

@pytest.mark.parametrize("key,expected", [
    ("up", (0, -1)),
    ("down", (0, 1)),
    ("left", (-1, 0)),
    ("right", (1, 0)),
])
def test_arrow_key_movement_changes_direction(key, expected):
    game = _load_game_module()
    import pygame
    key_const = getattr(pygame, "K_" + key.upper())
    original = game.snake_direction
    try:
        game.pygame.event.get = lambda: [_fake_keydown(key_const)]
        game.handle_events()
        assert game.snake_direction == expected
    finally:
        game.snake_direction = original


def test_escape_key_returns_false():
    game = _load_game_module()
    import pygame
    original = game.pygame.event.get
    try:
        game.pygame.event.get = lambda: [_fake_keydown(pygame.K_ESCAPE)]
        result = game.handle_events()
        assert result is False
    finally:
        game.pygame.event.get = original


def test_quit_event_returns_false():
    game = _load_game_module()
    original = game.pygame.event.get
    try:
        game.pygame.event.get = lambda: [_fake_quit()]
        result = game.handle_events()
        assert result is False
    finally:
        game.pygame.event.get = original


# --- OBJ-002 -- handle_events does not raise NameError on running -----------

def test_handle_events_does_not_reference_running():
    """`global running` was declared but never assigned in handle_events;
    calling it outside main() must not raise NameError."""
    game = _load_game_module()
    import pygame
    original = game.pygame.event.get
    try:
        game.pygame.event.get = lambda: []  # no events
        # Must not raise NameError: name 'running' is not defined
        result = game.handle_events()
        assert result is True
    finally:
        game.pygame.event.get = original


# --- OBJ-003 -- create_background_stars is idempotent at 100 ---------------

def test_background_stars_idempotent_at_100():
    game = _load_game_module()
    try:
        game.create_background_stars()
        assert len(game.background_stars) == 100
        game.create_background_stars()
        assert len(game.background_stars) == 100
        game.create_background_stars()
        assert len(game.background_stars) == 100
    finally:
        game.background_stars.clear()


# --- OBJ-004 -- reset_game restores snake_request ---------------------------

def test_reset_game_restores_snake_request():
    game = _load_game_module()
    try:
        game.snake_request = "StaleRequest"
        game.reset_game()
        pool = set(game.SHAPE_NAMES + game.FRUITS + game.VEGETABLES)
        assert game.snake_request in pool
        assert game.food is not None
    finally:
        # restore via another reset to leave known state
        game.reset_game()
