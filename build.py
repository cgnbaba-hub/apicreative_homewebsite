#!/usr/bin/env python3
"""Erzeugt die beiden abgeleiteten Fassungen aus index.html.

    python3 build.py

index.html ist die einzige Quelle. Nach jeder Änderung daran dieses Skript
erneut ausführen, sonst laufen die Dateien auseinander.

    index.html                      Quelle. Mit Intro, Bibliotheken per CDN.
    apicreative-praesentation.html  Mit Intro. Alles eingebettet, läuft offline.
    apicreative-ohne-intro.html     Ohne Intro. Nur die moderne Seite, ohne
                                    Animationsbibliotheken.

Die Dateien in vendor/ stammen aus den npm-Paketen gsap@3.12.5,
lenis@1.1.20 und @fontsource/inter@5.3.0.
"""

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
VENDOR = ROOT / "vendor"

# Blöcke in index.html, die hier ersetzt oder entfernt werden.
FONT_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""

CDN_SCRIPTS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" onerror="window.__gsapFailed=true"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" onerror="window.__gsapFailed=true"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js" onerror="window.__lenisFailed=true"></script>"""

LIBS = [
    ("gsap.min.js", "GSAP 3.12.5"),
    ("ScrollTrigger.min.js", "GSAP ScrollTrigger 3.12.5"),
    ("lenis.min.js", "Lenis 1.1.20"),
]


def fail(msg):
    sys.exit("build.py: " + msg)


def cut(text, start, end, what):
    """Schneidet alles von start bis vor end heraus."""
    a = text.find(start)
    b = text.find(end)
    if a == -1 or b == -1 or b < a:
        fail("Abschnitt nicht gefunden: " + what)
    return text[:a] + text[b:]


def replace_once(text, old, new, what):
    if old not in text:
        fail("Block nicht gefunden: " + what)
    return text.replace(old, new, 1)


def embedded_fonts():
    faces = []
    for weight in (400, 500, 600, 700):
        path = VENDOR / f"inter-latin-{weight}-normal.woff2"
        if not path.exists():
            fail("fehlt: " + str(path))
        data = base64.b64encode(path.read_bytes()).decode()
        faces.append(
            "@font-face{font-family:'Inter';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (weight, data)
        )
    return "<style>\n" + "\n".join(faces) + "\n</style>"


def embedded_libs():
    blocks = []
    for name, label in LIBS:
        path = VENDOR / name
        if not path.exists():
            fail("fehlt: " + str(path))
        code = path.read_text(encoding="utf-8")
        if "</script" in code:
            fail(name + " enthält </script und kann nicht eingebettet werden")
        blocks.append(f"<!-- {label} (lokal eingebettet) -->\n<script>{code}</script>")
    return "\n".join(blocks)


def build_presentation(src):
    """Mit Intro, ohne Netzwerkzugriff."""
    out = replace_once(src, FONT_LINKS, embedded_fonts(), "Schrift-Links")
    out = replace_once(out, CDN_SCRIPTS, embedded_libs(), "CDN-Skripte")
    return out


def build_without_intro(src):
    """Nur die moderne Seite: kein Intro, keine Animationsbibliotheken."""
    out = replace_once(src, FONT_LINKS, embedded_fonts(), "Schrift-Links")

    # Die Kopfzeilen-Weiche, die das Intro überhaupt erst aktiviert.
    out = cut(out, "<script>\n  /* Vor dem ersten Paint", "<style>\n/* ===", "Intro-Weiche")

    # CSS-Abschnitt 4 (Intro-Bühne) und die Zusatzregeln dazu.
    out = cut(out, "/* ============================================================\n   4. Intro-Bühne",
              "/* ============================================================\n   5. Moderne Seite",
              "CSS der Intro-Bühne")
    out = cut(out, "<style>\n/* Zustandsabhängige Regeln der Intro-Bühne */",
              '<script src="https://cdnjs', "Zusatzregeln der Intro-Bühne")

    # Das Intro-Markup.
    out = cut(out, "<!-- ============================================================\n     Intro: Scroll-Story",
              "<!-- ============================================================\n     1. Sticky-Header",
              "Intro-Markup")

    # Die Bibliotheken werden ohne Intro nicht gebraucht.
    out = replace_once(out, CDN_SCRIPTS, "", "CDN-Skripte")

    # Das Intro-Skript bleibt stehen, läuft aber nie an: ohne GSAP nimmt der
    # Code von sich aus den Weg über finishIntro(). Bewusst so gelassen,
    # damit hier nicht in getesteten Kontrollfluss geschnitten wird.
    return out


def check(name, text):
    urls = set(re.findall(r'https?://[^\s"\'<>)]+', text))
    external = [u for u in urls
                if not u.startswith(("http://www.w3.org", "https://gsap.com",
                                     "http://www.apicreative.ch", "https://[Platzhalter]"))]
    if external:
        fail(name + " lädt noch extern: " + ", ".join(sorted(external)))
    print(f"  {name}: {len(text.encode()) // 1024} KB, keine externen Abrufe")


def main():
    src_path = ROOT / "index.html"
    if not src_path.exists():
        fail("index.html nicht gefunden")
    src = src_path.read_text(encoding="utf-8")
    print(f"Quelle index.html: {len(src.encode()) // 1024} KB")

    for name, builder in (("apicreative-praesentation.html", build_presentation),
                          ("apicreative-ohne-intro.html", build_without_intro)):
        out = builder(src)
        check(name, out)
        (ROOT / name).write_text(out, encoding="utf-8")
    print("fertig")


if __name__ == "__main__":
    main()
