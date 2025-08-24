from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image

if TYPE_CHECKING:
    from pygame.rect import Rect
    from pygame.surface import Surface

    from game.screen import Screen
    from game.ship import Ship


class ShipConsumable(Sprite):

    def __init__(self, screen: "Screen", item: "Surface", rect: "Rect") -> None:
        super().__init__()
        self.screen = screen
        self.item = item
        self.rect = rect

    def draw_item(self) -> None:
        """Draw item on screen."""
        self.screen.it.blit(self.item, self.rect)


class ShipHealth(ShipConsumable):

    _IMAGE = load_image("stats_health.png")
    _ITEM = load_image("spawned_health.png")

    def __init__(self, screen: "Screen") -> None:
        self.image = self._IMAGE
        rect = self._IMAGE.get_rect()
        super().__init__(screen=screen, item=self._ITEM, rect=rect)


class ShipAmmo(ShipConsumable):

    _IMAGE = load_image("stats_ammo.png")
    _ITEM = load_image("spawned_ammo.png")

    def __init__(self, screen: "Screen") -> None:
        self.image = self._IMAGE
        rect = self.image.get_rect()
        super().__init__(screen=screen, item=self._ITEM, rect=rect)


class ShipShield(ShipConsumable):
    _IMAGE = load_image("stats_shield.png")
    _ITEM = load_image("spawned_shield.png")

    def __init__(self, screen: "Screen", ship: "Ship") -> None:
        self.image = self._IMAGE
        rect = self._ITEM.get_rect()
        super().__init__(screen=screen, item=self._ITEM, rect=rect)
        self.ship = ship

        self.rect.centerx = self.ship.centerx
        self.rect.centery = self.ship.centery
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def update(self) -> None:
        """Update position of used shield relatively ship position."""
        if self.ship.current_ship_rotation in ("up", "down"):
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation in ("left", "right"):
            self.centerx = self.ship.centerx - 8
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 3
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "up-left":
            self.centerx = self.ship.centerx - 9
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery - 5
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "up-right":
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery - 5
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "down-left":
            self.centerx = self.ship.centerx - 9
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 1
            self.rect.centery = self.centery + 1
        elif self.ship.current_ship_rotation == "down-right":
            self.centerx = self.ship.centerx - 1
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 2
            self.rect.centery = self.centery
