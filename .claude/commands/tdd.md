---
description: Walk one red-green-refactor TDD cycle for the named feature using stdlib unittest.
argument-hint: <one-line feature description>
---

You are running a single TDD cycle for the feature: **$ARGUMENTS**

Hard rules for this cycle (all from `CLAUDE.md`, repeated for emphasis):

- Standard library only. No third-party imports.
- Python 3.10+ idioms.
- Tests live in `tests/test_<module>.py` and use `unittest.TestCase`.
- Tests must run headlessly — never instantiate `turtle.Screen()` in a test.
- Type hints on every public function/method.

Follow these steps in order. Stop at each `STOP` and wait for the user before continuing.

## 1. Restate and scope

In one sentence, restate the feature in your own words. Then identify the **smallest single observable behavior** to test first. If the feature is too large for one cycle, list the behaviors as a checklist and confirm with the user which one this cycle covers.

**STOP** — confirm scope with the user before writing any code.

## 2. Bootstrap (only if needed)

If `tests/` does not exist, create it with an empty `tests/__init__.py`. If the target test file does not exist, create it with the minimum `unittest` skeleton — but no test cases yet.

## 3. Red — write ONE failing test

Add a single `def test_<behavior>(self):` method that exercises the chosen behavior. The test must:

- Import the production symbol it intends to drive into existence. If that symbol does not exist yet, the import will fail — that's fine, but on the *first* test for a new module, prefer to define the symbol as a stub returning `NotImplementedError` so the failure is a clear `AssertionError`, not an `ImportError`.
- Assert on observable behavior, not on internal state.
- Use `assertEqual` / `assertRaises` / `assertIs` etc., never `assertTrue(x == y)`.

Run the test:

```
python -m unittest discover -s tests -v
```

Verify the failure is the expected `AssertionError` (or `NotImplementedError`) — **not** a typo, syntax error, or unrelated `ImportError`. If the failure is for the wrong reason, fix the test first.

**STOP** — show the user the failing test output before implementing.

## 4. Green — minimum production code

Write the smallest amount of code in `turtle_invaders/<module>.py` that turns the failing test green. Resist adding anything the current test does not require. Type hints are not optional — add them as you write.

Re-run:

```
python -m unittest discover -s tests -v
```

All tests must pass. If anything regressed, the new code is wrong — fix it before continuing.

## 5. Refactor

With tests green, clean up:

- Extract helpers if a function got too long (>40 lines or doing two jobs).
- Improve names.
- Remove duplication you introduced.
- Add a `@dataclass`/`enum.Enum`/context manager if one would clarify the code.

Re-run tests after each non-trivial refactor. Never refactor on red.

## 6. Optional review

If the change touches anything resembling I/O, persistence, subprocesses, or user-influenced data, run the `security-reviewer` agent on the touched files:

```
Agent(subagent_type="security-reviewer", prompt="Audit <files>")
```

For non-trivial logic, run `python-expert` similarly. These are read-only and cheap — use them.

## 7. Report

Summarize in 2–3 sentences:
- What behavior is now tested and implemented.
- What files changed (paths only, no diff).
- What the next TDD cycle should pick up, if the feature isn't complete.

Do **not** commit. Commits are the user's call.
