---
name: teaser-kapitalanlagevertrieb
description: >
  Erstellt deutschsprachige CIRRUS-Vorhabenbeschreibungen und Vertriebs-Teaser
  fuer Kapitalanlagevertriebe als PDF, entweder als kurze One-Pager-/Factsheet-
  Version oder als lange mehrseitige Objekt- und Vorhabenbeschreibung. Nutze
  diesen Skill, wenn der Nutzer ein PDF fuer Kapitalanlagevertriebe,
  Vertriebspartner, Investorenvertriebe, Projekt-Memos, Vorhabenbeschreibungen,
  Verkaufs-Factsheets, One-Pager, Mehr-Pager oder eine Interessenspruefung fuer
  ein Immobilienprojekt erstellen oder ueberarbeiten moechte.
---

# Teaser Kapitalanlagevertrieb

Erstelle eine professionelle CIRRUS-Unterlage, mit der Kapitalanlagevertriebe schnell pruefen koennen, ob ein Immobilienprojekt fuer ihren Vertrieb interessant ist.

## Startabfrage

Wenn der Nutzer noch keine Variante eindeutig vorgibt, frage zuerst nach der gewuenschten Ausgabe:

- **Kurzversion:** One-Pager / kompaktes Vertriebs-Factsheet, A4 quer, PDF.
- **Langversion:** mehrseitige Objekt- und Vorhabenbeschreibung / Projekt-Memo, A4 hoch, PDF.

Frage danach nur die Informationen ab, die fuer die gewaehlte Variante fehlen. Erfinde keine belastbaren Zahlen, Links, Ansprechpartnerdaten oder rechtlichen Aussagen.

## Quellen

Nutze vorhandene Uploads, Projektunterlagen, Business-Case-Dateien, Exposes, Mietlisten, Objektlisten, Bilder, Grundrisse und Chat-Angaben. Wenn mehrere Quellen widersprechen, nenne den Widerspruch kurz und frage nach dem belastbaren Wert, sofern er fuer die PDF wesentlich ist.

Lies bei der Bearbeitung je nach Bedarf:

- `references/format-und-inhalt.md` fuer Aufbau, Pflichtfelder, Stil und Variantenlogik.
- `references/verkaufslogik.md` fuer Mietstory, Preisbildung, Provision und Rendite.
- `assets/short_factsheet_template.html` als HTML-Vorlage fuer die Kurzversion (enthaelt bereits das eingebettete CIRRUS-Logo).
- `assets/examples/short-version-am-sandhaus-4.pdf` als Beispiel fuer die Kurzversion (falls im Repo vorhanden).

Hinweis: Die Langversions-Beispiel-PDF ist bewusst nicht im Repo (Dateigroesse). Bei Bedarf im Cirrus Drive unter "03 Skills" nachschauen.

## Pflichtinformationen

Pruefe immer, ob folgende Angaben vorhanden sind:

- Objektadresse, Objektname, Ortsteil/Standort und Objektart.
- Anzahl Einheiten, Wohnflaeche, Zimmer-/Wohnungstypen, Baujahr/Modernisierung.
- Vermietungsstand, IST-Miete, SOLL-Miete oder Zielmiete, Jahresnettokaltmiete.
- Verkaufsmodell: Einzelverkauf, WEG-Aufteilung, Kapitalanlagevertrieb, Buy-and-hold oder sonstige Strategie.
- Endkundenpreis, Abgabepreis, Provision, Rendite oder die Parameter, aus denen diese berechnet werden.
- geplante Massnahmen vor Verkauf, Aufteilungs-/Genehmigungsstand, Zeitplan/Vermarktungsstart.
- Ansprechpartner, Kontaktdaten, Foto-/Unterlagenlinks und Vertraulichkeitshinweis.

Bei der Kurzversion darf die Unterlage mit weniger Details arbeiten, aber die Kernzahlen und die Verkaufsstory muessen nachvollziehbar sein. Bei der Langversion muessen fehlende Kapitelinformationen aktiv abgefragt oder klar als offen markiert werden.

## Kurzversion

Nutze die Kurzversion fuer schnelle Interessenspruefung, Erstansprache und Vertriebspartner-Screening.

Arbeite bevorzugt mit `assets/short_factsheet_template.html`: kopiere die Datei an einen beschreibbaren Ort, ersetze Inhalte und rendere sie mit `scripts/render_pdf.py`.

Ziel: eine Seite, maximal zwei Seiten, A4 quer. Enthalten sein muessen:

- CIRRUS-Logo, Objekttitel und Untertitel.
- Eckdaten-Strip mit Einheiten, Wohnflaeche, Baujahr, Grundstueck, Zielmiete/Garantiemiete und Rendite.
- Block "Objekt & Lage" mit Adresse, Google-Maps-Link, Zustand, Lagetext und Standort-Tags.
- Block "Mietstory" von IST-Miete ueber SOLL-/Garantiemiete zur Verkaufsrendite.
- Preisboxen fuer Endkundenpreis, Provision und Abgabepreis.
- Einheiten-/Mietuebersicht und Verkaufspreisliste, wenn Einzeldaten vorhanden sind.
- Footer mit CIRRUS-Adresse und Unverbindlichkeitshinweis.

Wenn die Kurzversion ueberlaeuft, verdichte Layout, Tabellen und Text, ohne Pflichtzahlen zu entfernen.

## Langversion

Nutze die Langversion fuer substanzielle Projektvorstellung, interne/extern abgestimmte Vorhabenbeschreibung und groessere Objekte.

Ziel: strukturierte mehrseitige PDF im Stil einer vertraulichen Objekt- und Vorhabenbeschreibung.

Standardgliederung:

1. Deckblatt mit `VERTRAULICH`, Projekttitel, Objektadresse, Claim und CIRRUS-Adresse.
2. Eckdatenseite mit Datum, Eigentuemer, Ansprechpartner, Objekt, Vermarktungsstart, Foto-/Unterlagenlinks.
3. Inhaltsverzeichnis.
4. Management Summary.
5. Objektbeschreibung.
6. Lagebeschreibung.
7. Wirtschaftliche Kennzahlen.
8. Geplante Sanierungs- oder Aufwertungsmassnahmen vor Verkauf.
9. Vorhaben und Vermarktungsansatz.
10. Visualisierungen, Fotos, Karten oder Platzhalter, falls Bilder fehlen.

Wenn Bilder, Karten oder Links fehlen, danach fragen bzw. klar als offen markieren statt zu erfinden.

## PDF-Erzeugung

`scripts/render_pdf.py` rendert eine HTML-Datei zu PDF. `scripts/embed_logo.py` bettet das CIRRUS-Logo als Base64 in eine HTML-Vorlage ein, falls eine neue Vorlage ohne eingebettetes Logo erstellt wird.

## Wichtig

- Niemals interne CIRRUS-Zahlen (Einkaufspreis, Marge) in eine fuer den Kapitalanlagevertrieb bestimmte Unterlage schreiben, sofern nicht ausdruecklich gewuenscht.
- Immer Unverbindlichkeits-/Vertraulichkeitshinweis im Footer/Deckblatt.
