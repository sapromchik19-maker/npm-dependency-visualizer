"""Консольное приложение для визуализации npm-зависимостей."""

import argparse
from pathlib import Path
from urllib.parse import urlparse

from src.ascii_tree import to_ascii_tree
from src.graph import build_graph
from src.load_order import get_load_order
from src.npm_graph import build_npm_graph
from src.plantuml import to_plantuml
from src.svg_renderer import render_svg
from src.test_repository import load_test_repository


def validate_arguments(args):
    """Проверить параметры командной строки."""
    if not args.package.strip():
        raise ValueError("Имя пакета не может быть пустым")
    if not args.version.strip():
        raise ValueError("Версия пакета не может быть пустой")
    if not args.output.lower().endswith(".svg"):
        raise ValueError("Файл должен иметь расширение .svg")

    if args.test_mode:
        if not Path(args.repository).is_file():
            raise ValueError("Тестовый файл не найден")
    else:
        parsed = urlparse(args.repository)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("Некорректный URL репозитория")


def parse_arguments():
    """Прочитать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор зависимостей npm"
    )
    parser.add_argument("--package", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--load-order", action="store_true")
    return parser.parse_args()


def save_graph_image(graph, output_file):
    """Сохранить граф зависимостей в SVG."""
    plantuml_text = to_plantuml(graph)
    try:
        path = render_svg(plantuml_text, output_file)
    except ValueError as error:
        print(f"Ошибка создания SVG: {error}")
        raise SystemExit(1) from error

    print(f"SVG-граф сохранён: {path}")


def print_test_graph(graph):
    """Вывести зависимости тестового репозитория."""
    print("Граф зависимостей:")
    for package, dependencies in graph.items():
        names = ", ".join(dependencies)
        print(f"{package}: {names or '(нет зависимостей)'}")


def print_npm_graph(graph):
    """Вывести зависимости npm-пакетов."""
    print("Полный граф npm-зависимостей:")
    for package, dependencies in graph.items():
        name, version = package
        print(f"\n{name}@{version}")
        if not dependencies:
            print("  (нет зависимостей)")
        for dep_name, dep_version in dependencies:
            print(f"  -> {dep_name}@{dep_version}")


def print_load_order(graph, test_mode):
    """Вывести топологический порядок зависимостей."""
    try:
        order = get_load_order(graph)
    except ValueError as error:
        print(f"Ошибка порядка загрузки: {error}")
        return

    print("\nПорядок загрузки:")
    if test_mode:
        print(" -> ".join(order))
    else:
        for index, (name, version) in enumerate(order, 1):
            print(f"{index}. {name}@{version}")


def get_test_graph(args):
    """Получить граф из тестового JSON-репозитория."""
    repository = load_test_repository(args.repository)
    if args.package not in repository:
        raise ValueError(f"Пакет {args.package} не найден")

    return build_graph(
        args.package,
        lambda name: repository[name]
    )


def main():
    """Запустить анализ и визуализацию зависимостей."""
    args = parse_arguments()
    try:
        validate_arguments(args)
        if args.test_mode:
            graph = get_test_graph(args)
        else:
            graph = build_npm_graph(
                args.repository, args.package, args.version
            )
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error

    if args.test_mode:
        print_test_graph(graph)
    else:
        print_npm_graph(graph)

    if args.load_order:
        print_load_order(graph, args.test_mode)

    if args.ascii:
        root = args.package
        if not args.test_mode:
            root = (args.package, args.version)
        print("\nASCII-дерево зависимостей:")
        print(to_ascii_tree(graph, root))

    save_graph_image(graph, args.output)


if __name__ == "__main__":
    main()
