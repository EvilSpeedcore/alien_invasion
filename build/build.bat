uv sync --group build
uv run nuitka --clean-cache=all
uv run nuitka --onefile --msvc=latest --include-data-dir=./alien_invasion/assets=assets ./alien_invasion/run.py
