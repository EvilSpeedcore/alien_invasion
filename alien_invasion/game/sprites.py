from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame.sprite import Group, GroupSingle

if TYPE_CHECKING:
    from game.alien import Alien
    from game.alien_bullet import AlienBullet
    from game.black_hole import BlackHole
    from game.boss_health import BossHealthTypes
    from game.bosses_bullets import BossBulletsTypes
    from game.bullet import Bullet
    from game.ship_consumables import ShipAmmo, ShipHealth, ShipShield


@dataclass
class Sprites:
    aliens: Group["Alien"]                       = field(default_factory=Group)
    alien_bullets: Group["AlienBullet"]          = field(default_factory=Group)
    # TODO: Add typing
    bosses: GroupSingle                          = field(default_factory=GroupSingle)
    # TODO: Add typing
    boss_bullets: Group                          = field(default_factory=Group)
    # TODO: Add typing
    boss_shields: GroupSingle                    = field(default_factory=GroupSingle)
    boss_health: GroupSingle["BossHealthTypes"]  = field(default_factory=GroupSingle)
    boss_black_holes: GroupSingle["BlackHole"]   = field(default_factory=GroupSingle)
    ship_bullets: Group["Bullet"]                = field(default_factory=Group)
    ship_health: Group["ShipHealth"]             = field(default_factory=Group)
    ship_ammo: Group["ShipAmmo"]                 = field(default_factory=Group)
    ship_shields: Group["ShipShield"]            = field(default_factory=Group)
