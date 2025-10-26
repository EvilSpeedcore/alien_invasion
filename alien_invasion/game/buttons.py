from typing import TYPE_CHECKING

from game.button import StartButton

if TYPE_CHECKING:
    from game.screen import Screen


class Buttons:

    def __init__(self, screen: "Screen") -> None:
        self.START = StartButton(screen)
