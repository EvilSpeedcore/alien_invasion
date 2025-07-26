from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.settings import Settings
    from game.ship import Ship


class ShipConsumable(Sprite):

    def __init__(self, ai_settings: "Settings", screen: "Surface") -> None:
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.spawned_item = None
        self.rect = None

    def draw_item(self) -> None:
        """Draw item on screen."""
        self.screen.blit(self.spawned_item, self.rect)


class ShipHealth(ShipConsumable):

    def __init__(self, ai_settings: "Settings", screen: "Surface") -> None:
        super().__init__(ai_settings, screen)
        self.image = load_image("stats_health.png")
        self.spawned_item = load_image("spawned_health.png")
        self.rect = self.image.get_rect()


class ShipAmmo(ShipConsumable):

    def __init__(self, ai_settings: "Settings", screen: "Surface") -> None:
        super().__init__(ai_settings, screen)
        self.image = load_image("stats_ammo.png")
        self.spawned_item = load_image("spawned_ammo.png")
        self.rect = self.image.get_rect()


class ShipShield(ShipConsumable):

    def __init__(self, ai_settings: "Settings", screen: "Surface", ship: "Ship") -> None:
        super().__init__(ai_settings, screen)
        self.ship = ship
        self.image = load_image("stats_shield.png")
        self.spawned_item = load_image("spawned_shield.png")
        self.rect = self.spawned_item.get_rect()
        self.rect.centerx = self.ship.centerx
        self.rect.centery = self.ship.centery
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self) -> None:
        """Update position of used shield relatively ship position."""
        if self.ship.current_ship_rotation in ("up", "down"):
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation in ("left", "right"):
            self.centerx = self.ship.centerx - 8.0
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 3.0
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "up-left":
            self.centerx = self.ship.centerx - 9.0
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery - 5.0
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "up-right":
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery - 5.0
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "down-left":
            self.centerx = self.ship.centerx - 9.0
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 1.0
            self.rect.centery = self.centery + 1.0
        elif self.ship.current_ship_rotation == "down-right":
            self.centerx = self.ship.centerx - 1.0
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 2.0
            self.rect.centery = self.centery
