#!/usr/bin/env python3
"""Erzeugt einen Veroeffentlichungsordner.

    python3 make_public.py                -> public/            (mit Intro)
    python3 make_public.py --ohne-intro   -> public-ohne-intro/ (ohne Intro)

Hinein kommt nur, was die Website im Browser braucht:

    index.html          die Seite, mit oertlichen statt fremden Adressen
    vendor/*.woff2      die Schrift Inter, vier Schnitte
    vendor/*.js         GSAP, ScrollTrigger, Lenis - nur in der Fassung
                        mit Intro; ohne Intro werden sie nicht gebraucht
    _headers            Vorschau-Schutz

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

import build

ROOT = pathlib.Path(__file__).parent
VENDOR = ROOT / "vendor"

SCHRIFTEN = [400, 500, 600, 700]
SKRIPTE = ["gsap.min.js", "ScrollTrigger.min.js", "lenis.min.js"]

FONT_LINKS = build.FONT_LINKS
CDN_SCRIPTS = build.CDN_SCRIPTS

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


def pruefen(text, ziel):
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
        if not (ziel / pfad).exists():
            fail("verweist auf eine Datei, die es nicht gibt: " + pfad)
    return sorted(pfade)


def main():
    ohne_intro = "--ohne-intro" in sys.argv[1:]
    for arg in sys.argv[1:]:
        if arg != "--ohne-intro":
            fail("unbekannte Option: " + arg)

    ziel = ROOT / ("public-ohne-intro" if ohne_intro else "public")

    quelle = ROOT / "index.html"
    if not quelle.exists():
        fail("index.html nicht gefunden")
    text = quelle.read_text(encoding="utf-8")
    if '<meta name="robots" content="noindex, nofollow">' not in text:
        fail("der Vorschau-Schutz fehlt in index.html")

    if ziel.exists():
        shutil.rmtree(ziel)
    (ziel / "vendor").mkdir(parents=True)

    dateien = ["inter-latin-%d-normal.woff2" % g for g in SCHRIFTEN]
    if not ohne_intro:
        dateien += SKRIPTE
    for name in dateien:
        pfad = VENDOR / name
        if not pfad.exists():
            fail("fehlt: " + str(pfad))
        shutil.copy2(pfad, ziel / "vendor" / name)

    if ohne_intro:
        # Genau dieselbe Fassung wie apicreative-ohne-intro.html, nur mit
        # der Schrift als eigene Datei statt als Data-URI.
        text = build.build_without_intro(text, schrift_block())
    else:
        text = ersetzen(text, FONT_LINKS, schrift_block(), "Schrift-Links")
        text = ersetzen(text, CDN_SCRIPTS, skript_block(), "CDN-Skripte")

    (ziel / "index.html").write_text(text, encoding="utf-8")
    (ziel / "_headers").write_text(HEADERS, encoding="utf-8")

    pfade = pruefen(text, ziel)
    for nr, block in enumerate(re.findall(r"<style>(.*?)</style>", text, re.S), 1):
        if block.count("/*") != block.count("*/"):
            fail("Style-Block %d hat einen offenen Kommentar" % nr)

    print("%s/ erzeugt - keine fremden Server, alle Pfade relativ und vorhanden"
          % ziel.name)
    print()
    gesamt = 0
    anzahl = 0
    for datei in sorted(ziel.rglob("*")):
        if datei.is_file():
            groesse = datei.stat().st_size
            gesamt += groesse
            anzahl += 1
            print("  %8.1f KB  %s" % (groesse / 1024, datei.relative_to(ziel)))
    print("  %8.1f KB  gesamt, %d Dateien" % (gesamt / 1024, anzahl))
    print()
    print("  oertliche Verweise im Dokument: " + ", ".join(pfade))


if __name__ == "__main__":
    main()
