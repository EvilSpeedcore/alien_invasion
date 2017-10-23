import sys
import pygame
import rotation as rt
import random
from bullet import Bullet
from alien import Alien
from ship_consumables import ShipHealth, ShipAmmo, ShipShield
from time import sleep
from alien_bullet import AlienBullet
from bosses import GreenBoss, RedBoss, BlueBoss
from bosses_bullets import GreenBossBullet, RedBossBullet, BlueBossBullet
from boss_shield import GreenBossShield, RedBossShield, BlueBossShield
from black_hole import BlackHole


def check_keydown_events(event, ai_settings, screen, stats, hud, ship, bullets, used_shields):
    """Handle events, when a key is pressed down.

    Args:
        :param event: KEYDOWN events, when the keyboard buttons are pressed.
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStars class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Instance of Bullet class.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
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
        fire_bullet(ai_settings, screen, stats, ship, bullets)
    if event.key == pygame.K_r:
        pass
    if stats.game_active:
        if event.key == pygame.K_SPACE:
            ai_settings.state = ai_settings.paused
    if event.key == pygame.K_s:
        ai_settings.state = ai_settings.running
    if event.key == pygame.K_d:
        use_ship_shield(ai_settings, screen, stats, hud, ship, used_shields)


def check_keyup_events(event, ship):
    """Handle events when a key is released.

    Args:
        :param event: KEYUP events, when the keyboard buttons released.
        :param ship: Instance of Ship class.

    """
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


def check_events(ai_settings, screen, stats, hud, play_button, ship, aliens, bullets, used_shields):
    """Handle keyup, keydown and mouse events.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param play_button: Instance of Button class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, hud, ship, bullets, used_shields)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, hud, play_button, ship, aliens, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, hud, play_button, ship, aliens, mouse_x, mouse_y):
    """Check if button to start the game is pressed.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param play_button: Instance of Button class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Aliens Sprites.
        :param mouse_x: X position of the mouse cursor.
        :param mouse_y: Y position of the mouse cursor.

    """
    button_clicked = play_button.ellipse_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        create_fleet(ai_settings, screen, stats, ship, aliens)
        ship.center_ship()
        rt.rotate_to_up(ship)
        hud.prep_health()
        hud.prep_ammo()
        hud.prep_shield()


def check_keys_pressed(ship):
    """Handle ship diagonal movement.

    Args:
        :param ship: Instance of Ship class.

    """
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


def update_screen(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, play_button, health, ammo,
                  used_shields, dt, bosses, boss_bullets, boss_shields, black_holes):
    """Update screen.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param play_button: Instance of Button class.
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param dt: Game timer to manage events.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    screen.fill(ai_settings.bg_color)

    #  Draw ship bullets on screen.
    for bullet in bullets.sprites():        
        bullet.draw_bullet()

    # Draw alien bullets on screen.
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()
    for green_boss_bullet in boss_bullets.sprites():
        green_boss_bullet.draw_bullet()
    for red_boss_bullet in boss_bullets.sprites():
        red_boss_bullet.draw_bullet()

    #  Ship shield duration handling.
    if len(used_shields) == 1:
        ai_settings.time_elapsed_since_shield += dt
        if ai_settings.time_elapsed_since_shield > 3000:
            ai_settings.time_elapsed_since_shield = 0
            used_shields.empty()

    #  Display ship shield on hud.
    for used_shield in used_shields:
        used_shield.draw_item()

    #  Display boss shield on hud.
    for boss_shield in boss_shields:
        if boss_shield.points > 0:
            boss_shield.draw_boss_shield()
            boss_shield.update()
        else:
            boss_shields.empty()

    if not stats.game_active:
        # Show start button and clear the screen.
        used_shields.empty()
        bosses.empty()
        boss_shields.empty()
        black_holes.empty()
        boss_bullets.empty()
        play_button.prep_msg(play_button.msg)
        play_button.draw_button()
    else:
        # Prepare initial state of game.
        hud.show_hud()
        ship.blitme()
        for health in health.sprites():
            health.draw_item()
        for ammo in ammo.sprites():
            ammo.draw_item()
        aliens.draw(screen)
        bosses.draw(screen)
    for black_hole in black_holes.sprites():
        black_hole.draw_black_hole()

    # Update screen.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health, ammo, bosses,
                   boss_bullets, boss_shields, black_holes):
    """Update ship bullets. Remove bullet from group of sprites, if it reach edge of the screen. Check for collisions.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    bullets.update(ship)
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
    # Check for collision between ship bullets and aliens.
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets,
                                  alien_bullets, health, ammo, bosses, black_holes)
    # Check for collision between ship billet and boss.
    check_bullet_boss_collision(ai_settings, screen, stats, hud, ship, aliens, bullets,
                                alien_bullets, bosses, boss_bullets, boss_shields, black_holes)


def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets,
                                  alien_bullets, health, ammo, bosses, black_holes):
    """Handle collisions between ship bullets and aliens.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0 and len(bosses) == 0:
        stats.stage += 1
        if stats.stage > ai_settings.boss_stages[2]:
            stats.game_active = False
            pygame.mouse.set_visible(True)
        if stats.stage in ai_settings.non_boss_stages:

            # CLS when moving to the next stage.
            ship.center_ship()
            health.empty()
            ammo.empty()
            alien_bullets.empty()
            bullets.empty()
            black_holes.empty()

            #  Flag, which shows the fact, that extra health not yet spawned.
            health_spawned = False

            # Extra health spawn.
            if stats.ships_left < 4:
                    random_number = random.choice([x for x in range(1, 6)])
                    if random_number == 1:
                        new_health = ShipHealth(ai_settings, screen)
                        banned_coordinates_x = [x for x in range(int(ship.centerx - 100.0), int(ship.centerx + 106.0))]
                        available_coordinates_x = [x for x in range(100, ship.screen_rect.right - 100) if
                                                   x not in banned_coordinates_x]
                        banned_coordinates_y = [y for y in range(int(ship.centery - 100.0), int(ship.centery + 106.0))]
                        available_coordinates_y = [y for y in range(100, ship.screen_rect.bottom - 100) if
                                                   y not in banned_coordinates_y]
                        new_health.rect.x = random.choice(available_coordinates_x)
                        new_health.rect.y = random.choice(available_coordinates_y)
                        health.add(new_health)
                        health_spawned = True
                    else:
                        health.empty()

            # Extra ammo spawn.
            if not health_spawned:
                if stats.ammo < 3:
                    random_number = random.choice([x for x in range(1, 6)])
                    if random_number == 1:
                        new_ammo = ShipAmmo(ai_settings, screen)

                        _banned_coordinates_x = [x for x in range(int(ship.centerx - 100.0), int(ship.centerx + 106.0))]
                        _available_coordinates_x = [x for x in range(100, ship.screen_rect.right - 100) if
                                                    x not in _banned_coordinates_x]

                        _banned_coordinates_y = [y for y in range(int(ship.centery - 100.0), int(ship.centery + 106.0))]
                        _available_coordinates_y = [y for y in range(100, ship.screen_rect.bottom - 100) if
                                                    y not in _banned_coordinates_y]

                        new_ammo.rect.x = random.choice(_available_coordinates_x)
                        new_ammo.rect.y = random.choice(_available_coordinates_y)

                        ammo.add(new_ammo)
                    else:
                        ammo.empty()

            #  Aliens movement speed increase.

            ai_settings.increase_aliens_speed()

            #  Create new fleet of aliens.
            create_fleet(ai_settings, screen, stats, ship, aliens)


def check_bullet_boss_collision(ai_settings, screen, stats, hud, ship, aliens, bullets,
                                alien_bullets, bosses, boss_bullets, boss_shields, black_holes):
    """Handle collisions between ship bullets and bosses.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    # Check collisions between ship and green boss.
    if stats.stage == ai_settings.boss_stages[0]:
        if len(aliens) == 0 and len(bosses) == 0:
            create_green_boss(ai_settings, screen, hud, bosses, boss_shields)
            alien_bullets.empty()
            bullets.empty()
            ship.prepare_for_boss()
            rt.rotate_to_up(ship)
        boss_collision = pygame.sprite.groupcollide(bullets, bosses, True, False)
        if boss_collision:
            for boss in bosses.sprites():
                boss.hit_points -= 1
                hud.green_boss_hp -= 1
                hud.prep_green_boss_health()
                if boss.hit_points < 1:
                    sleep(ai_settings.game_sleep_time)
                    bosses.empty()
                    boss_bullets.empty()

    # Check collisions between ship and red boss.
    elif stats.stage == ai_settings.boss_stages[1]:
        if len(aliens) == 0 and len(bosses) == 0:
            create_red_boss(ai_settings, screen, hud, bosses, boss_shields)
            alien_bullets.empty()
            bullets.empty()
            ship.prepare_for_boss()
            rt.rotate_to_up(ship)
        boss_collision = pygame.sprite.groupcollide(bullets, bosses, True, False)
        if boss_collision:
            for boss in bosses.sprites():
                boss.hit_points -= 1
                hud.red_boss_hp -= 1
                hud.prep_red_boss_health()
                if boss.hit_points < 1:
                    sleep(ai_settings.game_sleep_time)
                    bosses.empty()
                    boss_bullets.empty()

    # Check collisions between ship and blue boss.
    elif stats.stage == ai_settings.boss_stages[2]:
        if len(aliens) == 0 and len(bosses) == 0:
            create_blue_boss(ai_settings, screen, hud, bosses, boss_shields)
            alien_bullets.empty()
            bullets.empty()
            black_holes.empty()
            ship.prepare_for_boss()
            rt.rotate_to_up(ship)
        boss_collision = pygame.sprite.groupcollide(bullets, bosses, True, False)
        if boss_collision:
            for boss in bosses.sprites():
                boss.hit_points -= 1
                hud.blue_boss_hp -= 1
                hud.prep_blue_boss_health()
                if boss.hit_points < 1:
                    sleep(ai_settings.game_sleep_time)
                    bosses.empty()
                    boss_bullets.empty()


def fire_bullet(ai_settings, screen, stats, ship, bullets):
    """Create ship bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.

    """
    if len(bullets) < stats.ammo:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculate number of aliens in row.

    Args:
        :param ai_settings: Instance of Settings class.
        :param alien_width: Width of an alien Surface.

    Returns:
        :return: number_aliens_x: Maximum number of aliens on screen in one row.

    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, stats, ship, aliens, alien_number):
    """Create an alien and place it in a row.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param alien_number: Maximum number of aliens on screen in one row.

    """
    alien = Alien(ai_settings, screen, ship)    
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.fleet_creation_time = int(round(pygame.time.get_ticks()/1000)) + 1
    if stats.stage < ai_settings.boss_stages[0]:
        alien.alien_color = "green"
    elif stats.stage < ai_settings.boss_stages[1]:
        alien.image = alien.red_alien
        alien.alien_color = "red"
    elif stats.stage >= ai_settings.boss_stages[0] + 1:
        alien.image = alien.blue_alien
        alien.alien_color = "blue"
    aliens.add(alien)


def create_fleet(ai_settings, screen, stats, ship, aliens):
    """Create alien fleet.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.

    """
    alien = Alien(ai_settings, screen, ship)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, stats, ship, aliens, alien_number)


def ship_hit(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health, ammo, used_shields):
    """Handle collisions between ship and aliens.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
    if stats.ships_left > 1:      
        stats.ships_left -= 1
        hud.prep_health()
        health.empty()
        ammo.empty()
        used_shields.empty()
        ai_settings.time_elapsed_since_shield = 0
    else:
        stats.game_active = False
        sleep(ai_settings.game_sleep_time)
        pygame.mouse.set_visible(True)
    alien_bullets.empty()    
    aliens.empty()
    bullets.empty()
    if stats.game_active:
        create_fleet(ai_settings, screen, stats, ship, aliens)
        ship.center_ship()
        sleep(ai_settings.game_sleep_time)


def ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                           used_shields, bosses, boss_bullets, boss_shields, black_holes):
    """Handle collisions between ship and bosses.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    # Handle collisions between ship and green boss.
    if stats.stage == ai_settings.boss_stages[0]:
        if stats.ships_left > 1:
            stats.ships_left -= 1
            hud.prep_health()
            hud.green_boss_hp = 19
            hud.prep_green_boss_health()
            used_shields.empty()

            # Ship and boss shield timer refresh.
            ai_settings.time_elapsed_since_shield = 0
            ai_settings.time_elapsed_since_boss_shield = 0
        else:
            stats.game_active = False
            sleep(ai_settings.game_sleep_time)
            pygame.mouse.set_visible(True)
        bullets.empty()
        bosses.empty()
        boss_bullets.empty()
        if stats.game_active:
            create_green_boss(ai_settings, screen, hud, bosses, boss_shields)
            ship.prepare_for_boss()
            sleep(ai_settings.game_sleep_time)

    # Handle collisions between ship and red boss.
    elif stats.stage == ai_settings.boss_stages[1]:
        if stats.ships_left > 1:
            stats.ships_left -= 1
            hud.prep_health()
            hud.red_boss_hp = 14
            hud.prep_red_boss_health()
            used_shields.empty()
            ai_settings.time_elapsed_since_shield = 0
            ai_settings.time_elapsed_since_boss_shield = 0
        else:
            stats.game_active = False
            sleep(ai_settings.game_sleep_time)
            pygame.mouse.set_visible(True)
        bullets.empty()
        bosses.empty()
        boss_bullets.empty()
        if stats.game_active:
            create_red_boss(ai_settings, screen, hud, bosses, boss_shields)
            ship.prepare_for_boss()
            sleep(ai_settings.game_sleep_time)

    # Handle collisions between ship and blue boss.
    elif stats.stage == ai_settings.boss_stages[2]:
        if stats.ships_left > 1:
            stats.ships_left -= 1
            hud.prep_health()
            hud.blue_boss_hp = 19
            hud.prep_blue_boss_health()
            used_shields.empty()
            boss_bullets.empty()
            ai_settings.black_hole_spawn_timer = 0
            ai_settings.time_elapsed_since_shield = 0
            ai_settings.time_elapsed_since_boss_shield = 0
        else:
            stats.game_active = False
            sleep(ai_settings.game_sleep_time)
            pygame.mouse.set_visible(True)
        bullets.empty()
        bosses.empty()
        if stats.game_active:
            black_holes.empty()
            create_blue_boss(ai_settings, screen, hud, bosses, boss_shields)
            ship.prepare_for_boss()
            sleep(ai_settings.game_sleep_time)


def update_aliens(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health, ammo, used_shields):
    """Update aliens position in fleet.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
    aliens.update(aliens, ship)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health, ammo, used_shields)


def update_ship_health(stats, hud, ship, health):
    """Update extra health on hud after pick-up.

    Args:
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param health: Container to hold and manage ShipHealth Sprites.

    """
    if pygame.sprite.spritecollideany(ship, health):
        effect = pygame.mixer.Sound('effects/pick_up_1.ogg')
        effect.play()
        health.empty()
        stats.ships_left += 1
        hud.prep_health()


def update_ship_ammo(stats, hud, ship, ammo):
    """Update extra ammo om hud after pick-up.

    Args:
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param ammo: Container to hold and manage ShipAmmo Sprites.

    """
    if pygame.sprite.spritecollideany(ship, ammo):
        stats.ammo += 1
        ammo.empty()
        hud.prep_ammo()


def fire_alien_bullets(ai_settings, screen, stats, ship, aliens, alien_bullets, dt):
    """Create alien bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param dt: Game timer to manage events.

    """
    ai_settings.time_elapsed_since_last_alien_bullet += dt
    if ai_settings.time_elapsed_since_last_alien_bullet > 2500:
        for alien in aliens:
            alien_bullet = AlienBullet(ai_settings, screen, alien)
            if stats.stage < ai_settings.boss_stages[0]:
                pass
            elif stats.stage < ai_settings.boss_stages[1] + 1:
                alien_bullet.image = alien_bullet.red_bullet
            elif stats.stage >= ai_settings.boss_stages[1] + 1:
                alien_bullet.image = alien_bullet.blue_bullet
            alien_bullet.define_position(ship)
            alien_bullets.add(alien_bullet)
        ai_settings.time_elapsed_since_last_alien_bullet = 0


def fire_green_boss_bullets(ai_settings, screen, dt, bosses, boss_bullets):
    """Create green boss bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param dt: Game timer to manage events.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.

    """
    ai_settings.time_elapsed_since_last_boss_bullet += dt
    if ai_settings.time_elapsed_since_last_boss_bullet > ai_settings.green_boss_bullet_timer:
        for boss in bosses:
            green_boss_bullet_1 = GreenBossBullet(ai_settings, screen, boss)
            green_boss_bullet_1.shooting_angle_up = random.choice([x for x in range(0, 180)])
            green_boss_bullet_1.add(boss_bullets)

            green_boss_bullet_2 = GreenBossBullet(ai_settings, screen, boss)
            green_boss_bullet_2.shooting_angle_up = random.choice([x for x in range(90, 270)])
            green_boss_bullet_2.add(boss_bullets)

            green_boss_bullet_3 = GreenBossBullet(ai_settings, screen, boss)
            green_boss_bullet_3.shooting_angle_up = random.choice([x for x in range(180, 360)])
            green_boss_bullet_3.add(boss_bullets)

            green_boss_bullet_4 = GreenBossBullet(ai_settings, screen, boss)
            green_boss_bullet_4.shooting_angle_up = random.choice([x for x in range(270, 450)])
            green_boss_bullet_4.add(boss_bullets)

        ai_settings.time_elapsed_since_last_boss_bullet = 0
        ai_settings.green_boss_bullet_timer = 1650


def update_alien_bullets(ai_settings, screen, stats, hud, ship, aliens, bullets,
                         alien_bullets, health, ammo, used_shields):
    """Update alien bullets position.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param aliens: Container to hold and manage Alien Sprites.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites
        :param health: Container to hold and manage ShipHealth Sprites.
        :param ammo: Container to hold and manage ShipAmmo Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
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
        ship_hit(ai_settings, screen, stats, hud, ship, aliens, bullets, alien_bullets, health, ammo, used_shields)


def use_ship_shield(ai_settings, screen, stats, hud, ship, used_shields):
    """Handle use of ship shield.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param used_shields: Container to hold and manage ShipShield Sprites.

    """
    if stats.game_active:
        if stats.shields_left >= 1:
            effect = pygame.mixer.Sound('effects/1.ogg')
            effect.play()
            used_shield = ShipShield(ai_settings, screen, ship)
            used_shields.add(used_shield)
            stats.shields_left -= 1
            hud.prep_shield()


def update_ship_shield(ship, alien_bullets, used_shields, boss_bullets):
    """Update ship shield position. Check for collisions between shield and bullet.

    Args:
        :param ship: Instance of Ship class.
        :param alien_bullets: Container to hold and manage AlienBullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.

    """
    used_shields.update(ship)
    pygame.sprite.groupcollide(used_shields, alien_bullets, False, True)
    pygame.sprite.groupcollide(used_shields, boss_bullets, False, True)


def create_green_boss(ai_settings, screen, hud, bosses, boss_shields):
    """Create green boss.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param hud: Instance of Hud class.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_shields: Container to hold and manage single BossShield Sprite.

    """
    green_boss = GreenBoss(ai_settings, screen)
    boss_shield = GreenBossShield(ai_settings, screen, green_boss)
    hud.green_boss_hp = 19
    hud.prep_green_boss_health()
    bosses.add(green_boss)
    boss_shields.add(boss_shield)


def create_blue_boss(ai_settings, screen, hud, bosses, boss_shields):
    """Create blue boss.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param hud: Instance of Hud class.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_shields: Container to hold and manage single BossShield Sprite.

    """
    blue_boss = BlueBoss(ai_settings, screen)
    boss_shield = BlueBossShield(ai_settings, screen, blue_boss)
    hud.blue_boss_hp = 19
    hud.prep_blue_boss_health()
    bosses.add(blue_boss)
    boss_shields.add(boss_shield)


def update_green_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                              used_shields, bosses, boss_bullets, boss_shields, black_holes):
    """Update green boss bullets position. Check for collisions between ship and boss bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    boss_bullets.update()
    for green_boss_bullet in boss_bullets.copy():
        green_boss_bullet.change_direction(boss_bullets)

    if pygame.sprite.spritecollideany(ship, boss_bullets):
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)


def create_red_boss(ai_settings, screen, hud, bosses, boss_shields):
    """Create red boss.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param hud: Instance of Hud class.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_shields: Container to hold and manage single BossShield Sprite.

    """
    red_boss = RedBoss(ai_settings, screen)
    boss_shield = RedBossShield(ai_settings, screen, red_boss)
    hud.red_boss_hp = 14
    hud.prep_red_boss_health()
    bosses.add(red_boss)
    boss_shields.add(boss_shield)


def fire_red_boss_bullets(ai_settings, screen, ship, dt, bosses, boss_bullets):
    """Create red boss bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param ship: Instance of Ship class.
        :param dt: Game timer to manage events.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.

    """
    ai_settings.time_elapsed_since_last_red_boss_bullet += dt
    if ai_settings.time_elapsed_since_last_red_boss_bullet > 1350:
        for boss in bosses:
            red_boss_bullet = RedBossBullet(ai_settings, screen, boss)
            red_boss_bullet.define_position(ship)
            red_boss_bullet.add(boss_bullets)

            red_boss_bullet_2 = RedBossBullet(ai_settings, screen, boss)
            red_boss_bullet_2.define_position(ship)
            red_boss_bullet_2.shooting_angle += 15
            red_boss_bullet_2.add(boss_bullets)

            red_boss_bullet_3 = RedBossBullet(ai_settings, screen, boss)
            red_boss_bullet_3.define_position(ship)
            red_boss_bullet_3.shooting_angle += 30
            red_boss_bullet_3.add(boss_bullets)

            red_boss_bullet_4 = RedBossBullet(ai_settings, screen, boss)
            red_boss_bullet_4.define_position(ship)
            red_boss_bullet_4.shooting_angle -= 15
            red_boss_bullet_4.add(boss_bullets)

            red_boss_bullet_5 = RedBossBullet(ai_settings, screen, boss)
            red_boss_bullet_5.define_position(ship)
            red_boss_bullet_5.shooting_angle -= 30
            red_boss_bullet_5.add(boss_bullets)

            ai_settings.time_elapsed_since_last_red_boss_bullet = 0


def fire_blue_boss_bullets(ai_settings, screen, dt, bosses, boss_bullets):
    """Create blue boss bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param dt: Game timer to manage events.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.

    """
    ai_settings.time_elapsed_since_last_red_boss_bullet += dt
    if ai_settings.time_elapsed_since_last_red_boss_bullet > 300:
        for boss in bosses:
            blue_boss_bullet = BlueBossBullet(ai_settings, screen, boss, boss.shooting_angle)
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(ai_settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[0]))
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(ai_settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[1]))
            blue_boss_bullet.add(boss_bullets)

            blue_boss_bullet = BlueBossBullet(ai_settings, screen, boss,
                                              (boss.shooting_angle + boss.shooting_angles[2]))
            blue_boss_bullet.add(boss_bullets)

            ai_settings.time_elapsed_since_last_red_boss_bullet = 0
            if boss.rt_trigger:
                boss.shooting_angle += 15
                if boss.shooting_angle > 400:
                    boss.rt_trigger = False
            else:
                boss.shooting_angle -= 15
                if boss.shooting_angle < 0:
                    boss.rt_trigger = True


def update_red_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                            used_shields, bosses, boss_bullets, boss_shields, black_holes):
    """Update red boss bullets position. Check for collisions between ship and boss bullets.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
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
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)


def update_blue_boss_bullets(ai_settings, screen, stats, hud, ship, bullets,
                             used_shields, bosses, boss_bullets, boss_shields, black_holes):
    """Update blue boss bullets position. Check for collisions between ship and boss bullets.

    Args
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
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
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)


def update_green_boss(ai_settings, screen, stats, hud, ship, bullets, used_shields, bosses,
                      boss_bullets, boss_shields, black_holes):
    """Check for collisions between green boss and ship.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    if pygame.sprite.spritecollideany(ship, bosses):
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)


def update_green_boss_shield(hud, bullets, boss_shields):
    """Update hit points of green boss shield on a collision with ship bullets.

    Args:
        :param hud: Instance of Hud class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param boss_shields: Container to hold and manage BossBullet Sprites.

    """
    if pygame.sprite.groupcollide(boss_shields, bullets, False, True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.green_boss_hp -= 1
            hud.prep_green_boss_health()


def update_red_boss(ai_settings, screen, stats, hud, ship, bullets, used_shields, bosses,
                    boss_bullets, boss_shields, black_holes):
    """Update red boss position. Check for collisions between red boss and ship.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    if pygame.sprite.spritecollideany(ship, bosses):
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)
    for boss in bosses:
        boss.update()


def update_blue_boss(ai_settings, screen, stats, hud, ship, bullets, used_shields, bosses,
                     boss_bullets, boss_shields, black_holes):
    """Check for collisions between blue boss and ship

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    if pygame.sprite.spritecollideany(ship, bosses):
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)


def update_red_boss_shield(hud, bullets, boss_shields):
    """Update hit points of red boss shield on a collision with ship bullets.

    Args:
        :param hud: Instance of Hud class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param boss_shields: Container to hold and manage BossShield Sprites.

    """
    if pygame.sprite.groupcollide(boss_shields, bullets, False, True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.red_boss_hp -= 1
            hud.prep_red_boss_health()


def update_blue_boss_shield(hud, bullets, boss_shields):
    """Update hit points of blue boss shield on a collision with ship bullets

    Args:
        :param hud: Instance of Hud class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param boss_shields: Container to hold and manage BossShield Sprites.

    """
    if pygame.sprite.groupcollide(boss_shields, bullets, False, True):
        for boss_shield in boss_shields:
            boss_shield.points -= 1
            hud.blue_boss_hp -= 1
            hud.prep_blue_boss_health()


def create_black_hole(ai_settings, screen, ship, dt, black_holes):
    """Create black hole.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param ship: Instance of Ship class.
        :param dt: Game timer to manage events.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    ai_settings.black_hole_spawn_timer += dt
    if len(black_holes) == 0:
        if ai_settings.black_hole_spawn_timer > 2000:
            black_hole = BlackHole(ai_settings, screen, ship)
            black_holes.add(black_hole)
    elif len(black_holes) == 1:
        if ai_settings.black_hole_spawn_timer > 6000:
            black_holes.empty()
            ai_settings.black_hole_spawn_timer = 0


def update_black_hole(ai_settings, screen, stats, hud, ship, bullets, used_shields, dt, bosses,
                      boss_bullets, boss_shields, black_holes):
    """Update black hole animation. Check for collisions between ship and black hole.

    Args:
        :param ai_settings: Instance of Settings class.
        :param screen: Display Surface.
        :param stats: Instance of GameStats class.
        :param hud: Instance of Hud class.
        :param ship: Instance of Ship class.
        :param bullets: Container to hold and manage Bullet Sprites.
        :param used_shields: Container to hold and manage ShipShield Sprites.
        :param dt: Game timer to manage events.
        :param bosses: Container to hold and manage single Bosses Sprite.
        :param boss_bullets: Container to hold and manage BossBullet Sprites.
        :param boss_shields: Container to hold and manage single BossShield Sprite.
        :param black_holes: Container to hold and manage single BlackHole Sprite.

    """
    ai_settings.black_hole_rotation_timer += dt
    if ai_settings.black_hole_rotation_timer > 300:
        for black_hole in black_holes.sprites():
            if black_hole.rt_image_number < 11:
                black_hole.rt_image_number += 1
            else:
                black_hole.rt_image_number = 0
            black_hole.update()
            black_holes.add(black_hole)
            ai_settings.black_hole_rotation_timer = 0
    if pygame.sprite.spritecollideany(ship, black_holes):
        ship_hit_at_boss_stage(ai_settings, screen, stats, hud, ship, bullets,
                               used_shields, bosses, boss_bullets, boss_shields, black_holes)
