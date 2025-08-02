import random
from abc import abstractmethod
from itertools import count
from logging import getLogger
from typing import TYPE_CHECKING

import game.game_functions as gf
import game.rotation as rt
from game.ship_consumables import ShipAmmo, ShipHealth

log = getLogger(__name__)


if TYPE_CHECKING:
    from pygame.sprite import Group, GroupSingle
    from pygame.surface import Surface

    from game.collections import Sprites
    from game.game_stats import GameStats
    from game.hud import Hud
    from game.settings import Settings
    from game.ship import Ship


class BaseStage:

    counter = count(start=0)

    def __init__(self, sprites: "Sprites", name: str) -> None:
        self.sprites = sprites
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

    @abstractmethod
    def setup(self) -> None:
        log.debug("%s: setup()", self)

    @abstractmethod
    def transit(self) -> None:
        log.debug("%s: transit()", self)

    @abstractmethod
    def teardown(self) -> None:
        log.debug("%s: teardown()", self)
        self.sprites.ship_bullets.empty()
        self.sprites.ship_health.empty()
        self.sprites.ship_ammo.empty()
        self.sprites.ship_shields.empty()


class Stage(BaseStage):

    def __init__(self,
                 stages: "Stages",
                 settings: "Settings",
                 screen: "Surface",
                 stats: "GameStats",
                 ship: "Ship",
                 sprites: "Sprites",
                 name: str) -> None:
        super().__init__(sprites=sprites, name=name)

        self.stages = stages
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.ship = ship

    def setup(self) -> None:
        super().setup()
        self.ship.center_ship()

        if not maybe_spawn_extra_health(settings=self.settings,
                                        screen=self.screen,
                                        stats=self.stats,
                                        ship=self.ship,
                                        health=self.sprites.ship_health):
            maybe_spawn_extra_ammo(settings=self.settings,
                                   screen=self.screen,
                                   stats=self.stats,
                                   ship=self.ship,
                                   ammo=self.sprites.ship_ammo)

        gf.create_fleet(settings=self.settings,
                        screen=self.screen,
                        stages=self.stages,
                        ship=self.ship,
                        aliens=self.sprites.aliens)

    def transit(self) -> None:
        super().transit()
        # do not increase speed if next stage is a boss stage
        # TODO: self.stages.current is confusing
        #       (we set current to early),
        #       change to self.stages.next
        if not isinstance(self.stages.current, BossStage):
            self.settings.increase_aliens_speed()

    def teardown(self) -> None:
        super().teardown()
        self.sprites.alien_bullets.empty()


class BossStage(BaseStage):

    def __init__(self, ship: "Ship", sprites: "Sprites", name: str) -> None:
        super().__init__(sprites=sprites, name=name)

        self.ship = ship

    def setup(self) -> None:
        super().setup()
        self.ship.prepare_for_boss()
        rt.rotate_to_up(self.ship)

    def teardown(self) -> None:
        super().teardown()
        self.sprites.boss_health.empty()
        self.sprites.boss_shields.empty()


class GreenBossStage(BossStage):

    def __init__(self,
                 settings: "Settings",
                 screen: "Surface",
                 hud: "Hud",
                 ship: "Ship",
                 sprites: "Sprites",
                 name: str) -> None:
        super().__init__(ship=ship, sprites=sprites, name=name)

        self.settings = settings
        self.screen = screen
        self.hud = hud

    def setup(self) -> None:
        super().setup()
        gf.create_green_boss(settings=self.settings,
                             screen=self.screen,
                             hud=self.hud,
                             bosses=self.sprites.bosses,
                             boss_shields=self.sprites.boss_shields)


class RedBossStage(GreenBossStage):

    def setup(self) -> None:
        super(GreenBossStage, self).setup()
        gf.create_red_boss(settings=self.settings,
                           screen=self.screen,
                           hud=self.hud,
                           bosses=self.sprites.bosses,
                           boss_shields=self.sprites.boss_shields)


class BlueBossStage(BossStage):

    def __init__(self,
                 settings: "Settings",
                 screen: "Surface",
                 hud: "Hud",
                 ship: "Ship",
                 sprites: "Sprites",
                 name: str) -> None:
        super().__init__(ship=ship, sprites=sprites, name=name)

        self.settings = settings
        self.screen = screen
        self.hud = hud

    def setup(self) -> None:
        super().setup()
        gf.create_blue_boss(settings=self.settings,
                            screen=self.screen,
                            hud=self.hud,
                            bosses=self.sprites.bosses,
                            boss_shields=self.sprites.boss_shields)

    def teardown(self) -> None:
        super().teardown()
        self.sprites.boss_black_holes.empty()


class Stages(list[Stage | BossStage]):

    def __init__(self,
                 settings: "Settings",
                 screen: "Surface",
                 stats: "GameStats",
                 hud: "Hud",
                 ship: "Ship",
                 sprites: "Sprites") -> None:
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.hud = hud
        self.ship = ship
        self.sprites = sprites

        super().__init__(self.create_stages())

        self.current = None

    def create_stage(self, name: str) -> Stage:
        return Stage(stages=self,
                     settings=self.settings,
                     screen=self.screen,
                     stats=self.stats,
                     ship=self.ship,
                     sprites=self.sprites,
                     name=name)

    def create_boss_stage(self, name: str) -> BossStage:
        return BossStage(ship=self.ship, sprites=self.sprites, name=name)

    def create_green_boss_stage(self, name: str) -> GreenBossStage:
        return GreenBossStage(settings=self.settings,
                              screen=self.screen,
                              hud=self.hud,
                              ship=self.ship,
                              sprites=self.sprites,
                              name=name)

    def create_red_boss_stage(self, name: str) -> GreenBossStage:
        return RedBossStage(settings=self.settings,
                            screen=self.screen,
                            hud=self.hud,
                            ship=self.ship,
                            sprites=self.sprites,
                            name=name)

    def create_blue_boss_stage(self, name: str) -> None:
        return BlueBossStage(settings=self.settings,
                             screen=self.screen,
                             hud=self.hud,
                             ship=self.ship,
                             sprites=self.sprites,
                             name=name)

    def create_end_stage(self, name: str) -> BaseStage:
        return BaseStage(sprites=self.sprites, name=name)

    def create_stages(self) -> list[Stage | BossStage]:
        return [
            self.create_stage(name="1_1"),
            self.create_stage(name="1_2"),
            self.create_stage(name="1_3"),
            self.create_green_boss_stage(name="green_boss"),
            self.create_stage(name="2_1"),
            self.create_stage(name="2_2"),
            self.create_stage(name="2_3"),
            self.create_red_boss_stage(name="red_boss"),
            self.create_stage(name="3_1"),
            self.create_stage(name="3_2"),
            self.create_stage(name="3_3"),
            self.create_blue_boss_stage(name="blue_boss"),
            self.create_end_stage("end"),  # TODO: Fix. Not really a stage
        ]

    def get_by_name(self, name: str) -> Stage | BossStage:
        for stage in self:
            if stage.name == name:
                return stage
        # TODO: Raise proper error
        raise AssertionError

    def select(self, name: str) -> None:
        for stage in self:
            if stage.name == name:
                self.current = stage
                stage.setup()
                return
            self.current = stage
            stage.transit()
        # TODO: Raise proper error
        raise AssertionError

    def load_next_stage(self) -> Stage:
        prev_stage = self.current
        next_stage = self[prev_stage.index + 1]
        self.current = next_stage
        prev_stage.teardown()
        prev_stage.transit()
        next_stage.setup()
        log.info("%s -> %s", prev_stage, next_stage)
        return next_stage


def maybe_spawn_extra_health(settings: "Settings",
                             screen: "Surface",
                             stats: "GameStats",
                             ship: "Ship",
                             health: "GroupSingle") -> bool:
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


def maybe_spawn_extra_ammo(settings: "Settings",
                           screen: "Surface",
                           stats: "GameStats",
                           ship: "Ship",
                           ammo: "Group") -> bool:
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
