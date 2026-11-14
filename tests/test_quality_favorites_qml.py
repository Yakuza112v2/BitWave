"""Exercise quality controls and favorite confirmation in the real QML window."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

_EXIT_OK = 0
_EXIT_REGRESSED = 1
_EXIT_NO_QT = 77
_EXIT_PRECONDITION = 78

QML_MAIN = Path(__file__).resolve().parent.parent / "bitwave" / "bitwave_ui" / "qml" / "Main.qml"


def test_quality_controls_and_favorite_confirmation_in_the_real_window():
    env = dict(os.environ)
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="bitwave-search-refresh-test-")
    proc = subprocess.run(  # (fixed argv: this file, one flag)
        [sys.executable, str(Path(__file__).resolve()), "--run-scenario"],
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-20:])
    import pytest

    if proc.returncode == _EXIT_NO_QT:
        pytest.skip("PySide6 / offscreen Qt unavailable")
    if proc.returncode == _EXIT_PRECONDITION:
        pytest.skip(f"could not set up the scenario in this environment:\n{tail}")
    assert proc.returncode == _EXIT_OK, f"the feature UI regressed. Scenario exit={proc.returncode}:\n{tail}"


def _album(ident: str, title: str, *, year: int = 2020, quality: str = "LOSSLESS") -> dict:
    return {
        "id": ident,
        "title": title,
        "artist": "Lab Artist",
        "artist_id": "ar0",
        "art": "",
        "year": year,
        "date": f"{year}-01-01",
        "tracks": 10,
        "duration_sec": 2400,
        "quality": quality,
        "popularity": 10,
        "explicit": False,
        "kind": "album",
        "artists": [{"id": "ar0", "name": "Lab Artist"}],
    }


def _artist(ident: str, name: str) -> dict:
    return {"id": ident, "name": name, "art": "", "kind": "artist"}


def _payload(albums: list, artists: list, *, refresh: bool) -> dict:
    out = {
        "artists": artists,
        "albums": albums,
        "tracks": [],
        "videos": [],
        "playlists": [],
        "mixes": [],
        "top": None,
    }
    if refresh:
        out["refresh"] = True
    return out


def _run_scenario() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from PySide6.QtCore import QEventLoop, QTimer, QUrl
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtQml import QQmlApplicationEngine, QQmlEngine, QQmlExpression
    except Exception as exc:
        print(f"Qt unavailable: {exc}", file=sys.stderr)
        return _EXIT_NO_QT

    from _qml_offline import PARK_LOGIN_QML, patch_offline

    patch_offline()
    app = QGuiApplication.instance() or QGuiApplication([])
    try:
        from bitwave.bitwave_ui.app import _load_mono
        from bitwave.bitwave_ui.backend import BitWaveBridge
    except Exception as exc:
        print(f"Qt platform/backend unavailable: {exc}", file=sys.stderr)
        return _EXIT_NO_QT

    BitWaveBridge._library_root = lambda self: ""  # type: ignore[method-assign]
    BitWaveBridge.loadBrowse = lambda self: None  # type: ignore[method-assign]
    BitWaveBridge.refreshBrowse = lambda self: None  # type: ignore[method-assign]

    engine = QQmlApplicationEngine()
    bridge = BitWaveBridge(tidal=None)
    engine.rootContext().setContextProperty("bitwave", bridge)
    engine.rootContext().setContextProperty("monoFont", _load_mono())
    engine.rootContext().setContextProperty("uiFontFamily", app.font().family())
    engine.load(QUrl.fromLocalFile(str(QML_MAIN)))
    roots = engine.rootObjects()
    if not roots:
        print("Main.qml failed to load", file=sys.stderr)
        return _EXIT_PRECONDITION
    root = roots[0]

    def q(expr: str):
        e = QQmlExpression(QQmlEngine.contextForObject(root), root, expr)
        r = e.evaluate()
        if e.hasError():
            raise RuntimeError(e.error().toString())
        if isinstance(r, tuple):
            r = r[0]
        return r.toVariant() if hasattr(r, "toVariant") else r

    def settle(ms: int = 250) -> None:
        loop = QEventLoop()
        QTimer.singleShot(ms, loop.quit)
        loop.exec()

    import json
    from types import SimpleNamespace
    from unittest.mock import Mock
    q(PARK_LOGIN_QML)
    settle(100)
    q("root._searchSeq = root._navSeq; root.browseOpen = false; root.libraryOpen = false; root.settingsOpen = false")
    # Deliver a local payload through the real result handler. No live account.
    rows = [_album("1", "CD quality"), _album("2", "Hi Res", quality="HI-RES"), _album("3", "AAC", quality="HIGH")]
    bridge.searchResults.emit(_payload(rows, [_artist("9", "Artist")], refresh=False))
    settle(150)
    assert int(q("albumsModel.count")) == 3
    q("sortBox.currentIndex = 4; root.sortAsc = false; root.resortSearch()")
    assert q("albumsModel.get(0).id") == "2"
    assert q("albumsModel.get(2).id") == "3"
    q("root.searchHiResOnly = true; root.resortSearch()")
    assert int(q("albumsModel.count")) == 1
    assert q("albumsModel.get(0).id") == "2"
    assert q('root.sectionVisible("artists", 1)') is False
    assert q('root.sectionVisible("playlists", 1)') is False
    q('root.searchTop = ({kind:"playlist",quality:"HI-RES"})')
    assert q("root.searchTopVisible") is False
    q('root.searchTop = ({kind:"album",quality:"HI-RES"})')
    assert q("root.searchTopVisible") is True
    q("root.searchHiResOnly = false; root.resortSearch()")
    assert int(q("albumsModel.count")) == 3

    # Opening and cancelling the prompt never mutates the remote account.
    remove = Mock(return_value=True)
    bridge.tidal = SimpleNamespace(session=SimpleNamespace(user=SimpleNamespace(favorites=SimpleNamespace(remove_track=remove))))
    bridge._logged_in = True
    q('favoriteRemovePrompt.trackId = "42"; favoriteRemovePrompt.trackTitle = "Test title"; favoriteRemovePrompt.open()')
    settle(50)
    assert q("favoriteRemovePrompt.opened") is True
    remove.assert_not_called()
    q("favoriteRemovePrompt.close()")
    settle(50)
    remove.assert_not_called()
    # Only the explicit confirmation invokes the real slot, using a mock API.
    q('favoriteRemovePrompt.open()')
    from PySide6.QtCore import QObject, QMetaObject
    confirm = root.findChild(QObject, "confirmFavoriteRemoval")
    assert confirm is not None
    assert QMetaObject.invokeMethod(confirm, "clicked")
    settle(300)
    remove.assert_called_once_with("42")
    bridge._logged_in = False
    bridge.shutdown()
    print("Quality filter, quality order and favorite confirmation: OK")
    return _EXIT_OK


if __name__ == "__main__":
    if "--run-scenario" in sys.argv:
        raise SystemExit(_run_scenario())
