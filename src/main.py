import argparse
from pathlib import Path
from urllib.parse import urlparse
from src.graph import build_graph
from src.test_repository import load_test_repository
from src.npm_graph import build_npm_graph
from src.load_order import get_load_order

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


def main():
    """Получить и вывести параметры программы."""
    parser = argparse.ArgumentParser(
        description="Визуализатор зависимостей npm"
    )

    parser.add_argument("--package", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--ascii", action="store_true")

    parser.add_argument(
        "--load-order",
        action="store_true",
        help="Вывести порядок загрузки зависимостей"
    )
    args = parser.parse_args()
    try:
        validate_arguments(args)
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error



    if args.test_mode:
        try:
            repository = load_test_repository(args.repository)

            if args.package not in repository:
                raise ValueError(
                    f"Пакет {args.package} не найден"
                )

            graph = build_graph(
                args.package,
                lambda name: repository[name]
            )
        except ValueError as error:
            print(f"Ошибка: {error}")
            raise SystemExit(1) from error


        print("Граф зависимостей:")

        for package, dependencies in graph.items():
            names = ", ".join(dependencies)
            print(f"{package}: {names or '(нет зависимостей)'}")

        if args.load_order:
            try:
                order = get_load_order(graph)
                print("\nПорядок загрузки:")
                print(" -> ".join(order))
            except ValueError as error:
                print(f"\nОшибка порядка загрузки: {error}")

        return




    try:
        graph = build_npm_graph(
            args.repository,
            args.package,
            args.version
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error

    print("Полный граф npm-зависимостей:")

    for package, dependencies in graph.items():
        name, version = package

        print(f"\n{name}@{version}")

        if not dependencies:
            print("  (нет зависимостей)")

        for dep_name, dep_version in dependencies:
            print(f"  -> {dep_name}@{dep_version}")

    if args.load_order:
        try:
            order = get_load_order(graph)

            print("\nПорядок загрузки зависимостей:")

            for index, (name, version) in enumerate(order, 1):
                print(f"{index}. {name}@{version}")

        except ValueError as error:
            print(f"Ошибка порядка загрузки: {error}")


if __name__ == "__main__":
    main()
