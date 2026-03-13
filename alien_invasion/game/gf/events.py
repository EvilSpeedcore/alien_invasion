import json
import sys
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

import game.rotation as rt
from game.gf.common import fire_bullet, use_ship_shield
from game.screen import ScreenSide
from game.utils import Singleton

if TYPE_CHECKING:
    from game.button import Button
    from game.hud import Hud
    from game.pause_menu import PauseMenu
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stages import Stages
    from game.stats import Stats


RECORDED_EVENTS: list[dict] = []


@dataclass
class MainMenuEvents:
    quit: bool = False
    play: bool = False

    def update(self, events: MainMenuEvents) -> None:
        # Update once
        self.quit = self.quit or events.quit
        self.play = self.play or events.play


@dataclass
class PauseEvents:
    quit: bool = False
    unpause: bool = False
    to_main_menu: bool = False

    def update(self, events: PauseEvents) -> None:
        # Update once
        self.quit = self.quit or events.quit
        self.unpause = self.unpause or events.unpause
        self.to_main_menu = self.to_main_menu or events.to_main_menu


@dataclass
class ActiveGameEvents:
    quit: bool = False
    pause: bool = False

    def update(self, events: ActiveGameEvents) -> None:
        # Update once
        self.quit = self.quit or events.quit
        self.pause = self.pause or events.pause


def check_active_game_keydown_events(event: Event,
                                     settings: Settings,
                                     screen: Screen,
                                     stats: Stats,
                                     hud: Hud,
                                     ship: Ship,
                                     sprites: Sprites) -> ActiveGameEvents:
    events = ActiveGameEvents()
    match event.key:
        case pygame.K_RIGHT:
            ship.desirable_ship_rotation = ScreenSide.RIGHT
            ship.moving_right = True
            rt.rotate(ship)
        case pygame.K_LEFT:
            ship.desirable_ship_rotation = ScreenSide.LEFT
            ship.moving_left = True
            rt.rotate(ship)
        case pygame.K_UP:
            ship.desirable_ship_rotation = ScreenSide.TOP
            ship.moving_up = True
            rt.rotate(ship)
        case pygame.K_DOWN:
            ship.desirable_ship_rotation = ScreenSide.BOTTOM
            ship.moving_down = True
            rt.rotate(ship)
        case pygame.K_a:
            fire_bullet(settings, screen, stats, ship, sprites.ship_bullets)
        case pygame.K_SPACE:
            events.update(ActiveGameEvents(pause=True))
        case pygame.K_d:
            use_ship_shield(screen, stats, hud, ship, sprites.ship_shields)
    return events


def check_pause_keydown_events(event: Event, ship: Ship) -> PauseEvents:
    events = PauseEvents()
    match event.key:
        case pygame.K_RIGHT:
            ship.desirable_ship_rotation = ScreenSide.RIGHT
            ship.moving_right = True
            rt.rotate(ship)
        case pygame.K_LEFT:
            ship.desirable_ship_rotation = ScreenSide.LEFT
            ship.moving_left = True
            rt.rotate(ship)
        case pygame.K_UP:
            ship.desirable_ship_rotation = ScreenSide.TOP
            ship.moving_up = True
            rt.rotate(ship)
        case pygame.K_DOWN:
            ship.desirable_ship_rotation = ScreenSide.BOTTOM
            ship.moving_down = True
            rt.rotate(ship)
        case pygame.K_s:
            events.update(PauseEvents(unpause=True))
    return events


def check_active_game_keyup_events(event: Event, ship: Ship) -> ActiveGameEvents:
    check_keyup_events(event, ship)
    return ActiveGameEvents()


def check_pause_keyup_events(event: Event, ship: Ship) -> PauseEvents:
    check_keyup_events(event, ship)
    return PauseEvents()


def check_keyup_events(event: Event, ship: Ship) -> None:
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


def check_active_game_events(settings: Settings,
                             screen: Screen,
                             stats: Stats,
                             hud: Hud,
                             ship: Ship,
                             sprites: Sprites) -> ActiveGameEvents:
    active_game_events = ActiveGameEvents()
    events = Events().get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                active_game_events.update(ActiveGameEvents(quit=True))
            case pygame.KEYDOWN:
                active_game_events.update(
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
                active_game_events.update(check_active_game_keyup_events(event, ship))

    if Events().record:
        Events().add(events)

    return active_game_events


def check_pause_events(ship: Ship, pause_menu: PauseMenu) -> PauseEvents:
    events = PauseEvents()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                events.update(PauseEvents(quit=True))
            case pygame.KEYDOWN:
                events.update(check_pause_keydown_events(event, ship))
            case pygame.KEYUP:
                events.update(check_pause_keyup_events(event, ship))
            case pygame.MOUSEBUTTONDOWN:
                events.update(PauseEvents(to_main_menu=check_pause_back_to_menu_button_pressed(pause_menu)))
    return events


def check_main_menu_events(play_button: Button) -> MainMenuEvents:
    main_menu_events = MainMenuEvents()
    events = Events().get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                main_menu_events.update(MainMenuEvents(quit=True))
            case pygame.MOUSEBUTTONDOWN:
                main_menu_events.update(MainMenuEvents(play=check_play_button_pressed(play_button)))
            case pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_menu_events.update(MainMenuEvents(play=True))

    if Events().record:
        Events().add(events)

    return main_menu_events


def check_play_button_pressed(play_button: Button) -> bool:
    return play_button.ellipse_rect.collidepoint(pygame.mouse.get_pos())


def check_pause_back_to_menu_button_pressed(pause_menu: PauseMenu) -> bool:
    position = pause_menu.get_mouse_position()
    return pause_menu.back_to_menu_button.ellipse_rect.collidepoint(position)


def quit_game() -> None:
    Events().dump()
    pygame.quit()
    sys.exit(0)


def end_game(settings: Settings, screen: Screen, stages: Stages) -> None:
    # Hide ship fast
    screen.it.fill(settings.bg_color)
    stages.current.teardown()
    pygame.display.flip()
    time.sleep(settings.game_sleep_time)


class Events(metaclass=Singleton):

    def __init__(self) -> None:
        self.recorded_events: list[list[dict]] = []
        self.events: deque[list[Event]] = deque()

        self.record_filepath: str | None = None
        self.loaded = False

    @property
    def record(self) -> bool:
        return bool(self.record_filepath)

    def get(self) -> list[Event]:
        if not self.loaded:
            return pygame.event.get()

        try:
            return self.events.popleft()
        except IndexError:
            return []

    def add(self, events: list[Event]) -> None:
        self.recorded_events.append([{"type": event.type, "dict": event.dict} for event in events])

    def load(self, filepath: str) -> None:
        with Path(filepath).open(encoding="utf-8") as events_file:
            data = json.load(events_file)

        for events in data:
            if not events:
                self.events.append(events)
            else:
                self.events.append([Event(events["type"], events["dict"]) for events in events])

        self.loaded = True

    def dump(self) -> None:
        if not self.recorded_events or not self.record_filepath:
            return

        with Path(self.record_filepath).open("w", encoding="utf-8") as events_file:
            json.dump(self.recorded_events, events_file, indent=4)
