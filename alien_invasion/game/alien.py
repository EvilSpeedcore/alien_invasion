from random import choice
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.sprite import Group
    from pygame.surface import Surface

    from game.settings import Settings
    from game.ship import Ship


def collidable(alien_1: "Alien", alien_2: "Alien") -> bool:
    """Check collision between two aliens.

    Args:
        :param Alien alien_1: One alien from group of sprites.
        :param Alien alien_2: Another alien from group of sprites.

    Returns:
        :return bool: True if successful, False otherwise.

    """
    if alien_1 is alien_2:
        return False
    else:
        return alien_1.rect.colliderect(alien_2.rect)


class Alien(Sprite):
    """Class, which represents alien ships."""
    def __init__(self,
                 ai_settings: "Settings",
                 screen: "Surface",
                 ship: "Ship") -> None:
        """Initialize alien.

        Args:
            :param Settings ai_settings: Instance of Settings class.
            :param Surface screen: Display Surface.
            :param Ship ship: Instance of Ship class.

        """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Image load of different aliens.
        self.image = load_image('green_alien.png')
        self.red_alien = load_image('red_alien.png')
        self.blue_alien = load_image('blue_alien.png')

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Every new aliens spawns in random area of the screen from allowed coordinates.
        self.banned_coordinates = [y for y in range(int(ship.centery - 200.0), int(ship.centery + 206.0))]
        self.available_coordinates = [y for y in range(60, self.screen_rect.bottom - self.rect.height) if
                                      y not in self.banned_coordinates]
        self.rect.centery = choice(self.available_coordinates)

        # Current position of alien.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Fleet creation time.
        self.fleet_creation_time = None

        # Alien color.
        self.alien_color = None

    def update(self, aliens: "Group", ship: "Ship") -> None:
        """Update aliens position depending on ship current position. Check for collision between aliens.

        Args:
            :param Group aliens: Group of alien sprites.
            :param Ship ship: Instance of Ship class.

        """
        aliens_collision = pygame.sprite.spritecollide(self, aliens, False, collidable)
        if aliens_collision:
            aliens.remove(aliens_collision[0])
        else:
            if self.x > ship.centerx:
                self.x -= self.ai_settings.alien_speed_factor
                self.rect.centerx = self.x
            if self.y > ship.centery:
                self.y -= self.ai_settings.alien_speed_factor
                self.rect.centery = self.y
            if self.x < ship.centerx:
                self.x += self.ai_settings.alien_speed_factor
                self.rect.centerx = self.x
            if self.y < ship.centery:
                self.y += self.ai_settings.alien_speed_factor
                self.rect.centery = self.y
