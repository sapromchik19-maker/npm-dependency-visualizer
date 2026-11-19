"""Чтение тестового репозитория зависимостей."""

import json
import re
from pathlib import Path


def read_repository(file_path):
    """Прочитать JSON-файл тестового репозитория."""
    try:
        with Path(file_path).open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Ошибка чтения тестового репозитория: {error}"
        ) from error


def is_valid_name(name):
    """Проверить имя пакета: только заглавные буквы A-Z."""
    return (
        isinstance(name, str)
        and re.fullmatch(r"[A-Z]+", name) is not None
    )


def validate_repository(data):
    """Проверить структуру тестового репозитория."""
    if not isinstance(data, dict):
        raise ValueError(
            "Тестовый репозиторий должен быть объектом JSON"
        )

    for package, dependencies in data.items():
        if not is_valid_name(package):
            raise ValueError(
                "Имена пакетов должны состоять из A-Z"
            )

        if not isinstance(dependencies, list):
            raise ValueError(
                "Зависимости должны быть списком"
            )

        for dependency in dependencies:
            if not is_valid_name(dependency):
                raise ValueError(
                    "Некорректное имя зависимости"
                )


def load_test_repository(file_path):
    """Загрузить и проверить граф из JSON-файла."""
    data = read_repository(file_path)
    validate_repository(data)

    all_packages = set(data)
    for dependencies in data.values():
        all_packages.update(dependencies)

    return {
        package: data.get(package, [])
        for package in all_packages
    }
