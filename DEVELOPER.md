# Entwicklung von BitWave

BitWave ist eine eigenständige Windows-App. Das Python-Paket heißt `bitwave`, die Oberfläche liegt in `bitwave.bitwave_ui`. Oberfläche, Anwendungsdaten, Signierung und Veröffentlichungen gehören zu BitWave.

## Aufbau

- `bitwave/bitwave_ui/app.py`: Start der Qt-Anwendung, deutsche Standardsprache und Fenster.
- `bitwave/bitwave_ui/backend.py`: Verbindung zwischen QML-Oberfläche, TIDAL und Downloads.
- `bitwave/bitwave_ui/bridge_library.py`: Musiksammlung und Abgleich vorhandener Dateien.
- `bitwave/bitwave_ui/qml/Main.qml`: Hauptfenster, Suche, Warteschlange und Wiedergabe.
- `bitwave/bitwave_ui/qml/SettingsPage.qml`: Einstellungen aus dem Backend-Schema.
- `bitwave/bitwave_ui/qml/Deutsch.js`: deutsche Übersetzungen; `deutsch.tsv` enthält den lesbaren Katalog.
- `bitwave/bitwave_ui/updater.py` und `signing.py`: Updates aus dem BitWave-Repository und Signaturprüfung.

## Lokale Arbeit

Python 3.12 oder 3.13 und Poetry verwenden. Abhängigkeiten mit `poetry install --all-extras --with dev` installieren. Die Oberfläche startet mit `poetry run python -m bitwave.bitwave_ui`. Tests laufen mit `poetry run pytest`; `poetry check --lock` prüft die Paketdefinition.

Die Oberfläche übersetzt Beschriftungen und Meldungen beim Anzeigen. TIDAL-Titel, Künstlernamen, Albumtitel, Dateipfade und technische Kennungen dürfen dabei nicht verändert werden. Neue Oberflächentexte im deutschen Katalog ergänzen und die QML-Ladetests ausführen.

## Windows-Pakete und Updates

`make build-windows` erstellt das Windows-Paket. Der Veröffentlichungsablauf baut ausschließlich Windows x64 und Windows ARM64. Hilfsaufgaben dürfen auf anderen GitHub-Runnern laufen; daraus entstehen keine weiteren App-Versionen. Details stehen in `BITWAVE_RELEASE.md`.

Der private Signierschlüssel gehört ausschließlich in das Actions-Geheimnis `BITWAVE_SIGNING_KEY`. Er darf niemals im Quellcode, Paket oder Protokoll auftauchen. Der öffentliche Prüfschlüssel liegt in `signing.py` und in der deutschen Anleitung.
