#!/usr/bin/env python3
"""Konstruiert das Zeichen und schreibt es in index.html.

    python3 make_icons.py

Das Zeichen wird nicht gezeichnet, sondern gerechnet. Es folgt aus drei
Zahlen (RAND, BAND, SPITZE_INNEN) und hat deshalb Eigenschaften, die man
von Hand nur mühsam trifft:

    * Es ist spiegelsymmetrisch zur Mittelachse.
    * Es kennt nur zwei Kantenwinkel, dazu die Grundlinie.
    * Das Band des Chevrons ist überall gleich breit, senkrecht gemessen.
    * Die Spalte zwischen Chevron und innerer Fläche ist überall gleich
      breit, weil beide Kanten parallel laufen.
    * Der Abstand zu allen vier Rändern der Zeichenfläche ist gleich.

Geschrieben werden daraus, alle aus derselben Quelle:

    das <symbol id="i-mark"> im Inline-Sprite (Kopf, Footer),
    der Favicon-Data-URI (SVG, scharf in jeder Größe),
    das Homescreen-Symbol für iOS (PNG, 180x180),
    das allgemeine Symbol (PNG, 512x512).

Nach einer Änderung erst dieses Skript laufen lassen, dann build.py.
"""

import base64
import io
import math
import pathlib
import re
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("make_icons.py: benötigt Pillow (pip install Pillow)")

ROOT = pathlib.Path(__file__).parent

SEITE = 64.0          # Zeichenfläche
RAND = 7.0            # Abstand zu allen vier Kanten
BAND = 10.5           # Breite des Chevrons, senkrecht gemessen
SPITZE_INNEN = 42.8   # y der Spitze der inneren Fläche

ROT, WARM = (0xDA, 0x29, 0x1C), (0xFF, 0x6A, 0x2B)
GRUND = "#FAFAFA"


def fail(msg):
    sys.exit("make_icons.py: " + msg)


def flaechen():
    """Die beiden Polygone des Zeichens, dazu die Maße zum Nachrechnen."""
    cx = SEITE / 2
    oben, unten = RAND, SEITE - RAND
    halb = cx - RAND                       # halbe Breite an der Grundlinie
    hoch = unten - oben
    kante = math.hypot(halb, hoch)         # Länge einer Außenkante

    def versetzt(tiefe):
        """Die um <tiefe> senkrecht nach innen versetzte Kontur."""
        return oben + tiefe * kante / halb, halb - tiefe * kante / hoch

    spitze_band, halb_band = versetzt(BAND)
    tiefe_innen = (SPITZE_INNEN - oben) * halb / kante
    spitze_i, halb_i = versetzt(tiefe_innen)
    spalt = tiefe_innen - BAND
    if spalt <= 0:
        fail("SPITZE_INNEN liegt zu hoch: die innere Fläche berührt das Band")
    if halb_i <= 0:
        fail("SPITZE_INNEN liegt zu tief: die innere Fläche verschwindet")

    chevron = [(cx, oben), (cx + halb, unten), (cx + halb_band, unten),
               (cx, spitze_band), (cx - halb_band, unten), (cx - halb, unten)]
    innen = [(cx, SPITZE_INNEN), (cx + halb_i, unten), (cx - halb_i, unten)]
    return [chevron, innen], dict(spalt=spalt, band=BAND, kante=kante,
                                  spitze_band=spitze_band)


def als_d(punkte):
    return "M" + " ".join("%g %g" % (round(x, 2), round(y, 2)) for x, y in punkte) + "Z"


def verlauf(kante):
    bild = Image.new("RGB", (kante, kante))
    px = bild.load()
    for y in range(kante):
        for x in range(kante):
            t = (x + y) / (2 * (kante - 1))
            px[x, y] = tuple(round(ROT[i] + (WARM[i] - ROT[i]) * t) for i in range(3))
    return bild


def zeichnen(polygone, groesse, rand):
    ueber = 4                                   # vierfach zeichnen, dann verkleinern
    kante = groesse * ueber
    inhalt = kante - 2 * round(rand * kante)
    off = (kante - inhalt) / 2
    maske = Image.new("L", (kante, kante), 0)
    stift = ImageDraw.Draw(maske)
    for punkte in polygone:
        stift.polygon([(off + x / SEITE * inhalt, off + y / SEITE * inhalt)
                       for x, y in punkte], fill=255)
    bild = Image.new("RGB", (kante, kante), GRUND)
    bild.paste(verlauf(kante), (0, 0), maske)
    return bild.resize((groesse, groesse), Image.LANCZOS)


def als_png(bild):
    puffer = io.BytesIO()
    bild.save(puffer, "PNG", optimize=True)
    roh = puffer.getvalue()
    return base64.b64encode(roh).decode(), len(roh)


def symbol(ds):
    zeilen = "\n".join('      <path d="%s" fill="url(#markGrad)"/>' % x for x in ds)
    return ('<symbol id="i-mark" viewBox="0 0 %d %d">\n%s\n    </symbol>'
            % (SEITE, SEITE, zeilen))


def svg_uri(ds):
    """Data-URI für den Tab. # muss als %23 stehen, auch in url(#g)."""
    stufen = ("<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
              "<stop offset='0' stop-color='%23{:02X}{:02X}{:02X}'/>"
              "<stop offset='1' stop-color='%23{:02X}{:02X}{:02X}'/>"
              "</linearGradient></defs>").format(*ROT, *WARM)
    pfade = "".join("<path d='%s' fill='url(%%23g)'/>" % x for x in ds)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d'>%s%s</svg>"
            % (SEITE, SEITE, stufen, pfade))


def ersetzen(text, muster, neu, was):
    if len(re.findall(muster, text, re.S)) != 1:
        fail("%s: nicht genau ein Treffer" % was)
    return re.sub(muster, lambda _: neu, text, count=1, flags=re.S)


def main():
    quelle = ROOT / "index.html"
    if not quelle.exists():
        fail("index.html nicht gefunden")
    text = quelle.read_text(encoding="utf-8")

    polygone, mass = flaechen()
    ds = [als_d(p) for p in polygone]
    print("Zeichen konstruiert:")
    print("  Band %.1f, Spalt %.1f, Spitze des Bandes bei y=%.1f"
          % (mass["band"], mass["spalt"], mass["spitze_band"]))
    for x in ds:
        print("  " + x)

    apple, n1 = als_png(zeichnen(polygone, 180, 0.16))
    gross, n2 = als_png(zeichnen(polygone, 512, 0.10))
    print("  Homescreen 180x180: %5d Bytes" % n1)
    print("  Symbol     512x512: %5d Bytes" % n2)

    text = ersetzen(text, r'<symbol id="i-mark".*?</symbol>', symbol(ds), "Sprite-Symbol")
    text = ersetzen(text, r'(?<=href="data:image/svg\+xml,)<svg[^"]*(?=">)',
                    svg_uri(ds), "Favicon-SVG")
    text = ersetzen(text, r'(?<=rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,)[A-Za-z0-9+/=]+',
                    apple, "Homescreen-PNG")
    text = ersetzen(text, r'(?<=sizes="512x512" href="data:image/png;base64,)[A-Za-z0-9+/=]+',
                    gross, "512er-PNG")
    quelle.write_text(text, encoding="utf-8")
    print("index.html aktualisiert - jetzt build.py laufen lassen")


if __name__ == "__main__":
    main()
