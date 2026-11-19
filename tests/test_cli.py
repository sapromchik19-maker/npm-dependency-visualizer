import unittest
from argparse import Namespace

from src.main import validate_arguments


class TestArguments(unittest.TestCase):
    """Тесты параметров командной строки."""

    def setUp(self):
        """Создать корректные параметры для каждого теста."""
        self.args = Namespace(
            package="express",
            repository="https://registry.npmjs.org",
            version="4.18.2",
            output="graph.svg",
            test_mode=False,
            ascii=False
        )

    def test_valid_arguments(self):
        """Проверить корректные параметры."""
        validate_arguments(self.args)

    def test_invalid_url(self):
        """Проверить неправильный URL."""
        self.args.repository = "wrong_url"

        with self.assertRaises(ValueError):
            validate_arguments(self.args)

    def test_empty_package(self):
        """Проверить пустое имя пакета."""
        self.args.package = ""

        with self.assertRaises(ValueError):
            validate_arguments(self.args)

    def test_invalid_output(self):
        """Проверить неправильное расширение файла."""
        self.args.output = "graph.png"

        with self.assertRaises(ValueError):
            validate_arguments(self.args)

    def test_missing_test_file(self):
        """Проверить отсутствие тестового репозитория."""
        self.args.test_mode = True
        self.args.repository = "missing_repository.json"

        with self.assertRaises(ValueError):
            validate_arguments(self.args)


if __name__ == "__main__":
    unittest.main()
