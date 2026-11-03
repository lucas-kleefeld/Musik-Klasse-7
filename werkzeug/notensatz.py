"""Brücke zum Notensatz in assets/noten.js (läuft über Node)."""
import json, os, subprocess, html

_HIER = os.path.dirname(os.path.abspath(__file__))
_proc = None


def _server():
    global _proc
    if _proc is None:
        _proc = subprocess.Popen(["node", os.path.join(_HIER, "render_server.js")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    return _proc


def svg(noten, **spec):
    """Gibt das SVG für eine Notenzeile zurück."""
    spec["noten"] = noten
    p = _server()
    p.stdin.write(json.dumps(spec, ensure_ascii=False) + "\n")
    p.stdin.flush()
    ergebnis = json.loads(p.stdout.readline())
    if ergebnis.startswith("FEHLER"):
        raise ValueError(ergebnis + " in " + noten)
    return ergebnis


def N(noten, unterschrift="", titel="", klasse="", spiel=True, **spec):
    """Notenbeispiel als <figure>."""
    spec["titel"] = titel or unterschrift or "Notenbeispiel"
    cap = f"<figcaption>{unterschrift}</figcaption>" if unterschrift else ""
    daten_spiel = spiel
    spiel = ""
    import re as _re
    hat_toene = bool(_re.search(r"(^|\s|\(|\[|\*)\[?[A-G]", noten))   # nur Pausen: nichts zum Anhören
    if daten_spiel and hat_toene and "?" not in noten:
        daten = {"noten": noten, "tonart": spec.get("tonart", 0), "rhythmus": bool(spec.get("rhythmus"))}
        spiel = " data-spiel='" + html.escape(json.dumps(daten, ensure_ascii=False), quote=True) + "'"
    bild = svg(noten, **spec)
    import re
    breite = float(re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+)', bild).group(1))
    if breite > 420:
        klasse += " lang"
    return f'<figure class="notenbeispiel {klasse}"{spiel}><div class="bild">{bild}</div>{cap}</figure>'


def glyphen_js(ziel):
    with open(os.path.join(_HIER, "glyphen.json"), encoding="utf-8") as f:
        daten = f.read()
    with open(ziel, "w", encoding="utf-8") as f:
        f.write("/* Notenzeichen aus der Schrift Bravura (SIL Open Font License, siehe OFL-Bravura.txt) */\nwindow.NOTEN_GLYPHEN = " + daten + ";\n")
