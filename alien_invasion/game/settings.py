class Settings:

    def __init__(self, health: int | None) -> None:
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.bullets_allowed = 1
        self.ships_limit = health or 3
        self.ship_speed = 0.60
        self.bullet_speed_factor = 1.5
        self.shields_allowed = 1
        self.time_elapsed_since_shield = 0

        # Aliens settings.
        self.time_elapsed_since_last_alien_bullet = 0
        self.aliens_speed = 0.1
        self.alien_bullets_speed = 0.20

        # Bosses settings.
        self.red_boss_speed = 0.1
        self.green_boss_bullets_speed = 0.15
        self.red_boss_bullets_speed = 0.10
        self.blue_boss_bullets_speed = 0.3
        self.time_elapsed_since_last_boss_bullet = 0
        self.time_elapsed_since_boss_shield = 0
        self.time_elapsed_since_last_red_boss_bullet = 0
        self.time_elapsed_since_last_blue_boss_bullet = 0
        self.green_boss_bullet_timer = 300

        # Game settings
        self.framerate = 5000
        self.game_sleep_time = 0.3

        # Settings initialization.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Initialize settings, that change during the game."""
        self.black_hole_spawn_timer = 0
        self.black_hole_rotation_timer = 0
        self.black_hole_despawn_timer = 0
