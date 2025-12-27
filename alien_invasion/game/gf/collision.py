import time
from typing import TYPE_CHECKING

import pygame

from game.gf import common
from game.paths import Paths

if TYPE_CHECKING:
    from pygame.sprite import Group

    from game.boss_shield import BossShield
    from game.bosses import Boss
    from game.bullet import Bullet
    from game.hud import Hud
    from game.screen import Screen
    from game.settings import Settings
    from game.ship import Ship
    from game.sprites import Sprites
    from game.stats import Stats


def check_ship_aliens_collision(ship: "Ship", aliens: "Group") -> list | None:
    return pygame.sprite.spritecollideany(ship, aliens)


def check_ship_alien_bullets_collision(ship: "Ship", alien_bullets: "Group") -> list | None:
    return pygame.sprite.spritecollideany(ship, alien_bullets)


def check_ship_boss_bullets_collision(settings: "Settings",
                                      stats: "Stats",
                                      hud: "Hud",
                                      ship: "Ship",
                                      sprites: "Sprites") -> list | None:
    if collided := pygame.sprite.spritecollideany(ship, sprites.boss_bullets):
        common.ship_hit_on_boss_stage(settings=settings,
                                      stats=stats,
                                      hud=hud,
                                      ship=ship,
                                      sprites=sprites)
    return collided


def check_ship_bullets_boss_collision(settings: "Settings", sprites: "Sprites") -> None:
    if not pygame.sprite.groupcollide(sprites.ship_bullets,
                                      sprites.bosses,
                                      dokilla=True,
                                      dokillb=False):
        return

    boss: Boss = sprites.bosses.sprite
    boss.health_points -= 1
    boss.prepare_health()
    if boss.health_points < 1:
        time.sleep(settings.game_sleep_time)
        sprites.bosses.empty()
        sprites.boss_bullets.empty()


def check_ship_bosses_collision(settings: "Settings",
                                stats: "Stats",
                                hud: "Hud",
                                ship: "Ship",
                                sprites: "Sprites") -> list | None:
    if collided := pygame.sprite.spritecollideany(ship, sprites.bosses):
        common.ship_hit_on_boss_stage(settings=settings,
                                      stats=stats,
                                      hud=hud,
                                      ship=ship,
                                      sprites=sprites)
    return collided


def check_ship_bullets_boss_shield_collision(sprites: "Sprites") -> None:
    if pygame.sprite.groupcollide(sprites.boss_shields, sprites.ship_bullets, dokilla=False, dokillb=True):
        boss_shield: BossShield = sprites.boss_shields.sprite
        boss: Boss = sprites.bosses.sprite
        boss_shield.health_points -= 1
        boss.health_points -= 1
        boss.prepare_health()


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
                                     stats: "Stats",
                                     hud: "Hud",
                                     ship: "Ship",
                                     sprites: "Sprites") -> list | None:
    if collided := pygame.sprite.spritecollideany(ship, sprites.boss_black_holes):
        common.ship_hit_on_boss_stage(settings=settings,
                                      stats=stats,
                                      hud=hud,
                                      ship=ship,
                                      sprites=sprites)
    return collided


def check_bullets_screen_collision(screen: "Screen", bullets: "Group[Bullet]") -> None:
    screen_rect = screen.rect
    for bullet in bullets.copy():
        if not screen_rect.colliderect(bullet.rect):
            bullets.remove(bullet)
