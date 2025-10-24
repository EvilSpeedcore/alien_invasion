import math
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

import game.find_angle as fa
from game.images import load_image

if TYPE_CHECKING:
    from pygame.rect import Rect

    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


class AlienBullet(Sprite):
    """Class, which represent bullets of alien ships."""

    _IMAGE = load_image("alien_bullet.png")

    def __init__(self, settings: "Settings", screen: "Screen", rect: "Rect") -> None:
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.rect

        self.image = self._IMAGE
        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of bullet.
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed = settings.alien_bullets_speed
        self.ship_position = ""
        self.shooting_angle_cos = 0.0
        self.shooting_angle = 0.0
        self.angles = (180, 360)

    def update(self) -> None:
        """Update position of bullets depending on ship current position."""
        if self.ship_position == "4":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "1":
            bullet_move_x = self.speed * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "2":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "3":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "4-1":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "2-3":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "1-2":
            bullet_move_x = self.speed * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "3-4":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]

    def blitme(self) -> None:
        """Draw alien bullet on screen."""
        self.screen.it.blit(self.image, self.rect)

    def define_angle(self, ship: "Ship") -> None:
        """Define direction of bullet."""
        ab = abs(self.y - ship.centery)
        ac = abs(self.x - ship.centerx)
        bc = math.sqrt(pow(ab, 2) + pow(ac, 2))
        self.shooting_angle_cos = ac / bc
        self.shooting_angle = fa.find_angle_with_cos(self.shooting_angle_cos)

    def define_position(self, ship: "Ship") -> None:
        """Define position of ship."""
        if self.x < ship.centerx and self.y < ship.centery:
            self.ship_position = "4"
        elif self.x < ship.centerx and self.y > ship.centery:
            self.ship_position = "1"
        elif self.x > ship.centerx and self.y > ship.centery:
            self.ship_position = "2"
        elif self.x > ship.centerx and self.y < ship.centery:
            self.ship_position = "3"
        elif self.x < ship.centerx and self.y == ship.centery:
            self.ship_position = "4-1"
        elif self.x > ship.centerx and self.y == ship.centery:
            self.ship_position = "2-3"
        elif self.x == ship.centerx and self.y > ship.centery:
            self.ship_position = "1-2"
        elif self.x == ship.centerx and self.y < ship.centery:
            self.ship_position = "3-4"
        else:
            raise AssertionError
        self.define_angle(ship)

class RedAlienBullet(AlienBullet):
    _IMAGE = load_image("red_alien_bullet.png")


class BlueAlienBullet(AlienBullet):
    _IMAGE = load_image("blue_alien_bullet.png")
