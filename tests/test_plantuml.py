"""Тесты генерации диаграмм PlantUML."""

import unittest

from src.plantuml import to_plantuml


class TestPlantUML(unittest.TestCase):
    """Проверки преобразования графа в PlantUML."""

    def test_simple_graph(self):
        """Проверить описание обычного графа."""
        graph = {
            "A": ["B"],
            "B": []
        }

        result = to_plantuml(graph)

        self.assertIn("@startuml", result)
        self.assertIn("@enduml", result)
        self.assertIn('rectangle "A" as node_0', result)
        self.assertIn('rectangle "B" as node_1', result)
        self.assertIn("node_0 --> node_1", result)

    def test_npm_packages(self):
        """Проверить имена npm-пакетов с версиями."""
        graph = {
            ("is-odd", "3.0.1"): [("is-number", "6.0.0")],
            ("is-number", "6.0.0"): []
        }

        result = to_plantuml(graph)

        self.assertIn("is-odd@3.0.1", result)
        self.assertIn("is-number@6.0.0", result)

    def test_empty_dependencies(self):
        """Проверить пакет без зависимостей."""
        result = to_plantuml({"A": []})

        self.assertIn('rectangle "A"', result)
        self.assertNotIn("-->", result)


if __name__ == "__main__":
    unittest.main()
