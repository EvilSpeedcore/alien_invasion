class Settings:

    def __init__(self) -> None:
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.bullets_allowed = 1
        self.ships_limit = 3
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 1.5
        self.shields_allowed = 1
        self.time_elapsed_since_shield = 0

        # Aliens settings.
        # TODO: Not used? Use in increase_aliens_speed?
        self.alien_speed_factor_scale = 0.001
        # TODO: Not used? Use in increase_aliens_speed?
        self.alien_bullet_speed_factor_scale = 0.001
        self.time_elapsed_since_last_alien_bullet = 0

        # Bosses settings.
        self.red_boss_speed_factor = 0.004
        self.green_boss_bullet_speed_factor = 0.09
        self.red_boss_bullet_speed_factor = 0.08
        self.blue_boss_bullet_speed_factor = 1
        self.time_elapsed_since_last_boss_bullet = 0
        self.time_elapsed_since_boss_shield = 0
        self.time_elapsed_since_last_red_boss_bullet = 0
        self.green_boss_bullet_timer = 300

        # Game settings
        self.game_sleep_time = 0.3

        # Settings initialization.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Initialize settings, that change during the game."""
        self.black_hole_spawn_timer = 0
        self.black_hole_rotation_timer = 0
        self.black_hole_despawn_timer = 0

        self.alien_speed_factor = 0.1
        self.alien_bullet_speed_factor = 0.07

    def increase_aliens_speed(self) -> None:
        """Increase alien speed with stage progression."""
        self.alien_speed_factor += 0.01
        self.alien_bullet_speed_factor += 0.02
