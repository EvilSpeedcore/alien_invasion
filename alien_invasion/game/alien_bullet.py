from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.gf import direct_bullet
from game.images import load_image

if TYPE_CHECKING:
    from pygame.rect import Rect

    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


class AlienBullet(Sprite):
    IMAGE = load_image("aliens/green_alien_bullet.png")

    def __init__(self, settings: "Settings", screen: "Screen", rect: "Rect") -> None:
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.rect

        self.image = self.IMAGE
        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of bullet.
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed = settings.alien_bullets_speed
        self.ship_position: direct_bullet.ShipToBulletPosition | None = None
        self.shooting_angle_cos = 0.0
        self.shooting_angle = 0.0

    def update(self) -> None:
        direct_bullet.update_direct_bullet(bullet=self)

    def blitme(self) -> None:
        """Draw alien bullet on screen."""
        self.screen.it.blit(self.image, self.rect)

    def define_position(self, ship: "Ship") -> None:
        """Define position of ship."""
        direct_bullet.define_direct_bullet_position(bullet=self, ship=ship)


class RedAlienBullet(AlienBullet):
    IMAGE = load_image("aliens/red_alien_bullet.png")


class BlueAlienBullet(AlienBullet):
    IMAGE = load_image("aliens/blue_alien_bullet.png")
