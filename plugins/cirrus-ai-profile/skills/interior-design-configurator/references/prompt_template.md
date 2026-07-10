# Prompt-Vorlage für ChatGPT / Gemini

Diese Vorlage wird dem Nutzer im Chat ausgegeben (als Text zum Kopieren), nicht
selbst ausgeführt — die Bildgenerierung passiert in ChatGPT oder Gemini, nicht bei
Claude.

## Grundprinzip: ein Prompt pro Design, nicht pro Raum

ChatGPT und Gemini können pro Generierungslauf nur eine begrenzte Anzahl Bilder
rendern (in der Praxis meist bis zu ca. 10). Ein Sammel-Prompt mit "3 Varianten x
N Räume" sprengt das bei mehr als 3 Räumen. Ein Prompt pro Raum wiederum erzeugt
pro Raum unabhängig gewählte Stile, die über die Wohnung hinweg nicht zusammenpassen.

Deshalb: **immer 3 Prompts insgesamt, einer pro Design-Richtung, nicht einer pro
Raum.** Jeder der drei Prompts referenziert alle hochgeladenen Raumfotos zusammen
und liefert **genau ein möbliertes Bild je Raum** (nicht drei) — in diesem einen,
über alle Räume hinweg konsistenten Design. So bleiben Möbelstil, Materialien und
Farbwelt über die ganze Wohnung stimmig, und jeder Prompt bleibt unter dem
Bilder-Limit, solange die Wohnung nicht mehr als ca. 10 Räume hat.

Ablauf für den Nutzer: **3x** (einmal je Design) alle Originalfotos zusammen mit
dem jeweiligen Design-Prompt bei ChatGPT/Gemini hochladen → 3 Durchläufe, danach
liegt pro Raum das Original plus 3 Design-Varianten vor.

---

## Schritt 0: geplante Nutzung je Raum abfragen

Bevor die Design-Prompts gebaut werden, für **jedes hochgeladene Foto** kurz die
geplante Nutzung erfragen — nicht nur den Raumtyp, sondern wofür der Raum konkret
genutzt werden soll. Das hilft ChatGPT/Gemini, passende Möbel auszuwählen (z.B.
kann ein kleines Zimmer als Homeoffice, Gästezimmer, Ankleide oder Kinderzimmer
möbliert werden — optisch vom leeren Foto allein nicht unterscheidbar, macht aber
einen großen Unterschied für die Einrichtung).

Als eine kompakte Frage im Chat stellen, z.B.:

> Bevor ich die Prompts baue: wofür sollen die Räume genutzt werden?
> 1. [Foto 1, erkannter/vermuteter Raumtyp] – z.B. Wohnzimmer, Wohn-/Essbereich, ...?
> 2. [Foto 2] – ...?
> ...
> Falls die Standardnutzung passt (z.B. Küche bleibt Küche), einfach "passt so" sagen.

Bei eindeutigen Räumen (Küche mit Fliesenspiegel, Bad mit Sanitäranlagen) muss nicht
zwingend nachgefragt werden. Bei flexibel nutzbaren Räumen (zusätzliches Zimmer,
Studio, offener Grundriss) immer nachfragen.

## Schritt 1: drei Design-Richtungen festlegen

Für die Wohnung als Ganzes drei unterschiedliche, in sich stimmige Design-Richtungen
vorschlagen (nicht pro Raum unabhängig, sondern als roter Faden über alle Räume).
Für jede Design-Richtung: ein Name, eine kurze Stilbeschreibung (Materialien, Möbel-
charakter, generelle Farbwelt) und **je Raum eine passende Wandfarbe innerhalb dieser
Design-Linie** (Wandfarben dürfen zwischen Räumen variieren, sollen aber erkennbar
zur selben Design-Richtung gehören, z.B. alle in gedeckten Erdtönen).

Kurz im Chat vorschlagen und dem Nutzer die Möglichkeit geben, das anzupassen:
"Ich schlage folgende drei Design-Richtungen für die ganze Wohnung vor: … Sag mir
gern, falls du andere Stile oder Farben möchtest, sonst baue ich die Prompts damit."

Beispiel für drei Design-Richtungen:
1. **Skandinavisch hell** – helles Holz, neutrale Textilien, reduzierte Möblierung;
   Wandfarben durchgehend in warmem Weiß/Off-White-Tönen, leicht raumweise variiert
2. **Warmer Loft-Stil** – dunklere Hölzer, Samt/Leder-Akzente, Industrial-Elemente;
   Wandfarben in Terrakotta-/Sandtönen
3. **Minimalistisch monochrom** – klare Linien, reduzierte Möblierung, wenig Dekor;
   Wandfarben in hellen Grautönen

## Schritt 2: drei Prompts ausgeben (einen je Design)

Für jede der drei Design-Richtungen aus Schritt 1 einen eigenen Prompt als
kopierbaren Codeblock ausgeben. `[RAUMLISTE]` = nummerierte Liste aller Räume mit
geplanter Nutzung (aus Schritt 0). `[DESIGN-NAME]`, `[DESIGN-BESCHREIBUNG]` und
`[WANDFARBEN JE RAUM]` aus Schritt 1.

```
Ich lade dir [ANZAHL RÄUME] Fotos leerer/unmöblierter Räume derselben Wohnung hoch,
in dieser Reihenfolge. Zu jedem Foto die geplante Nutzung, damit du die Möblierung
passend auswählen kannst:
[RAUMLISTE]

Bitte erstelle für JEDES dieser Fotos GENAU EIN möbliertes Bild (also insgesamt
[ANZAHL RÄUME] Bilder, ein Bild pro Foto) im folgenden einheitlichen
Einrichtungsstil, sodass die ganze Wohnung stimmig wirkt:

Design: [DESIGN-NAME]
[DESIGN-BESCHREIBUNG]

Wandfarbe je Raum (innerhalb dieses Designs):
[WANDFARBEN JE RAUM]

Vermische dabei die Räume nicht — jedes Ausgabebild muss eindeutig auf dem
jeweiligen Originalfoto basieren und exakt diesen Raum zeigen, keinen anderen.
Bitte als separate Einzelbilder ausgeben (keine Collage) und in deiner Antwort klar
beschriften, zu welchem Raum jedes Bild gehört (z.B. "Wohnzimmer – [DESIGN-NAME]").

WICHTIG – für JEDES der Fotos gilt gleichermaßen:
- Raumgeometrie, Proportionen, Deckenhöhe und Perspektive/Kamerawinkel bleiben exakt wie im jeweiligen Originalfoto
- Position und Größe von Fenstern, Türen und Durchgängen bleiben unverändert
- Heizkörper/Heizungen bleiben an ihrer Position und Größe
- Steckdosen, Lichtschalter und sichtbare Installationen bleiben unverändert
- Bodenbelag (falls bereits vorhanden) bleibt wie im Original
- Keine strukturellen Veränderungen (keine neuen Wände, keine versetzten Fenster, kein verändertes Deckenniveau)

Bitte fotorealistisch rendern, gleiche Kameraperspektive und gleicher Bildausschnitt
wie im jeweiligen Originalfoto, damit die Bilder direkt mit dem Original vergleichbar sind.
```

`[RAUMLISTE]`-Format (Raumname + geplante Nutzung):
```
1. Wohnzimmer – geplante Nutzung: Wohn- und Essbereich für eine 3-köpfige Familie
2. Schlafzimmer – geplante Nutzung: Elternschlafzimmer
3. Kleines Zimmer – geplante Nutzung: Homeoffice
```

`[WANDFARBEN JE RAUM]`-Format:
```
- Wohnzimmer: warmes Off-White
- Schlafzimmer: helles Sandbeige
- Kleines Zimmer: warmes Weiß mit einer Akzentwand in mattem Salbeigrün
```

Am Ende alle drei Prompts kurz zusammenfassen: "Damit hast du 3 Prompts — einmal
alle Fotos zusammen mit Prompt 1 hochladen, dann mit Prompt 2, dann mit Prompt 3.
Am Ende hast du pro Raum das Original plus 3 Design-Varianten."

## Wenn die Wohnung mehr als ca. 10 Räume hat

Dann in Gruppen von maximal 10 Räumen aufteilen: denselben Design-Prompt pro Design
mehrfach ausgeben, einmal je Raumgruppe (nur `[RAUMLISTE]`/`[ANZAHL RÄUME]` auf die
jeweilige Gruppe anpassen, `[DESIGN-NAME]`/`[DESIGN-BESCHREIBUNG]`/Wandfarben-Logik
bleiben identisch, damit der Stil über die ganze Wohnung konsistent bleibt). Das
kurz erklären, bevor die zusätzlichen Prompts ausgegeben werden.

---

## Hinweise für Claude beim Ausfüllen dieser Vorlage

- **Immer genau 3 Prompts, nie mehr Prompts pro Raum.** Das Grundprinzip (ein Prompt
  je Design, alle Räume darin) ist keine Option unter mehreren, sondern der
  Standardablauf dieses Skills.
- **Schritt 0 nicht überspringen:** Bei flexibel nutzbaren Räumen immer nach der
  geplanten Nutzung fragen, bevor die Design-Prompts gebaut werden — das beeinflusst
  direkt, welche Möbel ChatGPT/Gemini wählt (Bett vs. Schreibtisch vs. Kleiderschrank
  sehen in einem leeren Zimmer identisch aus). Bei eindeutigen Räumen (Küche, Bad)
  kann die Nutzung direkt aus dem Bild übernommen werden, ohne nachzufragen.
- **Design-Richtungen gelten für die ganze Wohnung, nicht pro Raum einzeln
  erfunden.** Die Wandfarben dürfen je Raum variieren, sollen aber erkennbar zur
  selben Design-Linie gehören (z.B. alle drei Wandfarben eines Designs aus derselben
  Farbfamilie).
- **`[RAUMLISTE]`**: Raumnamen aus Dateiname oder Bildinhalt ableiten (z.B. an
  Fliesen/Sanitär als "Bad" erkennbar), sonst beim Nutzer nachfragen.
- Den fertigen Text **je Design als eigenen kopierbaren Codeblock** ausgeben, damit
  der Nutzer ihn 1:1 in ChatGPT/Gemini einfügen kann.
- Explizit erwähnen: **alle Fotos UND der jeweilige Design-Prompt gemeinsam** in
  ChatGPT/Gemini hochladen (der Prompt allein ohne die Fotos funktioniert nicht),
  und dass dieser Vorgang **dreimal** wiederholt wird (einmal je Design).
- Falls das Modell trotzdem eine Collage mit mehreren Räumen in einem Bild liefert
  (kommt vor allem bei Gemini vor): den Nutzer auf `scripts/crop_grid.py` hinweisen,
  um die Collage in Einzelbilder zu zerlegen.
- Falls Räume vermischt werden, fehlende Bilder auftauchen oder die Perspektive
  nicht mehr zum Originalfoto passt: dem Nutzer vorschlagen, für den betroffenen
  Raum einen Einzel-Prompt mit nur diesem einen Foto zu wiederholen (gleicher
  Design-Abschnitt aus dem Prompt, nur auf ein Foto reduziert), statt es einfach so
  zu lassen.
