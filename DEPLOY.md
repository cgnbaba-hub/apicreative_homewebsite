# Veröffentlichen

Die Website liegt fertig im Ordner **`public/`**. Nur dieser Ordner geht online.

```
public/
  index.html                 die Seite
  _headers                   Vorschau-Schutz (beim Livegang löschen)
  vendor/*.js                GSAP, ScrollTrigger, Lenis
  vendor/*.woff2             die Schrift Inter, vier Schnitte
```

`public/` wird **erzeugt**, nicht von Hand gepflegt. Quelle ist `index.html`
im Hauptordner.

## Nach jeder Änderung

Drei Befehle, immer in dieser Reihenfolge:

```
python3 build.py         # die beiden Einzeldateien zum Verschicken
python3 make_public.py   # den Veröffentlichungsordner neu bauen
npx wrangler pages deploy ./public --project-name apicreative --branch main
```

`make_public.py` bricht ab, wenn etwas nicht stimmt: wenn eine Adresse auf
einen fremden Server zeigt, wenn ein Pfad absolut statt relativ ist, oder
wenn eine Datei fehlt, auf die das Dokument verweist.

## Der einfachste Weg: ZIP hochladen

Ohne Kommandozeile, ohne Anmeldung per Wrangler. Aus `public/` ein ZIP
machen — die Dateien müssen **direkt** im ZIP liegen, nicht in einem Ordner
darin:

```
cd public && zip -r ../apicreative-website.zip . && cd ..
```

Dann im Cloudflare-Dashboard: **Workers & Pages → Create → Pages →
Upload assets**, Projektname `apicreative`, ZIP hineinziehen, **Deploy site**.

Für spätere Änderungen dasselbe Projekt öffnen → **Create new deployment** →
neues ZIP hineinziehen. Die Adresse bleibt gleich, auch die verbundene Domain.

## Das erste Mal

Einmalig, auf Ihrem eigenen Rechner:

```
npx wrangler login
```

Es öffnet sich ein Browserfenster, dort bestätigen. Danach:

```
npx wrangler pages project create apicreative --production-branch main
npx wrangler pages deploy ./public --project-name apicreative --branch main
```

Wrangler nennt Ihnen am Ende die Adresse, etwa
`https://apicreative.pages.dev`.

Haben Sie mehrere Cloudflare-Konten, fragt Wrangler, welches gemeint ist.
Sie können es auch fest vorgeben:

```
export CLOUDFLARE_ACCOUNT_ID=<Konto-Kennung aus dem Dashboard>
```

## Der andere Weg: ohne Kommandozeile

Weil `public/` im Repository liegt, geht es auch ganz ohne Wrangler:

1. Cloudflare-Dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**
2. Repository `cgnbaba-hub/apicreative_homewebsite` wählen
3. **Build command** leer lassen, **Build output directory** auf `public`
4. Production branch auf den gewünschten Zweig setzen

Danach veröffentlicht jeder Push automatisch. `build.py` und
`make_public.py` müssen Sie dann trotzdem vor dem Push laufen lassen, damit
`public/` aktuell ist.

## Beim echten Livegang

Der Vorschau-Schutz muss an **zwei** Stellen weg, sonst bleibt die Seite für
Suchmaschinen unsichtbar:

1. in `index.html` die markierte Zeile
   `<meta name="robots" content="noindex, nofollow">` samt Kommentarblock
2. die Datei `public/_headers` — und den Block `HEADERS` in
   `make_public.py`, sonst schreibt das Skript sie wieder hin

Danach `python3 make_public.py` und neu veröffentlichen.

## Eigene Domain

Im Cloudflare-Dashboard unter dem Pages-Projekt → **Custom domains**. Die
DNS-Einträge bei GoDaddy machen Sie selbst.

**Nicht angefasst wird dabei:** der bestehende Tunnel, bestehende
DNS-Einträge und alle anderen Projekte im Konto. Die Befehle oben sprechen
ausschliesslich das Pages-Projekt `apicreative` an.
