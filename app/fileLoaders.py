import json
import csv
from pathlib import Path
import tempfile
import shutil
import os

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


def load_csv(filename):
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value / filename

    if not filepath.exists():
        return None

    try:
        with filepath.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, dialect="unix")
            return list(reader)
    except (IOError, csv.Error) as e:
        print(f"Cannot read the file at '{filepath}': {e}")


def sync_csv(filename, tasks):
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value / filename

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
    ) as temp_file:
        fieldnames = list(Defaults.KEYS_ALLOWED.value)
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

        try:
            writer.writeheader()
            writer.writerows(tasks)
        except Exception as e:
            os.unlink(temp_file.name)
            raise RuntimeError(f"Cannot write in {filename}: {e}")

    try:
        shutil.move(temp_file.name, filepath)
    except Exception as e:
        os.unlink(temp_file.name)
        raise RuntimeError(f"The file {filename} cannot be saved: {e}")
