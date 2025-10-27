from typing import TYPE_CHECKING, ClassVar, TypeAlias, Union

from pygame.image import load
from pygame.sprite import Sprite

from game.images import load_image
from game.paths import Paths

if TYPE_CHECKING:
    from pygame.surface import Surface


BossHealthTypes: TypeAlias = Union["BlueBossHealth", "GreenBossHealth", "RedBossHealth"]  # noqa: UP040


def load_from_dirs(*directories: str) -> list["Surface"]:
    result: list[Surface] = []
    for name in directories:
        directory = Paths.images() / name
        images = (image for image in directory.glob("*.png"))
        result.extend(load(image) for image in sorted(images, key=lambda image: int(image.stem)))
    return result


class GreenBossHealth(Sprite):
    IMAGES: ClassVar[list["Surface"]] = load_from_dirs("green_boss_hp", "green_boss_shield")
    INITIAL_IMAGE = load_image("green_boss_hp/10.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE
        self.rect = self.image.get_rect()


class RedBossHealth(Sprite):
    IMAGES: ClassVar[list["Surface"]] = load_from_dirs("red_boss_hp", "red_boss_shield")
    INITIAL_IMAGE = load_image("red_boss_hp/10.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE
        self.rect = self.image.get_rect()


class BlueBossHealth(Sprite):
    IMAGES: ClassVar[list["Surface"]] = load_from_dirs("blue_boss_hp", "blue_boss_shield")
    INITIAL_IMAGE = load_image("blue_boss_hp/10.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE
        self.rect = self.image.get_rect()
