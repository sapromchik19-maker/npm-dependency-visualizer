
"""Определение порядка загрузки зависимостей."""

from collections import deque


def build_dependents(graph):
    """Построить обратные связи между пакетами."""
    dependents = {package: set() for package in graph}

    for package, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in dependents:
                raise ValueError(
                    f"Неизвестная зависимость: {dependency}"
                )
            dependents[dependency].add(package)

    return dependents


def get_load_order(graph):
    """Вернуть порядок с зависимостями перед пакетами."""
    remaining = {
        package: len(set(dependencies))
        for package, dependencies in graph.items()
    }
    dependents = build_dependents(graph)
    queue = deque(
        package for package, count in remaining.items()
        if count == 0
    )
    order = []

    while queue:
        package = queue.popleft()
        order.append(package)

        for dependent in sorted(dependents[package]):
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(graph):
        raise ValueError(
            "Обнаружен цикл: порядок загрузки определить нельзя"
        )

    return order
