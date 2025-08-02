import logging
from time import sleep
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Group, GroupSingle

import game.game_functions as gf
from game.button import Button
from game.game_stats import GameStats
from game.hud import Hud
from game.settings import Settings
from game.ship import Ship
from game.stages import Stages
from game.state import GameState, State

if TYPE_CHECKING:
    from game.alien import Alien
    from game.alien_bullet import AlienBullet
    from game.bosses_bullets import BossBullet
    from game.bullet import Bullet
    from game.ship_consumables import ShipAmmo, ShipHealth


def run_game() -> None:
    logging.basicConfig(filename="app.log", level=logging.DEBUG)

    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(settings, screen)
    stats = GameStats(settings)
    play_button = Button(screen, "Start")

    # TODO: How to type Group?
    aliens: Group[Alien] = Group()
    bullets: Group[Bullet] = Group()
    alien_bullets: Group[AlienBullet] = Group()

    health: Group[ShipHealth] = Group()
    ammo: Group[ShipAmmo] = Group()
    used_shields: Group[ShipHealth] = Group()

    # TODO: How to type GroupSingle?
    bosses = GroupSingle()
    boss_bullets: Group[BossBullet] = Group()
    boss_shields = GroupSingle()
    boss_health = GroupSingle()
    black_holes = GroupSingle()

    hud = Hud(settings, screen, stats, ship, boss_health)
    stages = Stages(settings=settings,
                    screen=screen,
                    stats=stats,
                    hud=hud,
                    aliens=aliens,
                    ship=ship,
                    health=health,
                    ammo=ammo,
                    bullets=bullets,
                    alien_bullets=alien_bullets,
                    used_shields=used_shields,
                    bosses=bosses,
                    boss_health=boss_health,
                    boss_shields=boss_shields,
                    black_holes=black_holes)

    state = GameState(State.MAIN_MENU)
    clock = pygame.time.Clock()

    # Main game cycle
    while True:
        # Pause state
        while state(State.PAUSED):
            pause_events = gf.check_pause_events(ship)
            if pause_events.quit:
                gf.quit_game()
            if pause_events.unpause:
               state.set(State.ACTIVE)

        # Menu state
        while state(State.MAIN_MENU):
            pygame.mouse.set_visible(True)

            menu_events = gf.check_main_menu_events(play_button)
            gf.update_main_menu_screen(settings, screen, play_button)

            if menu_events.play:
                gf.initialize_game_from_main_menu(settings, stats, hud, ship)
                stages.select("1_1")
                state.set(State.ACTIVE)
            if menu_events.quit:
                gf.quit_game()

        # Active game state
        while state(State.ACTIVE):
            dt = clock.tick()
            active_events = gf.check_active_game_events(settings, screen, stats, hud,
                                                        ship, bullets, used_shields)
            if active_events.quit:
                gf.quit_game()
            if active_events.pause:
                state.set(State.PAUSED)

            gf.check_keys_pressed(ship)
            ship.update()

            if not (aliens or bosses) and stats.ships_left:
                stages.load_next_stage()

            gf.update_ship_shield(alien_bullets, used_shields, boss_bullets)
            gf.update_bullets(settings, stages, hud, ship, aliens, bullets, bosses, boss_bullets)
            gf.update_aliens(settings, screen, stats, stages, hud, ship, aliens,
                             bullets, alien_bullets, health, ammo, used_shields)
            gf.fire_alien_bullets(settings, screen, stages, ship, aliens, alien_bullets, dt)
            gf.update_alien_bullets(settings, screen, stats, stages, hud, ship,
                                    aliens, bullets, alien_bullets, health, ammo, used_shields)
            if stages.current.name == "green_boss":
                gf.update_green_boss(settings, screen, stats, stages, hud, ship, bullets,
                                     used_shields, bosses, boss_bullets, boss_shields, bosses)
                gf.fire_green_boss_bullets(settings, screen, dt, bosses, boss_bullets)
                gf.update_green_boss_bullets(settings, screen, stats, stages, hud, ship, bullets,
                                             used_shields, bosses, boss_bullets, boss_shields, black_holes)
                gf.update_green_boss_shield(hud, bullets, boss_shields)
            elif stages.current.name == "red_boss":
                gf.update_red_boss(settings, screen, stats, stages, hud, ship, bullets,
                                   used_shields, bosses, boss_bullets, boss_shields, black_holes)
                gf.update_red_boss_shield(hud, bullets, boss_shields)
                gf.fire_red_boss_bullets(settings, screen, ship, dt, bosses, boss_bullets)
                gf.update_red_boss_bullets(settings, screen, stats, stages, hud, ship, bullets,
                                           used_shields, bosses, boss_bullets, boss_shields, black_holes)
            elif stages.current.name == "blue_boss":
                gf.update_blue_boss(settings, screen, stats, stages, hud, ship, bullets,
                                    used_shields, bosses, boss_bullets, boss_shields, black_holes)
                gf.update_blue_boss_shield(hud, bullets, boss_shields)
                gf.fire_blue_boss_bullets(settings, screen, dt, bosses, boss_bullets)
                gf.update_blue_boss_bullets(settings, screen, stats, stages, hud, ship, bullets,
                                            used_shields, bosses, boss_bullets, boss_shields, black_holes)
                gf.create_black_hole(settings, screen, ship, dt, black_holes)
                gf.update_black_hole(settings, screen, stats, stages, hud, ship, bullets,
                                     used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)

            gf.update_ship_health(stats, hud, ship, health)
            gf.update_ship_ammo(stats, hud, ship, ammo)

            gf.update_screen(settings, screen, hud, ship, aliens, bullets, alien_bullets,
                             health, ammo, used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)

            if gf.check_game_end(stages, stats):
                state.set(State.MAIN_MENU)
                # Hide ship fast
                screen.fill(settings.bg_color)
                stages.current.teardown()
                pygame.display.flip()
                sleep(settings.game_sleep_time)


if __name__ == "__main__":
    run_game()
