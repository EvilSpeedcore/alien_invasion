import random
from itertools import count
from logging import getLogger
from typing import TYPE_CHECKING

from game.ship_consumables import ShipAmmo, ShipHealth

log = getLogger(__name__)


if TYPE_CHECKING:
    from game.settings import Settings
    from game.ship import Ship


class BaseStage:

    counter = count(start=0)

    def __init__(self, name: str) -> None:
        self.name = name

        self.index = next(self.counter)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, other) -> None:
        if isinstance(other, BaseStage):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


class Stage(BaseStage):

    def __init__(self,
                 settings: "Settings",
                 screen,
                 stats,
                 ship: "Ship",
                 health,
                 ammo,
                 bullets,
                 alien_bullets,
                 name: str) -> None:
        super().__init__(name)

        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets

    def set_up(self) -> None:
        log.debug("%s: set_up()", self)
        self.settings.increase_aliens_speed()

        if not maybe_spawn_extra_health(settings=self.settings,
                                        screen=self.screen,
                                        stats=self.stats,
                                        ship=self.ship,
                                        health=self.health):
            maybe_spawn_extra_ammo(settings=self.settings,
                                   screen=self.screen,
                                   stats=self.stats,
                                   ship=self.ship,
                                   ammo=self.ammo)

    def tear_down(self) -> None:
        log.debug("%s: tear_down()", self)
        self.ship.center_ship()
        self.health.empty()
        self.ammo.empty()
        self.alien_bullets.empty()
        self.bullets.empty()


class BossStage(BaseStage):

    def set_up(self) -> None:
        log.debug("%s: set_up()", self)

    def tear_down(self) -> None:
        log.debug("%s: tear_down()", self)


class Stages(list[Stage | BossStage]):

    def __init__(self,
                 settings: "Settings",
                 screen,
                 stats,
                 ship,
                 health,
                 ammo,
                 bullets,
                 alien_bullets) -> None:
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets

        super().__init__(self.create_stages())

        self.current = None

    def create_stage(self, name: str) -> Stage:
        return Stage(settings=self.settings,
                     screen=self.screen,
                     stats=self.stats,
                     ship=self.ship,
                     health=self.health,
                     ammo=self.ammo,
                     bullets=self.bullets,
                     alien_bullets=self.alien_bullets,
                     name=name)

    def create_boss_stage(self, name: str) -> BossStage:
        return BossStage(name=name)

    def create_stages(self) -> list[Stage | BossStage]:
        return [
            self.create_stage(name="1_1"),
            self.create_stage(name="1_2"),
            self.create_stage(name="1_3"),
            self.create_boss_stage(name="green_boss"),
            self.create_stage(name="2_1"),
            self.create_stage(name="2_2"),
            self.create_stage(name="2_3"),
            self.create_boss_stage(name="red_boss"),
            self.create_stage(name="2_5"),
            self.create_stage(name="2_6"),
            self.create_stage(name="2_7"),
            self.create_boss_stage(name="blue_boss"),
            self.create_stage(name="end"),  # TODO: Fix. Not really a stage
        ]

    def get_by_name(self, name: str) -> Stage | BossStage:
        for stage in self:
            if stage.name == name:
                return stage
        # TODO: Raise proper error
        raise AssertionError

    def select(self, name: str) -> None:
        # TODO: "Rotate" calling set up
        self.current = self.get_by_name(name)

    def next_stage(self) -> Stage:
        prev_stage = self.current
        next_stage = self[prev_stage.index + 1]
        self.current = next_stage
        prev_stage.tear_down()
        next_stage.set_up()
        log.info("%s -> %s", prev_stage, next_stage)
        return next_stage

    def reset(self) -> None:
        self.current = self[0]


def maybe_spawn_extra_health(settings: "Settings", screen, stats, ship: "Ship", health) -> bool:
    # Flag, which shows the fact, that extra health not yet spawned.
    health_spawned = False
    # Extra health spawn.
    if stats.ships_left > 3:
        return health_spawned

    random_number = random.choice(range(1, 6))
    if random_number == 1:
        new_health = ShipHealth(settings, screen)
        banned_coordinates_x = list(range(int(ship.centerx - 100.0), int(ship.centerx + 106.0)))
        available_coordinates_x = [x for x in range(100, ship.screen_rect.right - 100) if
                                   x not in banned_coordinates_x]
        banned_coordinates_y = list(range(int(ship.centery - 100.0), int(ship.centery + 106.0)))
        available_coordinates_y = [y for y in range(100, ship.screen_rect.bottom - 100) if
                                   y not in banned_coordinates_y]
        new_health.rect.x = random.choice(available_coordinates_x)
        new_health.rect.y = random.choice(available_coordinates_y)
        health.add(new_health)
        health_spawned = True
    else:
        health.empty()

    return health_spawned


def maybe_spawn_extra_ammo(settings: "Settings", screen, stats, ship: "Ship", ammo) -> bool:
    # Extra ammo spawn.
    ammo_spawned = False
    if stats.ammo >= 3:
        return ammo_spawned

    random_number = random.choice(range(1, 6))
    if random_number == 1:
        new_ammo = ShipAmmo(settings, screen)
        _banned_coordinates_x = list(range(int(ship.centerx - 100.0), int(ship.centerx + 106.0)))
        _available_coordinates_x = [x for x in range(100, ship.screen_rect.right - 100) if
                                    x not in _banned_coordinates_x]
        _banned_coordinates_y = list(range(int(ship.centery - 100.0), int(ship.centery + 106.0)))
        _available_coordinates_y = [y for y in range(100, ship.screen_rect.bottom - 100) if
                                    y not in _banned_coordinates_y]
        new_ammo.rect.x = random.choice(_available_coordinates_x)
        new_ammo.rect.y = random.choice(_available_coordinates_y)
        ammo.add(new_ammo)
        ammo_spawned = True
    else:
        ammo.empty()

    return ammo_spawned
