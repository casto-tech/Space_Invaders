# Space Invaders — Project Instructions for Claude

## Project

A turtle-graphics Space Invaders game in pure Python. Entry point: `turtle_invaders.py`; package: `turtle_invaders/`. Tests in `tests/`. The game runs with `python turtle_invaders.py` or `python -m turtle_invaders`.

## Hard constraints

- **Standard library only.** No `pip install`. No third-party imports in any file under `turtle_invaders/` or `tests/`. If unsure whether a module qualifies, run `/check-stdlib`.
- No new top-level files outside the package, `tests/`, and the existing launcher.
- Target Python: **3.10+** (uses `match`/`case` and `sys.stdlib_module_names`).

## Working style — TDD always

Red → Green → Refactor. Every behavior change starts with a failing test.

1. Write **one** failing test in `tests/test_<module>.py` using `unittest.TestCase`.
2. Run `python -m unittest discover -s tests -v` and confirm it fails for the **right reason** (assertion failure, not `ImportError`).
3. Write the minimum production code to pass.
4. Re-run tests — all green.
5. Refactor with tests staying green.

Use `/tdd <feature>` to walk a single cycle. Pure refactors (no behavior change) do not need a new test, but existing tests must still pass.

Tests must not require a display — never instantiate `turtle.Screen()` in unit tests. Factor pure logic out of turtle-coupled classes so it can be tested headlessly.

## Python engineering standards

- Type hints on every public function/method. Use PEP 604 unions (`int | None`), not `Optional[int]`.
- Catch **specific** exceptions. No bare `except:`. No `except Exception:` unless re-raised or logged at a clear boundary.
- Context managers (`with`) for files, sockets, locks, sqlite connections.
- `@dataclass(frozen=True, slots=True)` for plain data; `enum.Enum` for state machines.
- `pathlib.Path` over `os.path` string juggling.
- f-strings only; no `%`-formatting or `.format()` in new code.
- No mutable default arguments.
- Functions stay under ~40 lines; one job per function.
- No dead code, no commented-out blocks, no `TODO` without a follow-up issue.
- Comments explain **why**, not **what**. Default to none.

## Security rules — apply everywhere

- **Never** `eval`, `exec`, or `compile` on input that isn't a verbatim source literal.
- `pickle.load` / `pickle.loads` only on bytes produced by this program on this machine. For any persistence touching user input, use `json`.
- `subprocess` calls must use the list form. `shell=True` is forbidden unless the command is a hard-coded literal with no interpolation. Never `os.system` / `os.popen`.
- For tokens, IDs, session keys, anything sensitive: `secrets`, not `random`.
- Integrity / fingerprinting: `hashlib.sha256` or stronger. MD5/SHA1 only for non-security checksums and only with a comment justifying it.
- SQL: `cursor.execute("... WHERE x = ?", (val,))` — never string-format query text.
- XML: prefer `json`. If XML is unavoidable, disable entity resolution explicitly.
- `ssl` contexts: verification on, hostname check on. No `verify=False`.
- Temp files: `tempfile.mkstemp` or `NamedTemporaryFile`. Never `mktemp`.
- Any `open(path)` where `path` is user-influenced must `Path(path).resolve()` and verify it stays under the intended root.
- No secrets, API keys, or credentials in source. The high-score file under `~/.turtle_invaders/` is the only persisted state.

## Tools available in this repo

- `/tdd <feature>` — walk one red-green-refactor cycle.
- `/check-stdlib` — scan `turtle_invaders/**/*.py` for non-stdlib imports.
- `security-reviewer` subagent — read-only security audit. Invoke with `Agent` and `subagent_type: "security-reviewer"`, pointing it at a file or diff.
- `python-expert` subagent — read-only idiom/quality review. Same invocation pattern.

Both review agents are read-only and safe to run any time; treat them as cheap second opinions before a commit.

## MCP servers configured

- `sequential-thinking` — structured reasoning for TDD decomposition and threat modeling.
- `context7` — live stdlib documentation lookup. Use this to verify a function's exact signature for the running Python rather than relying on memory.

## When in doubt

Prefer the boring stdlib solution over cleverness. If a feature seems to need a third-party library, the design is probably wrong — split the problem until each piece fits in the stdlib.
