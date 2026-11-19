"""Тесты чтения тестового репозитория."""

import json
import tempfile
import unittest
from pathlib import Path

from src.test_repository import load_test_repository


class TestRepository(unittest.TestCase):
    """Проверки загрузки JSON-репозитория."""

    def load_data(self, data):
        """Создать временный JSON-файл и загрузить его."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.json"
            path.write_text(
                json.dumps(data),
                encoding="utf-8"
            )
            return load_test_repository(path)

    def test_valid_graph(self):
        """Проверить правильный граф."""
        graph = self.load_data({
            "A": ["B"],
            "B": []
        })

        self.assertEqual(graph["A"], ["B"])
        self.assertEqual(graph["B"], [])

    def test_missing_package(self):
        """Проверить зависимость без отдельного описания."""
        graph = self.load_data({"A": ["B"]})

        self.assertEqual(graph["B"], [])

    def test_invalid_name(self):
        """Проверить неправильное имя пакета."""
        with self.assertRaises(ValueError):
            self.load_data({"package1": ["B"]})

    def test_invalid_dependencies(self):
        """Проверить неправильный список зависимостей."""
        with self.assertRaises(ValueError):
            self.load_data({"A": "B"})

    def test_missing_file(self):
        """Проверить отсутствие файла."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            with self.assertRaises(ValueError):
                load_test_repository(path)


if __name__ == "__main__":
    unittest.main()
