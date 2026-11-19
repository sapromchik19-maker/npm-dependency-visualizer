"""Чтение тестового репозитория зависимостей."""

import json
import re
from pathlib import Path


def load_test_repository(file_path):
    """Загрузить и проверить граф из JSON-файла."""
    try:
        with Path(file_path).open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Ошибка чтения тестового репозитория: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError("Тестовый репозиторий должен быть объектом JSON")

    for package, dependencies in data.items():
        if not isinstance(package, str) or not re.fullmatch(
            r"[A-Z]+", package
        ):
            raise ValueError("Имена пакетов должны состоять из A-Z")

        if not isinstance(dependencies, list):
            raise ValueError("Зависимости должны быть списком")

        for dependency in dependencies:
            if not isinstance(dependency, str) or not re.fullmatch(
                r"[A-Z]+", dependency
            ):
                raise ValueError("Некорректное имя зависимости")

    all_packages = set(data)
    for dependencies in data.values():
        all_packages.update(dependencies)

    return {
        package: data.get(package, [])
        for package in all_packages
    }
