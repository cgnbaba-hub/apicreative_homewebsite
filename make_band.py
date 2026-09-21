#!/usr/bin/env python3
"""Zeichnet das Bildband und schreibt es in index.html.

    python3 make_band.py

Das Band zwischen Referenzen und "Ueber uns" war ein Foto: ein Lichthof mit
einer Person an der Bruestung. Die Vorlage hatte 1376 Pixel Breite und wurde
ueber die volle Fensterbreite gezeigt - auf einem feinen Bildschirm sah man
das.

Hier steht stattdessen eine Zeichnung. Und zwar keine, bei der Flaechen ins
Bild geschoben werden, sondern eine echte Zentralperspektive: Koerper werden
im Raum beschrieben und projiziert. Dadurch fluchten alle Kanten von selbst
auf denselben Punkt, die Fenstersprossen stehen im richtigen Abstand, und die
Flaechen eines Koerpers bekommen ihren Ton aus ihrer Lage - oben hell, zur
Fensterwand heller, unten dunkel.

Die Person steht fuer den Massstab. Ohne sie verliert der Raum seine Groesse.

Nach einer Aenderung erst dieses Skript laufen lassen, dann build.py.
"""
import math
import pathlib
import re
import sys

B, H = 1600.0, 520.0
F = 900.0                      # Brennweite
CX, CY = 800.0, 252.0          # der Fluchtpunkt sitzt rechts der Mitte:
                               # die helle Fensterwand bekommt mehr Bild

# Tonleiter, warmes Grau wie Travertin
T = {
  "himmel": "#F6F3EE", "glanz": "#FFFFFF",
  "oben": "#E9E3D8", "front": "#D4CBBB", "seite": "#EFEAE1", "unten": "#9C9077",
  "tief": "#7C7160", "wand": "#E3DCD0", "wand_fern": "#EDE8DF",
  "glas": "#FAF9F6", "sprosse": "#C6BEB1", "boden": "#E7E1D6", "figur": "#4A443B",
}


def p(x, y, z):
    """3D nach 2D. z ist die Tiefe, y zeigt nach unten."""
    z = max(z, 0.35)
    return (CX + F * x / z, CY + F * y / z)


def flaeche(pkt3, farbe, o=None, teile=None):
    d = " ".join("%.1f,%.1f" % p(*q) for q in pkt3)
    teile.append('<polygon points="%s" fill="%s"%s/>' % (
        d, farbe, ' opacity="%s"' % o if o else ""))


def kante(a, b, farbe, w=1.0, o=None, teile=None):
    x1, y1 = p(*a)
    x2, y2 = p(*b)
    teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                 'stroke-width="%.2f"%s stroke-linecap="round"/>'
                 % (x1, y1, x2, y2, farbe, w, ' opacity="%s"' % o if o else ""))


def quader(x0, x1, y0, y1, z0, z1, teile, ton_oben=None, ton_front=None,
           ton_seite=None, ton_unten=None):
    """Ein Koerper. Gezeichnet werden nur die Flaechen, die man von hier sieht."""
    ton_oben = ton_oben or T["oben"]
    ton_front = ton_front or T["front"]
    ton_seite = ton_seite or T["seite"]
    ton_unten = ton_unten or T["unten"]
    if y0 > 0:                      # ueber Augenhoehe: Unterseite sichtbar
        flaeche([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], ton_unten, teile=teile)
    if y1 < 0:                      # unter Augenhoehe: Oberseite sichtbar
        flaeche([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], ton_oben, teile=teile)
    if x0 > 0:                      # rechts der Achse: linke Seite sichtbar
        flaeche([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], ton_seite, teile=teile)
    if x1 < 0:
        flaeche([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], ton_seite, teile=teile)
    flaeche([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], ton_front, teile=teile)


teile = []
def F_(pkt, farbe, o=None): flaeche(pkt, farbe, o, teile)
def K_(a, b, farbe, w=1.0, o=None): kante(a, b, farbe, w, o, teile)
def Q_(*a, **k): quader(*a, teile=teile, **k)

# Ein Lichthof: hoch, schmal, Licht von links.
DECKE, BODEN = -6.4, 2.3
LINKS, RECHTS = -4.2, 4.6
FERN = 26.0

teile.append('<rect x="0" y="0" width="%g" height="%g" fill="%s"/>' % (B, H, T["wand"]))

# --- Rueckwand, heller als die Seiten: dorthin faellt das Licht -------------
F_([(LINKS,DECKE,FERN),(RECHTS,DECKE,FERN),(RECHTS,BODEN,FERN),(LINKS,BODEN,FERN)], T["wand_fern"])
for x, w, o in ((-3.4, 1.5, "0.80"), (-1.2, 0.9, "0.55"), (0.5, 0.5, "0.34")):
    F_([(x,DECKE,FERN-0.01),(x+w,DECKE,FERN-0.01),(x+w+2.2,BODEN,FERN-0.01),(x+2.2,BODEN,FERN-0.01)],
       T["glanz"], o)

# --- Decke, weit oben: sie schliesst das Bild nach hinten -------------------
F_([(LINKS,DECKE,4.0),(RECHTS,DECKE,4.0),(RECHTS,DECKE,FERN),(LINKS,DECKE,FERN)], T["tief"], "0.55")

# --- Boden ------------------------------------------------------------------
F_([(LINKS,BODEN,4.0),(RECHTS,BODEN,4.0),(RECHTS,BODEN,FERN),(LINKS,BODEN,FERN)], T["boden"])
# Lichtfelder in der Rhythmik der Fensterachsen
for z0, br in ((5.4, 2.6), (9.2, 2.2), (14.0, 1.8), (20.0, 1.4)):
    F_([(LINKS,BODEN,z0),(LINKS+2.9,BODEN,z0+1.1),
        (LINKS+3.3,BODEN,z0+br+1.1),(LINKS,BODEN,z0+br)], T["glanz"], "0.62")

# --- Fensterwand links ------------------------------------------------------
F_([(LINKS,DECKE,4.0),(LINKS,DECKE,FERN),(LINKS,BODEN,FERN),(LINKS,BODEN,4.0)], T["glas"])
z = 4.6
while z < FERN:
    K_((LINKS,DECKE,z),(LINKS,BODEN,z), T["sprosse"], max(0.55, 14.0/z), "0.75")
    z *= 1.175
for y in (-4.3, -2.1, 0.1):
    K_((LINKS,y,4.0),(LINKS,y,FERN), T["sprosse"], 1.1, "0.42")

# --- Rechte Wand mit tiefen Einschnitten (Galerien) -------------------------
F_([(RECHTS,DECKE,4.0),(RECHTS,DECKE,FERN),(RECHTS,BODEN,FERN),(RECHTS,BODEN,4.0)], T["front"])
for yo, yu in ((-5.30,-4.86), (-3.85,-3.41), (-2.40,-1.96), (-0.95,-0.51), (0.50,0.94)):
    Q_(3.70, RECHTS, yo, yu, 4.4, FERN-0.4)
    K_((3.70,yo-0.80,4.4),(3.70,yo-0.80,FERN-0.4), T["sprosse"], 1.1, "0.4")
    K_((3.70,yo-0.03,4.4),(3.70,yo-0.03,FERN-0.4), T["glanz"], 1.4, "0.85")

# --- Auskragende Platten ----------------------------------------------------
Q_(LINKS, 1.5, -3.15, -2.78, 6.2, 7.9)         # nah, oben
Q_(-0.6, RECHTS, -1.28, -0.94, 10.4, 11.9)     # mitte
Q_(LINKS, 0.9, 0.55, 0.88, 15.6, 17.1)         # hinten, unten
Q_(-2.4, 2.6, -4.55, -4.28, 19.5, 20.7)        # ganz hinten, duenn

# --- Ein schlanker Pfeiler, der die Tiefe misst -----------------------------
Q_(-2.35, -2.05, DECKE, BODEN, 12.4, 12.7, ton_front=T["seite"], ton_seite=T["oben"])

# --- Die Person, auf der mittleren Platte -----------------------------------
fx, fz, FUSS = 4.15, 16.5, -0.95
kopf = p(fx, FUSS - 1.60, fz); r = F * 0.072 / fz
teile.append('<g fill="%s">' % T["figur"])
teile.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (kopf[0], kopf[1], r))
F_([(fx-0.15,FUSS-1.50,fz),(fx+0.15,FUSS-1.50,fz),(fx+0.17,FUSS-0.82,fz),(fx-0.17,FUSS-0.82,fz)], T["figur"])
F_([(fx-0.16,FUSS-0.84,fz),(fx-0.02,FUSS-0.84,fz),(fx-0.03,FUSS,fz),(fx-0.14,FUSS,fz)], T["figur"])
F_([(fx+0.03,FUSS-0.84,fz),(fx+0.16,FUSS-0.84,fz),(fx+0.14,FUSS,fz),(fx+0.04,FUSS,fz)], T["figur"])
teile.append('</g>')
# Handlauf vor ihr
K_((3.70,FUSS-0.92,16.5),(RECHTS,FUSS-0.92,16.5), T["sprosse"], 1.3, "0.55")

MARKUP = ('<svg class="band-pic" viewBox="0 0 %g %g" '
          'preserveAspectRatio="xMidYMid slice" focusable="false">%s</svg>'
          % (B, H, "".join(teile)))


def main():
    quelle = pathlib.Path(__file__).parent / "index.html"
    if not quelle.exists():
        sys.exit("make_band.py: index.html nicht gefunden")
    text = quelle.read_text(encoding="utf-8")
    muster = r'<svg class="band-pic".*?</svg>|<picture class="band-pic">.*?</picture>'
    if len(re.findall(muster, text, re.S)) != 1:
        sys.exit("make_band.py: das Bildband ist im Markup nicht eindeutig zu finden")
    text = re.sub(muster, lambda _: MARKUP, text, count=1, flags=re.S)
    quelle.write_text(text, encoding="utf-8")
    print("Bildband gezeichnet: %d Flächen, %d Zeichen" % (len(teile), len(MARKUP)))
    print("index.html aktualisiert - jetzt build.py laufen lassen")


if __name__ == "__main__":
    main()
