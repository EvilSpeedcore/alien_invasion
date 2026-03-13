from argparse import Namespace

import pytest


@pytest.fixture
def namespace() -> Namespace:
    return Namespace(
        record_events=False,
        health=None,
        stage=None,
        play_events=None,
    )
