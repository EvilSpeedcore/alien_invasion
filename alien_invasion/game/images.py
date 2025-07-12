import pygame
from pygame import Surface

from game.paths import Paths


def load_image(relative_path: str) -> Surface:
    images = Paths.images()
    image = images.joinpath(relative_path)
    return pygame.image.load(image)
