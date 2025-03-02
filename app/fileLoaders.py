import json
from pathlib import Path


def load_json(path, filename):
    BASE_DIRECTORY = Path.cwd()
    filepath = BASE_DIRECTORY / path / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Cannot find language file in {filepath}")

    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)
