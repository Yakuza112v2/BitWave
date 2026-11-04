# BitWave

BitWave ist eine Windows-App zum Offline-Speichern von Musik aus deinem eigenen TIDAL-Konto. Betreuung: [Yakuza112v2](https://github.com/Yakuza112v2).

## Downloads

BitWave wird ausschließlich für **Windows** veröffentlicht.

| Windows-System | Download |
| --- | --- |
| Intel/AMD, 64 Bit | `bitwave_windows-x64.zip` |
| ARM, 64 Bit | `bitwave_windows-arm64.zip` |

Die offiziellen Downloads findest du unter [Releases](https://github.com/Yakuza112v2/BitWave/releases). Entpacke das gesamte ZIP-Archiv und starte `BitWave.exe` im enthaltenen Ordner. Für die Anmeldung und Musikwiedergabe benötigst du ein kostenpflichtiges TIDAL-Konto. Speichere nur Inhalte, zu deren Nutzung du berechtigt bist.

## Eigene Einstellungen

BitWave startet eigenständig. Einstellungen, Anmeldung, Zwischenspeicher und Update-Daten werden nicht aus Waves übernommen. Der normale Datenordner ist `%APPDATA%\BitWave`. Ein nicht installiert ausgeführter Entwicklungsstand verwendet `BitWave-dev`. `XDG_CONFIG_HOME` kann den Basisordner für Tests überschreiben.

## Updates

Die optionale Update-Prüfung verwendet ausschließlich **Yakuza112v2/BitWave**. Vor der Installation prüft die App eine mit dem eigenen BitWave-Schlüssel signierte Prüfsummenliste. Nicht signierte, manipulierte oder ältere Updates werden abgelehnt.

Während der Umstellung bleibt das Repository privat. Öffentliche App-Updates sind verfügbar, sobald das Repository öffentlich ist und ein signiertes BitWave-Release veröffentlicht wurde. Bestehende Waves-Installationen bleiben eigenständig; BitWave wird separat installiert.

## Download prüfen

Lade zusammen mit dem ZIP-Archiv die Dateien `SHA256SUMS` und `SHA256SUMS.sig` herunter. Vergleiche unter PowerShell die Prüfsumme deines Downloads mit der entsprechenden Zeile in der Liste:

```powershell
(Get-FileHash .\bitwave_windows-x64.zip -Algorithm SHA256).Hash.ToLower()
Select-String -Path SHA256SUMS -Pattern bitwave_windows-x64.zip
```

Die beiden Prüfsummen müssen identisch sein. Die Signatur lässt sich zusätzlich mit Git Bash und OpenSSL 3 überprüfen. Dieser öffentliche Schlüssel ist auch fest in der App hinterlegt:

```
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAjQFMgwjIhp1dbcCAy31oUy4jX3E80+28Fb+MpQ+nZJA=
-----END PUBLIC KEY-----
```

```bash
printf '%s\n' '-----BEGIN PUBLIC KEY-----' 'MCowBQYDK2VwAyEAjQFMgwjIhp1dbcCAy31oUy4jX3E80+28Fb+MpQ+nZJA=' '-----END PUBLIC KEY-----' > bitwave-release.pem
base64 --decode < SHA256SUMS.sig > SHA256SUMS.sig.bin
openssl pkeyutl -verify -pubin -inkey bitwave-release.pem -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig.bin
grep -v '^#' SHA256SUMS | tr -d '\r' | shasum -a 256 --ignore-missing -c -
```

Die Signaturprüfung muss `Signature Verified Successfully` ausgeben. Die Prüfsummenprüfung muss für das heruntergeladene Archiv `OK` melden. Bei einer Abweichung darf die Datei nicht verwendet werden.

## Aus dem Quellcode starten

Benötigt werden Windows und Python 3.12 oder 3.13.

```powershell
poetry install --all-extras --with dev
poetry run python -m waves.waves_ui
```

Der interne Python-Paketname bleibt aus Kompatibilitätsgründen `waves`. Anwendung und installierbares Projekt heißen BitWave.

## Windows-Paket erstellen

```bash
poetry run make build-windows
```

Die automatischen Windows-Builds laufen über GitHub Actions. Die Einrichtung der Signierung und die Veröffentlichung sind in [BITWAVE_RELEASE.md](BITWAVE_RELEASE.md) beschrieben.


