import subprocess
import sys
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from src.main import main, validate_arguments


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
        """Проверить порядок без настоящего PlantUML."""
        arguments = [
            "src.main",
            "--package", "A",
            "--repository", "data/acyclic_graph.json",
            "--version", "1.0.0",
            "--output", "graph.svg",
            "--test-mode",
            "--load-order"
        ]
        output = StringIO()

        with patch.object(sys, "argv", arguments):
            with patch("src.main.save_graph_image") as mock_svg:
                with redirect_stdout(output):
                    main()

        text = output.getvalue()
        self.assertIn("Порядок загрузки:", text)
        self.assertIn("D -> E -> B -> C -> A", text)
        mock_svg.assert_called_once()


if __name__ == "__main__":
    unittest.main()
