from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.bosses import BlueBoss, GreenBoss, RedBoss
    from game.screen import Screen


class BossShield(Sprite):

    def __init__(self, screen: "Screen", shield: "Surface") -> None:
        super().__init__()
        self.screen = screen
        self.shield = shield
        self.rect = shield.get_rect()

    def draw_boss_shield(self) -> None:
        """Draw boss shield on screen."""
        self.screen.it.blit(self.shield, self.rect)


class GreenBossShield(BossShield):

    def __init__(self, screen: "Screen", boss: "GreenBoss") -> None:
        shield = load_image("spawned_green_boss_shield.png")
        super().__init__(screen=screen, shield=shield)
        self.boss = boss

        # Set starting position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Save shield position.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Shield hit points.
        self.points = 10


class RedBossShield(BossShield):

    def __init__(self, screen: "Screen", boss: "RedBoss") -> None:
        shield = load_image("spawned_red_boss_shield.png")
        super().__init__(screen=screen, shield=shield)
        self.boss = boss

        # Set starting position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Save shield position.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Shield hit points.
        self.points = 5

    def update(self) -> None:
        """Update position shield depending on boss current position."""
        self.x = self.boss.x  # type: ignore[assignment]
        self.rect.centerx = self.x
        self.y = self.boss.y  # type: ignore[assignment]
        self.rect.centery = self.y


class BlueBossShield(BossShield):

    def __init__(self, screen: "Screen", boss: "BlueBoss") -> None:
        shield = load_image("spawned_blue_boss_shield.png")
        super().__init__(screen=screen, shield=shield)
        self.boss = boss

        # Set position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current shield position.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Shield hit points.
        self.points = 10

    def update(self) -> None:
        """Update position shield depending on boss current position."""
        self.x = self.boss.x  # type: ignore[assignment]
        self.rect.centerx = self.x
        self.y = self.boss.y  # type: ignore[assignment]
        self.rect.centery = self.y
