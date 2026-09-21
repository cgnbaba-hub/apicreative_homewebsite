#!/usr/bin/env python3
"""Erzeugt den Veroeffentlichungsordner public/.

    python3 make_public.py

Hinein kommt nur, was die Website im Browser braucht:

    index.html          die Seite, mit oertlichen statt fremden Adressen
    vendor/*.js         GSAP, ScrollTrigger, Lenis
    vendor/*.woff2      die Schrift Inter, vier Schnitte
    _headers            Vorschau-Schutz fuer Cloudflare Pages

Der Unterschied zur Quelle: index.html laedt Schrift und Bibliotheken von
einem CDN. Auf der eigenen Adresse soll nichts von fremden Servern kommen -
also werden die Links auf die Dateien in vendor/ umgebogen, mit relativen
Pfaden. Bilder gibt es keine mehr als eigene Dateien; alles ist gezeichnet
oder liegt als Data-URI im Dokument.

Zum Schluss prueft das Skript, dass wirklich nichts Fremdes mehr geladen
wird und dass jeder oertliche Pfad auch existiert.
"""

import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).parent
ZIEL = ROOT / "public"
VENDOR = ROOT / "vendor"

SCHRIFTEN = [400, 500, 600, 700]
SKRIPTE = ["gsap.min.js", "ScrollTrigger.min.js", "lenis.min.js"]

FONT_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""

CDN_SCRIPTS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" onerror="window.__gsapFailed=true"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" onerror="window.__gsapFailed=true"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js" onerror="window.__lenisFailed=true"></script>"""

HEADERS = """# ===== VORSCHAU-SCHUTZ - BEIM ECHTEN LIVEGANG ENTFERNEN =====
# Diese Datei haelt die Vorschau aus den Suchmaschinen. Beim Livegang
# loeschen - und die Zeile <meta name="robots"> in index.html gleich mit.
/*
  X-Robots-Tag: noindex
"""


def fail(msg):
    sys.exit("make_public.py: " + msg)


def ersetzen(text, alt, neu, was):
    if text.count(alt) != 1:
        fail("%s: %d Treffer statt einem" % (was, text.count(alt)))
    return text.replace(alt, neu, 1)


def schrift_block():
    zeilen = []
    for gewicht in SCHRIFTEN:
        zeilen.append(
            "@font-face{font-family:'Inter';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url(vendor/inter-latin-%d-normal.woff2) format('woff2')}"
            % (gewicht, gewicht))
    return ("<!-- Die Schrift kommt vom eigenen Server, nicht von einem fremden. -->\n"
            "<style>\n" + "\n".join(zeilen) + "\n</style>")


def skript_block():
    return "\n".join(
        '<script src="vendor/%s" onerror="window.__%sFailed=true"></script>'
        % (name, "lenis" if "lenis" in name else "gsap")
        for name in SKRIPTE)


def pruefen(text):
    """Nichts Fremdes mehr, und jeder oertliche Pfad existiert."""
    fremd = (re.findall(r'\bsrc\s*=\s*"(https?://[^"]+)"', text)
             + re.findall(r'<link[^>]*\bhref\s*=\s*"(https?://[^"]+)"', text)
             + re.findall(r'url\(\s*["\']?(https?://[^"\')]+)', text))
    if fremd:
        fail("laedt noch von fremden Servern: " + ", ".join(sorted(set(fremd))))

    pfade = set(re.findall(r'\bsrc\s*=\s*"(?!data:|https?:)([^"#]+)"', text))
    pfade |= set(re.findall(r'<link[^>]*\bhref\s*=\s*"(?!data:|https?:)([^"#]+)"', text))
    pfade |= set(re.findall(r'url\(\s*["\']?(?!data:|https?:|#)([^"\')]+)', text))
    # %23 ist ein verschluesseltes #: ein Verweis innerhalb einer SVG-Datei,
    # keine Datei auf der Platte.
    pfade = {p for p in pfade if not p.startswith("%23")}
    for pfad in sorted(pfade):
        if pfad.startswith("/"):
            fail("absoluter Pfad, sollte relativ sein: " + pfad)
        if not (ZIEL / pfad).exists():
            fail("verweist auf eine Datei, die es nicht gibt: " + pfad)
    return sorted(pfade)


def main():
    quelle = ROOT / "index.html"
    if not quelle.exists():
        fail("index.html nicht gefunden")
    if '<meta name="robots" content="noindex, nofollow">' not in quelle.read_text(encoding="utf-8"):
        fail("der Vorschau-Schutz fehlt in index.html")

    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    (ZIEL / "vendor").mkdir(parents=True)

    for name in SKRIPTE + ["inter-latin-%d-normal.woff2" % g for g in SCHRIFTEN]:
        pfad = VENDOR / name
        if not pfad.exists():
            fail("fehlt: " + str(pfad))
        shutil.copy2(pfad, ZIEL / "vendor" / name)

    text = quelle.read_text(encoding="utf-8")
    text = ersetzen(text, FONT_LINKS, schrift_block(), "Schrift-Links")
    text = ersetzen(text, CDN_SCRIPTS, skript_block(), "CDN-Skripte")
    (ZIEL / "index.html").write_text(text, encoding="utf-8")
    (ZIEL / "_headers").write_text(HEADERS, encoding="utf-8")

    pfade = pruefen(text)
    print("public/ erzeugt - keine fremden Server, alle Pfade relativ und vorhanden")
    print()
    gesamt = 0
    for datei in sorted(ZIEL.rglob("*")):
        if datei.is_file():
            groesse = datei.stat().st_size
            gesamt += groesse
            print("  %8.1f KB  %s" % (groesse / 1024, datei.relative_to(ZIEL)))
    print("  %8.1f KB  gesamt, %d Dateien" % (gesamt / 1024, sum(1 for d in ZIEL.rglob('*') if d.is_file())))
    print()
    print("  oertliche Verweise im Dokument: " + ", ".join(pfade))


if __name__ == "__main__":
    main()
