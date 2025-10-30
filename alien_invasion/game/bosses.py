import secrets
from collections import deque
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.boss_health import BlueBossHudHealth, GreenBossHudHealth, RedBossHudHealth
from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.boss_health import BossHealthTypes
    from game.screen import Screen
    from game.settings import Settings


class Boss(Sprite):
    def __init__(self,
                 screen: "Screen",
                 image: "Surface",
                 health: "BossHealthTypes") -> None:
        super().__init__()
        self.screen = screen
        self.image = image
        self.health = health
        self.images = deque(health.IMAGES)

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.screen_rect = screen.rect
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.set_default_health_points()

    def prepare_health(self) -> None:
        """Prepare to drawn green boss health."""
        image = self.images[-1]
        self.images.rotate()
        self.health.image = image
        self.health.rect.x = 500
        self.health.rect.y = 60

    def set_default_health_points(self) -> None:
        self.health_points = len(self.health.IMAGES)

    def blitme(self) -> None:
        self.screen.it.blit(self.image, self.rect)


class GreenBoss(Boss):
    IMAGE = load_image("green_alien.png")

    def __init__(self, screen: "Screen") -> None:
        image = self.IMAGE
        health = GreenBossHudHealth()
        super().__init__(screen=screen, image=image, health=health)


class RedBoss(Boss):
    IMAGE = load_image("red_alien.png")

    def __init__(self, settings: "Settings", screen: "Screen") -> None:
        image = self.IMAGE
        health = RedBossHudHealth()
        super().__init__(screen=screen, image=image, health=health)

        # Current position of bullet
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Boss position.
        self.position = "center"

        # Boss speed.
        self.speed = settings.red_boss_speed
        self.moving_angle = None
        self.define_start_direction()

    def update(self) -> None:
        """Update boss position depending on boss current position."""
        if self.position == "center":
            if self.random_direction == 1:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed
                    self.rect.centery = self.y  # type: ignore[assignment]
                    self.rect.centerx = self.x  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed
                    self.rect.centery = self.y  # type: ignore[assignment]
                    self.rect.centerx = self.x  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 4:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "midtop":
            if self.random_direction == 1:
                if self.rect.top < self.screen_rect.centery:
                    self.y += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topright"
                    self.define_direction_2()
        elif self.position == "midleft":
            if self.random_direction == 1:
                if self.rect.left < self.screen_rect.centerx:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
        elif self.position == "midbottom":
            if self.random_direction == 1:
                if self.rect.bottom > self.screen_rect.centery:
                    self.y -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "midright":
            if self.random_direction == 1:
                if self.rect.right > self.screen_rect.centerx:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topright"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "topleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "topright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midright"
                    self.define_direction_1()

    def define_start_direction(self) -> None:
        """Define start direction of boss: left, right, top and bottom."""
        self.random_direction = secrets.choice(range(1, 5))

    def define_direction_1(self) -> None:
        """Define direction of boss from following positions: midleft, midright, midtop and midbottom."""
        self.random_direction = secrets.choice(range(1, 4))

    def define_direction_2(self) -> None:
        """Define follow up direction of boss from following positions: topright, bottomright, bottomleft, topleft."""
        self.random_direction = secrets.choice(range(1, 3))


class BlueBoss(Boss):
    IMAGE = load_image("blue_alien.png")

    def __init__(self, screen: "Screen") -> None:
        image = self.IMAGE
        health = BlueBossHudHealth()
        super().__init__(screen=screen, image=image, health=health)

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Angle to manipulate shooting direction.
        self.shooting_angle = 0

        # Trigger, that defines clock direction of boss: clockwise, counter-clockwise.
        self.rt_trigger = True
