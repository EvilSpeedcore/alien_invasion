class GameStats:
    """Class, which monitors game statistics."""
    def __init__(self, ai_settings):
        """Initialize game statistics.

        Args:
            :param ai_settings: Instance of Settings class.

        """
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Reset statistics, which change during the game."""
        self.ships_left = self.ai_settings.ships_limit
        self.shields_left = self.ai_settings.shields_allowed
        self.ammo = self.ai_settings.bullets_allowed
        self.stage = 1
