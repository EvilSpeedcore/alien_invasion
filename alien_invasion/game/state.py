from enum import Enum, auto
from logging import getLogger

log = getLogger(__name__)


class State(Enum):

    ACTIVE = auto()
    PAUSED = auto()
    MAIN_MENU = auto()


class GameState:

    def __init__(self, initial: State) -> None:
        self._state = initial

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._state})"

    def __call__(self, state: State) -> bool:
        return self._state == state

    def set(self, state: State) -> None:
        log.info("%s -> %s", self._state, state)
        self._state = state
