import secrets
from itertools import chain
from time import sleep
from typing import TYPE_CHECKING

import pygame

from game.black_hole import BlackHole
from game.boss_bullets import BlueBossBullet, GreenBossBullet, RedBossBullet
from game.boss_shield import BlueBossShield, GreenBossShield, RedBossShield
from game.bosses import BlueBoss, GreenBoss, RedBoss
from game.bullet import Bullet
from game.paths import Paths
from game.rotation import Rotation, rotate_to_up
from game.ship_consumables import ShipShield

if TYPE_CHECKING:
    from pygame.sprite import Group, GroupSingle

    from game.boss_shield import BossShield
    from game.bosses import Boss
    from game.button import Button
    from game.hud import Hud
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stats import Stats


def initialize_game_from_main_menu(settings: "Settings", stats: "Stats", hud: "Hud", ship: "Ship") -> None:
    settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    ship.set_default_movement()
    hud.prep_health()
    hud.prep_ammo()
    hud.prep_shield()
    rotate_to_up(ship)


def handle_ship_diagonal_movement(ship: "Ship") -> None:
    # Check for UP_LEFT ship direction.
    if ship.moving_up and ship.moving_left:
        ship.current_ship_rotation = Rotation.UP_LEFT
        while ship.current_ship_rotation == Rotation.UP_LEFT:
            ship.image = ship.Images.UP_LEFT
            break

    # Check for UP_RIGHT ship direction.
    if ship.moving_up and ship.moving_right:
        ship.current_ship_rotation = Rotation.UP_RIGHT
        while ship.current_ship_rotation == Rotation.UP_RIGHT:
            ship.image = ship.Images.UP_RIGHT
            break

    # Check for DOWN_LEFT ship direction.
    if ship.moving_down and ship.moving_left:
        ship.current_ship_rotation = Rotation.DOWN_LEFT
        while ship.current_ship_rotation == Rotation.DOWN_LEFT:
            ship.image = ship.Images.DOWN_LEFT
            break

    # Check for DOWN_RIGHT ship direction.
    if ship.moving_down and ship.moving_right:
        ship.current_ship_rotation = Rotation.DOWN_RIGHT
        while ship.current_ship_rotation == Rotation.DOWN_RIGHT:
            ship.image = ship.Images.DOWN_RIGHT
            break


def update_screen(settings: "Settings",
                  screen: "Screen",
                  hud: "Hud",
                  ship: "Ship",
                  sprites: "Sprites",
                  dt: int) -> None:
    """Update screen."""
    screen.it.fill(settings.bg_color)

    for item in chain(
        sprites.ship_bullets.sprites(),
        sprites.alien_bullets.sprites(),
        sprites.boss_bullets.sprites(),
        sprites.ship_shields.sprites(),
        sprites.ship_health.sprites(),
        sprites.ship_health.sprites(),
        sprites.boss_black_holes.sprites(),
        sprites.bosses.sprites(),
        sprites.aliens.sprites(),
        (ship,),
    ):
        item.blitme()

    # Ship shield duration handling.
    if sprites.ship_shields:
        settings.time_elapsed_since_shield += dt
        if settings.time_elapsed_since_shield > 3000:
            settings.time_elapsed_since_shield = 0
            sprites.ship_shields.empty()

    # Display boss shield on hud.
    boss_shield: BossShield
    if boss_shield := sprites.boss_shields.sprite:
        if boss_shield.points > 0:
            boss_shield.draw_boss_shield()
            boss_shield.update()
        else:
            sprites.boss_shields.empty()

    hud.show_hud()

    # Update screen.
    pygame.display.flip()


def update_main_menu_screen(settings: "Settings", screen: "Screen", start_button: "Button") -> None:
    screen.it.fill(settings.bg_color)

    start_button.draw_button()

    # Update screen.
    pygame.display.flip()


def fire_bullet(settings: "Settings",
                screen: "Screen",
                stats: "Stats",
                ship: "Ship",
                bullets: "Group") -> None:
    """Create ship bullets."""
    if len(bullets) < stats.ammo:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_aliens_row_count(settings: "Settings", alien_width: int) -> int:
    available_space_x = settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def ship_hit_on_regular_stage(settings: "Settings",
                              stats: "Stats",
                              hud: "Hud",
                              ship: "Ship",
                              sprites: "Sprites") -> None:
    stats.ships_left -= 1
    hud.prep_health()
    sprites.ship_health.empty()
    sprites.ship_ammo.empty()
    sprites.ship_shields.empty()
    settings.time_elapsed_since_shield = 0

    sprites.alien_bullets.empty()
    sprites.aliens.empty()
    sprites.ship_bullets.empty()
    if stats.ships_left:
        ship.center_ship()
        rotate_to_up(ship)
        sleep(settings.game_sleep_time)


def ship_hit_on_boss_stage(settings: "Settings",
                           stats: "Stats",
                           hud: "Hud",
                           ship: "Ship",
                           sprites: "Sprites") -> None:
    stats.ships_left -= 1
    hud.prep_health()
    boss: Boss = sprites.bosses.sprite
    boss.set_default_hit_points()
    boss.prepare_health()
    sprites.ship_bullets.empty()
    sprites.bosses.empty()
    sprites.boss_bullets.empty()
    sprites.ship_shields.empty()
    settings.time_elapsed_since_shield = 0
    settings.time_elapsed_since_boss_shield = 0
    ship.prepare_for_boss()


def fire_green_boss_bullets(settings: "Settings",
                            screen: "Screen",
                            boss: "GreenBoss",
                            boss_bullets: "Group",
                            dt: int) -> None:
    """Create green boss bullets."""
    settings.time_elapsed_since_last_boss_bullet += dt
    if settings.time_elapsed_since_last_boss_bullet <= settings.green_boss_bullet_timer:
        return

    ranges = (range(180), range(90, 270), range(180, 360), range(270, 450))
    for range_ in ranges:
        bullet = GreenBossBullet(settings=settings, screen=screen, boss=boss)
        bullet.shooting_angle_up = secrets.choice(range_)
        boss_bullets.add(bullet)

    settings.time_elapsed_since_last_boss_bullet = 0
    settings.green_boss_bullet_timer = 1650


def use_ship_shield(screen: "Screen",
                    stats: "Stats",
                    hud: "Hud",
                    ship: "Ship",
                    used_shields: "Group") -> None:
    """Handle use of ship shield."""
    if stats.shields_left:
        effect = pygame.mixer.Sound(Paths.effects() / "1.ogg")
        effect.play()
        used_shield = ShipShield(screen, ship)
        used_shields.add(used_shield)
        stats.shields_left -= 1
        hud.prep_shield()


def create_green_boss(screen: "Screen", sprites: "Sprites") -> None:
    """Create green boss."""
    boss = GreenBoss(screen=screen, boss_health=sprites.boss_health)
    boss_shield = GreenBossShield(screen, position=(boss.rect.centerx, boss.rect.centery))
    boss.set_default_hit_points()
    boss.prepare_health()
    sprites.bosses.add(boss)
    sprites.boss_shields.add(boss_shield)


def create_blue_boss(screen: "Screen", sprites: "Sprites") -> None:
    """Create blue boss."""
    blue_boss = BlueBoss(screen=screen, boss_health=sprites.boss_health)
    boss_shield = BlueBossShield(screen, blue_boss)
    blue_boss.set_default_hit_points()
    blue_boss.prepare_health()
    sprites.bosses.add(blue_boss)
    sprites.boss_shields.add(boss_shield)


def update_green_boss_bullets(boss_bullets: "Group[GreenBossBullet]") -> None:
    for green_boss_bullet in boss_bullets.copy():
        if green_boss_bullet.bounces > 3:
            boss_bullets.remove(green_boss_bullet)
        else:
            green_boss_bullet.change_direction()


def create_red_boss(settings: "Settings", screen: "Screen", sprites: "Sprites") -> None:
    """Create red boss."""
    red_boss = RedBoss(settings=settings, screen=screen, boss_health=sprites.boss_health)
    boss_shield = RedBossShield(screen, red_boss)
    red_boss.set_default_hit_points()
    red_boss.prepare_health()
    sprites.bosses.add(red_boss)
    sprites.boss_shields.add(boss_shield)


def fire_red_boss_bullets(settings: "Settings",
                          screen: "Screen",
                          ship: "Ship",
                          bosses: "GroupSingle",
                          boss_bullets: "Group",
                          dt: int) -> None:
    """Create red boss bullets."""
    settings.time_elapsed_since_last_red_boss_bullet += dt
    if settings.time_elapsed_since_last_red_boss_bullet <= 1350:
        return

    boss: RedBoss | None
    if not (boss := bosses.sprite):
        return

    for angle in (0, 15, 30, -15, -30):
        bullet = RedBossBullet(settings, screen, boss)
        bullet.define_position(ship)
        bullet.shooting_angle = bullet.shooting_angle + angle
        boss_bullets.add(bullet)

    settings.time_elapsed_since_last_red_boss_bullet = 0


def fire_blue_boss_bullets(settings: "Settings",
                           screen: "Screen",
                           bosses: "GroupSingle",
                           boss_bullets: "Group",
                           dt: int) -> None:
    """Create blue boss bullets."""
    settings.time_elapsed_since_last_blue_boss_bullet += dt
    if settings.time_elapsed_since_last_blue_boss_bullet <= 300:
        return

    boss: BlueBoss | None
    if not (boss := bosses.sprite):
        return

    angles = (30, 120, 210, 300)
    bullets = (BlueBossBullet(settings, screen, boss, boss.shooting_angle + angle) for angle in angles)
    boss_bullets.add(bullets)

    settings.time_elapsed_since_last_blue_boss_bullet = 0
    if boss.rt_trigger:
        boss.shooting_angle += 15
        if boss.shooting_angle > 400:
            boss.rt_trigger = False
    else:
        boss.shooting_angle -= 15
        if boss.shooting_angle < 0:
            boss.rt_trigger = True


def maybe_create_black_hole(settings: "Settings",
                            screen: "Screen",
                            ship: "Ship",
                            black_holes: "GroupSingle") -> None:
    if not black_holes and settings.black_hole_spawn_timer > 2000:
        black_holes.add(BlackHole(settings, screen, ship))


def update_black_hole(settings: "Settings", black_holes: "GroupSingle", dt: int) -> None:
    """Update black hole animation."""
    settings.black_hole_spawn_timer += dt
    if black_holes and settings.black_hole_spawn_timer > 6000:
        black_holes.empty()
        settings.black_hole_spawn_timer = 0
        return

    black_hole: BlackHole | None
    if not (black_hole := black_holes.sprite):
        return

    settings.black_hole_rotation_timer += dt
    if settings.black_hole_rotation_timer <= 300:
        return

    black_hole.update()
    settings.black_hole_rotation_timer = 0
