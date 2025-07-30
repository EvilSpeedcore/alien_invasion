from itertools import count
from typing import ClassVar


class Stage:

    counter = count(start=0)

    def __init__(self, name: str) -> None:
        self.index = next(self.counter)
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __eq__(self, other) -> None:
        if isinstance(other, Stage):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


class BossStage(Stage):
    pass


class Stages:

    lst: ClassVar[list[Stage]] = [
        Stage(name="1_1"),
        Stage(name="1_2"),
        Stage(name="1_3"),
        BossStage(name="green_boss"),
        Stage(name="2_1"),
        Stage(name="2_2"),
        Stage(name="2_3"),
        BossStage(name="red_boss"),
        Stage(name="2_5"),
        Stage(name="2_6"),
        Stage(name="2_7"),
        BossStage(name="blue_boss"),
        Stage(name="end"),  # TODO: Fix. Not really a stage
    ]

    def __init__(self) -> None:
        self.current = None

    def get_by_name(self, name: str) -> Stage | BossStage:
        for stage in self.lst:
            if stage.name == name:
                return stage
        # TODO: Raise proper error
        raise AssertionError

    def select(self, name: str) -> None:
        self.current = self.get_by_name(name)

    def next_stage(self) -> Stage:
        prev_stage = self.current
        next_stage = self.lst[prev_stage.index + 1]
        self.current = next_stage
        return next_stage

    def reset(self) -> None:
        self.current = self.lst[0]
