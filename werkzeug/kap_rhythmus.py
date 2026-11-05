"""Kapitel 1 bis 3: Notenwerte und Takt, Pausen, Punktierung, Haltebögen und Triolen."""
from notensatz import N
from zeichnungen import svg, g, note, text, notenlinien

R = {"rhythmus": True}


def aufbau_note():
    i = notenlinien(20, 40, 420, 12, "s2 nl-blass")
    i += g("noteheadBlack", 100, 100, 12) + f'<line class="s" x1="114" y1="98" x2="114" y2="58" stroke-width="1.6"/>' + g("flag8thUp", 113, 58, 12)
    i += g("noteheadBlack", 260, 88, 12) + g("noteheadBlack", 330, 76, 12)
    i += '<line class="s" x1="274" y1="86" x2="274" y2="44" stroke-width="1.6"/><line class="s" x1="344" y1="74" x2="344" y2="38" stroke-width="1.6"/>'
    i += '<path class="d" d="M273 44 L 345 38 L 345 44 L 273 50 Z"/>'
    for (x1, y1), (x2, y2), t in [((95, 102), (60, 140), "Notenkopf"), ((114, 80), (170, 120), "Notenhals"), ((124, 66), (180, 30), "Fähnchen"),
                                  ((310, 42), (330, 16), "Balken"), ((255, 92), (240, 140), "Notenkopf")]:
        i += f'<path class="s2 k-bernstein" fill="none" d="M{x1} {y1} L {x2} {y2 - 6 if y2 < y1 else y2 - 18}"/>' + text(x2, y2, t, "hk")
    return svg("0 0 460 150", i, "Aufbau einer Note", "Eine Achtelnote mit Notenkopf, Notenhals und Fähnchen. Daneben zwei Achtelnoten, deren Fähnchen zu einem Balken verbunden sind.")


NOTENBAUM = (
    N("C4/1", rhythmus=True, zoom=1.4, spiel=False)
    + N("C4/2 C4/2", rhythmus=True, zoom=1.4, spiel=False)
    + N("C4/4 C4/4 C4/4 C4/4", rhythmus=True, zoom=1.4, spiel=False)
    + N("( C4/8 C4/8 ) ( C4/8 C4/8 ) ( C4/8 C4/8 ) ( C4/8 C4/8 )", rhythmus=True, zoom=1.4, spiel=False)
    + N("( C4/16 C4/16 C4/16 C4/16 ) ( C4/16 C4/16 C4/16 C4/16 ) ( C4/16 C4/16 C4/16 C4/16 ) ( C4/16 C4/16 C4/16 C4/16 )", rhythmus=True, zoom=1.4, spiel=False)
)



def takt_aufgabe(takt, takte):
    """takte: Liste von Takten, jeder Takt eine Liste von Tokens. Ergebnis: Aufgabe ohne Taktstriche."""
    from fractions import Fraction as F
    z, n = map(int, takt.split("/"))
    soll = F(z, n)
    loesung, zaehler = [], 0
    for t in takte:
        summe, anzahl = F(0), 0
        for tok in " ".join(t).split():
            if tok in ("(", ")", "3(", "3["):
                continue
            wert = tok.split("/")[1]
            d = F(1, int(wert.rstrip("."))) * (F(3, 2) if wert.endswith(".") else 1)
            summe += soll if tok == "R/1" else d
            anzahl += 1
        assert summe == soll, (takt, t, summe)
        zaehler += anzahl
        loesung.append(zaehler - 1)
    return {"takt": takt, "noten": " ".join(" ".join(t) for t in takte), "loesung": loesung[:-1]}

KAPITEL = {}

# ======================================================================
KAPITEL[1] = {
"kurz": "Ganze, Halbe, Viertel, Achtel und Sechzehntel, Takt und Taktarten, richtig zählen.",
"inhalt": f"""
<p class="lead">Noten zeigen nicht nur, welcher Ton gespielt wird, sondern auch, wie lange er klingt. Diese Dauer nennt man <span class="fachwort">Notenwert</span>.</p>

<h2>Woraus eine Note besteht</h2>
<figure class="breit"><div class="bild">{aufbau_note()}</div><figcaption>Bestandteile einer Note</figcaption></figure>
<p>Der <strong>Notenkopf</strong> ist hohl oder ausgefüllt. Bis auf die ganze Note haben alle Noten einen <strong>Notenhals</strong>. Achtel und Sechzehntel bekommen zusätzlich <strong>Fähnchen</strong>. Stehen mehrere Achtel oder Sechzehntel nebeneinander, werden die Fähnchen meist zu <strong>Balken</strong> verbunden. Das macht die Noten leichter lesbar.</p>

<h2>Die Notenwerte</h2>
<div class="tabelle-scroll"><table class="notentabelle">
  <thead><tr><th>Note</th><th>Name</th><th>Dauer im 4/4-Takt</th></tr></thead>
  <tbody>
    <tr><td>{N("C4/1", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>ganze Note</td><td>4 Schläge (4 Viertel)</td></tr>
    <tr><td>{N("C4/2", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>halbe Note</td><td>2 Schläge</td></tr>
    <tr><td>{N("C4/4", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>Viertelnote</td><td>1 Schlag</td></tr>
    <tr><td>{N("C4/8", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>Achtelnote</td><td>½ Schlag</td></tr>
    <tr><td>{N("C4/16", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>Sechzehntelnote</td><td>¼ Schlag</td></tr>
  </tbody>
</table></div>
<p>Jeder Notenwert ist genau halb so lang wie der nächstgrößere. Das zeigt der <strong>Notenbaum</strong>: In jeder Zeile ist insgesamt gleich viel Zeit verteilt.</p>
<figure class="breit notenbaum">{NOTENBAUM}<figcaption>Der Notenbaum: 1 Ganze = 2 Halbe = 4 Viertel = 8 Achtel = 16 Sechzehntel</figcaption></figure>

<h2>Der Takt</h2>
<p>Musik ist in gleich lange Abschnitte eingeteilt, die <span class="fachwort">Takte</span>. Sie werden durch <strong>Taktstriche</strong> getrennt. Am Ende eines Stückes steht ein <strong>Schlussstrich</strong>. Die <span class="fachwort">Taktangabe</span> am Anfang sieht aus wie ein Bruch:</p>
<ul>
  <li>Die <strong>untere Zahl</strong> nennt den Notenwert, der gezählt wird (4 = Viertel, 8 = Achtel).</li>
  <li>Die <strong>obere Zahl</strong> sagt, wie viele davon in einen Takt passen.</li>
</ul>
{N("C4/4@1 C4/4@2 C4/4@3 C4/4@4 | C4/2@1(2) C4/2@3(4) | C4/1@1(2,3,4) |.", "4/4-Takt: vier Viertel pro Takt. Statt 4/4 steht oft ein C.", takt="4/4", rhythmus=True)}
{N("C4/4@1 C4/4@2 C4/4@3 | C4/2@1(2) C4/4@3 | C4/2.@1(2,3) |.", "3/4-Takt: drei Viertel pro Takt, zum Beispiel beim Walzer", takt="3/4", rhythmus=True)}
{N("C4/4@1 C4/4@2 | C4/2@1(2) |.", "2/4-Takt: zwei Viertel pro Takt, zum Beispiel beim Marsch", takt="2/4", rhythmus=True)}
{N("( C4/8@1 C4/8@2 C4/8@3 ) ( C4/8@4 C4/8@5 C4/8@6 ) | C4/4.@1(2,3) C4/4.@4(5,6) |.", "6/8-Takt: sechs Achtel pro Takt, gefühlt in zwei Gruppen zu je drei", takt="6/8", rhythmus=True)}
<p>Die erste Zählzeit eines Taktes ist am stärksten betont. Im 4/4-Takt ist auch die 3 betont, aber etwas schwächer.</p>

<h2>Richtig zählen</h2>
<p>Unter die Noten schreibt man die <span class="fachwort">Zählzeiten</span>. Zählzeiten, auf denen eine Note nur weiterklingt, stehen in Klammern: Sie werden mitgezählt, aber nicht neu gespielt. Im 4/4-Takt schreibt man so:</p>
<div class="tabelle-scroll"><table>
  <thead><tr><th>Notenwert (Note oder Pause)</th><th>Zählzeiten</th></tr></thead>
  <tbody>
    <tr><td>ganze Note, ganze Pause</td><td><strong>1(2,3,4)</strong></td></tr>
    <tr><td>halbe Note, halbe Pause</td><td><strong>1(2)</strong> oder <strong>3(4)</strong></td></tr>
    <tr><td>Viertelnote, Viertelpause</td><td><strong>1, 2, 3, 4</strong></td></tr>
    <tr><td>Achtelnote, Achtelpause</td><td><strong>1 + 2 + 3 + 4 +</strong></td></tr>
    <tr><td>Sechzehntelnote, Sechzehntelpause</td><td><strong>1 a + a, 2 a + a, 3 a + a, 4 a + a</strong></td></tr>
  </tbody>
</table></div>
<p>Das + spricht man „und“. Damit man auch kurze Notenwerte genau spielt, teilt man die Schläge beim Zählen also immer weiter auf:</p>
{N("C4/1@1(2,3,4) | C4/2@1(2) C4/2@3(4) | C4/4@1 C4/4@2 C4/4@3 C4/4@4 |", "Ganze, Halbe und Viertel mit Zählzeiten", takt="4/4", rhythmus=True)}
{N("( C4/8@1 C4/8@+ ) ( C4/8@2 C4/8@+ ) ( C4/8@3 C4/8@+ ) ( C4/8@4 C4/8@+ ) | ( C4/16@1 C4/16@a C4/16@+ C4/16@a ) ( C4/16@2 C4/16@a C4/16@+ C4/16@a ) ( C4/16@3 C4/16@a C4/16@+ C4/16@a ) ( C4/16@4 C4/16@a C4/16@+ C4/16@a ) |", "Achtel: 1 + 2 + 3 + 4 + – Sechzehntel: 1 a + a, 2 a + a …", takt="4/4", rhythmus=True)}
{N("C4/4@1 C4/4@2 ( C4/8@3 C4/8@+ ) ( C4/8@4 C4/8@+ ) | ( C4/16@1 C4/16@a C4/16@+ C4/16@a ) ( C4/8@2 C4/8@+ ) C4/2@3(4) |.", "Gemischte Notenwerte mit Zählzeiten", takt="4/4", rhythmus=True)}
<p>Beginnt ein Lied nicht auf der Eins, sondern mit einem unvollständigen Takt, spricht man von einem <span class="fachwort">Auftakt</span>. Der letzte Takt ist dann um genau diese Länge kürzer.</p>
<p><a class="knopf leise" href="../werkzeuge/taktbaukasten.html">Takte im Taktbaukasten selbst bauen und anhören</a></p>

<div class="merke"><strong>Merke</strong>
<p>1 ganze Note = 2 halbe = 4 Viertel = 8 Achtel = 16 Sechzehntel. Die Taktangabe zeigt, wie viele Schläge (obere Zahl) von welchem Notenwert (untere Zahl) in einen Takt passen. In jedem Takt muss die Summe der Notenwerte genau stimmen.</p></div>
""",
"aufgaben": [
 ("I", "Zeichne den Notenbaum von der ganzen Note bis zu den Sechzehnteln ab und beschrifte jede Zeile.", 0, ""),
 ("I", "Nenne die Bestandteile einer Achtelnote.", 2, ""),
 ("II", "Berechne: Wie viele Achtel passen in eine halbe Note? Wie viele Sechzehntel in eine Viertel? Wie viele Viertel in zwei ganze Noten?", 3, ""),
 ("II", "Schreibe unter jede Note die Zählzeiten (1, 2, 3, 4 bzw. 1 + 2 + oder 1(2) für eine halbe Note).", 0,
  N("C4/4 ( C4/8 C4/8 ) C4/2 | ( C4/8 C4/8 ) ( C4/8 C4/8 ) C4/4 C4/4 | C4/1 |.", takt="4/4", rhythmus=True)),
 ("II", "Setze die fehlenden Taktstriche. Achte auf die Taktangabe.", 0,
  N("C4/4 C4/4 C4/4 C4/2 C4/4 ( C4/8 C4/8 ) C4/4 C4/4 C4/2. |.", takt="3/4", rhythmus=True)),
 ("III", "Erfinde einen eigenen Rhythmus mit vier Takten im 4/4-Takt. Verwende jeden Notenwert mindestens einmal. Klatsche ihn deiner Nachbarin oder deinem Nachbarn vor.", 0, ""),
],
"uebungen": [
 {"slug": "k1-notenwerte", "titel": "Quiz: Welcher Notenwert ist das?", "kurz": "Notenwerte erkennen und vergleichen", "typ": "notenquiz", "symbol": "notenwerte",
  "anleitung": "Wähle die richtige Antwort. Du bekommst sofort eine Rückmeldung.",
  "daten": {"fragen": [
   {"frage": "Wie heißt diese Note?", "noten": "C4/2", "spec": R, "optionen": ["halbe Note", "ganze Note", "Viertelnote", "Achtelnote"], "richtig": 0, "erklaerung": "Hohler Kopf mit Hals: halbe Note."},
   {"frage": "Wie heißt diese Note?", "noten": "C4/16", "spec": R, "optionen": ["Sechzehntelnote", "Achtelnote", "Viertelnote", "halbe Note"], "richtig": 0, "erklaerung": "Zwei Fähnchen: Sechzehntel."},
   {"frage": "Wie heißt diese Note?", "noten": "C4/1", "spec": R, "optionen": ["ganze Note", "halbe Note", "Viertelnote", "Achtelpause"], "richtig": 0, "erklaerung": "Hohler Kopf ohne Hals: ganze Note."},
   {"frage": "Wie heißt diese Note?", "noten": "C4/8", "spec": R, "optionen": ["Achtelnote", "Sechzehntelnote", "Viertelnote", "halbe Note"], "richtig": 0, "erklaerung": "Ein Fähnchen: Achtel."},
   {"frage": "Welche Note dauert am längsten?", "optionen": [{"noten": "C4/2", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/16", "spec": R}], "richtig": 0, "erklaerung": "Die halbe Note dauert 2 Schläge."},
   {"frage": "Wie viele Achtel passen in eine halbe Note?", "optionen": ["4", "2", "8", "6"], "richtig": 0, "erklaerung": "1 Halbe = 2 Viertel = 4 Achtel."},
   {"frage": "Wie viele Sechzehntel ergeben eine Viertel?", "optionen": ["4", "2", "8", "16"], "richtig": 0, "erklaerung": "1 Viertel = 2 Achtel = 4 Sechzehntel."},
   {"frage": "Was ist gleich lang wie eine ganze Note?", "optionen": [{"noten": "C4/2 C4/4 C4/4", "spec": R}, {"noten": "C4/2 C4/4", "spec": R}, {"noten": "C4/4 C4/4 C4/4", "spec": R}, {"noten": "C4/2 ( C4/8 C4/8 )", "spec": R}], "richtig": 0, "erklaerung": "2 + 1 + 1 = 4 Viertel."},
   {"frage": "Was bedeutet die untere Zahl der Taktangabe 3/4?", "optionen": ["Es werden Viertel gezählt.", "Es gibt vier Takte.", "Der Takt hat vier Schläge.", "Man spielt viermal so schnell."], "richtig": 0, "erklaerung": "Die obere Zahl nennt die Anzahl: drei Viertel pro Takt."},
   {"frage": "Wie zählt man vier Sechzehntel auf einen Schlag?", "optionen": ["1 a + a", "1 + 2 +", "1 2 3 4", "1 tri o"], "richtig": 0, "erklaerung": "Die Sechzehntel teilen den Schlag in vier Teile."}
  ]}},
 {"slug": "k1-takt-vervollstaendigen", "titel": "Quiz: Was fehlt im Takt?", "kurz": "Takte mit dem passenden Notenwert vervollständigen", "typ": "notenquiz", "symbol": "rhythmus",
  "anleitung": "Welcher Notenwert gehört an die Stelle mit dem Fragezeichen, damit der Takt genau voll ist?",
  "daten": {"fragen": [
   {"frage": "4/4-Takt", "noten": "C4/2 C4/4 ?/4 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "C4/4", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/1", "spec": R}], "richtig": 0, "erklaerung": "2 + 1 = 3 Viertel, es fehlt eine Viertel."},
   {"frage": "3/4-Takt", "noten": "C4/4 ?/2 |", "spec": {"rhythmus": True, "takt": "3/4"}, "optionen": [{"noten": "C4/2", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/1", "spec": R}, {"noten": "C4/8", "spec": R}], "richtig": 0, "erklaerung": "1 + 2 = 3 Viertel."},
   {"frage": "2/4-Takt", "noten": "( C4/8 C4/8 ) ?/4 |", "spec": {"rhythmus": True, "takt": "2/4"}, "optionen": [{"noten": "C4/4", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/16", "spec": R}], "richtig": 0, "erklaerung": "Zwei Achtel = eine Viertel. Es fehlt noch eine Viertel."},
   {"frage": "4/4-Takt", "noten": "C4/4 ( C4/8 C4/8 ) ?/2 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "C4/2", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/1", "spec": R}, {"noten": "C4/8", "spec": R}], "richtig": 0, "erklaerung": "1 + 1 = 2 Viertel, es fehlt eine Halbe."},
   {"frage": "4/4-Takt", "noten": "( C4/16 C4/16 C4/16 C4/16 ) C4/2 ?/4 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "C4/4", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/16", "spec": R}], "richtig": 0, "erklaerung": "4 Sechzehntel = 1 Viertel; 1 + 2 = 3, es fehlt eine Viertel."},
   {"frage": "6/8-Takt", "noten": "( C4/8 C4/8 C4/8 ) C4/4 ?/8 |", "spec": {"rhythmus": True, "takt": "6/8"}, "optionen": [{"noten": "C4/8", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/16", "spec": R}, {"noten": "C4/2", "spec": R}], "richtig": 0, "erklaerung": "3 + 2 = 5 Achtel, es fehlt eine Achtel."},
   {"frage": "3/4-Takt", "noten": "( C4/8 C4/8 ) ( C4/8 C4/8 ) ?/4 |", "spec": {"rhythmus": True, "takt": "3/4"}, "optionen": [{"noten": "C4/4", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/16", "spec": R}], "richtig": 0, "erklaerung": "Vier Achtel = zwei Viertel, es fehlt eine Viertel."},
   {"frage": "Welche Taktangabe passt?", "noten": "C4/4 C4/4 C4/4 | C4/2 C4/4 | C4/4 ( C4/8 C4/8 ) C4/4 |", "spec": R, "optionen": ["3/4", "4/4", "2/4", "6/8"], "richtig": 0, "erklaerung": "Jeder Takt enthält drei Viertel."},
   {"frage": "Welche Taktangabe passt?", "noten": "C4/2 C4/2 | C4/4 C4/4 C4/2 | C4/1 |", "spec": R, "optionen": ["4/4", "3/4", "2/4", "6/8"], "richtig": 0, "erklaerung": "Jeder Takt enthält vier Viertel."}
  ]}},
 {"slug": "k1-taktstriche", "titel": "Taktstriche setzen", "kurz": "Takte in 2/4, 3/4 und 4/4 richtig abteilen", "typ": "taktstriche", "symbol": "rhythmus",
  "anleitung": "Achte auf die Taktangabe und zähle mit. Tippe zwischen zwei Noten, um dort einen Taktstrich zu setzen; noch einmal tippen nimmt ihn wieder weg. Der Schlussstrich ist schon da.",
  "daten": {"aufgaben": [
   takt_aufgabe("2/4", [["C4/4", "C4/4"], ["C4/2"], ["( C4/8 C4/8 )", "C4/4"], ["( C4/16 C4/16 C4/16 C4/16 )", "C4/4"]]),
   takt_aufgabe("2/4", [["( C4/8 C4/8 )", "( C4/8 C4/8 )"], ["C4/4", "( C4/8 C4/8 )"], ["C4/2"], ["C4/4", "C4/4"]]),
   takt_aufgabe("3/4", [["C4/2", "C4/4"], ["C4/4", "C4/4", "C4/4"], ["( C4/8 C4/8 )", "C4/2"], ["C4/4", "( C4/16 C4/16 C4/16 C4/16 )", "C4/4"]]),
   takt_aufgabe("3/4", [["C4/4", "C4/2"], ["( C4/8 C4/8 )", "( C4/8 C4/8 )", "C4/4"], ["C4/2", "( C4/8 C4/8 )"], ["C4/4", "C4/4", "C4/4"]]),
   takt_aufgabe("4/4", [["C4/2", "C4/4", "C4/4"], ["C4/1"], ["( C4/8 C4/8 )", "C4/4", "C4/2"], ["C4/4", "( C4/16 C4/16 C4/16 C4/16 )", "C4/2"]]),
   takt_aufgabe("4/4", [["C4/4", "C4/4", "C4/2"], ["( C4/8 C4/8 )", "( C4/8 C4/8 )", "C4/2"], ["C4/1"], ["C4/2", "C4/2"]])
  ]}},
 {"slug": "k1-begriffe", "titel": "Zuordnen: Begriffe rund um Note und Takt", "kurz": "Fachbegriffe und ihre Bedeutung", "typ": "zuordnen", "symbol": "zuordnen",
  "anleitung": "Wähle zu jedem Begriff die passende Erklärung.",
  "daten": {"paare": [
   {"links": "Notenkopf", "rechts": "zeigt Tonhöhe; hohl oder ausgefüllt"},
   {"links": "Notenhals", "rechts": "senkrechter Strich am Notenkopf"},
   {"links": "Fähnchen", "rechts": "kennzeichnet Achtel und Sechzehntel"},
   {"links": "Balken", "rechts": "verbindet mehrere Achtel oder Sechzehntel"},
   {"links": "Taktstrich", "rechts": "trennt zwei Takte voneinander"},
   {"links": "Schlussstrich", "rechts": "zeigt das Ende eines Stückes"},
   {"links": "Taktangabe", "rechts": "sagt, wie viele Schläge in einen Takt passen"},
   {"links": "Auftakt", "rechts": "unvollständiger Takt am Anfang"}
  ]}},
],
}

# ======================================================================
KAPITEL[2] = {
"kurz": "Pausenwerte von der ganzen bis zur Sechzehntelpause, ihre Lage im Notensystem und Pausen im Takt.",
"inhalt": f"""
<p class="lead">Auch Stille gehört zur Musik. Pausen sind genauso genau festgelegt wie Noten: Für jeden Notenwert gibt es eine passende Pause.</p>

<h2>Die Pausenwerte</h2>
<div class="tabelle-scroll"><table class="notentabelle">
  <thead><tr><th>Note</th><th>Pause</th><th>Name</th><th>Dauer im 4/4-Takt</th></tr></thead>
  <tbody>
    <tr><td>{N("C4/1", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>{N("R/1", oben=4, unten=1, zoom=1.2, klasse="mini", schluessel=False)}</td><td>ganze Pause</td><td>4 Schläge</td></tr>
    <tr><td>{N("C4/2", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>{N("R/2", oben=4, unten=1, zoom=1.2, klasse="mini", schluessel=False)}</td><td>halbe Pause</td><td>2 Schläge</td></tr>
    <tr><td>{N("C4/4", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>{N("R/4", oben=4, unten=1, zoom=1.2, klasse="mini", schluessel=False)}</td><td>Viertelpause</td><td>1 Schlag</td></tr>
    <tr><td>{N("C4/8", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>{N("R/8", oben=4, unten=1, zoom=1.2, klasse="mini", schluessel=False)}</td><td>Achtelpause</td><td>½ Schlag</td></tr>
    <tr><td>{N("C4/16", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>{N("R/16", oben=4, unten=1, zoom=1.2, klasse="mini", schluessel=False)}</td><td>Sechzehntelpause</td><td>¼ Schlag</td></tr>
  </tbody>
</table></div>

<h2>Ganze und halbe Pause unterscheiden</h2>
<p>Ganze und halbe Pause sehen fast gleich aus: ein kleiner Balken. Der Unterschied liegt in der Lage:</p>
<ul>
  <li>Die <strong>ganze Pause hängt</strong> unter der vierten Linie (von unten gezählt).</li>
  <li>Die <strong>halbe Pause liegt</strong> auf der dritten Linie, der Mittellinie.</li>
</ul>
<p>Eine Merkhilfe: Die ganze Pause ist schwerer, darum hängt sie nach unten. Oder: Die ganze Pause sieht aus wie ein Hut, der an der Garderobe hängt, die halbe wie ein Hut, der auf dem Kopf sitzt.</p>
{N("R/1@ganze R/2@halbe R/4@Viertel R/8@Achtel R/16@Sechzehntel", "Lage der Pausen im Notensystem", schluessel=False)}

<h2>Pausen im Takt</h2>
<p>Pausen werden genauso mitgezählt wie Noten. Noten und Pausen zusammen müssen den Takt genau füllen.</p>
{N("C4/4@1 R/4@2 C4/4@3 R/4@4 | C4/2@1(2) R/2@3(4) | R/4@1 C4/4@2 R/8@3 C4/8@+ C4/4@4 | C4/2@1(2) R/2@3(4) |.", "Noten und Pausen im 4/4-Takt mit Zählzeiten", takt="4/4", rhythmus=True)}
<p>Eine Besonderheit: Soll in einem Takt gar nichts gespielt werden, schreibt man immer eine <strong>ganze Pause</strong> in die Mitte des Taktes, egal welche Taktart gilt. Sie heißt dann <span class="fachwort">Ganztaktpause</span>.</p>
{N("C4/4 C4/4 C4/4 | R/1 | C4/2. |.", "Im 3/4-Takt steht die ganze Pause für einen ganzen Takt Stille.", takt="3/4", rhythmus=True)}

<div class="merke"><strong>Merke</strong>
<p>Zu jedem Notenwert gibt es eine Pause gleicher Länge. Die ganze Pause hängt unter der vierten Linie, die halbe liegt auf der Mittellinie. Pausen werden mitgezählt. Ein Takt ganz ohne Töne bekommt eine ganze Pause, auch im 3/4-Takt.</p></div>
""",
"aufgaben": [
 ("I", "Zeichne zu jedem Notenwert die passende Pause in ein Notensystem. Beschrifte sie.", 0, N("", schluessel=True, breite=480)),
 ("I", "Erkläre, woran du ganze und halbe Pause unterscheidest.", 3, ""),
 ("II", "Ergänze in jedem Takt die fehlende Pause.", 0, N("C4/4 C4/4 C4/4 _ | C4/2 _ _ | ( C4/8 C4/8 ) C4/4 C4/2 _ |", takt="4/4", rhythmus=True)),
 ("II", "Schreibe die Zählzeiten unter die Noten und Pausen und klatsche den Rhythmus. Bei Pausen öffnest du die Hände.", 0, N("C4/4 R/4 ( C4/8 C4/8 ) R/4 | R/8 C4/8 C4/4 C4/2 | R/2 C4/4 R/4 | C4/1 |.", takt="4/4", rhythmus=True)),
 ("III", "Ein Mitschüler hat im 3/4-Takt eine Pause über einen ganzen Takt als „halbe Pause mit Punkt“ notiert. Beurteile, ob das richtig ist.", 4, ""),
],
"uebungen": [
 {"slug": "k2-pausen", "titel": "Quiz: Pausen erkennen", "kurz": "Pausenwerte benennen und einsetzen", "typ": "notenquiz", "symbol": "pausen",
  "anleitung": "Wähle die richtige Antwort. Du bekommst sofort eine Rückmeldung.",
  "daten": {"fragen": [
   {"frage": "Wie heißt diese Pause?", "noten": "R/4", "spec": {"schluessel": False}, "optionen": ["Viertelpause", "Achtelpause", "halbe Pause", "Sechzehntelpause"], "richtig": 0, "erklaerung": "Das ist die Viertelpause, ein Schlag."},
   {"frage": "Wie heißt diese Pause?", "noten": "R/1", "spec": {"schluessel": False}, "optionen": ["ganze Pause", "halbe Pause", "Viertelpause", "Achtelpause"], "richtig": 0, "erklaerung": "Sie hängt unter der vierten Linie."},
   {"frage": "Wie heißt diese Pause?", "noten": "R/2", "spec": {"schluessel": False}, "optionen": ["halbe Pause", "ganze Pause", "Viertelpause", "Achtelpause"], "richtig": 0, "erklaerung": "Sie liegt auf der Mittellinie."},
   {"frage": "Wie heißt diese Pause?", "noten": "R/16", "spec": {"schluessel": False}, "optionen": ["Sechzehntelpause", "Achtelpause", "Viertelpause", "halbe Pause"], "richtig": 0, "erklaerung": "Zwei Häkchen: Sechzehntelpause."},
   {"frage": "Wie heißt diese Pause?", "noten": "R/8", "spec": {"schluessel": False}, "optionen": ["Achtelpause", "Sechzehntelpause", "Viertelpause", "ganze Pause"], "richtig": 0, "erklaerung": "Ein Häkchen: Achtelpause."},
   {"frage": "Welche Pause fehlt im 4/4-Takt?", "noten": "C4/2 C4/4 ?/4 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "R/4", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/2", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/8", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/1", "spec": {"schluessel": False, "oben": 4, "unten": 1}}], "richtig": 0, "erklaerung": "Es fehlt ein Schlag: Viertelpause."},
   {"frage": "Welche Pause fehlt im 4/4-Takt?", "noten": "C4/4 ?/2 C4/4 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "R/2", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/4", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/1", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/8", "spec": {"schluessel": False, "oben": 4, "unten": 1}}], "richtig": 0, "erklaerung": "1 + 1 = 2, es fehlen zwei Schläge: halbe Pause."},
   {"frage": "Welche Pause fehlt im 2/4-Takt?", "noten": "C4/4 C4/8 ?/8 |", "spec": {"rhythmus": True, "takt": "2/4"}, "optionen": [{"noten": "R/8", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/4", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/16", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/2", "spec": {"schluessel": False, "oben": 4, "unten": 1}}], "richtig": 0, "erklaerung": "Es fehlt eine Achtel."},
   {"frage": "Ein ganzer Takt im 3/4-Takt soll still sein. Was schreibt man?", "optionen": ["eine ganze Pause", "eine halbe Pause mit Punkt", "drei Achtelpausen", "nichts"], "richtig": 0, "erklaerung": "Für einen leeren Takt steht immer die ganze Pause (Ganztaktpause)."},
   {"frage": "Wie viele Achtelpausen sind so lang wie eine halbe Pause?", "optionen": ["4", "2", "8", "3"], "richtig": 0, "erklaerung": "Halbe = 2 Viertel = 4 Achtel."}
  ]}},
 {"slug": "k2-taktstriche", "titel": "Taktstriche setzen mit Pausen", "kurz": "Takte mit Noten und Pausen in 2/4, 3/4 und 4/4 abteilen", "typ": "taktstriche", "symbol": "pausen",
  "anleitung": "Pausen zählen genauso mit wie Noten. Denk daran: Eine ganze Pause füllt immer einen ganzen Takt, auch im 2/4- oder 3/4-Takt. Tippe zwischen zwei Zeichen, um einen Taktstrich zu setzen.",
  "daten": {"aufgaben": [
   takt_aufgabe("2/4", [["C4/4", "R/4"], ["R/1"], ["( C4/8 C4/8 )", "R/4"], ["R/8", "C4/8", "C4/4"]]),
   takt_aufgabe("2/4", [["R/4", "C4/4"], ["C4/8", "R/8", "C4/4"], ["R/1"], ["C4/2"]]),
   takt_aufgabe("3/4", [["C4/4", "R/4", "C4/4"], ["C4/2", "R/4"], ["R/1"], ["C4/4", "C4/4", "C4/4"]]),
   takt_aufgabe("3/4", [["R/4", "C4/2"], ["C4/8", "R/8", "C4/4", "R/4"], ["C4/4", "R/2"], ["C4/2", "R/4"]]),
   takt_aufgabe("4/4", [["C4/4", "R/4", "C4/2"], ["R/2", "C4/4", "C4/4"], ["R/1"], ["C4/2", "R/2"]]),
   takt_aufgabe("4/4", [["C4/8", "R/8", "C4/4", "R/4", "C4/4"], ["C4/2", "R/4", "C4/4"], ["R/16", "C4/16", "C4/8", "C4/4", "R/2"], ["C4/1"]])
  ]}},
 {"slug": "k2-wert-sortieren", "titel": "Sortieren: Wie lang ist das?", "kurz": "Noten und Pausen nach ihrer Dauer ordnen", "typ": "sortieren", "symbol": "sortieren",
  "anleitung": "Wie viele Viertel dauert das? Ordne zu und klicke dann auf „Prüfen“.",
  "daten": {"kategorien": ["½ Viertel", "1 Viertel", "2 Viertel", "4 Viertel"], "eintraege": [
   {"text": "Achtelnote", "kategorie": "½ Viertel"}, {"text": "Achtelpause", "kategorie": "½ Viertel"}, {"text": "zwei Sechzehntel", "kategorie": "½ Viertel"},
   {"text": "Viertelpause", "kategorie": "1 Viertel"}, {"text": "zwei Achtelnoten", "kategorie": "1 Viertel"}, {"text": "vier Sechzehntelpausen", "kategorie": "1 Viertel"},
   {"text": "halbe Note", "kategorie": "2 Viertel"}, {"text": "halbe Pause", "kategorie": "2 Viertel"}, {"text": "Viertelnote und Viertelpause", "kategorie": "2 Viertel"},
   {"text": "ganze Pause im 4/4-Takt", "kategorie": "4 Viertel"}, {"text": "zwei halbe Noten", "kategorie": "4 Viertel"}, {"text": "acht Achtel", "kategorie": "4 Viertel"}
  ]}},
],
}

# ======================================================================
KAPITEL[3] = {
"kurz": "Wie Punkt und Haltebogen eine Note verlängern, typische punktierte Rhythmen und Triolen.",
"inhalt": f"""
<p class="lead">Mit den Grundwerten allein lassen sich viele Rhythmen nicht aufschreiben. Drei Werkzeuge helfen: der Punkt, der Haltebogen und die Triole.</p>

<h2>Punktierte Noten</h2>
<p>Ein <span class="fachwort">Punkt</span> rechts neben dem Notenkopf verlängert die Note <strong>um die Hälfte ihres Wertes</strong>. Das gilt genauso für Pausen.</p>
<div class="tabelle-scroll"><table class="notentabelle">
  <thead><tr><th>punktiert</th><th>entspricht</th><th>Dauer</th></tr></thead>
  <tbody>
    <tr><td>{N("C4/2.", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>halbe + Viertel</td><td>2 + 1 = 3 Schläge</td></tr>
    <tr><td>{N("C4/4.", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>Viertel + Achtel</td><td>1 + ½ = 1½ Schläge</td></tr>
    <tr><td>{N("C4/8.", rhythmus=True, zoom=1.2, klasse="mini", spiel=False)}</td><td>Achtel + Sechzehntel</td><td>½ + ¼ = ¾ Schlag</td></tr>
  </tbody>
</table></div>
<p>Punktierte Noten stehen fast immer zusammen mit einer kurzen Note, die den angebrochenen Schlag auffüllt:</p>
{N("C4/2.@1(2,3) C4/4@4 | C4/4.@1(2) C4/8@+ C4/2@3(4) | ( C4/8.@1(a+) C4/16@a ) ( C4/8.@2(a+) C4/16@a ) C4/2@3(4) |.", "Typische punktierte Rhythmen. Die Zählzeiten in Klammern werden mitgezählt, aber nicht neu angeschlagen.", takt="4/4", rhythmus=True)}
<p>Die Kombination punktierte Achtel und Sechzehntel klingt hüpfend und kommt in vielen Liedern vor, zum Beispiel in Märschen.</p>

<h2>Haltebögen</h2>
<p>Ein <span class="fachwort">Haltebogen</span> verbindet <strong>zwei Noten mit derselben Tonhöhe</strong>. Die zweite Note wird nicht neu angeschlagen, sondern weiter gehalten. Die Dauern der beiden Noten werden <strong>zusammengezählt</strong>.</p>
{N("G4/2@1(2) ~ G4/4@(3) G4/4@4 | G4/4@1 G4/4@2 G4/2@3(4) |.", "Halbe + Viertel durch einen Haltebogen verbunden: Der Ton klingt drei Schläge lang.", takt="4/4", zoom=1.5)}
<p>Haltebögen braucht man vor allem dann, wenn ein Ton <strong>über den Taktstrich hinaus</strong> klingen soll. Ein Notenwert allein darf nämlich nicht über den Taktstrich ragen.</p>
{N("C5/2 C5/4 G4/4 ~ | G4/2 E4/2 |.", "Das g′ beginnt auf Schlag 4 und klingt über den Taktstrich bis zum Ende von Schlag 2 im nächsten Takt.", takt="4/4", zoom=1.5)}
<p>Oft kann man denselben Rhythmus mit einem Punkt oder mit einem Haltebogen aufschreiben. Beides klingt gleich:</p>
{N("C4/2.@3_Schläge || C4/2@2 ~ C4/4@+_1_=_3", "Punktierte Halbe oder Halbe mit Haltebogen an eine Viertel: beides dauert drei Schläge.", rhythmus=True, zoom=1.5)}
{N("C4/4.@1½_Schläge || C4/4@1 ~ C4/8@+_½_=_1½", "Punktierte Viertel oder Viertel mit Haltebogen an eine Achtel", rhythmus=True, zoom=1.5)}
<p>Achtung, nicht verwechseln: Ein <strong>Bindebogen</strong> sieht ähnlich aus, verbindet aber Noten mit <strong>verschiedenen</strong> Tonhöhen. Er bedeutet, dass die Töne gebunden (legato) gespielt werden. Ein Haltebogen verbindet immer nur gleiche Töne.</p>

<h2>Triolen</h2>
<p>Eine <span class="fachwort">Triole</span> sind <strong>drei Noten, die in der Zeit von zwei gleichen Noten</strong> gespielt werden. Sie wird mit einer 3 über oder unter den Noten gekennzeichnet.</p>
{N("( C4/8@1 C4/8@+ ) 3( C4/8@2 C4/8@tri C4/8@o ) C4/4@3 3( C4/8@4 C4/8@tri C4/8@o ) |", "Achteltriole: drei Achtel in der Zeit von zwei Achteln, also in einem Schlag", takt="4/4", rhythmus=True)}
{N("C4/4@1 C4/4@2 C4/4@3 C4/4@4 | 3[ C4/4@1 C4/4 C4/4 ] 3[ C4/4@3 C4/4 C4/4 ] |", "Viertel-Triole: drei Viertel in der Zeit von zwei Vierteln", takt="4/4", rhythmus=True)}
<p>Beim Zählen spricht man für die Achteltriole drei gleich lange Silben auf jeden Schlag: „1-tri-o, 2-tri-o, 3-tri-o …“. Man kann auch ein dreisilbiges Wort wie „Ananas“ auf jeden Schlag sprechen.</p>

<div class="merke"><strong>Merke</strong>
<p>Ein Punkt verlängert eine Note oder Pause um die Hälfte ihres Wertes: Eine punktierte Halbe dauert drei Viertel. Ein Haltebogen verbindet zwei gleiche Töne, ihre Dauern werden addiert; so kann ein Ton auch über den Taktstrich klingen. Eine Triole besteht aus drei Noten, die zusammen so lang sind wie zwei Noten desselben Wertes.</p></div>
""",
"aufgaben": [
 ("I", "Erkläre, was ein Punkt hinter einer Note bewirkt. Gib drei Beispiele mit ihrer Dauer in Vierteln an.", 4, ""),
 ("I", "Erkläre, was ein Haltebogen ist und wie er sich von einem Bindebogen unterscheidet.", 3, ""),
 ("I", "Erkläre, was eine Triole ist.", 3, ""),
 ("II", "Berechne die Dauer in Achteln: punktierte Halbe, punktierte Viertel, Achteltriole, Viertel-Triole.", 3, ""),
 ("II", "Setze die fehlenden Taktstriche und schreibe die Zählzeiten darunter.", 0, N("C4/4. C4/8 C4/2 C4/2. C4/4 3( C4/8 C4/8 C4/8 ) C4/4 C4/2 |.", takt="4/4", rhythmus=True)),
 ("II", "Klatscht den Rhythmus in Zweiergruppen. Eine Person zählt laut die Viertel.", 0, N("C4/4. C4/8 C4/4 C4/4 | ( C4/8. C4/16 ) ( C4/8. C4/16 ) C4/2 | 3( C4/8 C4/8 C4/8 ) 3( C4/8 C4/8 C4/8 ) C4/2 |.", takt="4/4", rhythmus=True)),
 ("III", "Ein Rhythmus aus einer punktierten Viertel und einer Achtel soll ohne Punkt aufgeschrieben werden. Erkläre, wie das mit einem Haltebogen geht, und zeichne es.", 4, ""),
],
"uebungen": [
 {"slug": "k3-punkt-triole", "titel": "Quiz: Punkte und Triolen", "kurz": "Punktierte Noten und Triolen berechnen", "typ": "notenquiz", "symbol": "punktierung",
  "anleitung": "Wähle die richtige Antwort. Du bekommst sofort eine Rückmeldung.",
  "daten": {"fragen": [
   {"frage": "Wie viele Viertel dauert diese Note?", "noten": "C4/2.", "spec": R, "optionen": ["3", "2", "2½", "4"], "richtig": 0, "erklaerung": "Halbe (2) + die Hälfte davon (1) = 3."},
   {"frage": "Wie viele Achtel dauert diese Note?", "noten": "C4/4.", "spec": R, "optionen": ["3", "2", "4", "1½"], "richtig": 0, "erklaerung": "Viertel = 2 Achtel, plus die Hälfte = 3 Achtel."},
   {"frage": "Was ist gleich lang wie eine punktierte Viertel?", "noten": "C4/4.", "spec": R, "optionen": [{"noten": "C4/4 C4/8", "spec": R}, {"noten": "C4/4 C4/4", "spec": R}, {"noten": "C4/8 C4/8", "spec": R}, {"noten": "C4/4 C4/16", "spec": R}], "richtig": 0, "erklaerung": "Viertel + Achtel."},
   {"frage": "Welche Note fehlt im 4/4-Takt?", "noten": "C4/4. ?/8 C4/2 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "C4/8", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/16", "spec": R}, {"noten": "C4/4.", "spec": R}], "richtig": 0, "erklaerung": "1½ + ? + 2 = 4, also ½: eine Achtel."},
   {"frage": "Welche Note fehlt im 3/4-Takt?", "noten": "?/2. |", "spec": {"rhythmus": True, "takt": "3/4"}, "optionen": [{"noten": "C4/2.", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/1", "spec": R}, {"noten": "C4/4.", "spec": R}], "richtig": 0, "erklaerung": "Drei Viertel: punktierte Halbe."},
   {"frage": "Welche Note fehlt?", "noten": "( C4/8. ?/16 ) C4/4 |", "spec": {"rhythmus": True, "takt": "2/4"}, "optionen": [{"noten": "C4/16", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/4", "spec": R}, {"noten": "C4/8.", "spec": R}], "richtig": 0, "erklaerung": "Punktierte Achtel (¾) + Sechzehntel (¼) = 1 Schlag."},
   {"frage": "Eine Achteltriole dauert so lang wie …", "noten": "3( C4/8 C4/8 C4/8 )", "spec": R, "optionen": ["eine Viertel", "drei Achtel", "eine halbe Note", "eine Achtel"], "richtig": 0, "erklaerung": "Drei Achtel in der Zeit von zwei Achteln = eine Viertel."},
   {"frage": "Eine Viertel-Triole dauert so lang wie …", "noten": "3[ C4/4 C4/4 C4/4 ]", "spec": R, "optionen": ["eine halbe Note", "drei Viertel", "eine Viertel", "eine ganze Note"], "richtig": 0, "erklaerung": "Drei Viertel in der Zeit von zwei Vierteln = eine Halbe."},
   {"frage": "Ist dieser Takt vollständig?", "noten": "C4/2. ( C4/8 C4/8 ) |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": ["ja, genau vier Viertel", "nein, zu kurz", "nein, zu lang"], "richtig": 0, "erklaerung": "3 + ½ + ½ = 4."},
   {"frage": "Ist dieser Takt vollständig?", "noten": "C4/4. C4/4. C4/4 |", "spec": {"rhythmus": True, "takt": "3/4"}, "optionen": ["nein, zu lang", "ja, genau drei Viertel", "nein, zu kurz"], "richtig": 0, "erklaerung": "1½ + 1½ + 1 = 4 Viertel – einer zu viel."},
   {"frage": "Ist dieser Takt vollständig?", "noten": "3( C4/8 C4/8 C4/8 ) C4/4 C4/8 |", "spec": {"rhythmus": True, "takt": "3/4"}, "optionen": ["nein, zu kurz", "ja, genau drei Viertel", "nein, zu lang"], "richtig": 0, "erklaerung": "1 + 1 + ½ = 2½ – eine Achtel fehlt."}
  ]}},
 {"slug": "k3-haltebogen", "titel": "Quiz: Haltebögen", "kurz": "Gebundene Noten zusammenzählen", "typ": "notenquiz", "symbol": "punktierung",
  "anleitung": "Zähle die Dauern der gebundenen Noten zusammen. Mit „Anhören“ hörst du, wie lange der Ton klingt.",
  "daten": {"hoeren": True, "fragen": [
   {"frage": "Wie viele Schläge (Viertel) klingt der erste Ton?", "noten": "G4/2 ~ G4/4 C5/4 |", "spec": {"takt": "4/4"}, "optionen": ["3", "2", "4", "1"], "richtig": 0, "erklaerung": "Halbe (2) + Viertel (1) = 3."},
   {"frage": "Wie viele Schläge klingt der gebundene Ton?", "noten": "C5/4 E4/4 E4/2 ~ | E4/2 G4/2 |", "spec": {"takt": "4/4"}, "optionen": ["4", "2", "3", "6"], "richtig": 0, "erklaerung": "Halbe + Halbe = 4 Schläge, über den Taktstrich hinweg."},
   {"frage": "Wie viele Schläge klingt der gebundene Ton?", "noten": "A4/4 ~ A4/8 G4/8 F4/2 |", "spec": {"takt": "4/4"}, "optionen": ["1½", "1", "2", "¾"], "richtig": 0, "erklaerung": "Viertel (1) + Achtel (½) = 1½."},
   {"frage": "Was ist gleich lang wie diese gebundenen Noten?", "noten": "C4/2 ~ C4/4", "spec": R, "optionen": [{"noten": "C4/2.", "spec": R}, {"noten": "C4/1", "spec": R}, {"noten": "C4/4.", "spec": R}, {"noten": "C4/2", "spec": R}], "richtig": 0, "erklaerung": "Halbe + Viertel = punktierte Halbe."},
   {"frage": "Was ist gleich lang wie diese gebundenen Noten?", "noten": "C4/4 ~ C4/8", "spec": R, "optionen": [{"noten": "C4/4.", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/8.", "spec": R}, {"noten": "C4/2.", "spec": R}], "richtig": 0, "erklaerung": "Viertel + Achtel = punktierte Viertel."},
   {"frage": "Welche Noten darf ein Haltebogen verbinden?", "optionen": ["nur Noten mit derselben Tonhöhe", "Noten mit verschiedener Tonhöhe", "nur Noten im selben Takt", "nur Noten mit Punkt"], "richtig": 0, "erklaerung": "Verschiedene Töne verbindet der Bindebogen (legato)."},
   {"frage": "Wird die zweite Note eines Haltebogens neu angeschlagen?", "optionen": ["Nein, der Ton wird weiter gehalten.", "Ja, sie wird leiser angeschlagen.", "Ja, sie wird betont.", "Nur über dem Taktstrich."], "richtig": 0, "erklaerung": "Darum heißt er Haltebogen."},
   {"frage": "Wozu braucht man Haltebögen besonders?", "optionen": ["damit ein Ton über den Taktstrich klingen kann", "damit Töne lauter werden", "damit man drei Noten in zwei spielen kann", "damit ein Ton kürzer wird"], "richtig": 0, "erklaerung": "Ein einzelner Notenwert darf nicht über den Taktstrich ragen."},
   {"frage": "Ein Ton soll im 4/4-Takt auf Schlag 3 beginnen und bis Schlag 2 des nächsten Taktes klingen. Wie schreibt man das?", "optionen": ["Halbe, Haltebogen über den Taktstrich, Halbe", "eine ganze Note auf Schlag 3", "punktierte Halbe auf Schlag 3", "zwei Halbe ohne Bogen"], "richtig": 0, "erklaerung": "2 Schläge im ersten Takt + 2 im zweiten, verbunden durch den Haltebogen."}
  ]}},
 {"slug": "k1-3-training", "titel": "Training: Rhythmus komplett", "kurz": "Notenwerte, Pausen, Punkte und Triolen gemischt", "typ": "notenquiz", "symbol": "quiz", "training": True,
  "anleitung": "Zehn gemischte Fragen zu den Kapiteln 1 bis 3.",
  "daten": {"fragen": [
   {"frage": "Wie viele Sechzehntel passen in eine punktierte Viertel?", "optionen": ["6", "4", "3", "8"], "richtig": 0, "erklaerung": "Viertel = 4, plus Hälfte = 6."},
   {"frage": "Welche Pause ist gleich lang wie diese Note?", "noten": "C4/2", "spec": R, "optionen": [{"noten": "R/2", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/1", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/4", "spec": {"schluessel": False, "oben": 4, "unten": 1}}, {"noten": "R/8", "spec": {"schluessel": False, "oben": 4, "unten": 1}}], "richtig": 0, "erklaerung": "Halbe Note – halbe Pause (liegt auf der Mittellinie)."},
   {"frage": "Welche Taktangabe passt?", "noten": "C4/4. C4/8 C4/4 | C4/2. |", "spec": R, "optionen": ["3/4", "4/4", "2/4", "6/8"], "richtig": 0, "erklaerung": "1½ + ½ + 1 = 3 Viertel."},
   {"frage": "Welche Taktangabe passt?", "noten": "( C4/8 C4/8 C4/8 ) ( C4/8 C4/8 C4/8 ) | C4/4. C4/4. |", "spec": R, "optionen": ["6/8", "3/4", "4/4", "2/4"], "richtig": 0, "erklaerung": "Sechs Achtel in zwei Dreiergruppen: 6/8."},
   {"frage": "Was fehlt im 4/4-Takt?", "noten": "3( C4/8 C4/8 C4/8 ) R/4 C4/4 ?/4 |", "spec": {"rhythmus": True, "takt": "4/4"}, "optionen": [{"noten": "C4/4", "spec": R}, {"noten": "C4/2", "spec": R}, {"noten": "C4/8", "spec": R}, {"noten": "C4/4.", "spec": R}], "richtig": 0, "erklaerung": "Triole (1) + Pause (1) + Viertel (1) = 3, es fehlt eine Viertel."},
   {"frage": "Wie zählt man eine Achteltriole auf Schlag 2?", "optionen": ["2 tri o", "2 +", "2 a + a", "2 3 4"], "richtig": 0, "erklaerung": "Drei gleich lange Silben auf einen Schlag."},
   {"frage": "Welche Rhythmen sind gleich lang?", "optionen": [{"noten": "C4/2. C4/4", "spec": R}, {"noten": "C4/2. C4/2", "spec": R}, {"noten": "C4/4. C4/4", "spec": R}, {"noten": "C4/2 C4/8", "spec": R}], "frage2": "", "richtig": 0, "erklaerung": "3 + 1 = 4 Viertel = eine ganze Note."},
   {"frage": "Welche Pause hängt unter der vierten Linie?", "optionen": ["die ganze Pause", "die halbe Pause", "die Viertelpause", "die Achtelpause"], "richtig": 0, "erklaerung": "Die halbe liegt auf der Mittellinie."},
   {"frage": "Wie viele Schläge dauert eine punktierte halbe Pause?", "optionen": ["3", "2", "1½", "4"], "richtig": 0, "erklaerung": "Der Punkt wirkt bei Pausen genauso."},
   {"frage": "Was verlängert eine Note um die Hälfte ihres Wertes?", "optionen": ["der Punkt", "der Balken", "die Triole", "das Fähnchen"], "richtig": 0, "erklaerung": "Punkt = + die Hälfte."}
  ]}},
],
}
