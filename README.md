## Prerequisites

1) Install uv: https://docs.astral.sh/uv/getting-started/installation/
2) Install dependencies: `uv sync --all-groups`

## Building
Windows:

1. Install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run:
```
uv sync --group build
uv run nuitka --clean-cache=all
uv run nuitka --onefile --msvc=latest --include-data-dir=./assets=assets run.py
```

## TODO
* Get TODOs from https://drive.google.com/open?id=10TSk52nwgsJAL2iT5ZD8vwbSAtyx0agB
* R key: reload level (debug only)
* Tests with input recording (events)
* Saves
* Change blue alien to shoot first bullets with delay
* .ini configuration for executable
