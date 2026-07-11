---
name: immoscout-marktrecherche
description: |
  Automatisierte Marktrecherche auf ImmoScout24 (Deutschland) für Wohnungen oder Häuser,
  jeweils zum Mieten oder Kaufen. Der Skill steuert per Claude-in-Chrome durch die Suche,
  passt den Umkreis dynamisch an, öffnet jedes Exposé, extrahiert die Kerndaten und
  liefert eine Excel-Datei (.xlsx) mit allen Treffern plus eine Übersichtstabelle im Chat.
  Verwende diesen Skill IMMER wenn der Nutzer eine Marktrecherche, Marktanalyse,
  Mietspiegel-Recherche, Verkaufspreis-Übersicht oder einen Wettbewerbsvergleich für
  Immobilien wünscht — auch wenn ImmoScout24 nicht namentlich genannt wird. Trigger sind
  Phrasen wie "Marktcheck Berlin", "was kosten 2-Zimmer-Wohnungen in München", "Häuser
  zum Kauf in der Region X", "Mietpreise um den Ort Y", "Marktsituation für ein Objekt",
  "Wettbewerbsanalyse Immobilien", "Excel mit aktuellen Angeboten". Liefert IMMER eine
  .xlsx — nie nur Text — und zeigt zusätzlich eine kompakte Tabelle im Chat.
---

# ImmoScout24 Marktrecherche

## Worum es geht

Du recherchierst für den Nutzer aktuelle Angebote auf ImmoScout24 und gibst ihm eine
saubere Excel-Datei zurück, mit der er die Marktsituation für ein konkretes Vorhaben
einschätzen kann (Vermietung, Verkauf, Investment, Vergleichsobjekte). Der Nutzer hat
in der Vergangenheit gute Indikationen aus genau diesem Workflow bekommen — wir bauen
darauf auf.

Der Skill geht in drei Phasen vor: **Klären** (Parameter abfragen), **Sammeln** (Browser
steuern, Treffer extrahieren), **Liefern** (Excel + Chat-Tabelle + Qualitätsbericht).

## Phase 1 — Parameter klären

Nutze `AskUserQuestion`, wenn der Nutzer nicht schon alle Parameter genannt hat. Frage
nie nach Dingen, die offensichtlich aus dem Kontext hervorgehen.

### Pflichtparameter

- **stadt** — Ort oder Ortsteil, z. B. `Neuhardenberg`, `Immenstadt im Allgäu`,
  `Berlin-Friedrichshain`.
- **objekttyp** — `wohnung` oder `haus`.
- **modus** — `mieten` oder `kaufen`.

### Optionale Parameter (mit Defaults)

- **umkreis_km_start** — Default `2`. Startradius in km.
- **umkreis_km_min** — Default `0.5`. Untere Grenze, falls heruntergedreht wird.
- **umkreis_km_max** — Default `50`. Obere Grenze, falls hochgedreht wird.
- **max_seiten** — Default: alle. Sicherheitslimit gegen endlose Läufe.
- **zusatzfilter** — Frei: z. B. „nur ab 60 m²", „nur ab 2 Zimmer", „nur EBK". Setze
  diese Filter in der UI, wenn die UI sie anbietet, sonst dokumentiere sie im Bericht
  und wende sie nachgelagert beim Datensatz an.

### Wenn der Nutzer einen Deep-Link mitgibt

Wenn der Nutzer bereits einen ImmoScout24-Suchlink schickt (z. B. aus einer früheren
Sitzung), überspringe das Einstellen von Stadt/Objekttyp/Modus und beginne direkt mit
der Umkreis-Logik und der Listenverarbeitung.

## Phase 2 — Sammeln (Claude in Chrome)

Voraussetzung: Die Claude-in-Chrome-Extension ist verbunden. Wenn nicht, weise den
Nutzer darauf hin und brich ab — Workarounds über `web_fetch` liefern auf ImmoScout24
zu schlechte Daten (JS-Rendering, Bot-Blockade) und sind hier explizit nicht
vorgesehen.

### Browser-Schritte

1. `mcp__Claude_in_Chrome__navigate` → `https://www.immobilienscout24.de/`.
2. Cookie-Banner und etwaige Newsletter-Popups schließen (über `find` +
   `form_input`/`computer` klicken).
3. Stadt eingeben, Kategorie wählen (Wohnungen vs. Häuser), Modus wählen
   (Mieten vs. Kaufen), Suche starten.
4. Falls die UI einen Umkreis-Filter anbietet: setze ihn auf `umkreis_km_start`.
5. Lies die Trefferzahl aus dem Listenkopf (`get_page_text` und reguläre Suche
   nach "Treffer" / "Ergebnisse").

### Umkreis-Logik (das Herzstück)

Ziel: 5–30 Treffer. Darunter ist die Stichprobe zu klein, darüber wird die Liste
unübersichtlich und der Lauf zu lang.

- **Zu wenig (< 5 Treffer)**: Umkreis schrittweise hochdrehen
  `2 → 5 → 10 → 20 → 30 → 40 → 50`, jeweils Liste neu laden und Treffer neu zählen.
  Stoppe sobald `> 5` oder `umkreis_km_max` erreicht.
- **Zu viele (> 30 Treffer)**: Umkreis schrittweise runterdrehen
  `10 → 5 → 3 → 2 → 1 → 0.5`, jeweils neu laden. Stoppe sobald `< 15` oder
  `umkreis_km_min` erreicht.
- **UI bietet keinen Radius**: Regel auslassen, mit allen Treffern weitermachen,
  im Endbericht vermerken.
- **Selbst bei max. Umkreis ≤ 5 Treffer**: akzeptieren und dokumentieren.
- **Selbst bei min. Umkreis ≥ 15 Treffer**: akzeptieren und dokumentieren.

### Listenverarbeitung

Gehe Seite für Seite durch die Paginierung („Weiter") bis `max_seiten` oder Ende.
Für jedes Listenelement:

1. Öffne das Exposé in einem neuen Tab (`mcp__Claude_in_Chrome__tabs_create_mcp` mit
   der Inserats-URL).
2. `get_page_text` auf dem Exposé-Tab.
3. Extrahiere die Felder (siehe Feldliste unten).
4. Schließe den Tab (`tabs_close_mcp`).
5. Wartezeit 200–600 ms zwischen Aktionen, damit der Lauf natürlich wirkt.

**Resilienz**: Popup taucht auf → schließen. Seite hängt → einmal reload. Inserat
nicht lesbar (z. B. Login-Wall) → überspringen, in der Excel als Zeile mit `notiz =
"übersprungen: <Grund>"` und ansonsten leeren Feldern hinterlassen, damit der Nutzer
weiß, dass es existiert hat.

### Felder

**Immer erfassen (alle Kombinationen):**

- `listing_url` — kanonischer Exposé-Link, Schlüssel für Deduplizierung
- `titel`
- `stadt` — Ort/Ortsteil aus dem Exposé
- `plz`
- `strasse` — leer lassen, wenn nicht sichtbar (nicht raten)
- `flaeche_qm` — Wohnfläche als Zahl
- `zimmer` — als Zahl (`„2,5"` → `2.5`)
- `zustand_kurz` — max. 5 Stichworte, mit `; ` getrennt: z. B.
  `gepflegt; EBK; Balkon; saniert; Lift`
- `energieeffizienzklasse` — falls angegeben
- `baujahr` — falls angegeben
- `etage` — bei Wohnungen relevant
- `anbieter_typ` — `privat` oder `Makler`, wenn erkennbar
- `vermietungsstatus` — `bezugsfrei` oder `vermietet`, wenn das Exposé das eindeutig
  ausweist. Typische Hinweise im Inserat: ein Feld „Vermietet: Ja/Nein",
  Formulierungen wie „bezugsfrei ab …", „aktuell vermietet", „vermietet,
  Mieteinnahme …", „frei", „leerstehend". **Leer lassen, wenn die Information fehlt
  oder unklar ist** — nicht aus dem Kontext raten. Diese Spalte ist vor allem für
  Kauf-Recherchen wichtig (Eigennutzung vs. Kapitalanlage), wird aber für jeden
  Modus erfasst, falls sie da ist, damit das Schema konsistent bleibt.
- `notiz` — leer, oder z. B. `übersprungen: Login erforderlich`

**Berechnet (nicht aus dem Exposé, sondern aus den anderen Feldern):**

- `preis_pro_qm` — Preis pro Quadratmeter, gerundet auf 2 Nachkommastellen. Wird
  nach dem Sammeln aus den bereits erfassten Feldern errechnet, damit der Nutzer
  Vergleichsobjekte sofort einsortieren kann.
  - Bei `modus = kaufen`: `kaufpreis / flaeche_qm`.
  - Bei `modus = mieten`: `kaltmiete / flaeche_qm` (Kaltmiete bevorzugt, weil
    objektiv vergleichbar; wenn `kaltmiete` leer ist, das Feld leer lassen — nicht
    aus der Warmmiete rechnen, das verzerrt den Vergleich).
  - Wenn einer der beiden Operanden fehlt oder `flaeche_qm` 0 ist, bleibt
    `preis_pro_qm` **leer**.

**Nur bei `modus = kaufen`:**

- `kaufpreis` — Zahl, ohne `€`
- `hausgeld` — bei Eigentumswohnungen
- `provision` — wenn angegeben

**Nur bei `modus = mieten`:**

- `kaltmiete`
- `warmmiete` — oder „Gesamtmiete"; leer lassen, wenn nicht explizit ausgewiesen
  (NICHT schätzen)
- `nebenkosten`

**Zusätzlich bei `objekttyp = haus`:**

- `grundstueck_qm`
- `haustyp` — z. B. `DHH`, `EFH`, `RH`
- `anzahl_etagen`

**Zusätzlich bei `objekttyp = wohnung`:**

- `wohnungstyp` — z. B. `Dachgeschoss`, `Maisonette`
- `hausgeld` — beim Kauf, falls genannt

### Normalisierung

- Währungs- und Einheitenzeichen entfernen (`€`, `m²`).
- Deutsche Dezimalkommas → Punkt (`74,74` → `74.74`).
- Tausendertrennzeichen und Leerzeichen in Zahlen entfernen (`1 234 €` → `1234`).
- Nicht gefundene Felder bleiben **leer** — nie raten, nie interpolieren.
- Dedupliziere am Ende nach `listing_url`.

## Phase 3 — Liefern

### Excel erzeugen

Verwende dafür den `xlsx`-Skill (`Read` auf
`/sessions/peaceful-charming-einstein/mnt/.claude/skills/xlsx/SKILL.md` und folge
dessen Anleitung), damit die Datei sauber formatiert ist.

- Eine einzige Sheet namens `Angebote`.
- Eine Zeile pro Inserat.
- Alle Spalten aus der vollständigen Feldliste oben in dieser Reihenfolge:
  `listing_url, titel, stadt, plz, strasse, flaeche_qm, zimmer, zustand_kurz,
  energieeffizienzklasse, baujahr, etage, anbieter_typ, vermietungsstatus,
  kaufpreis, preis_pro_qm, hausgeld, provision, kaltmiete, warmmiete, nebenkosten,
  grundstueck_qm, haustyp, anzahl_etagen, wohnungstyp, notiz`. Spalten, die für die
  Kombination keinen Sinn ergeben (z. B. `kaufpreis` beim Mieten), bleiben in der
  Datei vorhanden, aber leer — so passen alle Recherchen ins gleiche Schema und
  lassen sich zusammenführen. `preis_pro_qm` wird in Python berechnet und als
  Zahl geschrieben (nicht als Excel-Formel), damit Sortieren und Filtern in jedem
  Tool gleich funktioniert.
- Header fett, Zahlenformate für `flaeche_qm`, `zimmer`, Preise, `preis_pro_qm`
  und `grundstueck_qm` setzen (Tausendertrennzeichen, deutsche Lokalisierung;
  `preis_pro_qm` mit 2 Nachkommastellen).
- Spaltenbreiten autoFit.
- Dateiname:
  `immoscout_{stadt}_{objekttyp}_{modus}.xlsx`
  Sonderzeichen und Leerzeichen in `stadt` mit Unterstrich ersetzen, z. B.
  `immoscout_Immenstadt_im_Allgaeu_wohnung_kaufen.xlsx`.
- Speicherort: `outputs/` (damit der Nutzer sie über `computer://` öffnen kann).

### Chat-Tabelle

Zeige zusätzlich eine kompakte Markdown-Tabelle im Chat mit den wichtigsten Spalten
(je nach Modus 7–9 Spalten: `titel`, `stadt`/`plz`, `flaeche_qm`, `zimmer`,
Preis(e), `preis_pro_qm`, `vermietungsstatus` (sofern bei mindestens einer Zeile
gefüllt), `zustand_kurz`, `listing_url` als Link). So sieht der Nutzer ohne
Excel-Klick die Lage auf einen Blick — `preis_pro_qm` macht den Vergleich auf
einen Schlag möglich.

### Qualitätsbericht (am Ende der Antwort)

Berichte in 5–8 Zeilen:

- Stadt, Objekttyp, Modus
- Finaler Umkreis in km (oder „UI bietet keinen Umkreis-Filter")
- Treffer gesamt laut Liste vs. tatsächlich verarbeitete Inserate
- Anzahl verarbeiteter Seiten
- 3 Beispielzeilen aus der Excel
- Etwaige Anomalien (übersprungene Inserate, fehlende Felder gehäuft, etc.)

### Link

Schließe mit einem `computer://`-Link zur Excel-Datei ab, kurz und ohne Postamble:

```
[Marktrecherche öffnen](computer://<absoluter Pfad zur xlsx>)
```

## Verhalten bei Fehlern

- **Claude-in-Chrome nicht verbunden**: Klar sagen, nicht mit `web_fetch`
  improvisieren. Frage den Nutzer, die Extension zu verbinden.
- **ImmoScout24 zeigt Captcha / Bot-Wall**: Berichte das ehrlich, liefere die bis
  dahin gesammelten Treffer und brich kontrolliert ab.
- **Keine Treffer überhaupt**: Liefere die Excel mit Header-Zeile und leerem Body
  und vermerke das im Bericht — der Nutzer soll sehen, dass der Lauf sauber lief,
  der Markt aber leer ist.

## Beispiel-Eingaben

- „Mach mir eine Marktrecherche für 2-Zimmer-Wohnungen zur Miete in Neuhardenberg."
  → `stadt=Neuhardenberg`, `objekttyp=wohnung`, `modus=mieten`,
  `zusatzfilter="ab 2 Zimmer"`.
- „Was kosten Häuser zum Kauf in Immenstadt im Allgäu?"
  → `stadt=Immenstadt im Allgäu`, `objekttyp=haus`, `modus=kaufen`.
- „Hier ist mein Suchlink: <URL> — bau mir die Excel."
  → Deep-Link-Pfad: direkt auf der URL starten, ab Umkreis-Logik weitermachen.

## Warum dieser Skill so ist, wie er ist

Der Nutzer hat denselben Workflow vorher mit einem anderen Tool gefahren und gute
Marktindikationen bekommen. Drei Sachen sind dabei besonders wichtig und werden hier
bewusst beibehalten:

- **Adaptiver Umkreis** — zu wenige Treffer sind nutzlos, zu viele machen die Liste
  unbedienbar. Der Korridor 5–30 hat sich bewährt.
- **Konsistentes Spaltenschema** — auch wenn manche Felder leer bleiben, weil sie
  zum Modus nicht passen, lassen sich Excel-Dateien aus verschiedenen Läufen so
  später leicht zusammenführen.
- **Keine geschätzten Werte** — Warmmiete, Nebenkosten oder Provision werden nur
  übernommen, wenn sie tatsächlich im Inserat stehen. Sonst wäre die Excel
  trügerisch.
