import random
import sys
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
    from pygame.surface import Surface

    from game.button import Button
    from game.collections import Sprites
    from game.hud import Hud
    from game.settings import Settings
    from game.ship import Ship
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
                                     screen: "Surface",
                                     stats: "Stats",
                                     hud: "Hud",
                                     ship: "Ship",
                                     sprites: "Sprites") -> ActiveGameEvents:
    events = ActiveGameEvents()
    if event.key == pygame.K_RIGHT:
        ship.desirable_ship_rotation = "right"
        ship.moving_right = True
        rt.rotate(ship)
    if event.key == pygame.K_LEFT:
        ship.desirable_ship_rotation = "left"
        ship.moving_left = True
        rt.rotate(ship)
    if event.key == pygame.K_UP:
        ship.desirable_ship_rotation = "up"
        ship.moving_up = True
        rt.rotate(ship)
    if event.key == pygame.K_DOWN:
        ship.desirable_ship_rotation = "down"
        ship.moving_down = True
        rt.rotate(ship)
    if event.key == pygame.K_a:
        fire_bullet(settings, screen, stats, ship, sprites.ship_bullets)
    if event.key == pygame.K_SPACE:
        events.update(ActiveGameEvents(pause=True))
    if event.key == pygame.K_d:
        use_ship_shield(settings, screen, stats, hud, ship, sprites.ship_shields)
    return events


def check_pause_keydown_events(event: "Event", ship: "Ship") -> PauseEvents:
    events = PauseEvents()
    if event.key == pygame.K_RIGHT:
        ship.desirable_ship_rotation = "right"
        ship.moving_right = True
        rt.rotate(ship)
    if event.key == pygame.K_LEFT:
        ship.desirable_ship_rotation = "left"
        ship.moving_left = True
        rt.rotate(ship)
    if event.key == pygame.K_UP:
        ship.desirable_ship_rotation = "up"
        ship.moving_up = True
        rt.rotate(ship)
    if event.key == pygame.K_DOWN:
        ship.desirable_ship_rotation = "down"
        ship.moving_down = True
        rt.rotate(ship)
    if event.key == pygame.K_s:
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
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        if ship.moving_up:
            rt.rotate_to_up(ship)
        elif ship.moving_down:
            rt.rotate_to_down(ship)
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        if ship.moving_up:
            rt.rotate_to_up(ship)
        elif ship.moving_down:
            rt.rotate_to_down(ship)
    if event.key == pygame.K_UP:
        ship.moving_up = False
        if ship.moving_right:
            rt.rotate_to_right(ship)
        elif ship.moving_left:
            rt.rotate_to_left(ship)
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
        if ship.moving_right:
            rt.rotate_to_right(ship)
        elif ship.moving_left:
            rt.rotate_to_left(ship)


def check_active_game_events(settings: "Settings",
                             screen: "Surface",
                             stats: "Stats",
                             hud: "Hud",
                             ship: "Ship",
                             sprites: "Sprites") -> ActiveGameEvents:
    events = ActiveGameEvents()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.update(ActiveGameEvents(quit=True))
        elif event.type == pygame.KEYDOWN:
            events.update(check_active_game_keydown_events(event, settings, screen, stats,
                                                           hud, ship, sprites))
        elif event.type == pygame.KEYUP:
            events.update(check_active_game_keyup_events(event, ship))
    return events


def check_pause_events(ship: "Ship") -> PauseEvents:
    events = PauseEvents()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.update(PauseEvents(quit=True))
        elif event.type == pygame.KEYDOWN:
            events.update(check_pause_keydown_events(event, ship))
        elif event.type == pygame.KEYUP:
            events.update(check_pause_keyup_events(event, ship))
    return events


def check_main_menu_events(play_button: "Button") -> MainMenuEvents:
    events = MainMenuEvents()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.update(MainMenuEvents(quit=True))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            events.update(MainMenuEvents(play=check_play_button(play_button)))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
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
                  screen: "Surface",
                  hud: "Hud",
                  ship: "Ship",
                  dt: int,
                  sprites: "Sprites") -> None:
    """Update screen."""
    screen.fill(settings.bg_color)

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
    for boss_shield in sprites.boss_shields:
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
    sprites.aliens.draw(screen)
    sprites.bosses.draw(screen)
    for black_hole in sprites.boss_black_holes.sprites():
        black_hole.draw_black_hole()

    # Update screen.
    pygame.display.flip()


def update_main_menu_screen(settings: "Settings", screen: "Surface", play_button: "Button") -> None:
    screen.fill(settings.bg_color)

    # Show start button and clear the screen.
    play_button.prep_msg(play_button.msg)
    play_button.draw_button()

    # Update screen.
    pygame.display.flip()


def update_bullets(settings: "Settings",
                   stages: "Stages",
                   hud: "Hud",
                   ship: "Ship",
                   sprites: "Sprites") -> None:
    """Update ship bullets. Remove bullet from sprites, if it reach edge of the screen. Check for collisions."""
    bullets = sprites.ship_bullets
    bullets.update()
    for bullet in bullets.copy():
        # For UP bullet direction.
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # For RIGHT bullet direction.
        if bullet.rect.left > ship.screen_rect.right:
            bullets.remove(bullet)
        # For LEFT bullet direction.
        if bullet.rect.right < ship.screen_rect.left:
            bullets.remove(bullet)
        # For DOWN bullet direction.
        if bullet.rect.top > ship.screen_rect.bottom:
            bullets.remove(bullet)
        # For UP_RIGHT bullet direction.
        if bullet.rect.bottom <= 0 or bullet.rect.left > ship.screen_rect.right:
            bullets.remove(bullet)
        # For UP_LEFT bullet direction.
        if bullet.rect.bottom <= 0 or bullet.rect.right < ship.screen_rect.left:
            bullets.remove(bullet)
        # For DOWN_LEFT bullet direction.
        if bullet.rect.top > ship.screen_rect.bottom or bullet.rect.right < ship.screen_rect.left:
            bullets.remove(bullet)
        # For DOWN_RIGHT bullet direction.
        if bullet.rect.top > ship.screen_rect.bottom or bullet.rect.left > ship.screen_rect.right:
            bullets.remove(bullet)

    pygame.sprite.groupcollide(bullets, sprites.aliens, dokilla=True, dokillb=True)

    # Check for collision between ship billet and boss.
    check_bullet_boss_collision(settings, stages, hud, sprites)


def check_bullet_boss_collision(settings: "Settings",
                                stages: "Stages",
                                hud: "Hud",
                                sprites: "Sprites") -> None:
    """Handle collisions between ship bullets and bosses."""
    # Check collisions between ship and green boss.
    if stages.current.name == "green_boss":
        boss_collision = pygame.sprite.groupcollide(sprites.ship_bullets,
                                                    sprites.bosses,
                                                    dokilla=True,
                                                    dokillb=False)
        if boss_collision:
            for boss in sprites.bosses.sprites():
                boss.hit_points -= 1
                hud.green_boss_hp -= 1
                hud.prep_green_boss_health()
                if boss.hit_points < 1:
                    sleep(settings.game_sleep_time)
                    sprites.bosses.empty()
                    sprites.boss_bullets.empty()

    # Check collisions between ship and red boss.
    elif stages.current.name == "red_boss":
        boss_collision = pygame.sprite.groupcollide(sprites.ship_bullets,
                                                    sprites.bosses,
                                                    dokilla=True,
                                                    dokillb=False)
        if boss_collision:
            for boss in sprites.bosses.sprites():
                boss.hit_points -= 1
                hud.red_boss_hp -= 1
                hud.prep_red_boss_health()
                if boss.hit_points < 1:
                    sleep(settings.game_sleep_time)
                    sprites.bosses.empty()
                    sprites.boss_bullets.empty()

    # Check collisions between ship and blue boss.
    elif stages.current.name == "blue_boss":
        boss_collision = pygame.sprite.groupcollide(sprites.ship_bullets,
                                                    sprites.bosses,
                                                    dokilla=True,
                                                    dokillb=False)
        if boss_collision:
            for boss in sprites.bosses.sprites():
                boss.hit_points -= 1
                hud.blue_boss_hp -= 1
                hud.prep_blue_boss_health()
                if boss.hit_points < 1:
                    sleep(settings.game_sleep_time)
                    sprites.bosses.empty()
                    sprites.boss_bullets.empty()


def fire_bullet(settings: "Settings",
                screen: "Surface",
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
                 screen: "Surface",
                 stages: "Stages",
                 ship: "Ship",
                 aliens: "Group",
                 alien_number: int) -> None:
    """Create an alien and place it in a row."""
    alien = Alien(settings, screen, ship)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.fleet_creation_time = round(pygame.time.get_ticks()/1000) + 1
    if stages.current.index < stages.get_by_name("green_boss").index:
        alien.alien_color = "green"
    elif stages.current.index < stages.get_by_name("red_boss").index:
        alien.image = alien.red_alien
        alien.alien_color = "red"
    elif stages.current.index < stages.get_by_name("blue_boss").index:
        alien.image = alien.blue_alien
        alien.alien_color = "blue"
    aliens.add(alien)


def create_fleet(settings: "Settings",
                 screen: "Surface",
                 stages: "Stages",
                 ship: "Ship",
                 aliens: "Group") -> None:
    """Create alien fleet."""
    alien = Alien(settings, screen, ship)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    for alien_number in range(number_aliens_x):
        create_alien(settings, screen, stages, ship, aliens, alien_number)


def ship_hit(settings: "Settings",
             screen: "Surface",
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
                           screen: "Surface",
                           stats: "Stats",
                           stages: "Stages",
                           hud: "Hud",
                           ship: "Ship",
                           sprites: "Sprites") -> None:
    """Handle collisions between ship and bosses."""
    # Handle collisions between ship and green boss.
    if stages.current.name == "green_boss":
        stats.ships_left -= 1
        hud.prep_health()
        hud.green_boss_hp = 19
        hud.prep_green_boss_health()

        # Ship and boss timers refresh.
        settings.time_elapsed_since_shield = 0
        settings.time_elapsed_since_boss_shield = 0

        sprites.ship_bullets.empty()
        sprites.bosses.empty()
        sprites.boss_bullets.empty()
        sprites.ship_shields.empty()

        if stats.ships_left:
            create_green_boss(settings, screen, hud, sprites.bosses, sprites.boss_shields)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)

    # Handle collisions between ship and red boss.
    elif stages.current.name == "red_boss":
        stats.ships_left -= 1
        hud.prep_health()
        hud.red_boss_hp = 14
        hud.prep_red_boss_health()

        # Ship and boss timers refresh.
        settings.time_elapsed_since_shield = 0
        settings.time_elapsed_since_boss_shield = 0

        sprites.bullets.empty()
        sprites.bosses.empty()
        sprites.boss_bullets.empty()
        sprites.ship_shields.empty()

        if stats.ships_left:
            create_red_boss(settings, screen, hud, sprites.bosses, sprites.boss_shields)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)

    # Handle collisions between ship and blue boss.
    elif stages.current.name == "blue_boss":
        stats.ships_left -= 1
        hud.prep_health()
        hud.blue_boss_hp = 19
        hud.prep_blue_boss_health()

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
            create_blue_boss(settings, screen, hud, sprites.bosses, sprites.boss_shields)
            ship.prepare_for_boss()
            sleep(settings.game_sleep_time)


def update_aliens(settings: "Settings",
                  screen: "Surface",
                  stats: "Stats",
                  stages: "Stages",
                  hud: "Hud",
                  ship: "Ship",
                  sprites: "Sprites") -> None:
    """Update aliens position in fleet."""
    sprites.aliens.update(sprites.aliens, ship)
    if pygame.sprite.spritecollideany(ship, sprites.aliens):
        ship_hit(settings, screen, stats, stages, hud, ship, sprites)


def update_ship_health(stats: "Stats", hud: "Hud", ship: "Ship", health: "Group") -> None:
    """Update extra health on hud after pick-up."""
    if pygame.sprite.spritecollideany(ship, health):
        effect = pygame.mixer.Sound(Paths.effects() / "pick_up_1.ogg")
        effect.play()
        health.empty()
        stats.ships_left += 1
        hud.prep_health()


def update_ship_ammo(stats: "Stats", hud: "Hud", ship: "Ship", ammo: "Group") -> None:
    """Update extra ammo om hud after pick-up."""
    if pygame.sprite.spritecollideany(ship, ammo):
        stats.ammo += 1
        ammo.empty()
        hud.prep_ammo()


def fire_alien_bullets(settings: "Settings",
                       screen: "Surface",
                       stages: "Stages",
                       ship: "Ship",
                       dt: int,
                       sprites: "Sprites") -> None:
    """Create alien bullets."""
    settings.time_elapsed_since_last_alien_bullet += dt
    if settings.time_elapsed_since_last_alien_bullet > 2500:
        for alien in sprites.aliens:
            alien_bullet = AlienBullet(settings, screen, alien)
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
                            screen: "Surface",
                            dt: int,
                            bosses: "GroupSingle",
                            boss_bullets: "Group") -> None:
    """Create green boss bullets."""
    settings.time_elapsed_since_last_boss_bullet += dt
    if settings.time_elapsed_since_last_boss_bullet > settings.green_boss_bullet_timer:
        for boss in bosses:
            green_boss_bullet_1 = GreenBossBullet(settings, screen, boss)
            green_boss_bullet_1.shooting_angle_up = random.choice(range(180))
            green_boss_bullet_1.add(boss_bullets)

            green_boss_bullet_2 = GreenBossBullet(settings, screen, boss)
            green_boss_bullet_2.shooting_angle_up = random.choice(range(90, 270))
            green_boss_bullet_2.add(boss_bullets)

            green_boss_bullet_3 = GreenBossBullet(settings, screen, boss)
            green_boss_bullet_3.shooting_angle_up = random.choice(range(180, 360))
            green_boss_bullet_3.add(boss_bullets)

            green_boss_bullet_4 = GreenBossBullet(settings, screen, boss)
            green_boss_bullet_4.shooting_angle_up = random.choice(range(270, 450))
            green_boss_bullet_4.add(boss_bullets)

        settings.time_elapsed_since_last_boss_bullet = 0
        settings.green_boss_bullet_timer = 1650


def update_alien_bullets(settings: "Settings",
                         screen: "Surface",
                         stats: "Stats",
                         stages: "Stages",
                         hud: "Hud",
                         ship: "Ship",
                         sprites: "Sprites") -> None:
    """Update alien bullets position."""
    alien_bullets = sprites.alien_bullets
    alien_bullets.update()
    for alien_bullet in alien_bullets.copy():
            if alien_bullet.rect.bottom <= 0:
                alien_bullets.remove(alien_bullet)
            if alien_bullet.rect.left > alien_bullet.screen_rect.right:
                alien_bullets.remove(alien_bullet)
            if alien_bullet.rect.right < alien_bullet.screen_rect.left:
                alien_bullets.remove(alien_bullet)
            if alien_bullet.rect.top > alien_bullet.screen_rect.bottom:
                alien_bullets.remove(alien_bullet)
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(settings, screen, stats, stages, hud, ship, sprites)


def use_ship_shield(settings: "Settings",
                    screen: "Surface",
                    stats: "Stats",
                    hud: "Hud",
                    ship: "Ship",
                    used_shields: "Group") -> None:
    """Handle use of ship shield."""
    if stats.shields_left:
        effect = pygame.mixer.Sound(Paths.effects() / "1.ogg")
        effect.play()
        used_shield = ShipShield(settings, screen, ship)
        used_shields.add(used_shield)
        stats.shields_left -= 1
        hud.prep_shield()


def update_ship_shield(alien_bullets: "Group", used_shields: "Group", boss_bullets: "Group") -> None:
    """Update ship shield position. Check for collisions between shield and bullet."""
    used_shields.update()
    pygame.sprite.groupcollide(used_shields, alien_bullets, dokilla=False, dokillb=True)
    pygame.sprite.groupcollide(used_shields, boss_bullets, dokilla=False, dokillb=True)


def create_green_boss(settings: "Settings",
                      screen: "Surface",
                      hud: "Hud",
                      bosses: "GroupSingle",
                      boss_shields: "GroupSingle") -> None:
    """Create green boss."""
    green_boss = GreenBoss(settings, screen)
    boss_shield = GreenBossShield(settings, screen, green_boss)
    hud.green_boss_hp = 19
    hud.prep_green_boss_health()
    bosses.add(green_boss)
    boss_shields.add(boss_shield)


def create_blue_boss(settings: "Settings",
                     screen: "Surface",
                     hud: "Hud",
                     bosses: "GroupSingle",
                     boss_shields: "GroupSingle") -> None:
    """Create blue boss."""
    blue_boss = BlueBoss(settings, screen)
    boss_shield = BlueBossShield(settings, screen, blue_boss)
    hud.blue_boss_hp = 19
    hud.prep_blue_boss_health()
    bosses.add(blue_boss)
    boss_shields.add(boss_shield)


def update_green_boss_bullets(settings: "Settings",
                              screen: "Surface",
                              stats: "Stats",
                              stages: "Stages",
                              hud: "Hud",
                              ship: "Ship",
                              sprites: "Sprites") -> None:
    """Update green boss bullets position. Check for collisions between ship and boss bullets."""
    boss_bullets = sprites.boss_bullets
    boss_bullets.update()

    for green_boss_bullet in boss_bullets.copy():
        green_boss_bullet.change_direction(boss_bullets)

    if pygame.sprite.spritecollideany(ship, boss_bullets):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def create_red_boss(settings: "Settings",
                    screen: "Surface",
                    hud: "Hud",
                    bosses: "GroupSingle",
                    boss_shields: "Group") -> None:
    """Create red boss."""
    red_boss = RedBoss(settings, screen)
    boss_shield = RedBossShield(settings, screen, red_boss)
    hud.red_boss_hp = 14
    hud.prep_red_boss_health()
    bosses.add(red_boss)
    boss_shields.add(boss_shield)


def fire_red_boss_bullets(settings: "Settings",
                          screen: "Surface",
                          ship: "Ship",
                          dt: int,
                          bosses: "GroupSingle",
                          boss_bullets: "Group") -> None:
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
                           screen: "Surface",
                           dt: int,
                           bosses: "GroupSingle",
                           boss_bullets: "Group") -> None:
    """Create blue boss bullets."""
    settings.time_elapsed_since_last_red_boss_bullet += dt
    if settings.time_elapsed_since_last_red_boss_bullet > 300:
        for boss in bosses:
            blue_boss_bullet = BlueBossBullet(settings, screen, boss, boss.shooting_angle)
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[0]))
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[1]))
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[2]))
            blue_boss_bullet.add(boss_bullets)

            settings.time_elapsed_since_last_red_boss_bullet = 0
            if boss.rt_trigger:
                boss.shooting_angle += 15
                if boss.shooting_angle > 400:
                    boss.rt_trigger = False
            else:
                boss.shooting_angle -= 15
                if boss.shooting_angle < 0:
                    boss.rt_trigger = True


def update_red_boss_bullets(settings: "Settings",
                            screen: "Surface",
                            stats: "Stats",
                            stages: "Stages",
                            hud: "Hud",
                            ship: "Ship",
                            sprites: "Sprites") -> None:
    """Update red boss bullets position. Check for collisions between ship and boss bullets."""
    boss_bullets = sprites.boss_bullets
    boss_bullets.update()
    for red_boss_bullet in boss_bullets.copy():
            if red_boss_bullet.rect.bottom <= 0:
                boss_bullets.remove(red_boss_bullet)
            if red_boss_bullet.rect.left > red_boss_bullet.screen_rect.right:
                boss_bullets.remove(red_boss_bullet)
            if red_boss_bullet.rect.right < red_boss_bullet.screen_rect.left:
                boss_bullets.remove(red_boss_bullet)
            if red_boss_bullet.rect.top > red_boss_bullet.screen_rect.bottom:
                boss_bullets.remove(red_boss_bullet)
    if pygame.sprite.spritecollideany(ship, boss_bullets):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def update_blue_boss_bullets(settings: "Settings",
                             screen: "Surface",
                             stats: "Stats",
                             stages: "Stages",
                             hud: "Hud",
                             ship: "Ship",
                             sprites: "Sprites") -> None:
    """Update blue boss bullets position. Check for collisions between ship and boss bullets."""
    boss_bullets = sprites.boss_bullets
    boss_bullets.update()
    for blue_boss_bullet in boss_bullets.copy():
            if blue_boss_bullet.rect.bottom <= 0:
                boss_bullets.remove(blue_boss_bullet)
            if blue_boss_bullet.rect.left > blue_boss_bullet.screen_rect.right:
                boss_bullets.remove(blue_boss_bullet)
            if blue_boss_bullet.rect.right < blue_boss_bullet.screen_rect.left:
                boss_bullets.remove(blue_boss_bullet)
            if blue_boss_bullet.rect.top > blue_boss_bullet.screen_rect.bottom:
                boss_bullets.remove(blue_boss_bullet)
    if pygame.sprite.spritecollideany(ship, boss_bullets):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def update_green_boss(settings: "Settings",
                      screen: "Surface",
                      stats: "Stats",
                      stages: "Stages",
                      hud: "Hud",
                      ship: "Ship",
                      sprites: "Sprites") -> None:
    """Check for collisions between green boss and ship."""
    if pygame.sprite.spritecollideany(ship, sprites.bosses):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def update_green_boss_shield(hud: "Hud", bullets: "Group", boss_shields: "GroupSingle") -> None:
    """Update hit points of green boss shield on a collision with ship bullets."""
    if pygame.sprite.groupcollide(boss_shields, bullets, dokilla=False, dokillb=True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.green_boss_hp -= 1
            hud.prep_green_boss_health()


def update_red_boss(settings: "Settings",
                    screen: "Surface",
                    stats: "Stats",
                    stages: "Stages",
                    hud: "Hud",
                    ship: "Ship",
                    sprites: "Sprites") -> None:
    """Update red boss position. Check for collisions between red boss and ship."""
    if pygame.sprite.spritecollideany(ship, sprites.bosses):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)
    for boss in sprites.bosses:
        boss.update()


def update_blue_boss(settings: "Settings",
                     screen: "Surface",
                     stats: "Stats",
                     stages: "Stages",
                     hud: "Hud",
                     ship: "Ship",
                     sprites: "Sprites") -> None:
    """Check for collisions between blue boss and ship."""
    if pygame.sprite.spritecollideany(ship, sprites.bosses):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def update_red_boss_shield(hud: "Hud", bullets: "Group", boss_shields: "GroupSingle") -> None:
    """Update hit points of red boss shield on a collision with ship bullets."""
    if pygame.sprite.groupcollide(boss_shields, bullets, dokilla=False, dokillb=True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.red_boss_hp -= 1
            hud.prep_red_boss_health()


def update_blue_boss_shield(hud: "Hud", bullets: "Group", boss_shields: "GroupSingle") -> None:
    """Update hit points of blue boss shield on a collision with ship bullets."""
    if pygame.sprite.groupcollide(boss_shields, bullets, dokilla=False, dokillb=True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.blue_boss_hp -= 1
            hud.prep_blue_boss_health()


def create_black_hole(settings: "Settings",
                      screen: "Surface",
                      ship: "Ship",
                      dt: int,
                      black_holes: "GroupSingle") -> None:
    """Create black hole."""
    settings.black_hole_spawn_timer += dt
    if len(black_holes) == 0 and settings.black_hole_spawn_timer > 2000:
        black_hole = BlackHole(settings, screen, ship)
        black_holes.add(black_hole)
    elif len(black_holes) == 1:
        if settings.black_hole_spawn_timer > 6000:
            black_holes.empty()
            settings.black_hole_spawn_timer = 0


def update_black_hole(settings: "Settings",
                      screen: "Surface",
                      stats: "Stats",
                      stages: "Stages",
                      hud: "Hud",
                      ship: "Ship",
                      dt: int,
                      sprites: "Sprites") -> None:
    """Update black hole animation. Check for collisions between ship and black hole."""
    black_holes = sprites.boss_black_holes
    settings.black_hole_rotation_timer += dt
    if settings.black_hole_rotation_timer > 300:
        for black_hole in black_holes.sprites():
            if black_hole.rt_image_number < 11:
                black_hole.rt_image_number += 1
            else:
                black_hole.rt_image_number = 0
            black_hole.update()
            black_holes.add(black_hole)
            settings.black_hole_rotation_timer = 0
    if pygame.sprite.spritecollideany(ship, black_holes):
        ship_hit_at_boss_stage(settings, screen, stats, stages, hud, ship, sprites)


def quit_game() -> None:
    pygame.quit()
    sys.exit(0)


def check_game_end(stages: "Stages", stats: "Stats") -> bool:
    if stages.current.name == "end":
        return True

    return stats.ships_left < 1
