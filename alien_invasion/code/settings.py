class Settings():
    """Class, which store setting of the game."""
    def __init__(self):
        """Initialize game settings"""
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
        self.alien_speed_factor_scale = 0.01
        self.alien_bullet_speed_factor_scale = 0.1
        self.time_elapsed_since_last_alien_bullet = 0

        # Bosses settings.
        self.red_boss_speed_factor = 0.4
        self.green_boss_bullet_speed_factor = 0.9
        self.red_boss_bullet_speed_factor = 0.8
        self.blue_boss_bullet_speed_factor = 1
        self.time_elapsed_since_last_boss_bullet = 0
        self.time_elapsed_since_boss_shield = 0
        self.time_elapsed_since_last_red_boss_bullet = 0
        self.green_boss_bullet_timer = 300

        # Environment settings.
        self.black_hole_spawn_timer = 0
        self.black_hole_rotation_timer = 0
        self.black_hole_despawn_timer = 0

        # Game settings
        self.running = 1
        self.paused = 0
        self.state = None
        self.boss_stages = (4, 8, 12)
        self.game_sleep_time = 0.3
        self.non_boss_stages = (non_boss_stage for non_boss_stage in range(1, self.boss_stages[2] + 1) if
                                non_boss_stage not in self.boss_stages)
        self.non_boss_stages = tuple(self.non_boss_stages)

        # Settings initialization.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings, that change during the game."""
        self.alien_speed_factor = 0.1
        self.alien_bullet_speed_factor = 0.7

    def increase_aliens_speed(self):
        """Increase alien speed with stage progression."""
        self.alien_speed_factor += 0.01
        self.alien_bullet_speed_factor += 0.02
