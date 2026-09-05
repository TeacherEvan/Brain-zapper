# Brain-zapper Maintenance Plan — 2026-09-05

Living maintenance backlog for the `TeacherEvan/Brain-zapper` repo.
Authored by a surgical-implementation run; this doc is the future runs'
`search:plan` target (see `rg -l -g 'docs/**/*.md' -i 'todo|objective|tick|plan|WIP|\[x\]|\[ \]' .`).

Source-of-truth on entry: branch `main` @ a792208 (single commit).
Baseline gates (re-verify on every commit):
- `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py` -> exit 0
- `pytest -q` with `SDL_VIDEODRIVER=dummy` -> 44 passed, exit 0

## Objectives

- [x] OBJ-001 — Add this maintenance plan doc under `docs/plans/` so future
  surgical-implementation runs have a search target.
  File: `docs/plans/2026-09-05-brain-zapper-MAINTENANCE.md`
  Validation: `ls docs/plans/` shows it.

- [x] OBJ-002 — Document the test workflow in `README.md` (install pytest,
  run `pytest -q`, set `SDL_VIDEODRIVER=dummy` for headless).
  Validation: `rg -n 'pytest' README.md` returns hits.

- [x] OBJ-003 — Word lists (`SHAPE_NAMES`, `FRUITS`, `VEGETABLES`) are
  non-empty lists of non-empty strings. Locked in by
  `test_shape_names_non_empty_strings`, `test_fruits_non_empty_strings`,
  `test_vegetables_non_empty_strings`.

- [x] OBJ-004 — All 34 named RGB constants and the gradient/particle palettes
  are 3-tuples of `int` in `[0, 255]`. Locked in by
  `test_named_rgb_constant_is_3_tuple_in_range` (parametrized over 34 names),
  `test_enhanced_particle_colors_all_rgb`,
  `test_gradient_themes_have_at_least_three_stops`.

- [x] OBJ-005 — `create_background_stars` and `create_spectacular_particle`
  emit well-formed dicts with the expected keys/ranges. Locked in by
  `test_create_background_stars_appends_to_global_list`,
  `test_create_spectacular_particle_appends_well_formed_particles`.

- [x] OBJ-006 — `generate_tone` returns `None` when sound is disabled or
  audio is unavailable. Locked in by
  `test_generate_tone_returns_none_when_sound_disabled`,
  `test_generate_tone_returns_array_of_expected_length_when_audio_off`.

- [x] OBJ-007 — `reset_game` restores snake length to 5 at the screen centre
  and resets `lives=3`, `score=0`, `game_state=STATE_PLAYING`. Locked in by
  `test_reset_game_returns_snake_to_start_position`.

## Definition of Done

- `pytest -q` -> 44 passed, exit 0.
- `python3 -m py_compile Enhanced_Wild_Worm_Visual_Demo.py` -> exit 0.
- `git check-ignore -v docs/.scratch-audit/` -> ignored.
- Branch pushed to `origin`; no PR opened (per run constraints).

## Out of scope (future backlog, not this run)

- Refactor single-file pygame game into modules — would break the test
  loader's `importlib.util.spec_from_file_location` import path.
- Add coverage for `update_game`, `handle_events`, `draw_*` — these touch
  the real pygame surface; out of budget without a mock surface.
- Add CI matrix (Python 3.10/3.11/3.12) — workflow already pins 3.11.
