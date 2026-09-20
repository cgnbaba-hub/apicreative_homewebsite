#!/usr/bin/env python3
"""Zeichnet das Bildband und schreibt es in index.html.

    python3 make_band.py

Das Band zwischen Referenzen und "Ueber uns" war ein Foto: ein Lichthof mit
einer Person an der Bruestung. Die Vorlage hatte 1376 Pixel Breite und wurde
ueber die volle Fensterbreite gezeigt - auf einem feinen Bildschirm sah man
das. Hier steht stattdessen eine Zeichnung: dieselbe Szene, aber als Vektor,
und damit in jeder Groesse scharf und ein paar Kilobyte gross.

Aufbau in Ebenen, von hinten nach vorn. Ein Fluchtpunkt, zwei Kantenwinkel
und eine Tonleiter aus sieben Werten - damit das Bild Tiefe bekommt und nicht
als heller Brei zerfaellt. Die Person steht fuer den Massstab; ohne sie
verliert der Raum seine Groesse.

Nach einer Aenderung erst dieses Skript laufen lassen, dann build.py.
"""
import pathlib
import re
import sys

B, H = 1600.0, 500.0
VX, VY = 1010.0, 238.0

# Warme Grautoene wie Travertin, von tief nach hell
TON = ["#6E6558", "#8A8071", "#A2988A", "#BCB2A3", "#D3CABC", "#E7E1D6", "#F7F4EE"]
TIEF, DUNKEL, MITTELD, MITTEL, HELL, HELLER, LICHT = TON
FIGUR = "#4A443B"

teile = []
add = teile.append

def poly(pkt, farbe, o=None):
    add('<polygon points="%s" fill="%s"%s/>' % (
        " ".join("%.1f,%.1f" % p for p in pkt), farbe,
        ' opacity="%s"' % o if o else ""))

def linie(a, b, farbe, w=1.0, o=None):
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f"%s/>'
        % (a[0], a[1], b[0], b[1], farbe, w, ' opacity="%s"' % o if o else ""))

def vp(p, t):
    return (p[0] + (VX - p[0]) * t, p[1] + (VY - p[1]) * t)

# ---------------------------------------------------------------- Grund
add('<rect width="%g" height="%g" fill="%s"/>' % (B, H, HELL))

# --------------------------------------------- Rueckwand aus Stein, hell
poly([(300, 0), (1210, 0), (1210, H), (300, H)], HELLER)

# ---------------------------------------- Lichtbahnen ueber der Steinwand
# Erst das Licht, dann der Schatten daneben: so bekommt die Wand Richtung.
for x, w, o in ((330, 185, "0.85"), (610, 120, "0.62"), (790, 70, "0.42")):
    poly([(x, 0), (x + w, 0), (x + w + 300, H), (x + 300, H)], LICHT, o)
for x, w, o in ((515, 70, "0.30"), (730, 46, "0.22")):
    poly([(x, 0), (x + w, 0), (x + w + 300, H), (x + 300, H)], MITTELD, o)

# ------------------------------------------------ Verglaste Wand links
o_v, u_v = (-10.0, -10.0), (-10.0, H + 10)
o_h, u_h = vp(o_v, 0.74), vp(u_v, 0.74)
poly([o_v, o_h, u_h, u_v], LICHT)
poly([o_v, o_h, u_h, u_v], HELLER, "0.35")
for i in range(1, 13):
    t = (1 - (1 - i / 13) ** 2.0) * 0.74
    linie(vp(o_v, t), vp(u_v, t), MITTEL, 3.0 * (1 - t) + 0.6, "0.75")
# angedeutete Nachbarhaeuser, sehr blass
poly([(18, 232), (104, 232), (104, H), (18, H)], MITTEL, "0.16")
poly([(126, 286), (196, 286), (196, H), (126, H)], MITTEL, "0.11")
# Der Pfeiler, der die Verglasung begrenzt
poly([(286, -10), (330, -10), (330, H + 10), (286, H + 10)], HELLER)
poly([(322, -10), (330, -10), (330, H + 10), (322, H + 10)], MITTEL, "0.5")

# ----------------------------------------------- Galerien rechts, gestaffelt
def galerie(y, hoehe, tiefe_schatten, ton):
    a = (1210.0, y)
    b = (B + 10, y - (y - VY) * 0.30)
    c = (B + 10, b[1] + hoehe * 0.72)
    d = (1210.0, y + hoehe)
    poly([a, b, c, d], ton)                                    # Stirnseite
    poly([d, c, (c[0], c[1] + tiefe_schatten * 0.72), (d[0], d[1] + tiefe_schatten)], DUNKEL, "0.55")
    linie((a[0], a[1] - 34), (b[0], b[1] - 26), MITTEL, 1.8, "0.55")   # Glasbruestung
    linie((a[0], a[1] - 2), (b[0], b[1] - 2), HELL, 2.2, "0.9")

poly([(1210, -10), (B + 10, -10), (B + 10, H + 10), (1210, H + 10)], HELL)
galerie(90, 74, 30, MITTEL)
galerie(262, 50, 26, HELLER)
galerie(418, 84, 36, MITTEL)
# Die Kante, an der die Steinwand in die Galerien umbricht. Ohne sie stossen
# zwei Flaechen ohne Koerper aneinander.
poly([(1186, -10), (1214, -10), (1214, H + 10), (1186, H + 10)], MITTELD)
poly([(1206, -10), (1214, -10), (1214, H + 10), (1206, H + 10)], DUNKEL, "0.4")

# ------------------------------------ Auskragende Platten, die den Raum queren
def platte(x0, y0, x1, y1, dicke, unterseite, ton=HELLER):
    poly([(x0, y0), (x1, y1), (x1, y1 + dicke), (x0, y0 + dicke)], ton)
    poly([(x0, y0 + dicke), (x1, y1 + dicke),
          (x1, y1 + dicke + unterseite * 0.8), (x0, y0 + dicke + unterseite)], MITTELD)
    linie((x0, y0), (x1, y1), LICHT, 2.0, "0.8")               # Lichtkante oben

# oben: eine schwere Decke, die das Bild oben schliesst
poly([(300, -10), (1210, -10), (1210, 44), (300, 58)], MITTEL)
poly([(300, 44), (1210, 44), (1210, 62), (300, 82)], DUNKEL, "0.45")

platte(250, 120, 1010, 186, 34, 22, HELL)
platte(180, 296, 960, 320, 30, 26, HELLER)
platte(120, 430, 900, 408, 44, 30, HELL)

# ------------------------------------------------------ Bruestung und Figur
kante = 296.0
linie((640, kante - 2), (930, kante + 8), MITTELD, 2.2, "0.85")
linie((640, kante - 52), (930, kante - 42), MITTEL, 1.6, "0.55")
for x in (640, 785, 930):
    t = (x - 640) / 290
    linie((x, kante - 52 + 10 * t), (x, kante - 2 + 10 * t), MITTEL, 1.2, "0.45")

# Die Figur steht fuer den Massstab. Schlank, ohne Gesicht, ohne Geste.
fx, fy = 700.0, kante - 1
add('<g fill="%s">' % FIGUR)
add('<circle cx="%.1f" cy="%.1f" r="4.6"/>' % (fx, fy - 58))
poly([(fx - 4.8, fy - 52), (fx + 4.8, fy - 52), (fx + 6.2, fy - 22), (fx - 5.8, fy - 22)], FIGUR)
poly([(fx - 5.4, fy - 23), (fx - 1.0, fy - 23), (fx - 1.2, fy), (fx - 4.6, fy)], FIGUR)
poly([(fx + 1.2, fy - 23), (fx + 5.8, fy - 23), (fx + 5.2, fy), (fx + 1.6, fy)], FIGUR)
add('</g>')
poly([(fx - 7, fy), (fx + 7, fy), (fx + 14, fy + 6), (fx - 14, fy + 6)], DUNKEL, "0.22")

# ------------------------------------------------------------------ Boden
poly([(-10, 452), (1186, 452), (1186, H + 10), (-10, H + 10)], HELL)
poly([(-10, 452), (1186, 452), (1186, 470), (-10, 462)], MITTEL, "0.45")
poly([(60, H + 10), (330, 466), (620, 466), (520, H + 10)], LICHT, "0.7")
poly([(560, H + 10), (640, 466), (740, 466), (700, H + 10)], LICHT, "0.45")

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" '
       'preserveAspectRatio="xMidYMid slice">%s</svg>' % (B, H, "".join(teile)))

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
