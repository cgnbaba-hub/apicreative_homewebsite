# apicreative_homewebsite

Website der Webagentur apicreative, Zürich.

## Dateien

| Datei | Grösse | Intro | Internet nötig | Wofür |
|---|---|---|---|---|
| `index.html` | 634 KB | ja | ja | Quelle. Bibliotheken und Schrift per CDN. |
| `apicreative-praesentation.html` | 887 KB | ja | nein | Zum Verschicken und Vorführen. |
| `apicreative-ohne-intro.html` | 742 KB | nein | nein | Nur die moderne Seite, ohne Intro. |

Alle drei sind einzelne HTML-Dateien ohne Server und ohne Installation: herunterladen,
doppelklicken, öffnet im Browser.

**`index.html`** ist die Arbeitsfassung. Sie lädt GSAP, ScrollTrigger, Lenis und die
Schrift Inter von einem CDN. Ohne Internet überspringt sie das Intro und zeigt sofort
die moderne Seite; die Schrift fällt dann auf eine Systemschrift zurück.

**`apicreative-praesentation.html`** ist dieselbe Seite mit allem eingebettet. Kein
einziger Netzwerkabruf, das Intro läuft auch ohne Verbindung.

**`apicreative-ohne-intro.html`** zeigt nur die moderne Seite. Kein Scroll-Intro, keine
Animationsbibliotheken.

## Aufbau der Seite

Sticky-Header mit DE/EN-Umschalter · Hero über die volle Breite · Leistungen ·
Vorgehen · Pakete · Referenzen · Bildband · Über uns · Newsletter ·
Kontakt mit Website-Check · Impressum und Datenschutz · Footer. Dazu ein
Newsletter-Pop-up ab 60 % Scrolltiefe oder bei Exit-Intent auf dem Desktop,
einmal pro Sitzung.

Kontakt und Website-Check sind **ein** Abschnitt am Seitenende: Kontaktdaten
links, Formular rechts. Vorher standen sie getrennt, und der Knopf im
Kontaktbereich schickte den Besucher wieder nach oben.

Es gibt bewusst nur **zwei Formulare**: den Website-Check und das
Newsletter-Pop-up. Der Newsletter-Streifen öffnet das Pop-up, statt ein
eigenes Feld danebenzustellen.

Referenzen ausblenden: `class="is-hidden"` an `<section id="referenzen">` ergänzen
oder im Skript `SHOW_REFERENCES = false` setzen.

## Bewegung

Die moderne Seite hat eine eigene Bewegungsschicht, unabhängig vom Intro. Der
Gedanke dahinter: Die Seite verhält sich wie ein Präzisionsinstrument. Nichts
schwebt oder federt, Dinge rasten ein und Masse werden gezogen.

Drei Bewegungen tragen das:

- **Raster.** An jeder Abschnittsgrenze wird das Zwölf-Spalten-Raster kurz als
  rote Haarlinie sichtbar, während die Inhalte darauf einrasten.
- **Bemassung.** An Vorgehen und Paketen zeichnet sich eine Masslinie mit
  Endstrichen über die Karte und bleibt danach als feine Linie stehen.
- **Blende.** Der Hero-Hintergrund öffnet sich beim Laden aus einem schmalen Band
  auf volle Höhe.

Dazu fünf feinere Bewegungen:

- **Zeilensatz.** Grosse Überschriften steigen zeilenweise aus einer Maske, 70 ms
  versetzt. Die Umbrüche werden gemessen, nicht geraten, und nach einem
  Sprachwechsel oder einer Grössenänderung neu gesetzt.
- **Richtung.** Einblendungen kommen aus der Richtung, in die das Element gehört:
  Marken von links, Formularkarten von rechts, Karten von unten.
- **Linien.** Trennlinien zwischen den Abschnitten, im Footer und unter dem
  Footer-Raster ziehen sich von links auf.
- **Navigation.** Ein einziger roter Strich wandert zwischen den Menüpunkten.
  Auf den Leistungskarten schiebt sich beim Überfahren ein Pfeil herein.
- **Tiefe.** Der Hero-Hintergrund läuft langsamer als die Seite und driftet
  zusätzlich langsam in sich, auch wenn niemand scrollt.
- **Schwebende Objekte.** Fenster auf ein Bild mit freigestellten Scheiben und
  Platten, über `mix-blend-mode: multiply` in den Seitengrund eingelassen und in
  einer langsamen 3D-Schleife bewegt. Sie liegen entweder im freien Aussenrand
  oder hinter den Karten, wo nur die Lücken die Bewegung durchlassen.
- **Bildband.** Die Architekturaufnahme zwischen Referenzen und Über uns läuft
  beim Scrollen langsamer als die Seite.
- **Leistungen als Block.** Die sechs Leistungen stehen in einem Block mit
  Haarlinien. Beim Überfahren löst sich die Zeile heraus: Sie tritt nach links
  aus dem Rahmen, bekommt Schatten und eine rote Kante, die übrigen treten zurück.
- **Bleibende Zustände.** Eine Schiene am linken Rand markiert den aktuellen
  Abschnitt und lässt die bereits gelesenen markiert. Im Vorgehen wird eine Linie
  über die drei Schritte gezogen, die gezogen bleibt, auch beim Zurückscrollen.
- **Hover überall.** Pakete heben sich und lassen die Häkchen nacheinander
  anspringen, Referenzkarten zeigen einen Pfeil, Teamkarten zoomen das Foto und
  ziehen eine Linie unter den Namen, Kontaktzeilen drehen ihr Symbol,
  Footer-Links unterstreichen sich von links.
- **Gepinntes Vorgehen.** Der Abschnitt bleibt über rund zweieinhalb
  Bildschirmhöhen stehen, während man durch die drei Schritte wandert. Der
  aktive Schritt tritt hervor, ein Zähler zeigt `02 / 03`. Umgesetzt über
  `position:sticky`, damit es auch in der Fassung ohne Animationsbibliothek
  läuft.

## Ohne Maus

Auf Touchgeräten gibt es kein Überfahren. Dort übernimmt die **Bildmitte** die
Rolle des Zeigers: Das Element, dessen Mitte dem Fenstermittelpunkt am nächsten
liegt, bekommt `.is-focus` und damit dieselbe Darstellung wie beim Hover. Das
gilt für die Leistungszeilen, die Pakete, die Referenzen, die Teamkarten und die
Kontaktzeilen. Beim Scrollen wandert die Hervorhebung mit.

Die Schiene erscheint auf kleinen Geräten als Punktreihe am rechten Rand, ohne
Beschriftung. Antippen gibt über `:active` eine kurze Rückmeldung.

Im gepinnten Vorgehen fallen auf schmalen Geräten die inaktiven Schritte auf
eine Zeile zusammen. Sonst wäre der festgehaltene Inhalt höher als das Fenster
und der dritte Schritt nie vollständig zu sehen.

Dazu die Trägerschicht: versetzte Einblendungen, Fortschrittsstreifen unter der
Kopfzeile, sich verdichtende Kopfzeile, einrollende Ziffern, Teamfotos von
Graustufe zu Farbe, Knöpfe die sich von links füllen, überblendender
Sprachwechsel und ein Rasterblitz am Sprungziel eines Menüklicks.

Jede der fünf lässt sich einzeln abschalten. Im Skript, am Anfang von
`initMotion()`:

```js
var MOTION = {
  headlines: true, direction: true, lines: true, navInk: true, rail: true,
  touchFocus: true, pinnedSteps: true, parallax: true, ambient: true
};
```

Alles läuft über `transform`, `opacity` und `clip-path`, also über den
Compositor. Die Auslöser setzt das Skript, nicht das Markup: `initMotion()`
vergibt die Attribute und hängt die Beobachter ein. Ohne JavaScript bleibt
nichts unsichtbar.

### Bewegung reduzieren

Ist `prefers-reduced-motion` gesetzt (auf dem iPhone: Einstellungen →
Bedienungshilfen → Bewegung → Bewegung reduzieren), läuft die Seite in einer
ruhigen Fassung: `html.motion-soft` statt `html.motion`.

Es bleiben Deckkraft-Übergänge beim Einblenden, die Schiene und die
Hervorhebung ohne Maus. Es entfallen Parallaxe, die Dauerschleifen der
schwebenden Objekte, das Festhalten des Vorgehens, der Zeilensatz der
Überschriften, das Raster, die Bemassung und die Blende.

Vorher schaltete die Einstellung die gesamte Schicht ab, und die Seite stand
auf solchen Geräten völlig still. Die pauschale Regel setzte zudem jede
Übergangsdauer auf `.001ms`; sie begrenzt jetzt auf `.2s`, damit
Deckkraft-Übergänge überleben.

`diagnose.html` prüft auf einem Gerät, was zugelassen ist: reduzierte Bewegung,
Zeigergerät, IntersectionObserver, `position:sticky`, `backdrop-filter`,
JavaScript-Fehler, dazu vier sichtbare Testfelder. Bleibt die Tabelle leer und
wächst nur Testfeld 4, führt die Umgebung kein JavaScript aus.

### Ohne Skript

Eine lokale Datei wird nicht überall in einem vollen Browser geöffnet. Die
Dateiverwaltung auf dem Telefon zeigt sie in einer Vorschau, die kein
JavaScript ausführt. Dann fehlt `html.motion`, und die Seite stünde völlig
still: alle Inhalte da, nichts in Bewegung.

Dagegen steht Abschnitt 7 des Stylesheets. Am `<html>` hängt von Anfang an die
Klasse `nojs`; ein sehr frühes Skript nimmt sie wieder weg, sobald überhaupt
eines läuft. Bleibt sie stehen, übernimmt CSS die Bewegung:

* Dauerschleifen, die keinen Auslöser brauchen (Hero-Hintergrund,
  Systembild, Bildband).
* Ein Auftritt beim Laden für Kopfzeile und Hero. Zeitgesteuert, läuft
  deshalb in jedem Browser.
* Einblendungen am Scrollstand über `animation-timeline: view()`, mit
  Versatz je Position in der Reihe, dazu ein Fortschrittsbalken über
  `scroll(root)`. Hinter `@supports`, denn das können erst neuere Browser
  (Safari ab 26, Chrome ab 115).

Verschoben wird über `translate` statt `transform`: der Endzustand einer
Animation mit `fill: both` würde sonst jede spätere Hover-Regel schlagen.

Auf den Hero-Hintergrund wirkt dabei keine Parallaxe. Er liegt in einem Kasten
mit `overflow:hidden`, und `view()` misst gegen den nächsten Scroll-Container:
der Fortschritt bliebe stehen und das Bild verschoben. Aus demselben Grund sind
nur Elemente scrollgesteuert, über denen kein solcher Kasten liegt.

## Lesbarkeit über dem Bild

Text über einem Bild ist die klassische Stolperstelle. Gemessen wurde am
dunkelsten Punkt des Hintergrunds unter dem jeweiligen Textkasten, bei 1440,
1920 und 390 Pixel Breite:

| | Headline `#1D1D1F` | Vorspann `#6E6E73` |
|---|---|---|
| 1440 | 11,0:1 | 4,9:1 |
| 1920 | 10,8:1 | 4,9:1 |
| 390 | 16,1:1 | 4,8:1 |

Die schwebenden Objekte liegen entweder im freien Aussenrand, den es erst ab
1400 Pixel Breite gibt, oder hinter den Karten. Direkt hinter Fliesstext drücken
sie den Kontrast unter den Grenzwert, auch bei geringer Deckkraft; dort stehen
sie deshalb nicht.

Karten tragen `position:relative; z-index:1`. Ohne das liegt die absolut
gesetzte Objektebene über den unpositionierten Karten und trübt deren Text.

## Einblendung und Hover

`html.motion [data-reveal].is-in` setzt `transform:none` und `opacity:1` und ist
mit (0,3,1) spezifischer als eine gewöhnliche Hover-Regel. Solange das Attribut
am Element hängt, bleibt jeder Hover mit `transform` wirkungslos — der
Karten-Hover war dadurch eine Zeit lang still ausser Kraft.

Deshalb räumt der Beobachter `data-reveal` und `--d` ab, sobald die Einblendung
durch ist. Danach greifen Hover-Regeln wieder auf ihrer natürlichen Stufe.

## Was noch offen ist

Es ist ein Prototyp ohne Backend. Die Formulare prüfen die Eingaben und zeigen eine
Erfolgsmeldung, versenden aber nichts.

Vor einer Veröffentlichung zu ersetzen oder zu prüfen:

- **Telefonnummer** `+41 44 123 45 67` ist ein Beispiel und gehört niemandem zu.
- **Referenzen** sind Beispielinhalte. Die Firmennamen beginnen mit «Muster», die
  Sektion weist im Vorspann darauf hin.
- **Impressum und Datenschutz** sind Entwürfe. Handelsregistereintrag, UID-Nummer
  und vertretungsberechtigte Personen fehlen; beide Texte gehören juristisch geprüft.
  Ein Hinweis darauf steht sichtbar über den beiden Spalten.

## Ändern und neu erzeugen

`index.html` ist die einzige Quelle. Die beiden anderen Dateien werden daraus erzeugt:

```
python3 build.py
```

Nach jeder Änderung an `index.html` ausführen, sonst laufen die Dateien auseinander.
Das Skript prüft zum Schluss, dass die erzeugten Dateien nichts mehr extern nachladen.

`vendor/` enthält die eingebetteten Fremdbestandteile: GSAP 3.12.5 mit ScrollTrigger,
Lenis 1.1.20 und die Schrift Inter 5.3.0 (Zeichensatz Latein, Schnitte 400 bis 700).

`assets/` enthält die beiden Teamfotos im Original und den daraus erzeugten
Ausschnitt sowie die beiden Hintergründe `bg-geometrie.jpg` (Hero, gespiegelt,
damit der Text links freien Grund hat), `bg-objekte.jpg` (die schwebenden
Objekte), `bg-netzwerk.jpg` (Abschnittskopf der Leistungen) und
`bg-architektur.jpg` (das Bildband). `crop_portraits.py` schneidet beide auf dasselbe Hochformat 4:5 zu,
mit gleicher Kopfgrösse und gleicher Kinnhöhe:

```
python3 crop_portraits.py
```

Die Ausschnitte liegen anschliessend als `assets/team-1.jpg` und `assets/team-2.jpg`
und sind in `index.html` als Datenkanal eingebettet.

## Entwürfe

`stitch_apicreative_website_evolution_journey.zip` enthält die vier Stitch-Entwürfe
und die DESIGN.md, aus denen die Seite entstanden ist. Der entpackte Ordner ist per
`.gitignore` ausgenommen.
