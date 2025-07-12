import math

from pygame.sprite import Sprite

import game.find_angle as fa
from game.images import load_image


class AlienBullet(Sprite):
    """Class, which represent bullets of alien ships."""
    
    def __init__(self, ai_settings, screen, alien):
        """Initialize alien bullet.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.
            :param alien: Instance of Aliens class.

        """
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Image load for different bullets.
        self.image = load_image('alien_bullet.png')
        self.red_bullet = load_image('red_alien_bullet.png')
        self.blue_bullet = load_image('blue_alien_bullet.png')

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of bullet.
        self.rect.centerx = alien.rect.centerx
        self.rect.centery = alien.rect.centery

        # Current position of bullet.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed_factor = ai_settings.alien_bullet_speed_factor  # Bullet speed.
        self.ship_position = None
        self.shooting_angle_cos = None
        self.shooting_angle = None
        self.angles = (180, 360)

    def update(self):
        """Update position of bullets depending on ship current position."""
        if self.ship_position == "4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[1] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[1] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x
            self.rect.centery = self.y
        elif self.ship_position == "1":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x
            self.rect.centery = self.y
        elif self.ship_position == "2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] - self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] - self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x
            self.rect.centery = self.y
        elif self.ship_position == "3":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centerx = self.x
            self.rect.centery = self.y
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
            self.rect.centerx = self.x
        elif self.ship_position == "1-2":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x
        elif self.ship_position == "3-4":
            bullet_move_x = self.speed_factor * math.cos(math.radians(self.angles[0] + self.shooting_angle))
            bullet_move_y = -self.speed_factor * math.sin(math.radians(self.angles[0] + self.shooting_angle))
            self.x += bullet_move_x
            self.y += bullet_move_y
            self.rect.centery = self.y
            self.rect.centerx = self.x

    def draw_alien_bullet(self):
        """Draw alien bullet on screen."""
        self.screen.blit(self.image, self.rect)

    def define_angle(self, ship):
        """Define direction of bullet.

        Args:
            :param ship: Instance of Ship class.

        """
        ab = abs(self.y - ship.centery)
        ac = abs(self.x - ship.centerx)
        bc = math.sqrt(pow(ab, 2) + pow(ac, 2))
        self.shooting_angle_cos = ac / bc
        self.shooting_angle = fa.find_angle_with_cos(self.shooting_angle_cos)

    def define_position(self, ship):
        """Define position of ship.

        Args:
            :param ship: Instance of Ship class.

        """
        if self.x < ship.centerx and self.y < ship.centery:
            self.ship_position = "4"
            self.define_angle(ship)
        elif self.x < ship.centerx and self.y > ship.centery:
            self.ship_position = "1"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y > ship.centery:
            self.ship_position = "2"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y < ship.centery:
            self.ship_position = "3"
            self.define_angle(ship)
        elif self.x < ship.centerx and self.y == ship.centery:
            self.ship_position = "4-1"
            self.define_angle(ship)
        elif self.x > ship.centerx and self.y == ship.centery:
            self.ship_position = "2-3"
            self.define_angle(ship)
        elif self.x == ship.centerx and self.y > ship.centery:
            self.ship_position = "1-2"
            self.define_angle(ship)
        elif self.x == ship.centerx and self.y < ship.centery:
            self.ship_position = "3-4"
            self.define_angle(ship)
