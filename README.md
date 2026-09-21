# apicreative_homewebsite

Website der Webagentur apicreative, Zürich.

## Dateien

| Datei | Grösse | Intro | Internet nötig | Wofür |
|---|---|---|---|---|
| `index.html` | 517 KB | ja | ja | Quelle. Bibliotheken und Schrift per CDN. |
| `apicreative-praesentation.html` | 770 KB | ja | nein | Zum Verschicken und Vorführen. |
| `apicreative-ohne-intro.html` | 624 KB | nein | nein | Nur die moderne Seite, ohne Intro. |

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
Vorgehen · Pakete · Referenzen · Bildband · Über uns · Beitrag · Newsletter ·
Kontakt mit Website-Check · Impressum und Datenschutz · Footer. Dazu ein
Newsletter-Pop-up ab 60 % Scrolltiefe oder bei Exit-Intent auf dem Desktop,
einmal pro Sitzung.

Kontakt und Website-Check sind **ein** Abschnitt am Seitenende: Kontaktdaten
links, Formular rechts. Vorher standen sie getrennt, und der Knopf im
Kontaktbereich schickte den Besucher wieder nach oben.

Es gibt bewusst nur **zwei Formulare**: den Website-Check und das
Newsletter-Pop-up. Der Newsletter-Streifen öffnet das Pop-up, statt ein
eigenes Feld danebenzustellen.

Im Website-Check sind **drei** Felder Pflicht: Name, E-Mail-Adresse und die
Einwilligung. Mehr braucht es nicht, um zu antworten. Unternehmen,
Website-Adresse und Anmerkungen sind freiwillig — wer sich meldet, hat nicht
zwangsläufig eine Firma oder eine Website. Ein Satz über dem Absenden sagt das
auch so.

Referenzen ausblenden: `class="is-hidden"` an `<section id="referenzen">` ergänzen
oder im Skript `SHOW_REFERENCES = false` setzen.

## Zeichen

Das Zeichen ist ein **A aus zwei Flächen**: ein Chevron und eine kleinere
Fläche darin. Es wird nicht gezeichnet, sondern **gerechnet** — `make_icons.py`
konstruiert es aus drei Zahlen:

| | |
|---|---|
| `RAND` | Abstand zu allen vier Kanten der Zeichenfläche |
| `BAND` | Breite des Chevrons, senkrecht gemessen |
| `SPITZE_INNEN` | y der Spitze der inneren Fläche |

Daraus folgt, was man von Hand nur mühsam trifft: Spiegelsymmetrie zur
Mittelachse, nur zwei Kantenwinkel im ganzen Zeichen, ein überall gleich
breites Band, eine überall gleich breite Spalte zwischen Chevron und innerer
Fläche, und gleicher Abstand zu allen vier Rändern.

Die erste Fassung war von Hand gesetzt. Sie sah verschoben aus, und zu Recht:
die Spalte war keil- statt parallelförmig, das Band an der Spitze schmaler
als am Fuss, und das Ganze sass rechts aus der Mitte. Nichts davon kann jetzt
noch passieren, weil nichts mehr von Hand gesetzt wird.

Gezeichnet ist es als **SVG**, nicht als Pixelbild: scharf in jeder Grösse,
wenige hundert Byte, und die Farbe steckt in einem Verlauf (`--red` nach
`--red-warm`), nicht im Bild. Die Akzentfarbe der Seite bleibt `--red`; das
warme Orange kommt ausschliesslich im Zeichen vor.

Aus derselben Quelle schreibt `make_icons.py` vier Dinge in `index.html`:
das `<symbol id="i-mark">` im Sprite (Kopf und Footer), den Favicon-Data-URI,
das 180×180-PNG für den Homescreen von iOS und das 512×512-PNG für alles
übrige. Der Tab kann damit nie ein anderes Zeichen zeigen als die Seite.

```
python3 make_icons.py     # konstruiert das Zeichen, schreibt alle vier Fassungen
python3 build.py          # erzeugt die beiden abgeleiteten Dateien
```

**Herkunft:** Die Form geht auf einen Entwurf zurück, den der Auftraggeber
beigestellt hat. Die Vorlage trug ein Wasserzeichen. Ob die Lizenz die
kommerzielle Nutzung deckt, ist vor der Veröffentlichung zu klären; die hier
konstruierte Fassung ist eine Neuzeichnung, keine Kopie der Datei.

## Bilder

Bis auf die beiden Porträts ist **kein Bild mehr ein Bild**. Alle Flächen sind
gezeichnet: scharf in jeder Grösse, in jedem Fall wenige Kilobyte.

| Fläche | vorher | jetzt |
|---|---|---|
| Hero-Hintergrund | Render 1376×768 | axonometrisches Relieffeld, `make_grafik.py` |
| Systembild Leistungen | Render 1376×768 | Netz aus Knoten und Kanten, `make_grafik.py` |
| Bildband | Foto 1376×768 | Lichthof in Zentralperspektive, `make_band.py` |
| Schwebende Körper | vier Ausschnitte eines Bildes | CSS-Verläufe, ohne Bilddaten |
| Vorschau im Intro | Ausschnitt des Hero-Bildes | CSS-Verlauf |
| Porträts | Fotos | Fotos — das bleiben sie |

Das hat die Dateien um **rund 400 KB** leichter gemacht und das Thema
Auflösung erledigt: Vektoren kennen keine zu kleine Vorlage.

### Bildband

Eine echte **Zentralperspektive**, keine geschobenen Flächen. Körper werden im
Raum beschrieben und projiziert, deshalb fluchten alle Kanten von selbst auf
denselben Punkt, die Fenstersprossen stehen im richtigen Abstand, und jede
Fläche bekommt ihren Ton aus ihrer Lage: oben hell, zur Fensterwand heller,
unten dunkel.

Die erste Fassung war flach und blass, weil sie aus Parallelogrammen bestand
statt aus Körpern. Man sah es, ohne sagen zu können, woran es liegt.

Die Person steht für den Massstab. Ohne sie verliert der Raum seine Grösse.

### Hero-Hintergrund

Ein Feld aus niedrigen Körpern in Axonometrie — kein Gegenstand, sondern eine
Fläche mit Relief. Die Höhen kommen aus einer glatten Funktion, nicht aus
Zufall; deshalb wirkt das Feld geordnet und nicht gewürfelt. Nach links hin
löst es sich auf, damit der Text freien Grund hat.

### Systembild

Ein Netz aus Knoten und Verbindungen, drei davon rot. Es zeigt, wovon der
Abschnitt handelt — verbundene Systeme — und ist als Zeichnung präziser, als
ein Renderbild es je war. Die Lage der Knoten kommt aus einer festen
Zahlenfolge: zwei Läufe ergeben dasselbe Bild.

```
python3 make_band.py      # das Bildband
python3 make_grafik.py    # Hero und Systembild
python3 build.py
```

## Beitrag

Ein eigener Abschnitt zwischen «Über uns» und dem Newsletter-Streifen:
zehn Prozent des Umsatzes gehen an gute Zwecke.

Links steht das Mass — zehn Felder, eines davon rot — rechts die Aussage. Der
Gedanke dahinter: eine Behauptung, die man nachzählen kann, wiegt mehr als eine,
die man glauben muss. Die Felder sind reines CSS und `aria-hidden`; blinde
Leser bekommen dieselbe Information aus dem Text daneben.

Der Ort ist bewusst gewählt. Die Aussage gehört zum Unternehmen, also hinter
dessen Vorstellung. Direkt nach den Paketen läse sie sich als Verkaufsargument
und entwertete sich damit; im Footer wirkte sie wie ein Nachgedanke.

## Detailansichten der Leistungen

Jede der sechs Leistungszeilen führt auf eine eigene Ansicht unter
`#leistung/<slug>`: `website-marke`, `wartung-hosting`, `kundenmanagement`,
`anfragen-leads`, `kundenportal`, `kommunikation`.

Sichtbar macht sie **`:target`**, also der Browser selbst. Daraus folgt einiges
umsonst: eigene Adresse, Zurück und Vorwärts, Deep-Link — und alles davon auch
dann, wenn kein Skript läuft. Der Schrägstrich in der Kennung ist Absicht; er
trifft keine normale Element-Kennung, der Browser springt also nicht daneben.
Im CSS steht deshalb `.svc-detail:target`, nie die Kennung selbst.

Das Skript ergänzt nur, was CSS nicht kann: die Seite darunter stillhalten
(`body.detail-offen`), die Scrollposition bewahren, den Fokus in die Ansicht
setzen und dort halten, Escape.

Die Scrollposition liegt im Verlaufseintrag (`history.replaceState`), nicht in
einer Variablen. Nur so findet sie auch nach Zurück und Vorwärts an dieselbe
Stelle zurück.

Die ganze Zeile ist ein `<a>`, nicht nur der Pfeil. Damit sind Hover, Fokus und
Tastaturbedienung ohne Zutun richtig.

Jede Ansicht ist ein abgeschlossenes `<article>`. Für echte Unterseiten wird es
später unverändert in eine eigene Datei gehoben; die Slugs sind schon die
Adressen.

## Bedienelemente ohne Skript

Eine lokale Datei wird nicht überall in einem vollen Browser geöffnet — die
Dateivorschau auf dem Telefon führt kein JavaScript aus. Dort standen zuerst
Sprachumschalter, Menü und Pop-up still, während der Rest der Seite lief.

Alle drei hängen jetzt an unsichtbaren Eingabefeldern ganz oben im Dokument,
die CSS über `:has()` ausliest:

| Feld | steuert |
|---|---|
| `#lang-de` / `#lang-en` | welche Sprachfassung sichtbar ist |
| `#nav-auf` | das Menü auf schmalen Fenstern |
| `#nl-auf` | das Newsletter-Pop-up |

Die sichtbaren Knöpfe sind `<label>`-Elemente dazu. Läuft ein Skript, liest es
dieselben Felder und setzt zusätzlich eine Klasse am `<html>` — für Browser,
die `:has()` noch nicht können, und weil sich daran leichter weitere Regeln
hängen. Beide Regelsätze stehen im Stylesheet **getrennt** und nicht als
Liste: ein Browser ohne `:has()` würde sonst auch die Klassenregel daneben
verwerfen.

Die Felder stehen `position:fixed` am Fensterrand. Stünden sie im normalen
Fluss am Dokumentanfang, holte der Browser sie beim Fokussieren ins Bild und
die Seite spränge beim Umschalten nach oben.

**Eine Einschränkung bleibt:** ohne Skript schliesst sich das Menü nicht von
selbst, wenn man einen Punkt darin wählt. Die Seite springt zum Abschnitt, das
Menü bleibt offen, bis man das Kreuz antippt. CSS kann ein Ankreuzfeld nicht
von einem Verweis aus zurücksetzen.

## Sprachen

Deutsch und Englisch sind gleichrangig. Englisch ist keine Übersetzung, sondern
eigener Text in britischer Schreibung; `lang` steht entsprechend auf `en-GB`
oder `de-CH`.

**Beide Fassungen stehen im Dokument.** Jede übersetzte Stelle trägt zwei
Kinder, sichtbar ist immer genau eines:

```html
<h2><span class="t" lang="de-CH">Klein, persönlich, verlässlich.</span>
    <span class="t" lang="en-GB">Small, personal, reliable.</span></h2>
```

Vorher tauschte JavaScript den Text aus. Das funktionierte — aber eben nur mit
JavaScript. Jetzt macht es CSS, und für die Sprache ist kein Skript mehr nötig.

Was CSS nicht erreicht, bleibt beim Skript: Platzhalter in Formularfeldern
(`data-en-placeholder`), Vorlesetexte (`data-en-aria`) und Bildbeschreibungen
(`data-en-alt`). Ohne Skript bleiben diese drei deutsch; sichtbarer Fliesstext
ist davon nicht betroffen.

Die Startsprache kommt aus `navigator.language` (`de*` → Deutsch, sonst
Englisch), die Wahl liegt im `sessionStorage` und bleibt für die Sitzung.

**Die Scrollposition** bleibt beim Umschalten erhalten, aber nicht als Zahl:
Englisch braucht für denselben Inhalt andere Zeilenzahlen. Gemerkt wird
deshalb, welcher Abschnitt gerade oben steht; nach dem Tausch wird er wieder
an dieselbe Stelle gesetzt.

**Der Zeilensatz der Überschriften** wird beim Wechsel zurückgebaut und neu
gemessen — und ausserdem, sobald die Schrift geladen ist. Wird gegen die
Ersatzschrift gemessen, bricht die Überschrift sonst anders um als nach einem
Neuladen.

Das **Intro bleibt deutsch**. Es ist ein Zeitstück, eine deutsche Website von
1999; eine englische Fassung wäre eigene Textarbeit, kein Übersetzen.

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

- **Freigestelltes Teamfoto**: die Stelle in «Über uns» ist vorbereitet, aber
  inaktiv. Gebraucht wird ein Bild von beiden, bei dem der Hintergrund
  entfernt ist. Ein Versuch, stattdessen die vorhandenen Porträts
  abgeschwächt in den Hintergrund zu legen, wurde verworfen: bei zehn Prozent
  Deckkraft sieht man nichts, bei mehr steht ein Schleier hinter Karten, die
  dieselben Gesichter schon scharf zeigen.
- **Unterstützte Organisationen** im Abschnitt «Beitrag» sind noch offen;
  `[Platzhalter: unterstützte Organisationen]` steht sichtbar auf der Seite.
- **Lizenz des Zeichens** klären, siehe **Zeichen**.
- **Referenzen** sind Beispielinhalte. Die Firmennamen beginnen mit «Muster», die
  Sektion weist im Vorspann darauf hin.
- **Impressum und Datenschutz** sind Entwürfe. Handelsregistereintrag, UID-Nummer
  und vertretungsberechtigte Personen fehlen; beide Texte gehören juristisch geprüft.
  Ein Hinweis darauf steht sichtbar über den beiden Spalten.

## Porträts

Die beiden Porträts sind die einzigen Fotos, die geblieben sind. Sie stammen
aus Aufnahmen mit 704×1527 und 896×1195; der gemeinsame Ausschnitt gibt
682×853 beziehungsweise 606×757 her. Mehr als 600×750 ist daraus nicht zu
holen, ohne hochzuskalieren. Auf dem Telefon bei dreifacher Pixeldichte bleibt
das knapp. Besser wird es nur mit neuen Aufnahmen.

Eingebunden sind sie als `<picture>` mit zwei Grössen, gesetzter `width` und
`height` und `loading="lazy"`.

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
Ausschnitt sowie drei Hintergründe: `bg-geometrie.jpg` (Hero, gespiegelt, damit
der Text links freien Grund hat), `bg-objekte.jpg` (die schwebenden Objekte)
und `bg-netzwerk.jpg` (Abschnittskopf der Leistungen). Das Bildband ist kein
Foto mehr, sondern gezeichnet — siehe **Bildband**.

`crop_portraits.py` schneidet die beiden Porträts auf dasselbe Hochformat 4:5
zu, mit gleicher Kopfgrösse und gleicher Kinnhöhe:

```
python3 crop_portraits.py
```

Die Ausschnitte liegen anschliessend als `assets/team-1.jpg` und `assets/team-2.jpg`
und sind in `index.html` als Datenkanal eingebettet.

## Entwürfe

`stitch_apicreative_website_evolution_journey.zip` enthält die vier Stitch-Entwürfe
und die DESIGN.md, aus denen die Seite entstanden ist. Der entpackte Ordner ist per
`.gitignore` ausgenommen.
