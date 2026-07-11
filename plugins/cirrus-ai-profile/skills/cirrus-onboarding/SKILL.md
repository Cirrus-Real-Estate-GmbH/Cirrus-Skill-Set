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
  version: "0.4.1"
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

## Kontext: zentrales GitHub-Plugin

Die Quelle der Wahrheit für Team-Skills ist jetzt das GitHub-Repository
**`https://github.com/Cirrus-Real-Estate-GmbH/Cirrus-Skill-Set`** (öffentlich lesbar). Es
enthält ein einziges Plugin (`cirrus-skill-set`), das alle Team-Skills sowie die Standard-
Connectors bündelt. Jede Person bindet dieses Repo einmalig als Marketplace ein und
installiert das Plugin — Updates werden danach per "Sync automatically" + "Check for
updates" abgeholt, kein manuelles Kopieren aus Drive mehr nötig.

Der alte, rein Drive-basierte Weg (Schritt für Schritt jeden Skill einzeln aus dem
"03 Skills"-Ordner als ZIP hochladen) ist damit abgelöst. Falls ein Nutzer noch einzelne,
so installierte Alt-Skills hat, die inzwischen auch im GitHub-Plugin enthalten sind, kurz
empfehlen, die Alt-Version zu entfernen, um Dopplungen zu vermeiden.

**Bekannte Eigenheit beim Marketplace-Update:** Ein reiner Inhalts-Push auf GitHub wird von
Claude nicht automatisch übernommen — der interne `"name"`-Wert in der `marketplace.json`
muss bei jedem Update mit hochgezählt werden (z. B. `-v3` → `-v4`), sonst bleibt der alte
Stand sichtbar, auch nach "Check for updates". Das übernimmt automatisch, wer den
`cirrus-skill-creator`-Skill zum Ausrollen von Updates benutzt.

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
- **Claude in Chrome** (browser control — funktioniert auf Mac und Windows)
- **Control Chrome** (local MCP — schnelles Tab-Lesen/Scripting, funktioniert auf Mac
  und Windows)
- **Control Your Mac** (local MCP — AppleScript-Automatisierung, **Mac-exklusiv**; hat
  aktuell KEIN Windows-Äquivalent laut Anthropic. Windows-Nutzer:innen überspringen diesen
  Punkt einfach — kein Ersatz nötig, kein Blocker für den Rest des Onboardings)
- **Filesystem** (local MCP — Zugriff auf eigene Dateien, funktioniert auf Mac und Windows)

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

## Step 1b — GitHub Custom Connector (nur für Skill-Autor:innen)

Nur nötig für Personen, die selbst Skills bauen/hochladen wollen (nicht für reine Nutzer
— die brauchen für Step 3/4 keinen GitHub-Zugang). Falls unklar: fragen, ob die Person
plant, eigene Skills beizutragen; wenn nein, diesen Schritt überspringen.

1. In Claude: Settings → Connectors → **"Add custom connector"**.
2. MCP Server URL: `https://api.githubcopilot.com/mcp`
3. Unter "Advanced settings": Client ID + Client Secret eintragen — bei Liron erfragen
   (gemeinsame, bereits registrierte OAuth-App). Diese Werte NICHT per offener
   Chat-Nachricht teilen lassen, sondern über einen sicheren Kanal (Passwort-Manager o. ä.).
4. Eindeutig benennen (Empfehlung: **"Cirrus GitHub"**, nicht mehrfach anlegen — doppelte
   Connector-Einträge mit unklaren Namen sorgen später für Verwirrung).
5. "Add" klicken, dann "Connect" → mit dem EIGENEN GitHub-Account einloggen und bestätigen.
6. Verifizieren, dass der Connector danach als Werkzeug nutzbar ist (kurzer Testaufruf,
   z. B. das eigene GitHub-Profil abrufen).

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

## Step 4 — Cirrus Team-Skills über den GitHub-Marketplace

Das ist der wichtigste Schritt für die tägliche Arbeit — bündelt alle Team-Skills in einem
Plugin, ohne einzeln aus Drive kopieren zu müssen.

1. In Claude: **Customize → Plugins → "+" → "Add marketplace" → "Add from a repository"**.
2. URL eintragen: `https://github.com/Cirrus-Real-Estate-GmbH/Cirrus-Skill-Set`
3. Plugin **"Cirrus Skill Set"** installieren.
4. Verifizieren: Anzahl der Skills im Plugin sollte deutlich größer 0 sein. Falls 0 Skills
   angezeigt werden (bekannter, gelegentlich auftretender Anzeigefehler): Marketplace
   entfernen und mit derselben URL neu hinzufügen, oder kurz bei Liron melden.
5. In einem NEUEN Chat kurz `/` oder "+" öffnen und prüfen, dass die Team-Skills dort
   auftauchen (Plugin-Installationen laden nicht rückwirkend in bereits offene Chats).

**Update-Hinweis für später:** Sobald ein Skill im Repo aktualisiert wird (Team-Mail folgt
jeweils), reicht: Marketplace-Eintrag öffnen → **"Sync automatically"** aktivieren (falls
noch nicht geschehen) → **"Check for updates"** klicken. Falls das nichts zieht: Marketplace
entfernen und mit derselben URL neu hinzufügen.

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
- Plugins: confirm Wix, Productivity, PDF Viewer, Apollo.io, Lusha, and Cirrus Skill Set
  show as installed
- Cirrus Skill Set: confirm skill count > 0 and at least one Team-Skill is usable in a
  new chat
- GitHub (only if Step 1b was done): fetch the user's own GitHub profile via the connector

Summarize what passed. For anything that failed, point back to the relevant step.

## Step 7 — Done

Confirm the profile now matches the Cirrus baseline: required connectors, Claude in Chrome,
required plugins, and the Team-Skills the user chose to install. Make clear that from here
on, further customization — which optional skills to add or remove later, extra connectors,
personal preferences — is entirely up to the individual. Remind them that email sending is
always "draft + your click", and that Team-Skill updates are manual (check "03 Skills" →
repeat Step 4 for the changed skill).
