"""Pure-logic tests for the gameplay loop (OBJ-017..OBJ-024).

Headless-safe: mirrors the importlib pattern used by the existing suites.
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
    spec = importlib.util.spec_from_file_location("game_under_test_gl", GAME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- OBJ-017 -- pick_new_request -------------------------------------------

def test_pick_new_request_assigns_from_pool():
    game = _load_game_module()
    pool = set(game.SHAPE_NAMES + game.FRUITS + game.VEGETABLES)
    random.seed(1)
    game.pick_new_request()
    assert game.snake_request in pool


def test_pick_new_request_changes_value():
    game = _load_game_module()
    random.seed(42)
    before = game.snake_request
    game.pick_new_request()
    assert game.snake_request != before


# --- OBJ-018 -- spawn_food -------------------------------------------------

def test_spawn_food_well_formed():
    game = _load_game_module()
    f = game.spawn_food()
    assert set(f.keys()) >= {"pos", "type", "color"}
    assert isinstance(f["pos"], tuple) and len(f["pos"]) == 2
    assert isinstance(f["type"], str) and f["type"]
    assert isinstance(f["color"], tuple) and len(f["color"]) == 3


def test_spawn_food_in_bounds():
    game = _load_game_module()
    random.seed(7)
    for _ in range(20):
        f = game.spawn_food()
        x, y = f["pos"]
        assert 80 <= x <= game.screen_width - 80
        assert 180 <= y <= game.screen_height - 80


# --- OBJ-019 -- check_food_collision ----------------------------------------

def test_check_food_collision_true_within_tolerance():
    game = _load_game_module()
    game.snake_segments = [(100, 200)]
    food = {"pos": (110, 205), "type": "Apple", "color": (255, 0, 0)}
    assert game.check_food_collision(food, tolerance=25) is True


def test_check_food_collision_false_outside_tolerance():
    game = _load_game_module()
    game.snake_segments = [(100, 200)]
    food = {"pos": (200, 300), "type": "Apple", "color": (255, 0, 0)}
    assert game.check_food_collision(food, tolerance=25) is False


def test_check_food_collision_no_food():
    game = _load_game_module()
    game.snake_segments = [(100, 200)]
    assert game.check_food_collision(None) is False


def test_check_food_collision_no_snake():
    game = _load_game_module()
    game.snake_segments = []
    food = {"pos": (100, 200), "type": "Apple", "color": (255, 0, 0)}
    assert game.check_food_collision(food) is False


# --- OBJ-020 -- award_score ------------------------------------------------

def test_award_score_accumulates():
    game = _load_game_module()
    original = game.score
    try:
        game.award_score(3)
        assert game.score == original + 3
        game.award_score(2)
        assert game.score == original + 5
    finally:
        game.score = original


# --- OBJ-021 -- advance_level ----------------------------------------------

def test_advance_level_promotes_on_target():
    game = _load_game_module()
    original = (game.current_level, game.request_time_limit, game.snake_speed)
    try:
        game.current_level = 1
        game.score = 0
        assert game.advance_level() is False  # not yet at target
        game.score = LEVELS_TARGET_1
        assert game.advance_level() is True
        assert game.current_level == 2
        assert game.request_time_limit == game.LEVELS[2]["time"]
        assert game.snake_speed == int(3 * game.LEVELS[2]["speed_mult"])
    finally:
        game.current_level, game.request_time_limit, game.snake_speed = original


def test_advance_level_noop_when_max_level():
    game = _load_game_module()
    original = (game.current_level, game.request_time_limit, game.snake_speed)
    try:
        max_lvl = max(game.LEVELS.keys())
        game.current_level = max_lvl
        game.score = 9999
        assert game.advance_level() is False
        assert game.current_level == max_lvl
    finally:
        game.current_level, game.request_time_limit, game.snake_speed = original


LEVELS_TARGET_1 = 3


# --- OBJ-022 -- update_game food loop ---------------------------------------

def test_update_game_food_loop_eats_and_awards():
    game = _load_game_module()
    original = {
        "game_state": game.game_state,
        "lives": game.lives,
        "request_timer": game.request_timer,
        "score": game.score,
        "snake_request": game.snake_request,
    }
    game.play_life_lost_sound = lambda: None
    game.play_game_over_sound = lambda: None
    try:
        game.game_state = game.STATE_PLAYING
        game.lives = 3
        game.request_timer = 5.0
        game.score = 0
        game.snake_segments = [(100, 200)]
        game.food = {"pos": (100, 200), "type": "Apple", "color": (255, 0, 0)}
        game.update_game(0.016)
        assert game.score == 1
        assert game.food is not None and game.food != {"pos": (100, 200), "type": "Apple", "color": (255, 0, 0)}
        pool = set(game.SHAPE_NAMES + game.FRUITS + game.VEGETABLES)
        assert game.snake_request in pool
    finally:
        for k, v in original.items():
            setattr(game, k, v)


def test_update_game_food_loop_no_collision_no_score():
    game = _load_game_module()
    original = {
        "game_state": game.game_state,
        "lives": game.lives,
        "request_timer": game.request_timer,
        "score": game.score,
    }
    game.play_life_lost_sound = lambda: None
    game.play_game_over_sound = lambda: None
    try:
        game.game_state = game.STATE_PLAYING
        game.lives = 3
        game.request_timer = 5.0
        game.score = 0
        game.snake_segments = [(100, 200)]
        game.food = {"pos": (500, 500), "type": "Apple", "color": (255, 0, 0)}
        game.update_game(0.016)
        assert game.score == 0
        assert game.food["pos"] == (500, 500)
    finally:
        for k, v in original.items():
            setattr(game, k, v)


# --- OBJ-023/024 -- globals + reset_game ------------------------------------

def test_current_level_defaults_to_one():
    game = _load_game_module()
    assert game.current_level == 1


def test_reset_game_resets_current_level():
    game = _load_game_module()
    game.current_level = 5
    game.reset_game()
    assert game.current_level == 1
    assert game.food is not None
