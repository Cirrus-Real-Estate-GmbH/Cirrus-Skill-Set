---
name: facade-color-configurator
description: Baut eine interaktive, in sich geschlossene HTML-Seite (ein einzelnes Vorher/Nachher-"Baukasten"-Tool) zum Vergleichen von Fassaden- oder Farbvarianten eines oder mehrerer Gebäude. Immer verwenden, wenn der Nutzer Fassadenvisualisierungen, Farbkonzepte, Vorher-Nachher-Vergleiche für Gebäude, Renderings von Fassadenvarianten oder eine Webseite/ein Tool zum Durchklicken von Design-/Farbvarianten möchte – auch bei Formulierungen wie "Fassade visualisieren", "Farbvarianten vergleichen", "IST/SOLL-Vergleich", "Baukasten für Farben", oder wenn mehrere Renderings/Fotos eines Gebäudes in unterschiedlichen Farben vorliegen und daraus etwas Anschauliches entstehen soll. Erzeugt eine einzelne, portable HTML-Datei mit eingebetteten Bildern (kein Hosting nötig), mit Regler für Vorher/Nachher, frei wählbarem Links/Rechts-Vergleich zwischen beliebigen Varianten (nicht nur IST vs. SOLL) und einer anklickbaren Farbmuster-Liste pro Gebäude.
---

# Facade Color Configurator

## Worum es geht

Ein Bauherr oder Eigentümer hat ein Gebäude (oder mehrere), ein Ist-Foto der
Fassade und mehrere Farb-/Gestaltungsvarianten (eigene Fotos einer Renovierung,
KI-generierte Renderings, oder ein Raster mit mehreren Varianten in einem
Bild). Statt die Bilder einzeln als PDF oder Word-Datei zu verschicken, baut
dieser Skill eine interaktive Webseite: ein Vorher/Nachher-Regler in der
Mitte, daneben eine Liste aller Varianten als Farbmuster-Kacheln. Jede Kachel
hat zwei Knöpfe, "Links" und "Rechts" — damit lässt sich jede beliebige
Variante gegen jede andere stellen (nicht nur Ist- gegen Soll-Zustand). Bei
mehreren Gebäuden/Fassadenseiten gibt es oben Tabs zum Umschalten.

Das Ergebnis ist eine einzelne HTML-Datei mit allen Bildern als Base64
eingebettet — sie lässt sich per Mail verschicken oder lokal öffnen, ohne
dass Bilder als separate Dateien mitgeschickt werden müssen oder ein Server
nötig ist.

## Wann dieser Skill greift

Auch ohne dass der Nutzer explizit "Skill" oder "Baukasten" sagt — z.B. bei:
- "Kannst du daraus eine Webseite bauen, auf der man die Fassade besser sehen kann?"
- "Ich habe Fotos in verschiedenen Farben, mach daraus was Interaktives"
- "Vergleich der Farbvarianten für [Adresse]"
- Der Nutzer lädt ein IST-Foto und mehrere SOLL-Renderings/Farbvarianten hoch und möchte diese "gegenüberstellen" oder "vergleichen können"

## Workflow

### 1. Bilder sammeln und zuordnen

Für jedes Gebäude/jede Fassadenseite: ein IST-Foto plus N Farbvarianten.
Manchmal liegen die Varianten als ein einzelnes Rasterbild vor (z.B. von
Gemini/Midjourney generiert, mehrere Häuser-Renderings mit Bildunterschrift
in einem PNG). In dem Fall zuerst zuschneiden:

```bash
python scripts/crop_grid.py grid.png outdir/ --prefix v
```

Das Script erkennt Zeilen/Spalten automatisch anhand weißer Zwischenräume und
schneidet jede Zelle einzeln aus (Bildunterschriften werden dabei mit
erkannt/ausgeschlossen, je nach Layout — die erkannten Segmente werden
ausgegeben, damit man kontrollieren kann, ob sie sinnvoll aussehen). Bei
unregelmäßigen Rastern `--rows`/`--cols` explizit angeben. Ergebnis-Dateien
danach **immer visuell prüfen** (z.B. mit dem Read-Tool ansehen) und sinnvoll
umbenennen, bevor sie weiterverwendet werden — die Zuordnung "welches Bild
gehört zu welcher Fassadenseite" muss inhaltlich stimmen (z.B. anhand von
Straßenpflaster, Vegetation, Fensteranordnung im Foto erkennbar), das lässt
sich nicht automatisieren.

Falls die Bilder nur inline im Chat eingefügt wurden (nicht als Datei
hochgeladen oder über einen verbundenen Ordner erreichbar), gibt es keinen
Dateizugriff darauf — dann den Nutzer bitten, die Bilder entweder als
Dateianhang hochzuladen, oder einen Ordner mit den Bildern zu verbinden
(`request_cowork_directory`).

### 2. Config-Datei schreiben

Ein JSON nach dem Muster in `references/config_example.json` anlegen: pro
Gebäude/Fassadenseite ein Objekt mit `key`, `label` und einer `items`-Liste
(IST zuerst, dann die Varianten). Jedes Item braucht `image` (Pfad relativ
zur Config-Datei), `tag`, `short` (kurzes Label, erscheint direkt auf dem
Regler — z.B. "IST", "V1"), `title` und `desc`. Die empfohlene Variante mit
`"recommended": true` markieren, das IST-Item mit `"is_ist": true`.

Beschreibungstexte kurz halten (1 Satz) — sie erscheinen unter dem Regler in
einer kleinen Karte, nicht als Fließtext.

Wenn die Quellfotos Hochformat sind (typische Straßenfassaden-Fotos), pro
Objekt `"aspect": "3/4"` setzen; bei Querformat-Renderings (wie bei
KI-generierten Gebäudeansichten) reicht der Standardwert `4/3`.

### 3. Seite bauen

```bash
python scripts/build_site.py config.json output.html
```

Das Script lädt jedes referenzierte Bild, bettet es als Base64 ein (und
verkleinert große Fotos automatisch auf max. 900px Breite, damit die
HTML-Datei nicht ausufert), und rendert `assets/template.html` mit den Daten.
Nicht das Template von Hand mit Bildpfaden befüllen — das Script existiert
genau deshalb, weil das Base64-Einbetten von Hand fehleranfällig ist.

### 4. Verifizieren, bevor die Datei geteilt wird

```bash
node scripts/verify_site.js output.html
```

Prüft strukturell (nicht visuell), dass die Seite ohne JS-Fehler lädt, die
Anzahl der Farbmuster pro Gebäude mit der Config übereinstimmt, Bilder
tatsächlich als Base64 eingebettet sind (kein kaputter Link), Klicks auf
"Links"/"Rechts" die Regler-Beschriftung aktualisieren, der Tausch-Knopf
funktioniert und der Tab-Wechsel zwischen Gebäuden greift. Braucht das
`jsdom`-npm-Paket (`npm install jsdom`, falls nicht vorhanden). Bei Fehlern:
die Config prüfen (fehlende Felder, falsche `key`-Referenzen), nicht das
Template anpassen, es sei denn das Problem liegt nachweislich dort.

Diese Verifikation ersetzt keinen echten Blick auf die Seite — wenn möglich
zusätzlich ein, zwei Screenshots machen oder die Datei kurz beschreiben und
den Nutzer selbst reinschauen lassen, bevor man sie als fertig meldet.

### 5. Datei übergeben

Die fertige HTML-Datei ins Zielverzeichnis kopieren und dem Nutzer über die
Datei-Präsentations-Funktion zeigen (z.B. `present_files` in Cowork). Kurz
erklären, was er tun kann (Regler ziehen, Links/Rechts anklicken, Tabs
wechseln) statt die ganze Struktur nochmal aufzuzählen.

## Design-Entscheidungen, die sich bewährt haben

- **Immer beide Seiten frei wählbar, nicht nur IST fest links.** Ein reiner
  Vorher/Nachher-Regler klingt naheliegend, aber Nutzer wollen oft auch zwei
  Varianten direkt gegeneinander vergleichen, ohne den Ist-Zustand. Deshalb
  ist IST einfach ein weiteres Element in der Farbmuster-Liste, kein
  Sonderfall im Code.
- **Ein Tausch-Knopf statt nur Drag.** Kostet fast nichts, spart aber Klicks,
  wenn man zwei Varianten einfach andersherum sehen will.
- **Kurze `short`-Labels auf dem Regler selbst** (z.B. "V2" statt "Variante 2
  — Terracotta mit Grün") — der Platz auf dem Bild ist knapp, die
  ausführliche Beschreibung steht ohnehin in der Karte darunter.
- **Alles in eine Datei, per Base64.** Kein Hosting, keine kaputten
  Bildpfade, wenn der Nutzer die Datei verschickt oder verschiebt. Der
  Nachteil (größere Datei) ist es wert — bei ~10–15 Fotos liegt die
  fertige Seite meist bei 1,5–3 MB, das ist für eine einmalige HTML-Datei
  unproblematisch.
- **Erst grob zuschneiden/skalieren, dann erst einbetten.** Rohfotos von
  Smartphones sind oft 4000×3000px und mehrere MB — ungeskaliert eingebettet
  wird die Seite unnötig groß und langsam. `build_site.py` skaliert
  automatisch auf 900px Breite; bei Bedarf `--max-width` anpassen.

## Wenn etwas nicht passt

- **Bilder aus dem Grid falsch zugeschnitten** (Bildunterschrift mit im
  Bild, oder Zelle beschnitten): `--caption-frac` bei `crop_grid.py` erhöhen,
  oder `--rows`/`--cols` explizit setzen statt Auto-Erkennung.
- **Seitenverhältnis der Vorschaubilder in der Liste passt nicht** (zu
  gequetscht/gestreckt): liegt an `object-fit: cover` im Template — das ist
  bewusst so, damit alle Kacheln gleich groß bleiben; bei sehr
  unterschiedlichen Seitenverhältnissen innerhalb eines Gebäudes lieber die
  Quellbilder vorab auf ein einheitliches Verhältnis zuschneiden.
- **Mehr als zwei Fassadenseiten/Gebäude:** funktioniert ohne Änderung am
  Code — einfach weitere Objekte in `config.json` ergänzen, das Template
  erzeugt Tabs und Vergleichs-Logik dynamisch für beliebig viele.
