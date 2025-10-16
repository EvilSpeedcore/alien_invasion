# TODO: Split into multiple files?
import secrets
import sys
import time
from dataclasses import dataclass
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
    from pygame.event import Event
    from pygame.sprite import Group, GroupSingle

    from game.button import Button
    from game.hud import Hud
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stages import Stages
    from game.stats import Stats


@dataclass
class MainMenuEvents:
    quit: bool = False
    play: bool = False

    def update(self, events: "MainMenuEvents") -> None:
        # Update once
        if self.quit is False and events.quit is True:
            self.quit = events.quit
        if self.play is False and events.play is True:
            self.play = events.play


@dataclass
class PauseEvents:
    quit: bool = False
    unpause: bool = False

    def update(self, events: "PauseEvents") -> None:
        # Update once
        if self.quit is False and events.quit is True:
            self.quit = events.quit
        if self.unpause is False and events.unpause is True:
            self.unpause = events.unpause


@dataclass
class ActiveGameEvents:
    quit: bool = False
    pause: bool = False

    def update(self, events: "ActiveGameEvents") -> None:
        # Update once
        if self.quit is False and events.quit is True:
            self.quit = events.quit
        if self.pause is False and events.pause is True:
            self.pause = events.pause


def check_active_game_keydown_events(event: "Event",
                                     settings: "Settings",
                                     screen: "Screen",
                                     stats: "Stats",
                                     hud: "Hud",
                                     ship: "Ship",
                                     sprites: "Sprites") -> ActiveGameEvents:
    events = ActiveGameEvents()
    match event.key:
        case pygame.K_RIGHT:
            ship.desirable_ship_rotation = "right"
            ship.moving_right = True
            rt.rotate(ship)
        case pygame.K_LEFT:
            ship.desirable_ship_rotation = "left"
            ship.moving_left = True
            rt.rotate(ship)
        case pygame.K_UP:
            ship.desirable_ship_rotation = "up"
            ship.moving_up = True
            rt.rotate(ship)
        case pygame.K_DOWN:
            ship.desirable_ship_rotation = "down"
            ship.moving_down = True
            rt.rotate(ship)
        case pygame.K_a:
            fire_bullet(settings, screen, stats, ship, sprites.ship_bullets)
        case pygame.K_SPACE:
            events.update(ActiveGameEvents(pause=True))
        case pygame.K_d:
            use_ship_shield(screen, stats, hud, ship, sprites.ship_shields)
    return events


def check_pause_keydown_events(event: "Event", ship: "Ship") -> PauseEvents:
    events = PauseEvents()
    match event.key:
        case pygame.K_RIGHT:
            ship.desirable_ship_rotation = "right"
            ship.moving_right = True
            rt.rotate(ship)
        case pygame.K_LEFT:
            ship.desirable_ship_rotation = "left"
            ship.moving_left = True
            rt.rotate(ship)
        case pygame.K_UP:
            ship.desirable_ship_rotation = "up"
            ship.moving_up = True
            rt.rotate(ship)
        case pygame.K_DOWN:
            ship.desirable_ship_rotation = "down"
            ship.moving_down = True
            rt.rotate(ship)
        case pygame.K_s:
            events.update(PauseEvents(unpause=True))
    return events


def check_active_game_keyup_events(event: "Event", ship: "Ship") -> ActiveGameEvents:
    check_keyup_events(event, ship)
    return ActiveGameEvents()


def check_pause_keyup_events(event: "Event", ship: "Ship") -> PauseEvents:
    check_keyup_events(event, ship)
    return PauseEvents()


def check_keyup_events(event: "Event", ship: "Ship") -> None:
    """Handle events when a key is released."""
    match event.key:
        case pygame.K_RIGHT:
            ship.moving_right = False
            if ship.moving_up:
                rt.rotate_to_up(ship)
            elif ship.moving_down:
                rt.rotate_to_down(ship)
        case pygame.K_LEFT:
            ship.moving_left = False
            if ship.moving_up:
                rt.rotate_to_up(ship)
            elif ship.moving_down:
                rt.rotate_to_down(ship)
        case pygame.K_UP:
            ship.moving_up = False
            if ship.moving_right:
                rt.rotate_to_right(ship)
            elif ship.moving_left:
                rt.rotate_to_left(ship)
        case pygame.K_DOWN:
            ship.moving_down = False
            if ship.moving_right:
                rt.rotate_to_right(ship)
            elif ship.moving_left:
                rt.rotate_to_left(ship)


def check_active_game_events(settings: "Settings",
                             screen: "Screen",
                             stats: "Stats",
                             hud: "Hud",
                             ship: "Ship",
                             sprites: "Sprites") -> ActiveGameEvents:
    events = ActiveGameEvents()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                events.update(ActiveGameEvents(quit=True))
            case pygame.KEYDOWN:
                events.update(
                    check_active_game_keydown_events(
                        event=event,
                        settings=settings,
                        screen=screen,
                        stats=stats,
                        hud=hud,
                        ship=ship,
                        sprites=sprites,
                    ),
                )
            case pygame.KEYUP:
                events.update(check_active_game_keyup_events(event, ship))
    return events


def check_pause_events(ship: "Ship") -> PauseEvents:
    events = PauseEvents()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                events.update(PauseEvents(quit=True))
            case pygame.KEYDOWN:
                events.update(check_pause_keydown_events(event, ship))
            case pygame.KEYUP:
                events.update(check_pause_keyup_events(event, ship))
    return events


def check_main_menu_events(play_button: "Button") -> MainMenuEvents:
    events = MainMenuEvents()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                events.update(MainMenuEvents(quit=True))
            case pygame.MOUSEBUTTONDOWN:
                events.update(MainMenuEvents(play=check_play_button(play_button)))
            case pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    events.update(MainMenuEvents(play=True))
    return events


def check_play_button(play_button: "Button") -> bool:
    """Check if button to start the game is pressed."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return play_button.ellipse_rect.collidepoint(mouse_x, mouse_y)


def initialize_game_from_main_menu(settings: "Settings", stats: "Stats", hud: "Hud", ship: "Ship") -> None:
    settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    ship.set_default_movement()
    hud.prep_health()
    hud.prep_ammo()
    hud.prep_shield()
    rt.rotate_to_up(ship)


def check_keys_pressed(ship: "Ship") -> None:
    """Handle ship diagonal movement."""
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

    #  Draw ship bullets on screen.
    for bullet in sprites.ship_bullets.sprites():
        bullet.draw_bullet()

    # Draw alien bullets on screen.
    for alien_bullet in sprites.alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()
    for green_boss_bullet in sprites.boss_bullets.sprites():
        green_boss_bullet.draw_bullet()
    for red_boss_bullet in sprites.boss_bullets.sprites():
        red_boss_bullet.draw_bullet()

    #  Ship shield duration handling.
    if len(sprites.ship_shields) == 1:
        settings.time_elapsed_since_shield += dt
        if settings.time_elapsed_since_shield > 3000:
            settings.time_elapsed_since_shield = 0
            sprites.ship_shields.empty()

    #  Display ship shield on hud.
    for used_shield in sprites.ship_shields:
        used_shield.draw_item()

    #  Display boss shield on hud.
    if boss_shield := sprites.boss_shields.sprite:
        if boss_shield.points > 0:
            boss_shield.draw_boss_shield()
            boss_shield.update()
        else:
            sprites.boss_shields.empty()

    hud.show_hud()
    ship.blitme()
    for health_sprite in sprites.ship_health.sprites():
        health_sprite.draw_item()
    for ammo_sprite in sprites.ship_ammo.sprites():
        ammo_sprite.draw_item()
    sprites.aliens.draw(screen.it)
    sprites.bosses.draw(screen.it)
    if black_hole := sprites.boss_black_holes.sprite:
        black_hole.draw_black_hole()

    # Update screen.
    pygame.display.flip()


def update_main_menu_screen(settings: "Settings", screen: "Screen", play_button: "Button") -> None:
    screen.it.fill(settings.bg_color)

    # Show start button and clear the screen.
    play_button.prep_msg(play_button.msg)
    play_button.draw_button()

    # Update screen.
    pygame.display.flip()


def update_bullets(screen: "Screen", bullets: "Group") -> None:
    bullets.update()
    screen_rect = screen.rect
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:  # UP
            bullets.remove(bullet)
        if bullet.rect.left > screen_rect.right:  # RIGHT
            bullets.remove(bullet)
        if bullet.rect.right < screen_rect.left:  # LEFT
            bullets.remove(bullet)
        if bullet.rect.top > screen_rect.bottom:  # BOTTOM
            bullets.remove(bullet)


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
        sprites.bosses.sprite.set_default_hit_points()
        sprites.bosses.sprite.prepare_health()

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
        sprites.bosses.sprite.set_default_hit_points()
        sprites.bosses.sprite.prepare_health()

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
        sprites.bosses.sprite.set_default_hit_points()
        sprites.bosses.sprite.prepare_health()

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


def check_ship_aliens_collision(settings: "Settings",
                                screen: "Screen",
                                stats: "Stats",
                                stages: "Stages",
                                hud: "Hud",
                                ship: "Ship",
                                sprites: "Sprites") -> None:
    if pygame.sprite.spritecollideany(ship, sprites.aliens):
        ship_hit(settings, screen, stats, stages, hud, ship, sprites)


def check_ship_alien_bullets_collision(settings: "Settings",
                                       screen: "Screen",
                                       stats: "Stats",
                                       stages: "Stages",
                                       hud: "Hud",
                                       ship: "Ship",
                                       sprites: "Sprites") -> None:
    if pygame.sprite.spritecollideany(ship, sprites.alien_bullets):
        ship_hit(settings, screen, stats, stages, hud, ship, sprites)


def check_ship_boss_bullets_collision(settings: "Settings",
                                      screen: "Screen",
                                      stats: "Stats",
                                      stages: "Stages",
                                      hud: "Hud",
                                      ship: "Ship",
                                      sprites: "Sprites") -> None:
    if pygame.sprite.spritecollideany(ship, sprites.boss_bullets):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def check_ship_bullets_boss_collision(settings: "Settings", sprites: "Sprites") -> None:
    collision = pygame.sprite.groupcollide(sprites.ship_bullets,
                                                sprites.bosses,
                                                dokilla=True,
                                                dokillb=False)
    if not collision:
        return

    boss = sprites.bosses.sprite
    boss.hit_points -= 1
    boss.hit_points_with_shield -= 1
    boss.prepare_health()
    if boss.hit_points < 1:
        time.sleep(settings.game_sleep_time)
        sprites.bosses.empty()
        sprites.boss_bullets.empty()


def check_ship_bosses_collision(settings: "Settings",
                                screen: "Screen",
                                stats: "Stats",
                                stages: "Stages",
                                hud: "Hud",
                                ship: "Ship",
                                sprites: "Sprites") -> None:
    if pygame.sprite.spritecollideany(ship, sprites.bosses):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def check_ship_bullets_boss_shield_collision(sprites: "Sprites") -> None:
    if pygame.sprite.groupcollide(sprites.boss_shields, sprites.ship_bullets, dokilla=False, dokillb=True):
        sprites.boss_shields.sprite.points -= 1
        sprites.bosses.sprite.hit_points_with_shield -= 1
        sprites.bosses.sprite.prepare_health()


def check_ship_health_collision(stats: "Stats", hud: "Hud", ship: "Ship", health: "Group") -> None:
    if pygame.sprite.spritecollideany(ship, health):
        effect = pygame.mixer.Sound(Paths.effects() / "pick_up_1.ogg")
        effect.play()
        health.empty()
        stats.ships_left += 1
        hud.prep_health()


def check_ship_ammo_collision(stats: "Stats", hud: "Hud", ship: "Ship", ammo: "Group") -> None:
    if pygame.sprite.spritecollideany(ship, ammo):
        stats.ammo += 1
        ammo.empty()
        hud.prep_ammo()


def check_ship_black_holes_collision(settings: "Settings",
                                     screen: "Screen",
                                     stats: "Stats",
                                     hud: "Hud",
                                     stages: "Stages",
                                     ship: "Ship",
                                     sprites: "Sprites") -> None:
    if pygame.sprite.spritecollideany(ship, sprites.boss_black_holes):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


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
        bullet.add(boss_bullets)

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


def update_green_boss_bullets(boss_bullets: "Group") -> None:
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
    if settings.time_elapsed_since_last_red_boss_bullet > 1350:
        for boss in bosses:
            red_boss_bullet = RedBossBullet(settings, screen, boss)
            red_boss_bullet.define_position(ship)
            red_boss_bullet.add(boss_bullets)

            red_boss_bullet_2 = RedBossBullet(settings, screen, boss)
            red_boss_bullet_2.define_position(ship)
            red_boss_bullet_2.shooting_angle += 15
            red_boss_bullet_2.add(boss_bullets)

            red_boss_bullet_3 = RedBossBullet(settings, screen, boss)
            red_boss_bullet_3.define_position(ship)
            red_boss_bullet_3.shooting_angle += 30
            red_boss_bullet_3.add(boss_bullets)

            red_boss_bullet_4 = RedBossBullet(settings, screen, boss)
            red_boss_bullet_4.define_position(ship)
            red_boss_bullet_4.shooting_angle -= 15
            red_boss_bullet_4.add(boss_bullets)

            red_boss_bullet_5 = RedBossBullet(settings, screen, boss)
            red_boss_bullet_5.define_position(ship)
            red_boss_bullet_5.shooting_angle -= 30
            red_boss_bullet_5.add(boss_bullets)

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

    settings.black_hole_rotation_timer += dt
    if settings.black_hole_rotation_timer <= 300:
        return

    if black_hole := black_holes.sprite:
        if black_hole.rt_image_number < 11:
            black_hole.rt_image_number += 1
        else:
            black_hole.rt_image_number = 0
        black_hole.update()
        settings.black_hole_rotation_timer = 0


def quit_game() -> None:
    pygame.quit()
    sys.exit(0)


def check_game_end(stages: "Stages", stats: "Stats") -> bool:
    if stages.end:
        return True

    return stats.ships_left < 1
