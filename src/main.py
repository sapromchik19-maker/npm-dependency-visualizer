import argparse
from pathlib import Path
from urllib.parse import urlparse
from src.npm_api import get_dependencies

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

    args = parser.parse_args()
    try:
        validate_arguments(args)
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error


    if args.test_mode:
        print("Тестовый режим будет реализован на этапе 3.")
        return

    try:
        dependencies = get_dependencies(
            args.repository,
            args.package,
            args.version
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error

    print(f"Прямые зависимости {args.package}@{args.version}:")

    if not dependencies:
        print("Прямые зависимости отсутствуют.")
        return

    for name, version in sorted(dependencies.items()):
        print(f"{name}: {version}")



if __name__ == "__main__":
    main()
