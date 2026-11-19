"""Тесты построения графа зависимостей."""

import unittest

from src.graph import build_graph


class TestGraph(unittest.TestCase):
    """Проверки алгоритма BFS."""

    def test_simple_graph(self):
        """Проверить обычный граф."""
        data = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }

        graph = build_graph("A", lambda name: data[name])

        self.assertEqual(graph, data)

    def test_cycle(self):
        """Проверить граф с циклом."""
        data = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }

        graph = build_graph("A", lambda name: data[name])

        self.assertEqual(graph, data)

    def test_no_dependencies(self):
        """Проверить пакет без зависимостей."""
        data = {"A": []}

        graph = build_graph("A", lambda name: data[name])

        self.assertEqual(graph, data)

    def test_shared_dependency(self):
        """Проверить общую зависимость."""
        data = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": []
        }

        graph = build_graph("A", lambda name: data[name])

        self.assertEqual(graph, data)


if __name__ == "__main__":
    unittest.main()
