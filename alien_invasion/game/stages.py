from itertools import count
from logging import getLogger
from typing import TYPE_CHECKING

log = getLogger(__name__)


if TYPE_CHECKING:
    from game.settings import Settings


class Stage:

    counter = count(start=0)

    def __init__(self, settings: "Settings", name: str) -> None:
        self.name = name
        self.settings = settings

        self.index = next(self.counter)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, other) -> None:
        if isinstance(other, Stage):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def set_up(self) -> None:
        self.settings.increase_aliens_speed()


class BossStage(Stage):

    def set_up(self) -> None:
        pass


class Stages(list[Stage | BossStage]):

    def __init__(self, settings: "Settings") -> None:
        super().__init__(create_stages(settings))

        self.current = None

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
        next_stage.set_up()
        log.info("%s -> %s", prev_stage, next_stage)
        return next_stage

    def reset(self) -> None:
        self.current = self[0]


def create_stages(settings: "Settings") -> list[Stage | BossStage]:
    return [
        Stage(settings, name="1_1"),
        Stage(settings, name="1_2"),
        Stage(settings, name="1_3"),
        BossStage(settings, name="green_boss"),
        Stage(settings, name="2_1"),
        Stage(settings, name="2_2"),
        Stage(settings, name="2_3"),
        BossStage(settings, name="red_boss"),
        Stage(settings, name="2_5"),
        Stage(settings, name="2_6"),
        Stage(settings, name="2_7"),
        BossStage(settings, name="blue_boss"),
        Stage(settings, name="end"),  # TODO: Fix. Not really a stage
    ]
