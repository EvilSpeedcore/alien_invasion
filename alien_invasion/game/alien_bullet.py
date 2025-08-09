import math
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

import game.find_angle as fa
from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.alien import Alien
    from game.settings import Settings
    from game.ship import Ship


class AlienBullet(Sprite):
    """Class, which represent bullets of alien ships."""

    def __init__(self, settings: "Settings", screen: "Surface", alien: "Alien") -> None:
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image load for different bullets.
        # TODO: Split by color
        self.image = load_image("alien_bullet.png")
        self.red_bullet = load_image("red_alien_bullet.png")
        self.blue_bullet = load_image("blue_alien_bullet.png")

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of bullet.
        self.rect.centerx = alien.rect.centerx
        self.rect.centery = alien.rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed_factor = settings.alien_bullet_speed_factor  # Bullet speed.
        self.ship_position = ""
        self.shooting_angle_cos = 0.0
        self.shooting_angle = 0.0
        self.angles = (180, 360)

    def update(self) -> None:
        """Update position of bullets depending on ship current position."""
        if self.ship_position == "4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "1":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "3":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x  # type: ignore[assignment]
            self.rect.centery = self.y  # type: ignore[assignment]
        elif self.ship_position == "4-1":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "2-3":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "1-2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]
        elif self.ship_position == "3-4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y  # type: ignore[assignment]
            self.rect.centerx = self.x  # type: ignore[assignment]

    def draw_alien_bullet(self) -> None:
        """Draw alien bullet on screen."""
        self.screen.blit(self.image, self.rect)

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
            self.define_angle(ship)
        elif self.x < ship.centerx and self.y > ship.centery:
            self.ship_position = "1"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y > ship.centery:
            self.ship_position = "2"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y < ship.centery:
            self.ship_position = "3"
            self.define_angle(ship)
        elif self.x < ship.centerx and self.y == ship.centery:
            self.ship_position = "4-1"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y == ship.centery:
            self.ship_position = "2-3"
            self.define_angle(ship)
        elif self.x == ship.centerx and self.y > ship.centery:
            self.ship_position = "1-2"
            self.define_angle(ship)
        elif self.x == ship.centerx and self.y < ship.centery:
            self.ship_position = "3-4"
            self.define_angle(ship)
