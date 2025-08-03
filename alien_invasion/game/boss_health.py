from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.settings import Settings


class BossHealth(Sprite):
    """Parent class, which represents health and shield bar of boss."""

    IMAGE_DIR: str | None = None

    def __init__(self, settings: "Settings", screen: "Surface") -> None:
        """Initialize boss health."""
        super().__init__()
        self.settings = settings
        self.screen = screen

        # List, which will contain loaded images.
        self.hp_images = []

        # List for names of images in directory.
        self.hp_list = []

    def prepare_images(self) -> None:
        """Add loaded images to list."""
        for hp in self.hp_list:
            self.hp_images.append(load_image(f"{self.IMAGE_DIR}/{hp}"))


class GreenBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of green boss."""

    IMAGE_DIR = "green_boss_hp"

    def __init__(self, settings: "Settings", screen: "Surface") -> None:
        super().__init__(settings, screen)
        self.hp_list = ["1_hp.png", "2_hp.png", "3_hp.png", "4_hp.png", "5_hp.png",
                        "6_hp.png", "7_hp.png", "8_hp.png", "9_hp.png", "10_hp.png",
                        "1_shield.png", "2_shield.png", "3_shield.png", "4_shield.png", "5_shield.png",
                        "6_shield.png", "7_shield.png", "8_shield.png", "9_shield.png", "10_shield.png"]

        # Load of image, which represents health bar of undamaged boss.
        self.image = load_image(f"{self.IMAGE_DIR}/10_hp.png")

        # Rectangular area of the image.
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        # To make an dynamic health bar, we store several loaded images in list to iterate through it later.
        self.prepare_images()


class RedBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of red boss."""

    IMAGE_DIR = "red_boss_hp"

    def __init__(self, settings: "Settings", screen: "Surface") -> None:
        super().__init__(settings, screen)
        self.hp_list = ["1_hp.png", "2_hp.png", "3_hp.png", "4_hp.png", "5_hp.png",
                        "6_hp.png", "7_hp.png", "8_hp.png", "9_hp.png", "10_hp.png",
                        "1_shield.png", "2_shield.png", "3_shield.png", "4_shield.png", "5_shield.png"]
        self.image = load_image(f"{self.IMAGE_DIR}/10_hp.png")
        self.rect = self.image.get_rect()
        self.prepare_images()


class BlueBossHealth(BossHealth):
    """Child class of BossHealth class, which represents health and shield of blue boss."""

    IMAGE_DIR = "blue_boss_hp"

    def __init__(self, settings: "Settings", screen: "Surface") -> None:
        super().__init__(settings, screen)
        self.hp_list = ["1_hp.png", "2_hp.png", "3_hp.png", "4_hp.png", "5_hp.png",
                        "6_hp.png", "7_hp.png", "8_hp.png", "9_hp.png", "10_hp.png",
                        "1_shield.png", "2_shield.png", "3_shield.png", "4_shield.png", "5_shield.png",
                        "6_shield.png", "7_shield.png", "8_shield.png", "9_shield.png", "10_shield.png"]
        self.image = load_image(f"{self.IMAGE_DIR}/10_hp.png")
        self.rect = self.image.get_rect()
        self.prepare_images()
