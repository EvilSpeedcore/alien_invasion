import math
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.gf import direct_bullet
from game.images import load_image

if TYPE_CHECKING:
    from game.bosses import BlueBoss, GreenBoss, RedBoss
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


class BossBullet(Sprite):
    IMAGE = load_image("aliens/green_alien_bullet.png")

    def __init__(self, screen: "Screen") -> None:
        super().__init__()
        self.screen = screen
        self.image = self.IMAGE
        self.rect = self.image.get_rect()

    def blitme(self) -> None:
        """Draw bullet on screen."""
        self.screen.it.blit(self.image, self.rect)


class GreenBossBullet(BossBullet):

    def __init__(self, settings: "Settings", screen: "Screen", boss: "GreenBoss") -> None:
        super().__init__(screen)

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
        radians = math.radians(angle)
        bullet_move_x = self.speed * math.cos(radians)
        bullet_move_y = -self.speed * math.sin(radians)
        self.x += bullet_move_x  # type: ignore[assignment]
        self.y += bullet_move_y  # type: ignore[assignment]
        self.rect.centery = self.y
        self.rect.centerx = self.x

    def change_direction(self) -> None:
        """Change bullet direction after it reaching screen borders."""
        if (self.rect.top <= 0) or (self.rect.bottom > self.screen_rect.bottom):
            self.shooting_angle_up = 360 - self.shooting_angle_up
            self.bounces += 1
        elif self.rect.right > self.screen_rect.right:
            self.shooting_angle_up = abs(270 - self.shooting_angle_up) + 180
            self.bounces += 1
        elif self.rect.left < self.screen_rect.left:
            self.shooting_angle_up = 180 - self.shooting_angle_up
            self.bounces += 1


class RedBossBullet(BossBullet):
    IMAGE = load_image("aliens/red_alien_bullet.png")

    def __init__(self, settings: "Settings", screen: "Screen", boss: "RedBoss") -> None:
        super().__init__(screen=screen)

        self.screen_rect = self.screen.rect

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.speed = settings.red_boss_bullets_speed
        self.ship_position: direct_bullet.ShipToBulletPosition | None = None
        self.shooting_angle_cos = 0.0
        self.shooting_angle = 0.0

    def update(self) -> None:
        direct_bullet.update_direct_bullet(bullet=self)

    def define_position(self, ship: "Ship") -> None:
        direct_bullet.define_direct_bullet_position(bullet=self, ship=ship)


class BlueBossBullet(BossBullet):
    IMAGE = load_image("aliens/blue_alien_bullet.png")

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 boss: "BlueBoss",
                 angle: int) -> None:
        super().__init__(screen=screen)

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
        radians = math.radians(self.angle)
        bullet_move_x = self.speed * math.cos(radians)
        bullet_move_y = -self.speed * math.sin(radians)
        self.x += bullet_move_x  # type: ignore[assignment]
        self.y += bullet_move_y  # type: ignore[assignment]
        self.rect.centery = self.y
        self.rect.centerx = self.x
