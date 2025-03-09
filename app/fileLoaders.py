import json
import csv
from pathlib import Path

from config import Defaults

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


def add_tasks_to_csv(path, filename, tasks):
    filepath = BASE_DIRECTORY / path / filename

    try:
        with filepath.open("a", encoding="utf-8") as csv_file:
            fieldnames = list(Defaults.KEYS_ALLOWED.value)
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if csv_file.tell() == 0:
                writer.writeheader()

            writer.writerows(tasks)
    except (IOError, csv.Error) as e:
        raise RuntimeError(f"Cannot write task to the file {filename}: {e}")
