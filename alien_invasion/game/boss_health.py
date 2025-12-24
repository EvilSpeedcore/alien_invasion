from collections import UserList, deque
from typing import TYPE_CHECKING, TypeAlias, Union

from pygame.image import load
from pygame.sprite import Sprite

from game.paths import Paths

if TYPE_CHECKING:
    from pygame.surface import Surface


BossHealthTypes: TypeAlias = Union["BlueBossHealth", "GreenBossHealth", "RedBossHealth"]  # noqa: UP040


def load_sequential_from_dirs(*directories: str) -> list["Surface"]:
    result: list[Surface] = []
    for name in directories:
        directory = Paths.images() / name
        images = (image for image in directory.glob("*.png"))
        result.extend(load(image) for image in sorted(images, key=lambda image: int(image.stem)))
    return result


class BossHudHealth(UserList):

    def __init__(self, images: list["Surface"]) -> None:
        super().__init__(images)


class BossHudShield(BossHudHealth):
    pass


class GreenBossHealth(Sprite):
    HUD_HEALTH = BossHudHealth(load_sequential_from_dirs("green_boss_hp"))
    HUD_SHIELD = BossHudShield(load_sequential_from_dirs("green_boss_shield"))

    def __init__(self) -> None:
        super().__init__()
        self.hud_health = self.HUD_HEALTH
        self.hud_shield = self.HUD_SHIELD
        self.images = deque(self.hud_health + self.hud_shield)
        self.image: Surface = self.hud_health[-1]
        self.rect = self.image.get_rect()
        self.hit_points = len(self.hud_health) + len(self.hud_shield)

    def rotate(self) -> None:
        image = self.images[-1]
        self.images.rotate()
        self.image = image


class RedBossHealth(GreenBossHealth):
    HUD_HEALTH = BossHudHealth(load_sequential_from_dirs("red_boss_hp"))
    HUD_SHIELD = BossHudShield(load_sequential_from_dirs("red_boss_shield"))


class BlueBossHealth(GreenBossHealth):
    HUD_HEALTH = BossHudHealth(load_sequential_from_dirs("blue_boss_hp"))
    HUD_SHIELD = BossHudShield(load_sequential_from_dirs("blue_boss_shield"))
