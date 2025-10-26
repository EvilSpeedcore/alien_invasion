from typing import TYPE_CHECKING

from pygame.sprite import Sprite

from game.images import load_image
from game.rotation import Rotation

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

    def blitme(self) -> None:
        """Draw item on screen."""
        self.screen.it.blit(self.item, self.rect)


class ShipHealth(ShipConsumable):
    IMAGE = load_image("stats_health.png")
    ITEM = load_image("spawned_health.png")

    def __init__(self, screen: "Screen") -> None:
        self.image = self.IMAGE
        rect = self.IMAGE.get_rect()
        super().__init__(screen=screen, item=self.ITEM, rect=rect)


class ShipAmmo(ShipConsumable):
    IMAGE = load_image("stats_ammo.png")
    ITEM = load_image("spawned_ammo.png")

    def __init__(self, screen: "Screen") -> None:
        self.image = self.IMAGE
        rect = self.image.get_rect()
        super().__init__(screen=screen, item=self.ITEM, rect=rect)


class ShipShield(ShipConsumable):
    IMAGE = load_image("stats_shield.png")
    ITEM = load_image("spawned_shield.png")

    def __init__(self, screen: "Screen", ship: "Ship") -> None:
        self.image = self.IMAGE
        rect = self.ITEM.get_rect()
        super().__init__(screen=screen, item=self.ITEM, rect=rect)
        self.ship = ship

        self.rect.centerx = self.ship.centerx
        self.rect.centery = self.ship.centery
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def update(self) -> None:
        """Update position of used shield relatively ship position."""
        match self.ship.current_ship_rotation:
            case Rotation.UP | Rotation.DOWN:
                self.centerx = self.ship.centerx
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery
                self.rect.centery = self.centery
            case Rotation.LEFT | Rotation.RIGHT:
                self.centerx = self.ship.centerx - 8
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery + 3
                self.rect.centery = self.centery
            case Rotation.UP_LEFT:
                self.centerx = self.ship.centerx - 9
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery - 5
                self.rect.centery = self.centery
            case Rotation.UP_RIGHT:
                self.centerx = self.ship.centerx
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery - 5
                self.rect.centery = self.centery
            case Rotation.DOWN_LEFT:
                self.centerx = self.ship.centerx - 9
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery + 1
                self.rect.centery = self.centery + 1
            case Rotation.DOWN_RIGHT:
                self.centerx = self.ship.centerx - 1
                self.rect.centerx = self.centerx
                self.centery = self.ship.centery + 2
                self.rect.centery = self.centery
