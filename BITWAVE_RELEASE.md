# BitWave veröffentlichen

BitWave wird unter `Yakuza112v2/BitWave` für Windows veröffentlicht. Der öffentliche Download enthält die App für Intel/AMD mit 64 Bit.

## Version vorbereiten

Die App-Version in `bitwave/bitwave_ui/__init__.py` muss zum Release-Tag passen. `pyproject.toml` verwendet die entsprechende Paketversion nach PEP 440 (`0.2.3b0` für `0.2.3-Beta`). Die Änderungen stehen in einem eigenen Abschnitt der `CHANGELOG.md`.

`0.2.3-Beta` ist eine separate Vorabversion. Die nächste reguläre Version ist `0.2.4`. Die Windows-Dateiversion verwendet ausschließlich den numerischen Teil; die App zeigt den vollständigen Versionsnamen.

## Veröffentlichung

Unter GitHub Actions den Ablauf **Windows-Release** starten. Als `release_tag` zum Beispiel `v0.2.3-Beta` und als `only` den Wert `windows-x64` eintragen. Der Ablauf baut die App, prüft das Windows-Paket und veröffentlicht Downloads erst nach erfolgreicher Signierung.

Beta-Ausgaben werden als Vorabversion markiert und ersetzen den regulären Standarddownload nicht. Eine Beta mit derselben Nummer wie eine bereits vorhandene reguläre Version wartet bei der Update-Prüfung auf die nächste höhere Versionsnummer.

## Signaturen

Der private Schlüssel liegt ausschließlich im Actions-Geheimnis `BITWAVE_SIGNING_KEY`. Der öffentliche Prüfschlüssel steht in `bitwave/bitwave_ui/signing.py`. Das Repository muss öffentlich sein, damit die App Releases ohne GitHub-Anmeldung abrufen kann.

Jedes Release enthält das Windows-ZIP, die Prüfsummenliste `SHA256SUMS` und ihre Signatur `SHA256SUMS.sig`. Ohne gültige Signatur wird kein App-Update installiert. Die Prüfung eines Downloads ist in der [README](README.md) beschrieben.
