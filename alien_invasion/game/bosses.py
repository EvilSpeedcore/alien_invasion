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
    IMAGE = load_image("aliens/green_alien.png")

    def __init__(self, screen: "Screen") -> None:
        image = self.IMAGE
        health = GreenBossHealth()
        super().__init__(screen=screen, image=image, health=health)


class RedBoss(Boss):
    IMAGE = load_image("aliens/red_alien.png")

    def __init__(self, settings: "Settings", screen: "Screen") -> None:
        image = self.IMAGE
        health = RedBossHealth()
        super().__init__(screen=screen, image=image, health=health)

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.position: Side = Side.CENTER
        self.define_direction(Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM)

        self.speed = settings.red_boss_speed
        self.margin = 150

        # TODO: Sometimes boss gets stuck in the center
        self.movement_map = {
            (Side.CENTER, Side.TOP): (
                lambda: self.rect.top > self.screen_rect.top + self.margin,
                self.go_up,
                (Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT),
            ),
            (Side.CENTER, Side.LEFT): (
                lambda: self.rect.left > self.screen_rect.left + self.margin,
                self.go_left,
                (Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT),
            ),
            (Side.CENTER, Side.BOTTOM): (
                lambda: self.rect.bottom < self.screen_rect.bottom - self.margin,
                self.go_down,
                (Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT),
            ),
            (Side.CENTER, Side.RIGHT): (
                lambda: self.rect.right < self.screen_rect.right - self.margin,
                self.go_right,
                (Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT),
            ),
            (Side.TOP, Side.CENTER): (
                lambda: self.rect.top < self.screen_rect.centery,
                self.go_down,
                (Side.LEFT, Side.RIGHT, Side.TOP_LEFT, Side.BOTTOM),
            ),
            (Side.TOP, Side.TOP_LEFT): (
                lambda: self.rect.left > self.screen_rect.left + self.margin,
                self.go_left,
                (Side.LEFT, Side.TOP),
            ),
            (Side.TOP, Side.TOP_RIGHT): (
                lambda: self.rect.right < self.screen_rect.right - self.margin,
                self.go_right,
                (Side.TOP, Side.RIGHT),
            ),
            (Side.LEFT, Side.CENTER): (
                lambda: self.rect.left < self.screen_rect.centerx,
                self.go_right,
                (Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM),
            ),
            (Side.LEFT, Side.TOP_LEFT): (
                lambda: self.rect.top > self.screen_rect.top + self.margin,
                self.go_up,
                (Side.LEFT, Side.TOP),
            ),
            (Side.LEFT, Side.BOTTOM_LEFT): (
                lambda: self.rect.bottom < self.screen_rect.bottom - self.margin,
                self.go_down,
                (Side.LEFT, Side.BOTTOM),
            ),
            (Side.BOTTOM, Side.CENTER): (
                lambda: self.rect.bottom > self.screen_rect.centery,
                self.go_up,
                (Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM),
            ),
            (Side.BOTTOM, Side.BOTTOM_LEFT): (
                lambda: self.rect.left > self.screen_rect.left + self.margin,
                self.go_left,
                (Side.LEFT, Side.BOTTOM),
            ),
            (Side.BOTTOM, Side.BOTTOM_RIGHT): (
                lambda: self.rect.right < self.screen_rect.right - self.margin,
                self.go_right,
                (Side.RIGHT, Side.BOTTOM),
            ),
            (Side.RIGHT, Side.CENTER): (
                lambda: self.rect.right > self.screen_rect.centerx,
                self.go_left,
                (Side.LEFT, Side.RIGHT, Side.TOP, Side.BOTTOM),
            ),
            (Side.RIGHT, Side.TOP_RIGHT): (
                lambda: self.rect.top > self.screen_rect.top + self.margin,
                self.go_up,
                (Side.RIGHT, Side.TOP),
            ),
            (Side.RIGHT, Side.BOTTOM_RIGHT): (
                lambda: self.rect.bottom < self.screen_rect.bottom - self.margin,
                self.go_down,
                (Side.RIGHT, Side.BOTTOM),
            ),
            (Side.TOP_LEFT, Side.TOP): (
                lambda: self.x < self.screen_rect.centerx,
                self.go_right,
                (Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT),
            ),
            (Side.TOP_LEFT, Side.LEFT): (
                lambda: self.y < self.screen_rect.centery,
                self.go_down,
                (Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT),
            ),
            (Side.BOTTOM_LEFT, Side.BOTTOM): (
                lambda: self.x < self.screen_rect.centerx,
                self.go_right,
                (Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT),
            ),
            (Side.BOTTOM_LEFT, Side.LEFT): (
                lambda: self.y > self.screen_rect.centery,
                self.go_up,
                (Side.CENTER, Side.TOP_LEFT, Side.BOTTOM_LEFT),
            ),
            (Side.BOTTOM_RIGHT, Side.BOTTOM): (
                lambda: self.x > self.screen_rect.centerx,
                self.go_left,
                (Side.CENTER, Side.BOTTOM_LEFT, Side.BOTTOM_RIGHT),
            ),
            (Side.BOTTOM_RIGHT, Side.RIGHT): (
                lambda: self.y > self.screen_rect.centery,
                self.go_up,
                (Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT),
            ),
            (Side.TOP_RIGHT, Side.TOP): (
                lambda: self.x > self.screen_rect.centerx,
                self.go_left,
                (Side.CENTER, Side.TOP_LEFT, Side.TOP_RIGHT),
            ),
            (Side.TOP_RIGHT, Side.RIGHT): (
                lambda: self.y < self.screen_rect.centery,
                self.go_down,
                (Side.CENTER, Side.TOP_RIGHT, Side.BOTTOM_RIGHT),
            ),
        }

    def update_coordinates(self) -> None:
        self.rect.centerx = self.x  # type: ignore[assignment]
        self.rect.centery = self.y  # type: ignore[assignment]

    def go_up(self) -> None:
        self.y -= self.speed
        self.update_coordinates()

    def go_left(self) -> None:
        self.x -= self.speed
        self.update_coordinates()

    def go_down(self) -> None:
        self.y += self.speed
        self.update_coordinates()

    def go_right(self) -> None:
        self.x += self.speed
        self.update_coordinates()

    def update(self) -> None:
        action = self.movement_map.get((self.position, self.direction))
        if not action:
            return

        condition, move_function, next_directions = action
        if condition():
            move_function()
        else:
            self.position = self.direction
            self.define_direction(*next_directions)

    def define_direction(self, *sides: Side) -> None:
        self.direction = secrets.choice(sides)


class BlueBoss(Boss):
    IMAGE = load_image("aliens/blue_alien.png")

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
