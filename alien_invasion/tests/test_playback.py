from typing import TYPE_CHECKING

import pytest

from game.paths import Paths
from run import run_game

if TYPE_CHECKING:
    from argparse import Namespace


def test_press_play_button_enter_and_quit(namespace: Namespace) -> None:
    events = Paths.playbacks() / "press_play_button_enter_and_quit.json"
    namespace.playback_events = events
    with pytest.raises(SystemExit):
        run_game(namespace)
