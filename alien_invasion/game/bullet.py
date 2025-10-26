from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image
from game.ship import Rotation, Ship

if TYPE_CHECKING:
    from game.screen import Screen
    from game.settings import Settings


class Bullet(Sprite):
    IMAGE = load_image("bullet.png")

    def __init__(self, settings: "Settings", screen: "Screen", ship: "Ship") -> None:
        super().__init__()
        self.screen = screen
        self.image = self.IMAGE

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        # Set starting position of bullet at the center of ship.
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.centery

        # Current bullet position for different ship positions.
        # For UP position of ship.
        self.y_up = float(self.rect.centery) - 35
        self.x_up = float(self.rect.centerx)

        # For RIGHT position of ship.
        self.y_right = float(self.rect.centery) + 5
        self.x_right = float(self.rect.centerx) + 30

        # For LEFT position of ship.
        self.y_left = float(self.rect.centery) + 5
        self.x_left = float(self.rect.centerx) - 45

        # For DOWN position of ship.
        self.y_down = float(self.rect.centery) + 35
        self.x_down = float(self.rect.centerx) - 1

        # For UP_RIGHT position of ship.
        self.y_up_right = float(self.rect.centery) - 27
        self.x_up_right = float(self.rect.centerx) + 24

        # For UP_LEFT position of ship.
        self.y_up_left = float(self.rect.centery) - 30
        self.x_up_left = float(self.rect.centerx) - 30

        # For DOWN_LEFT position of ship.
        self.y_down_left = float(self.rect.centery) + 30
        self.x_down_left = float(self.rect.centerx) - 33

        # For DOWN_RIGHT position of ship.
        self.y_down_right = float(self.rect.centery) + 32
        self.x_down_right = float(self.rect.centerx) + 27

        self.speed_factor = settings.bullet_speed_factor
        self.bullet_rotation = ship.current_ship_rotation

    def update(self) -> None:
        """Update bullet position depending on ship current rotation."""
        match self.bullet_rotation:
            case Rotation.UP:
                self.y_up -= self.speed_factor
                self.rect.centery = self.y_up  # type: ignore[assignment]
                self.rect.centerx = self.x_up  # type: ignore[assignment]
            case Rotation.RIGHT:
                self.x_right += self.speed_factor
                self.rect.centerx = self.x_right  # type: ignore[assignment]
                self.rect.centery = self.y_right  # type: ignore[assignment]
            case Rotation.LEFT:
                self.x_left -= self.speed_factor
                self.rect.centerx = self.x_left  # type: ignore[assignment]
                self.rect.centery = self.y_left  # type: ignore[assignment]
            case Rotation.DOWN:
                self.y_down += self.speed_factor
                self.rect.centery = self.y_down  # type: ignore[assignment]
                self.rect.centerx = self.x_down  # type: ignore[assignment]
            case Rotation.UP_RIGHT:
                self.y_up_right -= self.speed_factor
                self.x_up_right += self.speed_factor
                self.rect.centery = self.y_up_right  # type: ignore[assignment]
                self.rect.centerx = self.x_up_right  # type: ignore[assignment]
            case Rotation.UP_LEFT:
                self.y_up_left -= self.speed_factor
                self.x_up_left -= self.speed_factor
                self.rect.centery = self.y_up_left  # type: ignore[assignment]
                self.rect.centerx = self.x_up_left  # type: ignore[assignment]
            case Rotation.DOWN_LEFT:
                self.y_down_left += self.speed_factor
                self.x_down_left -= self.speed_factor
                self.rect.centery = self.y_down_left  # type: ignore[assignment]
                self.rect.centerx = self.x_down_left  # type: ignore[assignment]
            case Rotation.DOWN_RIGHT:
                self.y_down_right += self.speed_factor
                self.x_down_right += self.speed_factor
                self.rect.centery = self.y_down_right  # type: ignore[assignment]
                self.rect.centerx = self.x_down_right  # type: ignore[assignment]

    def blitme(self) -> None:
        self.screen.it.blit(self.image, self.rect)
