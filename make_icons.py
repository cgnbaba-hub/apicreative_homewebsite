#!/usr/bin/env python3
"""Erzeugt die Tab- und Homescreen-Symbole aus dem Zeichen in index.html.

    python3 make_icons.py

Die Form des Zeichens steht an genau einer Stelle: im <symbol id="i-mark">
im Inline-Sprite. Dieses Skript liest sie von dort und schreibt daraus

    den Favicon-Data-URI (SVG, scharf in jeder Groesse),
    das Homescreen-Symbol fuer iOS (PNG, 180x180),
    das allgemeine Symbol (PNG, 512x512)

zurueck in index.html. So kann der Tab nie ein anderes Zeichen zeigen als
die Seite. Nach einer Aenderung am Zeichen erst dieses Skript laufen lassen,
dann build.py.
"""

import base64
import io
import pathlib
import re
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("make_icons.py: benötigt Pillow (pip install Pillow)")

ROOT = pathlib.Path(__file__).parent
ROT, WARM = (0xDA, 0x29, 0x1C), (0xFF, 0x6A, 0x2B)
GRUND = "#FAFAFA"
SEITE = 64          # Zeichenfläche des Symbols


def fail(msg):
    sys.exit("make_icons.py: " + msg)


def pfade(text):
    """Holt die Pfade aus dem <symbol id="i-mark">."""
    m = re.search(r'<symbol id="i-mark".*?</symbol>', text, re.S)
    if not m:
        fail("<symbol id=\"i-mark\"> nicht gefunden")
    ds = re.findall(r'<path d="([^"]+)"', m.group(0))
    if not ds:
        fail("keine Pfade im Zeichen gefunden")
    return ds


def punkte(d):
    """Nur gerade Strecken: M/L/Z mit absoluten Koordinaten."""
    zahlen = [float(z) for z in re.findall(r'-?\d+(?:\.\d+)?', d)]
    if len(zahlen) % 2:
        fail("ungerade Anzahl Koordinaten in: " + d)
    if re.search(r'[CcSsQqTtAaHhVvmlz]', d.replace('M', '').replace('L', '').replace('Z', '')):
        fail("das Zeichen enthält Kurven oder relative Befehle - "
             "dieses Skript kann nur gerade, absolute Strecken")
    return list(zip(zahlen[0::2], zahlen[1::2]))


def verlauf(kante):
    bild = Image.new("RGB", (kante, kante))
    px = bild.load()
    for y in range(kante):
        for x in range(kante):
            t = (x + y) / (2 * (kante - 1))
            px[x, y] = tuple(round(ROT[i] + (WARM[i] - ROT[i]) * t) for i in range(3))
    return bild


def zeichnen(ds, groesse, rand):
    ueber = 4                                   # vierfach zeichnen, dann verkleinern
    kante = groesse * ueber
    inhalt = kante - 2 * round(rand * kante)
    off = (kante - inhalt) / 2
    maske = Image.new("L", (kante, kante), 0)
    stift = ImageDraw.Draw(maske)
    for d in ds:
        stift.polygon([(off + x / SEITE * inhalt, off + y / SEITE * inhalt)
                       for x, y in punkte(d)], fill=255)
    bild = Image.new("RGB", (kante, kante), GRUND)
    bild.paste(verlauf(kante), (0, 0), maske)
    return bild.resize((groesse, groesse), Image.LANCZOS)


def als_png(bild):
    puffer = io.BytesIO()
    bild.save(puffer, "PNG", optimize=True)
    roh = puffer.getvalue()
    return base64.b64encode(roh).decode(), len(roh)


def svg_uri(ds):
    """Data-URI fuer den Tab. # muss als %23 stehen, auch in url(#g)."""
    stufen = ("<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
              "<stop offset='0' stop-color='%23{:02X}{:02X}{:02X}'/>"
              "<stop offset='1' stop-color='%23{:02X}{:02X}{:02X}'/>"
              "</linearGradient></defs>").format(*ROT, *WARM)
    flaechen = "".join("<path d='%s' fill='url(%%23g)'/>" % d.replace('"', "'") for d in ds)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d'>%s%s</svg>"
            % (SEITE, SEITE, stufen, flaechen))


def ersetzen(text, muster, neu, was):
    treffer = re.findall(muster, text)
    if len(treffer) != 1:
        fail("%s: %d Treffer statt einem" % (was, len(treffer)))
    return re.sub(muster, lambda _: neu, text, count=1)


def main():
    quelle = ROOT / "index.html"
    if not quelle.exists():
        fail("index.html nicht gefunden")
    text = quelle.read_text(encoding="utf-8")
    ds = pfade(text)
    print("Zeichen: %d Flächen aus <symbol id=\"i-mark\">" % len(ds))

    # Homescreen: voller Grund, mehr Luft - iOS legt seine eigene Maske darüber.
    apple, n1 = als_png(zeichnen(ds, 180, 0.16))
    gross, n2 = als_png(zeichnen(ds, 512, 0.10))
    print("  180x180: %5d Bytes" % n1)
    print("  512x512: %5d Bytes" % n2)

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
