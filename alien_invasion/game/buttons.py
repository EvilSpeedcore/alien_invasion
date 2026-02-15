from typing import TYPE_CHECKING

from game.button import Button

if TYPE_CHECKING:
    from game.screen import Screen


class Buttons:

    def __init__(self, screen: "Screen") -> None:
        self.START = Button(surface=screen.it,
                            position={"center": (screen.rect.center)},
                            message="Start")
