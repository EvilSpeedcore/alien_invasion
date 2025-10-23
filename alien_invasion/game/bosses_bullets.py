import math
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

import game.find_angle as fa
from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.bosses import BlueBoss, GreenBoss, RedBoss
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


class BossBullet(Sprite):

    def __init__(self, screen: "Screen", image: "Surface") -> None:
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = image.get_rect()

    def blitme(self) -> None:
        """Draw bullet on screen."""
        self.screen.it.blit(self.image, self.rect)


class GreenBossBullet(BossBullet):

    def __init__(self, settings: "Settings", screen: "Screen", boss: "GreenBoss") -> None:
        image = load_image("alien_bullet.png")
        super().__init__(screen, image=image)

        self.screen_rect = self.screen.rect

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Bullet speed.
        self.speed = settings.green_boss_bullets_speed

        # Angle of bullet direction.
        self.shooting_angle_up = 0

        # Counter of bounces bullets make, when they collide with screen borders.
        self.bounces = 0

    def update(self) -> None:
        """Update bullet position."""
        angle = self.shooting_angle_up
        bullet_move_x = self.speed * math.cos(math.radians(angle))
        bullet_move_y = -self.speed * math.sin(math.radians(angle))
        self.x += bullet_move_x  # type: ignore[assignment]
        self.y += bullet_move_y  # type: ignore[assignment]
        self.rect.centery = self.y
        self.rect.centerx = self.x

    def change_direction(self) -> None:
        """Change bullet direction after it reaching screen borders."""
        if self.rect.top <= 0:
            self.shooting_angle_up = 360 - self.shooting_angle_up
            self.bounces += 1
        elif self.rect.right > self.screen_rect.right:
            self.shooting_angle_up = abs(270 - self.shooting_angle_up) + 180
            self.bounces += 1
        elif self.rect.left < self.screen_rect.left:
            self.shooting_angle_up = 180 - self.shooting_angle_up
            self.bounces += 1
        elif self.rect.bottom > self.screen_rect.bottom:
            self.shooting_angle_up = 360 - self.shooting_angle_up
            self.bounces += 1


class RedBossBullet(BossBullet):

    def __init__(self, settings: "Settings", screen: "Screen", boss: "RedBoss") -> None:
        image = load_image("red_alien_bullet.png")
        super().__init__(screen=screen, image=image)

        self.screen_rect = self.screen.rect

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.speed = settings.red_boss_bullets_speed
        self.ship_position = ""
        self.shooting_angle_cos = 0.0
        self.shooting_angle = 0.0
        self.angles = (180, 360)

    def update(self) -> None:
        """Update bullet position."""
        if self.ship_position == "4":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "1":
            bullet_move_x = self.speed * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "2":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "3":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "4-1":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "2-3":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "1-2":
            bullet_move_x = self.speed * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x
        if self.ship_position == "3-4":
            bullet_move_x = self.speed * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x  # type: ignore[assignment]
            self.y += bullet_move_y  # type: ignore[assignment]
            self.rect.centery = self.y
            self.rect.centerx = self.x

    def define_angle(self, ship: "Ship") -> None:
        """Define shooting angle of bullet depending on ship current position.

        Args:
            :param ship: Instance of Ship class.

        """
        ab = abs(self.y - ship.centery)
        ac = abs(self.x - ship.centerx)
        bc = math.sqrt(pow(ab, 2) + pow(ac, 2))
        self.shooting_angle_cos = ac / bc
        self.shooting_angle = fa.find_angle_with_cos(self.shooting_angle_cos)

    def define_position(self, ship: "Ship") -> None:
        """Define ship position relatively bullet position."""
        if self.x < ship.centerx and self.y < ship.centery:
            self.ship_position = "4"
            self.define_angle(ship)
        if self.x < ship.centerx and self.y > ship.centery:
            self.ship_position = "1"
            self.define_angle(ship)
        if self.x > ship.centerx and self.y > ship.centery:
            self.ship_position = "2"
            self.define_angle(ship)
        if self.x > ship.centerx and self.y < ship.centery:
            self.ship_position = "3"
            self.define_angle(ship)
        if self.x < ship.centerx and self.y == ship.centery:
            self.ship_position = "4-1"
            self.define_angle(ship)
        if self.x > ship.centerx and self.y == ship.centery:
            self.ship_position = "2-3"
            self.define_angle(ship)
        if self.x == ship.centerx and self.y > ship.centery:
            self.ship_position = "1-2"
            self.define_angle(ship)
        if self.x == ship.centerx and self.y < ship.centery:
            self.ship_position = "3-4"
            self.define_angle(ship)


class BlueBossBullet(BossBullet):

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 boss: "BlueBoss",
                 angle: int) -> None:
        image = load_image("blue_alien_bullet.png")
        super().__init__(screen=screen, image=image)

        self.screen_rect = self.screen.rect

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.speed = settings.blue_boss_bullets_speed
        self.angle = angle

    def update(self) -> None:
        """Update bullet position."""
        bullet_move_x = self.speed * math.cos(math.radians(self.angle))
        bullet_move_y = -self.speed * math.sin(math.radians(self.angle))
        self.x += bullet_move_x  # type: ignore[assignment]
        self.y += bullet_move_y  # type: ignore[assignment]
        self.rect.centery = self.y
        self.rect.centerx = self.x
