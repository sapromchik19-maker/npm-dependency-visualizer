import subprocess
import sys
import unittest
from argparse import Namespace

from src.main import validate_arguments


class TestArguments(unittest.TestCase):
    """Тесты параметров командной строки."""

    def setUp(self):
        """Создать корректные параметры для тестов."""
        self.args = Namespace(
            package="express",
            repository="https://registry.npmjs.org",
            version="4.18.2",
            output="graph.svg",
            test_mode=False,
            ascii=False,
            load_order=False
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
        """Проверить отсутствие тестового файла."""
        self.args.test_mode = True
        self.args.repository = "missing_repository.json"

        with self.assertRaises(ValueError):
            validate_arguments(self.args)

    def test_invalid_load_order_argument(self):
        """Проверить лишнее значение флага."""
        result = subprocess.run(
            [
                sys.executable, "-m", "src.main",
                "--package", "A",
                "--repository", "data/acyclic_graph.json",
                "--version", "1.0.0",
                "--output", "graph.svg",
                "--test-mode", "--load-order", "wrong"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized arguments", result.stderr)

    def test_missing_output_argument(self):
        """Проверить отсутствие обязательного параметра."""
        result = subprocess.run(
            [
                sys.executable, "-m", "src.main",
                "--package", "A",
                "--repository", "data/acyclic_graph.json",
                "--version", "1.0.0",
                "--test-mode", "--load-order"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--output", result.stderr)


    def test_successful_load_order(self):
        """Проверить успешный вывод порядка загрузки."""
        result = subprocess.run(
            [
                sys.executable, "-m", "src.main",
                "--package", "A",
                "--repository", "data/acyclic_graph.json",
                "--version", "1.0.0",
                "--output", "graph.svg",
                "--test-mode", "--load-order"
            ],
            capture_output=True,
            text=True,
            check=False
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Порядок загрузки:", result.stdout)
        self.assertIn("D -> E -> B -> C -> A", result.stdout)

if __name__ == "__main__":
    unittest.main()