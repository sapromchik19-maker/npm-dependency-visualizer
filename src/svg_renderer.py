"""Создание SVG-изображений с помощью PlantUML."""

import subprocess
from pathlib import Path


def render_svg(plantuml_text, output_file, jar_path="plantuml.jar"):
    """Сгенерировать SVG из текста диаграммы PlantUML."""
    jar = Path(jar_path)

    if not jar.is_file():
        raise ValueError(
            f"Файл PlantUML не найден: {jar_path}"
        )

    try:
        result = subprocess.run(
            ["java", "-jar", str(jar), "-tsvg", "-pipe"],
            input=plantuml_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=60
        )
    except FileNotFoundError as error:
        raise ValueError("Java не найдена в PATH") from error
    except subprocess.TimeoutExpired as error:
        raise ValueError("Превышено время ожидания PlantUML") from error
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"Ошибка PlantUML: {error.stderr}"
        ) from error

    if "<svg" not in result.stdout:
        raise ValueError("PlantUML не вернул SVG-изображение")

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.stdout, encoding="utf-8")

    return path
