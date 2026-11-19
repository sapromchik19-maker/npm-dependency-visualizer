"""Тесты порядка загрузки зависимостей."""

import unittest

from src.load_order import get_load_order


class TestLoadOrder(unittest.TestCase):
    """Проверки порядка загрузки."""

    def test_simple_graph(self):
        """Проверить порядок для обычного графа."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }

        order = get_load_order(graph)

        self.assertLess(order.index("D"), order.index("B"))
        self.assertLess(order.index("B"), order.index("A"))
        self.assertLess(order.index("C"), order.index("A"))

    def test_no_dependencies(self):
        """Проверить пакет без зависимостей."""
        graph = {"A": []}

        self.assertEqual(get_load_order(graph), ["A"])

    def test_cycle(self):
        """Проверить обнаружение цикла."""
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }

        with self.assertRaises(ValueError):
            get_load_order(graph)

    def test_shared_dependency(self):
        """Проверить общую зависимость."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": []
        }

        order = get_load_order(graph)

        self.assertLess(order.index("D"), order.index("B"))
        self.assertLess(order.index("D"), order.index("C"))
        self.assertEqual(order[-1], "A")


if __name__ == "__main__":
    unittest.main()
