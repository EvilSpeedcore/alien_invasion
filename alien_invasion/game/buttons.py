from typing import TYPE_CHECKING

from game.button import Button

if TYPE_CHECKING:
    from game.screen import Screen


class Buttons:

    def __init__(self, screen: "Screen") -> None:
        self.START = Button(screen=screen, message="Start")
