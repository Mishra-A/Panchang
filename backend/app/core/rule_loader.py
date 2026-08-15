import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RULES_DIR = PROJECT_ROOT / "data" / "rules"


def load_rule(filename: str) -> dict:
    path = RULES_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Rule file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)