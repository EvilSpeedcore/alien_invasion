import math
from enum import Enum, auto
from typing import TYPE_CHECKING

from game import find_angle as fa

if TYPE_CHECKING:
    from game.alien_bullet import AlienBullet
    from game.boss_bullets import RedBossBullet
    from game.ship import Ship


class ShipToBulletPosition(Enum):
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()


def define_direct_bullet_angle(bullet: "AlienBullet | RedBossBullet", ship: "Ship") -> None:
    ab = abs(bullet.y - ship.centery)
    ac = abs(bullet.x - ship.centerx)
    bc = math.sqrt(pow(ab, 2) + pow(ac, 2))
    bullet.shooting_angle_cos = ac / bc
    bullet.shooting_angle = fa.find_angle_with_cos(bullet.shooting_angle_cos)


def define_direct_bullet_position(bullet: "AlienBullet | RedBossBullet", ship: "Ship") -> None:
    if (bullet.x < ship.centerx and bullet.y < ship.centery) or (
        bullet.x < ship.centerx and bullet.y == ship.centery
    ):
        bullet.ship_position = ShipToBulletPosition.DOWN_RIGHT
    elif (bullet.x < ship.centerx and bullet.y > ship.centery) or (
        bullet.x == ship.centerx and bullet.y > ship.centery
    ):
        bullet.ship_position = ShipToBulletPosition.UP_RIGHT
    elif (bullet.x > ship.centerx and bullet.y > ship.centery) or (
        bullet.x > ship.centerx and bullet.y == ship.centery
    ):
        bullet.ship_position = ShipToBulletPosition.UP_LEFT
    elif (bullet.x > ship.centerx and bullet.y < ship.centery) or (
        bullet.x == ship.centerx and bullet.y < ship.centery
    ):
        bullet.ship_position = ShipToBulletPosition.DOWN_LEFT
    else:
        raise AssertionError
    define_direct_bullet_angle(bullet=bullet, ship=ship)


def update_direct_bullet(bullet: "AlienBullet | RedBossBullet") -> None:
    match bullet.ship_position:
        case ShipToBulletPosition.DOWN_RIGHT:
            radians = math.radians(360 - bullet.shooting_angle)
        case ShipToBulletPosition.UP_RIGHT:
            radians = math.radians(bullet.shooting_angle)
        case ShipToBulletPosition.UP_LEFT:
            radians = math.radians(180 - bullet.shooting_angle)
        case ShipToBulletPosition.DOWN_LEFT:
            radians = math.radians(180 + bullet.shooting_angle)

    bullet_move_x = bullet.speed * math.cos(radians)
    bullet_move_y = -bullet.speed * math.sin(radians)
    bullet.x += bullet_move_x
    bullet.y += bullet_move_y
    bullet.rect.centerx = bullet.x  # type: ignore[assignment]
    bullet.rect.centery = bullet.y  # type: ignore[assignment]
