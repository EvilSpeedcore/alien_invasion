from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.settings import Settings
    from game.ship import Ship


class Bullet(Sprite):

    def __init__(self, ai_settings: "Settings", screen: "Surface", ship: "Ship") -> None:
        super().__init__()
        self.screen = screen
        self.image = load_image("bullet.png")

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

        self.speed_factor = ai_settings.bullet_speed_factor
        self.bullet_rotation = ship.current_ship_rotation

    def update(self) -> None:
        """Update bullet position depending on ship current rotation.

        Args:
            :param ship: Instance of Ship class.

        """
        if self.bullet_rotation == "up":
            self.y_up -= self.speed_factor
            self.rect.centery = self.y_up
            self.rect.centerx = self.x_up
        if self.bullet_rotation == "right":
            self.x_right += self.speed_factor
            self.rect.centerx = self.x_right
            self.rect.centery = self.y_right
        if self.bullet_rotation == "left":
            self.x_left -= self.speed_factor
            self.rect.centerx = self.x_left
            self.rect.centery = self.y_left
        if self.bullet_rotation == "down":
            self.y_down += self.speed_factor
            self.rect.centery = self.y_down
            self.rect.centerx = self.x_down
        if self.bullet_rotation == "up-right":
            self.y_up_right -= self.speed_factor
            self.x_up_right += self.speed_factor
            self.rect.centery = self.y_up_right
            self.rect.centerx = self.x_up_right
        if self.bullet_rotation == "up-left":
            self.y_up_left -= self.speed_factor
            self.x_up_left -= self.speed_factor
            self.rect.centery = self.y_up_left
            self.rect.centerx = self.x_up_left
        if self.bullet_rotation == "down-left":
            self.y_down_left += self.speed_factor
            self.x_down_left -= self.speed_factor
            self.rect.centery = self.y_down_left
            self.rect.centerx = self.x_down_left
        if self.bullet_rotation == "down-right":
            self.y_down_right += self.speed_factor
            self.x_down_right += self.speed_factor
            self.rect.centery = self.y_down_right
            self.rect.centerx = self.x_down_right

    def draw_bullet(self) -> None:
        """Draw bullet on screen depending on ship current rotation."""
        if self.bullet_rotation == "up":
            """Вывод пули на экран."""
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "right":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "left":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "down":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "up-right":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "up-left":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "down-left":
            self.screen.blit(self.image, self.rect)
        if self.bullet_rotation == "down-right":
            self.screen.blit(self.image, self.rect)
