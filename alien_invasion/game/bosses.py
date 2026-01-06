import secrets
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.boss_health import BlueBossHealth, GreenBossHealth, RedBossHealth
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
        self.combined_health = health

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.screen_rect = screen.rect
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.set_default_health_points()

    def prepare_health(self) -> None:
        """Prepare to drawn green boss health."""
        self.combined_health.rotate()
        self.combined_health.rect.x, self.combined_health.rect.y = 500, 60

    def set_default_health_points(self) -> None:
        self.health_points = self.combined_health.hit_points

    def blitme(self) -> None:
        self.screen.it.blit(self.image, self.rect)


class GreenBoss(Boss):
    IMAGE = load_image("green_alien.png")

    def __init__(self, screen: "Screen") -> None:
        image = self.IMAGE
        health = GreenBossHealth()
        super().__init__(screen=screen, image=image, health=health)


class RedBoss(Boss):
    IMAGE = load_image("red_alien.png")

    def __init__(self, settings: "Settings", screen: "Screen") -> None:
        image = self.IMAGE
        health = RedBossHealth()
        super().__init__(screen=screen, image=image, health=health)

        # Current position of bullet
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Boss position.
        self.position = "center"

        # Boss speed.
        self.speed = settings.red_boss_speed
        self.define_start_direction()

    def move_up(self) -> None:
        self.y -= self.speed
        self.rect.centerx = self.x  # type: ignore[assignment]
        self.rect.centery = self.y  # type: ignore[assignment]

    def move_left(self) -> None:
        self.x -= self.speed
        self.rect.centerx = self.x  # type: ignore[assignment]
        self.rect.centery = self.y  # type: ignore[assignment]

    def move_down(self) -> None:
        self.y += self.speed
        self.rect.centerx = self.x  # type: ignore[assignment]
        self.rect.centery = self.y  # type: ignore[assignment]

    def move_right(self) -> None:
        self.x += self.speed
        self.rect.centerx = self.x  # type: ignore[assignment]
        self.rect.centery = self.y  # type: ignore[assignment]

    def update(self) -> None:
        """Update boss position depending on boss current position."""
        if self.position == "center":
            if self.random_direction == 1:
                if self.rect.top > self.screen_rect.top + 150:
                    self.move_up()
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.move_left()
                else:
                    self.position = "midleft"
                    self.define_direction_1()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.move_down()
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 4:
                if self.rect.right < self.screen_rect.right - 150:
                    self.move_right()
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "midtop":
            if self.random_direction == 1:
                if self.rect.top < self.screen_rect.centery:
                    self.move_down()
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.move_left()
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.move_right()
                else:
                    self.position = "topright"
                    self.define_direction_2()
        elif self.position == "midleft":
            if self.random_direction == 1:
                if self.rect.left < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.move_up()
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.move_down()
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
        elif self.position == "midbottom":
            if self.random_direction == 1:
                if self.rect.bottom > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.move_left()
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.move_right()
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "midright":
            if self.random_direction == 1:
                if self.rect.right > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.move_up()
                else:
                    self.position = "topright"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.move_down()
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "topleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.move_down()
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "topright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.move_down()
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
        health = BlueBossHealth()
        super().__init__(screen=screen, image=image, health=health)

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Angle to manipulate shooting direction.
        self.shooting_angle = 0

        # Trigger, that defines clock direction of boss: clockwise, counter-clockwise.
        self.rt_trigger = True
