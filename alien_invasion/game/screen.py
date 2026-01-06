from enum import Enum, auto

import pygame


class ScreenSide(Enum):
    TOP = auto()
    RIGHT = auto()
    LEFT = auto()
    BOTTOM = auto()
    CENTER = auto()
    TOP_RIGHT = auto()
    TOP_LEFT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()


class Screen:

    def __init__(self, width: int, height: int) -> None:
        self.it = pygame.display.set_mode((width, height))
        self.rect = self.it.get_rect()
