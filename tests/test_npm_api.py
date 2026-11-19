import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from src.npm_api import get_dependencies


class TestNpmApi(unittest.TestCase):
    """Тесты получения зависимостей npm-пакетов."""

    @patch("src.npm_api.urlopen")
    def test_dependencies(self, mock_urlopen):
        """Проверить получение прямых зависимостей."""
        data = {
            "dependencies": {
                "accepts": "~1.3.8",
                "debug": "2.6.9"
            }
        }
        response = io.BytesIO(json.dumps(data).encode())
        mock_urlopen.return_value.__enter__.return_value = response

        result = get_dependencies(
            "https://registry.npmjs.org",
            "express",
            "4.18.2"
        )

        self.assertEqual(result, data["dependencies"])

    @patch("src.npm_api.urlopen")
    def test_no_dependencies(self, mock_urlopen):
        """Проверить пакет без зависимостей."""
        response = io.BytesIO(b"{}")
        mock_urlopen.return_value.__enter__.return_value = response

        result = get_dependencies(
            "https://registry.npmjs.org",
            "example",
            "1.0.0"
        )

        self.assertEqual(result, {})

    @patch("src.npm_api.urlopen")
    def test_http_error(self, mock_urlopen):
        """Проверить ошибку отсутствующего пакета."""
        mock_urlopen.side_effect = HTTPError(
            "https://registry.npmjs.org/example",
            404,
            "Not Found",
            None,
            None
        )

        with self.assertRaises(ValueError):
            get_dependencies(
                "https://registry.npmjs.org",
                "example",
                "999.0.0"
            )


if __name__ == "__main__":
    unittest.main()
