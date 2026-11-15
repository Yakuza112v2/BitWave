# BitWave

<img src="bitwave/ui/icon512.png" alt="BitWave-Logo" width="160">

BitWave ist eine Windows-App zum Offline-Speichern von Musik aus deinem eigenen TIDAL-Konto. Betreuung: [Yakuza112v2](https://github.com/Yakuza112v2).

## Funktionen

- TIDAL nach Künstlern, Alben und Titeln durchsuchen; Suchergebnisse nach verfügbarer Audioqualität sortieren und auf Hi-Res filtern.
- Playlists und Favoriten aus „Mein TIDAL“ abrufen und herunterladen. Titel lassen sich direkt aus den TIDAL-Favoriten entfernen.
- Vorhandene Musik im Musik- und Download-Ordner erkennen und doppelte Downloads vermeiden.
- Neu hinzugefügte Playlist-Titel erkennen sowie Downloads und Wiedergabe in der App steuern.

Fehlende Künstlerbiografien lassen sich unter „Einstellungen → Darstellung“ optional mit Texten von Wikipedia oder Discogs und verlinkter Quellenangabe ergänzen. Die Funktion ist standardmäßig ausgeschaltet.

## Downloads

BitWave wird ausschließlich für **Windows** veröffentlicht.

| Windows-System | Download |
| --- | --- |
| Intel/AMD, 64 Bit | `bitwave_windows-x64.zip` |

Die offiziellen Downloads findest du unter [Releases](https://github.com/Yakuza112v2/BitWave/releases). Entpacke das gesamte ZIP-Archiv und starte `BitWave.exe` im enthaltenen Ordner. Für die Anmeldung und Musikwiedergabe benötigst du ein kostenpflichtiges TIDAL-Konto. Speichere nur Inhalte, zu deren Nutzung du berechtigt bist.

## Einstellungen

Deine Einstellungen und Anmeldedaten liegen im Datenordner `%APPDATA%\BitWave`.

## Updates

Die optionale Update-Prüfung verwendet ausschließlich **Yakuza112v2/BitWave**. Vor der Installation prüft die App eine mit dem eigenen BitWave-Schlüssel signierte Prüfsummenliste. Nicht signierte, manipulierte oder ältere Updates werden abgelehnt.

**0.2.5 ist eine reguläre Version** und wird sowohl von 0.2.3 als auch von 0.2.3-Beta über die Update-Prüfung erkannt. Deine Einstellungen bleiben im oben genannten Datenordner erhalten.

[0.2.5 für Windows herunterladen](https://github.com/Yakuza112v2/BitWave/releases/download/v0.2.5/bitwave_windows-x64.zip)

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
poetry run python -m bitwave.bitwave_ui
```

## Windows-Paket erstellen

```bash
poetry run make build-windows
```

Die automatischen Windows-Builds laufen über GitHub Actions. Die benötigten Bau- und Veröffentlichungshelfer liegen unter `.github/build`. Der Workflow „Windows-Release“ erstellt und prüft die Pakete und signiert die Prüfsummen mit dem Repository-Geheimnis `BITWAVE_SIGNING_KEY`.
