def rotate(ship):
    """Change ship direction.

    Args:
        :param ship: Instance of Ship class.

    """
    if ship.current_ship_rotation == ship.desirable_ship_rotation:
        pass
    else:
        if ship.desirable_ship_rotation == "up":
            rotate_to_up(ship)
        if ship.desirable_ship_rotation == "right":
            rotate_to_right(ship)
        if ship.desirable_ship_rotation == "left":
            rotate_to_left(ship)
        if ship.desirable_ship_rotation == "down":
            rotate_to_down(ship)


def rotate_to_up(ship):
    """Rotate ship to UP direction.

    Args:
        :param ship: Instance of Ship class.

    """
    ship.image = ship.original_image
    ship.current_ship_rotation = "up"


def rotate_to_right(ship):
    """Rotate ship to RIGHT direction."""
    ship.image = ship.original_image_right
    ship.current_ship_rotation = "right"


def rotate_to_left(ship):
    """Rotate ship to LEFT direction."""
    ship.image = ship.original_image_left
    ship.current_ship_rotation = "left" 


def rotate_to_down(ship):
    """Rotate ship to DOWN direction."""
    ship.image = ship.original_image_down
    ship.current_ship_rotation = "down"
