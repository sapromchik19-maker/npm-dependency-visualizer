"""Вывод графа зависимостей в виде ASCII-дерева."""

from src.plantuml import format_package


def to_ascii_tree(graph, root):
    """Построить ASCII-дерево без зацикливания."""
    lines = [format_package(root)]
    visited = {root}
    stack = [(root, "", iter(graph.get(root, [])))]

    while stack:
        package, prefix, children = stack[-1]
        remaining = list(children)

        if not remaining:
            stack.pop()
            continue

        dependency = remaining[0]
        stack[-1] = (package, prefix, iter(remaining[1:]))

        is_last = len(remaining) == 1
        branch = "`-- " if is_last else "|-- "
        name = format_package(dependency)

        if dependency in visited:
            lines.append(prefix + branch + name + " (повтор)")
            continue

        lines.append(prefix + branch + name)
        visited.add(dependency)

        extension = "    " if is_last else "|   "
        stack.append((
            dependency,
            prefix + extension,
            iter(graph.get(dependency, []))
        ))

    return "\n".join(lines)
