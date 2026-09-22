#!/usr/bin/env python3
"""Schneidet die Teamfotos auf einen einheitlichen Ausschnitt zu.

    python3 crop_portraits.py

Beide Bilder bekommen dasselbe Hochformat 4:5, dieselbe relative Kopfgroesse
und dieselbe Kinnhoehe, damit die Karten nebeneinander ruhig wirken.

Als Mass dient die Kieferbreite, gemessen in einem schmalen Band knapp
oberhalb des Kinns. Zwei fruehere Ansaetze taugten nicht: die Anzugfarbe,
weil der eine Anzug taupe und der andere schwarz ist, und die Gesichtshoehe
ab Haaransatz, weil blondes Haar in der Hautmaske mitzaehlt und den Kopf
dadurch zu gross erscheinen laesst. Dicht ueber dem Kinn liegt nie Haar.

Die Messwerte werden beim Lauf ausgegeben, damit sich das Ergebnis
nachvollziehen laesst.
"""

import base64
import io
import pathlib
import re
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("crop_portraits.py: benoetigt Pillow und numpy (pip install Pillow numpy)")

ASSETS = pathlib.Path(__file__).parent / "assets"

SOURCES = [
    ("portrait-1.jpg", "team-1.jpg"),
    ("portrait-2.jpg", "team-2.jpg"),
]

RATIO = 4 / 5        # Breite zu Hoehe
HOEHE = 5.63         # Gesamthoehe des Ausschnitts, in Kieferbreiten
KINN = 0.633         # Hoehe des Kinns, als Anteil der Ausschnitthoehe
OUT_SIZE = (600, 750)
OUT_SMALL = (360, 450)


ROOT_HTML = pathlib.Path(__file__).parent / "index.html"
html = ROOT_HTML.read_text(encoding="utf-8") if ROOT_HTML.exists() else ""


def datenadresse(bild):
    puffer = io.BytesIO()
    bild.save(puffer, "JPEG", quality=88, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(puffer.getvalue()).decode()


def einbetten(nr, gross, klein):
    """Tauscht die beiden Datenadressen der Karte member-photo--nr aus."""
    global html
    muster = re.compile(
        r'(member-photo--%d"><picture class="member-pic"><source media='
        r'"\(max-width:900px\)" srcset=")data:image/jpeg;base64,[^"]*'
        r'("[^>]*><img src=")data:image/jpeg;base64,[^"]*' % nr)
    neu, treffer = muster.subn(
        lambda m: m.group(1) + datenadresse(klein) + m.group(2) + datenadresse(gross),
        html)
    if treffer != 1:
        sys.exit("crop_portraits.py: member-photo--%d %d mal gefunden statt einmal"
                 % (nr, treffer))
    html = neu


def hautmaske(arr):
    """Haut ist warm und mittelhell; Pflanzen und Fenster fallen heraus."""
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    hell = arr.mean(axis=2)
    haut = (r > 95) & (r > g + 14) & (g > b + 4) & (hell > 70) & (hell < 240)
    h, w = haut.shape
    # Nur obere Bildhaelfte, mittlere 60 % der Breite: der Kopf sitzt dort,
    # Haende und Holztoene weiter unten stoeren so nicht.
    maske = np.zeros_like(haut)
    oben, links, rechts = int(h * 0.55), int(w * 0.20), int(w * 0.80)
    maske[:oben, links:rechts] = haut[:oben, links:rechts]
    return maske


def messen(maske):
    """Liefert Kinnhoehe, Kieferbreite und Gesichtsmitte in Pixeln."""
    zeilen = np.nonzero(maske.sum(axis=1) > 20)[0]
    if not len(zeilen):
        sys.exit("crop_portraits.py: kein Gesicht gefunden")
    kinn = int(zeilen[-1])

    band = maske[max(0, kinn - 110):kinn - 40]
    breiten, mitten = [], []
    for zeile in band:
        treffer = np.nonzero(zeile)[0]
        if len(treffer):
            breiten.append(int(treffer[-1] - treffer[0]))
            mitten.append(int((treffer[0] + treffer[-1]) / 2))
    if not breiten:
        sys.exit("crop_portraits.py: kein Kieferband gefunden")
    return kinn, int(np.median(breiten)), int(np.median(mitten))


def main():
    for nr, (quelle, ziel) in enumerate(SOURCES, 1):
        pfad = ASSETS / quelle
        if not pfad.exists():
            sys.exit("crop_portraits.py: fehlt: " + str(pfad))
        im = Image.open(pfad).convert("RGB")
        arr = np.asarray(im).astype(int)
        kinn, kiefer, cx = messen(hautmaske(arr))

        hoehe = HOEHE * kiefer
        breite = hoehe * RATIO
        top = kinn - KINN * hoehe
        left = cx - breite / 2

        # In das Bild hineinschieben, falls eine Kante ueberlaeuft.
        breite, hoehe = min(breite, im.width), min(hoehe, im.height)
        left = max(0, min(left, im.width - breite))
        top = max(0, min(top, im.height - hoehe))
        box = (round(left), round(top), round(left + breite), round(top + hoehe))

        gross = im.crop(box).resize(OUT_SIZE, Image.LANCZOS)
        gross.save(ASSETS / ziel, quality=88, optimize=True, progressive=True)
        klein = im.crop(box).resize(OUT_SMALL, Image.LANCZOS)

        einbetten(nr, gross, klein)
        print("%s: Kinn y=%d, Kieferbreite %dpx, Mitte x=%d -> %s  %s"
              % (quelle, kinn, kiefer, cx, box, ziel))

    ROOT_HTML.write_text(html, encoding="utf-8")
    print("index.html: beide Portraets ersetzt")


if __name__ == "__main__":
    main()
