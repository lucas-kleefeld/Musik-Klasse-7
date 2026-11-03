"""Eigene Zeichnungen (Skizzenheft-Stil) für Köpfe, Kacheln und das Logo."""
import json, math, os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "glyphen.json"), encoding="utf-8") as _f:
    GLYPHEN = json.load(_f)


def deko(viewbox, inhalt, klasse="ill"):
    return f'<svg class="{klasse}" viewBox="{viewbox}" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">{inhalt}</svg>'


def svg(viewbox, inhalt, titel, beschreibung="", klasse="ill"):
    import hashlib
    vid = "i" + hashlib.md5(titel.encode()).hexdigest()[:8]
    desc = f'<desc id="{vid}d">{beschreibung}</desc>' if beschreibung else ""
    return (f'<svg class="{klasse}" viewBox="{viewbox}" role="img" aria-labelledby="{vid}t{" " + vid + "d" if desc else ""}" xmlns="http://www.w3.org/2000/svg">'
            f'<title id="{vid}t">{titel}</title>{desc}{inhalt}</svg>')


def text(x, y, t, klasse="h", anker="middle", drehung=0):
    rot = f' transform="rotate({drehung} {x} {y})"' if drehung else ""
    return f'<text class="{klasse}" x="{x}" y="{y}" text-anchor="{anker}"{rot}>{t}</text>'


def pfeil(x1, y1, x2, y2, klasse="s2", bogen=0):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - bogen
    ang = math.atan2(y2 - my, x2 - mx)
    a1 = (x2 - 9 * math.cos(ang - 0.45), y2 - 9 * math.sin(ang - 0.45))
    a2 = (x2 - 9 * math.cos(ang + 0.45), y2 - 9 * math.sin(ang + 0.45))
    return (f'<path class="{klasse}" fill="none" d="M{x1} {y1} Q {mx} {my} {x2} {y2}"/>'
            f'<path class="{klasse}" fill="none" d="M{a1[0]:.1f} {a1[1]:.1f} L {x2} {y2} L {a2[0]:.1f} {a2[1]:.1f}"/>')


def blob(x, y, rx, ry, fill, drehung=0):
    return (f'<path transform="translate({x} {y}) rotate({drehung})" class="{fill}" '
            f'd="M{-rx} 0 C {-rx} {-ry * 0.9:.1f}, {-rx * 0.3:.1f} {-ry}, {rx * 0.2:.1f} {-ry} C {rx * 0.9:.1f} {-ry}, {rx} {-ry * 0.4:.1f}, {rx} {ry * 0.1:.1f} '
            f'C {rx} {ry * 0.8:.1f}, {rx * 0.4:.1f} {ry}, {-rx * 0.1:.1f} {ry} C {-rx * 0.8:.1f} {ry}, {-rx} {ry * 0.6:.1f}, {-rx} 0 Z"/>')


def funkeln(x, y, s=1.0, klasse="k-bernstein"):
    return f'<path transform="translate({x} {y}) scale({s})" class="s2 {klasse}" d="M0 -8 V8 M-8 0 H8 M-5 -5 L5 5 M5 -5 L-5 5" fill="none"/>'


def g(name, x, y, groesse=10, klasse="d"):
    """Notenzeichen aus Bravura; groesse = Linienabstand in px"""
    return f'<path class="{klasse}" transform="translate({x} {y}) scale({groesse})" d="{GLYPHEN[name]["d"]}"/>'


def note(x, y, groesse=10, art="viertel", hals=True, klasse="d"):
    kopf = {"ganze": "noteheadWhole", "halbe": "noteheadHalf"}.get(art, "noteheadBlack")
    i = g(kopf, x, y, groesse, klasse)
    if art != "ganze" and hals:
        hx = x + 1.12 * groesse
        i += f'<line class="s" x1="{hx:.1f}" y1="{y - 0.17 * groesse:.1f}" x2="{hx:.1f}" y2="{y - 3.5 * groesse:.1f}" stroke-width="{max(1.2, 0.13 * groesse):.1f}"/>'
        if art in ("achtel", "sechzehntel"):
            i += g("flag8thUp" if art == "achtel" else "flag16thUp", hx - 0.06 * groesse, y - 3.5 * groesse, groesse, klasse)
    return i


def notenlinien(x, y, breite, sp=10, klasse="s2"):
    return "".join(f'<line class="{klasse}" x1="{x}" y1="{y + k * sp}" x2="{x + breite}" y2="{y + k * sp}"/>' for k in range(5))


def tasten(x, y, n=8, w=26, h=96, markiert=(), schwarz_markiert=()):
    """Klaviatur ab c: n weiße Tasten"""
    i = ""
    for k in range(n):
        f = "f-gelb" if k in markiert else "f-weiss"
        i += f'<rect class="s2 {f}" x="{x + k * w}" y="{y}" width="{w}" height="{h}" rx="3"/>'
    for k in range(n - 1):
        if k % 7 in (2, 6):
            continue
        f = "f-rosa-tief" if k in schwarz_markiert else "d"
        i += f'<rect class="{f}" x="{x + (k + 1) * w - w * 0.3}" y="{y}" width="{w * 0.6}" height="{h * 0.6}" rx="2"/>'
    return i


def lautsprecher(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path class="s f-gelb" d="M-20 -10 h12 l16 -14 v48 l-16 -14 h-12 z"/>'
            '<path class="s2" fill="none" d="M16 -8 q8 8 0 16 M22 -14 q14 14 0 28"/></g>')


def metronom(x, y, s=1.0, winkel=-18):
    return (f'<g transform="translate({x} {y}) scale({s})"><path class="s f-sand" d="M-26 40 L -12 -40 H 12 L 26 40 Z"/>'
            f'<rect class="s2 f-weiss" x="-14" y="-6" width="28" height="30" rx="3"/>'
            f'<g transform="rotate({winkel} 0 30)"><line class="s" x1="0" y1="30" x2="0" y2="-34"/><rect class="s f-rosa" x="-6" y="-14" width="12" height="9" rx="2"/></g></g>')


# ---------------------------------------------------------------- Logo
LOGO = deko("0 0 40 40", '<circle class="s2 f-gelb" cx="20" cy="20" r="17"/>' + note(12, 27, 5.5, "achtel", klasse="d"))


# ---------------------------------------------------------------- Startseite
def hero_bild():
    i = blob(260, 160, 240, 130, "f-gelb-weich", -4)
    i += notenlinien(40, 70, 440, 14)
    i += g("gClef", 52, 112, 14)
    for k, (st, art) in enumerate([(0, "viertel"), (2, "viertel"), (4, "halbe"), (7, "achtel"), (9, "achtel"), (11, "ganze")]):
        i += note(130 + k * 55, 126 - st * 7, 14, art)
    i += tasten(150, 200, 8, 26, 80, markiert=(0, 2, 4)) + metronom(430, 230, 0.9) + lautsprecher(80, 240, 1.2)
    i += funkeln(470, 40, 1) + funkeln(30, 180, 0.8, "k-rosa")
    return deko("0 0 520 320", i, "ill hero-bild")


def kopf(nr):
    """Kopfbild eines Kapitels"""
    hint = blob(300, 112, 280, 96, "f-gelb-weich", 2)
    i = hint
    if nr == 1:
        for k, art in enumerate(["ganze", "halbe", "viertel", "achtel", "sechzehntel"]):
            i += note(70 + k * 88, 150, 16, art)
        i += metronom(540, 120, 0.8)
    elif nr == 2:
        for k, (n, yy) in enumerate([("restWhole", 90), ("restHalf", 110), ("restQuarter", 120), ("rest8th", 120), ("rest16th", 120)]):
            i += notenlinien(60 + k * 100, 70, 70, 14, "s2 gestrichelt") if k == 0 else ""
            i += g(n, 80 + k * 100, yy, 16)
        i += text(330, 200, "psst …", "hk")
    elif nr == 3:
        i += note(120, 150, 16, "halbe") + g("augmentationDot", 152, 150, 16) + text(200, 160, "=", "h")
        i += note(250, 150, 16, "viertel") + note(310, 150, 16, "viertel") + note(370, 150, 16, "viertel")
        i += g("tuplet3", 460, 70, 16) + note(430, 150, 14, "achtel") + note(470, 150, 14, "achtel") + note(510, 150, 14, "achtel")
    elif nr == 4:
        i += notenlinien(60, 70, 480, 14) + g("gClef", 74, 112, 14)
        for k in range(8):
            i += note(160 + k * 46, 140 - k * 7, 14, "ganze")
        i += text(300, 200, "c′ d′ e′ f′ g′ a′ h′ c″", "hk")
    elif nr == "bass":
        i += notenlinien(60, 70, 480, 14) + g("fClef", 74, 84, 14)
        for k in range(8):
            i += note(170 + k * 44, 126 - k * 7, 14, "ganze")
        i += text(330, 200, "G A H c d e f g", "hk")
        i += '<path class="s f-sand" d="M520 40 q 18 -6 26 10 l -6 120 q -8 18 -22 0 z"/><line class="s2" x1="534" y1="60" x2="534" y2="180"/>'
    elif nr == 5:
        i += g("accidentalSharp", 140, 110, 22) + g("accidentalFlat", 280, 120, 22) + g("accidentalNatural", 420, 110, 22)
        i += text(160, 196, "erhöht", "hk") + text(290, 196, "erniedrigt", "hk") + text(430, 196, "löst auf", "hk")
    elif nr == 6:
        i += g("dynamicPiano", 90, 140, 22) + text(130, 190, "leise", "hk")
        i += '<path class="s k-bernstein" fill="none" stroke-width="3" d="M250 80 L 170 110 L 250 140"/>'.replace("170", "180")
        i += g("dynamicForte", 300, 140, 22) + text(330, 190, "laut", "hk") + lautsprecher(480, 110, 1.6)
    elif nr == 7:
        for k in range(8):
            i += f'<rect class="s {"f-gelb" if k in (2, 6) else "f-weiss"}" x="{70 + k * 60}" y="{180 - k * 16}" width="58" height="{18 + k * 16}" rx="4"/>'
        i += text(220, 60, "1 – 1 – ½ – 1 – 1 – 1 – ½", "h")
    elif nr == 8:
        for k in range(8):
            i += f'<rect class="s {"f-blau" if k in (1, 4) else "f-weiss"}" x="{70 + k * 60}" y="{180 - k * 16}" width="58" height="{18 + k * 16}" rx="4"/>'
        i += text(220, 60, "1 – ½ – 1 – 1 – ½ – 1 – 1", "h")
    elif nr == 9:
        i += tasten(90, 60, 9, 34, 120, markiert=(0, 2, 4)) + '<path class="s2 k-rosa" fill="none" stroke-width="3" d="M107 52 Q 141 18 175 52"/>' + text(141, 26, "Terz", "hk")
        i += '<path class="s2 k-blau" fill="none" stroke-width="3" d="M107 192 Q 175 240 243 192"/>' + text(175, 214, "Quinte", "hk")
    elif nr == 10:
        i += notenlinien(160, 60, 280, 14) + g("gClef", 172, 102, 14)
        for st in (0, 2, 4):
            i += g("noteheadWhole", 300, 130 - st * 7, 14)
        i += text(470, 130 - 0 * 7, "Grundton", "hk", "start") + text(470, 130 - 2 * 7 - 10, "Terz", "hk", "start") + text(470, 130 - 4 * 7 - 20, "Quinte", "hk", "start")
    else:
        cx, cy, r = 300, 110, 90
        i += f'<circle class="s f-weiss" cx="{cx}" cy="{cy}" r="{r}"/><circle class="s2 f-gelb-weich" cx="{cx}" cy="{cy}" r="{r * 0.58}"/>'
        for k, t in enumerate(["C", "G", "D", "A", "E", "H", "Fis", "Des", "As", "Es", "B", "F"]):
            w = math.radians(-90 + k * 30)
            i += text(round(cx + math.cos(w) * r * 0.8), round(cy + math.sin(w) * r * 0.8 + 6), t, "hk")
        i += pfeil(400, 60, 430, 110, "s2 k-bernstein", -20)
    return deko("0 0 600 220", i, "ill lt-kopf")


def symbol(name):
    """Kleine Kachel-Symbole (64 x 64)"""
    S = {
        "notenwerte": note(14, 46, 7, "halbe") + note(36, 46, 7, "achtel"),
        "pausen": g("restQuarter", 18, 32, 10) + g("rest8th", 38, 32, 10),
        "punktierung": note(18, 46, 8, "halbe") + g("augmentationDot", 34, 46, 8),
        "triolen": g("tuplet3", 24, 14, 8) + note(8, 50, 6, "achtel") + note(26, 50, 6, "achtel") + note(44, 50, 6, "achtel"),
        "violinschluessel": notenlinien(4, 18, 56, 7) + g("gClef", 10, 39, 7),
        "bassschluessel": notenlinien(4, 18, 56, 7) + g("fClef", 8, 25, 7),
        "vorzeichen": g("accidentalSharp", 12, 32, 10) + g("accidentalFlat", 36, 34, 10),
        "dynamik": g("dynamicMezzo", 8, 38, 9) + g("dynamicForte", 32, 38, 9),
        "tonleiter": "".join(f'<rect class="s2 {"f-gelb" if k in (2, 6) else "f-weiss"}" x="{4 + k * 7}" y="{52 - k * 5}" width="7" height="{6 + k * 5}"/>' for k in range(8)),
        "moll": "".join(f'<rect class="s2 {"f-blau" if k in (1, 4) else "f-weiss"}" x="{4 + k * 7}" y="{52 - k * 5}" width="7" height="{6 + k * 5}"/>' for k in range(8)),
        "intervalle": tasten(4, 14, 7, 8, 36, markiert=(0, 4)),
        "dreiklaenge": "".join(g("noteheadWhole", 22, 48 - k * 10, 9) for k in range(3)),
        "quintenzirkel": '<circle class="s2 f-weiss" cx="32" cy="32" r="24"/><circle class="s2 f-gelb-weich" cx="32" cy="32" r="13"/>' + text(32, 16, "C", "hk") + text(52, 38, "G", "hk") + text(12, 38, "F", "hk"),
        "klaviatur": tasten(4, 12, 7, 8, 40),
        "taktbaukasten": '<rect class="s2 f-weiss" x="6" y="14" width="52" height="36" rx="4"/>' + note(14, 42, 5, "viertel") + note(30, 42, 5, "achtel") + note(44, 42, 5, "achtel"),
        "notentrainer": notenlinien(6, 16, 52, 7) + g("noteheadBlack", 28, 30, 7) + funkeln(52, 10, 0.6),
        "quiz": '<path class="s f-gelb" d="M10 14 Q 10 8 16 8 H 48 Q 54 8 54 14 V 38 Q 54 44 48 44 H 28 L 18 54 L 20 44 H 16 Q 10 44 10 38 Z"/><text class="h" x="32" y="36" text-anchor="middle">?</text>',
        "lesen": notenlinien(6, 12, 52, 7) + g("noteheadBlack", 22, 26, 7) + '<rect class="s2 f-weiss" x="10" y="48" width="44" height="10" rx="2"/>',
        "notieren": notenlinien(6, 12, 52, 7) + g("noteheadBlack", 30, 33, 7, "d k-rosa-f") + '<path class="s2" d="M44 50 l 8 -14 l 4 2 l -8 14 z" fill="none"/>',
        "zuordnen": '<rect class="s2 f-weiss" x="6" y="12" width="20" height="12" rx="3"/><rect class="s2 f-gelb" x="38" y="12" width="20" height="12" rx="3"/><rect class="s2 f-weiss" x="6" y="40" width="20" height="12" rx="3"/><rect class="s2 f-gelb" x="38" y="40" width="20" height="12" rx="3"/><path class="s2" d="M26 18 L 38 46 M 26 46 L 38 18" fill="none"/>',
        "sortieren": '<rect class="s2 f-weiss" x="6" y="10" width="52" height="12" rx="3"/><rect class="s2 f-gelb" x="6" y="26" width="52" height="12" rx="3"/><rect class="s2 f-weiss" x="6" y="42" width="52" height="12" rx="3"/>',
        "luecken": '<path class="s2" d="M6 20 H 22 M 42 20 H 58 M 6 40 H 30 M 50 40 H 58" fill="none"/><rect class="s2 f-gelb" x="24" y="13" width="16" height="12" rx="2"/><rect class="s2 f-gelb" x="32" y="33" width="16" height="12" rx="2"/>',
        "halbtoene": "".join(g("noteheadBlack", 6 + k * 13, 46 - k * 4, 6) for k in range(4)) + '<path class="s2 k-rosa" fill="none" d="M30 26 Q 37 16 44 22"/>',
        "rhythmus": note(8, 48, 6, "viertel") + note(24, 48, 6, "achtel") + note(40, 48, 6, "sechzehntel"),
    }
    return deko("0 0 64 64", S.get(name, S["quiz"]), "ill symbol")
