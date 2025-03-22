import json
import csv
from pathlib import Path
import tempfile
import shutil
import os

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


def load_csv(filename, path):
    filepath = BASE_DIRECTORY / path / filename

    if not filepath.exists():
        return None

    try:
        with filepath.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, dialect="unix")
            return list(reader)
    except (IOError, csv.Error) as e:
        raise RuntimeError(f"Cannot read the file at '{filepath}': {e}")


def clean_directory(filename_pattern, path):
    filepath = BASE_DIRECTORY / path
    for file in filepath.glob(filename_pattern):
        if file.is_file():
            os.unlink(file)


def add_record_csv(filename, path, tasks, keys):
    filepath = BASE_DIRECTORY / path / filename

    with filepath.open("a+", encoding="utf-8") as csv_file:
        fieldnames = list(keys)
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        try:
            if csv_file.tell() == 0:
                csv_writer.writeheader()

            csv_writer.writerows(tasks)
        except (IOError, csv.Error) as e:
            raise RuntimeError(f"Cannot write new tasks in '{filepath}': {e}")


def sync_csv(filename, path, tasks, keys):
    filepath = BASE_DIRECTORY / path / filename

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
    ) as temp_file:
        fieldnames = list(keys)
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
