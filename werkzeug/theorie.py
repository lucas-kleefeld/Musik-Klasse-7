"""Musiktheorie-Helfer: Tonnamen, Halbtöne, Tonleitern, Intervalle, Dreiklänge.

Interne Schreibweise wie im Notensatz: Buchstabe A–G (B = h), Vorzeichen # oder b, Oktave.
C4 = c′ (eingestrichenes c), C5 = c″.
"""
import re

STAMM = "CDEFGAB"
HALB = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
DEUTSCH = {"C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "A": "a", "B": "h"}


def zerlege(ton):
    m = re.fullmatch(r"([A-G])(#|b|n)?(\d)", ton)
    return m.group(1), (m.group(2) or "").replace("n", ""), int(m.group(3))


def midi(ton):
    b, v, o = zerlege(ton)
    return 12 * (o + 1) + HALB[b] + (1 if v == "#" else -1 if v == "b" else 0)


def stufe(ton):
    b, v, o = zerlege(ton)
    return STAMM.index(b) + 7 * o


def name(ton, oktave=False):
    """deutscher Tonname, z. B. F#4 -> fis (mit oktave=True: fis′)"""
    b, v, o = zerlege(ton)
    n = DEUTSCH[b]
    if v == "#":
        n += "is"
    elif v == "b":
        n = {"E": "es", "A": "as", "B": "b"}.get(b, n + "es")
    if oktave:
        if o <= 2:
            n = n[0].upper() + n[1:]
        n += {3: "", 4: "′", 5: "″", 6: "‴"}.get(o, "")
    return n


def antwort(ton, oktave=False):
    """akzeptierte Schreibweisen für Eingaben"""
    n = name(ton)
    if not oktave:
        alt = {"b": ["b"], "h": ["h"]}.get(n, [n])
        return alt
    b, v, o = zerlege(ton)
    if o == 2:
        return [n[0].upper() + n[1:]]
    striche = {3: "", 4: "'", 5: "''", 6: "'''"}[o]
    return [n + striche, n + str(o - 3) if o > 3 else n]


def ton_aus(stufe_nr, halbton):
    """Ton mit gegebener diatonischer Stufe und Halbtonzahl (MIDI)"""
    b = STAMM[stufe_nr % 7]
    o = stufe_nr // 7
    basis = 12 * (o + 1) + HALB[b]
    d = halbton - basis
    v = {0: "", 1: "#", -1: "b"}.get(d)
    if v is None:
        raise ValueError(f"Doppelvorzeichen nötig: {b}{o} {d}")
    return f"{b}{v}{o}"


DUR = [2, 2, 1, 2, 2, 2, 1]
MOLL = [2, 1, 2, 2, 1, 2, 2]
MOLL_HARM = [2, 1, 2, 2, 1, 3, 1]


def tonleiter(grundton, schritte=DUR):
    toene = [grundton]
    st, m = stufe(grundton), midi(grundton)
    for s in schritte:
        st += 1
        m += s
        toene.append(ton_aus(st, m))
    return toene


INTERVALLE = {  # (Stufenabstand, Halbtöne) -> Name
    (0, 0): "reine Prime", (1, 1): "kleine Sekunde", (1, 2): "große Sekunde", (2, 3): "kleine Terz", (2, 4): "große Terz",
    (3, 5): "reine Quarte", (3, 6): "übermäßige Quarte", (4, 6): "verminderte Quinte", (4, 7): "reine Quinte",
    (5, 8): "kleine Sexte", (5, 9): "große Sexte", (6, 10): "kleine Septime", (6, 11): "große Septime", (7, 12): "reine Oktave",
}
INTERVALL_HALB = {v: k for k, v in INTERVALLE.items()}


def intervall(a, b):
    return INTERVALLE[(stufe(b) - stufe(a), midi(b) - midi(a))]


def ueber(ton, intervall_name):
    d, h = INTERVALL_HALB[intervall_name]
    return ton_aus(stufe(ton) + d, midi(ton) + h)


DREIKLANG = {"Dur": (4, 7), "Moll": (3, 7), "vermindert": (3, 6), "übermäßig": (4, 8)}


def dreiklang(grundton, art="Dur"):
    t, q = DREIKLANG[art]
    return [grundton, ton_aus(stufe(grundton) + 2, midi(grundton) + t), ton_aus(stufe(grundton) + 4, midi(grundton) + q)]


# Quintenzirkel: Vorzeichenzahl -> (Dur, Moll)
TONARTEN = {0: ("C-Dur", "a-Moll"), 1: ("G-Dur", "e-Moll"), 2: ("D-Dur", "h-Moll"), 3: ("A-Dur", "fis-Moll"), 4: ("E-Dur", "cis-Moll"),
            5: ("H-Dur", "gis-Moll"), 6: ("Fis-Dur", "dis-Moll"), -1: ("F-Dur", "d-Moll"), -2: ("B-Dur", "g-Moll"), -3: ("Es-Dur", "c-Moll"),
            -4: ("As-Dur", "f-Moll"), -5: ("Des-Dur", "b-Moll"), -6: ("Ges-Dur", "es-Moll")}
GRUNDTON = {0: "C4", 1: "G4", 2: "D4", 3: "A4", 4: "E4", 5: "B4", 6: "F#4", -1: "F4", -2: "Bb4", -3: "Eb4", -4: "Ab4", -5: "Db4", -6: "Gb4"}


def ganze(toene, labels=None, sep=" "):
    """Hilfsfunktion: Liste von Tönen als ganze Noten für den Notensatz"""
    out = []
    for i, t in enumerate(toene):
        lab = ("@" + labels[i].replace(" ", "_")) if labels else ""
        out.append(f"{t}/1{lab}")
    return sep.join(out)


if __name__ == "__main__":
    assert tonleiter("G4") == ["G4", "A4", "B4", "C5", "D5", "E5", "F#5", "G5"]
    assert tonleiter("F4") == ["F4", "G4", "A4", "Bb4", "C5", "D5", "E5", "F5"]
    assert tonleiter("A4", MOLL) == ["A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5"]
    assert intervall("C4", "E4") == "große Terz" and intervall("E4", "G4") == "kleine Terz" and intervall("F4", "B4") == "übermäßige Quarte"
    assert dreiklang("D4", "Moll") == ["D4", "F4", "A4"] and dreiklang("B4", "vermindert") == ["B4", "D5", "F5"]
    assert name("Bb4") == "b" and name("Eb4") == "es" and name("Ab4") == "as" and name("Db4") == "des" and name("F#4", True) == "fis′"
    for n, gt in GRUNDTON.items():
        tl = tonleiter(gt)
        vz = sum(1 if "#" in t else -1 if "b" in t else 0 for t in tl[:7])
        assert vz == n, (gt, vz)
    print("ok")
