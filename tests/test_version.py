"""Тесты получения версий npm-пакета."""

import io
import json
import unittest
from unittest.mock import patch

from src.npm_api import get_package_versions


class TestVersions(unittest.TestCase):
    """Проверки списка версий."""

    @patch("src.npm_api.urlopen")
    def test_get_versions(self, mock_urlopen):
        """Проверить получение опубликованных версий."""
        data = {
            "versions": {
                "1.0.0": {},
                "1.1.0": {},
                "2.0.0": {}
            }
        }
        response = io.BytesIO(json.dumps(data).encode())
        mock_urlopen.return_value.__enter__.return_value = response

        versions = get_package_versions(
            "https://registry.npmjs.org",
            "example"
        )

        self.assertEqual(
            versions,
            ["1.0.0", "1.1.0", "2.0.0"]
        )

    @patch("src.npm_api.urlopen")
    def test_missing_versions(self, mock_urlopen):
        """Проверить ответ без списка версий."""
        response = io.BytesIO(b"{}")
        mock_urlopen.return_value.__enter__.return_value = response

        with self.assertRaises(ValueError):
            get_package_versions(
                "https://registry.npmjs.org",
                "example"
            )


if __name__ == "__main__":
    unittest.main()
