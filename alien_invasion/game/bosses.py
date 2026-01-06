import secrets
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.boss_health import BlueBossHealth, GreenBossHealth, RedBossHealth
from game.images import load_image
from game.screen import ScreenSide as Side

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
        self.position: Side = Side.CENTER

        # Boss speed.
        self.speed = settings.red_boss_speed
        self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM)
        self.movement_margin = 150

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
        if self.position == Side.CENTER:
            if self.direction == Side.TOP:
                if self.rect.top > self.screen_rect.top + self.movement_margin:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT)
            elif self.direction == Side.LEFT:
                if self.rect.left > self.screen_rect.left + self.movement_margin:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT)
            elif self.direction == Side.BOTTOM:
                if self.rect.bottom < self.screen_rect.bottom - self.movement_margin:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT)
            elif self.direction == Side.RIGHT:
                if self.rect.right < self.screen_rect.right - self.movement_margin:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT)
        elif self.position == Side.TOP:
            if self.direction == Side.CENTER:
                if self.rect.top < self.screen_rect.centery:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP_LEFT, Side.BOTTOM)
            elif self.direction == Side.TOP_LEFT:
                if self.rect.left > self.screen_rect.left + self.movement_margin:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.TOP)
            elif self.direction == Side.TOP_RIGHT:
                if self.rect.right < self.screen_rect.right - self.movement_margin:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.TOP, Side.RIGHT)
        elif self.position == Side.LEFT:
            if self.direction == Side.CENTER:
                if self.rect.left < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM)
            elif self.direction == Side.TOP_LEFT:
                if self.rect.top > self.screen_rect.top + self.movement_margin:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.TOP)
            elif self.direction == Side.BOTTOM_LEFT:
                if self.rect.bottom < self.screen_rect.bottom - self.movement_margin:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side. BOTTOM)
        elif self.position == Side.BOTTOM:
            if self.direction == Side.CENTER:
                if self.rect.bottom > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM)
            elif self.direction == Side.BOTTOM_LEFT:
                if self.rect.left > self.screen_rect.left + self.movement_margin:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.BOTTOM)
            elif self.direction == Side.BOTTOM_RIGHT:
                if self.rect.right < self.screen_rect.right - self.movement_margin:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.RIGHT, Side.BOTTOM)
        elif self.position == Side.RIGHT:
            if self.direction == Side.CENTER:
                if self.rect.right > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM)
            elif self.direction == Side.TOP_RIGHT:
                if self.rect.top > self.screen_rect.top + self.movement_margin:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.RIGHT, Side.TOP)
            elif self.direction == Side.BOTTOM_RIGHT:
                if self.rect.bottom < self.screen_rect.bottom - self.movement_margin:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.RIGHT, Side.BOTTOM)
        elif self.position == Side.TOP_LEFT:
            if self.direction == Side.TOP:
                if self.x < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT)
            elif self.direction == Side.LEFT:
                if self.y < self.screen_rect.centery:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT)
        elif self.position == Side.BOTTOM_LEFT:
            if self.direction == Side.BOTTOM:
                if self.x < self.screen_rect.centerx:
                    self.move_right()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT)
            elif self.direction == Side.LEFT:
                if self.y > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT)
        elif self.position == Side.BOTTOM_RIGHT:
            if self.direction == Side.BOTTOM:
                if self.x > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT)
            elif self.direction == Side.RIGHT:
                if self.y > self.screen_rect.centery:
                    self.move_up()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT)
        elif self.position == Side.TOP_RIGHT:
            if self.direction == Side.TOP:
                if self.x > self.screen_rect.centerx:
                    self.move_left()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT)
            elif self.direction == Side.RIGHT:
                if self.y < self.screen_rect.centery:
                    self.move_down()
                else:
                    self.position = self.direction
                    self.define_direction(Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT)

    def define_direction(self, *sides: Side) -> None:
        self.direction = secrets.choice(sides)


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
