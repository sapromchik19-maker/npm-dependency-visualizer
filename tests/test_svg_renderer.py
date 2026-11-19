"""Тесты создания SVG-изображений."""

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.svg_renderer import render_svg


class TestSvgRenderer(unittest.TestCase):
    """Проверки генератора SVG."""

    def test_missing_jar(self):
        """Проверить отсутствие PlantUML."""
        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / "missing.jar"

            with self.assertRaises(ValueError):
                render_svg(
                    "@startuml\nA --> B\n@enduml",
                    "graph.svg",
                    jar_path=jar
                )

    @patch("src.svg_renderer.subprocess.run")
    def test_successful_render(self, mock_run):
        """Проверить успешное сохранение SVG."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="<svg></svg>",
            stderr=""
        )

        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / "plantuml.jar"
            jar.touch()
            output = Path(directory) / "graph.svg"

            result = render_svg(
                "@startuml\nA --> B\n@enduml",
                output,
                jar_path=jar
            )

            self.assertTrue(result.is_file())
            self.assertEqual(
                result.read_text(encoding="utf-8"),
                "<svg></svg>"
            )

    @patch("src.svg_renderer.subprocess.run")
    def test_invalid_svg(self, mock_run):
        """Проверить некорректный ответ PlantUML."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="invalid response",
            stderr=""
        )

        with tempfile.TemporaryDirectory() as directory:
            jar = Path(directory) / "plantuml.jar"
            jar.touch()
            output = Path(directory) / "graph.svg"

            with self.assertRaises(ValueError):
                render_svg(
                    "@startuml\nA --> B\n@enduml",
                    output,
                    jar_path=jar
                )


if __name__ == "__main__":
    unittest.main()
