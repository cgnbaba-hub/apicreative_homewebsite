# apicreative_homewebsite

Website der Webagentur apicreative, Zürich.

## Dateien

| Datei | Grösse | Intro | Internet nötig | Wofür |
|---|---|---|---|---|
| `index.html` | 277 KB | ja | ja | Quelle. Bibliotheken und Schrift per CDN. |
| `apicreative-praesentation.html` | 530 KB | ja | nein | Zum Verschicken und Vorführen. |
| `apicreative-ohne-intro.html` | 384 KB | nein | nein | Nur die moderne Seite, ohne Animation. |

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

Sticky-Header mit DE/EN-Umschalter · Hero · Leistungen · Vorgehen · Pakete ·
Referenzen (ausgeblendet) · Über uns · Gratis Website-Check · Newsletter · Kontakt ·
Footer. Dazu ein Newsletter-Pop-up ab 60 % Scrolltiefe oder bei Exit-Intent auf dem
Desktop, einmal pro Sitzung.

Die Referenzen-Sektion liegt fertig im Markup, ist aber ausgeblendet. Einblenden:
`class="is-hidden"` an `<section id="referenzen">` entfernen oder im Skript
`SHOW_REFERENCES = true` setzen.

Es ist ein Prototyp ohne Backend. Die Formulare prüfen die Eingaben und zeigen eine
Erfolgsmeldung, versenden aber nichts. Namen, Zahlen und Kontaktdaten stehen als
sichtbare `[Platzhalter]` in der Seite, ebenso die längeren englischen Texte.

## Ändern und neu erzeugen

`index.html` ist die einzige Quelle. Die beiden anderen Dateien werden daraus erzeugt:

```
python3 build.py
```

Nach jeder Änderung an `index.html` ausführen, sonst laufen die Dateien auseinander.
Das Skript prüft zum Schluss, dass die erzeugten Dateien nichts mehr extern nachladen.

`vendor/` enthält die eingebetteten Fremdbestandteile: GSAP 3.12.5 mit ScrollTrigger,
Lenis 1.1.20 und die Schrift Inter 5.3.0 (Zeichensatz Latein, Schnitte 400 bis 700).

## Entwürfe

`stitch_apicreative_website_evolution_journey.zip` enthält die vier Stitch-Entwürfe
und die DESIGN.md, aus denen die Seite entstanden ist. Der entpackte Ordner ist per
`.gitignore` ausgenommen.
