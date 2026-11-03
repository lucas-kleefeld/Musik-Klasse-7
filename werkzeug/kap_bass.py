"""Kapitel 5: Noten im Bassschlüssel."""
import random
from notensatz import N
import theorie as T

B = {"schluessel": "bass"}
BASS_TOENE = ["G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]
TIEF = ["C2", "D2", "E2", "F2"]


def lese_aufgaben(listen, oktave=False):
    return [{"noten": " ".join(f"{t}/1" for t in toene), "spec": B, "antworten": [T.antwort(t, oktave) for t in toene]} for toene in listen]


random.seed(21)
_l1 = [random.sample(BASS_TOENE, 6) for _ in range(4)]
random.seed(22)
_l2 = [[random.choice(BASS_TOENE + TIEF) for _ in range(6)] for _ in range(4)]

ALLE = TIEF + ["G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]
ALLE = ["C2", "D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]

KAPITEL = {}

KAPITEL[5] = {
"kurz": "Der F-Schlüssel, die Töne vom großen C bis zum c′, große und kleine Oktave, Merksätze und der Vergleich mit dem Violinschlüssel.",
"inhalt": f"""
<p class="lead">Kontrabass, Cello, Tuba, Fagott und die linke Hand am Klavier spielen tiefe Töne. Im Violinschlüssel bräuchte man dafür viele Hilfslinien. Deshalb gibt es für tiefe Töne einen eigenen Schlüssel: den <span class="fachwort">Bassschlüssel</span>.</p>

<h2>Der F-Schlüssel</h2>
<p>Der Bassschlüssel heißt auch <strong>F-Schlüssel</strong>. Er beginnt auf der <strong>vierten Linie</strong> (von unten gezählt), und seine beiden Punkte umschließen diese Linie. Auf ihr liegt das <strong>kleine f</strong>.</p>
{N("F3/1@f |", "Der Bassschlüssel legt fest: Auf der vierten Linie liegt das kleine f.", schluessel="bass", zoom=1.8)}

<h2>Die Töne im Bassschlüssel</h2>
{N(T.ganze(ALLE, [T.name(t, True) for t in ALLE]), "Vom großen C bis zum eingestrichenen c′", schluessel="bass", zoom=1.7)}
<ul>
  <li><strong>große Oktave:</strong> C D E F G A H – mit großen Buchstaben geschrieben</li>
  <li><strong>kleine Oktave:</strong> c d e f g a h – kleine Buchstaben ohne Striche</li>
  <li>Das <strong>c′</strong> (eingestrichen) liegt auf der ersten <strong>Hilfslinie über</strong> dem System.</li>
</ul>

<h2>Merksätze</h2>
<div class="zwei-spalten">
  <div>{N("G2/1@G B2/1@H D3/1@d F3/1@f A3/1@a", "Töne auf den Linien", schluessel="bass", zoom=1.5)}<p class="legende">z. B. „<strong>G</strong>roße <strong>H</strong>unde <strong>D</strong>ürfen <strong>F</strong>ast <strong>A</strong>lles“</p></div>
  <div>{N("A2/1@A C3/1@c E3/1@e G3/1@g", "Töne in den Zwischenräumen", schluessel="bass", zoom=1.5)}<p class="legende">z. B. „<strong>A</strong>lle <strong>C</strong>lowns <strong>E</strong>ssen <strong>G</strong>ern“</p></div>
</div>
<p>Am besten merkt ihr euch eigene Sätze. Wichtig ist nur die Reihenfolge der Buchstaben von unten nach oben.</p>

<h2>Ein Trick: der Vergleich mit dem Violinschlüssel</h2>
<p>Steht eine Note im Bassschlüssel an derselben Stelle wie im Violinschlüssel, heißt sie <strong>zwei Buchstaben weiter</strong> (eine Terz höher im Alphabet c d e f g a h), liegt aber zwei Oktaven tiefer:</p>
<div class="zwei-spalten">
  <div>{N("E4/1@e′ G4/1@g′ B4/1@h′", "Violinschlüssel", zoom=1.5)}</div>
  <div>{N("G2/1@G B2/1@H D3/1@d", "Bassschlüssel: gleiche Stellen, zwei Buchstaben weiter", schluessel="bass", zoom=1.5)}</div>
</div>
<p>Auf der untersten Linie steht im Violinschlüssel e′, im Bassschlüssel G. Auf der Mittellinie steht h′ beziehungsweise d.</p>

<h2>Das c′ als Brücke</h2>
<p>Am Klavier liest man meist zwei Notensysteme gleichzeitig: oben den Violinschlüssel für die rechte Hand, unten den Bassschlüssel für die linke Hand. Diese Verbindung heißt <span class="fachwort">Klaviersystem</span> oder Akkolade. Das <strong>c′</strong> liegt genau dazwischen: im Violinschlüssel auf der ersten Hilfslinie unten, im Bassschlüssel auf der ersten Hilfslinie oben. Es ist dieselbe Taste, das „mittlere c“ am Klavier.</p>
<div class="zwei-spalten">
  <div>{N("C4/1@c′ D4/1@d′ E4/1@e′", "Violinschlüssel", zoom=1.5)}</div>
  <div>{N("A3/1@a B3/1@h C4/1@c′", "Bassschlüssel", schluessel="bass", zoom=1.5)}</div>
</div>
<p>Vorzeichen, Notenwerte, Halsrichtung (ab der Mittellinie nach unten) und alles andere funktionieren im Bassschlüssel genauso wie im Violinschlüssel.</p>
{N("C3/4 E3/4 G3/4 C4/4 | F3/4 A3/4 C4/2 | G2/4 B2/4 D3/4 G3/4 | C3/1 |.", "Eine Bassbegleitung im Bassschlüssel", schluessel="bass", takt="4/4", zoom=1.5)}
<p><a class="knopf leise" href="../werkzeuge/notentrainer.html">Bassschlüssel im Notentrainer üben</a></p>

<div class="merke"><strong>Merke</strong>
<p>Der Bassschlüssel (F-Schlüssel) legt das kleine f auf die vierte Linie. Die Linien heißen von unten G – H – d – f – a, die Zwischenräume A – c – e – g. Töne der großen Oktave schreibt man mit großen Buchstaben, Töne der kleinen Oktave mit kleinen. Das c′ steht im Bassschlüssel auf der ersten Hilfslinie oben.</p></div>
""",
"aufgaben": [
 ("I", "Zeichne fünfmal einen Bassschlüssel. Achte darauf, dass die Punkte die vierte Linie umschließen.", 0, N("", schluessel="bass", breite=520)),
 ("I", "Schreibe die Namen unter die Noten (große Oktave mit großen Buchstaben).", 0, N(" ".join(f"{t}/1" for t in ["F3", "A2", "D3", "G2", "C4", "E3", "B2", "G3", "C3", "A3"]), schluessel="bass", zoom=1.5)),
 ("I", "Notiere im Bassschlüssel als ganze Noten: c, G, e, A, h, d, f, c′.", 0, N("", schluessel="bass", breite=520)),
 ("II", "Schreibe dieselben Töne einmal im Violinschlüssel und einmal im Bassschlüssel: c′, d′, e′. Was fällt dir auf?", 0, N("", breite=300) + N("", schluessel="bass", breite=300)),
 ("II", "Benenne die Töne dieser Bassbegleitung und spiele sie auf einem Instrument oder der virtuellen Klaviatur.", 0, N("C3/4 G2/4 C3/4 G2/4 | F2/4 C3/4 F2/4 C3/4 | G2/4 D3/4 G2/4 D3/4 | C3/1 |.", schluessel="bass", takt="4/4", zoom=1.4)),
 ("III", "Erkläre, warum man für tiefe Instrumente nicht einfach den Violinschlüssel mit Hilfslinien verwendet.", 4, ""),
],
"uebungen": [
 {"slug": "k5-bass-lesen", "titel": "Noten lesen im Bassschlüssel", "kurz": "Notennamen von G bis c′ eintragen", "typ": "notenlesen", "symbol": "bassschluessel",
  "anleitung": "Schreibe unter jede Note ihren Namen ohne Oktavangabe (z. B. „g“ oder „h“). Groß- und Kleinschreibung ist hier egal.",
  "daten": {"aufgaben": lese_aufgaben(_l1)}},
 {"slug": "k5-bass-lesen-oktave", "titel": "Bassschlüssel mit Oktave", "kurz": "Große und kleine Oktave unterscheiden", "typ": "notenlesen", "symbol": "bassschluessel",
  "anleitung": "Achte auf die Oktave: große Oktave mit großem Buchstaben (G, A, H), kleine Oktave mit kleinem Buchstaben (c, d, e), eingestrichen mit Strich (c').",
  "daten": {"oktave": True, "aufgaben": lese_aufgaben(_l2, oktave=True)}},
 {"slug": "k5-bass-notieren", "titel": "Noten im Bassschlüssel notieren", "kurz": "Töne per Klick in den Bassschlüssel setzen", "typ": "notieren", "symbol": "notieren",
  "anleitung": "Klicke im Notensystem auf die richtige Linie oder den richtigen Zwischenraum.",
  "daten": {"schluessel": "bass", "aufgaben": [{"frage": f"Notiere {T.name(t, True)}", "ziel": [t]} for t in ["F3", "C3", "G2", "A3", "D3", "B2", "E3", "C4"]]}},
 {"slug": "k5-bass-quiz", "titel": "Quiz: Violin- oder Bassschlüssel?", "kurz": "Töne in beiden Schlüsseln vergleichen", "typ": "notenquiz", "symbol": "quiz",
  "anleitung": "Achte genau auf den Schlüssel. Mit „Anhören“ kannst du dir die Noten vorspielen lassen.",
  "daten": {"hoeren": True, "fragen": [
   {"frage": "Wie heißt der Ton?", "noten": "F3/1", "spec": B, "optionen": ["f", "a", "d", "f′"], "richtig": 0, "erklaerung": "Vierte Linie im Bassschlüssel: kleines f."},
   {"frage": "Wie heißt der Ton?", "noten": "G2/1", "spec": B, "optionen": ["G", "e′", "g", "H"], "richtig": 0, "erklaerung": "Unterste Linie im Bassschlüssel: großes G."},
   {"frage": "Wie heißt der Ton?", "noten": "C4/1", "spec": B, "optionen": ["c′", "a", "e″", "c"], "richtig": 0, "erklaerung": "Erste Hilfslinie oben: c′."},
   {"frage": "Wie heißt der Ton?", "noten": "D3/1", "spec": B, "optionen": ["d", "h′", "f", "D"], "richtig": 0, "erklaerung": "Mittellinie im Bassschlüssel."},
   {"frage": "Wie heißt der Ton?", "noten": "A2/1", "spec": B, "optionen": ["A", "a", "F", "c"], "richtig": 0, "erklaerung": "Erster Zwischenraum: großes A."},
   {"frage": "Wie heißt der Ton?", "noten": "Bb2/1", "spec": B, "optionen": ["B", "H", "As", "Bes"], "richtig": 0, "erklaerung": "Zweite Linie ist H, mit b wird daraus B."},
   {"frage": "Wie heißt der Ton?", "noten": "F#3/1", "spec": B, "optionen": ["fis", "f", "gis", "ais"], "richtig": 0, "erklaerung": "Vierte Linie mit Kreuz."},
   {"frage": "Welche Note ist dasselbe c′ wie im Violinschlüssel?", "noten": "C4/1", "optionen": [{"noten": "C4/1", "spec": B}, {"noten": "C3/1", "spec": B}, {"noten": "E3/1", "spec": B}, {"noten": "A3/1", "spec": B}], "richtig": 0, "erklaerung": "Im Bassschlüssel steht c′ auf der ersten Hilfslinie oben."},
   {"frage": "Auf welcher Linie beginnt der Bassschlüssel?", "optionen": ["auf der vierten Linie", "auf der zweiten Linie", "auf der Mittellinie", "auf der ersten Hilfslinie"], "richtig": 0, "erklaerung": "Darum heißt er F-Schlüssel: Auf dieser Linie liegt das f."},
   {"frage": "Wie heißen die Töne auf den Linien im Bassschlüssel (von unten)?", "optionen": ["G – H – d – f – a", "E – G – H – d – f", "F – A – c – e – g", "A – c – e – g – h"], "richtig": 0, "erklaerung": "Merksatz z. B. „Große Hunde Dürfen Fast Alles“."},
   {"frage": "Eine Note steht im Bassschlüssel dort, wo im Violinschlüssel ein e′ stünde. Wie heißt sie?", "optionen": ["G", "E", "c", "e"], "richtig": 0, "erklaerung": "Zwei Buchstaben weiter, zwei Oktaven tiefer."},
   {"frage": "Welche Instrumente lesen meist im Bassschlüssel?", "optionen": ["Kontrabass, Cello, Tuba", "Querflöte, Geige, Trompete", "Blockflöte und Klarinette", "nur Schlagzeug"], "richtig": 0, "erklaerung": "Tiefe Instrumente und die linke Hand am Klavier."}
  ]}},
],
}
