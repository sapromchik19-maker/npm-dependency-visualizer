"""Тесты выбора версий пакетов."""

import unittest

from src.semver import resolve_version, version_matches


class TestSemver(unittest.TestCase):
    """Проверки диапазонов версий."""

    def test_exact_version(self):
        """Проверить точную версию."""
        self.assertTrue(
            version_matches("1.2.3", "1.2.3")
        )
        self.assertFalse(
            version_matches("1.2.4", "1.2.3")
        )

    def test_caret(self):
        """Проверить диапазон с ^."""
        self.assertTrue(
            version_matches("1.9.0", "^1.2.3")
        )
        self.assertFalse(
            version_matches("2.0.0", "^1.2.3")
        )

    def test_tilde(self):
        """Проверить диапазон с ~."""
        self.assertTrue(
            version_matches("1.3.9", "~1.3.8")
        )
        self.assertFalse(
            version_matches("1.4.0", "~1.3.8")
        )

    def test_resolve(self):
        """Проверить выбор подходящей версии."""
        versions = [
            "1.3.8",
            "1.3.9",
            "1.4.0",
            "2.0.0"
        ]

        result = resolve_version(versions, "~1.3.8")

        self.assertEqual(result, "1.3.9")

    def test_no_match(self):
        """Проверить отсутствие подходящей версии."""
        with self.assertRaises(ValueError):
            resolve_version(["1.0.0"], "^2.0.0")


if __name__ == "__main__":
    unittest.main()
