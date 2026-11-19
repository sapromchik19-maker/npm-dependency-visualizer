"""Генерация описания графа зависимостей PlantUML."""


def format_package(package):
    """Получить текстовое имя вершины графа."""
    if isinstance(package, tuple):
        name, version = package
        return f"{name}@{version}"

    return str(package)


def to_plantuml(graph):
    """Преобразовать граф зависимостей в PlantUML."""
    nodes = list(graph)
    identifiers = {
        package: f"node_{index}"
        for index, package in enumerate(nodes)
    }

    lines = [
        "@startuml",
        "left to right direction"
    ]

    for package in nodes:
        label = format_package(package)
        escaped = label.replace('"', '\\"')
        identifier = identifiers[package]
        lines.append(f'rectangle "{escaped}" as {identifier}')

    for package, dependencies in graph.items():
        for dependency in dependencies:
            source = identifiers[package]
            target = identifiers[dependency]
            lines.append(f"{source} --> {target}")

    lines.append("@enduml")

    return "\n".join(lines)
