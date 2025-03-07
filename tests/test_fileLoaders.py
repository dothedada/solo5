import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from app.fileLoaders import load_json


class TestLoadJson(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_json(self):
        data = {"key": "value"}
        file_path = self.base_path / "test.json"

        with open(file_path, "w") as file:
            json.dump(data, file)

        load = load_json(self.base_path, "test.json")
        self.assertEqual(load, data)

    def test_rise_error_if_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_json(self.base_path, "nofile.json")

    def test_relative_file_path(self):

        subdir = self.base_path / "new_subdir"
        subdir.mkdir()
        data = {"key": "value"}
        file_path = subdir / "test.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

        result = load_json(subdir, "test.json")
        self.assertEqual(data, result)
