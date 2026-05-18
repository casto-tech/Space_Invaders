import json
import pathlib

_SCORE_PATH = pathlib.Path.home() / ".turtle_invaders" / "highscore.json"


def load() -> int:
    try:
        return int(json.loads(_SCORE_PATH.read_text()).get("high_score", 0))
    except Exception:
        return 0


def save(score: int) -> None:
    try:
        _SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _SCORE_PATH.write_text(json.dumps({"high_score": score}))
    except Exception:
        pass
