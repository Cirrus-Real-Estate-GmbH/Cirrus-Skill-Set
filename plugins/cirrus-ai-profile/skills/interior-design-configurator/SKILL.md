---
name: interior-design-configurator
description: >
  Baut aus Wohnungsfotos einen zweistufigen Einrichtungs-Workflow: (1) Claude fragt kurz
  die geplante Nutzung jedes Raums ab, legt drei Design-Richtungen für die ganze Wohnung
  fest und erstellt daraus genau drei kopierbare Prompts für ChatGPT/Gemini (einen je
  Design, nicht einen pro Raum), mit denen konsistente, fotorealistische
  Einrichtungsvarianten (inkl. Wandfarbe) für alle Räume generiert werden, ohne dass
  sich Geometrie, Fenster, Heizkörper oder Steckdosen verändern; (2) nach Upload der
  generierten Bilder baut Claude daraus eine interaktive HTML-Seite (Vorher/Nachher-
  Regler pro Raum, Tabs zwischen Räumen) als Wohnungs-Exposé. Verwenden, wenn Fotos
  einer leeren/unmöblierten Wohnung hochgeladen werden und Einrichtungsideen,
  Möblierungsvarianten oder ein visuelles Exposé gewünscht sind — auch bei
  "Einrichtungsvorschläge", "Home Staging", "virtuell möblieren", "Interior-Konzept",
  oder wenn bereits mehrere KI-generierte Varianten pro Raum vorliegen.
---

# Interior Design Configurator

## Worum es geht

Ein Vermieter, Makler oder Investor hat Fotos einer leeren oder unmöblierten Wohnung
und möchte zeigen, wie die Räume mit unterschiedlicher Möblierung wirken könnten —
klassisches virtuelles Home Staging. Claude selbst kann keine Bilder generieren, die
Fotorealismus und Konsistenz mit dem Originalfoto garantieren; das übernehmen
ChatGPT (Bildgenerierung) oder Gemini. Dieser Skill überbrückt das in zwei Phasen:

1. **Prompt-Phase**: Claude fragt die geplante Nutzung je Raum ab, legt gemeinsam mit
   dem Nutzer drei Design-Richtungen für die ganze Wohnung fest und erstellt daraus
   drei Prompts — einen je Design, nicht einen pro Raum. Jeder Prompt referenziert
   alle Raumfotos zusammen und liefert ein konsistent gestaltetes Bild je Raum in
   diesem Design. Das hält jeden Generierungslauf unter dem üblichen Bilder-Limit
   von ChatGPT/Gemini und sorgt für einen stimmigen Stil über die ganze Wohnung,
   statt pro Raum unabhängig gewählter Stile. Der Nutzer nimmt die drei Prompts
   (zusammen mit allen Originalfotos) mit zu ChatGPT oder Gemini und generiert dort
   in drei Durchläufen alle Design-Varianten.
2. **Exposé-Phase**: Der Nutzer lädt die generierten Bilder wieder bei Claude hoch.
   Claude baut daraus eine einzelne interaktive HTML-Datei mit einem
   Vorher/Nachher-Regler pro Raum (Original vs. Variante, frei wählbar welche Seite)
   und Tabs zum Wechseln zwischen den Räumen — analog zum Facade-Color-Configurator,
   aber für Innenräume und Möblierung statt Fassaden und Farbe.

## Wann dieser Skill greift

- Nutzer lädt Fotos einer leeren/unmöblierten Wohnung hoch und fragt nach
  Einrichtungsideen, Möblierungsvorschlägen oder virtuellem Home Staging
- "Kannst du zeigen, wie das möbliert aussehen könnte?"
- "Ich brauche Einrichtungsvarianten für das Exposé"
- Nutzer hat bereits KI-generierte Möblierungsbilder (aus ChatGPT/Gemini) und möchte
  daraus eine vergleichbare/interaktive Ansicht bauen

## Workflow

### Phase 1: Prompts für ChatGPT/Gemini erstellen

**Grundprinzip: immer genau 3 Prompts, einer je Design-Richtung — nicht einer pro
Raum und nicht ein Sammel-Prompt mit allen Varianten.** Jeder Prompt referenziert
alle Raumfotos zusammen und liefert ein Bild je Raum in diesem einen Design. Das
hält jeden Generierungslauf unter dem üblichen Bilder-Limit von ChatGPT/Gemini
(~10 Bilder pro Lauf) und sorgt für einen stimmigen Stil über die ganze Wohnung.
Details und vollständige Vorlage: `references/prompt_template.md`.

**1. Fotos entgegennehmen und Räumen zuordnen.** Der Nutzer lädt ein oder mehrere
Fotos hoch (ein Foto pro Raum, im Idealfall). Räume anhand Dateiname oder Bildinhalt
identifizieren (Wohnzimmer, Schlafzimmer, Küche, Bad, Flur, …). Bei Unklarheit kurz
nachfragen, welches Foto zu welchem Raum gehört.

**2. Geplante Nutzung je Raum abfragen.** Für jeden Raum kurz die geplante Nutzung
erfragen (nicht nur den Raumtyp) — Details siehe `references/prompt_template.md`,
Abschnitt "Schritt 0". Bei eindeutigen Räumen (Küche, Bad) kann das übersprungen
werden. Bei flexibel nutzbaren Räumen (Zusatzzimmer, offener Grundriss) immer
fragen, z.B. ob ein Zimmer als Homeoffice, Gästezimmer oder Kinderzimmer möbliert
werden soll — das beeinflusst maßgeblich, welche Möbel ChatGPT/Gemini wählt.

**3. Drei Design-Richtungen für die ganze Wohnung festlegen.** Nicht pro Raum
unabhängig erfinden, sondern drei stimmige Gesamtkonzepte (Name, Stilbeschreibung,
je Raum eine passende Wandfarbe innerhalb der Design-Linie). Kurz im Chat
vorschlagen und dem Nutzer die Möglichkeit zur Anpassung geben. Details und
Beispiele: `references/prompt_template.md`, Abschnitt "Schritt 1".

**4. Drei Prompts ausgeben (einen je Design).** Vorlage aus
`references/prompt_template.md`, Abschnitt "Schritt 2" verwenden — jeden der drei
Prompts als eigenen kopierbaren Codeblock ausgeben. Erklären: alle Fotos **und**
der jeweilige Design-Prompt gemeinsam bei ChatGPT/Gemini hochladen, das **dreimal**
wiederholen (einmal je Design). Bei mehr als ca. 10 Räumen: siehe Abschnitt "Wenn
die Wohnung mehr als ca. 10 Räume hat" in der Vorlage — dort in Raumgruppen
aufteilen, statt das Bilder-Limit zu riskieren.

**5. Erwartung setzen.** Der Nutzer generiert die Bilder selbst in ChatGPT/Gemini
(Claude kann das nicht in diesem Schritt übernehmen) und kommt danach mit den
Ergebnissen zurück. Kurz ankündigen: "Sobald du alle drei Durchläufe hast, lade
die Bilder hier hoch — dann baue ich dir daraus eine interaktive Vergleichsseite."

### Phase 2: Interaktives Exposé bauen

**1. Generierte Bilder entgegennehmen.** Der Nutzer lädt pro Raum das Original plus
die (in der Regel drei) generierten Varianten hoch. Falls ein Modell alle Varianten
als ein einziges Collage-Bild statt als Einzelbilder liefert (kommt v.a. bei Gemini
vor), zuerst zerschneiden:

```bash
python scripts/crop_grid.py grid.png outdir/ --prefix wohnzimmer
```

Erkennt Zeilen/Spalten automatisch anhand heller Zwischenräume. Bei unregelmäßigen
Rastern `--rows`/`--cols` explizit setzen. Ergebnis-Dateien danach **immer visuell
prüfen** (z.B. mit dem View-Tool ansehen) und sinnvoll umbenennen — welches Bild zu
welcher Variante gehört, muss inhaltlich stimmen, das lässt sich nicht automatisieren.

Falls Bilder nur inline im Chat eingefügt wurden (nicht als Datei hochgeladen), gibt
es keinen Dateizugriff darauf — den Nutzer bitten, sie als Dateianhang hochzuladen.

**2. Config-Datei schreiben.** Ein `config.json` nach dem Muster in
`references/config_example.json` anlegen: ein Objekt mit `title` und einer
`rooms`-Liste. Jeder Raum hat `key`, `label`, optional `aspect` (Seitenverhältnis der
Fotos, Standard `4/3`) und eine `items`-Liste — das Original zuerst (mit
`"is_ist": true`), danach die generierten Varianten. Jedes Item braucht `image`
(Pfad relativ zur config.json), `short` (kurzes Label für den Regler, z.B. "Option 1"),
`title` (ausführlicherer Titel), `desc` (ein Satz Beschreibung). Die empfohlene
Variante mit `"recommended": true` markieren, falls eine hervorgehoben werden soll —
optional, kann auch weggelassen werden.

Beschreibungstexte kurz halten (1 Satz) — sie erscheinen in kleinen Karten unter dem
Regler, nicht als Fließtext.

**3. Seite bauen.**

```bash
python scripts/build_site.py config.json output.html
```

Das Script lädt jedes referenzierte Bild, bettet es als Base64 ein (verkleinert
große Fotos automatisch auf max. 1100px Breite, damit die Datei nicht ausufert) und
rendert `assets/template.html` mit den Daten. Nicht das Template von Hand mit
Bildpfaden befüllen — das Script existiert genau deshalb, weil Base64-Einbetten von
Hand fehleranfällig ist. Braucht Pillow (`pip install pillow --break-system-packages`
falls nicht vorhanden; funktioniert auch ohne, dann werden Bilder unskaliert
eingebettet).

**4. Verifizieren, bevor die Datei geteilt wird.**

```bash
node scripts/verify_site.js output.html
```

Prüft strukturell (nicht visuell), dass die Seite ohne JS-Fehler lädt, die Anzahl der
Tabs mit der Anzahl der Räume übereinstimmt, die Anzahl der Swatches pro Raum mit der
Config übereinstimmt und alle Bilder tatsächlich als Base64 eingebettet sind. Braucht
das `jsdom`-npm-Paket (`npm install jsdom`, falls nicht vorhanden). Bei Fehlern: die
Config prüfen (fehlende Felder, falsche `key`-Referenzen), nicht das Template
anpassen, es sei denn das Problem liegt nachweislich dort.

Diese Verifikation ersetzt keinen echten Blick auf die Seite — wenn möglich
zusätzlich kurz beschreiben, was der Nutzer sehen wird, und ihn selbst reinschauen
lassen, bevor die Datei als fertig gemeldet wird.

**5. Datei übergeben.** Die fertige HTML-Datei ins Ausgabeverzeichnis kopieren und
dem Nutzer über die Datei-Präsentations-Funktion zeigen. Kurz erklären, was er tun
kann (Regler ziehen, Links/Rechts an den Kacheln anklicken, zwischen Raum-Tabs
wechseln, Tausch-Knopf) statt die ganze Struktur nochmal aufzuzählen.

## Design-Entscheidungen, die sich bewährt haben

- **Beide Seiten des Reglers frei wählbar, nicht nur Original fest links.** Nutzer
  wollen oft auch zwei Möblierungsvarianten direkt gegeneinander vergleichen, ohne
  den unmöblierten Zustand. Das Original ist deshalb einfach ein weiteres Element in
  der Swatch-Liste (`is_ist: true`), kein Sonderfall im Code.
- **Ein Tausch-Knopf statt nur Drag.** Kostet fast nichts, spart aber Klicks.
- **Kurze `short`-Labels auf dem Regler selbst** (z.B. "Option 2" statt "Option 2 —
  Warmer Loft-Stil mit dunklerem Holz") — der ausführliche Titel/Beschreibung steht
  in der Karte darunter.
- **Alles in eine Datei, per Base64.** Kein Hosting, keine kaputten Bildpfade beim
  Verschicken oder Verschieben der Datei.
- **Immer 3 Prompts, einer je Design, nicht einer pro Raum oder ein Sammel-Prompt
  mit allen Varianten.** Ein Prompt pro Design hält jeden Generierungslauf unter dem
  üblichen Bilder-Limit von ChatGPT/Gemini (~10 Bilder) und sorgt dafür, dass der
  Stil über die ganze Wohnung konsistent bleibt, statt pro Raum unabhängig gewählter
  Einzelstile.
- **Wandfarbe ist Teil der Variante, nicht nur Möblierung.** Jede der drei Varianten
  bekommt eine eigene, zum Stil passende Wandfarbe vorgeschlagen — das macht die
  Optionen im Regler-Vergleich klarer unterscheidbar. Nur Bodenbelag, Fenster,
  Heizkörper und Steckdosen bleiben fix.

## Wenn etwas nicht passt

- **Generierte Bilder verändern doch die Fensterposition/Raumgeometrie:** kommt
  gelegentlich vor, v.a. bei starken Stilwechseln. Den Nutzer darauf hinweisen, dass
  er die Variante in ChatGPT/Gemini neu generieren oder den Prompt um einen expliziten
  Hinweis auf das jeweils betroffene Element ergänzen sollte (z.B. "Fenster exakt an
  Position X wie im Originalfoto belassen").
- **Bilder aus der Collage falsch zugeschnitten:** `--caption-frac` bei
  `crop_grid.py` erhöhen, oder `--rows`/`--cols` explizit setzen statt Auto-Erkennung.
- **Seitenverhältnis der Vorschaubilder passt nicht** (gequetscht/gestreckt): liegt an
  `object-fit: cover` im Template — bewusst so, damit alle Kacheln gleich groß
  bleiben. Bei sehr unterschiedlichen Seitenverhältnissen die Quellbilder vorab auf
  ein einheitliches Verhältnis zuschneiden.
- **Mehr als 2-3 Räume oder mehr als 3 Varianten pro Raum:** funktioniert ohne
  Codeänderung — einfach weitere Objekte in `config.json` ergänzen, Template erzeugt
  Tabs und Swatch-Listen dynamisch.
