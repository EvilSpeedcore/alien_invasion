import pygame
from pygame.sprite import Sprite


class ShipConsumable(Sprite):
    """Parent class, which represents items that ship can pick up on screen and use later."""
    def __init__(self, ai_settings, screen):
        """Initialize ship consumable.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.

        """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.spawned_item = None
        self.rect = None

    def draw_item(self):
        """Draw item on screen."""
        self.screen.blit(self.spawned_item, self.rect)


class ShipHealth(ShipConsumable):
    """Child class of ShipConsumable class, which represents health pick-ups."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.image = pygame.image.load('images/stats_health.png')
        self.spawned_item = pygame.image.load('images/spawned_health.png')
        self.rect = self.image.get_rect()


class ShipAmmo(ShipConsumable):
    """Child class of ShipConsumable class, which represents ammo pick-ups."""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        self.image = pygame.image.load('images/stats_ammo.png')
        self.spawned_item = pygame.image.load('images/spawned_ammo.png')
        self.rect = self.image.get_rect()


class ShipShield(ShipConsumable):
    """Child class of ShipConsumable class, which represents shield pick-ups."""
    def __init__(self, ai_settings, screen, ship):
        """Initialize ship shield.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.
            :param ship: Instance of Ship class.

        """
        super().__init__(ai_settings, screen)
        self.ship = ship
        self.image = pygame.image.load('images/stats_shield.png')
        self.spawned_item = pygame.image.load('images/spawned_shield.png')
        self.rect = self.spawned_item.get_rect()
        self.rect.centerx = self.ship.centerx
        self.rect.centery = self.ship.centery
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self, ship):
        """Update position of used shield relatively ship position.

        Args:
            :param ship: Instance of Ship class.

        """
        if self.ship.current_ship_rotation == "up":
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "down":
            self.centerx = self.ship.centerx
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "left":
            self.centerx = self.ship.centerx - 8.0
            self.rect.centerx = self.centerx
            self.centery = self.ship.centery + 3.0
            self.rect.centery = self.centery
        elif self.ship.current_ship_rotation == "right":
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
