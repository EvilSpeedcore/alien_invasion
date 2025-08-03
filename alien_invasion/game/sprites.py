from dataclasses import dataclass, field

from pygame.sprite import Group, GroupSingle


@dataclass
class Sprites:
    # TODO: How to type Group?
    aliens: Group                 = field(default_factory=Group)
    alien_bullets: Group          = field(default_factory=Group)
    # TODO: How to type GroupSingle?
    bosses: GroupSingle           = field(default_factory=GroupSingle)
    boss_bullets: Group           = field(default_factory=Group)
    boss_shields: GroupSingle     = field(default_factory=GroupSingle)
    boss_health: GroupSingle      = field(default_factory=GroupSingle)
    boss_black_holes: GroupSingle = field(default_factory=GroupSingle)
    ship_bullets: Group           = field(default_factory=Group)
    ship_health: Group            = field(default_factory=Group)
    ship_ammo: Group              = field(default_factory=Group)
    ship_shields: Group           = field(default_factory=Group)
