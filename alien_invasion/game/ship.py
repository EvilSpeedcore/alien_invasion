from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image
from game.rotation import Rotation, rotate_to_up

if TYPE_CHECKING:
    from game.screen import Screen
    from game.settings import Settings


class Ship(Sprite):

    class Images:
        UP = load_image("ship_up.png")
        RIGHT = load_image("ship_right.png")
        LEFT = load_image("ship_left.png")
        DOWN = load_image("ship_down.png")
        UP_RIGHT = load_image("ship_up_right.png")
        UP_LEFT = load_image("ship_up_left.png")
        DOWN_RIGHT = load_image("ship_down_right.png")
        DOWN_LEFT = load_image("ship_down_left.png")

    def __init__(self, settings: "Settings", screen: "Screen") -> None:
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = self.Images.UP

        # Get the rectangular area of the image.
        self.rect = self.image.get_rect()

        self.screen_rect = screen.rect

        # Set starting position of ship at the center of screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # Current ship position.
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

        self.speed = self.settings.ship_speed

        self.set_default_movement()

    def update(self) -> None:
        """Update ship position depending on movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.speed  # type: ignore[assignment]
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.speed  # type: ignore[assignment]
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.speed  # type: ignore[assignment]
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.speed  # type: ignore[assignment]
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self) -> None:
        """Set ship position on center of the screen."""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.centery

    def prepare_for_boss(self) -> None:
        """Set ship position below boss position."""
        self.centerx = self.screen_rect.centerx
        self.centery = 700
        rotate_to_up(ship=self)

    def blitme(self) -> None:
        """Draw ship."""
        self.screen.it.blit(self.image, self.rect)

    def set_default_movement(self) -> None:
        # Flags to check if ship moving in one or another direction.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Default ship direction.
        self.current_ship_rotation: Rotation = Rotation.UP

        # Direction in which ship currently moving.
        self.desirable_ship_rotation: Rotation | None = None
