#!/usr/bin/env python3
"""Zeichnet die beiden uebrigen Bildflaechen und schreibt sie in index.html.

    python3 werkzeuge/make_grafik.py

Hero-Hintergrund und das Systembild bei den Leistungen waren Renderbilder mit
1376 Pixel Breite. Ueber die volle Fensterbreite gezogen war das zu wenig.
Beide sind jetzt gezeichnet: als Vektor scharf in jeder Groesse, zusammen ein
paar Kilobyte statt ueber hundert.

    Hero        eine axonometrische Gruppe aus Koerpern, ruhig und hell.
                Die Masse liegt rechts, damit der Text links freien Grund hat.
    Systembild  ein Netz aus Knoten und Verbindungen. Es zeigt, wovon der
                Abschnitt handelt - verbundene Systeme - und ist als Zeichnung
                praeziser, als ein Renderbild es je war.

Beide Bilder entstehen aus einer festen Zahlenfolge, nicht aus Zufall: zwei
Laeufe ergeben dasselbe Bild.

Nach einer Aenderung erst dieses Skript laufen lassen, dann build.py.
"""

import math
import pathlib
import re
import sys

# Die Werkzeuge liegen in werkzeuge/, die Quelle eine Ebene hoeher.
ROOT = pathlib.Path(__file__).resolve().parent.parent


# --------------------------------------------------------------- Werkzeug
class Folge:
    """Eine feste Zahlenfolge. Sieht zufaellig aus, ist es aber nicht."""

    def __init__(self, saat=20260921):
        self.x = saat

    def __call__(self, a=0.0, b=1.0):
        self.x = (1103515245 * self.x + 12345) % 2147483648
        return a + (b - a) * self.x / 2147483648.0


def poly(punkte, fuellung, o=None):
    d = " ".join("%.1f,%.1f" % q for q in punkte)
    return '<polygon points="%s" fill="%s"%s/>' % (d, fuellung, ' opacity="%s"' % o if o else "")


# ------------------------------------------------------------------- Hero
HB, HH = 1600.0, 900.0
HELL, MITTE, TIEF = "#FCFBF8", "#EAE5DC", "#D5CEC0"
SCHATTEN = "#C9C2B4"


def iso(x, y, z, ox, oy, s):
    """Axonometrie: x nach rechts hinten, z nach links hinten, y nach oben."""
    return (ox + (x - z) * 0.866 * s, oy + (x + z) * 0.5 * s - y * s)


def koerper(x, z, bx, bz, hoehe, ox, oy, s, ton=None):
    """Ein liegender Quader. Drei Flaechen, drei Toene - das reicht fuer Koerper."""
    oben, links, rechts = ton or (HELL, MITTE, TIEF)
    e = lambda X, Y, Z: iso(X, Y, Z, ox, oy, s)
    o = [e(x, hoehe, z), e(x + bx, hoehe, z), e(x + bx, hoehe, z + bz), e(x, hoehe, z + bz)]
    l = [e(x, hoehe, z + bz), e(x + bx, hoehe, z + bz), e(x + bx, 0, z + bz), e(x, 0, z + bz)]
    r = [e(x + bx, hoehe, z), e(x + bx, hoehe, z + bz), e(x + bx, 0, z + bz), e(x + bx, 0, z)]
    return poly(l, links) + poly(r, rechts) + poly(o, oben)


def hero():
    """Ein Feld aus niedrigen Koerpern, axonometrisch.

    Kein Gegenstand, sondern eine Flaeche mit Relief: sie fuellt die rechte
    Bildhaelfte ruhig aus, statt als Objekt in der Ecke zu sitzen. Die Hoehen
    kommen aus einer glatten Funktion, nicht aus Zufall - deshalb wirkt das
    Feld geordnet und nicht gewuerfelt.
    """
    OX, OY, S = 940.0, 300.0, 66.0
    N = 13
    teile = ['<rect width="%g" height="%g" fill="url(#hgrund)"/>' % (HB, HH)]

    def hoehe(i, j):
        u, v = i / (N - 1.0), j / (N - 1.0)
        w = 0.5 + 0.5 * math.sin(u * 5.1 + 0.7) * math.cos(v * 4.3 - 0.4)
        return 0.10 + 1.70 * w * w

    felder = [(i, j) for i in range(N) for j in range(N)]
    felder.sort(key=lambda k: k[0] + k[1])
    for i, j in felder:
        h = hoehe(i, j)
        # Was weiter hinten liegt, tritt zurueck: weniger Kontrast, heller
        fern = 1.0 - (i + j) / (2.0 * (N - 1))
        misch = lambda c1, c2, t: "#%02X%02X%02X" % tuple(
            round(int(c1[k:k+2], 16) + (int(c2[k:k+2], 16) - int(c1[k:k+2], 16)) * t)
            for k in (1, 3, 5))
        oben = misch(HELL, "#FFFFFF", fern * 0.8)
        links = misch(MITTE, "#F7F4EF", fern * 0.85)
        rechts = misch(TIEF, "#EDE9E1", fern * 0.85)
        teile.append(koerper(i * 0.92 - 6, j * 0.92 - 6, 0.84, 0.84, h, OX, OY, S,
                             (oben, links, rechts)))

    # Ein einziger roter Strich auf einer Kante, als Akzent
    e1 = iso(2 * 0.92 - 6, hoehe(2, 8) , 8 * 0.92 - 6, OX, OY, S)
    e2 = iso(2 * 0.92 - 6 + 0.84, hoehe(2, 8), 8 * 0.92 - 6, OX, OY, S)
    teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#DA291C" '
                 'stroke-width="2.6" opacity=".75" stroke-linecap="round"/>'
                 % (e1[0], e1[1], e2[0], e2[1]))

    defs = ('<defs>'
            '<linearGradient id="hgrund" x1="0" y1="0" x2="0.5" y2="1">'
            '<stop offset="0" stop-color="#FDFCFA"/><stop offset="1" stop-color="#EFEBE3"/>'
            '</linearGradient>'
            '<linearGradient id="hduft" x1="0" y1="0" x2="1" y2="0.35">'
            '<stop offset="0" stop-color="#FAFAFA" stop-opacity=".92"/>'
            '<stop offset=".45" stop-color="#FAFAFA" stop-opacity="0"/></linearGradient>'
            '</defs>')
    # Nach links hin verliert sich das Feld, damit der Text dort freien Grund hat
    teile.append('<rect width="%g" height="%g" fill="url(#hduft)"/>' % (HB, HH))
    return ('<svg class="hero-pic" viewBox="0 0 %g %g" preserveAspectRatio="xMidYMid slice" '
            'focusable="false" aria-hidden="true">%s%s</svg>'
            % (HB, HH, defs, "".join(teile)))


# -------------------------------------------------------------- Systembild
NB, NH = 800.0, 450.0


def netz():
    z = Folge(7731)
    knoten = []
    # Gestoertes Raster: gleichmaessig verteilt, aber nicht gleichfoermig
    for sp in range(7):
        for ze in range(4):
            x = 70 + sp * 110 + z(-34, 34)
            y = 70 + ze * 103 + z(-30, 30)
            t = z()                       # Tiefe: steuert Groesse und Deckkraft
            knoten.append((x, y, 2.6 + 3.4 * t, 0.30 + 0.55 * t))
    # Jeder Knoten verbindet sich mit seinen zwei naechsten Nachbarn
    kanten = set()
    for i, a in enumerate(knoten):
        d = sorted(((math.dist(a[:2], b[:2]), j) for j, b in enumerate(knoten) if j != i))
        for _, j in d[:2]:
            kanten.add((min(i, j), max(i, j)))
    rot = {5, 12, 19}
    teile = ['<rect width="%g" height="%g" fill="url(#ngrund)"/>' % (NB, NH)]
    for i, j in sorted(kanten):
        a, b = knoten[i], knoten[j]
        heiss = i in rot or j in rot
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="%.2f" opacity="%.2f"/>'
                     % (a[0], a[1], b[0], b[1], "#DA291C" if heiss else "#8E8577",
                        1.0 if heiss else 0.8, (0.5 if heiss else 0.28) * min(a[3], b[3]) * 1.6))
    for i, (x, y, r, o) in enumerate(knoten):
        teile.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (x, y, r, "#DA291C" if i in rot else "#6E6558", min(1.0, o + 0.25)))
        if i in rot:
            teile.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#DA291C" '
                         'stroke-width="1" opacity=".35"/>' % (x, y, r + 5))
    defs = ('<defs><linearGradient id="ngrund" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#FAF8F4"/><stop offset="1" stop-color="#EDE9E1"/>'
            '</linearGradient></defs>')
    return ('<svg class="svc-pic" viewBox="0 0 %g %g" preserveAspectRatio="xMidYMid slice" '
            'focusable="false" aria-hidden="true">%s%s</svg>' % (NB, NH, defs, "".join(teile)))


def ersetzen(text, muster, neu, was):
    if len(re.findall(muster, text, re.S)) != 1:
        sys.exit("make_grafik.py: %s - nicht genau ein Treffer" % was)
    return re.sub(muster, lambda _: neu, text, count=1, flags=re.S)


def main():
    quelle = ROOT / "index.html"
    if not quelle.exists():
        sys.exit("make_grafik.py: index.html nicht gefunden")
    text = quelle.read_text(encoding="utf-8")
    h, n = hero(), netz()
    text = ersetzen(text, r'<svg class="hero-pic".*?</svg>|<picture class="hero-pic">.*?</picture>',
                    h, "Hero")
    text = ersetzen(text, r'<svg class="svc-pic".*?</svg>|<picture class="svc-pic">.*?</picture>',
                    n, "Systembild")
    quelle.write_text(text, encoding="utf-8")
    print("Hero %d Zeichen, Systembild %d Zeichen" % (len(h), len(n)))
    print("index.html aktualisiert - jetzt build.py laufen lassen")


if __name__ == "__main__":
    main()
