# BitWave veröffentlichen

Quellcode, Fehlerberichte, Downloads und Updates gehören zu `Yakuza112v2/BitWave`. Es gibt ausschließlich Windows-Ausgaben für x64 und ARM64.

## Einmalige Einrichtung

1. Das Repository bleibt während der Umstellung und Abnahme privat.
2. Der private BitWave-Signierschlüssel wird als geschütztes Actions-Geheimnis `BITWAVE_SIGNING_KEY` hinterlegt. Der zugehörige öffentliche Schlüssel steht in `waves/waves_ui/signing.py`. Der private Schlüssel gehört niemals in den Quellcode.
3. GitHub Actions muss für das Repository aktiviert sein. Für Veröffentlichungen genügt das Repository-eigene `GITHUB_TOKEN`.
4. Vor öffentlichen App-Updates muss das Repository öffentlich sein. Private Releases sind für die anonyme Update-Prüfung der App nicht erreichbar.

## Version und Testpaket

Die Versionsnummern in `pyproject.toml` und `waves/waves_ui/__init__.py` müssen identisch sein. Ergänze in `CHANGELOG.md` einen Abschnitt `## vX.Y.Z (JJJJ-MM-TT)`.

Für einen Test starte unter Actions den Ablauf `release-or-test-build`. Lass `release_tag` leer. Mit `only=windows-x64` oder `only=windows-arm64` lässt sich eine Variante auswählen; ein leeres Feld erstellt beide. Testläufe veröffentlichen kein Release.

## Signiertes Release

Markiere den geprüften Commit mit `vX.Y.Z` und übertrage den Tag zu GitHub. Alternativ starte den Ablauf manuell mit `release_tag=vX.Y.Z` und leerem `only`. Ein offizielles Release muss beide Windows-Varianten enthalten.

Nach erfolgreichen Builds sammelt der Ablauf die Prüfsummen, signiert `SHA256SUMS` und veröffentlicht anschließend das Release mit `SHA256SUMS.sig`. Ohne passenden Signierschlüssel schlägt die Veröffentlichung fehl.

## Vor der ersten Verteilung

- Programmname und ausführbare Datei müssen BitWave heißen.
- Oberfläche und Meldungen müssen deutsch sein.
- Der erste Start darf keine Einstellungen oder Anmeldung aus Waves übernehmen.
- Beide Windows-Pakete müssen auf der jeweiligen Architektur starten.
- Prüfsummenliste und Signatur müssen am Release angehängt sein.
- Ein signiertes Update zwischen zwei BitWave-Versionen muss geprüft werden.

Der ursprüngliche Waves-Schlüssel, dessen Update-Repository und dessen Paketverwaltungen werden nicht verwendet. Die internen Namen `waves`, `waves.dist` und das Manifestfeld `waves-version` bleiben aus Kompatibilitätsgründen erhalten.
