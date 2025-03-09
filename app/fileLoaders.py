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


def remove_tasks_from_csv(path, filename, task_ids):
    filepath = BASE_DIRECTORY / path / filename
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        encoding="utf-8",
    )

    try:
        with filepath.open("r", encoding="utf-8") as csv_file:
            fieldnames = list(Defaults.KEYS_ALLOWED.value)
            data_readed = csv.DictReader(csv_file, dialect="unix")
            data_writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            data_writer.writeheader()

            for row in data_readed:
                if row["id"] in task_ids:
                    continue
                data_writer.writerow(row)

        temp_file.close()
        shutil.move(temp_file.name, filepath)
    except Exception as e:
        temp_file.close()
        try:
            os.unlink(temp_file.name)
        except Exception as e:
            print(e)
            pass
        raise RuntimeError(f"Cannot delete task from the file {filename}: {e}")
