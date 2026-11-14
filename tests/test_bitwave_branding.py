"""Public application and package identity."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_application_identity():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["name"] == "bitwave"
    assert project["authors"] == [{"name": "Yakuza112v2"}]
    assert project["urls"]["repository"] == "https://github.com/Yakuza112v2/BitWave"
    assert (ROOT / "bitwave/bitwave_ui/__main__.py").is_file()
