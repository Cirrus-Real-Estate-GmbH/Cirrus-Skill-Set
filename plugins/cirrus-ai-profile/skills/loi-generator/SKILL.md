---
name: loi-generator
description: >
  Erstelle einen immobilienspezifischen Letter of Intent (LOI / Interessenbekundung) auf Deutsch für Cirrus Real Estate GmbH.
  Trigger diesen Skill immer dann, wenn der Nutzer ein LOI, Letter of Intent, eine Interessenbekundung oder Angebotsschreiben
  für eine Immobilie erstellen möchte — auch wenn nur Begriffe wie "LOI schreiben", "Angebot rausschicken",
  "Interesse bekunden" oder eine Immobilien-/Objektbezeichnung genannt werden.
  Der Skill sucht das Exposé automatisch (Upload, Google Drive oder Gmail), holt die LOI-Vorlage aus Drive,
  passt sie objektspezifisch an und gibt ein fertiges PDF sowie DOCX aus.
---

# LOI-Generator für Cirrus Real Estate GmbH

## Überblick

Dieser Skill erstellt einen vollständig ausgefüllten, immobilienspezifischen Letter of Intent (LOI) als DOCX und PDF.

**Ablauf:**
1. Exposé-Quelle ermitteln → Infos extrahieren
2. LOI-Vorlage aus Drive holen (oder hochgeladene verwenden)
3. LOI objektspezifisch befüllen (Titel, Datum, Makler, Kaufpreis etc.)
4. DOCX + PDF ausgeben

---

## Schritt 1: Exposé beschaffen

Es gibt drei Quellen. Prüfe in dieser Reihenfolge:

### A) Datei direkt hochgeladen
Wenn der Nutzer eine Datei mitgegeben hat (PDF, DOCX, etc.) → sofort einlesen und mit Schritt 2 fortfahren.

### B) Exposé liegt in Google Drive
Drive-Ordner des Nutzers: `https://drive.google.com/drive/folders/0AMak0p1_5T5XUk9PVA`

```
Suche in Google Drive nach dem Objektnamen oder der Adresse.
Lade die Datei herunter und lies den Inhalt.
```

Nutze das Google Drive MCP:
```javascript
// mcp_servers: [{ type: "url", url: "https://drivemcp.googleapis.com/mcp/v1", name: "google-drive-mcp" }]
// Tool: search_files mit query = Objektname/Adresse
// Dann: read_file_content mit der gefundenen file_id
```

### C) Exposé per Gmail vom Makler
Wenn kein Exposé hochgeladen und nichts im Drive gefunden → Gmail durchsuchen:

```javascript
// mcp_servers: [{ type: "url", url: "https://gmailmcp.googleapis.com/mcp/v1", name: "gmail-mcp" }]
// Tool: search_threads mit query = Objektname + "exposé" ODER Makler-Name
// Anhänge aus relevanten Threads herunterladen und einlesen
```

**Falls gar kein Exposé gefunden wird:** Den Nutzer direkt fragen, welche Infos fehlen (Kaufpreis, Adresse, Einheiten, Fläche, Jahresnettokaltmiete).

---

## Schritt 2: LOI-Vorlage beschaffen

### Priorität 1: Vorlage hochgeladen
Wenn der Nutzer selbst eine Vorlage mitgegeben hat → diese verwenden.

### Priorität 2: Vorlage aus Google Drive
Drive-Ordner für LOI-Vorlagen: `https://drive.google.com/drive/folders/18R_VAohMrVGlual3zEnCr61nTeQc12P8`

```javascript
// Tool: search_files mit query = "LOI" oder "Letter of Intent"
// Datei herunterladen → als Basis verwenden
```

### Priorität 3: Eingebettete Vorlage (Fallback)
Wenn Drive nicht erreichbar → Vorlage aus `assets/LOI_Vorlage.docx` in diesem Skill-Verzeichnis verwenden.

---

## Schritt 3: Fehlende Infos vom Nutzer erfragen

Bevor du den LOI befüllst, prüfe ob folgende Pflichtfelder bekannt sind.
**Frage nur nach, was du NICHT aus dem Exposé ableiten konntest:**

| Feld | Quelle | Pflicht? |
|------|--------|----------|
| Objektbezeichnung / Portfolioname | Exposé | ✅ |
| Adresse / Standort(e) | Exposé | ✅ |
| Anzahl Wohn- und Gewerbeeinheiten | Exposé | ✅ |
| Wohnfläche (m²) | Exposé | ✅ |
| Jahresnettokaltmiete (€) | Exposé | ✅ |
| Kaufpreisangebot (Bandbreite oder Festpreis) | Nutzer | ✅ |
| Makler-Name & Firma | Exposé oder Nutzer | ✅ |
| Makler-Adresse (Straße, PLZ, Ort) | Exposé oder Nutzer | ✅ |
| Beurkundungsdatum | Automatisch: heute + 1 Monat (gleicher Tag) | ✅ |
| Zusätzliche Wunschinhalte | Nutzer (optional) | ⚪ |

Stelle alle fehlenden Pflichtfelder in einer einzigen kompakten Nachricht ab.

---

## Schritt 4: LOI befüllen und erstellen

### Vorlage bearbeiten (Unpack → XML editieren → Pack)

Folge dem DOCX-Skill-Workflow:
```bash
python /mnt/skills/public/docx/scripts/office/unpack.py LOI_Vorlage.docx unpacked/
# XML in unpacked/word/document.xml editieren
python /mnt/skills/public/docx/scripts/office/pack.py unpacked/ LOI_[Objektname]_[Datum].docx --original LOI_Vorlage.docx
```

### Zu ändernde Felder in der Vorlage

| Platzhalter / Bereich | Ersetzen durch |
|----------------------|----------------|
| `[Empfänger]` | Makler-Name (Vorname Nachname) |
| `[Unternehmen]` | Makler-Firma |
| `[Straße]` | Makler-Straße |
| `[Postleitzahl Stadt]` | Makler-PLZ und Ort |
| `Portfolio Solum` (in Überschrift) | Aktueller Portfolioname / Objektbezeichnung |
| `22. Juni 2026` (Datum oben) | Heutiges Datum (ausgeschrieben) |
| Beschreibungstext Objekt | Objektspezifisch aus Exposé (Standorte, WE, GE) |
| Kaufpreisspanne / -betrag | Vom Nutzer angegeben |
| Kaufpreis in Worten | Automatisch ausschreiben |
| Wohneinheiten, Wohnfläche, JNKM | Aus Exposé |
| Beurkundungsdatum | Automatisch berechnen: heutiges Datum + 1 Monat (gleicher Kalendertag), ausgeschrieben auf Deutsch (z.B. „25. Juli 2026") |
| `Berlin, den 22. Mai 2026` | `Berlin, den [heutiges Datum]` |

### Zusätzliche Inhalte
Falls der Nutzer Sonderwünsche hat (z.B. bestimmte Finanzierungshinweise, Klauseln, Ergänzungen) → diese in den passenden Abschnitt einarbeiten.

---

## Schritt 5: Als PDF exportieren

```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf LOI_[Objektname].docx
```

---

## Schritt 6: Ausgabe

1. **DOCX** als Download bereitstellen (Dateiname: `LOI_[Objektname]_[JJJJ-MM-TT].docx`)
2. **PDF** als Download bereitstellen (Dateiname: `LOI_[Objektname]_[JJJJ-MM-TT].pdf`)
3. Kurze Zusammenfassung im Chat: welche Felder befüllt wurden, welche ggf. noch zu prüfen sind.

---

## Wichtige Hinweise

- **Sprache:** Immer Deutsch
- **Absender:** Immer Cirrus Real Estate GmbH, Rathausgasse 17, 12529 Schönefeld
- **Unterzeichner:** Jan Philipp Wesemann (Geschäftsführer), Conrad Bloser (Inhaber/Kontakt)
- **Kaufpreis in Worten:** Immer ausschreiben (z.B. „achtzehnmillionzweihunderttausend Euro")
- **Datum:** Heutiges Datum verwenden, nicht das Datum aus der Vorlage
- **Beurkundungsdatum:** Immer automatisch auf heutiges Datum + 1 Monat (gleicher Kalendertag) setzen. Beispiel: Erstellung am 25. Juni 2026 → Beurkundungsdatum 25. Juli 2026. Kein Rückfragen beim Nutzer erforderlich.
- **Finanzierungsvorbehalt:** Standardmäßig KEIN Finanzierungsvorbehalt (Eigenfinanzierung durch Cirrus)
- **Dateiname:** Immer objektspezifisch benennen, nie „LOI_Vorlage" o.ä.
