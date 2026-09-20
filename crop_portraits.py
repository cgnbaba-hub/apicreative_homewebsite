#!/usr/bin/env python3
"""Schneidet die Teamfotos auf einen einheitlichen Ausschnitt zu.

    python3 crop_portraits.py

Beide Bilder bekommen dasselbe Hochformat 4:5, dieselbe relative Kopfgrösse
und dieselbe Kinnhöhe, damit die Karten nebeneinander ruhig wirken. Die
Schnittkante liegt deutlich unterhalb der Schultern.

Als Maß dient die Gesichtshöhe (Haaransatz bis Kinn). Sie wird aus dem Bild
bestimmt: der Anzug über eine Blaumaske, das Gesicht über eine Hautmaske
oberhalb der Schulterlinie. Die Messwerte werden beim Lauf ausgegeben, damit
sich das Ergebnis nachvollziehen lässt.
"""

import pathlib
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("crop_portraits.py: benötigt Pillow und numpy (pip install Pillow numpy)")

ASSETS = pathlib.Path(__file__).parent / "assets"

# Quelle, oberer und unterer Rand des Inhalts (IMG_9080 hat schwarze Balken), Ziel
SOURCES = [
    ("IMG_9080.JPG", 51, 1494, "team-1.jpg"),
    ("IMG_9081.JPG", 0, 1195, "team-2.jpg"),
]

RATIO = 4 / 5        # Breite zu Höhe
ABOVE = 0.55         # Luft über dem Haaransatz, in Gesichtshöhen
TOTAL = 2.45         # Gesamthöhe des Ausschnitts, in Gesichtshöhen
OUT_SIZE = (600, 750)   # so gross, wie die Originale es hergeben - mehr steckt nicht drin


def measure(arr):
    """Liefert Haaransatz, Kinn, Schulterlinie und Gesichtsmitte in Pixeln."""
    height, width, _ = arr.shape
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    bright = arr.mean(axis=2)

    # Der Anzug ist dunkel und blaustichig. Graue Fensterrahmen im Hintergrund
    # sind neutral und fallen dadurch heraus.
    navy = (bright < 125) & (b > r + 10)
    navy_width = navy.sum(axis=1) / width
    shoulder = next((y for y in range(height) if navy_width[y] > 0.30), height // 2)

    band = navy[shoulder:shoulder + 150].sum(axis=0)
    hit = np.nonzero(band > band.max() * 0.35)[0]
    body_cx = int((hit[0] + hit[-1]) / 2) if len(hit) else width // 2

    # Haut nur oberhalb der Schulter und in der Nähe der Körpermitte suchen,
    # damit Pflanzen und Holz im Hintergrund nicht stören.
    skin = (r > 95) & (r > g + 12) & (g > b + 4) & (bright > 70)
    lo, hi = max(0, body_cx - 230), min(width, body_cx + 230)
    mask = np.zeros_like(skin)
    mask[:shoulder, lo:hi] = skin[:shoulder, lo:hi]

    rows = np.nonzero(mask.sum(axis=1) > 0.035 * (hi - lo))[0]
    if not len(rows):
        sys.exit("crop_portraits.py: kein Gesicht gefunden")
    face_top, chin = int(rows[0]), int(rows[-1])

    cols = mask[face_top:chin].sum(axis=0)
    hit = np.nonzero(cols > cols.max() * 0.30)[0]
    face_cx = int((hit[0] + hit[-1]) / 2)
    return face_top, chin, shoulder, face_cx


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, y0, y1, target in SOURCES:
        path = ASSETS / name
        if not path.exists():
            sys.exit("crop_portraits.py: fehlt: " + str(path))
        im = Image.open(path).convert("RGB")
        arr = np.asarray(im)[y0:y1].astype(int)
        face_top, chin, shoulder, face_cx = measure(arr)
        face_h = chin - face_top

        height = TOTAL * face_h
        width = height * RATIO
        top = face_top - ABOVE * face_h
        left = face_cx - width / 2

        # in das Bild hineinschieben, falls eine Kante überläuft
        content_h, content_w = arr.shape[0], arr.shape[1]
        width, height = min(width, content_w), min(height, content_h)
        left = max(0, min(left, content_w - width))
        top = max(0, min(top, content_h - height))

        box = (round(left), round(top + y0), round(left + width), round(top + y0 + height))
        im.crop(box).resize(OUT_SIZE, Image.LANCZOS).save(
            ASSETS / target, quality=88, optimize=True, progressive=True)

        rel_chin = (chin - top) / height
        print(f"{name}: Gesichtshöhe {face_h}px, Schulter y={shoulder}, "
              f"Ausschnitt {box} -> assets/{target} (Kinn bei {rel_chin:.1%} der Höhe)")


if __name__ == "__main__":
    main()
