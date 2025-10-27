import secrets
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.sprite import Group

    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


def collidable(alien: "Alien", other: "Alien") -> bool:
    """Check collision between two aliens."""
    if alien is other:
        return False
    return alien.rect.colliderect(other.rect)


class Alien(Sprite):
    IMAGE = load_image("green_alien.png")

    def __init__(self, settings: "Settings", screen: "Screen", ship: "Ship") -> None:
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = self.IMAGE

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.rect

        # Every new aliens spawns in random area of the screen from allowed coordinates.
        self.banned_coordinates = list(range(int(ship.centery - 200.0), int(ship.centery + 206.0)))
        self.available_coordinates = [y for y in range(60, self.screen_rect.bottom - self.rect.height) if
                                      y not in self.banned_coordinates]
        self.rect.centery = secrets.choice(self.available_coordinates)

        # Current position of alien.
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.speed = self.settings.aliens_speed

    def update(self, aliens: "Group[Alien]", ship: "Ship") -> None:
        """Update aliens position depending on ship current position. Check for collision between aliens."""
        aliens_collision = pygame.sprite.spritecollide(self, aliens, dokill=False, collided=collidable)
        if aliens_collision:
            for alien in aliens_collision:
                aliens.remove(alien)

        if self.x > ship.centerx:
            self.x -= self.speed  # type: ignore[assignment]
            self.rect.centerx = self.x
        if self.y > ship.centery:
            self.y -= self.speed  # type: ignore[assignment]
            self.rect.centery = self.y
        if self.x < ship.centerx:
            self.x += self.speed  # type: ignore[assignment]
            self.rect.centerx = self.x
        if self.y < ship.centery:
            self.y += self.speed  # type: ignore[assignment]
            self.rect.centery = self.y

    def adjust_in_fleet(self, index: int) -> None:
        alien_width = self.rect.width
        self.x = alien_width + 2 * alien_width * index
        self.rect.x = self.x


    def blitme(self) -> None:
        self.screen.it.blit(self.image, self.rect)


class GreenAlien(Alien):
    ...


class RedAlien(Alien):
    IMAGE = load_image("red_alien.png")


class BlueAlien(Alien):
    IMAGE = load_image("blue_alien.png")
