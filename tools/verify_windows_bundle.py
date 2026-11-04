"""Reject a Windows bundle with stale branding or translated UI files."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]


def verify(bundle: Path) -> None:
    assert (bundle / 'BitWave.exe').is_file(), 'BitWave.exe fehlt'
    for source in (ROOT / 'bitwave/ui').glob('icon*'):
        if source.suffix not in {'.png', '.ico'}:
            continue
        packaged = bundle / 'ui' / source.name
        assert packaged.is_file(), f'{packaged} fehlt'
        assert hashlib.sha256(packaged.read_bytes()).digest() == hashlib.sha256(source.read_bytes()).digest(), f'Veraltetes Symbol: {packaged}'
    for name in ['Main.qml', 'SettingsPage.qml', 'Deutsch.js', 'deutsch.tsv', 'bitwave-logo.png']:
        source = ROOT / 'bitwave/bitwave_ui/qml' / name
        packaged = bundle / 'bitwave_ui/qml' / name
        assert packaged.is_file(), f'{packaged} fehlt'
        assert packaged.read_bytes() == source.read_bytes(), f'Veraltete Oberfläche: {name}'
    main = (bundle / 'bitwave_ui/qml/Main.qml').read_text(encoding='utf-8')
    assert 'title: "BitWave by Yakuza112"' in main
    assert 'source: "bitwave-logo.png"' in main
    settings = (bundle / 'bitwave_ui/qml/SettingsPage.qml').read_text(encoding='utf-8')
    assert 'I18n.t("BROWSE")' not in settings
    print('Fertiges Paket geprüft: neues Logo, Fenstertitel und deutsche Texte stimmen mit dem Release-Quellcode überein.')


if __name__ == '__main__':
    verify(Path(sys.argv[1]))
