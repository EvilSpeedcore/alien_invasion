import math

import pygame
from pygame.sprite import Sprite

import find_angle as fa
from images import load_image


class BossBullet(Sprite):
    """Parent class, which represents bullet of the boss."""
    def __init__(self, ai_settings, screen):
        """Initialize bullet of the boss.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.

        """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = None
        self.rect = None

    def draw_bullet(self):
        """Draw bullet on screen."""
        self.screen.blit(self.image, self.rect)


class GreenBossBullet(BossBullet):
    """Child class, which represents bullet of green boss."""
    def __init__(self, ai_settings, screen, boss):
        """Initialize bullet of green boss.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Application window.
            :param boss: Instance of Boss class.

        """
        super(GreenBossBullet, self).__init__(ai_settings, screen)
        self.image = load_image('alien_bullet.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Bullet speed.
        self.speed_factor = ai_settings.green_boss_bullet_speed_factor

        # Angle of bullet direction.
        self.shooting_angle_up = None

        # Counter of bounces bullets make, when they collide with screen borders.
        self.bounces = 0

    def update(self):
        """Update bullet position."""
        angle = self.shooting_angle_up
        bullet_move_x = self.speed_factor * math.cos(math.radians(angle))
        bullet_move_y = -self.speed_factor * math.sin(math.radians(angle))
        self.x += bullet_move_x
        self.y += bullet_move_y
        self.rect.centery = self.y
        self.rect.centerx = self.x

    def change_direction(self, boss_bullets):
        """Change bullet direction after it reaching screen borders.

        Args:
            :param boss_bullets: Group of boss_bullets sprites.

        """
        if self.bounces > 3:
            boss_bullets.remove(self)
        elif self.rect.top <= 0:
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
    """Child class, which represents bullet of red boss."""
    def __init__(self, ai_settings, screen, boss):
        """Initialize bullet of red boss.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.
            :param boss: Instance of Boss class

        """
        super(RedBossBullet, self).__init__(ai_settings, screen)
        self.image = load_image('red_alien_bullet.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed_factor = ai_settings.red_boss_bullet_speed_factor
        self.ship_position = None
        self.shooting_angle_cos = None
        self.shooting_angle = None
        self.angles = (180, 360)

    def update(self):
        """Update bullet position."""
        if self.ship_position == "4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "1":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "3":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "4-1":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "2-3":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "1-2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        if self.ship_position == "3-4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x

    def define_angle(self, ship):
        """Define shooting angle of bullet depending on ship current position.

        Args:
            :param ship: Instance of Ship class.

        """
        ab = abs(self.y - ship.centery)
        ac = abs(self.x - ship.centerx)
        bc = math.sqrt(pow(ab, 2) + pow(ac, 2))
        self.shooting_angle_cos = ac / bc
        self.shooting_angle = fa.find_angle_with_cos(self.shooting_angle_cos)

    def define_position(self, ship):
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
    """Child class, which represents bullets of blue boss."""
    def __init__(self, ai_settings, screen, boss, angle):
        """Initialize bullet of blue boss.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.
            :param boss: Instance of Boss class.
            :param angle: Bullet shooting angle.

        """
        super(BlueBossBullet, self).__init__(ai_settings, screen)
        self.image = load_image('blue_alien_bullet.png')

        # Rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of boss.
        self.rect.centerx = boss.rect.centerx
        self.rect.centery = boss.rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed_factor = ai_settings.blue_boss_bullet_speed_factor
        self.angle = angle

    def update(self):
        """Update bullet position."""
        bullet_move_x = self.speed_factor * math.cos(math.radians(self.angle))
        bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angle))
        self.x += bullet_move_x
        self.y += bullet_move_y
        self.rect.centery = self.y
        self.rect.centerx = self.x
