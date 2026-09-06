"""Extended pure-logic tests for Enhanced_Wild_Worm_Visual_Demo.

OBJ-008..OBJ-015. Same headless-safe import pattern as test_game_logic.py.
"""
import importlib.util
import os
from pathlib import Path

import pytest

# Headless pygame (mirror of test_game_logic.py).
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_PATH = REPO_ROOT / "Enhanced_Wild_Worm_Visual_Demo.py"


def _load_game_module():
    spec = importlib.util.spec_from_file_location("game_under_test_ext", GAME_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- OBJ-008 -- LEVELS dict shape -------------------------------------------

def test_levels_dict_has_at_least_three_entries():
    game = _load_game_module()
    assert isinstance(game.LEVELS, dict)
    assert len(game.LEVELS) >= 3


def test_levels_entries_have_required_keys_with_correct_types():
    game = _load_game_module()
    for level_id, data in game.LEVELS.items():
        assert isinstance(level_id, int), f"level key {level_id!r} not int"
        assert level_id > 0
        assert isinstance(data, dict), f"level {level_id} value not dict"
        assert "target" in data and isinstance(data["target"], int)
        assert "time" in data and isinstance(data["time"], int)
        assert "speed_mult" in data and isinstance(data["speed_mult"], (int, float))


# --- OBJ-009 -- update_particles(dt) ages and culls -------------------------

def _make_particle(pos=(100.0, 100.0), vel=(1.0, 0.0), lifetime=1.0, color=None):
    return {
        "pos": list(pos),
        "vel": list(vel),
        "size": 4,
        "color": color if color is not None else (255, 255, 255),
        "lifetime": lifetime,
        "total_lifetime": lifetime,
        "sparkle": False,
    }


def test_update_particles_decrements_lifetime_for_living_particle():
    game = _load_game_module()
    game.particles.clear()
    p = _make_particle(lifetime=2.0)
    game.particles.append(p)
    try:
        game.update_particles(0.5)
        assert p["lifetime"] == pytest.approx(1.5)
        assert p in game.particles
    finally:
        game.particles.clear()


def test_update_particles_removes_expired_particles():
    game = _load_game_module()
    game.particles.clear()
    p = _make_particle(lifetime=0.0)
    game.particles.append(p)
    try:
        game.update_particles(0.016)
        assert p not in game.particles
    finally:
        game.particles.clear()


def test_update_particles_drifts_position_with_velocity():
    game = _load_game_module()
    game.particles.clear()
    p = _make_particle(pos=(0.0, 0.0), vel=(10.0, 0.0), lifetime=1.0)
    game.particles.append(p)
    try:
        game.update_particles(0.1)
        # pos[0] += vel[0] * dt * 60 = 10 * 0.1 * 60 = 60
        assert p["pos"][0] == pytest.approx(60.0, abs=1e-6)
    finally:
        game.particles.clear()


# --- OBJ-010 -- toggle_sound() is a flip and idempotent --------------------

def test_toggle_sound_flips_sound_enabled():
    game = _load_game_module()
    original = game.SOUND_ENABLED
    try:
        game.SOUND_ENABLED = True
        game.toggle_sound()
        assert game.SOUND_ENABLED is False
    finally:
        game.SOUND_ENABLED = original


def test_toggle_sound_twice_returns_to_original():
    game = _load_game_module()
    original = game.SOUND_ENABLED
    try:
        for start in (True, False):
            game.SOUND_ENABLED = start
            game.toggle_sound()
            game.toggle_sound()
            assert game.SOUND_ENABLED is start
    finally:
        game.SOUND_ENABLED = original


# --- OBJ-011 -- STATE_* constants are distinct integers --------------------

def test_state_constants_are_distinct_integers():
    game = _load_game_module()
    welcome = game.STATE_WELCOME
    playing = game.STATE_PLAYING
    over = game.STATE_GAME_OVER
    assert isinstance(welcome, int) and isinstance(playing, int) and isinstance(over, int)
    assert len({welcome, playing, over}) == 3


# --- OBJ-012 -- update_game(dt) decrements request_timer in PLAYING --------

def test_update_game_decrements_request_timer_when_playing():
    game = _load_game_module()
    original_state = game.game_state
    original_timer = game.request_timer
    game.game_state = game.STATE_PLAYING
    game.request_timer = 5.0
    try:
        game.update_game(0.5)
        assert game.request_timer == pytest.approx(4.5)
    finally:
        game.game_state = original_state
        game.request_timer = original_timer


def test_update_game_skips_logic_when_not_playing():
    game = _load_game_module()
    original_state = game.game_state
    original_timer = game.request_timer
    original_lives = game.lives
    game.game_state = game.STATE_GAME_OVER
    game.request_timer = 5.0
    game.lives = 3
    try:
        game.update_game(0.5)
        assert game.request_timer == 5.0
        assert game.lives == 3
    finally:
        game.game_state = original_state
        game.request_timer = original_timer
        game.lives = original_lives


# --- OBJ-013 -- update_game drains lives on timer expiry -------------------

def test_update_game_life_loss_when_timer_expires():
    game = _load_game_module()
    original = {
        "game_state": game.game_state,
        "lives": game.lives,
        "request_timer": game.request_timer,
    }
    original_life_sound = game.play_life_lost_sound
    game.play_life_lost_sound = lambda: None  # silence side effect
    try:
        game.game_state = game.STATE_PLAYING
        game.lives = 3
        game.request_timer = 0.1
        game.update_game(0.5)
        assert game.lives == 2
        assert game.request_timer == game.request_time_limit
        assert game.game_state == game.STATE_PLAYING
    finally:
        game.play_life_lost_sound = original_life_sound
        for k, v in original.items():
            setattr(game, k, v)


# --- OBJ-014 -- update_game transitions to STATE_GAME_OVER -----------------

def test_update_game_over_when_last_life_lost():
    game = _load_game_module()
    original = {
        "game_state": game.game_state,
        "lives": game.lives,
        "request_timer": game.request_timer,
    }
    original_life_sound = game.play_life_lost_sound
    original_over_sound = game.play_game_over_sound
    game.play_life_lost_sound = lambda: None
    game.play_game_over_sound = lambda: None
    try:
        game.game_state = game.STATE_PLAYING
        game.lives = 1
        game.request_timer = 0.1
        game.update_game(0.5)
        assert game.lives == 0
        assert game.game_state == game.STATE_GAME_OVER
    finally:
        game.play_life_lost_sound = original_life_sound
        game.play_game_over_sound = original_over_sound
        for k, v in original.items():
            setattr(game, k, v)


# --- OBJ-015 -- create_spectacular_particle colour-pool -------------------

def test_create_spectacular_particle_color_from_pool():
    game = _load_game_module()
    original = game.play_particle_sound
    game.play_particle_sound = lambda: None
    try:
        game.particles.clear()
        pool = set(game.ENHANCED_PARTICLE_COLORS)
        # 50 calls; the function caps total particles at ~100 (last 100 kept),
        # so we just assert the surviving particles' colours come from the pool.
        for _ in range(50):
            game.create_spectacular_particle((200, 200), game.NEON_PINK)
        spawned = [p["color"] for p in game.particles]
        assert len(spawned) >= 50  # at least one call batch survived
        for c in spawned:
            assert c in pool, f"particle color {c} not in pool {pool}"
        # When caller color IS in the pool, every spawned particle must use it verbatim.
        game.particles.clear()
        game.create_spectacular_particle((50, 50), game.NEON_PINK)
        assert all(p["color"] == game.NEON_PINK for p in game.particles)
    finally:
        game.play_particle_sound = original
        game.particles.clear()
