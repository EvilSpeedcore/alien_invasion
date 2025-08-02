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

    @abstractmethod
    def set_up(self) -> None:
        log.debug("%s: set_up()", self)

    @abstractmethod
    def transit(self) -> None:
        log.debug("%s: transit()", self)

    @abstractmethod
    def tear_down(self) -> None:
        log.debug("%s: tear_down()", self)


class Stage(BaseStage):

    def __init__(self,
                 stages: "Stages",
                 settings: "Settings",
                 screen,
                 stats,
                 aliens,
                 ship: "Ship",
                 health,
                 ammo,
                 bullets,
                 alien_bullets,
                 used_shields,
                 name: str) -> None:
        super().__init__(name)

        self.stages = stages
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.aliens = aliens
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets
        self.used_shields = used_shields

    def set_up(self) -> None:
        super().set_up()
        self.ship.center_ship()

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

        gf.create_fleet(ai_settings=self.settings,
                        screen=self.screen,
                        stages=self.stages,
                        ship=self.ship,
                        aliens=self.aliens)

    def transit(self) -> None:
        super().transit()
        # do not increase speed if next stage is a boss stage
        # TODO: self.stages.current is confusing
        #       (we set current to early),
        #       change to self.stages.next
        if not isinstance(self.stages.current, BossStage):
            self.settings.increase_aliens_speed()

    def tear_down(self) -> None:
        super().tear_down()
        self.health.empty()
        self.ammo.empty()
        self.alien_bullets.empty()
        self.bullets.empty()
        self.used_shields.empty()


class BossStage(BaseStage):

    def __init__(self,
                 ship: "Ship",
                 boss_health,
                 boss_shields,
                 name: str) -> None:
        super().__init__(name)

        self.ship = ship
        self.boss_health = boss_health
        self.boss_shields = boss_shields

    def set_up(self) -> None:
        super().set_up()
        self.ship.prepare_for_boss()
        rt.rotate_to_up(self.ship)

    def tear_down(self) -> None:
        super().tear_down()
        self.boss_health.empty()
        self.boss_shields.empty()


class GreenBossStage(BossStage):

    def __init__(self,
                 settings: "Settings",
                 screen,
                 hud,
                 ship: "Ship",
                 bosses,
                 boss_health,
                 boss_shields,
                 name: str) -> None:
        super().__init__(ship=ship,
                         boss_health=boss_health,
                         boss_shields=boss_shields,
                         name=name)

        self.settings = settings
        self.screen = screen
        self.hud = hud
        self.bosses = bosses

    def set_up(self) -> None:
        super().set_up()
        gf.create_green_boss(ai_settings=self.settings,
                             screen=self.screen,
                             hud=self.hud,
                             bosses=self.bosses,
                             boss_shields=self.boss_shields)


class RedBossStage(GreenBossStage):

    def set_up(self) -> None:
        super(GreenBossStage, self).set_up()
        gf.create_red_boss(ai_settings=self.settings,
                           screen=self.screen,
                           hud=self.hud,
                           bosses=self.bosses,
                           boss_shields=self.boss_shields)


class BlueBossStage(BossStage):

    def __init__(self,
                 settings: "Settings",
                 screen,
                 hud,
                 ship: "Ship",
                 bosses,
                 boss_health,
                 boss_shields,
                 black_holes,
                 name: str) -> None:
        super().__init__(ship=ship,
                         boss_health=boss_health,
                         boss_shields=boss_shields,
                         name=name)

        self.settings = settings
        self.screen = screen
        self.hud = hud
        self.bosses = bosses
        self.black_holes = black_holes

    def set_up(self) -> None:
        super().set_up()
        gf.create_blue_boss(ai_settings=self.settings,
                            screen=self.screen,
                            hud=self.hud,
                            bosses=self.bosses,
                            boss_shields=self.boss_shields)

    def tear_down(self) -> None:
        super().tear_down()
        self.black_holes.empty()


class Stages(list[Stage | BossStage]):

    def __init__(self,
                 settings: "Settings",
                 screen,
                 stats,
                 hud,
                 aliens,
                 ship,
                 health,
                 ammo,
                 bullets,
                 alien_bullets,
                 used_shields,
                 bosses,
                 boss_health,
                 boss_shields,
                 black_holes) -> None:
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.hud = hud
        self.aliens = aliens
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets
        self.used_shields = used_shields
        self.bosses = bosses
        self.boss_health = boss_health
        self.boss_shields = boss_shields
        self.black_holes = black_holes

        super().__init__(self.create_stages())

        self.current = None

    def create_stage(self, name: str) -> Stage:
        return Stage(stages=self,
                     settings=self.settings,
                     screen=self.screen,
                     stats=self.stats,
                     aliens=self.aliens,
                     ship=self.ship,
                     health=self.health,
                     ammo=self.ammo,
                     bullets=self.bullets,
                     alien_bullets=self.alien_bullets,
                     used_shields=self.used_shields,
                     name=name)

    def create_boss_stage(self, name: str) -> BossStage:
        return BossStage(ship=self.ship,
                         boss_health=self.boss_health,
                         boss_shields=self.boss_shields,
                         name=name)

    def create_green_boss_stage(self, name: str) -> GreenBossStage:
        return GreenBossStage(settings=self.settings,
                              screen=self.screen,
                              hud=self.hud,
                              ship=self.ship,
                              bosses=self.bosses,
                              boss_health=self.boss_health,
                              boss_shields=self.boss_shields,
                              name=name)

    def create_red_boss_stage(self, name: str) -> GreenBossStage:
        return RedBossStage(settings=self.settings,
                            screen=self.screen,
                            hud=self.hud,
                            ship=self.ship,
                            bosses=self.bosses,
                            boss_health=self.boss_health,
                            boss_shields=self.boss_shields,
                            name=name)

    def create_blue_boss_stage(self, name: str) -> None:
        return BlueBossStage(settings=self.settings,
                             screen=self.screen,
                             hud=self.hud,
                             bosses=self.bosses,
                             ship=self.ship,
                             boss_health=self.boss_health,
                             boss_shields=self.boss_shields,
                             black_holes=self.black_holes,
                             name=name)

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
            BaseStage(name="end"),  # TODO: Fix. Not really a stage
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
                stage.set_up()
                return
            self.current = stage
            stage.transit()
        # TODO: Raise proper error
        raise AssertionError

    def load_next_stage(self) -> Stage:
        prev_stage = self.current
        next_stage = self[prev_stage.index + 1]
        self.current = next_stage
        prev_stage.tear_down()
        prev_stage.transit()
        next_stage.set_up()
        log.info("%s -> %s", prev_stage, next_stage)
        return next_stage


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
