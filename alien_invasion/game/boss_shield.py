from pygame.sprite import Sprite

from game.images import load_image


class BossShield(Sprite):

    def __init__(self, settings, screen, boss) -> None:
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.boss = boss
        self.spawned_boss_shield = None
        self.rect = None

    def draw_boss_shield(self) -> None:
        """Draw boss shield on screen."""
        self.screen.blit(self.spawned_boss_shield, self.rect)


class GreenBossShield(BossShield):

    def __init__(self, settings, screen, boss) -> None:
        super().__init__(settings, screen, boss)
        self.spawned_boss_shield = load_image("spawned_green_boss_shield.png")
        # Get the rectangular area of the image.
        self.rect = self.spawned_boss_shield.get_rect()

        # Set starting position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Save shield position.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Shield hit points.
        self.points = 10


class RedBossShield(BossShield):

    def __init__(self, settings, screen, boss) -> None:
        super().__init__(settings, screen, boss)
        self.spawned_boss_shield = load_image("spawned_red_boss_shield.png")
        # Get the rectangular area of the image.
        self.rect = self.spawned_boss_shield.get_rect()

        # Set starting position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Save shield position.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Shield hit points.
        self.points = 5

    def update(self) -> None:
        """Update position shield depending on boss current position."""
        self.x = self.boss.x
        self.rect.centerx = self.x
        self.y = self.boss.y
        self.rect.centery = self.y


class BlueBossShield(BossShield):

    def __init__(self, settings, screen, boss) -> None:
        super().__init__(settings, screen, boss)
        self.spawned_boss_shield = load_image("spawned_blue_boss_shield.png")
        # Get the rectangular area of the image.
        self.rect = self.spawned_boss_shield.get_rect()

        # Set position of shield.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current shield position .
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Shield hit points.
        self.points = 10

    def update(self) -> None:
        """Update position shield depending on boss current position."""
        self.x = self.boss.x
        self.rect.centerx = self.x
        self.y = self.boss.y
        self.rect.centery = self.y
