# Arbeitsanleitung für dieses Projekt

Diese Datei ist für die nächste Sitzung geschrieben — für einen Assistenten,
der dieses Repository zum ersten Mal sieht, und für die Menschen, die mit ihm
arbeiten. Sie hält fest, was gilt, was sich bewährt hat und welche Fehler
schon gemacht wurden. Wer sie liest, spart die Umwege.

## Was das hier ist

Die Website der Webagentur **apicreative**, Zürich. Eine einzelne, in sich
geschlossene HTML-Datei, zweisprachig Deutsch/Englisch, ohne Baukasten und
ohne Rahmenwerk. Gegründet 2026, zwei Personen: Peter (CEO), Jason (CTO).

## Unverrückbare Regeln

Diese Vorgaben kommen vom Auftraggeber und gelten für jeden Text, jedes Bild
und jede Codezeile. Sie sind mehrfach bestätigt worden.

- **Keine erfundenen Zahlen.** Keine Prozentwerte, Fallzahlen, Umsätze,
  Projektzahlen. Keine Garantien, Reaktionszeiten, Zertifizierungen, Preise.
- **Keine erfundenen Referenzen.** Keine Kundennamen, Logos, Testimonials,
  Auszeichnungen, Standorte. Der Referenzabschnitt trägt bewusst
  Musternamen und einen Satz, der ihn als Beispiel kennzeichnet. Ein
  Schalter `SHOW_REFERENCES` im Skript blendet ihn aus.
- **White Label.** Keine Namen von Drittanbietern — auch nicht in
  Kommentaren, Alt-Texten oder Dateinamen.
- **Keine Rechtsform.** Nie „AG", nie „GmbH". Nur „apicreative".
- **Schweizer Rechtschreibung.** „ss" statt „ß", überall. Englisch in
  britischer Schreibweise (`organisation`, `programme`) — mit einer
  bewussten Ausnahme: **`percent`, nicht `per cent`.**
- **Platzhalter sichtbar machen.** Was noch fehlt, steht als
  `[Platzhalter: …]` in der Seite, nicht als stille Lücke.
- **Ton:** souverän, präzise, diskret, zurückhaltend. Kurze Sätze. Keine
  Superlative, keine Ausrufezeichen, kein Agentursprech.

## Aufbau

`index.html` ist die **einzige Quelle**. Alles andere wird daraus erzeugt.
Nie eine abgeleitete Datei von Hand ändern — sie wird beim nächsten Lauf
überschrieben.

```
index.html                     Quelle. Mit Intro, Bibliotheken per CDN.
  │
  ├─ build.py                  → apicreative-praesentation.html  (offline, mit Intro)
  │                            → apicreative-ohne-intro.html     (offline, ohne Intro)
  │
  └─ make_public.py            → public/            (mit Intro, für den Webserver)
     make_public.py --ohne-intro → public-ohne-intro/ (ohne Intro)
```

Die Grafiken sind nicht fotografiert, sondern gerechnet. Jedes Skript
schreibt sein Ergebnis direkt in `index.html`:

| Skript | erzeugt |
|---|---|
| `make_icons.py` | Wort-Bild-Marke aus drei Zahlen, Favicon, Touch-Icons |
| `make_band.py` | Gebäudeband in Zentralperspektive |
| `make_grafik.py` | Reliefeld und Knotennetz |
| `crop_portraits.py` | Teamfotos zuschneiden **und einbetten** |

`build.py` prüft am Ende selbst: keine externen Abrufe, keine offenen
CSS-Kommentare. `make_public.py` prüft zusätzlich, dass jeder örtliche Pfad
existiert und relativ ist. Diese Prüfungen haben mehrfach etwas gefangen —
nicht abschalten.

## Die Bedingung, die alles geprägt hat

**Der Auftraggeber testet, indem er die Datei aus der Dateien-App auf dem
iPhone öffnet. Dort läuft kein JavaScript.**

Das ist der wichtigste Satz in dieser Datei. Er hat die gesamte Architektur
bestimmt. Jede interaktive Funktion musste ohne Skript funktionieren:

- **Bewegung:** CSS-Animationen plus `animation-timeline: view()`,
  abgesichert über `@supports`. Eine `html.nojs`-Klasse schaltet die
  skriptfreie Schicht.
- **Detailansichten:** `:target` mit IDs, die einen Schrägstrich enthalten
  (`leistung/website-marke`). Der Browser liefert damit URL, Zurück-Taste
  und Direktlinks von selbst.
- **Sprache, Menü, Pop-up:** versteckte `<input>`-Elemente ganz oben im
  `<body>`, gelesen über `:has()`. Die sichtbaren Knöpfe sind `<label>`.
- **Festhalten im Abschnitt „Vorgehen":** `position: sticky` plus eine
  benannte `view-timeline`.

Eine Grenze bleibt und ist dokumentiert: Ohne Skript schliesst sich das
mobile Menü nicht von selbst, wenn man einen Eintrag wählt.

**Wenn eine neue Funktion dazukommt: zuerst fragen, ob sie ohne JavaScript
geht. Meistens geht sie.**

## Fallen, die mehrfach zugeschlagen haben

### Spezifität in CSS

Die häufigste Fehlerquelle im ganzen Projekt. Drei echte Fälle:

- `.choice span` traf nach dem Umbau auf Zweisprachigkeit **auch die beiden
  Übersetzungs-`<span>`**, die in jedem Element stecken. Ergebnis: doppelter
  Rahmen um jedes Formularkästchen. Richtig ist `.choice > span`.
- `.main-nav{position:relative}` stand weiter unten im Stylesheet und schlug
  damit das `position:absolute` aus der Media Query. Das offene Menü schob
  die Kopfzeilen-Knöpfe aus dem Bild.
- Eine Klasse `.form-note` existierte bereits ungenutzt und kollidierte mit
  einer neuen Regel. Der Hinweistext erschien zentriert in Schreibmaschine.

**Regel daraus:** Seit jedes übersetzte Element zwei innere `<span>` trägt,
ist jeder Selektor, der auf `span`, `i` oder `*` endet, verdächtig. Immer
prüfen, ob der direkte Nachkomme gemeint ist.

### `:has()` und Klassenregeln getrennt schreiben

Beide Regelsätze stehen **in eigenen Blöcken**, nie in einer gemeinsamen
Selektorliste. Ein Browser ohne `:has()` verwirft sonst die ganze Liste —
also auch die Klassenregel, die als Rückfallebene gedacht war.

### Versteckte Formularelemente

Die Sprachumschalter liegen am Dokumentanfang. Solange sie nicht
`position:fixed` waren, sprang die Seite beim Umschalten nach ganz oben,
weil der Browser das fokussierte Element ins Bild holt.

### Abgeleitete Zustände zurücksetzen

Die Überschriften werden für die Einblendanimation in Zeilen zerlegt. Beim
Sprachwechsel muss **jedes** `.t`-Element aus seinem `data-raw` neu
aufgebaut werden, nicht nur das äussere. Sonst sammeln sich die Zeilen an.
Und das Zerlegen erst nach `document.fonts.ready` — sonst bricht es gegen
die Ersatzschrift und sitzt hinterher falsch.

## Arbeitsweise, die sich bewährt hat

**Pull Requests selbst mergen.** Der Auftraggeber hat das ausdrücklich
übertragen: Änderungen gehen als Pull Request nach `main` und werden danach
direkt gemerged, sobald sie geprüft sind. Einen schon gemergten Pull Request
nie weiterverwenden — neue Commits auf den aktuellen `main` setzen und einen
neuen öffnen.

**Messen statt annehmen.** Jede Behauptung über das Ergebnis wurde geprüft:
Kontrastwerte gerechnet, Bildgrössen im Browser ausgelesen, Anfragen
mitgezählt, Scrollpositionen abgefragt, Deckkraft gemessen. Ein Fehler —
die unsichtbare Hauptüberschrift — wurde nur deshalb vor der Auslieferung
gefunden, weil der Transformationswert tatsächlich nachgesehen wurde.

**Eigene Fehler als solche benennen.** Im Verlauf wurde konsequent getrennt:
„das war mein Fehler" gegenüber „das war schon vorher kaputt". Das hat
Vertrauen geschaffen und Suchzeit gespart.

**Gebautes wieder wegwerfen, wenn es nicht trägt.** Zwei Dinge wurden
fertiggestellt, ehrlich beurteilt und entfernt: der Hintergrund aus
verblassten Porträts im Abschnitt „Über uns" (bei 10 % Deckkraft
unsichtbar, darüber ein Schmierfleck) und die Person im Gebäudeband (las
sich auch im zweiten Anlauf als Piktogramm). Der Code steht noch hinter
einem Schalter `PERSON = False`.

**Vor dem Bauen den Plan zeigen**, wenn der Auftraggeber danach fragt. Er
hat das einmal ausdrücklich verlangt und es hat sich gelohnt.

## Was diese Umgebung kann und nicht kann

Das hier hat mehrfach Zeit gekostet. Bitte vorher lesen.

- **Gesperrt sind:** `dash.cloudflare.com`, `api.cloudflare.com`,
  `developers.cloudflare.com`, `*.workers.dev`, Unsplash, Pexels. Der Proxy
  antwortet mit `CONNECT tunnel failed, response 403`.
  **Daraus folgt: Oberflächen und Dokumentationen nie aus dem Gedächtnis
  beschreiben.** Stattdessen sagen, *was* ein Schritt bewirkt, und die
  Zuordnung zum Schirm dem Menschen überlassen. Ein Screenshot vom
  Auftraggeber schlägt jede Erinnerung.
- **DNS-Abfragen gehen.** `pip install dnspython`, dann lässt sich direkt
  bei der Registry nachfragen, ob eine Delegation durchgelaufen ist. Das war
  bei der Domainumstellung deutlich schneller als auf die Bestätigungsmail
  zu warten.
- **Playwright liegt nicht am Standardpfad.** Chromium starten mit
  `executable_path="/opt/pw-browsers/chromium"`. Kein `playwright install`.
- **Testen mit echtem HTTP-Server**, nicht über `file://` — sonst verhalten
  sich relative Pfade und Sicherheitsregeln anders als später live.
  Zusätzlich immer einmal mit `java_script_enabled=False` laufen lassen.

## Fehlerprotokoll

Ehrlich geführt, damit sich dasselbe nicht wiederholt.

### Meine Fehler

| Was | Woran es lag |
|---|---|
| Cloudflare-Knöpfe falsch benannt („Create" statt „Create application") | Aus dem Gedächtnis beschrieben, obwohl die Doku gesperrt ist. Mehrfach passiert. |
| Behauptet, öffentliche URLs erreichen zu können | Stimmte für `*.workers.dev` nicht. Vor einer Zusage prüfen, nicht danach. |
| Dreimal eine Datei mit demselben Namen geschickt | Der Auftraggeber lud eine alte Fassung hoch und suchte den Fehler bei sich. **Ausgelieferte Dateien immer eindeutig benennen**, mit Datum oder Stichwort. |
| Die Zuordnung der Teamfotos geraten | Aus der Anhangreihenfolge geschlossen statt zu fragen. Sie war vertauscht. Quelldateien heissen jetzt `portrait-peter.jpg` / `portrait-jason.jpg`. |
| `.choice span` statt `.choice > span` | Die Folgen des Zweisprachen-Umbaus nicht zu Ende gedacht. |
| `querySelector('#leistung/…')` warf eine Ausnahme | Ein Schrägstrich in einer ID ist in HTML erlaubt, in einem CSS-Selektor nicht. |

### Was uns gemeinsam Zeit gekostet hat

| Was | Besser |
|---|---|
| Bilder waren als Anhang angekündigt, kamen aber nicht mit | Kurz gegenprüfen, ob der Anhang wirklich dran ist |
| `apicreative.com` eingetippt, Domain ist `.ch` | Beides gehört der Firma, aber nur `.ch` war eingerichtet |
| Die alte ZIP-Datei hochgeladen | Siehe oben: mein Namensproblem, nicht Ihres |
| „Da stimmt was nicht" ohne Beschreibung | Ein Satz dazu, was auf dem Schirm steht, spart eine ganze Rückfrage |

## Betrieb

Die Seite läuft als **Cloudflare Worker mit statischen Dateien** — das ist
Cloudflares aktueller Weg, Pages ist die ältere Schiene. Statische Abrufe
werden nicht abgerechnet; für diese Website fallen keine Hostingkosten an.

- Veröffentlicht wird der Inhalt von `public-ohne-intro/` als ZIP, Dateien
  in der Wurzel, nicht in einem Unterordner.
- Domain `apicreative.ch`: DNS bei Cloudflare (Nameserver `decker` und
  `norah.ns.cloudflare.com`), Registrierung weiterhin bei GoDaddy. `.com`
  und `.net` gehören der Firma ebenfalls und sollen auf `.ch` zeigen.
- Der einzige DNS-Eintrag aus der GoDaddy-Zeit, der bei `.ch` bleiben
  musste, ist `TXT _dmarc`. **Auf `apicreative.ch` läuft kein
  E-Mail-Empfang** — deshalb war der Umzug risikoarm.
- **Auf `apicreative.com` läuft dagegen das Postfach** `business@apicreative.com`:
  Microsoft 365 über GoDaddy (`MX` → `apicreative-com.mail.protection.outlook.com`,
  `autodiscover` → Outlook, SPF `include:secureserver.net -all`). Diese
  Adresse steht auf der Website und ist die Rückfallebene der Formulare.
  **Vor jeder DNS-Änderung an `.com` alle Einträge sichern** — ein
  verlorener MX-Eintrag legt die Firmen-Mail still, ohne Fehlermeldung.
- `apicreative.net` hat keine Mail.
- **CRM-Anbindung.** `make_public.py` setzt vor `</body>` das Tracking-Skript
  des CRM ein (Kennung in `CRM_KENNUNG`). Es zählt Seitenaufrufe und legt
  aus jedem abgeschickten Formular einen Kontakt an. Es kommt **nur** in
  `public/` und `public-ohne-intro/`, nie in die Offline-Fassungen.
  `--debug` schaltet seine Konsolenmeldungen ein, nur zum Prüfen.
  Anforderungen des CRM an Formulare: echtes `<form>`, jedes Feld mit
  `name`, E-Mail als `type="email" name="email"`, Absenden über
  `type="submit"`, und das `submit`-Ereignis darf nicht blockiert werden —
  nur `preventDefault` ist erlaubt. Ungültige Eingaben und Bots hält
  `stopImmediatePropagation` zurück.
- **Formulare.** Ein verstecktes Feld `quelle` (`anfrage` / `newsletter`)
  sagt dem CRM, woher ein Kontakt kommt. Ein unsichtbares Feld
  `firmenseite` ist eine Falle für Bots. Lädt das CRM-Skript nicht
  (Werbeblocker, offline), öffnet das Formular das E-Mail-Programm mit
  vorausgefüllter Nachricht an `business@apicreative.com`.
- `_headers` enthält zweierlei: `no-cache` für die Seite selbst, damit ein
  neues Deployment sofort sichtbar ist, und den Vorschau-Schutz.

## Noch offen

- **Erster echter Formulartest im CRM** steht aus: In den CRM-Einstellungen
  müssen „Form Analytics" und „Form Submissions" eingeschaltet sein. Danach
  eine Testanfrage absenden und prüfen, ob der Kontakt mit dem Feld
  `quelle` ankommt.
- **Newsletter-Versand aus dem CRM** unter `@apicreative.com`: Der
  SPF-Eintrag endet auf `-all` und kennt nur GoDaddy. Bevor das CRM in
  diesem Namen Mails verschickt, braucht es eine eigene Absenderdomain im
  CRM oder einen angepassten SPF-/DKIM-Eintrag — sonst landet der
  Newsletter im Spam.
- **`.com` und `.net` auf `.ch` weiterleiten.** Empfohlen: die
  Weiterleitung bei GoDaddy („Forward only", nicht „masking"), weil sie
  die Nameserver von `.com` und damit das Postfach nicht berührt.
- **Vorschau-Schutz entfernen** beim Livegang, an zwei Stellen: die Zeile
  `<meta name="robots">` in `index.html` und der markierte Block in
  `make_public.py`, aus dem `_headers` entsteht.
- **Auf dem Handy ist die Bildquelle knapp** — 360 px für 348 px Anzeige.
  Bis 648 px ginge ohne Hochrechnen.
- **Datenschutzerklärung** nennt den CRM-Dienstleister nur als Kategorie
  („Dienstleister für Kundenmanagement und Marketing", Bearbeitung auch in
  den USA) — so bleibt der White-Label-Grundsatz gewahrt. Juristisch prüfen
  lassen, ob das genügt und ob für Besucher aus der EU eine Einwilligung
  nötig ist.
- **Bei 320 px Breite ist die Seite 384 px breit** und scrollt seitlich.
  Ursache ist eine der gezeichneten Grafiken (`<polygon>` ragt heraus).
  Ab 390 px, also bei allen aktuellen iPhones, tritt es nicht auf.
- **Referenzen:** Musternamen oder ausblenden. Erfundene Firmennamen wurden
  vorgeschlagen und begründet abgeraten.
- **Rechtstexte** (Impressum, Datenschutz) sind Entwürfe und brauchen eine
  juristische Durchsicht. Die Lizenz der Logo-Vorlage ist ungeklärt.
- **Freigestelltes Teamfoto** ist als Platzhalter markiert.
