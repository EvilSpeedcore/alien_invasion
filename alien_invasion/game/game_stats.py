from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.settings import Settings


class GameStats:

    def __init__(self, ai_settings: "Settings") -> None:
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self) -> None:
        """Reset statistics, which change during the game."""
        self.ships_left = self.ai_settings.ships_limit
        self.shields_left = self.ai_settings.shields_allowed
        self.ammo = self.ai_settings.bullets_allowed
