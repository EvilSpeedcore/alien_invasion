import secrets
from itertools import chain
from time import sleep
from typing import TYPE_CHECKING

import pygame

import game.rotation as rt
from game.alien import Alien
from game.alien_bullet import AlienBullet
from game.black_hole import BlackHole
from game.boss_shield import BlueBossShield, GreenBossShield, RedBossShield
from game.bosses import BlueBoss, GreenBoss, RedBoss
from game.bosses_bullets import BlueBossBullet, GreenBossBullet, RedBossBullet
from game.bullet import Bullet
from game.paths import Paths
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
    from game.stages import Stages
    from game.stats import Stats


def initialize_game_from_main_menu(settings: "Settings", stats: "Stats", hud: "Hud", ship: "Ship") -> None:
    settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    ship.set_default_movement()
    hud.prep_health()
    hud.prep_ammo()
    hud.prep_shield()
    rt.rotate_to_up(ship)


def handle_ship_diagonal_movement(ship: "Ship") -> None:
    # Check for UP_LEFT ship direction.
    if ship.moving_up and ship.moving_left:
        ship.current_ship_rotation = "up-left"
        while ship.current_ship_rotation == "up-left":
            ship.image = ship.original_image_up_left
            break

    # Check for UP_RIGHT ship direction.
    if ship.moving_up and ship.moving_right:
        ship.current_ship_rotation = "up-right"
        while ship.current_ship_rotation == "up-right":
            ship.image = ship.original_image_up_right
            break

    # Check for DOWN_LEFT ship direction.
    if ship.moving_down and ship.moving_left:
        ship.current_ship_rotation = "down-left"
        while ship.current_ship_rotation == "down-left":
            ship.image = ship.original_image_down_left
            break

    # Check for DOWN_RIGHT ship direction.
    if ship.moving_down and ship.moving_right:
        ship.current_ship_rotation = "down-right"
        while ship.current_ship_rotation == "down-right":
            ship.image = ship.original_image_down_right
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


def update_main_menu_screen(settings: "Settings", screen: "Screen", play_button: "Button") -> None:
    screen.it.fill(settings.bg_color)

    # Show start button and clear the screen.
    play_button.prep_msg(play_button.msg)
    play_button.draw_button()

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


def get_number_aliens_x(settings: "Settings", alien_width: int) -> int:
    """Calculate number of aliens in row."""
    available_space_x = settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def create_alien(settings: "Settings",
                 screen: "Screen",
                 stages: "Stages",
                 ship: "Ship",
                 aliens: "Group",
                 alien_number: int) -> None:
    """Create an alien and place it in a row."""
    alien = Alien(settings, screen, ship)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # TODO: Rework
    if stages.current.index < stages.get_by_name("green_boss").index:
        pass
    elif stages.current.index < stages.get_by_name("red_boss").index:
        alien.image = alien.red_alien
    elif stages.current.index < stages.get_by_name("blue_boss").index:
        alien.image = alien.blue_alien
    aliens.add(alien)


def create_fleet(settings: "Settings",
                 screen: "Screen",
                 stages: "Stages",
                 ship: "Ship",
                 aliens: "Group") -> None:
    """Create alien fleet."""
    alien = Alien(settings, screen, ship)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    for alien_number in range(number_aliens_x):
        create_alien(settings, screen, stages, ship, aliens, alien_number)


def ship_hit(settings: "Settings",
             screen: "Screen",
             stats: "Stats",
             stages: "Stages",
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
        create_fleet(settings, screen, stages, ship, sprites.aliens)
        ship.center_ship()
        sleep(settings.game_sleep_time)


def ship_hit_at_boss_stage(settings: "Settings",
                           screen: "Screen",
                           stats: "Stats",
                           stages: "Stages",
                           hud: "Hud",
                           ship: "Ship",
                           sprites: "Sprites") -> None:
    """Handle collisions between ship and bosses."""
    # Handle collisions between ship and green boss.
    # TODO: Rework.
    if stages.current.name == "green_boss":
        stats.ships_left -= 1
        hud.prep_health()
        boss: Boss = sprites.bosses.sprite
        boss.set_default_hit_points()
        boss.prepare_health()

        # Ship and boss timers refresh.
        settings.time_elapsed_since_shield = 0
        settings.time_elapsed_since_boss_shield = 0

        sprites.ship_bullets.empty()
        sprites.bosses.empty()
        sprites.boss_bullets.empty()
        sprites.ship_shields.empty()

        if stats.ships_left:
            create_green_boss(settings=settings, screen=screen, sprites=sprites)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)

    # Handle collisions between ship and red boss.
    elif stages.current.name == "red_boss":
        stats.ships_left -= 1
        hud.prep_health()
        boss = sprites.bosses.sprite
        boss.set_default_hit_points()
        boss.prepare_health()

        # Ship and boss timers refresh.
        settings.time_elapsed_since_shield = 0
        settings.time_elapsed_since_boss_shield = 0

        sprites.ship_bullets.empty()
        sprites.bosses.empty()
        sprites.boss_bullets.empty()
        sprites.ship_shields.empty()

        if stats.ships_left:
            create_red_boss(settings=settings, screen=screen, sprites=sprites)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)

    # Handle collisions between ship and blue boss.
    elif stages.current.name == "blue_boss":
        stats.ships_left -= 1
        hud.prep_health()
        boss = sprites.bosses.sprite
        boss.set_default_hit_points()
        boss.prepare_health()

        # Ship and boss timers refresh.
        settings.black_hole_spawn_timer = 0
        settings.time_elapsed_since_shield = 0
        settings.time_elapsed_since_boss_shield = 0

        sprites.ship_bullets.empty()
        sprites.bosses.empty()
        sprites.boss_bullets.empty()
        sprites.ship_shields.empty()

        if stats.ships_left:
            sprites.boss_black_holes.empty()
            create_blue_boss(settings=settings, screen=screen, sprites=sprites)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)


def fire_alien_bullets(settings: "Settings",
                       screen: "Screen",
                       stages: "Stages",
                       ship: "Ship",
                       sprites: "Sprites",
                       dt: int) -> None:
    """Create alien bullets."""
    settings.time_elapsed_since_last_alien_bullet += dt
    if settings.time_elapsed_since_last_alien_bullet > 2500:
        for alien in sprites.aliens:
            alien_bullet = AlienBullet(settings, screen, alien)
            # TODO: Rework
            if stages.current.index < stages.get_by_name("green_boss").index:
                pass
            elif stages.current.index < stages.get_by_name("red_boss").index + 1:
                alien_bullet.image = alien_bullet.red_bullet
            elif stages.current.index >= stages.get_by_name("red_boss").index + 1:
                alien_bullet.image = alien_bullet.blue_bullet
            alien_bullet.define_position(ship)
            sprites.alien_bullets.add(alien_bullet)
        settings.time_elapsed_since_last_alien_bullet = 0


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


def create_green_boss(settings: "Settings", screen: "Screen", sprites: "Sprites") -> None:
    """Create green boss."""
    green_boss = GreenBoss(settings=settings, screen=screen, boss_health=sprites.boss_health)
    boss_shield = GreenBossShield(screen, green_boss)
    green_boss.set_default_hit_points()
    green_boss.prepare_health()
    sprites.bosses.add(green_boss)
    sprites.boss_shields.add(boss_shield)


def create_blue_boss(settings: "Settings", screen: "Screen", sprites: "Sprites") -> None:
    """Create blue boss."""
    blue_boss = BlueBoss(settings=settings,
                         screen=screen,
                         boss_health=sprites.boss_health)
    boss_shield = BlueBossShield(screen, blue_boss)
    blue_boss.set_default_hit_points()
    blue_boss.prepare_health()
    sprites.bosses.add(blue_boss)
    sprites.boss_shields.add(boss_shield)


def update_green_boss_bullets(boss_bullets: "Group[GreenBossBullet]") -> None:
    """Update green boss bullets position."""
    boss_bullets.update()
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

    angles = (0, 90, 180, 270)
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
    """Create black hole."""
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

    if black_hole.rt_image_number < 11:
        black_hole.rt_image_number += 1
    else:
        black_hole.rt_image_number = 0
    black_hole.update()
    settings.black_hole_rotation_timer = 0
