---
name: finanzierungsanfrage-email
description: Erstellt eine bankfertige Finanzierungsanfrage-E-Mail für ein Immobilien-Ankaufsobjekt (Fix & Flip / Aufteiler / Einzelobjekt) im CIRRUS-Stil mit fester Struktur (I. Objektdaten, II. Vorhaben & Finanzierungsbedarf, III. Financials, IV. Weitergehende Details, V. Objektunterlagen). Diesen Skill IMMER nutzen, wenn der Nutzer eine "Finanzierungsanfrage", "Finanzierungsemail", "E-Mail an die Bank", "Bankanfrage", "Ankaufsfinanzierung anfragen" oder ähnliches erstellen möchte – auch wenn nur gesagt wird "formuliere eine E-Mail an Herrn X für die Finanzierung" oder ein Business Case, Datenraum-Link oder Exposé mit Finanzierungsbezug übergeben wird. Der Skill zieht die Zahlen aus dem Business Case (Excel), baut die Objektunterlagenliste aus dem Drive-Datenraum, und liefert auf Wunsch ein formatiertes Google Doc im Drive sowie einen Gmail-Entwurf.
---

# Finanzierungsanfrage-E-Mail (Bank-Pitch für Ankaufsobjekte)

Erstellt eine strukturierte Finanzierungsanfrage an eine Bank/einen Finanzierer für den Ankauf eines Immobilienobjekts. Sprache: Deutsch, formelle Anrede ("Sie"). Der Stil ist sachlich-professionell mit persönlicher Note in Eröffnung und Abschluss.

## Benötigte Inputs (vor dem Schreiben sammeln)

1. **Business Case (Excel)** – die einzige Zahlenquelle. Relevante Blätter typischerweise: `BC - Aufteiler` (Cases), `INPUT_ Stammdaten`, `INPUT_ Objektliste`, `INPUT_ Verkaufsliste`, `INPUT_ Finanzierung`, `INPUT_ Sanierungskosten`. Immer mit `data_only=True` (openpyxl) lesen. NIE Zahlen aus älteren Objektlisten oder aus dem Gedächtnis verwenden – ausschließlich aus der aktuellsten übergebenen Datei.
2. **Datenraum (Google Drive Link oder Screenshot)** – für Abschnitt V. Wenn die Drive-Suche einzelne Dateien nicht listet, den Nutzer um einen Screenshot der Ordneransicht bitten.
3. **Google-Fotos-Link** (Objektaufnahmen), falls vorhanden.
4. **Empfänger** (Name des Bankkontakts + E-Mail) – falls unbekannt, Platzhalter `[Name]` setzen und darauf hinweisen.
5. **Google-Maps-Link** selbst erzeugen: `https://maps.google.com/?q=<Straße+Nr>,+<PLZ>+<Ort>`

## Feste E-Mail-Struktur

### Betreff
`Finanzierungsanfrage – Ankauf <Objekttyp/Portfolio> <Adresse> (<n> WE + <n> TG-Stellplätze)`

### Eröffnung
- Anrede: **"Sehr geehrter Herr/Frau <Name>,"** (nicht "Lieber", außer der Nutzer wünscht es).
- Kurze persönliche Eröffnung mit Tages-/Anlassbezug (z. B. "ich hoffe, Sie haben ein angenehmes Wochenende" oder Dank für einen Termin).
- Überleitung: Vorstellung des Ankaufsobjekts, Verweis auf Anhang/Datenraum.

### I. Objektdaten
Adresse + Maps-Link, dann Kurzbeschreibung (Objekttyp, Anzahl WE, Stellplätze inkl. Aufschlüsselung Standard/Duplex, WEG-Aufteilungsstatus). Danach als Bullets:
- **Kaufpreis gesamt** – IMMER mit Zerlegung in Klammern: EUR/m² vermietete Fläche, EUR/m² leerstehende Fläche, EUR je Stellplatztyp.
- Baujahr
- Wohnfläche (exakter Wert aus dem Business Case, mit Nachkommastelle)
- Vermietungsstand: vermietet (unbefristet?) / leerstehend (m²) mit Hinweis "sofort für Renovierung und Neupositionierung verfügbar"
- Aktuelle Nettokaltmiete IST: EUR/Monat und EUR p.a., Ø EUR/m² – klarstellen, ob Stellplätze enthalten sind
- Regulatorik: "Kein Milieuschutz, kein Sanierungsgebiet, kein Denkmalschutz" (nur wenn zutreffend; sonst korrekt benennen)
- Energieeffizienzklasse
Abschließend Link zum Google-Fotos-Album.

### II. Vorhaben und Finanzierungsbedarf
Erster Satz: Ankauf über welche Gesellschaft (z. B. Cirrus Real Estate GmbH).

**Vorhaben und Vermarktungsansatz:** (Fließtext, 1–2 Absätze)
- Konkrete Wertschöpfungshebel VOR dem Verkauf nennen: z. B. individuelle Mietergespräche mit Zielsteigerung der IST-Mieten (in %), Modernisierung Hausflure, kosmetische Sanierung der Leerstände, teilweiser Fenstertausch.
- Dann Exit: Einzelabverkauf – vermietete Einheiten über Kapitalanlagevertrieb an private Kapitalanleger, Leerstände renoviert an Eigennutzer/Anleger. CAPEX-Budgets für Gemeinschaftseigentum und Sondereigentum nennen. Stellplätze werden parallel mitverkauft.

**Finanzierungsbedarf:** (Fließtext)
- Gesuchte Finanzierung: Art (variabel) + Höhe in EUR + Verwendung ("Kaufpreis zzgl. anteiliger Erwerbsnebenkosten / Sanierungskosten"). KEINE LTC-Angabe, KEINE Zinsannahme nennen – das ist Verhandlungssache.
- Besicherung: erstrangige Grundschuld.
- Rückführung: sukzessive aus Einzelverkäufen, "vereinbarte Rückführung pro m² Wohnfläche".
- Eigenkapital: Betrag nennen, weitere Projektkosten aus Eigenmitteln.

### III. Financials
**WICHTIG – was hier NICHT hinein gehört:** keine Bulletliste mit Gesamtkosten, Projektgewinn oder absoluten Gewinnzahlen je Case, kein Screenshot-Platzhalter. Die Detailzahlen stehen im beigefügten Business Case; die E-Mail liefert nur die Herleitung und eine Robustheitsaussage.

Inhalt (Fließtext):
1. Herleitung der Verkaufspreise: Ankaufsrendite für Erwerber im Base Case (z. B. 3,5 %) → daraus EUR/m² für vermietete Einheiten (inkl. Abgabepreis in Klammern und Garantiemiete in EUR/m²) und EUR/m² für renovierte Leerstände im freien Verkauf (mit konservativer Marktmiete). Stellplätze separat zu marktüblichen Preisen.
2. Robustheitsaussage relativ formuliert: "Selbst im Worst-Case-Szenario (Abschlag von rund X % auf die Verkaufserlöse) verbleibt eine komfortable Marge von über Y % auf die Gesamtkosten."
3. Hinweis auf die Anlagen: Business Case als Excel sowie – falls vorhanden – interaktives HTML-Dashboard (Cases + Slider im Browser), mit einem kurzen erklärenden Satz.

### IV. Weitergehende Details
Drei Unterabschnitte, jeweils Bullets:
1. **Objektzustand** – Bausubstanz, WEG-Aufteilung/Grundbücher/Abgeschlossenheit, Vermietungsquote als Cashflow-Argument, Leerstands-Potential ("Renovierung und freihändiger Verkauf"), Energieausweis-Status mit Modernisierungsperspektive, Tiefgarage als Werttreiber.
2. **Lage** – Bezirk/Kiez, ÖPNV, Nahversorgung/Naherholung, ein Satz zur Marktnachfrage im Segment als Vertriebsargument.
3. **Sanierung** – Maßnahmen mit Budgets (Gemeinschaftseigentum inkl. konkreter Gewerke, Sondereigentum), plus professionelle Vermarktungsaufbereitung/Objektfotografie.

### V. Objektunterlagen
- Einleitungssatz + Link zum Datenraum (Google Drive).
- **Dokumente:** durchnummerierte Liste exakt nach Datenraum-Benennung (0 – Business Case, 1 – Objektliste, …). Nummerierung auf Lücken/Dubletten prüfen und ggf. den Nutzer hinweisen.
- **Ordner:** separate Liste der Unterordner.

### Abschluss
- "Für Rückfragen stehe ich Ihnen jederzeit gerne zur Verfügung."
- Bitte um **erste Einschätzung** (nicht "Feedback zur Finanzierungsbegleitung").
- Tageswunsch passend zum Versanddatum (z. B. "…und wünsche Ihnen noch einen schönen Sonntag.").
- Grußformel: "Mit besten Grüßen" + Name (+ Gesellschaft).

## Stil- und Formatierungsregeln

- Abschnittsüberschriften (I.–V.) und Zwischenüberschriften **fett**; Aufzählungen als Bullets; Fließtext für Vorhaben, Finanzierungsbedarf und Financials.
- Links klickbar einbetten (Maps, Fotoalbum, Datenraum).
- Zahlenformat deutsch: 2.300.000 EUR, 9,18 EUR/m², "ca." bei gerundeten Werten.
- Konservative, faktenbasierte Tonalität – Superlative vermeiden, Risiken nicht verschweigen aber auch nicht dramatisieren (Datenraum enthält die Unterlagen, z. B. Altlastenauskunft).
- Keine internen Kennzahlen, die Verhandlungsspielraum offenlegen (Projektgewinn absolut, Marge je Case, LTC, Zinsannahme).

## Delivery-Workflow

1. Entwurf zuerst als Klartext im Chat zeigen (Review-Schleife des Nutzers).
2. Auf Wunsch **Google Doc** im Drive ablegen: `Google Drive:create_file` mit `contentMimeType: text/html` (konvertiert automatisch zu einem formatierten Doc). Titel: `0 - <Objekt> - Entwurf Finanzierungs-E-Mail (Ankaufsfinanzierung)`. Hinweis geben, falls der Zielordner mit Externen geteilt ist.
3. Auf Wunsch **Gmail-Entwurf**: `Gmail:create_draft` mit `htmlBody` (gleiches HTML). Gmail verlangt einen Empfänger – falls unbekannt, die eigene Adresse des Nutzers als Platzhalter eintragen und explizit darauf hinweisen, dass sie ersetzt werden muss.
4. Immer abschließend die offenen Platzhalter auflisten ([Name], Empfängeradresse, ggf. Anhänge wie Excel/Dashboard, die manuell angehängt werden müssen).
