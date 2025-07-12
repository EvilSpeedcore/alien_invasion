from functools import cache
from pathlib import Path


class Paths:

    @staticmethod
    @cache
    def assets() -> Path:
        return Path(__file__).parent.parent / 'assets'

    @staticmethod
    @cache
    def images() -> Path:
        return Paths.assets() / 'images'

    @staticmethod
    @cache
    def effects() -> Path:
        return Paths.assets() / 'effects'

    @staticmethod
    @cache
    def math() -> Path:
        return Paths.assets() / 'math'
