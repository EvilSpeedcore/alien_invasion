import random

from pygame.sprite import Sprite

from game.images import load_image


class Boss(Sprite):
    """Parent class, which represents bosses."""
    def __init__(self, ai_settings, screen):
        """Initialize boss.

        Args:
            :param ai_settings: Instance of Settings class
            :param screen: Application window.

        """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()


class GreenBoss(Boss):
    """Child class, which represents green boss."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.image = load_image('green_alien.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Boss hit points.
        self.hit_points = 10


class RedBoss(Boss):
    """Child class, which represents red boss."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.image = load_image('red_alien.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
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
        self.speed_factor = ai_settings.red_boss_speed_factor
        self.moving_angle = None
        self.define_start_direction()

    def update(self):
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

    def define_start_direction(self):
        """Define start direction of boss: left, right, top and bottom"""
        self.random_direction = random.choice([x for x in range(1, 5)])

    def define_direction_1(self):
        """Define direction of boss from following positions: midleft, midright, midtop and midbottom"""
        self.random_direction = random.choice([x for x in range(1, 4)])

    def define_direction_2(self):
        """Define follow up direction of boss from following positions: topright, bottomright, bottomleft, topleft."""
        self.random_direction = random.choice([x for x in range(1, 3)])


class BlueBoss(Boss):
    """Child class, which represents blue boss."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.image = load_image('blue_alien.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

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
