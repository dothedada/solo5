import json
import csv
from pathlib import Path
import tempfile
import shutil
from datetime import date
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
        except (IOError, csv.Error) as e:
            os.unlink(temp_file.name)
            raise RuntimeError(f"Cannot write in {filename}: {e}")

    try:
        shutil.move(temp_file.name, filepath)
    except (IOError, csv.Error) as e:
        os.unlink(temp_file.name)
        raise RuntimeError(f"The file {filename} cannot be saved: {e}")


def append_tasks_csv(filename, tasks):
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value / filename
    file_exist = filepath.exists()

    with filepath.open("a+", encoding="utf-8") as file:
        fieldnames = list(Defaults.KEYS_ALLOWED.value)
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exist:
            file.seek(0)
            if not file.read():
                writer.writeheader()

        try:
            writer.writerows(tasks)
        except (IOError, csv.Error) as e:
            raise RuntimeError(f"Cannot append to '{filepath}': {e}")


def remove_csv(filename):
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value / filename

    if filepath.exists():
        os.unlink(filepath)


def check_for_today_csv():
    filename = f"today_{str(date.today())}.csv"
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value / filename

    return filepath.exists()


def purge_old_today_csv():
    filepath = BASE_DIRECTORY / Defaults.DATA_PATH.value
    today_str = str(date.today())
    results = []

    for dirpath, _, filenames in os.walk(filepath):
        for file in filenames:
            if "today" in file:
                results.append(os.path.join(dirpath, file))

    for file in results:
        if today_str not in file:
            os.unlink(file)
