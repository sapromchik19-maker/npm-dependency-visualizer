"""Тесты графа реальных npm-зависимостей."""

import unittest
from unittest.mock import patch

from src.npm_graph import build_npm_graph


class TestNpmGraph(unittest.TestCase):
    """Проверки построения npm-графа."""

    @patch("src.npm_graph.get_package_versions")
    @patch("src.npm_graph.get_dependencies")
    def test_transitive_dependencies(self, mock_deps, mock_versions):
        """Проверить транзитивные зависимости."""
        packages = {
            ("A", "1.0.0"): {"B": "^1.0.0"},
            ("B", "1.2.0"): {"C": "~2.0.0"},
            ("C", "2.0.1"): {}
        }
        versions = {
            "B": ["1.0.0", "1.2.0", "2.0.0"],
            "C": ["2.0.0", "2.0.1", "2.1.0"]
        }

        mock_deps.side_effect = (
            lambda repository, name, version:
            packages[(name, version)]
        )
        mock_versions.side_effect = (
            lambda repository, name: versions[name]
        )

        graph = build_npm_graph(
            "https://registry.npmjs.org",
            "A",
            "1.0.0"
        )

        self.assertEqual(
            graph[("A", "1.0.0")],
            [("B", "1.2.0")]
        )
        self.assertEqual(
            graph[("B", "1.2.0")],
            [("C", "2.0.1")]
        )
        self.assertEqual(graph[("C", "2.0.1")], [])

    @patch("src.npm_graph.get_dependencies")
    def test_empty_graph(self, mock_deps):
        """Проверить пакет без зависимостей."""
        mock_deps.return_value = {}

        graph = build_npm_graph(
            "https://registry.npmjs.org",
            "A",
            "1.0.0"
        )

        self.assertEqual(graph, {("A", "1.0.0"): []})


if __name__ == "__main__":
    unittest.main()
