"""Упрощённое разрешение версий npm-пакетов."""

import re


VERSION_PATTERN = re.compile(
    r"^(\d+)\.(\d+)\.(\d+)$"
)


def parse_version(version):
    """Преобразовать версию в кортеж чисел."""
    match = VERSION_PATTERN.fullmatch(version)

    if not match:
        raise ValueError(f"Неподдерживаемая версия: {version}")

    return tuple(int(part) for part in match.groups())


def version_matches(version, requirement):
    """Проверить соответствие версии условию."""
    current = parse_version(version)

    if requirement.startswith("^"):
        minimum = parse_version(requirement[1:])
        major, minor, patch = minimum

        if major > 0:
            maximum = (major + 1, 0, 0)
        elif minor > 0:
            maximum = (0, minor + 1, 0)
        else:
            maximum = (0, 0, patch + 1)

        return minimum <= current < maximum

    if requirement.startswith("~"):
        minimum = parse_version(requirement[1:])
        major, minor, _ = minimum
        maximum = (major, minor + 1, 0)

        return minimum <= current < maximum

    return current == parse_version(requirement)


def resolve_version(versions, requirement):
    """Выбрать максимальную подходящую версию."""
    matches = []

    for version in versions:
        try:
            if version_matches(version, requirement):
                matches.append(version)
        except ValueError:
            continue

    if not matches:
        raise ValueError(
            f"Не найдена версия для условия {requirement}"
        )

    return max(matches, key=parse_version)
