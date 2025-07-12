import csv

from game.paths import Paths


def find_angle_with_cos(value: float) -> float:
    """Find angle with cos value.

    Args:
        :param value: Cos value.

    Returns:
        :return: Angle.

    """
    cos_values = []
    cos = {}
    with open(Paths.math() / 'cos.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            cos[float(row[1])] = int(row[0])
            cos_values.append(float(row[1]))
    for x in sorted(cos_values):
        if x > value:
            break
    return cos[x]


def find_angle_with_sin(value: float) -> float:
    """FInd angle with sin value.

    Args:
        :param value: Sin value.

    Returns:
        :return: Angle.

    """
    sin_values = []
    sin = {}
    with open(Paths.math() / 'sin.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            sin[float(row[1])] = int(row[0])
            sin_values.append(float(row[1]))
    for x in sin_values:
        if x > value:
            break
    return sin[x]
