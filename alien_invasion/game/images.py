import pygame
from pygame import Surface

from game.paths import Paths


def load_image(relative_path: str) -> Surface:
    images = Paths.images()
    image = images.joinpath(relative_path)
    return pygame.image.load(image)


def load_sequential_from_dirs(*directories: str) -> list["Surface"]:
    result: list[Surface] = []
    for name in directories:
        directory = Paths.images() / name
        images = (image for image in directory.glob("*.png"))
        result.extend(pygame.image.load(image) for image in sorted(images, key=lambda image: int(image.stem)))
    return result
