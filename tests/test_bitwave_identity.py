"""Application data and signed update configuration."""
from bitwave import __config_dirname__, name_app, name_package
from bitwave.bitwave_ui import signing, updater


def test_application_profile():
    assert __config_dirname__ in {"BitWave", "BitWave-dev"}
    assert name_package() == "bitwave"
    assert name_app() in {"BitWave", "BitWave-dev"}


def test_signed_update_configuration():
    assert updater.REPO == "Yakuza112v2/BitWave"
    assert signing.UPDATE_PUBLIC_KEY == "jQFMgwjIhp1dbcCAy31oUy4jX3E80+28Fb+MpQ+nZJA="
