"""Получение прямых зависимостей из npm Registry."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen


def get_dependencies(repository, package, version):
    """Получить зависимости конкретной версии npm-пакета."""
    package_path = quote(package, safe="@")
    version_path = quote(version, safe="")
    url = (
        f"{repository.rstrip('/')}/"
        f"{package_path}/{version_path}"
    )

    try:
        with urlopen(url, timeout=10) as response:
            data = json.load(response)
    except HTTPError as error:
        raise ValueError(
            f"Ошибка HTTP {error.code}: пакет или версия не найдены"
        ) from error
    except URLError as error:
        raise ValueError(
            f"Не удалось подключиться к репозиторию: {error.reason}"
        ) from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Не удалось прочитать ответ репозитория: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError("Некорректный ответ npm Registry")

    dependencies = data.get("dependencies", {})

    if not isinstance(dependencies, dict):
        raise ValueError("Некорректный формат зависимостей")

    return dependencies


def get_package_versions(repository, package):
    """Получить список опубликованных версий npm-пакета."""
    package_path = quote(package, safe="@")
    url = f"{repository.rstrip('/')}/{package_path}"

    try:
        with urlopen(url, timeout=10) as response:
            data = json.load(response)
    except HTTPError as error:
        raise ValueError(
            f"Ошибка HTTP {error.code} при получении версий"
        ) from error
    except (URLError, OSError, ValueError) as error:
        raise ValueError(
            f"Не удалось получить версии: {error}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError("Некорректный ответ npm Registry")

    versions = data.get("versions")

    if not isinstance(versions, dict):
        raise ValueError("Список версий отсутствует")

    return list(versions)
