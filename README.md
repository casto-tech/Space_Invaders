# Turtle Invaders

A Space Invaders clone written in pure Python using the `turtle` graphics
module from the standard library. No third-party dependencies — clone, run,
play.

```
        ┌────────────────────────────────────────────────────┐
        │  Score:  1240   Hi:  3500   Level: 2     ■ ■ ■    │
        │                                                    │
        │              ●         ■                           │
        │                  ▲                                 │
        │       ●                            ●               │
        │              |                                     │
        │                                                    │
        │   ▓▓▓▓▓▓▓        ▓▓▓▓▓▓▓        ▓▓▓▓▓▓▓           │
        │   ▓▓▓▓▓▓▓        ▓▓ ▓▓ ▓        ▓▓▓▓▓▓▓           │
        │                                                    │
        │                      ─┴─                           │
        └────────────────────────────────────────────────────┘
```

## Features

- **Three alien types** — fast/weak, medium, slow/tanky — each with their own
  HP, fire rate, point value, and color. Damaged aliens visibly brighten as
  their HP drops.
- **Destructible bunkers** — three multi-block shields between you and the
  invaders. Lasers eat through them block by block.
- **Progressive difficulty** — every level boosts alien speed by 15% and
  shortens spawn intervals by 15%; kills-to-clear grows by 5 each level.
- **Lives, invulnerability frames, and pause** — three lives by default, with
  a 1.5s flicker after each hit. Press `P` to pause anywhere mid-game.
- **Persistent high score** — saved to `~/.turtle_invaders/highscore.json`.
- **Fullscreen on launch** — the window auto-zooms and the canvas resizes to
  match, so sprites use the whole display.

## Requirements

- **Python 3.10 or newer** (the code uses PEP 604 unions and `match`/`case`).
- A working Tk install (`tkinter`). On most Linux distros this means the
  `python3-tk` package; macOS and Windows Python builds ship with it.
- A display — the game opens a window; it will not run headless.

There is nothing else to install. **No `pip` step.**

Verify your Python:

```bash
python --version       # must report 3.10+
python -c "import tkinter; print(tkinter.TkVersion)"
```

## Installation

```bash
git clone <repo-url> Space_Invaders
cd Space_Invaders
```

That's it. There's no virtualenv to set up, no requirements file to install.

## Running the game

Either of these works from the repo root:

```bash
python turtle_invaders.py
# or
python -m turtle_invaders
```

The first launch creates `~/.turtle_invaders/` to hold the high-score file.

## Controls

| Key             | Action                            |
|-----------------|-----------------------------------|
| `←` / `→`       | Move cannon left / right          |
| `Space`         | Fire (also: start game from menu) |
| `P`             | Pause / resume                    |
| `R`             | Restart (only after Game Over)    |
| `Q`             | Quit                              |

Hold an arrow key to keep moving — the cannon stops on key-release.

## Gameplay

You control the white cannon at the bottom of the screen. Aliens spawn at the
top and descend toward you. Shoot them; don't let them reach the floor;
don't get shot.

- **Hit an alien** → score its point value. The alien is destroyed when its
  HP reaches zero; tougher aliens take multiple hits.
- **Hit a bunker block** (yours or theirs) → block disappears.
- **Get hit by an alien laser or let an alien reach the floor** → you lose a
  life and gain 1.5s of invulnerability (the cannon flickers).
- **Lose all lives** → Game Over. Press `R` to play again.
- **Hit the per-level kill quota** → level up; aliens get faster and spawn
  more often.

### Alien types

| Type       | Shape    | HP | Points | Speed     | Fire rate |
|------------|----------|----|--------|-----------|-----------|
| Scout      | circle   | 1  | 10     | fast      | low       |
| Soldier    | square   | 2  | 20     | medium    | medium    |
| Heavy      | turtle   | 3  | 30     | slow      | high      |

Tweak the table in `turtle_invaders/config.py` if you want a different
balance.

## Project layout

```
Space_Invaders/
├── turtle_invaders.py        # entry point (python turtle_invaders.py)
├── turtle_invaders/          # package
│   ├── __init__.py
│   ├── __main__.py           # enables `python -m turtle_invaders`
│   ├── game.py               # main loop, state machine, collisions
│   ├── cannon.py             # player ship
│   ├── alien.py              # enemy sprites
│   ├── laser.py              # projectile (player + alien)
│   ├── bunker.py             # destructible shields
│   ├── hud.py                # score / lives overlay
│   ├── scenes.py             # start / pause / game-over screens
│   ├── highscore.py          # JSON persistence
│   └── config.py             # tunables + Bounds/AlienType dataclasses
├── tests/                    # unittest suite (headless — no display)
│   ├── test_config.py
│   └── test_highscore.py
└── CLAUDE.md                 # contributor instructions for AI assistants
```

## Architecture

The game is built around a single `Game` class (`turtle_invaders/game.py`)
that owns a `State` enum (`START`, `PLAYING`, `PAUSED`, `GAME_OVER`) and a
list per entity type (aliens, bunkers, player lasers, alien lasers).

Each frame:

1. `cannon.update(dt)` / `cannon.draw()` — move and redraw the player.
2. `_spawn_alien(dt)` — maybe spawn one new alien.
3. `_update_aliens(dt)` — move aliens; off-floor aliens cost a life.
4. `_process_player_lasers(dt)` — advance, then check vs aliens and bunkers.
5. `_process_alien_lasers(dt)` — advance, then check vs cannon and bunkers.
6. `hud.draw(...)` — redraw the score / lives / level overlay.

The frame loop targets 60 FPS but caps `dt` at 50 ms so a long pause doesn't
teleport everything across the screen on resume.

Geometry uses two dataclasses from `config.py`:

- `Bounds` — screen extents (`left`, `right`, `top`, `bottom`, `floor_level`,
  `gutter`), computed once from the resized canvas.
- `AlienType` — immutable spec for each alien tier (shape, color, HP, points,
  speed and fire multipliers).

Both are `frozen=True, slots=True` — cheap, hashable, immutable.

## Configuration

Knob-twiddling lives in `turtle_invaders/config.py`. Edit the module-level
constants:

| Constant                    | Meaning                                    |
|-----------------------------|--------------------------------------------|
| `FRAME_RATE`                | Target frames per second.                  |
| `CANNON_STEP`               | Player speed (px/s).                       |
| `CANNON_FIRE_COOLDOWN`      | Seconds between player shots.              |
| `LASER_SPEED`               | Projectile speed (px/s).                   |
| `STARTING_LIVES`            | Lives at game start.                       |
| `INVULN_DURATION`           | Post-hit invulnerability seconds.          |
| `ALIEN_SPAWN_INTERVAL`      | Base seconds between alien spawns.         |
| `ALIEN_SPEED`               | Base alien speed (px/s).                   |
| `ALIEN_FIRE_CHANCE_PER_SEC` | Per-alien fire probability per second.     |
| `LEVEL_SPEED_MULT`          | Speed multiplier applied per level.        |
| `LEVEL_SPAWN_MULT`          | Spawn-interval multiplier per level.       |
| `ALIENS_PER_LEVEL`          | Base kills required to clear level 1.      |
| `BUNKER_COUNT`              | Number of bunkers on screen.               |
| `BUNKER_BLOCK_ROWS/COLS`    | Bunker block grid.                         |
| `ALIEN_TYPES`               | List of `AlienType` definitions.           |

## Persistence

The only persisted state is the high score, stored as JSON at:

```
~/.turtle_invaders/highscore.json
```

The schema is trivial:

```json
{"high_score": 4200}
```

Both load and save fail silently on missing files, bad JSON, or filesystem
errors — a corrupt score file is treated as score 0, never a crash. Delete
the file to reset.

## Development

This project follows a **strict TDD workflow** and a **standard-library-only**
rule. See [`CLAUDE.md`](./CLAUDE.md) for the full set of constraints — they
apply to humans too.

### Running tests

```bash
python -m unittest discover -s tests -v
```

Tests are headless: they never instantiate `turtle.Screen()`. Pure logic
(geometry, persistence, score math) is factored so it can be tested without
a display. Adding tests that pop a window will fail in CI.

### Working style

1. Write **one** failing test in `tests/test_<module>.py` using
   `unittest.TestCase`.
2. Run the suite — confirm it fails for the right reason (an assertion, not
   an `ImportError`).
3. Write the minimum production code to pass.
4. Re-run — all green.
5. Refactor with tests staying green.

Pure refactors (no behavior change) skip step 1 but must still keep the
existing suite green.

### Engineering standards (highlights)

- Type hints on every public function/method; PEP 604 unions (`int | None`).
- `@dataclass(frozen=True, slots=True)` for plain data; `enum.Enum` for state.
- No `eval` / `exec` / `pickle.load` on user-influenced input.
- No bare `except:`; no `except Exception:` without a re-raise or boundary log.
- f-strings only.
- Functions under ~40 lines; one job each.
- Comments explain **why**, not **what** — default to none.

The full ruleset is in `CLAUDE.md`.

## Troubleshooting

**`ModuleNotFoundError: No module named 'tkinter'`**
Install the Tk bindings for your Python:
- Debian/Ubuntu: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- macOS (Homebrew): `brew install python-tk`

**The window doesn't fill the screen**
The maximize step uses a platform-specific Tk call (`-zoomed` on Linux,
`zoomed` state on Windows). On exotic window managers neither may apply; the
game still runs in a default-sized window.

**No sound**
There is none. `turtle` has no audio support; adding sound would require a
third-party library, which the project bans.

**Performance hiccups**
The renderer leans on `turtle.tracer(0)` plus manual `screen.update()`,
which is fast for the dozens of sprites in play. If you crank
`BUNKER_BLOCK_ROWS`/`COLS` or `ALIEN_SPAWN_INTERVAL` aggressively, expect
frame drops — Python's `turtle` is not optimized for hundreds of sprites.

## License

This project is unlicensed by default. Add a `LICENSE` file before
distributing.
