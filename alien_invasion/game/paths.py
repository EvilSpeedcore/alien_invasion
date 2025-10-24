import sys
from functools import cache
from pathlib import Path


def is_compiled() -> bool:
    return "__compiled__" in globals()


class Paths:

    @staticmethod
    @cache
    def assets() -> Path:
        if is_compiled():
            return Path(sys.executable).parent / "assets"
        return Path(__file__).parent.parent / "assets"

    @staticmethod
    @cache
    def images() -> Path:
        return Paths.assets() / "images"

    @staticmethod
    @cache
    def effects() -> Path:
        return Paths.assets() / "effects"

    @staticmethod
    @cache
    def math() -> Path:
        return Paths.assets() / "math"
