from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Group, GroupSingle

import game.game_functions as gf
from game.button import Button
from game.game_stats import GameStats
from game.hud import Hud
from game.settings import Settings
from game.ship import Ship

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
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings, screen)
    stats = GameStats(ai_settings)
    hud = Hud(ai_settings, screen, stats, ship)
    play_button = Button(screen, "Start")

    bullets: Group["Bullet"] = Group()
    aliens: Group["Alien"] = Group()
    alien_bullets: Group["AlienBullet"] = Group()
    health: Group["ShipHealth"] = Group()
    ammo: Group["ShipAmmo"] = Group()
    used_shields: Group["ShipHealth"] = Group()
    boss_bullets: Group["BossBullet"] = Group()
    # TODO: How to type GroupSingle?
    bosses: GroupSingle = GroupSingle()
    boss_shields: GroupSingle = GroupSingle()
    black_holes: GroupSingle = GroupSingle()

    clock = pygame.time.Clock()
    ai_settings.state = ai_settings.running
    # Main game cycle.
    while True:
        dt = clock.tick()
        gf.check_events(ai_settings, screen, stats, hud, play_button, ship, aliens, bullets, used_shields)
        gf.check_keys_pressed(ship)
        if ai_settings.state == ai_settings.running:
            if stats.game_active:
                ship.update()
                gf.update_ship_shield(ship, alien_bullets, used_shields, boss_bullets)
                gf.update_bullets(ai_settings, screen, stats, hud, ship, aliens, bullets,
                                  alien_bullets, health, ammo, bosses, boss_bullets, boss_shields, black_holes)
                gf.update_aliens(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health,
                                 ammo, used_shields)
                gf.fire_alien_bullets(ai_settings, screen, stats, ship, aliens, alien_bullets, dt)
                gf.update_alien_bullets(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health,
                                        ammo, used_shields)
                if stats.stage == ai_settings.boss_stages[0]:
                    gf.update_green_boss(ai_settings, screen, stats, hud, ship, bullets,
                                         used_shields, bosses, boss_bullets, boss_shields, bosses)
                    gf.fire_green_boss_bullets(ai_settings, screen, dt, bosses, boss_bullets)
                    gf.update_green_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                                                 used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_green_boss_shield(hud, bullets, boss_shields)
                elif stats.stage == ai_settings.boss_stages[1]:
                    gf.update_red_boss(ai_settings, screen, stats, hud, ship, bullets,
                                       used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_red_boss_shield(hud, bullets, boss_shields)
                    gf.fire_red_boss_bullets(ai_settings, screen, ship, dt, bosses, boss_bullets)
                    gf.update_red_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                                               used_shields, bosses, boss_bullets, boss_shields, black_holes)
                elif stats.stage == ai_settings.boss_stages[2]:
                    gf.update_blue_boss(ai_settings, screen, stats, hud, ship, bullets,
                                        used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.update_blue_boss_shield(hud, bullets, boss_shields)
                    gf.fire_blue_boss_bullets(ai_settings, screen, dt, bosses, boss_bullets)
                    gf.update_blue_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                                                used_shields, bosses, boss_bullets, boss_shields, black_holes)
                    gf.create_black_hole(ai_settings, screen, ship, dt, black_holes)
                    gf.update_black_hole(ai_settings, screen, stats, hud, ship, bullets,
                                         used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)

                gf.update_ship_health(stats, hud, ship, health)
                gf.update_ship_ammo(stats, hud, ship, ammo)

            gf.update_screen(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, play_button,
                             health, ammo, used_shields, dt, bosses, boss_bullets, boss_shields, black_holes)


if __name__ == '__main__':
    run_game()
