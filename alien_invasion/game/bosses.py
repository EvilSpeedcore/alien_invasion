import secrets
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.boss_health import BlueBossHealth, GreenBossHealth, RedBossHealth
from game.images import load_image

if TYPE_CHECKING:
    from pygame.sprite import GroupSingle
    from pygame.surface import Surface

    from game.boss_health import BossHealthTypes
    from game.screen import Screen
    from game.settings import Settings


class Boss(Sprite):

    _HIT_POINTS = 0
    _HIT_POINTS_WITH_SHIELD = 0

    def __init__(self,
                 screen: "Screen",
                 boss_health: "GroupSingle",
                 image: "Surface",
                 health: "BossHealthTypes") -> None:
        super().__init__()
        self.boss_health = boss_health
        self.image = image
        self.health = health

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.screen_rect = screen.rect
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.set_default_hit_points()

    def prepare_health(self) -> None:
        """Prepare to drawn green boss health."""
        hp_image = self.health.hp_images[self.hit_points_with_shield]
        self.health.image = hp_image.copy()
        self.health.rect.x = 500
        self.health.rect.y = 60
        self.boss_health.add(self.health)

    def set_default_hit_points(self) -> None:
        self.hit_points = self._HIT_POINTS
        self.hit_points_with_shield = self._HIT_POINTS_WITH_SHIELD


class GreenBoss(Boss):

    # TODO: Join or calculate?
    _HIT_POINTS = 10
    _HIT_POINTS_WITH_SHIELD = 19

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 boss_health: "GroupSingle") -> None:
        # TODO: Load once?
        image = load_image("green_alien.png")
        health = GreenBossHealth(settings, screen)
        super().__init__(screen=screen, boss_health=boss_health, image=image, health=health)


class RedBoss(Boss):

    _HIT_POINTS = 10
    _HIT_POINTS_WITH_SHIELD = 14

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 boss_health: "GroupSingle") -> None:
        image = load_image("red_alien.png")
        health = RedBossHealth(settings, screen)
        super().__init__(screen=screen, boss_health=boss_health, image=image, health=health)

        # Current position of bullet
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Boss position.
        self.position = "center"

        # Boss speed.
        self.speed_factor = settings.red_boss_speed_factor
        self.moving_angle = None
        self.define_start_direction()

    def update(self) -> None:
        """Update boss position depending on boss current position."""
        if self.position == "center":
            if self.random_direction == 1:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed_factor
                    self.rect.centery = self.y  # type: ignore[assignment]
                    self.rect.centerx = self.x  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centery = self.y  # type: ignore[assignment]
                    self.rect.centerx = self.x  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 4:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "midtop":
            if self.random_direction == 1:
                if self.rect.top < self.screen_rect.centery:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topright"
                    self.define_direction_2()
        elif self.position == "midleft":
            if self.random_direction == 1:
                if self.rect.left < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
        elif self.position == "midbottom":
            if self.random_direction == 1:
                if self.rect.bottom > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "midright":
            if self.random_direction == 1:
                if self.rect.right > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "topright"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "topleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "topright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x  # type: ignore[assignment]
                    self.rect.centery = self.y  # type: ignore[assignment]
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed_factor
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

    _HIT_POINTS = 10
    _HIT_POINTS_WITH_SHIELD = 19

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 boss_health: "GroupSingle") -> None:
        image = load_image("blue_alien.png")
        health = BlueBossHealth(settings, screen)
        super().__init__(screen=screen, boss_health=boss_health, image=image, health=health)

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Angle to manipulate shooting direction.
        self.shooting_angle = 0

        # Trigger, that defines clock direction of boss: clockwise, counter-clockwise.
        self.rt_trigger = True
