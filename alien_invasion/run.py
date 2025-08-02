import logging
from time import sleep

import pygame

import game.game_functions as gf
from game.button import Button
from game.collections import Sprites
from game.game_stats import GameStats
from game.hud import Hud
from game.settings import Settings
from game.ship import Ship
from game.stages import Stages
from game.state import GameState, State


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
    sprites = Sprites()

    hud = Hud(settings, screen, stats, ship, sprites)
    stages = Stages(settings=settings,
                    screen=screen,
                    stats=stats,
                    hud=hud,
                    ship=ship,
                    sprites=sprites)

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
            active_events = gf.check_active_game_events(settings, screen, stats, hud, ship, sprites)
            if active_events.quit:
                gf.quit_game()
            if active_events.pause:
                state.set(State.PAUSED)

            gf.check_keys_pressed(ship)
            ship.update()

            if not (sprites.aliens or sprites.bosses) and stats.ships_left:
                stages.load_next_stage()

            gf.update_ship_shield(sprites.alien_bullets, sprites.ship_shields, sprites.boss_bullets)
            gf.update_bullets(settings, stages, hud, ship, sprites)
            gf.update_aliens(settings, screen, stats, stages, hud, ship, sprites)
            gf.fire_alien_bullets(settings, screen, stages, ship, dt, sprites)
            gf.update_alien_bullets(settings, screen, stats, stages, hud, ship, sprites)
            if stages.current.name == "green_boss":
                gf.update_green_boss(settings, screen, stats, stages, hud, ship, sprites)
                gf.fire_green_boss_bullets(settings, screen, dt, sprites.bosses, sprites.boss_bullets)
                gf.update_green_boss_bullets(settings, screen, stats, stages, hud, ship, sprites)
                gf.update_green_boss_shield(hud, sprites.ship_bullets, sprites.boss_shields)
            elif stages.current.name == "red_boss":
                gf.update_red_boss(settings, screen, stats, stages, hud, ship, sprites)
                gf.update_red_boss_shield(hud, sprites.ship_bullets, sprites.boss_shields)
                gf.fire_red_boss_bullets(settings, screen, ship, dt, sprites.bosses, sprites.boss_bullets)
                gf.update_red_boss_bullets(settings, screen, stats, stages, hud, ship, sprites)
            elif stages.current.name == "blue_boss":
                gf.update_blue_boss(settings, screen, stats, stages, hud, ship, sprites)
                gf.update_blue_boss_shield(hud, sprites.ship_bullets, sprites.boss_shields)
                gf.fire_blue_boss_bullets(settings, screen, dt, sprites.bosses, sprites.boss_bullets)
                gf.update_blue_boss_bullets(settings, screen, stats, stages, hud, ship, sprites)
                gf.create_black_hole(settings, screen, ship, dt, sprites.boss_black_holes)
                gf.update_black_hole(settings, screen, stats, stages, hud, ship, dt, sprites)

            gf.update_ship_health(stats, hud, ship, sprites.ship_health)
            gf.update_ship_ammo(stats, hud, ship, sprites.ship_ammo)

            gf.update_screen(settings, screen, hud, ship, dt, sprites)

            if gf.check_game_end(stages, stats):
                state.set(State.MAIN_MENU)
                # Hide ship fast
                screen.fill(settings.bg_color)
                stages.current.teardown()
                pygame.display.flip()
                sleep(settings.game_sleep_time)


if __name__ == "__main__":
    run_game()
