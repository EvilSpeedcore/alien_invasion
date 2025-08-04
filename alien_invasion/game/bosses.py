import random
from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.settings import Settings


class GreenBoss(Sprite):

    def __init__(self, screen: "Surface") -> None:
        super().__init__()
        self.image = load_image("green_alien.png")

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery

        # Boss hit points.
        self.hit_points = 10


class RedBoss(Sprite):

    def __init__(self, settings: "Settings", screen: "Surface") -> None:
        super().__init__()
        self.image = load_image("red_alien.png")

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Current position of bullet
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Boss position.
        self.position = "center"

        # Boss hit points.
        self.hit_points = 10

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
                    self.rect.centery = self.y
                    self.rect.centerx = self.x
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midleft"
                    self.define_direction_1()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centery = self.y
                    self.rect.centerx = self.x
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 4:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "midtop":
            if self.random_direction == 1:
                if self.rect.top < self.screen_rect.centery:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "topright"
                    self.define_direction_2()
        elif self.position == "midleft":
            if self.random_direction == 1:
                if self.rect.left < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "topleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
        elif self.position == "midbottom":
            if self.random_direction == 1:
                if self.rect.bottom > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.left > self.screen_rect.left + 150:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "bottomleft"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.right < self.screen_rect.right - 150:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "midright":
            if self.random_direction == 1:
                if self.rect.right > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "center"
                    self.define_start_direction()
            elif self.random_direction == 2:
                if self.rect.top > self.screen_rect.top + 150:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "topright"
                    self.define_direction_2()
            elif self.random_direction == 3:
                if self.rect.bottom < self.screen_rect.bottom - 150:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "bottomright"
                    self.define_direction_2()
        elif self.position == "topleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomleft":
            if self.random_direction == 1:
                if self.x < self.screen_rect.centerx:
                    self.x += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midleft"
                    self.define_direction_1()
        elif self.position == "bottomright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midbottom"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y > self.screen_rect.centery:
                    self.y -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midright"
                    self.define_direction_1()
        elif self.position == "topright":
            if self.random_direction == 1:
                if self.x > self.screen_rect.centerx:
                    self.x -= self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midtop"
                    self.define_direction_1()
            elif self.random_direction == 2:
                if self.y < self.screen_rect.centery:
                    self.y += self.speed_factor
                    self.rect.centerx = self.x
                    self.rect.centery = self.y
                else:
                    self.position = "midright"
                    self.define_direction_1()

    def define_start_direction(self) -> None:
        """Define start direction of boss: left, right, top and bottom."""
        self.random_direction = random.choice(range(1, 5))

    def define_direction_1(self) -> None:
        """Define direction of boss from following positions: midleft, midright, midtop and midbottom."""
        self.random_direction = random.choice(range(1, 4))

    def define_direction_2(self) -> None:
        """Define follow up direction of boss from following positions: topright, bottomright, bottomleft, topleft."""
        self.random_direction = random.choice(range(1, 3))


class BlueBoss(Sprite):

    def __init__(self, screen: "Surface") -> None:
        super().__init__()
        self.image = load_image("blue_alien.png")

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Boss hit points.
        self.hit_points = 10

        # Angles to manipulate shooting direction.
        self.shooting_angle = 0
        self.shooting_angles = [90, 180, 270]

        # Trigger, that defines clock direction of boss: clockwise, counter-clockwise.
        self.rt_trigger = True
