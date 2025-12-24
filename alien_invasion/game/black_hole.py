import secrets
from collections import deque
from typing import TYPE_CHECKING, ClassVar

from pygame.sprite import Sprite

from game.images import load_sequential_from_dirs

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship


class BlackHole(Sprite):
    ROTATION_IMAGES: ClassVar[list["Surface"]] = load_sequential_from_dirs("black_hole")

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 ship: "Ship") -> None:
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.rect

        self.images: deque[Surface] = deque(self.ROTATION_IMAGES)
        self.image = self.images[0].copy()

        self.rect = self.image.get_rect()

        # Black holes spawns in random area of screen from allowed coordinates.
        self.banned_coordinates_x_1 = list(range(int(ship.centerx - 100.0), int(ship.centerx + 106.0)))
        self.banned_coordinates_x_2 = list(range(int(self.screen_rect.centerx - 150.0),
                                                 int(self.screen_rect.centerx + 150.0)))
        self.banned_coordinates_x = list(set(self.banned_coordinates_x_1 + self.banned_coordinates_x_2))
        self.available_coordinates_x = [x for x in range(100, self.screen_rect.right - 100) if
                                        x not in self.banned_coordinates_x]
        self.banned_coordinates_y_1 = list(range(int(ship.centery - 100.0), int(ship.centery + 106.0)))
        self.banned_coordinates_y_2 = list(range(int(self.screen_rect.centery - 150.0),
                                                 int(self.screen_rect.centery + 150.0)))
        self.banned_coordinates_y = list(set(self.banned_coordinates_y_1 + self.banned_coordinates_y_2))
        self.available_coordinates_y = [y for y in range(100, self.screen_rect.bottom - 100) if
                                        y not in self.banned_coordinates_y]
        self.rect.centerx = secrets.choice(self.available_coordinates_x)
        self.rect.centery = secrets.choice(self.available_coordinates_y)

    def blitme(self) -> None:
        self.screen.it.blit(self.image, self.rect)

    def update(self) -> None:
        """Change image of black hole to make animation effect."""
        self.images.rotate()
        hp_image = self.images[0]
        self.image = hp_image.copy()
