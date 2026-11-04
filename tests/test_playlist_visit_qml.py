"""Exercise actual page entry, refresh and return through the QML bindings."""
import os
from pathlib import Path
import subprocess
import sys


def test_playlist_visit_badges_in_real_qml(tmp_path):
    env = dict(os.environ, QT_QPA_PLATFORM='offscreen', XDG_CONFIG_HOME=str(tmp_path))
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--scenario'], env=env, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr


def scenario():
    import json
    root = Path(__file__).resolve().parents[1]
    sys.path[:0] = [str(root), str(root/'tests')]
    from _qml_offline import patch_offline
    patch_offline()
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtCore import QUrl
    from PySide6.QtQml import QQmlApplicationEngine, QQmlEngine, QQmlExpression
    from bitwave.bitwave_ui.backend import BitWaveBridge
    app = QGuiApplication([])
    app.setApplicationName('BitWave-test')
    app.setOrganizationName('BitWave-test')
    bridge = BitWaveBridge(tidal=None)
    bridge._cache_user_id = lambda: 'test-user'
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('bitwave', bridge)
    engine.rootContext().setContextProperty('monoFont', 'monospace')
    engine.rootContext().setContextProperty('uiFontFamily', app.font().family())
    engine.load(QUrl.fromLocalFile(str(root/'bitwave/bitwave_ui/qml/Main.qml')))
    assert engine.rootObjects()
    window = engine.rootObjects()[0]
    def q(text):
        expression = QQmlExpression(QQmlEngine.contextForObject(window), window, text)
        result = expression.evaluate()
        assert not expression.hasError(), expression.error().toString()
        return result[0] if isinstance(result, tuple) else result
    def page(*ids):
        return json.dumps({'key':'item:playlist:p', 'title':'Playlist', 'header':{'id':'p','kind':'playlist','title':'Playlist'}, 'playlist_complete':True, 'error':False, 'sections':[{'rowKind':'tracks','title':'Tracks','items':[{'id':x,'kind':'track','title':x,'num':i+1} for i,x in enumerate(ids)]}]})
    def flags():
        return json.loads(q('JSON.stringify(root.playlistFreshMask)'))
    q('root.settingsOpen=false; root.artistOpen=false; root.libraryOpen=false; root.releasesOpen=false; root.browseOpen=true; root.browsePageKey="item:playlist:p"')
    q('root.browsePage='+page('old'))
    assert flags() == [False]
    q('root.settingsOpen=true')
    q('root.browsePage='+page('old','added'))
    # A payload arriving while another page is visible cannot consume additions.
    q('root.settingsOpen=false')
    assert flags() == [False, True], flags()
    q('root.browsePage='+page('old','added'))
    assert flags() == [False, True], flags()
    q('root.settingsOpen=true; root.settingsOpen=false')
    assert flags() == [False, False], flags()
    q('root.browsePage='+page('old','added','later'))
    assert flags() == [False, False, True], flags()
    print('Playlist NEW: first open, hidden refresh, same-visit refresh and return passed')


if __name__ == '__main__':
    scenario()
