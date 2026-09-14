# Brain Zapper — Sound Toggle Dead-Code Fix (2026-09-14)

## Original Request
Surgical-implementation run on `TeacherEvan/Brain-zapper` (single-file pygame
game). No prior plans existed; author fresh plan from code state, gate, implement.

## Discovery
- Repo: single-file game `Enhanced_Wild_Worm_Visual_Demo.py` (883 LOC) + 5 pytest
  suites. 83 tests green under `SDL_VIDEODRIVER=dummy`.
- `handle_events()` KEYDOWN chain binds `K_s` to **two** branches:
  - line 780: `elif event.key in (pygame.K_DOWN, pygame.K_s): snake_direction = (0, 1)`
  - line 796: `elif event.key == pygame.K_s: toggle_sound()`
  Because the chain is `if/elif`, the movement branch always wins. The sound-toggle
  branch is **dead code** — pressing S moves the snake down and never toggles
  sound, contradicting the welcome-screen prompt "Press S to toggle sound".

## Objectives
| ID    | Objective | Requirement | Validation |
|-------|-----------|-------------|------------|
| OBJ-01 | Remove `K_s` from the DOWN movement binding so the sound-toggle branch is reachable | AC-01 | Pressing S toggles `SOUND_ENABLED`, does not change `snake_direction` |
| OBJ-02 | Add regression test `test_s_key_toggles_sound_not_direction` | AC-02 | pytest green; test fails on pre-fix source |
| OBJ-03 | Add regression test `test_s_key_no_longer_moves_down` | AC-03 | pytest green; test fails on pre-fix source |
| OBJ-04 | Full suite stays green (83 -> 85) | AC-04 | `python -m pytest -q` exit 0 |

## Definition of Done
- [x] Source patched (one binding change)
- [x] Two regression tests added under `tests/`
- [x] `python -m pytest -q` green
- [x] No other behaviour changed
