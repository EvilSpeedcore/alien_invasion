from typing import TYPE_CHECKING, ClassVar, TypeAlias, Union

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface


BossHealthTypes: TypeAlias = Union["BlueBossHealth", "GreenBossHealth", "RedBossHealth"]  # noqa: UP040


class GreenBossHealth(Sprite):
    IMAGE_NAMES: tuple[str, ...] = (
        *(f"{index}_hp.png" for index in range(1, 11)),
        *(f"{index}_shield.png" for index in range(1, 11)),
    )
    IMAGES: ClassVar[list["Surface"]] = [load_image(f"green_boss_hp/{name}") for name in IMAGE_NAMES]
    INITIAL_IMAGE: "Surface" = load_image("green_boss_hp/10_hp.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE  # undamaged
        self.rect = self.image.get_rect()


class RedBossHealth(Sprite):
    IMAGE_NAMES: tuple[str, ...] = (
        *(f"{index}_hp.png" for index in range(1, 11)),
        *(f"{index}_shield.png" for index in range(1, 6)),
    )
    IMAGES: ClassVar[list["Surface"]] = [load_image(f"red_boss_hp/{name}") for name in IMAGE_NAMES]
    INITIAL_IMAGE: "Surface" = load_image("red_boss_hp/10_hp.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE  # undamaged
        self.rect = self.image.get_rect()


class BlueBossHealth(Sprite):
    IMAGE_NAMES: tuple[str, ...] = (
        *(f"{index}_hp.png" for index in range(1, 11)),
        *(f"{index}_shield.png" for index in range(1, 11)),
    )
    IMAGES: ClassVar[list["Surface"]] = [load_image(f"blue_boss_hp/{name}") for name in IMAGE_NAMES]
    INITIAL_IMAGE: "Surface" = load_image("blue_boss_hp/10_hp.png")

    def __init__(self) -> None:
        super().__init__()
        self.image = self.INITIAL_IMAGE  # undamaged
        self.rect = self.image.get_rect()
