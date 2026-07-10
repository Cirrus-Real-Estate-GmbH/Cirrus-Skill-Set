---
name: comps-analyse-generator
description: >
  Erstelle eine Comps-Analyse (Vergleichswertanalyse) für ein Immobilienobjekt von Cirrus Real Estate GmbH.
  Trigger diesen Skill immer dann, wenn der Nutzer eine "Comps-Analyse", "Vergleichswertanalyse", "Marktvergleich"
  oder ähnliches für ein Objekt erstellen möchte — auch bei Formulierungen wie "mach mal Comps zu...",
  "vergleichbare Objekte suchen" oder "was ist die Wohnung wert im Vergleich zum Markt". Der Skill fragt zuerst
  nach dem Zielobjekt und der Strategie (Buy & Hold oder Fix & Flip), liefert dann passende ImmoScout24-Suchparameter
  sowie eine Anleitung für den CHECK24-Immobiliencheck, lässt sich die ImmoScout24-Ergebnisseite (HTML) sowie
  möglichst viele CHECK24-Marktwerteinschätzungen vom Nutzer einfügen, und baut daraus eine Excel-Analyse nach der
  festen Cirrus-Vorlage (Google Sheets Vorlage-ID: 15F--X7AlEwJ0A3wVQbwSpqhHhpphWUBpo5i6fC_zqls).
---

# Comps-Analyse-Generator für Cirrus Real Estate GmbH

## Überblick

Dieser Skill erstellt eine vollständige Comps-Analyse (Vergleichswertanalyse) als XLSX-Datei nach fester
Cirrus-Vorlage. Er kombiniert zwei Datenquellen:

1. **ImmoScout24** — Vergleichsobjekte aus dem Einzelverkauf (Ergebnisliste als HTML vom Nutzer eingefügt)
2. **CHECK24 Immobiliencheck** (PriceHubble AVM) — automatisierte Marktwerteinschätzungen

**Ablauf:**
1. Objekt & Strategie erfragen (Buy & Hold vs. Fix & Flip)
2. ImmoScout24-Suchparameter + CHECK24-Anleitung an den Nutzer ausgeben
3. Nutzer fügt ImmoScout24-HTML und möglichst viele CHECK24-Einschätzungen ein
4. Daten extrahieren, in die Cirrus-Vorlage einbauen, Mittelwert/Median berechnen
5. XLSX ausgeben + als Download bereitstellen
6. Falls der Nutzer keine eigene Kopie der Vorlage hat: eine Kopie in seinem Google Drive ablegen

---

## Schritt 1: Objekt & Strategie erfragen

Bevor irgendetwas anderes passiert, IMMER zuerst fragen (in einer kompakten Nachricht, ggf. mit `ask_user_input_v0`):

1. **Welches Objekt?** (Adresse, Exposé-Upload, oder Objektname aus vorherigem Chat)
2. **Buy & Hold oder Fix & Flip?**

Falls das Zielobjekt bereits im Chat-Kontext eindeutig ist (z.B. gerade hochgeladenes Exposé), nur nach der
Strategie fragen.

Aus dem Objekt (Exposé, Upload oder Nutzerangabe) folgende Eckdaten ableiten bzw. erfragen, falls nicht vorhanden:
- Adresse (Straße, PLZ, Ort)
- Wohnfläche (m²) und Zimmerzahl
- Objektart (Wohnung, Zinshaus, Mehrfamilienhaus etc.)

---

## Schritt 2: Suchparameter ausgeben

### A) ImmoScout24-Suchparameter

Immer angeben:
- **Suchradius**: 1–2 km in Städten/dichten Lagen, 2–5 km in ländlichen Lagen (Einwohnerzahl < 20.000 → eher 5 km)
- **Immobilientyp**: Wohnung kaufen (Einzelverkauf, keine Neubauprojekte/Paketverkäufe außer explizit gewünscht)
- **Wohnfläche**: Zielobjekt-Fläche ±30–50%
- **Zimmerzahl**: Zielobjekt-Zimmerzahl ±1

Je nach Strategie unterschiedlicher Fokus:

**Buy & Hold** (Kapitalanlage, Halten & Vermieten):
- Zusätzlich nach vermieteten Objekten filtern bzw. "Kapitalanlage"/"vermietet" im Titel beachten, da diese
  die Marktrealität für Renditeobjekte widerspiegeln
- Hinweis an Nutzer: sowohl vermietete als auch unvermietete Vergleichsobjekte einbeziehen, aber
  Vermietungsstatus in der Tabelle vermerken (Spalte `vermietungsstatus`)
- Optional: falls Mietrendite relevant ist, zusätzlich auf Mietwohnungen-Comps hinweisen (separates Sheet, nur
  falls der Nutzer das explizit will)

**Fix & Flip** (Sanieren & Verkaufen):
- Fokus auf den **Exit-Zustand**: Vergleichsobjekte sollten saniert/modernisiert/neuwertig sein (also der
  Zustand, den das Zielobjekt NACH der Sanierung haben wird), nicht der aktuelle (oft unsanierte) Zustand
  des Zielobjekts
- Zusätzlich unsanierte Objekte als Anhaltspunkt für den aktuellen Einkaufspreis-Vergleich sammeln, falls
  vorhanden — aber die Kernanalyse (Mittelwert/Median €/m²) bezieht sich auf den poliertierten Exit-Zustand

Gib dem Nutzer die fertige ImmoScout24-Such-URL oder zumindest die konkreten Filterkriterien in einer klar
kopierbaren Form.

### B) CHECK24 Immobiliencheck

Anleitung an den Nutzer:
1. Auf check24.de den Immobiliencheck / die Immobilienbewertung öffnen
2. Adresse des Zielobjekts (des Objekts in Akquise) eingeben, Objektart "Wohnung", Verkauf
3. **Wichtig**: Der Nutzer soll für **jede einzelne Wohneinheit des Zielobjekts in Akquise** (also die
   tatsächlichen Wohnungen/Einheiten des Objekts, das gerade angekauft werden soll) eine eigene
   CHECK24-Einschätzung erstellen — mit der jeweils echten Wohnfläche, Zimmerzahl etc. dieser Einheit. So
   entsteht pro Einheit ein CHECK24-Marktwert (PriceHubble AVM), der anschließend dem marktüblichen
   €/m²-Preis aus den ImmoScout24-Vergleichsobjekten (Einzelverkauf) gegenübergestellt wird.
4. Für jede Wohneinheit des Objekts eine Einschätzung erstellen (bei einem Mehrfamilienhaus/Zinshaus also
   potenziell mehrere Einschätzungen, eine je Einheit) — jede CHECK24-Bewertung als PDF oder Screenshot/Text
   an den Chat übergeben

Sag dem Nutzer explizit:
> "Bitte kopiere die HTML-Seite der ImmoScout24-Ergebnisliste (z.B. mit Rechtsklick → Seitenquelltext anzeigen,
> alles kopieren, oder einfach die komplette Seite per Strg+A / Strg+C) und füge sie hier ein. Erstelle zusätzlich
> so viele CHECK24-Einschätzungen wie möglich für die Region — mit einer Wohnfläche, die dem Durchschnitt der
> m²-Zahl deiner ImmoScout24-Vergleichswohnungen entspricht — und lade sie hier hoch oder füge sie ein."

---

## Schritt 3: Daten extrahieren

### ImmoScout24-HTML

Aus der eingefügten HTML-Seite pro Objekt extrahieren (siehe Spaltenstruktur unten):
- `listing_url` (aus `/expose/{id}` Links, volle URL rekonstruieren: `https://www.immobilienscout24.de/expose/{id}`)
- `expose_id`
- `titel`
- `stadt`, `plz`, `strasse` (aus Adressfeld, falls vorhanden — sonst leer lassen)
- `flaeche_qm`, `zimmer`
- `kaufpreis`, `kaufpreis_qm` (berechnen falls nicht direkt angegeben: kaufpreis / flaeche_qm)
- `zustand_kurz` (Tags/Schlagworte aus der Karte, z.B. "vermietet; Balkon; Keller")
- `zustandsbeschreibung_kurz` (kurzer Fließtext, max. 1–2 Sätze)
- `vermietungsstatus` (falls im Titel/Text erkennbar, sonst leer)
- `energieeffizienzklasse`, `baujahr`
- `etage` (falls erkennbar)
- `anbieter_typ` (i.d.R. "Makler"), `anbieter` (Firmenname)
- `hausgeld` (falls angegeben)
- `provision` ("ja"/"nein"/Prozentsatz, je nach Angabe — courtage-Feld beachten)
- `wohnungstyp` (z.B. "Maisonette", "Penthouse" — nur falls explizit im Titel/Tags erwähnt, sonst leer lassen)

**Wichtig:** Keine Objekte erfinden oder Daten schätzen, die nicht in der HTML stehen — leere Felder bleiben leer.

### CHECK24-Einschätzungen

Pro eingefügter CHECK24-Bewertung extrahieren:
- `adresse`, `objektart`
- `marktwert_eur`, `marktwert_qm_eur`
- `wertspanne_min`, `wertspanne_max`
- `konfidenz`
- `zimmer`, `badezimmer`, `flaeche_qm`, `baujahr`
- `garagenplaetze`, `aussenparkplaetze`
- `bewertungsdatum`

---

## Schritt 4: Vorlage anwenden & XLSX erstellen

**Immer die xlsx-Skill-Konventionen befolgen** (`/mnt/skills/public/xlsx/SKILL.md` lesen, falls noch nicht im
Kontext) — insbesondere: Formeln statt hartcodierter Werte für Mittelwert/Median, danach mit
`scripts/recalc.py` neu berechnen und auf Null Fehler prüfen.

### Struktur (exakt nach Vorlage übernehmen)

**Tabelle 1 — Vergleichsobjekte (ImmoScout24):**
Spaltenreihenfolge exakt wie oben in Schritt 3 aufgeführt (`listing_url` bis `wohnungstyp`).
Direkt unter der letzten Datenzeile:
- Zeile "Mittelwert:" mit `=AVERAGE(...)` auf Spalte `kaufpreis_qm`
- Zeile "Median:" mit `=MEDIAN(...)` auf Spalte `kaufpreis_qm`

**Tabelle 2 — CHECK24 Marktwerteinschätzungen:**
Mit deutlichem Abstand (mind. 2 Leerzeilen) unter Tabelle 1, mit eigener Überschrift
"CHECK24 Marktwerteinschätzungen (PriceHubble AVM) – Zielobjekte" und Spaltenreihenfolge wie in Schritt 3.
Ebenfalls Mittelwert/Median-Zeilen für `marktwert_qm_eur`.

### Formatierung
- Schriftart: Arial, konsistent mit bisherigen Cirrus-Comps-Dateien
- Kopfzeilen: dunkelblauer Hintergrund (`1F3864`), weiße fette Schrift, zentriert
- Währungsformate: `#,##0"€"` für Preis-/€-Spalten
- Spaltenbreiten großzügig für lange Titel/Anbieter-Felder

### Dateiname
`Comps Analyse - [Objektart] - [Adresse].xlsx` (z.B. `Comps Analyse - Wohnung - Wallstraße 3, 14641 Nauen.xlsx`)

---

## Schritt 5: Ausgabe

1. XLSX in `/mnt/user-data/outputs/` speichern und per `present_files` bereitstellen
2. Kurze Zusammenfassung im Chat: Anzahl gefundener Vergleichsobjekte, Anzahl CHECK24-Einschätzungen,
   Mittelwert/Median €/m² aus beiden Quellen, kurze Einordnung des Zielobjekts relativ zu diesen Werten
   (Aufschlag/Abschlag in %), unter Berücksichtigung der gewählten Strategie (Buy & Hold vs. Fix & Flip)

---

## Schritt 6: Vorlage in Google Drive sicherstellen

Die Cirrus-Vorlage liegt unter dieser Google Sheets ID:
`15F--X7AlEwJ0A3wVQbwSpqhHhpphWUBpo5i6fC_zqls`

Bevor die Analyse erstellt wird, prüfen: hat der Nutzer bereits eine eigene Kopie dieser Vorlage in seinem
Drive (z.B. durch Suche nach "Vorlage" + "Comps Analyse")?

- **Falls ja**: Struktur dieser Kopie verwenden (falls der Nutzer sie inzwischen angepasst hat, seine Version
  respektieren).
- **Falls nein**: Mit dem Google Drive MCP (`copy_file`) eine Kopie der Vorlage in "Meine Ablage" (Drive-Root)
  des Nutzers ablegen, benannt nach dem aktuellen Objekt (z.B. `Vorlage - Wohnung - Wallstraße 3, 14641 Nauen -
  Comps Analyse`), bevor die eigentliche Analyse-Datei erstellt wird. Den Nutzer kurz informieren, dass die
  Vorlage abgelegt wurde.

---

## Wichtige Hinweise

- **Sprache:** Immer Deutsch
- **Keine Daten erfinden:** Nur Objekte/Werte übernehmen, die tatsächlich in der eingefügten HTML bzw. den
  CHECK24-Einschätzungen enthalten sind
- **Reihenfolge einhalten:** Erst Objekt & Strategie klären → dann Suchparameter ausgeben → erst nach Erhalt
  der Daten die Analyse bauen. Nicht vorzeitig eine Analyse ohne echte Vergleichsdaten erstellen.
- **CHECK24 = Einheiten des Zielobjekts, ImmoScout24 = Marktvergleich:** Die CHECK24-Einschätzungen beziehen
  sich immer auf die tatsächlichen Wohneinheiten des Objekts in Akquise (nicht auf eine Musterfläche). Der
  Vergleich erfolgt, indem der CHECK24-Marktwert pro Einheit (€/m²) den marktüblichen €/m²-Preisen aus den
  ImmoScout24-Vergleichsobjekten gegenübergestellt wird — so lässt sich einschätzen, ob die Einheiten über
  oder unter dem Marktniveau bewertet sind.
- **Cirrus-Branding:** Wie bei anderen Cirrus-Skills gilt: keine Fremdmarken-Vorlagen verändern, Dateinamen
  immer objektspezifisch (nie "Vorlage" oder "Comps" alleine ohne Objektbezug im finalen Analyse-Dateinamen).
