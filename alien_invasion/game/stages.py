import secrets
from abc import abstractmethod
from itertools import count
from logging import getLogger
from typing import TYPE_CHECKING

import pygame

import game.game_functions as gf
import game.rotation as rt
from game.ship_consumables import ShipAmmo, ShipHealth

log = getLogger(__name__)

type StageTypes = "BossStage" | "Stage" | "EndStage"


if TYPE_CHECKING:
    from pygame.sprite import Group

    from game.hud import Hud
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stats import Stats


class BaseStage:

    counter = count(start=0)

    def __init__(self, sprites: "Sprites", name: str) -> None:
        self.sprites = sprites
        self.name = name

        self.index = next(self.counter)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, other: object) -> bool:
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
    def check_collision(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

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
                 screen: "Screen",
                 hud: "Hud",
                 stats: "Stats",
                 ship: "Ship",
                 sprites: "Sprites",
                 name: str) -> None:
        super().__init__(sprites=sprites, name=name)
        self.stages = stages
        self.settings = settings
        self.screen = screen
        self.hud = hud
        self.stats = stats
        self.ship = ship

    def setup(self) -> None:
        super().setup()
        self.ship.center_ship()

        if not maybe_spawn_extra_health(screen=self.screen,
                                        stats=self.stats,
                                        ship=self.ship,
                                        health=self.sprites.ship_health):
            maybe_spawn_extra_ammo(screen=self.screen,
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

    def check_collision(self) -> None:
        # Ship bullets and aliens
        pygame.sprite.groupcollide(self.sprites.ship_bullets,
                                   self.sprites.aliens,
                                   dokilla=True, dokillb=True)

        # Ship and aliens
        gf.check_ship_aliens_collision(settings=self.settings,
                                       screen=self.screen,
                                       stats=self.stats,
                                       stages=self.stages,
                                       hud=self.hud,
                                       ship=self.ship,
                                       sprites=self.sprites)

        # Ship shield and alien bullets
        pygame.sprite.groupcollide(self.sprites.ship_shields,
                                   self.sprites.alien_bullets,
                                   dokilla=False, dokillb=True)

        # Ship and alien bullets
        gf.check_ship_alien_bullets_collision(settings=self.settings,
                                              screen=self.screen,
                                              stats=self.stats,
                                              stages=self.stages,
                                              hud=self.hud,
                                              ship=self.ship,
                                              sprites=self.sprites)

        # Ship and health
        gf.check_ship_health_collision(stats=self.stats,
                                       hud=self.hud,
                                       ship=self.ship,
                                       health=self.sprites.ship_health)

        # Ship and ammon
        gf.check_ship_ammo_collision(stats=self.stats,
                                     hud=self.hud,
                                     ship=self.ship,
                                     ammo=self.sprites.ship_ammo)

    def update(self) -> None:
        self.sprites.aliens.update(self.sprites.aliens, self.ship)
        gf.update_bullets(self.screen, self.sprites.alien_bullets)

    def teardown(self) -> None:
        super().teardown()
        self.sprites.alien_bullets.empty()


class BossStage(BaseStage):

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 stats: "Stats",
                 stages: "Stages",
                 hud: "Hud",
                 ship: "Ship",
                 sprites: "Sprites",
                 name: str) -> None:
        super().__init__(sprites=sprites, name=name)
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.stages = stages
        self.hud = hud
        self.ship = ship

    def setup(self) -> None:
        super().setup()
        self.ship.prepare_for_boss()
        rt.rotate_to_up(self.ship)

    def transit(self) -> None:
        super().transit()

    def check_collision(self) -> None:
        # Ship shield and boss bullets
        pygame.sprite.groupcollide(self.sprites.ship_shields,
                                   self.sprites.boss_bullets,
                                   dokilla=False, dokillb=True)
        # Ship and boss bullets
        gf.check_ship_boss_bullets_collision(settings=self.settings,
                                             screen=self.screen,
                                             stats=self.stats,
                                             stages=self.stages,
                                             hud=self.hud,
                                             ship=self.ship,
                                             sprites=self.sprites)
        # Ship and bosses
        gf.check_ship_bosses_collision(settings=self.settings,
                                       screen=self.screen,
                                       stats=self.stats,
                                       stages=self.stages,
                                       hud=self.hud,
                                       ship=self.ship,
                                       sprites=self.sprites)

        # Ship bullets and bosses
        gf.check_ship_bullets_boss_collision(settings=self.settings, sprites=self.sprites)

        # Ship bullets and boss shield
        gf.check_ship_bullets_boss_shield_collision(self.sprites)

    def update(self) -> None:
        pass

    def teardown(self) -> None:
        super().teardown()
        self.sprites.boss_health.empty()
        self.sprites.boss_shields.empty()


class GreenBossStage(BossStage):

    def setup(self) -> None:
        super().setup()
        gf.create_green_boss(settings=self.settings, screen=self.screen, sprites=self.sprites)


class RedBossStage(BossStage):

    def setup(self) -> None:
        super().setup()
        gf.create_red_boss(settings=self.settings, screen=self.screen, sprites=self.sprites)

    def update(self) -> None:
        self.sprites.bosses.sprite.update()
        gf.update_bullets(self.screen, self.sprites.boss_bullets)


class BlueBossStage(BossStage):

    def setup(self) -> None:
        super().setup()
        gf.create_blue_boss(settings=self.settings, screen=self.screen, sprites=self.sprites)

    def update(self) -> None:
        gf.update_bullets(self.screen, self.sprites.boss_bullets)

    def teardown(self) -> None:
        super().teardown()
        self.sprites.boss_black_holes.empty()


class EndStage(BaseStage):

    def setup(self) -> None:
        pass

    def transit(self) -> None:
        pass

    def check_collision(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def update(self) -> None:
        pass


class Stages(list[StageTypes]):

    def __init__(self,
                 settings: "Settings",
                 screen: "Screen",
                 stats: "Stats",
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

        self.current: StageTypes = self[0]

    @property
    def end(self) -> bool:
        return self.current == self[-1] if self.current else False

    def create_stage(self, name: str) -> Stage:
        return Stage(stages=self,
                     settings=self.settings,
                     screen=self.screen,
                     hud=self.hud,
                     stats=self.stats,
                     ship=self.ship,
                     sprites=self.sprites,
                     name=name)

    def create_green_boss_stage(self, name: str) -> GreenBossStage:
        return GreenBossStage(settings=self.settings,
                              screen=self.screen,
                              stats=self.stats,
                              hud=self.hud,
                              stages=self,
                              ship=self.ship,
                              sprites=self.sprites,
                              name=name)

    def create_red_boss_stage(self, name: str) -> RedBossStage:
        return RedBossStage(settings=self.settings,
                            screen=self.screen,
                            stats=self.stats,
                            hud=self.hud,
                            stages=self,
                            ship=self.ship,
                            sprites=self.sprites,
                            name=name)

    def create_blue_boss_stage(self, name: str) -> BlueBossStage:
        return BlueBossStage(settings=self.settings,
                             screen=self.screen,
                             stats=self.stats,
                             hud=self.hud,
                             stages=self,
                             ship=self.ship,
                             sprites=self.sprites,
                             name=name)

    def create_end_stage(self, name: str) -> EndStage:
        return EndStage(sprites=self.sprites, name=name)

    def create_stages(self) -> list[StageTypes]:
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
            self.create_end_stage("end"),  # TODO: Not a stage
        ]

    def get_by_name(self, name: str) -> StageTypes:
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

    def load_next_stage(self) -> StageTypes:
        prev_stage = self.current
        next_stage = self[prev_stage.index + 1]
        self.current = next_stage
        prev_stage.teardown()
        prev_stage.transit()
        next_stage.setup()
        log.info("%s -> %s", prev_stage, next_stage)
        return next_stage


def maybe_spawn_consumable(screen: "Screen",
                           ship: "Ship",
                           group: "Group",
                           consumable: ShipHealth | ShipAmmo) -> bool:
    if secrets.choice(range(5)):
        return False

    x_padding = consumable.rect.width * 3
    y_padding = consumable.rect.height * 3
    # left x
    left_x = range(screen.rect.left + x_padding, ship.rect.left - x_padding)
    # right x
    right_x = range(ship.rect.right + x_padding, screen.rect.right - x_padding)
    # top y
    top_y = range(screen.rect.top + y_padding, ship.rect.top - y_padding)
    # bottom y
    bottom_y = range(ship.rect.bottom + y_padding, screen.rect.bottom - y_padding)

    consumable.rect.x = secrets.choice(secrets.choice([left_x or right_x, right_x or left_x]))
    consumable.rect.y = secrets.choice(secrets.choice([top_y or bottom_y, bottom_y or top_y]))
    group.add(consumable)
    return True


def maybe_spawn_extra_health(screen: "Screen",
                             stats: "Stats",
                             ship: "Ship",
                             health: "Group") -> bool:
    if stats.ships_left > 3:
        return False
    consumable = ShipHealth(screen)
    return maybe_spawn_consumable(screen=screen,
                                  ship=ship,
                                  group=health,
                                  consumable=consumable)


def maybe_spawn_extra_ammo(screen: "Screen",
                           ship: "Ship",
                           ammo: "Group") -> bool:
    consumable = ShipAmmo(screen)
    return maybe_spawn_consumable(screen=screen,
                                  ship=ship,
                                  group=ammo,
                                  consumable=consumable)
