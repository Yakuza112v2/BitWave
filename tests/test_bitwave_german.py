"""Exercise the actual QML translator, including dynamic messages and media names."""
from pathlib import Path
import json
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication
from PySide6.QtQml import QJSEngine

QML = Path(__file__).resolve().parents[1] / "waves/waves_ui/qml"


def test_german_catalogue_and_dynamic_messages():
    app = QCoreApplication.instance() or QCoreApplication([])
    engine = QJSEngine()
    source = (QML / "Deutsch.js").read_text(encoding="utf-8").replace(".pragma library", "", 1)
    result = engine.evaluate(source)
    assert not result.isError(), result.toString()
    def translate(value):
        return engine.evaluate("t(" + json.dumps(value) + ")").toString()
    assert translate("Settings") == "Einstellungen"
    assert translate("Download folder") == "Download-Ordner"
    assert translate("✗ Could not check") == "✗ Prüfung nicht möglich"
    assert translate("DOWNLOAD ALL") == "ALLES HERUNTERLADEN"
    assert translate("Welcome to BitWave") == "Willkommen bei BitWave"
    assert "finished" not in translate("3 downloads finished")
    assert translate("“Home”") == "“Home”"
    assert translate("https://github.com/Yakuza112v2/BitWave") == "https://github.com/Yakuza112v2/BitWave"
    assert translate("<b>Settings</b>") == "<b>Einstellungen</b>"


def test_windows_release_targets_only():
    import yaml
    root = QML.parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/release-or-test-build.yml").read_text(encoding="utf-8"))
    matrices = [j["strategy"]["matrix"] for j in workflow["jobs"].values() if "strategy" in j]
    assert matrices
    assert "linux" not in json.dumps(matrices).lower()
    assert "macos" not in json.dumps(matrices).lower()
    assert "windows" in json.dumps(matrices).lower()
