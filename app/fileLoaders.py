import json
import csv
from pathlib import Path


BASE_DIRECTORY = Path.cwd()


def load_json(path, filename):
    filepath = BASE_DIRECTORY / path / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Cannot find language file in {filepath}")

    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Cannot read the JSON file at '{filepath}': {e}")


def load_csv(path, filename):
    filepath = BASE_DIRECTORY / path / filename

    if not filepath.exists():
        return None

    try:
        with filepath.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, dialect="unix")
            return list(reader)
    except (IOError, csv.Error) as e:
        print(f"Cannot read the file at '{filepath}': {e}")
