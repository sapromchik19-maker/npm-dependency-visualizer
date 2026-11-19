"""Построение графа зависимостей алгоритмом BFS."""

from collections import deque


def build_graph(start_package, get_neighbors):
    """Построить граф зависимостей без рекурсии."""
    graph = {}
    visited = set()
    queue = deque([start_package])

    while queue:
        package = queue.popleft()

        if package in visited:
            continue

        visited.add(package)

        dependencies = get_neighbors(package)
        graph[package] = list(dependencies)

        for dependency in dependencies:
            if dependency not in visited:
                queue.append(dependency)

    return graph
