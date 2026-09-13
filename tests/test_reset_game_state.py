"""Regression test: reset_game() must restore level-1 defaults.

OBJ-025. After advance_level() mutates request_time_limit and snake_speed,
calling reset_game() must re-read LEVELS[1] so the next game starts with the
correct timer and speed instead of the last level's values.
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
    spec = importlib.util.spec_from_file_location("game_under_test_reset", GAME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reset_game_restores_request_time_limit_and_speed():
    game = _load_game_module()
    game.reset_game()
    game.current_level = 3
    game.request_time_limit = game.LEVELS[3]["time"]
    game.snake_speed = int(3 * game.LEVELS[3]["speed_mult"])

    assert game.request_time_limit != game.LEVELS[1]["time"]

    game.reset_game()

    assert game.current_level == 1
    assert game.request_time_limit == game.LEVELS[1]["time"]
    assert game.snake_speed == int(3 * game.LEVELS[1]["speed_mult"])
    assert game.request_timer == game.request_time_limit
    assert game.lives == 3
    assert game.score == 0
    assert game.food is not None
    assert game.snake_request in set(game.SHAPE_NAMES + game.FRUITS + game.VEGETABLES)
