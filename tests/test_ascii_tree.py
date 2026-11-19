"""Тесты вывода ASCII-дерева зависимостей."""

import unittest

from src.ascii_tree import to_ascii_tree


class TestAsciiTree(unittest.TestCase):
    """Проверки построения ASCII-дерева."""

    def test_simple_tree(self):
        """Проверить обычное дерево."""
        graph = {
            "A": ["B", "C"],
            "B": [],
            "C": []
        }

        result = to_ascii_tree(graph, "A")

        self.assertEqual(
            result,
            "A\n|-- B\n`-- C"
        )

    def test_shared_dependency(self):
        """Проверить повторяющуюся зависимость."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": []
        }

        result = to_ascii_tree(graph, "A")

        self.assertIn("D (повтор)", result)
        self.assertEqual(result.count("D"), 2)

    def test_cycle(self):
        """Проверить циклическую зависимость."""
        graph = {
            "A": ["B"],
            "B": ["A"]
        }

        result = to_ascii_tree(graph, "A")

        self.assertIn("A (повтор)", result)

    def test_no_dependencies(self):
        """Проверить пакет без зависимостей."""
        result = to_ascii_tree({"A": []}, "A")

        self.assertEqual(result, "A")

    def test_npm_packages(self):
        """Проверить имена npm-пакетов с версиями."""
        root = ("is-odd", "3.0.1")
        dependency = ("is-number", "6.0.0")
        graph = {
            root: [dependency],
            dependency: []
        }

        result = to_ascii_tree(graph, root)

        self.assertIn("is-odd@3.0.1", result)
        self.assertIn("is-number@6.0.0", result)


if __name__ == "__main__":
    unittest.main()
