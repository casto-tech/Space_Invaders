---
description: Scan the project for non-stdlib imports. Fails if any source file imports a module outside the Python standard library.
allowed-tools: Bash
---

Run the following Python one-liner to scan `turtle_invaders/` and `tests/` for any `import` that targets a module outside `sys.stdlib_module_names`. The check uses `ast`, so it's not fooled by comments or string-literal mentions, and the allowlist is whatever the running interpreter ships with — no hand-maintained list to drift.

```
python - <<'PY'
import ast, pathlib, sys

roots = [pathlib.Path("turtle_invaders"), pathlib.Path("tests")]
bad: list[str] = []

for root in roots:
    if not root.exists():
        continue
    for path in root.rglob("*.py"):
        try:
            tree = ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as e:
            bad.append(f"{path}:{e.lineno} SyntaxError: {e.msg}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in sys.stdlib_module_names and top != "turtle_invaders":
                        bad.append(f"{path}:{node.lineno} non-stdlib import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.level != 0 or not node.module:
                    continue
                top = node.module.split(".")[0]
                if top not in sys.stdlib_module_names and top != "turtle_invaders":
                    bad.append(f"{path}:{node.lineno} non-stdlib import: from {node.module}")

if bad:
    print("FAIL: non-stdlib imports found")
    for line in bad:
        print(f"  {line}")
    sys.exit(1)
print("PASS: stdlib-only")
PY
```

Interpret the result for the user:

- **PASS** — say so in one line and stop.
- **FAIL** — list the offending imports, then for each one suggest the closest stdlib equivalent (e.g. `requests` → `urllib.request`, `yaml` → `json`, `numpy` → list comprehensions / `array`, `pytest` → `unittest`). Do **not** edit files yet — wait for the user to confirm the rewrite direction.

The project's own package `turtle_invaders` is allowlisted because internal imports (`from turtle_invaders.cannon import Cannon`) are obviously fine; everything else must be stdlib.
