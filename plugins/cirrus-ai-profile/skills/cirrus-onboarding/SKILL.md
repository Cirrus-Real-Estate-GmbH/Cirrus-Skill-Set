---
name: cirrus-onboarding
description: >
  This skill should be used as the FIRST step when a new Cirrus Real Estate GmbH
  team member sets up their Claude profile, or whenever the user says
  "Onboarding", "Onboarding starten", "Profil einrichten", "erste Einrichtung",
  "Cirrus Setup", "richte mein Claude ein", "set up my profile", or asks to make
  their Claude match the company standard. It guides the user step by step through
  connecting the required connectors, installing the Claude in Chrome extension,
  installing the required Plugins, installing every current Team-Skill from the
  shared "03 Skills" Drive folder (skippable per skill), setting the default reach,
  and running a final functional test — until the profile matches the Cirrus baseline.
metadata:
  version: "0.3.0"
  author: "Cirrus Real Estate GmbH"
---

# Cirrus Onboarding

Guide a new (or resetting) Cirrus Real Estate team member through a complete, verified
setup of their Claude profile so it matches the company baseline. Run this as an
interactive, one-step-at-a-time flow. Speak German with the user (the team works in
German). Be warm, concrete, and never overwhelm — one action per step, confirm, then
continue. After the baseline is reached, make clear that further customization
(which optional skills to keep active, extra connectors, etc.) is entirely up to the
individual person.

## Kontext: warum manuell statt zentralem Plugin

Es gibt bewusst KEIN zentrales `cirrus-ai-profile`-Plugin mehr, das Team-Skills bündelt
und synchronisiert (das würde einen Team-Account und GitHub-Kenntnisse voraussetzen, die
aktuell nicht vorhanden sind). Falls dieses Plugin bei einem Nutzer noch installiert ist,
darauf hinweisen, dass es veraltet ist und deinstalliert werden kann.

Stattdessen ist die Quelle der Wahrheit für Team-Skills der gemeinsame Drive-Ordner
**"03 Skills"** (im Cirrus Shared Drive, oberste Ebene). Dort legt jede Person, die einen
Skill baut oder verbessert, einen nummerierten Unterordner mit ihren Initialen an
(Beispiel: `14 - Comps Analyse (LE)`), der die fertige Skill-Struktur (`SKILL.md` + ggf.
`references/`, `assets/`, `scripts/`) enthält. Der Ordnerinhalt ändert sich laufend — bei
jedem Onboarding-Lauf den aktuellen Stand live abfragen, NICHT eine feste Liste annehmen.
Jede Person installiert sich die gewünschten Skills einmalig selbst als eigene,
persönliche Skills in Claude. Bei Verbesserungen wird der jeweilige Unterordner im Drive
aktualisiert und im Team kommuniziert — jede Person zieht sich das Update dann manuell
nach demselben Verfahren wie bei der Erstinstallation nach.

## Guardrails (always apply)

- Never enter the user's passwords, credentials, or OAuth logins yourself. Each
  connector/plugin is authenticated BY THE USER in their own browser. You only guide and verify.
- Never send email on the user's behalf without explicit approval. Company standard is
  "draft + manual click".
- Do not modify sharing permissions, security settings, or delete anything during onboarding.
- Logins and installs cannot be automated — walk the user through them and verify status instead.
- Skills are optional per person past the baseline — always offer a skip option, never force
  a skill on someone who says they don't need it.

## Step 0 — Welcome & orientation

Greet the user, ask for their name and role (optional, for personalization), and briefly
explain what onboarding will do: connect the required connectors, install the Claude in
Chrome extension, install the required plugins, install the current Team-Skills from Drive
(skippable per skill), set the default reach, and run a quick test — roughly 15-20 minutes
depending on how many skills are installed. Then start.

## Step 1 — Connectors

Required connectors for the Cirrus baseline:

- **Apollo.io**
- **ClickUp**
- **Gmail**
- **Google Calendar**
- **Google Drive**
- **Claude in Chrome** (browser control)
- **Control Chrome** (local MCP — fast tab reading/scripting)
- **Control Your Mac** (local MCP — AppleScript automation)
- **Filesystem** (local MCP — access to the user's own files)

Not part of the standard: GitHub (not used at Cirrus).

Call `ListConnectors` and compare against this list. Present a short checklist showing
which are already connected (✅) and which are still missing (⬜). For each missing
connector:

1. Tell the user exactly which one to connect and that they log in with their own
   Cirrus account (Google account, Apollo account, etc.), or — for the three local
   MCP servers (Control Chrome, Control Your Mac, Filesystem) — that these run via
   the Claude Desktop app and need to be enabled there once.
2. Offer the connect card with `SuggestConnectors` (resolve the connector via
   `SearchMcpRegistry` first if you need its directoryUuid), or instruct them to open
   this chat's connector settings and enable it.
3. Wait for the user to confirm they connected it.
4. Re-run `ListConnectors` to verify it is now green before moving on.

Go connector by connector, never batch all logins at once so nothing is skipped.

## Step 2 — Claude in Chrome extension

Separate from the connector handshake: the actual browser extension needs to be installed
once in Chrome (chrome web store → "Claude in Chrome"). Verify with `list_connected_browsers`
— it should show a connected browser. If none shows up, walk the user through installing
and pairing the extension, then re-verify.

## Step 3 — Plugins

Required plugins for the Cirrus baseline (Customize → Plugins):

- **Wix**
- **Productivity**
- **PDF Viewer**
- **Apollo.io**
- **Lusha**

For each: check if already installed; if not, guide the user to Customize → Plugins →
find it → Install. Confirm each one shows as installed before moving on.

If `cirrus-ai-profile` (the old bundled Team-Skill plugin) is still installed, point out
that it's deprecated and recommend removing it, so it doesn't conflict with the individually
installed Team-Skills from Step 4.

## Step 4 — Team-Skills aus dem "03 Skills"-Drive-Ordner

Das ist der wichtigste Schritt für die tägliche Arbeit. Der Ordnerinhalt ändert sich
laufend, deshalb IMMER live nachschauen statt eine gespeicherte Liste zu verwenden.
Keine Vorab-Bewertung oder Sortierung der Skills vornehmen — einfach die nummerierten
Ordner der Reihe nach abarbeiten. Es müssen nicht alle 100% perfekt/einheitlich formatiert
sein; kleine Extra-Handgriffe pro Skill (z. B. Datei umbenennen, Ordner ordentlich packen)
sind normal und kein Blocker.

1. Im gemeinsamen Cirrus Shared Drive den Ordner **"03 Skills"** öffnen (oberste Ebene,
   nicht unter "00 Onboarding"). Falls die ID/der Pfad unklar ist, per Google-Drive-Suche
   nach dem Ordnernamen "03 Skills" auflösen.
2. Alle aktuell enthaltenen **nummerierten** Unterordner auflisten (Format meist
   `[Nummer] - [Skill-Name] ([Initialen des Erstellers])`) — das ist die Liste der
   tatsächlichen Team-Skills. Wie viele es aktuell sind, ist offen (aktuell ~15, kann mit
   der Zeit wachsen). Unnummerierte Ordner im selben Verzeichnis sind kein Teil dieser
   Liste und können ignoriert werden. Dem Nutzer die Liste zeigen, sortiert nach Nummer.
3. Die Liste **der Reihe nach, einen Skill nach dem anderen** durchgehen. Pro Skill kurz
   fragen, ob installiert werden soll — **Skip ist jederzeit eine valide Antwort**, ohne
   Nachfrage warum. Kein Zwang, alle zu nehmen.
4. Für jeden Skill, den der Nutzer haben will:
   a. Zugehörigen Unterordner-Inhalt aus Drive holen (SKILL.md bzw. die Hauptdatei plus
      etwaige `references/`, `assets/`, `scripts/`).
   b. Daraus eine sauber benannte, installierbare Struktur bauen: Hauptdatei ggf. in
      `SKILL.md` umbenennen, alles in einen einzigen, nach dem Skill benannten Ordner
      packen, dann als ZIP.
   c. In Claude: **Customize → Skills → "+" → "Create skill"** → ZIP hochladen.
   d. Kurz bestätigen, dass der Skill in der Liste erscheint und aktiviert ist. Falls der
      Upload aus irgendeinem Grund nicht klappt: kurz benennen, was fehlgeschlagen ist,
      und mit dem nächsten Skill weitermachen statt hier stecken zu bleiben — der Nutzer
      kann das einzelne Problem später mit dem/der Ersteller:in klären.
5. Am Ende eine kurze Zusammenfassung zeigen: installierte Skills vs. übersprungene Skills.

**Update-Hinweis für später:** Wenn jemand einen Skill im "03 Skills"-Ordner verbessert,
ersetzt er/sie den jeweiligen Unterordner dort und meldet es im Team. Jede Person, die
diesen Skill nutzt, wiederholt dann Schritt 4 für genau diesen einen Skill (alten Skill in
Customize → Skills entfernen, neuen hochladen). Es gibt aktuell keinen automatischen Sync
— das ist eine bewusste, einfache Zwischenlösung, bis es dafür eine bessere Infrastruktur gibt.

## Step 5 — Default reach

Explain the company default reach for a new member and have them grant it:

- **Access to their own files** (Filesystem / folder access).
- **Access to their own Google Drive** (already via the Drive connector).

Full local depth (Chrome + Mac control) is part of the baseline per Step 1, but how deeply
each person actually uses it is their own call.

## Step 6 — Functional test

Run one small, read-only check per connected system and report a pass/fail table:

- Gmail: search 1 recent thread
- Drive: list a couple of recent files
- Calendar: list calendars
- ClickUp: list workspace members
- Apollo.io: fetch own profile
- Chrome: list tabs / open a neutral test page + screenshot
- Filesystem: list the user's home directory
- Plugins: confirm Wix, Productivity, PDF Viewer, Apollo.io, Lusha show as installed
- Skills: confirm each newly installed Team-Skill appears in Customize → Skills

Summarize what passed. For anything that failed, point back to the relevant step.

## Step 7 — Done

Confirm the profile now matches the Cirrus baseline: required connectors, Claude in Chrome,
required plugins, and the Team-Skills the user chose to install. Make clear that from here
on, further customization — which optional skills to add or remove later, extra connectors,
personal preferences — is entirely up to the individual. Remind them that email sending is
always "draft + your click", and that Team-Skill updates are manual (check "03 Skills" →
repeat Step 4 for the changed skill).
