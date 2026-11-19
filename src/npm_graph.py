"""Построение графа реальных npm-зависимостей."""

from src.graph import build_graph
from src.npm_api import get_dependencies, get_package_versions
from src.semver import resolve_version


def build_npm_graph(repository, package, version):
    """Построить граф npm-зависимостей алгоритмом BFS."""
    versions_cache = {}
    dependencies_cache = {}

    def get_neighbors(node):
        """Получить зависимости конкретной версии пакета."""
        name, current_version = node

        if node not in dependencies_cache:
            dependencies_cache[node] = get_dependencies(
                repository,
                name,
                current_version
            )

        dependencies = dependencies_cache[node]
        neighbors = []

        for dependency, requirement in dependencies.items():
            if dependency not in versions_cache:
                versions_cache[dependency] = get_package_versions(
                    repository,
                    dependency
                )

            selected = resolve_version(
                versions_cache[dependency],
                requirement
            )
            neighbors.append((dependency, selected))

        return neighbors

    return build_graph((package, version), get_neighbors)
