"""BitWave's QML interface and application version.

The interface uses the engine's configuration, download and helper modules.
"""

# The app's user-facing version, the one the in-app updater
# (:mod:`bitwave.bitwave_ui.updater`) compares against the latest GitHub release
# tag. tests/test_package_version.py checks the normalized pyproject.toml version.
# Bump both (and tag a matching ``vX.Y.Z`` release) on every shipped build.
__version__ = "0.2.6"
