from typing import TYPE_CHECKING

from game.screen import ScreenSide

if TYPE_CHECKING:
    from game.ship import Ship


def rotate(ship: "Ship") -> None:
    """Change ship direction."""
    if ship.current_ship_rotation == ship.desirable_ship_rotation:
        return

    match ship.desirable_ship_rotation:
        case ScreenSide.TOP:
            rotate_to_up(ship)
        case ScreenSide.RIGHT:
            rotate_to_right(ship)
        case ScreenSide.LEFT:
            rotate_to_left(ship)
        case ScreenSide.BOTTOM:
            rotate_to_down(ship)


def rotate_to_up(ship: "Ship") -> None:
    ship.image = ship.Images.UP
    ship.current_ship_rotation = ScreenSide.TOP


def rotate_to_right(ship: "Ship") -> None:
    ship.image = ship.Images.RIGHT
    ship.current_ship_rotation = ScreenSide.RIGHT


def rotate_to_left(ship: "Ship") -> None:
    ship.image = ship.Images.LEFT
    ship.current_ship_rotation = ScreenSide.LEFT


def rotate_to_down(ship: "Ship") -> None:
    ship.image = ship.Images.DOWN
    ship.current_ship_rotation = ScreenSide.BOTTOM
