---
name: cirrus-skill-creator
description: >
  Erstellt oder verbessert einen Cirrus-internen Claude-Skill und rollt ihn danach
  automatisch fuers ganze Team aus: Skill-Ordner ins GitHub-Repo Cirrus-Skill-Set pushen,
  den internen Marketplace-Namen hochzaehlen (damit das Update tatsaechlich ankommt),
  und eine Team-E-Mail im etablierten Cirrus-Format vorbereiten. Nutze diesen Skill immer,
  wenn der Nutzer "einen neuen Skill bauen", "Skill erstellen", "Skill verbessern/updaten",
  "Skill ausrollen" oder "Skill ins Team-Repo/Marketplace hochladen" moechte -- auch wenn nur
  gesagt wird "mach daraus einen Skill" oder "lad den Skill hoch".
---

# Cirrus Skill Creator

Zweistufiger Workflow: (1) Skill entwickeln/verbessern nach dem etablierten Verfahren des
allgemeinen `skill-creator`-Skills, (2) danach automatisch fuers Cirrus-Team ausrollen.

## Phase 1: Skill entwickeln

Folge fuer das eigentliche Erstellen, Testen und Iterieren exakt dem Ablauf des
`skill-creator`-Skills (Interview -> Entwurf -> Testfaelle -> Review mit dem Nutzer ->
verbessern -> wiederholen), inklusive der "Claude.ai-specific instructions" darin (keine
Subagents, Tests selbst durchspielen, Ergebnisse direkt im Chat zeigen statt Browser-Viewer).

Frage bei einer Aktualisierung eines bestehenden Skills zuerst, ob es sich um ein
Bugfix/Verbesserung des bestehenden Skills handelt oder um einen komplett neuen Skill.
Bei einer Aktualisierung: Namen und Ordnerstruktur des bestehenden Skills beibehalten.

Bevor mit Phase 2 begonnen wird: Nutzer explizit fragen, ob der Skill jetzt final ist und
ausgerollt werden soll ("Skill jetzt ins Team-Repo hochladen und ankuendigen?" /
"Nur lokal speichern, noch nicht ausrollen?").

## Phase 2: Cirrus-Rollout (erst nach Bestaetigung durch den Nutzer)

### Schritt 1: Skill-Ordner ins Repo bringen

Repo: `https://github.com/Cirrus-Real-Estate-GmbH/Cirrus-Skill-Set` (public), lokal geklont
mit `gh`/`git`. Der fertige Skill-Ordner (SKILL.md + ggf. references/, assets/, scripts/)
kommt nach `plugins/cirrus-ai-profile/skills/<skill-name>/` -- neu anlegen bei neuem Skill,
ueberschreiben bei einem Update eines bestehenden.

### Schritt 2: marketplace.json aktualisieren -- WICHTIG

Bekannter Sync-Mechanismus: Claude zieht Aenderungen an einem bereits verbundenen Marketplace
nur, wenn sich der interne `"name"`-Wert der marketplace.json aendert (reiner Inhalts-Push
ohne Namensaenderung wird ignoriert). Deshalb bei JEDEM Rollout zwingend:

1. `.claude-plugin/marketplace.json` oeffnen.
2. Den Top-Level `"name"`-Wert um eine Versionsnummer hochzaehlen (z.B. endet er auf
   `-v2`, dann neu `-v3`; falls keine Nummer vorhanden, `-v2` anhaengen).
3. Falls ein neuer Skill hinzugefuegt wird: den Pfad `"./skills/<skill-name>"` in der
   `skills`-Liste des `cirrus-ai-profile`/`cirrus-skill-set`-Plugin-Eintrags ergaenzen.
4. Das `"version"`-Feld des Plugin-Eintrags ebenfalls hochzaehlen (z.B. 1.2.0 -> 1.3.0).
5. `"strict": false` und die restliche Struktur unveraendert lassen.

Ohne Schritt 2 kommt das Update bei niemandem an, auch nicht beim Ausrollenden selbst.

### Schritt 3: Commit + Push

```bash
cd <lokaler-klon-von-Cirrus-Skill-Set>
git add -A
git commit -m "Skill <skill-name>: <kurze Beschreibung der Aenderung>"
git push origin main
```

Falls kein lokaler Klon mit GitHub-Zugriff existiert: `gh auth status` pruefen; falls nicht
eingeloggt, `gh auth login` per Device-Flow durchfuehren (Code + Link an den Nutzer geben,
auf Bestaetigung warten), dann `gh repo clone Cirrus-Real-Estate-GmbH/Cirrus-Skill-Set`.

### Schritt 4: Nutzer zum Abholen des Updates anleiten

Dem Nutzer mitteilen:
- Eigener Marketplace: **"Sync automatically"** aktivieren + **"Check for updates"** klicken
  reicht in der Regel (kein Entfernen/Neu-Hinzufuegen noetig, sofern der Name in Schritt 2
  wirklich geaendert wurde).
- Falls das nicht zieht: Marketplace entfernen und mit derselben URL neu hinzufuegen.

### Schritt 5: Team-E-Mail vorbereiten (Gmail-Entwurf, NICHT automatisch senden)

Entwurf im etablierten Cirrus-Format erstellen (siehe bisherige Skill-Ankuendigungen):

- **Was macht der Skill?**
- **Wann einsetzen?**
- **Was Claude dafuer braucht** (Connectors etc.)
- **Was dabei rauskommt**
- **So wird der Skill genutzt** (kurzer Hinweis: Marketplace "Check for updates" klicken,
  falls das Plugin schon installiert ist; sonst einmalig ueber
  `Cirrus-Real-Estate-GmbH/Cirrus-Skill-Set` hinzufuegen)

Empfaenger: Team-Mitglieder, die den Skill betrifft (im Zweifel den Nutzer fragen, wer
informiert werden soll). Immer als **Gmail-Entwurf** erstellen und dem Nutzer zeigen --
nur auf explizite Bestaetigung tatsaechlich versenden.

## Wichtig

- Niemals Schritt 2 (Namensaenderung) vergessen -- das ist die haeufigste Fehlerquelle und
  fuehrt dazu, dass ein Update unsichtbar bleibt, obwohl der Push technisch erfolgreich war.
- Bei Unsicherheit ueber den aktuellen internen Namen: `.claude-plugin/marketplace.json` aus
  dem Repo lesen, nicht raten.
- Rollout nur nach expliziter Bestaetigung durch den Nutzer, nie automatisch nach Phase 1.
