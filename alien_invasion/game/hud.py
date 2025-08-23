from typing import TYPE_CHECKING

from pygame.sprite import Group

from game.ship_consumables import ShipAmmo, ShipHealth, ShipShield

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stats import Stats


class Hud:

    def __init__(self,
                 settings: "Settings",
                 screen: "Surface",
                 stats: "Stats",
                 ship: "Ship",
                 sprites: "Sprites") -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.ship = ship
        self.boss_health = sprites.boss_health

        # Preparing of hud.
        self.prep_health()
        self.prep_ammo()
        self.prep_shield()

    def prep_health(self) -> None:
        """Prepare to drawn ship health."""
        self.health: Group[ShipHealth] = Group()
        for ship_number in range(self.stats.ships_left):
            ship_health = ShipHealth(self.screen)
            ship_health.rect.x = 20 + ship_number * (ship_health.rect.width + 10)
            ship_health.rect.y = 28
            self.health.add(ship_health)

    def prep_ammo(self) -> None:
        """Prepare to drawn ship ammo."""
        self.ammo: Group[ShipAmmo] = Group()
        for ammo in range(self.stats.ammo):
            ship_ammo = ShipAmmo(self.screen)
            ship_ammo.rect.x = 20 + ammo * (ship_ammo.rect.width + 10)
            ship_ammo.rect.y = 60
            self.ammo.add(ship_ammo)

    def prep_shield(self) -> None:
        """Prepare to drawn ship shield."""
        self.shield: Group[ShipShield] = Group()
        for _ in range(self.stats.shields_left):
            stats_shield = ShipShield(self.screen, self.ship)
            stats_shield.rect.x = 20
            stats_shield.rect.y = 750
            self.shield.add(stats_shield)

    def show_hud(self) -> None:
        """Draw hud on screen."""
        self.health.draw(self.screen)
        self.ammo.draw(self.screen)
        self.shield.draw(self.screen)
        self.boss_health.draw(self.screen)
