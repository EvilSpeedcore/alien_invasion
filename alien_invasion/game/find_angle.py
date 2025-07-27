import csv
from pathlib import Path

from game.paths import Paths


def find_angle_with_cos(value: float) -> float:
    """Find angle with cos value.

    Args:
        :param value: Cos value.

    Returns:
        :return: Angle.

    """
    return find_angle(Paths.math() / "cos.csv", value)


def find_angle_with_sin(value: float) -> float:
    """Find angle with sin value.

    Args:
        :param value: Sin value.

    Returns:
        :return: Angle.

    """
    return find_angle(Paths.math() / "sin.csv", value)


def find_angle(filepath: Path, value: float) -> float:
    data = {}
    with Path.open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            data[float(row[1])] = int(row[0])
    for x in sorted(data.keys()):
        if x > value:
            break
    return data[x]
