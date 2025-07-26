from enum import Enum, auto


class State(Enum):

    ACTIVE = auto()
    PAUSED = auto()
    MAIN_MENU = auto()


class GameState:

    def __init__(self, initial: State) -> None:
        self._state = initial

    def __call__(self, state: State) -> bool:
        return self._state == state

    def set(self, state: State) -> None:
        self._state = state
