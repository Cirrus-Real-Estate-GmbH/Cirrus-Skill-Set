---
name: team-weekly-summary
description: Erstellt eine WhatsApp-optimierte Team Weekly Summary aus Gmail und Google Kalender der vergangenen Woche. Diesen Skill immer nutzen, wenn der Nutzer eine "Weekly Summary", ein "Wochenupdate", eine "Team-Nachricht zur Woche", ein "Weekly fürs Team", einen "Wochenrückblick" oder ähnliches erstellen möchte – auch wenn nur gesagt wird "fass die Woche fürs Team zusammen" oder "schick mir das Weekly". Der Skill sammelt automatisch alle relevanten Ereignisse aus E-Mails und Kalender, fragt VOR dem Entwurf nach eigenen Fokuspunkten des Nutzers, und liefert das Ergebnis immer als kopierbaren Text plus danach als separate Nachricht einen WhatsApp-Link, der die komplette Summary über die WhatsApp-API-Linkstruktur enthält.
---

# Team Weekly Summary

Erstellt eine wöchentliche Team-Zusammenfassung (WhatsApp-Format, Deutsch, mit Emojis) aus Gmail, Google Kalender und eigenen Fokuspunkten des Nutzers.

## Workflow (Schritte strikt in dieser Reihenfolge)

### Schritt 1: Zeitraum bestimmen

- Standard: Montag bis Freitag der aktuellen Woche (bzw. seit der letzten Weekly Summary, meist letzter Freitag/Samstag).
- Kalenderwoche (KW) für die Überschrift berechnen.
- Nur bei Unklarheit nachfragen.

### Schritt 2: Daten sammeln (Gmail + Google Kalender)

**Gmail:**
- `Gmail:search_threads` mit `query: "after:YYYY/MM/DD"` (Startdatum des Zeitraums), `pageSize: 50`.
- **Wichtig: Alle Seiten durchpaginieren** (`pageToken`), bis der gesamte Zeitraum abgedeckt ist – eine aktive Woche hat oft 150–250 Threads. Nicht nach der ersten Seite aufhören.
- Relevante Themen extrahieren: Objekte/Deals (Angebote, LOIs, Datenräume, Due Diligence, Kaufverträge, Notartermine), Finanzierungen (Banken, Zusagen, Konditionen), Kapitalgeber-Kontakte, Besichtigungen, Operations (Verwaltung, Handwerker, Personal, Office), Buchhaltung/Jahresabschlüsse, Team-Themen.

**Google Kalender:**
- Zuerst `tool_search` nach "Google Calendar list events", dann `Google Calendar:list_events` mit `startTime`/`endTime` des Zeitraums, `orderBy: startTime`, `pageSize: 100`.
- Falls ein lokales Kalender-Tool (z.B. `event_search_v0`) fehlschlägt oder Zugriff verweigert: immer auf Google Calendar ausweichen.
- Termine liefern: Besichtigungen, Gespräche mit Kapitalgebern/Banken, Team-Events, Notartermine, wichtige Meetings.

### Schritt 3: PFLICHT – Eigene Fokuspunkte abfragen (VOR dem Entwurf)

Bevor der Entwurf geschrieben wird, den Nutzer **immer** fragen:

> "Ich habe E-Mails und Kalender der Woche durch. Möchtest du noch eigene Fokuspunkte setzen, bevor ich den Entwurf schreibe? Z.B. Highlights, Dankeschöns ans Team, Dinge die nicht in den E-Mails stehen – gerne auch einfach als Sprachnachricht/Diktat reinsprechen."

- Dabei kurz (3–5 Stichpunkte) nennen, welche Hauptthemen bereits gefunden wurden, damit der Nutzer weiß, was schon abgedeckt ist.
- Auf die Antwort warten. Erst danach den Entwurf schreiben.
- Vom Nutzer genannte Punkte haben Vorrang und gehören prominent in die Summary (Highlight-Sektion, Danksagungen).

**Hinweis Diktat:** Der Nutzer diktiert oft per Voice (Wispr Flow). Mit Erkennungsfehlern rechnen, besonders bei Straßen-/Eigennamen. Unklare Namen anhand von E-Mail-/Kalenderdaten plausibilisieren und die Interpretation transparent machen ("Ich habe X als Y interpretiert – sag Bescheid, falls falsch").

### Schritt 4: Entwurf schreiben und zur Durchsicht geben

Format: WhatsApp-optimiert, Deutsch, Emojis, `*Sternchen*` für Fettdruck (WhatsApp-Syntax, kein Markdown-`**`).

Bewährte Struktur (Sektionen bei Bedarf anpassen/weglassen):

```
📢 *Weekly Summary – KW__* (TT.MM.–TT.MM.)

Hi zusammen, hier das Update der Woche! 💪

🏆 *Highlight der Woche*
[Das wichtigste Ereignis – meist vom Nutzer genannt]

🎯 *[Fokus-Deal/-Objekt]*
▪️ [Meilensteine: Angebot, DD, Kaufvertrag, Termine...]

🔍 *Besichtigungen & neue Objekte*
▪️ [Besichtigt / in Analyse / LOIs]

💶 *Kapitalgeber & Finanzierung*
▪️ [Gespräche, Zusagen, Vorprüfungen]

🏗️ *Projekte & Operations*
▪️ [Laufende Projekte, Office, Personal, Buchhaltung]
▪️ [Danksagungen an Teammitglieder namentlich! 👏]

🎉 *Team-Event / Team*
[Falls vorhanden]

Habt ein starkes Wochenende! 🚀
[Name/Kürzel des Nutzers]
```

Stilregeln:
- Positiv, energiegeladen, motivierend – es ist eine Team-Nachricht.
- Teammitglieder bei guten Leistungen **namentlich** loben.
- Konkrete Zahlen nennen (Kaufpreise, Einheiten, Profit), sofern der Nutzer sie freigegeben/genannt hat.
- Kompakt: pro Bullet eine Zeile, keine Romane.

Den Entwurf zunächst als normalen Text im Chat zeigen und Feedback abwarten. Feedback einarbeiten, ggf. mehrere Runden.

### Schritt 5: Finale Ausgabe – IMMER Summary und danach separaten WhatsApp-Link liefern

Sobald der Nutzer zufrieden ist, **immer zwei Chat-Nachrichten in dieser Reihenfolge** liefern:

**Nachricht 1 – Kopierbarer Text (primär, funktioniert immer):**
`message_compose_v1` mit `kind: "other"` aufrufen – rendert einen Kopieren-Button. Den finalen Text unverändert als eine Variante übergeben. In dieser Nachricht keinen WhatsApp-Link und keine Zusatznotizen anhängen.

**Nachricht 2 – WhatsApp-Link separat:**
Direkt nach der ursprünglichen Summary eine eigene separate Chat-Nachricht senden, die nur den WhatsApp-Link enthält. Der Link muss die komplette finale Summary enthalten, damit der Nutzer nur den Link klicken und danach in WhatsApp den gewünschten Chat auswählen muss.

Den Link über die WhatsApp-API-Linkstruktur mit leerem Empfänger und `text`-Parameter bauen:

```python
import urllib.parse
print("https://api.whatsapp.com/send?text=" + urllib.parse.quote(text))
```

`text` ist exakt der finale WhatsApp-Text aus Nachricht 1, inklusive Überschrift, Emojis, Zeilenumbrüchen und Signatur. Den Text immer per Python URL-encoden, nie von Hand. Den Link als klickbaren Markdown-Link ausgeben, z.B. `[In WhatsApp öffnen](https://api.whatsapp.com/send?text=...)`. Keine Telefonnummer angeben, damit WhatsApp den Chat-Auswahldialog öffnet.

Falls der Nutzer meldet, dass der Link nicht funktioniert: HTML-Datei mit zwei Buttons erzeugen (`whatsapp://send?text=...` für die native App und `https://api.whatsapp.com/send?text=...` als Fallback) und per `present_files` bereitstellen – aber der Kopieren-Button aus Nachricht 1 bleibt der zuverlässige Fallback und wird immer mitgeliefert.

## Häufige Fehler vermeiden

- Nicht nur die erste Gmail-Seite lesen – paginieren bis zum Zeitraumbeginn.
- Schritt 3 (Fokuspunkte-Frage) nie überspringen, auch wenn die Datenlage gut aussieht.
- Kein Markdown-Fettdruck (`**`) im WhatsApp-Text – nur einfache `*Sternchen*`.
- Vertrauliche Details (interne Konditionen, Personalthemen wie Kündigungen) nur aufnehmen, wenn der Nutzer sie explizit nennt oder freigibt; im Zweifel in Schritt 3/4 nachfragen.
- Die finale Ausgabe besteht immer aus zwei separaten Nachrichten: zuerst die kopierbare Summary, danach nur der WhatsApp-Link mit der kompletten Summary im `text`-Parameter.
