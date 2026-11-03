"""Gemeinsame Bausteine zum Erzeugen der statischen HTML-Seiten."""
import json, os, html
from zeichnungen import LOGO

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "Musik Klasse 7"

# Lernstufen: Farbe (CSS-Klasse reihe-N) und Name
STUFEN = {
    1: ("Rhythmus", "Notenwerte, Pausen, Punkte und Triolen"),
    2: ("Tonhöhe und Lautstärke", "Violin- und Bassschlüssel, Vorzeichen, Dynamik"),
}

# Kapitel in der Reihenfolge der Reihe: (Nummer, Slug, Titel, Stufe)
KAPITEL = [
    (1, "01-notenwerte", "Notenwerte und Takt", 1),
    (2, "02-pausen", "Pausen", 1),
    (3, "03-punktierung-triolen", "Punktierte Noten, Haltebögen und Triolen", 1),
    (4, "04-violinschluessel", "Noten im Violinschlüssel", 2),
    (5, "05-bassschluessel", "Noten im Bassschlüssel", 2),
    (6, "06-vorzeichen", "Vorzeichen", 2),
    (7, "07-dynamik", "Dynamik", 2),
]


def seite(pfad, titel, inhalt, stufe=None, krumen=None, beschreibung="", skripte=(), hauptklasse="", sperre=False):
    """pfad: relativ zum Repo, z. B. 'kapitel/01-notenwerte.html'"""
    tiefe = pfad.count("/")
    wurzel = "../" * tiefe if tiefe else "./"
    krumen = krumen or []
    pfad_html = ""
    if krumen:
        teile = []
        for text, link in krumen:
            if link:
                teile.append(f'<li><a href="{link}">{html.escape(text)}</a></li>')
            else:
                teile.append(f'<li aria-current="page">{html.escape(text)}</li>')
        pfad_html = f'<nav aria-label="Brotkrümel"><ol class="pfad">{"".join(teile)}</ol></nav>'
    body_klasse = f' class="reihe-{stufe}"' if stufe else ""
    if sperre and stufe:
        body_klasse += f' data-stufe="{stufe}"'
    body_klasse += f' data-wurzel="{wurzel}"'
    skripte = list(skripte) + ["assets/lernpfad.js", "assets/fortschritt.js"]
    skript_html = "".join(f'\n  <script src="{wurzel}{s}" defer></script>' for s in skripte)
    seite_html = f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titel)} – {SITE}</title>
  <meta name="description" content="{html.escape(beschreibung)}">
  <link rel="stylesheet" href="{wurzel}assets/style.css">{skript_html}
</head>
<body{body_klasse}>
  <header class="kopf">
    <div class="huelle">
      <a class="marke" href="{wurzel}index.html">{LOGO}{SITE}</a>
      {pfad_html}
    </div>
  </header>
  <main id="inhalt"{(' class="' + hauptklasse + '"') if hauptklasse else ''}>
{inhalt}
  </main>
  <footer class="fuss">
    <div class="huelle">
      <p>Musik Klasse 7: Notenlehre. Keine Anmeldung, keine Datenübertragung. Welche Übungen du gelöst hast, merkt sich nur dein Browser auf diesem Gerät.</p>
    </div>
  </footer>
</body>
</html>
"""
    ziel = os.path.join(REPO, pfad)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(seite_html)
    return ziel


def uebung(typ, daten, slug=""):
    js = json.dumps(daten, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<div class="uebung" data-typ="{typ}" data-id="{slug}">\n<script type="application/json">\n{js}\n</script>\n</div>'
