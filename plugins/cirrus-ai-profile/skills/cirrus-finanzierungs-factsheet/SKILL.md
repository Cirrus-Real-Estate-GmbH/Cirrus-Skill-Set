---
name: cirrus-finanzierungs-factsheet
description: Erzeugt ein bankfähiges CIRRUS-Finanzierungs-Factsheet (One-Pager-PDF, A4 quer) für ein Immobilien-Aufteilungsprojekt. Nutze diesen Skill immer, wenn der Nutzer aus einem Projekt-Dashboard, einer Mieter-/Einheitenliste, einem Exposé oder Energieausweisen eine Finanzierungs-PDF, ein Finanzierungs-Factsheet, ein Banker-One-Pager oder eine Endkunden-Finanzierungseinschätzung machen möchte — auch wenn nur Begriffe wie „Factsheet für die Bank", „Finanzierungsübersicht", „aufgeteilte Einheiten finanzierbar", „Kaufpreisliste je Einheit" oder „Endkundenrendite" fallen. Der Skill rechnet Verkaufspreis ↔ Kalkulationsmiete über die Endkundenrendite um, baut eine Einheitentabelle mit Kaufpreisen und optional ein Energieausweis-Panel, im CIRRUS-Branding (Logo, Poppins, #00407B). Er gibt NIEMALS Einkaufspreis, Sanierungsbudget, Vertriebskosten oder Marge aus.
---

# CIRRUS Finanzierungs-Factsheet

Zweck: Aus Projektdaten (Dashboard/Exposé/Mieterliste + optional Energieausweise) einen
einseitigen, bankfähigen Finanzierungs-One-Pager erzeugen. Adressat ist ein Finanzierer /
Bankberater, der einschätzen soll, ob die **Einheiten im aufgeteilten (WEG-)Zustand für
Endkunden finanzierbar** sind. Es geht um die Endkundenfinanzierung, nicht um die
Objektfinanzierung von CIRRUS.

## Eiserne Regel: keine internen Zahlen

Das Factsheet enthält **ausschließlich endkundenrelevante Daten**. Niemals aufnehmen — auch
nicht abgeleitet oder rückrechenbar:

- Einkaufspreis / Ankaufspreis von CIRRUS
- Sanierungs-/CapEx-Budget, Baukosten
- Vertriebs-/Maklerprovision, garantierte Mieten an Vertriebspartner
- Marge, Gewinn, IRR des Projekts
- Ist-Mieten, wenn daraus die aktuelle Rendite/Einkauf rückrechenbar wäre (nur die
  **Kalkulationsmiete** ausweisen, klar als „nach Mietanpassung/Neuvermietung" gekennzeichnet)

Wenn der Nutzer explizit interne Zahlen aufs Factsheet setzen will, kurz nachfragen und auf den
Zweck (Bankvorlage) hinweisen, bevor du es tust.

## Kern-Rechenlogik

Zwei Basisannahmen steuern alles: **Endkundenrendite** (%) und entweder **Verkaufspreis**
(€/m²) oder **Kalkulationsmiete** (€/m²·Monat). Die jeweils fehlende Größe wird zurückgerechnet:

```
Kalkulationsmiete €/m²·Monat = Verkaufspreis €/m² × Rendite / 12
Verkaufspreis €/m²           = Kalkulationsmiete €/m²·Monat × 12 / Rendite
```

Beispiel: 1.160 €/m² × 7,0 % / 12 = **6,77 €/m²·Monat**.

Je Einheit: `Kaufpreis = Fläche × Verkaufspreis`, `NKM/Monat = Fläche × Kalkulationsmiete`.
Die Summenzeile aggregiert Fläche, Kaufpreisvolumen und JNKM.

## Workflow

1. **Projektdaten sammeln.** Woher kommen die Einheiten (Fläche je WE, Adresse, Baujahr)?
   Meist aus einem hochgeladenen Dashboard (HTML), Exposé (PDF) oder einer Mieterliste. Lies
   die Datei und extrahiere je Einheit mindestens die **Wohnfläche**; WE-Nummer, Adresse und
   Baujahr wenn vorhanden. Bei HTML-Dashboards stecken die Daten oft im `<script>`-Block —
   dort nachsehen, nicht nur im sichtbaren Text.

2. **Annahmen klären.** Endkundenrendite und Verkaufspreis (oder Miete) beim Nutzer erfragen,
   falls nicht genannt. Häufig gibt der Nutzer den Preis vor (z. B. „1.160 €/m², 7 %") — dann
   Miete zurückrechnen.

3. **Energieausweise (optional).** Wenn Energieausweis-PDFs vorliegen, je Gebäude den
   Endenergie-Kennwert (Pflichtangabe für Immobilienanzeigen), die Effizienzklasse, die
   Ausweisart (Bedarf/Verbrauch), den Energieträger und das Baujahr des Wärmeerzeugers
   entnehmen. Diese Werte kommen ins optionale Energie-Panel. **Bedarfs- vs.
   Verbrauchsausweis** unbedingt korrekt kennzeichnen — der Endenergiewert steht bei
   Bedarfsausweisen auf Seite 2, bei Verbrauchsausweisen auf Seite 3.

4. **Config bauen.** Fülle eine JSON-Konfiguration nach dem Schema in
   `references/config_schema.md`. Als Vorlage dient `assets/example_config_thoeringswerder.json`.

5. **PDF generieren.**
   ```bash
   python3 scripts/build_factsheet.py <config.json> <output.pdf>
   ```
   Das Standard-Logo (`assets/CIRRUS_LOGO_BLUE.jpg`) wird automatisch verwendet; mit
   `--logo <pfad>` überschreibbar. Das Skript gibt die berechneten Eckwerte aus (Fläche,
   Preis, Miete, KP gesamt, JNKM) — kurz gegen die Erwartung prüfen.

6. **Prüfen.** Das Skript hat eingebaute `assert`-Checks, die abbrechen, wenn Text aus einem
   Panel oder der Seite läuft. Zusätzlich das PDF rendern (`pdftoppm -png -r 110`) und
   optisch kontrollieren. Für eine harte Kollisionsprüfung siehe
   `references/layout_notes.md` (pdfplumber-Snippet).

7. **Ausliefern.** Finale PDF in den Output-Ordner kopieren und mit `present_files` teilen.
   Dateiname-Konvention: `CIRRUS_Finanzierungs-Factsheet_<Projekt>_<Ort>.pdf`.

## Layout (fix, nicht neu erfinden)

Der One-Pager ist A4 quer und hat immer denselben Aufbau — das Skript erzeugt ihn; du musst
nur die Config befüllen:

- **Kopf:** Logo links, zweizeiliger Titel (Titel + Objekt-Kurzbezeichnung + Tagline),
  Firmen-/Stand-Block rechts.
- **KPI-Leiste:** 5 Kacheln — Objekt · Verkaufspreis · Endkundenrendite · Kalkulationsmiete ·
  Standort. Verkaufspreis und Rendite sind blau hervorgehoben.
- **Links:** Panels „Objekt & Lage", „Zustand & Energie" (optional), „Anlass dieser Anfrage".
- **Rechts:** Einheitentabelle mit Summenzeile; darunter optional „Energieausweise je Gebäude".
- **Fuß:** Firma, Ansprechpartner, Haftungshinweis, blauer Balken.

Design-Tokens: Blau `#00407B`, Dunkel `#273349`, Grau `#B9BCC1`, Schrift **Poppins**
(Regular/Medium/Bold). Details in `references/layout_notes.md`.

## Wichtige Hinweise

- **Garagen/Stellplätze:** klären, ob sie in den Kaufpreisen enthalten oder separat sind — das
  gehört in die Tabellen-Fußnote und den Anlass-Text, weil es die ausgewiesene Rendite berührt.
- **Energieklassen ehrlich zeigen:** Schlechte Klassen (F–H) nicht verstecken — sie sind für die
  Beleihung relevant. Der geplante Ertüchtigungs-Hinweis ordnet sie ein.
- **Zahlen doppelt prüfen:** Die Kalkulationsmiete/den Preis nach der Rückrechnung gegen die
  Nutzervorgabe checken (Skript-Ausgabe nutzen).
- **Bei sehr vielen Einheiten (>~30)** in der Config `"gruppierung": "auto"` setzen — dann
  aggregiert das Skript nach Gebäude/Adresse (Spalte „Anzahl", z. B. „8×"), und das Portfolio
  bleibt auf einer Seite lesbar. Ohne Gruppierung bricht das Skript bei Überlauf bewusst mit
  einem Assert ab (kein stilles Überlappen). Details in `references/config_schema.md`.

## Ressourcen

- `scripts/build_factsheet.py` — Generator (Config-JSON → PDF). Selbst-validierend.
- `references/config_schema.md` — vollständiges Feld-für-Feld-Schema der Config.
- `references/layout_notes.md` — Layout-Tokens, Anpass-Stellen, Prüf-Snippets.
- `assets/example_config_thoeringswerder.json` — vollständige Beispielkonfig (22 WE, mit Energie).
- `assets/CIRRUS_LOGO_BLUE.jpg` — Standard-Logo.
