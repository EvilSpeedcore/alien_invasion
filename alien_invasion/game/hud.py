from typing import TYPE_CHECKING

from pygame.sprite import Group, GroupSingle

from game.boss_health import BlueBossHealth, GreenBossHealth, RedBossHealth
from game.ship_consumables import ShipAmmo, ShipHealth, ShipShield

if TYPE_CHECKING:
    from pygame.surface import Surface

    from game.game_stats import GameStats
    from game.settings import Settings
    from game.ship import Ship


class Hud:
    """Class, which represents head-up display."""
    def __init__(self,
                 ai_settings: "Settings",
                 screen: "Surface",
                 stats: "GameStats",
                 ship: "Ship") -> None:
        """Initialize hud.

        Args:
            :param ai_settings: Instance of Settings class.
            :param screen: Display Surface.
            :param stats: Instance of GameStats class.
            :param ship: Instance of Ship class.

        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.ship = ship
        self.green_boss_hp = 19
        self.red_boss_hp = 14
        self.blue_boss_hp = 19

        # Preparing of hud.
        self.prep_health()
        self.prep_ammo()
        self.prep_shield()
        self.prep_green_boss_health()

    def prep_health(self) -> None:
        """Prepare to drawn ship health."""
        self.health: Group[ShipHealth] = Group()
        for ship_number in range(self.stats.ships_left):
            ship_health = ShipHealth(self.ai_settings, self.screen)
            ship_health.rect.x = 20 + ship_number * (ship_health.rect.width + 10)
            ship_health.rect.y = 28
            self.health.add(ship_health)

    def prep_green_boss_health(self) -> None:
        """Prepare to drawn green boss health."""
        # TODO: How to type GroupSingle?
        self.boss_health: GroupSingle = GroupSingle()
        boss_health = GreenBossHealth(self.ai_settings, self.screen)
        hp_image = boss_health.hp_images[self.green_boss_hp]
        boss_health.image = hp_image.copy()
        boss_health.rect.x = 500
        boss_health.rect.y = 60
        self.boss_health.add(boss_health)

    def prep_red_boss_health(self) -> None:
        """Prepare to drawn red boss health."""
        self.boss_health = GroupSingle()
        boss_health = RedBossHealth(self.ai_settings, self.screen)
        hp_image = boss_health.hp_images[self.red_boss_hp]
        boss_health.image = hp_image.copy()
        boss_health.rect.x = 500
        boss_health.rect.y = 60
        self.boss_health.add(boss_health)

    def prep_blue_boss_health(self) -> None:
        """Prepare to drawn blue boss track."""
        self.boss_health = GroupSingle()
        boss_health = BlueBossHealth(self.ai_settings, self.screen)
        hp_image = boss_health.hp_images[self.blue_boss_hp]
        boss_health.image = hp_image.copy()
        boss_health.rect.x = 500
        boss_health.rect.y = 60
        self.boss_health.add(boss_health)

    def prep_ammo(self) -> None:
        """Prepare to drawn ship ammo."""
        self.ammo: Group[ShipAmmo] = Group()
        for ammo in range(self.stats.ammo):
            ship_ammo = ShipAmmo(self.ai_settings, self.screen)
            ship_ammo.rect.x = 20 + ammo * (ship_ammo.rect.width + 10)
            ship_ammo.rect.y = 60
            self.ammo.add(ship_ammo)

    def prep_shield(self) -> None:
        """Prepare to drawn ship shield."""
        self.shield: Group[ShipShield] = Group()
        for _ in range(self.stats.shields_left):
            stats_shield = ShipShield(self.ai_settings, self.screen, self.ship)
            stats_shield.rect.x = 20
            stats_shield.rect.y = 750
            self.shield.add(stats_shield)

    def show_hud(self) -> None:
        """Draw hud on screen."""
        self.health.draw(self.screen)
        self.ammo.draw(self.screen)
        self.shield.draw(self.screen)
        if self.stats.stage in self.ai_settings.boss_stages:
            self.boss_health.draw(self.screen)
            self.boss_health.draw(self.screen)
