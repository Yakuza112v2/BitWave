"""The separately distributed beta waits for 0.2.4, retaining its display label."""
from bitwave.bitwave_ui.updater import AppUpdater, Release, _is_older


def test_beta_skips_existing_same_number_stable_and_offers_next_version(tmp_path):
    up = AppUpdater(tmp_path, "0.2.3-Beta", repo="Yakuza112v2/BitWave", update_floor="0.2.3")
    up.latest = lambda *a, **k: Release(version="v0.2.3", asset="a", url="u")
    assert up.update_available() == (False, "0.2.3-Beta", "0.2.3")
    up.latest = lambda *a, **k: Release(version="v0.2.4", asset="a", url="u")
    assert up.update_available() == (True, "0.2.3-Beta", "0.2.4")
    assert _is_older("0.2.2", "0.2.3-Beta")


def test_regular_version_comparison_is_unchanged(tmp_path):
    up = AppUpdater(tmp_path, "0.2.3", repo="Yakuza112v2/BitWave")
    up.latest = lambda *a, **k: Release(version="v0.2.4", asset="a", url="u")
    assert up.update_available() == (True, "0.2.3", "0.2.4")
