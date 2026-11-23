# Änderungen

## v0.2.8 (2026-11-23)

**BitWave by Yakuza112**

### Neu

- BitWave erkennt falsche Folge-Einträge bei namensgleichen TIDAL-Künstlern anhand der Mediathek. Eindeutige Zuordnungen werden automatisch gewechselt und lassen sich mit „RÜCKGÄNGIG“ widerrufen. Bei unsicheren Zuordnungen entscheidest du mit „WECHSELN“ oder „BEIBEHALTEN“. Die Künstlerseite nennt die zugrunde liegenden Alben; „Folge ich“ kennzeichnet Wechsel und Vorschläge. TIDAL-Favoriten bleiben unverändert.
- „In Mediathek“ berücksichtigt die erkannte Künstlerzuordnung. Auf einem namensgleichen fremden Profil führt ein Hinweis direkt zum Künstler aus der Mediathek.
- Erkannte fremde Veröffentlichungen auf einem gemeinsam genutzten TIDAL-Profil stehen eingeklappt unter „Andere Künstler namens …“. Sie werden aus Veröffentlichungen, Benachrichtigungen und automatischen Downloads ausgeschlossen.

### Behoben

- Titel mit der Explicit-Kennzeichnung werden wieder als vorhanden in der Mediathek erkannt.
- Ein nicht entfernbarer alter Update-Ordner stoppt die Installation, bevor die neue Version in einem falschen Unterordner landet.
- Fehlgeschlagene Veröffentlichungsprüfungen hinterlassen keinen teilweise gespeicherten Stand. Ausstehende automatische Downloads bleiben beim Beenden erhalten.
- Vorübergehend unlesbare Einstellungsdateien werden nicht durch Standardwerte überschrieben.
- Videos mit fehlgeschlagenem letztem Abschnitt werden nicht als vollständig heruntergeladen markiert. Vorübergehende Serverfehler werden erneut versucht.
- Gleichzeitig geladene gleichnamige Editionen reservieren ihre Dateinamen gemeinsam und überschreiben sich nicht gegenseitig.
- „Symlink im Titelordner erstellen“ berücksichtigt führende Nullen bei Titelnummern und erkennt vorhandene Dateien auch mit der älteren Schreibweise.
- Lange Playlist-Dateinamen behalten die Endung .m3u8. Kopierte Playlist-Titel werden über eine temporäre Datei gespeichert, damit bei vollem Speicher keine unvollständige Zieldatei entsteht.

Das türkisfarbene BitWave-Logo und die deutsche Oberfläche bleiben erhalten.

## v0.2.7 (2026-11-18)

**BitWave by Yakuza112**

- Nach dem Neuladen einer Playlist bleiben abgeschlossene Titel erneut herunterladbar – auch wenn die Datei inzwischen verschoben oder gelöscht wurde oder die Dateierkennung noch aktualisiert wird.
- Ein Klick auf „Heruntergeladen“ öffnet die Bestätigung „Erneut herunterladen“. Der bestätigte Download wird tatsächlich neu geladen und nicht als bereits vorhanden übersprungen.
- Ein Hinweis beim Darüberfahren macht den erneuten Download erkennbar. Laufende und wartende Downloads bleiben gegen doppelte Starts geschützt.


## v0.2.6 (2026-11-18)

**BitWave by Yakuza112**

- TIDAL-Kontonummern werden auch bei fehlgeschlagenen Anmeldungen in Diagnoseprotokollen und beim Diagnose-Export unkenntlich gemacht.
- Das Anmeldefenster erklärt falsche Links, abgelehnte Anmeldecodes, Verbindungsfehler und Probleme beim Speichern direkt im Fenster.
- Der Hinweis zur TIDAL-Seite „Seite nicht gefunden“ erklärt, welche Adresse kopiert werden muss und warum „Home“ nicht angeklickt werden soll.
- Während einer Anmeldung wird ein zweites Absenden verhindert. Fremde Links und TIDAL-Seiten ohne passenden Anmeldecode werden vor der Verarbeitung zurückgewiesen.

Das türkisfarbene BitWave-Symbol und vorhandene Einstellungen bleiben erhalten.

## v0.2.5 (2026-11-15)

**BitWave by Yakuza112**

- **Künstlerbiografien ergänzen:** Unter „Einstellungen → Darstellung“ lassen sich fehlende TIDAL-Biografien durch Texte von Wikipedia oder Discogs mit verlinkter Quellenangabe ergänzen. Die Funktion ist standardmäßig ausgeschaltet.
- Die Warteschlangen-Schaltfläche zeigt die Download-Geschwindigkeit ohne Restzeit an.
- Neue Veröffentlichungen gefolgter Künstler werden nach dem Start oder „JETZT PRÜFEN“ in der Regel innerhalb etwa einer Minute gefunden. Erreichbarkeit und Antwortzeiten von TIDAL können dies beeinflussen.
- Nach dem Entfolgen eines Künstlers verschwinden dessen Veröffentlichungen sofort aus der Neuerscheinungsübersicht.
- Die Geschwindigkeitskurve nutzt bei kurzen Alben die ganze Schaltfläche und bewahrt schnelle und langsame Abschnitte des Downloads.
- Während der letzten Download-Schritte erscheint „ABSCHLUSS“ auch ohne Mauszeiger über der Schaltfläche.

Hi-Res-Filter, die Sortierung nach verfügbarer Qualität und das Entfernen von TIDAL-Favoriten aus der bisherigen Beta sind ebenfalls enthalten. Das türkisfarbene BitWave-Symbol bleibt erhalten.

Diese reguläre Version wird über die Update-Prüfung angeboten. Alternativ das vollständige Windows-ZIP entpacken und `BitWave.exe` starten. Vorhandene Einstellungen bleiben erhalten.

## v0.2.3-Beta (2026-11-14)

**BitWave by Yakuza112 – Beta**

- **Nur Hi-Res:** Die Suche kann geladene Alben und Titel auf verfügbare Hi-Res-Ausgaben beschränken.
- **Verfügbare Qualität:** Eine neue Sortierung ordnet die Suchergebnisse nach ihrer angebotenen Audioqualität – unabhängig von der eingestellten Download-Qualität.
- **TIDAL-Favoriten verwalten:** Unter „Mein TIDAL → Titel“ entfernt ein Klick auf das Herz einen Favoriten nach Bestätigung direkt aus deinem TIDAL-Konto. Heruntergeladene Dateien bleiben erhalten.

Diese Vorabversion wurde separat angeboten. Die Funktionen sind seit 0.2.5 regulär enthalten.

## v0.2.3 (2026-11-10)

**BitWave by Yakuza112**

- Ein separater Download-Ordner zählt zusammen mit dem Musikordner zur Musiksammlung. Fertige Downloads werden sofort als vorhanden angezeigt; Sammeldownloads überspringen bereits vorhandene Musik aus beiden Ordnern.
- Die Playlist-Seite lädt auch bei mindestens 50 Playlists in einem Ordner vollständig. Weitere Playlists und Unterordner werden über alle Seiten hinweg geladen.
- Das Geschwindigkeitsdiagramm der Warteschlange bewahrt den Verlauf bereits abgeschlossener Abschnitte und zeigt schnelle und langsame Downloadphasen korrekt an.
- Die Auswahl expliziter oder bereinigter Fassungen erkennt passende Ausgaben auch bei fehlenden Apostrophen oder mit Sternchen zensierten Wörtern. Mehrdeutige Titel und unterschiedlich lange Aufnahmen werden weiterhin getrennt behandelt.

Lade das Windows-ZIP herunter, entpacke es vollständig und starte `BitWave.exe`.

## v0.2.2 (2026-11-04)

**BitWave by Yakuza112**

- Cover haben weichere Übergänge zwischen Rundungen und geraden Kanten und behalten ihre quadratische Form.
- Vorschau- und Download-Schaltflächen auf Covern fahren nach abgeschlossenen Downloads wieder ein. In der Musiksammlung gespeicherte Downloads zeigen sofort „IN MUSIKSAMMLUNG“.
- Ohne Cover zeigt die Wellenform der Wiedergabeleiste den abgespielten Teil türkis und den verbleibenden Teil grau.
- Bereits vorhandene Titel stehen in den Top-Titeln eines Künstlers wieder bündig mit den übrigen Zeilen.
- Die Restzeitanzeige bietet auch bei Titeln über zehn Minuten ausreichend Platz.
- Neu eingetroffene Veröffentlichungen erscheinen sofort mit abgerundeten Cover-Ecken und türkisfarbenem Rahmen.

Lade das Windows-ZIP herunter, entpacke es vollständig und starte `BitWave.exe`.

## v0.2.1 (2026-11-04)

**BitWave by Yakuza112**

- Türkise Texte, Umrandungen, Schalter und aktive Zustände passend zur Logo-Welle.
- Neu zu einer Playlist hinzugefügte Titel erhalten beim nächsten Öffnen eine Neu-Markierung, unabhängig von ihrem Erscheinungsdatum.
- Die Markierung bleibt während dieses Besuchs sichtbar und verschwindet beim darauffolgenden Öffnen. Später hinzugefügte Titel werden erneut markiert.
- Beim ersten Öffnen einer Playlist wird ihr Ausgangsstand gespeichert. Dieser Vergleich bleibt auch nach einem App-Neustart erhalten.
- Neues BitWave-Logo im Fenster, in der App und an der Programmdatei.
- Fenstertitel: „BitWave by Yakuza112“.
- „Durchsuchen“ bei der Auswahl des Download-Ordners, der Musiksammlung und von FFmpeg.
- Die Anmeldung erklärt, dass die TIDAL-Seite „Seite nicht gefunden“ anzeigen kann und welche Adresse du zurück in die App kopieren musst.

### Starten

Lade `bitwave_windows-x64.zip` herunter, entpacke den gesamten Inhalt und starte `BitWave.exe`. Diese Ausgabe unterstützt Windows-PCs mit 64-Bit-Prozessoren von Intel oder AMD. Für die TIDAL-Funktionen benötigst du ein kostenpflichtiges TIDAL-Konto.
