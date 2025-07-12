from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.ship import Ship


def rotate(ship: "Ship") -> None:
    """Change ship direction.

    Args:
        :param Ship ship: Instance of Ship class.

    """
    if ship.current_ship_rotation == ship.desirable_ship_rotation:
        return

    if ship.desirable_ship_rotation == "up":
        rotate_to_up(ship)
    if ship.desirable_ship_rotation == "right":
        rotate_to_right(ship)
    if ship.desirable_ship_rotation == "left":
        rotate_to_left(ship)
    if ship.desirable_ship_rotation == "down":
        rotate_to_down(ship)


def rotate_to_up(ship: "Ship") -> None:
    """Rotate ship to UP direction.

    Args:
        :param ship: Instance of Ship class.

    """
    ship.image = ship.original_image
    ship.current_ship_rotation = "up"


def rotate_to_right(ship: "Ship") -> None:
    """Rotate ship to RIGHT direction."""
    ship.image = ship.original_image_right
    ship.current_ship_rotation = "right"


def rotate_to_left(ship: "Ship") -> None:
    """Rotate ship to LEFT direction."""
    ship.image = ship.original_image_left
    ship.current_ship_rotation = "left" 


def rotate_to_down(ship: "Ship") -> None:
    """Rotate ship to DOWN direction."""
    ship.image = ship.original_image_down
    ship.current_ship_rotation = "down"
