from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Group, GroupSingle

import game.game_functions as gf
from game.button import Button
from game.game_stats import GameStats
from game.hud import Hud
from game.settings import Settings
from game.ship import Ship
from game.state import State

if TYPE_CHECKING:
    from game.alien import Alien
    from game.alien_bullet import AlienBullet
    from game.bosses_bullets import BossBullet
    from game.bullet import Bullet
    from game.ship_consumables import ShipAmmo, ShipHealth


def run_game() -> None:
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(settings, screen)
    stats = GameStats(settings)
    hud = Hud(settings, screen, stats, ship)
    play_button = Button(screen, "Start")

    # TODO: How to type Group?
    bullets: Group[Bullet] = Group()
    aliens: Group[Alien] = Group()
    alien_bullets: Group[AlienBullet] = Group()
    health: Group[ShipHealth] = Group()
    ammo: Group[ShipAmmo] = Group()
    used_shields: Group[ShipHealth] = Group()
    boss_bullets: Group[BossBullet] = Group()

    # TODO: How to type GroupSingle?
    bosses: GroupSingle = GroupSingle()
    boss_shields: GroupSingle = GroupSingle()
    black_holes: GroupSingle = GroupSingle()

    clock = pygame.time.Clock()
    settings.state = State.MAIN_MENU

    # Main game cycle
    while True:
        # Pause
        while settings.state == State.PAUSED:
            pause_events = gf.check_pause_events(ship)
            if pause_events.quit:
                gf.quit()
            if pause_events.unpause:
               settings.state = State.RUNNING

        # Menu
        while settings.state == State.MAIN_MENU:
            menu_events = gf.check_main_menu_events(stats, play_button)
            gf.update_main_menu_screen(settings, screen, stats, play_button)

            if menu_events.play:
                gf.initialize_game_from_main_menu(settings, screen, stats, hud, ship, aliens, used_shields, black_holes)
                settings.state = State.RUNNING
            if menu_events.quit:
                gf.quit()

        # Game
        while settings.state == State.RUNNING:
            dt = clock.tick()
            gf.check_events(settings, screen, stats, hud, ship, bullets, used_shields)
            gf.check_keys_pressed(ship)
            if stats.game_active:
                ship.update()

                if not (aliens or bosses):
                    gf.prepare_next_regular_stage(settings, screen, stats, ship, aliens,
                                                  bullets, alien_bullets, health, ammo)

                gf.update_ship_shield(alien_bullets, used_shields, boss_bullets)
                gf.update_bullets(settings, screen, stats, hud, ship, aliens, bullets,
                                  alien_bullets, bosses, boss_bullets, boss_shields, black_holes)
                gf.update_aliens(settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health,
                                ammo, used_shields)
                gf.fire_alien_bullets(settings, screen, stats, ship, aliens, alien_bullets, dt)
                gf.update_alien_bullets(settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health,
                                        ammo, used_shields)
                if stats.stage == settings.boss_stages[0]:
                    gf.update_green_boss(settings, screen, stats, hud, ship, bullets,
                                        used_shields, bosses, boss_bullets, boss_shields, bosses)
                    gf.fire_green_boss_bullets(settings, screen, dt, bosses, boss_bullets)
                    gf.update_green_boss_bullets(settings, screen, stats, hud, ship, bullets,
                                                used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_green_boss_shield(hud, bullets, boss_shields)
                elif stats.stage == settings.boss_stages[1]:
                    gf.update_red_boss(settings, screen, stats, hud, ship, bullets,
                                    used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_red_boss_shield(hud, bullets, boss_shields)
                    gf.fire_red_boss_bullets(settings, screen, ship, dt, bosses, boss_bullets)
                    gf.update_red_boss_bullets(settings, screen, stats, hud, ship, bullets,
                                            used_shields, bosses, boss_bullets, boss_shields, black_holes)
                elif stats.stage == settings.boss_stages[2]:
                    gf.update_blue_boss(settings, screen, stats, hud, ship, bullets,
                                        used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_blue_boss_shield(hud, bullets, boss_shields)
                    gf.fire_blue_boss_bullets(settings, screen, dt, bosses, boss_bullets)
                    gf.update_blue_boss_bullets(settings, screen, stats, hud, ship, bullets,
                                                used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.create_black_hole(settings, screen, ship, dt, black_holes)
                    gf.update_black_hole(settings, screen, stats, hud, ship, bullets,
                                        used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)

                gf.update_ship_health(stats, hud, ship, health)
                gf.update_ship_ammo(stats, hud, ship, ammo)

                gf.update_screen(settings, screen, stats, hud, ship, aliens, bullets, alien_bullets,
                                 health, ammo, used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)


if __name__ == '__main__':
    run_game()
