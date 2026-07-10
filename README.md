# Cirrus Profile

Dieses Repository ist der zentrale Marktplatz fuer die internen Claude-Skills von Cirrus Real Estate GmbH.

## Struktur

```
Cirrus-Profile/
├── .claude-plugin/marketplace.json   # Katalog-Datei
├── plugins/cirrus-ai-profile/
│   ├── .claude-plugin/plugin.json    # Plugin-Metadaten
│   └── skills/                       # alle Skills
└── README.md
```

## Enthaltene Skills

- ausschreibungs-manager
- bauablauf-tracker
- cirrus-finanzierungs-factsheet
- cirrus-onboarding
- comps-analyse-generator
- facade-color-configurator
- finanzierungsanfrage-email
- interior-design-configurator
- loi-generator
- service-provider-outreach
- team-weekly-summary

## Nutzung (fuer Team-Mitglieder)

1. In Claude: **Customize → Plugins → Personal plugins → "+" → "Add marketplace" → "Add from a repository"**
2. Repository-URL eintragen: `https://github.com/Cirrus-Real-Estate-GmbH/Cirrus-Profile`
3. Plugin `cirrus-ai-profile` installieren
4. Bei neuen Versionen: im Marketplace auf **"Update"** klicken

## Updates

Aenderungen werden direkt auf `main` gepusht. Nach jedem Update bitte im Marketplace auf "Update" klicken, um die neueste Version zu ziehen.
