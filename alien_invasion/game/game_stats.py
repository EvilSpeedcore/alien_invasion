from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.settings import Settings


class GameStats:

    def __init__(self, settings: "Settings") -> None:
        self.settings = settings
        self.reset_stats()

    def reset_stats(self) -> None:
        """Reset statistics, which change during the game."""
        self.ships_left = self.settings.ships_limit
        self.shields_left = self.settings.shields_allowed
        self.ammo = self.settings.bullets_allowed
