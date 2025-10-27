from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.ship import Ship


class Rotation(Enum):
    UP         = auto()
    RIGHT      = auto()
    LEFT       = auto()
    DOWN       = auto()
    UP_RIGHT   = auto()
    UP_LEFT    = auto()
    DOWN_LEFT  = auto()
    DOWN_RIGHT = auto()


def rotate(ship: "Ship") -> None:
    """Change ship direction."""
    if ship.current_ship_rotation == ship.desirable_ship_rotation:
        return

    match ship.desirable_ship_rotation:
        case Rotation.UP:
            rotate_to_up(ship)
        case Rotation.RIGHT:
            rotate_to_right(ship)
        case Rotation.LEFT:
            rotate_to_left(ship)
        case Rotation.DOWN:
            rotate_to_down(ship)


def rotate_to_up(ship: "Ship") -> None:
    ship.image = ship.Images.UP
    ship.current_ship_rotation = Rotation.UP


def rotate_to_right(ship: "Ship") -> None:
    ship.image = ship.Images.RIGHT
    ship.current_ship_rotation = Rotation.RIGHT


def rotate_to_left(ship: "Ship") -> None:
    ship.image = ship.Images.LEFT
    ship.current_ship_rotation = Rotation.LEFT


def rotate_to_down(ship: "Ship") -> None:
    ship.image = ship.Images.DOWN
    ship.current_ship_rotation = Rotation.DOWN
