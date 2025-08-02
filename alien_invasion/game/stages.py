from itertools import count
from logging import getLogger
from typing import TYPE_CHECKING

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
                 ship: "Ship",
                 health,
                 ammo,
                 bullets,
                 alien_bullets,
                 name: str) -> None:
        super().__init__(name)

        self.settings = settings
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets

    def set_up(self) -> None:
        log.debug("%s: set_up()", self)
        self.settings.increase_aliens_speed()

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
                 ship,
                 health,
                 ammo,
                 bullets,
                 alien_bullets) -> None:
        self.settings = settings
        self.ship = ship
        self.health = health
        self.ammo = ammo
        self.bullets = bullets
        self.alien_bullets = alien_bullets

        super().__init__(self.create_stages())

        self.current = None

    def create_stage(self, name: str) -> Stage:
        return Stage(settings=self.settings,
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
