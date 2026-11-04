"""BitWave must not read BitWave profiles or install upstream releases."""

import tomllib
from pathlib import Path

from bitwave import __config_dirname__, name_app, name_package
from bitwave.bitwave_ui import signing, updater


def test_profile_and_distribution_are_independent():
    assert __config_dirname__ in {"BitWave", "BitWave-dev"}
    assert name_package() == "bitwave"
    assert name_app() in {"BitWave", "BitWave-dev"}


def test_release_identity_and_key_do_not_trust_upstream():
    assert updater.REPO == "Yakuza112v2/BitWave"
    assert signing.UPDATE_PUBLIC_KEY
    assert signing.UPDATE_PUBLIC_KEY != "cetggrhiqyMN5HsBCi/f2gJL75FVPOYGU/sd4dI5b+0="
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["name"] == "bitwave"
    assert project["urls"]["repository"] == "https://github.com/Yakuza112v2/BitWave"


def test_upstream_package_manager_is_never_invoked(monkeypatch):
    monkeypatch.setattr(updater, "_find_brew", lambda: "/opt/homebrew/bin/brew")
    for channel in ("homebrew", "homebrew-cask", "scoop", "winget"):
        assert updater.managed_upgrade_command(channel) is None
        assert updater.channel_hint(channel) == ""
