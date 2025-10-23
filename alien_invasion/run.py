import logging
from argparse import ArgumentParser, Namespace

import pygame

from game.button import Button
from game.gf import common, events
from game.hud import Hud
from game.screen import Screen
from game.settings import Settings
from game.ship import Ship
from game.sprites import Sprites
from game.stages import Stages
from game.state import GameState, State
from game.stats import Stats


def initialize() -> None:
    pygame.init()
    pygame.display.set_caption("Alien Invasion")
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()


def run_game(args: Namespace) -> None:
    initialize()

    settings = Settings(health=args.health)
    screen = Screen(settings.screen_width, settings.screen_height)
    ship = Ship(settings, screen)
    stats = Stats(settings)
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
            pause_events = events.check_pause_events(ship)
            if pause_events.quit:
                events.quit_game()
            if pause_events.unpause:
               state.set(State.ACTIVE)

        # Menu state
        while state(State.MAIN_MENU):
            pygame.mouse.set_visible(True)

            menu_events = events.check_main_menu_events(play_button)
            common.update_main_menu_screen(settings=settings,
                                           screen=screen,
                                           play_button=play_button)

            if menu_events.play:
                common.initialize_game_from_main_menu(settings=settings,
                                                      stats=stats,
                                                      hud=hud,
                                                      ship=ship)
                stages.select(args.stage or stages.first.name)
                state.set(State.ACTIVE)
            if menu_events.quit:
                events.quit_game()

        # Active game state
        framerate = settings.framerate
        while state(State.ACTIVE):
            dt = clock.tick(framerate)
            active_events = events.check_active_game_events(settings=settings,
                                                            screen=screen,
                                                            stats=stats,
                                                            hud=hud,
                                                            ship=ship,
                                                            sprites=sprites)
            if active_events.quit:
                events.quit_game()
            if active_events.pause:
                state.set(State.PAUSED)

            common.handle_ship_diagonal_movement(ship)
            ship.update()

            if not (sprites.aliens or sprites.bosses) and stats.ships_left:
                if stages.current == stages.last:
                    state.set(State.MAIN_MENU)
                    events.end_game(settings=settings, screen=screen, stages=stages)
                    continue
                stages.load_next_stage()

            stages.current.update()
            stages.current.gameplay(dt)
            stages.current.check_collision()

            common.update_screen(settings=settings,
                                 screen=screen,
                                 hud=hud,
                                 ship=ship,
                                 sprites=sprites,
                                 dt=dt)

            if stats.ships_left < 1:
                state.set(State.MAIN_MENU)
                events.end_game(settings=settings, screen=screen, stages=stages)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--stage", type=str)
    parser.add_argument("--health", type=int)
    args = parser.parse_args()

    logging.basicConfig(filename="app.log", level=logging.DEBUG)

    run_game(args)
