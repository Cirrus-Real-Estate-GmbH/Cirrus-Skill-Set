---
name: ausschreibungs-manager
description: >
  Steuert den kompletten Ausschreibungsprozess fuer Bauleistungen: von der
  Handwerker-Recherche bis zum Angebots-Tracking. Trigger diesen Skill immer dann, wenn der
  Nutzer Handwerker, Gewerke oder ausfuehrende Firmen sucht, eine Ausschreibung herausschicken,
  Angebote einholen, vergleichen oder nachverfolgen moechte - auch bei Formulierungen wie
  "Ausschreibung Dachdecker", "Handwerker finden", "Angebotsanfrage rausschicken",
  "Status der Ausschreibung", "Follow-up an die Firmen", "Tagessummary" oder einer reinen
  Gewerk-/Ortsangabe ("Elektriker Berlin Pankow 20 km"). Recherchiert echte Firmenkontakte live
  ueber mehrere Quellen und prueft sie gegen, bevorzugt kleine inhabergefuehrte Betriebe statt
  Ketten, pflegt eine zentrale Google-Tabelle als Gedaechtnis, erstellt und versendet (nur nach
  Freigabe) Angebotsanfragen mit PDF-Anhang ueber Gmail, verwaltet Follow-ups und Summaries und
  legt pro Angebot einen Google-Drive-Ordner an.
---

# Ausschreibungs-Manager fuer Bauleistungen

## Was dieser Skill leistet

Ein operativer Ende-zu-Ende-Prozess fuer Ausschreibungen von Bauleistungen. Er deckt vier
Phasen ab, die der Nutzer einzeln oder am Stueck anstoesst:

1. **Recherche** — qualifizierte, gegengeprueften Firmenkontakte zu einem Gewerk in einer Region finden
2. **Versand** — professionelle Angebotsanfragen mit Ausschreibungs-PDF erstellen und (nach Freigabe) versenden
3. **Nachverfolgung** — Follow-ups bei ausbleibender Reaktion, taegliche Summary, Ordner pro eingegangenem Angebot
4. **Tracking** — eine zentrale Google-Tabelle, die nach JEDER Aktion aktualisiert wird

## Grundprinzip: Die Tracking-Tabelle ist das Gedaechtnis

Claude laeuft nicht im Hintergrund und kann sich nicht selbst zeitgesteuert aufwecken.
Es gibt keine echten Cronjobs. Stattdessen:

- **Jeder Lauf beginnt damit, die Tracking-Tabelle der Ausschreibung vollstaendig zu lesen.**
  Daraus rekonstruiert Claude den kompletten Stand (wer wurde wann angeschrieben, wer hat
  geantwortet, was ist faellig).
- **Jede Aktion wird sofort in die Tabelle zurueckgeschrieben**, bevor die naechste beginnt.
  Wird ein Lauf unterbrochen, ist der Stand trotzdem korrekt.
- "Faellige" Follow-ups und die Tagessummary werden **bei jedem vom Nutzer angestossenen Lauf**
  berechnet (Tage seit Versand aus den Zeitstempeln), nicht automatisch im Hintergrund.

Beim ersten Kontakt in einer Session, in der zeitbasierte Aktionen erwartet werden, kurz
klarstellen: "Ich kann nicht von allein nach 3 Tagen aufwachen — sag mir einfach 'Status'
oder 'Follow-ups raus', dann pruefe ich, was faellig ist."

## Verbundene Quellen & Tools

- **Web-Recherche** (Maps, Suche, Branchenbuecher, MyHammer, Kleinanzeigen u.a.) — fuer die Firmensuche.
- **Google Drive** — Ausschreibungs-PDF lesen, Tracking-Tabelle anlegen/lesen/aktualisieren, Angebots-Ordner anlegen.
- **Gmail** — Angebotsanfragen + Follow-ups als Entwurf erstellen und (nach Freigabe) versenden, Label anlegen, eingegangene Antworten suchen.

Wenn ein Connector im Thread nicht verfuegbar ist: Nutzer kurz hinweisen und mit Uploads /
manueller Eingabe weiterarbeiten, statt abzubrechen.

## Sicherheits- und Freigaberegeln (nicht verhandelbar)

- **Niemals eine E-Mail senden, weiterleiten, labeln oder ein Follow-up verschicken ohne
  ausdrueckliche Freigabe des Nutzers fuer genau diesen Durchlauf.** Immer zuerst die
  vollstaendige Empfaengerliste + die fertige Mail zeigen und auf ein klares "Ja" warten.
- **Keine E-Mail-Adressen, Telefonnummern oder Firmen erfinden.** Wenn eine Adresse nicht
  belegbar ist, bleibt das Feld leer und der Kontakt wird als "Kontakt ungeprueft" markiert.
- Freigabe gilt pro Durchlauf, nicht dauerhaft. Eine Freigabe fuer den Erstversand ist keine
  Freigabe fuer Follow-ups.

## Setup pro Ausschreibung (einmalig, durch den Nutzer)

Empfohlene Drive-Ordnerstruktur, in der Claude arbeitet:

```
[Gewerk] - [Projektkurzname]/
├── Ausschreibung/
│   └── Vorhabensbeschreibung.pdf        (vom Nutzer abgelegt)
├── Tracking/
│   └── (Claude legt hier die Tracking-Tabelle ab)
└── Angebote/
    └── (Claude legt pro Firma mit Angebot einen Unterordner an)
```

Wenn der Nutzer keinen Ordner vorbereitet hat: anbieten, die Struktur anzulegen, sobald der
Pfad / das Gewerk / der Projektname bekannt ist. Den Ausschreibungs-PDF immer aus dem
`Ausschreibung/`-Ordner oder als Upload beziehen.

---

## Phase 1 — Recherche

### Schritt 1.1: Pflicht-Inputs einsammeln (gebuendelt, nicht einzeln)

Drei Angaben werden benoetigt. Was schon in der Nachricht steht, NICHT erneut fragen.
Fehlende per `ask_user_input_v0` mit Buttons abfragen:

- **Gewerk** (z.B. Dachdecker, Elektro, Trockenbau, Maler, Geruestbau)
- **Region**: Ort oder PLZ als Mittelpunkt
- **Umkreis** in km — IMMER abfragen, falls nicht genannt (typische Optionen: 10 / 25 / 50 / 100 km)

Optional, falls vorhanden: gewuenschte Mindestanzahl Kontakte (Default-Ziel: 10-15 qualifizierte Firmen).

### Schritt 1.2: Mehrquellen-Recherche (gruendlich, nicht oberflaechlich)

Nimm dir Zeit. Suche systematisch ueber MEHRERE unabhaengige Quellen und kombiniere sie.
Detaillierte Such-Strategie, Quellenliste und Gegenpruef-Logik stehen in
`references/recherche.md` — diese Datei lesen, bevor die Recherche startet.

Kernregeln:
- **Betriebsgroesse priorisieren:** Bevorzugt kleine, inhabergefuehrte Betriebe, Einzelunternehmer
  und kleine GmbHs. Grosse Unternehmen, Ketten, Filialbetriebe und Konzerne meiden bzw. nur als
  Notnagel aufnehmen, wenn nicht genug kleine Betriebe im Umkreis gefunden werden — und dann klar
  als "gross" markieren. Indikatoren fuer "klein/inhabergefuehrt" stehen in `references/recherche.md`.
- Pro Firma mindestens **Firmenname, Ort und EINE verlaessliche Kontaktmoeglichkeit** (E-Mail bevorzugt).
- **Gegenpruefung:** Jeder Kontakt braucht entweder (a) eine E-Mail/Telefon direkt von der
  Firmen-Website oder einem Impressum, oder (b) Uebereinstimmung aus zwei unabhaengigen Quellen.
  Andernfalls Status "Kontakt ungeprueft".
- Pruefen: Liegt die Firma wirklich im Umkreis? Fuehrt sie das gesuchte Gewerk aus? Existiert
  sie noch (aktuelle Website/Eintraege)?
- Keine Privatpersonen-Kleinanzeigen ohne Gewerbekontext als seriose Firma werten.

### Schritt 1.3: In Tracking-Tabelle ablegen

Die recherchierten Firmen in die Google-Tabelle der Ausschreibung schreiben (Aufbau siehe
unten unter "Tracking-Tabelle"). Existiert noch keine Tabelle, anlegen. Existiert sie schon,
**vergleichen und nur neue Firmen ergaenzen** (keine Duplikate, bestehende Eintraege nicht
ueberschreiben). Dann dem Nutzer eine kompakte Liste zeigen: Name, Ort, Kontakt, Pruef-Status.

---

## Phase 2 — Versand

### Schritt 2.1: Ausschreibungs-PDF & Projektdaten beschaffen

PDF aus dem `Ausschreibung/`-Ordner oder als Upload lesen. Daraus die fuer die Mail noetigen
Eckdaten ziehen: **Gewerk, Projekt-/Objektadresse, ggf. Leistungsumfang in einem Satz,
Abgabefrist falls genannt**. Fehlt die Objektadresse, beim Nutzer erfragen — sie wird im
Betreff gebraucht.

### Schritt 2.2: Gmail-Label anlegen

Pro Ausschreibung ein eigenes Label erstellen, Format: `Ausschreibung [Gewerk] [Projektkurzname]`.
Alle Mails dieser Ausschreibung erhalten dieses Label. (Label anlegen ist eine Aktion — kurz
ankuendigen, aber dafuer ist keine separate Sende-Freigabe noetig.)

### Schritt 2.3: Individuelle Anfrage-Mail erstellen

Vorlage und Tonalitaet stehen in `references/email-vorlagen.md`. Pro Firma:

- **Betreff IMMER individuell:** `Angebotsanfrage [Firmenname] – [Gewerk], [Objektadresse]`
- Anrede personalisiert, professioneller, hoeflicher Ton (Berliner Immobilienbestandshalter/-entwickler).
- Bezug zur Recherche herstellen ("im Rahmen unserer Recherche fuer ... auf Sie gestossen").
- Projekt kurz benennen, auf den PDF-Anhang verweisen, um Angebotsabgabe bitten, Frist nennen falls vorhanden.

### Schritt 2.4: Freigabe einholen, DANN versenden

Dem Nutzer die vollstaendige Empfaengerliste + eine Beispiel-Mail (oder alle, bei kleiner Menge)
zeigen und ausdruecklich fragen: "An diese N Firmen versenden?" Erst nach klarem Ja versenden.

**Anhang-Robustheit (wichtig):** Grosse PDF-Anhaenge ueber Gmail-Tools koennen still
abgeschnitten/korrumpiert werden. Nach dem Senden/Erstellen jeder Mail mit Anhang per
`has:attachment`-Suche pruefen, ob der Anhang wirklich dranhaengt. Wenn nicht zuverlaessig
moeglich: Mail als Entwurf mit Hinweis "PDF bitte manuell anhaengen" erstellen statt einen
Versand mit fehlendem Anhang zu riskieren. Den Nutzer ueber den Fallback informieren.

### Schritt 2.5: Tracking sofort aktualisieren

Fuer jede versendete Firma in der Tabelle eintragen: Status "Angefragt", Versanddatum
(heutiges Datum + Uhrzeit), Betreff. **Nach dem Versand sofort schreiben, nicht am Ende.**

---

## Phase 3 — Nachverfolgung (laeuft pro vom Nutzer angestossenem Lauf)

### Schritt 3.1: Stand aus Tabelle rekonstruieren

Tabelle lesen. Fuer jede angefragte Firma: Tage seit Versanddatum berechnen (gegen das heutige
Datum). Eingegangene Antworten via Gmail-Suche (Label + `Angebotsanfrage`/Firmenname) abgleichen
und Status aktualisieren (z.B. "Angebot erhalten", "Absage", "Rueckfrage").

### Schritt 3.2: Faellige Follow-ups

Firmen mit Status "Angefragt" UND >= 3-4 Tagen ohne Reaktion sind follow-up-faellig.
Kurze, freundliche Follow-up-Mail im selben Thread (Reply, Threading beibehalten) vorbereiten
— Vorlage in `references/email-vorlagen.md`. Liste der faelligen Follow-ups zeigen,
**Freigabe einholen**, dann senden, Tabelle aktualisieren (Status "Follow-up gesendet", Datum,
Follow-up-Zaehler +1). Maximal 1 Follow-up pro Firma, sofern der Nutzer nicht mehr wuenscht.

### Schritt 3.3: Angebots-Ordner anlegen

Sobald eine Firma ein Angebot mit Summe abgegeben hat: im `Angebote/`-Ordner einen Unterordner
anlegen, Format: `[Angebotssumme EUR] - [Firmenname]` (z.B. `48750 EUR - Mustermann Dach GmbH`).
Das Angebots-PDF/-Dokument dort ablegen, falls vorhanden. In der Tabelle Angebotssumme +
Ordner-Link eintragen.

### Schritt 3.4: Tagessummary

Auf Anstoss ("Summary", "Tagesbericht") oder am Ende eines Laufs anbieten: eine kompakte
Summary-Mail an den Nutzer (Default-Empfaenger: sp@cirrus-real.de) und auf Nachfrage an weitere
Empfaenger. Inhalt: was heute versendet wurde, was zurueckkam, Gesamtstand (angefragt / offen /
Angebote / Absagen), faellige Follow-ups, naechste Schritte. Format in
`references/email-vorlagen.md`. **Versand der Summary ebenfalls erst nach Freigabe.**

---

## Tracking-Tabelle (zentrales Gedaechtnis)

Eine Google-Tabelle pro Ausschreibung im `Tracking/`-Ordner. Name:
`Tracking [Gewerk] [Projektkurzname]`. Spalten (genau diese, in dieser Reihenfolge):

| Spalte | Inhalt |
|---|---|
| Firma | Firmenname |
| Ort | Ort / PLZ |
| Entfernung_km | grobe Distanz zum Mittelpunkt |
| Gewerk | ausgeschriebenes Gewerk |
| Email | gepruefte E-Mail (leer, wenn ungeprueft) |
| Telefon | falls vorhanden |
| Website | falls vorhanden |
| Quellen | Quellen, aus denen Kontakt belegt ist (z.B. "Website + Maps") |
| Betriebsgroesse | klein / inhabergefuehrt / mittel / gross — Einschaetzung aus der Recherche |
| Pruef_Status | Geprueft / Kontakt ungeprueft |
| Status | Recherchiert / Angefragt / Follow-up gesendet / Angebot erhalten / Absage / Rueckfrage |
| Versanddatum | Datum + Uhrzeit Erstversand |
| Follow_up_Datum | Datum letztes Follow-up |
| Follow_up_Anzahl | Zaehler |
| Betreff | verwendeter Betreff |
| Angebotssumme_EUR | bei Angebot |
| Angebots_Ordner | Drive-Link zum Angebots-Unterordner |
| Letzte_Aktualisierung | Zeitstempel der letzten Aenderung dieser Zeile |
| Notiz | Freitext |

**Regel:** Nach jeder Aktion betroffene Zeilen aktualisieren UND `Letzte_Aktualisierung` setzen.
Bestehende Daten beim erneuten Recherche-Lauf nicht ueberschreiben — nur neue Firmen ergaenzen
und Status fortschreiben.

---

## Einstiegslogik (welche Phase ist gemeint?)

Anhand der Nutzer-Nachricht die richtige Phase waehlen:

- Gewerk + Ort/Umkreis, "finde Handwerker", "recherchiere" → **Phase 1**
- "Anfrage raus", "verschick die Ausschreibung", PDF liegt vor → **Phase 2** (vorher Phase 1 nutzen, falls noch keine Firmen)
- "Status", "Stand", "was ist zurueckgekommen", "Follow-ups", "Summary" → **Phase 3**

Bei reinem "Starte Ausschreibung [Gewerk] [Ort]" der Reihe nach durch 1 → 2 fuehren, mit der
Freigabe-Pause vor dem Versand. Immer zuerst die Tracking-Tabelle suchen — existiert sie,
an den vorhandenen Stand anknuepfen statt neu zu beginnen.

## Qualitaetsstandard (Selbstpruefung vor Abschluss)

- Keine erfundenen Kontaktdaten; jeder "Geprueft"-Kontakt hat belegte Quellen.
- Jede Firma liegt nachweislich im Umkreis und fuehrt das Gewerk aus.
- Schwerpunkt liegt auf kleinen, inhabergefuehrten Betrieben; grosse Betriebe nur zur Auffuellung und als "gross" markiert.
- Betreff jeder Mail folgt exakt dem Format und ist individuell.
- Kein Versand ohne Freigabe; Anhang nach Versand verifiziert.
- Tracking-Tabelle nach jeder Aktion aktuell; keine Duplikate.
- Summary nennt konkrete Zahlen, keine Floskeln.

## Negativregeln

- Nicht raten, wenn Daten fehlen — recherchieren oder Feld leer lassen.
- Keine Telefonnummern/Adressen aus dem Gedaechtnis "rekonstruieren".
- Nicht mehrere Einzelrueckfragen stellen, wenn eine gebuendelte Button-Abfrage reicht.
- Keine Massenmail ohne sichtbare, freigegebene Empfaengerliste.
- Nicht behaupten, im Hintergrund zu laufen oder selbsttaetig nach Tagen zu senden.
