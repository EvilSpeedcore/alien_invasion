import sys
from functools import cache
from pathlib import Path


class Paths:

    @staticmethod
    @cache
    def assets() -> Path:
        if getattr(sys, "frozen", False):
            base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(sys.executable).parent  # noqa: SLF001
            return base / "assets"

        base = Path(__file__).resolve().parent.parent
        return base / "assets"

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

    @staticmethod
    @cache
    def playbacks() -> Path:
        return Paths.assets() / "playbacks"

    @staticmethod
    @cache
    def logs() -> Path:
        path = Path(__file__).resolve().parent.parent / "logs"
        path.mkdir(parents=True, exist_ok=True)
        return path
