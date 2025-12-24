from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.bosses import BlueBoss, RedBoss
    from game.screen import Screen


class BossShield(Sprite):

    def __init__(self,
                 screen: "Screen",
                 image: "Surface",
                 position: tuple[int, int]) -> None:
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = image.get_rect()

        # Set position of shield.
        self.rect.centerx, self.rect.centery = position

        # Save shield position.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Shield health points.
        self.health_points = 0

    def draw_boss_shield(self) -> None:
        """Draw boss shield on screen."""
        self.screen.it.blit(self.image, self.rect)


class MovingBossShield(BossShield):

    def __init__(self, screen: "Screen", image: "Surface", boss: "BlueBoss | RedBoss") -> None:
        super().__init__(screen=screen,
                         image=image,
                         position=(boss.rect.centerx, boss.rect.centery))
        self.boss = boss

    def update(self) -> None:
        """Update position shield depending on boss current position."""
        self.x = self.boss.x  # type: ignore[assignment]
        self.rect.centerx = self.x
        self.y = self.boss.y  # type: ignore[assignment]
        self.rect.centery = self.y


class GreenBossShield(BossShield):
    IMAGE = load_image("spawned_green_boss_shield.png")

    def __init__(self, screen: "Screen", position: tuple[int, int]) -> None:
        super().__init__(screen=screen, image=self.IMAGE, position=position)


class RedBossShield(MovingBossShield):
    IMAGE = load_image("spawned_red_boss_shield.png")

    def __init__(self, screen: "Screen", boss: "RedBoss") -> None:
        super().__init__(screen=screen, image=self.IMAGE, boss=boss)


class BlueBossShield(MovingBossShield):
    IMAGE = load_image("spawned_blue_boss_shield.png")

    def __init__(self, screen: "Screen", boss: "BlueBoss") -> None:
        super().__init__(screen=screen, image=self.IMAGE, boss=boss)
