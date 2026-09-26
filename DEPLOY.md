# Veröffentlichen

Live auf **apicreative.ch** läuft der Ordner **`ausgabe/public-ohne-intro/`** —
die Seite ohne Scroll-Intro.

```
ausgabe/public-ohne-intro/
  index.html                 die Seite, mit CRM-Skript
  _headers                   Zwischenspeicher-Regel und Vorschau-Schutz
  vendor/*.woff2             die Schrift Inter, vier Schnitte
```

Der Ordner wird **erzeugt**, nicht von Hand gepflegt. Quelle ist `index.html`.
Daneben liegt `ausgabe/public/`, dieselbe Seite mit Intro; sie ist derzeit nicht
veröffentlicht.

## Wie es eingerichtet ist

- **Cloudflare**, als *Worker mit statischen Dateien* namens `apicreative`
  (Workers & Pages). Statische Abrufe werden nicht abgerechnet.
- Testadresse: `apicreative.cgnbaba.workers.dev`.
- **Eigene Domains** am Worker: `apicreative.ch` und `www.apicreative.ch`.
- Das **DNS von `apicreative.ch`** führt Cloudflare (Nameserver `decker` und
  `norah.ns.cloudflare.com`). Registriert ist die Domain weiterhin bei GoDaddy.
- **`apicreative.com` und `apicreative.net`** bleiben bei GoDaddy und sollen dort
  per Weiterleitung auf `apicreative.ch` zeigen. **Die Nameserver von `.com` nicht
  ändern:** Dort läuft das Postfach `business@apicreative.com` (Microsoft 365).

Nicht angefasst werden der bestehende Tunnel im Cloudflare-Konto und alle anderen
Projekte darin.

## Nach jeder Änderung

Aus der Wurzel des Repositorys:

```
python3 werkzeuge/build.py                       # die beiden Offline-Dateien
python3 werkzeuge/make_public.py --ohne-intro    # den Live-Ordner neu bauen
```

`make_public.py` bricht ab, wenn etwas nicht stimmt: wenn eine Adresse auf einen
fremden Server zeigt (ausser dem CRM-Skript), wenn ein Pfad absolut statt relativ
ist, oder wenn eine Datei fehlt, auf die das Dokument verweist.

Dann den Ordner als ZIP packen. Die Dateien müssen **direkt** im ZIP liegen,
nicht in einem Unterordner darin:

```
cd ausgabe/public-ohne-intro && zip -r ../../apicreative-JJJJ-MM-TT-stichwort.zip . && cd ../..
```

Den Namen immer mit Datum und Stichwort versehen. Mehrere ZIPs mit demselben
Namen führen dazu, dass eine alte Fassung hochgeladen wird.

Hochladen: im Cloudflare-Dashboard den Worker `apicreative` öffnen →
**New deployment** → ZIP hineinziehen. Adresse und Domains bleiben gleich. Weil
`_headers` die Seite nicht zwischenspeichern lässt, ist die neue Fassung sofort
sichtbar; im Zweifel in einem privaten Fenster prüfen.

Eine automatische Veröffentlichung bei jedem Push nach GitHub ist nicht
eingerichtet.

## Beim echten Livegang

Der Vorschau-Schutz hält die Seite aus den Suchmaschinen. Er muss an **zwei**
Stellen weg:

1. in `index.html` die markierte Zeile
   `<meta name="robots" content="noindex, nofollow">` samt Kommentarblock
2. in `werkzeuge/make_public.py` den markierten Teil von `HEADERS`, aus dem
   `_headers` entsteht — die Zwischenspeicher-Regel darüber bleibt

Danach neu bauen und hochladen wie oben.
