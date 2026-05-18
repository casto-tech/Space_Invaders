import json
import pathlib

_SCORE_PATH = pathlib.Path.home() / ".turtle_invaders" / "highscore.json"


def load() -> int:
    try:
        data = json.loads(_SCORE_PATH.read_text())
        return int(data.get("high_score", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError):
        return 0


def save(score: int) -> None:
    try:
        _SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _SCORE_PATH.write_text(json.dumps({"high_score": score}))
    except OSError:
        pass
