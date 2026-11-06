"""Kapitel 4, 6 und 7: Noten im Violinschlüssel, Vorzeichen, Dynamik."""
import random
from notensatz import N
from zeichnungen import svg, text, g, notenlinien
import theorie as T

STAMMTOENE = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5"]


def klaviatur_bild(von=0, n=15, namen="stamm", markiert=(), titel="Klaviatur", beschreibung=""):
    """Klaviatur ab c; namen: 'stamm', 'kreuz', 'be', 'beide'"""
    w, h, x0, y0 = 40, 150, 10, 30
    weiss = ["c", "d", "e", "f", "g", "a", "h"]
    i = ""
    for k in range(n):
        nm = weiss[(von + k) % 7]
        f = "f-gelb" if k in markiert else "f-weiss"
        i += f'<rect class="s2 {f}" x="{x0 + k * w}" y="{y0}" width="{w}" height="{h}" rx="4"/>' + text(x0 + k * w + w / 2, y0 + h - 14, nm, "hk")
    for k in range(n - 1):
        if (von + k) % 7 in (2, 6):
            continue
        x = x0 + (k + 1) * w - 13
        i += f'<rect class="d" x="{x}" y="{y0}" width="26" height="{h * 0.6}" rx="3"/>'
        stamm = weiss[(von + k) % 7]
        oben = T.name({"c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "a": "A", "h": "B"}[stamm] + "#4")
        unten_st = weiss[(von + k + 1) % 7]
        unten = T.name({"c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "a": "A", "h": "B"}[unten_st] + "b4")
        if namen in ("kreuz", "beide"):
            i += text(x + 13, y0 - 8, oben, "hk k-rosa-t")
        if namen in ("be", "beide"):
            i += text(x + 13, y0 - 8 - (22 if namen == "beide" else 0), unten, "hk k-blau-t")
    return svg(f"0 {-20 if namen == 'beide' else 0} {x0 * 2 + n * w} {h + 50 + (20 if namen == 'beide' else 0)}", i, titel, beschreibung)


def lese_aufgaben(toene_listen, oktave=False, spec=None, wert="1"):
    out = []
    for toene in toene_listen:
        out.append({"noten": " ".join(f"{t}/{wert}" for t in toene), "spec": spec or {}, "antworten": [T.antwort(t, oktave) for t in toene]})
    return out


random.seed(10)
_lesen1 = [random.sample(STAMMTOENE, 6) for _ in range(4)]
random.seed(11)
_lesen2 = [[random.choice(STAMMTOENE) for _ in range(6)] for _ in range(4)]

KAPITEL = {}

# ======================================================================
KAPITEL[4] = {
"kurz": "Notensystem, Violinschlüssel, die Stammtöne von c′ bis a″, Oktavbereiche, Hilfslinien und Halsrichtung.",
"inhalt": f"""
<p class="lead">Je höher eine Note im Notensystem steht, desto höher klingt sie. Mit dem Violinschlüssel weiß man genau, welcher Ton gemeint ist.</p>

<h2>Notensystem und Violinschlüssel</h2>
<p>Noten werden in ein <span class="fachwort">Notensystem</span> aus <strong>fünf Linien</strong> und <strong>vier Zwischenräumen</strong> geschrieben. Linien und Zwischenräume werden <strong>von unten nach oben</strong> gezählt. Noten können auf einer Linie liegen (die Linie geht durch den Notenkopf) oder in einem Zwischenraum.</p>
<p>Der <span class="fachwort">Violinschlüssel</span> heißt auch <strong>G-Schlüssel</strong>: Er beginnt auf der zweiten Linie und umkreist sie. Auf dieser Linie liegt das g′.</p>
{N("G4/4@g′ |", "Der Violinschlüssel legt fest: Auf der zweiten Linie liegt g′.", zoom=1.8)}

<h2>Die Stammtöne</h2>
<p>Die sieben <span class="fachwort">Stammtöne</span> heißen <strong>c – d – e – f – g – a – h</strong>. Danach beginnt die Reihe wieder von vorn, nur eine <strong>Oktave</strong> höher. Achtung: Im Deutschen heißt der siebte Ton <strong>h</strong>, nicht b. Das b ist ein anderer Ton (siehe Kapitel 6).</p>
{N(T.ganze(STAMMTOENE, [T.name(t, True) for t in STAMMTOENE]).replace("/1", "/4"), "Die Stammtöne vom eingestrichenen c bis zum zweigestrichenen a", zoom=1.7)}
<p>Damit man weiß, in welcher Oktave ein Ton liegt, bekommt sein Name Striche:</p>
<ul>
  <li><strong>eingestrichene Oktave:</strong> c′ d′ e′ f′ g′ a′ h′ (gesprochen „c eins“ oder „eingestrichenes c“)</li>
  <li><strong>zweigestrichene Oktave:</strong> c″ d″ e″ f″ g″ a″ h″</li>
  <li>Darunter liegt die <strong>kleine Oktave</strong> ohne Striche (c d e …).</li>
</ul>

<h2>Hilfslinien</h2>
<p>Für Töne über oder unter dem Notensystem zeichnet man kurze <span class="fachwort">Hilfslinien</span>. Das c′ liegt auf der ersten Hilfslinie unter dem System, das a″ auf der ersten Hilfslinie darüber.</p>
{N("C4/4@c′ D4/4@d′ _ G5/4@g″ A5/4@a″", "Hilfslinien unter und über dem Notensystem", zoom=1.7)}

<h2>Merksätze</h2>
<div class="zwei-spalten">
  <div>{N("E4/4@e′ G4/4@g′ B4/4@h′ D5/4@d″ F5/4@f″", "Töne auf den Linien", zoom=1.5)}<p class="legende">„<strong>E</strong>s <strong>G</strong>eht <strong>H</strong>urtig <strong>D</strong>urch <strong>F</strong>leiß“</p></div>
  <div>{N("F4/4@f′ A4/4@a′ C5/4@c″ E5/4@e″", "Töne in den Zwischenräumen", zoom=1.5)}<p class="legende">Von unten gelesen ergibt sich das Wort <strong>FACE</strong>.</p></div>
</div>

<h2>Wohin zeigt der Notenhals?</h2>
<p>Noten <strong>unterhalb der Mittellinie</strong> bekommen den Hals <strong>rechts nach oben</strong>. Noten <strong>ab der Mittellinie</strong> (h′) bekommen ihn <strong>links nach unten</strong>. So bleibt der Hals im Notensystem.</p>
{N("C4/4 E4/4 G4/4 A4/4 | B4/4 C5/4 E5/4 A5/4 |", "Halsrichtung: bis a′ nach oben, ab h′ nach unten", zoom=1.6)}

<h2>Noten auf der Klaviatur</h2>
<p>Auf der Klaviatur wiederholen sich Gruppen aus zwei und drei schwarzen Tasten. Das <strong>c</strong> liegt immer <strong>links neben den zwei schwarzen Tasten</strong>. Von dort gehen die weißen Tasten der Reihe nach: c, d, e, f, g, a, h, c.</p>
<figure class="breit klavier"><div class="bild">{klaviatur_bild(0, 15, "stamm", (0, 7, 14), "Klaviatur mit den Namen der weißen Tasten", "Zwei Oktaven weiße Tasten von c bis c mit Namen; die c-Tasten sind markiert.")}</div><figcaption>Die weißen Tasten sind die Stammtöne. Das c liegt links neben den zwei schwarzen Tasten.</figcaption></figure>
<p><a class="knopf leise" href="../werkzeuge/klaviatur.html">Klaviatur ausprobieren</a> <a class="knopf leise" href="../werkzeuge/notentrainer.html">Noten lesen trainieren</a></p>

<div class="merke"><strong>Merke</strong>
<p>Das Notensystem hat fünf Linien, gezählt wird von unten. Der Violinschlüssel legt das g′ auf die zweite Linie. Die Stammtöne heißen c d e f g a h. c′ und a″ stehen auf Hilfslinien. Ab der Mittellinie (h′) zeigt der Notenhals nach unten.</p></div>
""",
"aufgaben": [
 ("I", "Schreibe die Namen unter die Noten (mit Oktavstrichen).", 0, N(" ".join(f"{t}/1" for t in ["G4", "C5", "E4", "A5", "D4", "F5", "B4", "C4", "G5", "A4"]), zoom=1.5)),
 ("I", "Notiere die Töne als ganze Noten: f′, a′, c″, e″, d′, g″, h′, c′.", 0, N("", breite=520)),
 ("II", "Setze die Hälse richtig an (Viertelnoten) und begründe die Richtung bei h′.", 0, N("D4/1 F4/1 A4/1 B4/1 D5/1 G5/1", zoom=1.5)),
 ("II", "Löse das Notenrätsel: Schreibe unter jede Note ihren Namen. Welche Wörter entstehen?", 0,
  N("C5/1 A4/1 F4/1 E4/1 | E4/1 B4/1 E4/1 | A4/1 F4/1 F4/1 E4/1 |", zoom=1.5)),
 ("II", "Erfinde selbst drei Notenrätsel-Wörter (nur mit den Buchstaben c d e f g a h) und notiere sie. Tausche mit deinem Nachbarn.", 0, N("", breite=520)),
 ("III", "In einer englischen Notenausgabe steht „B“, wo im Deutschen „h“ steht. Erkläre, warum es hier leicht zu Missverständnissen kommen kann.", 4, ""),
],
"uebungen": [
 {"slug": "k4-noten-lesen", "titel": "Noten lesen: Stammtöne", "kurz": "Notennamen von c′ bis a″ eintragen", "typ": "notenlesen", "symbol": "lesen",
  "anleitung": "Schreibe unter jede Note ihren Namen (ohne Oktavstriche, z. B. „g“). Prüfen kannst du, wenn alle Felder ausgefüllt sind.",
  "daten": {"aufgaben": lese_aufgaben(_lesen1, wert="4")}},
 {"slug": "k4-noten-lesen-oktave", "titel": "Noten lesen mit Oktave", "kurz": "Namen mit Oktavstrichen, z. B. g′ oder c″", "typ": "notenlesen", "symbol": "lesen",
  "anleitung": "Schreibe die Namen mit Oktavstrichen: g' oder g1 für das eingestrichene g, c'' oder c2 für das zweigestrichene c.",
  "daten": {"oktave": True, "aufgaben": lese_aufgaben(_lesen2, oktave=True, wert="4")}},
 {"slug": "k4-noten-notieren", "titel": "Noten notieren", "kurz": "Töne per Klick ins Notensystem setzen", "typ": "notieren", "symbol": "notieren",
  "anleitung": "Klicke im Notensystem auf die richtige Linie oder den richtigen Zwischenraum. Mit „Zurück“ nimmst du eine Note wieder weg.",
  "daten": {"aufgaben": [{"frage": f"Notiere {T.name(t, True)}", "ziel": [t]} for t in ["G4", "C5", "E4", "A5", "D4", "F5", "B4", "C4"]]}},
 {"slug": "k4-woerter", "titel": "Notenrätsel", "kurz": "Wörter aus Notennamen lesen", "typ": "notenlesen", "symbol": "lesen",
  "anleitung": "Jede Zeile ergibt ein Wort. Schreibe unter jede Note ihren Namen.",
  "daten": {"aufgaben": lese_aufgaben([["C5", "A4", "F4", "E4"], ["B4", "E4", "F4", "E5"], ["E4", "G4", "G4", "E4"], ["D5", "A4", "C5", "B4"], ["F4", "A4", "C5", "B4"]], wert="4")}},
],
}

# ======================================================================
KAPITEL[6] = {
"kurz": "Kreuz, b und Auflösungszeichen, die Namen der erhöhten und erniedrigten Töne, Gültigkeit und enharmonische Verwechslung.",
"inhalt": f"""
<p class="lead">Zwischen den meisten weißen Tasten liegen schwarze. Für diese Töne braucht man <span class="fachwort">Vorzeichen</span>.</p>

<h2>Drei Vorzeichen</h2>
<div class="tabelle-scroll"><table class="notentabelle">
  <thead><tr><th>Zeichen</th><th>Name</th><th>Wirkung</th><th>Silbe</th></tr></thead>
  <tbody>
    <tr><td>{N("F#4/1", zoom=1.2, klasse="mini", spiel=False, schluessel=False, oben=3, unten=2)}</td><td>Kreuz (♯)</td><td>erhöht um einen Halbton</td><td>+ is: f → fis</td></tr>
    <tr><td>{N("Eb4/1", zoom=1.2, klasse="mini", spiel=False, schluessel=False, oben=3, unten=2)}</td><td>b (♭)</td><td>erniedrigt um einen Halbton</td><td>+ es: e → es</td></tr>
    <tr><td>{N("Bn4/1", zoom=1.2, klasse="mini", spiel=False, schluessel=False, oben=3, unten=2)}</td><td>Auflösungszeichen (♮)</td><td>hebt ein Vorzeichen auf</td><td>wieder Stammton</td></tr>
  </tbody>
</table></div>
<p>Ein <span class="fachwort">Halbton</span> ist der kleinste Tonabstand auf der Klaviatur: von einer Taste zur direkt benachbarten, egal ob weiß oder schwarz.</p>

<h2>Die Namen</h2>
{N("C#4/1@cis D#4/1@dis E#4/1@eis F#4/1@fis G#4/1@gis A#4/1@ais B#4/1@his", "Mit Kreuz: Die Silbe „is“ wird angehängt.", zoom=1.5)}
{N("Cb5/1@ces Db4/1@des Eb4/1@es Fb4/1@fes Gb4/1@ges Ab4/1@as Bb4/1@b", "Mit b: Die Silbe „es“ wird angehängt.", zoom=1.5)}
<p>Bei den b-Tönen gibt es drei Ausnahmen: Aus e wird <strong>es</strong>, aus a wird <strong>as</strong> (nicht „ees“, „aes“) und aus h wird <strong>b</strong>.</p>
<figure class="breit klavier"><div class="bild">{klaviatur_bild(0, 8, "beide", (), "Klaviatur mit den Namen der schwarzen Tasten", "Eine Oktave Klaviatur. Über jeder schwarzen Taste stehen zwei Namen, zum Beispiel cis und des.")}</div><figcaption>Jede schwarze Taste hat zwei Namen: unten mit Kreuz, darüber mit b.</figcaption></figure>

<h2>Wie lange gilt ein Vorzeichen?</h2>
<ul>
  <li>Ein Vorzeichen direkt vor einer Note heißt <span class="fachwort">Versetzungszeichen</span>. Es gilt <strong>bis zum Ende des Taktes</strong> und nur für diese eine Tonhöhe.</li>
  <li>Im nächsten Takt gilt wieder der Stammton, außer die Note wird über den Taktstrich gehalten.</li>
  <li>Ein Auflösungszeichen hebt das Vorzeichen schon früher auf.</li>
</ul>
{N("F#4/4@fis F4/4@fis F4/4@fis Fn4/4@f | F4/2@f F#4/2@fis |", "Das Kreuz gilt bis zum Taktstrich oder bis zum Auflösungszeichen.", takt="4/4", zoom=1.6)}
<p>Stehen Vorzeichen gleich hinter dem Schlüssel, heißen sie <span class="fachwort">Generalvorzeichen</span>. Sie gelten für das ganze Stück und in allen Oktaven. An ihnen erkennt man die Tonart eines Stückes. Mehr dazu lernst du später bei den Tonleitern.</p>
{N("F4/4@fis G4/4@g A4/4@a F5/4@fis″ |", "Das Generalvorzeichen fis gilt für jedes f, auch für f″.", tonart=1, takt="4/4", zoom=1.6)}

<h2>Ein Ton, zwei Namen</h2>
<p>cis und des klingen gleich, es ist dieselbe Taste. Man nennt das <span class="fachwort">enharmonische Verwechslung</span>. Auch weiße Tasten können so einen zweiten Namen haben: eis klingt wie f, his wie c, fes wie e, ces wie h. Welcher Name richtig ist, hängt von der Tonart ab.</p>
{N("C#4/1@cis Db4/1@des _ F#4/1@fis Gb4/1@ges _ E#4/1@eis F4/1@f", "Enharmonisch gleiche Töne", zoom=1.5)}

<div class="merke"><strong>Merke</strong>
<p>Das Kreuz erhöht um einen Halbton (+ is), das b erniedrigt um einen Halbton (+ es; Ausnahmen es, as, b). Das Auflösungszeichen hebt ein Vorzeichen auf. Versetzungszeichen gelten bis zum Taktende, Generalvorzeichen für das ganze Stück. Zwei Namen für denselben Ton nennt man enharmonische Verwechslung.</p></div>
""",
"aufgaben": [
 ("I", "Schreibe die Namen unter die Noten.", 0, N("F#4/1 Bb4/1 C#5/1 Eb4/1 G#4/1 Ab4/1 D#5/1 Db5/1", zoom=1.5)),
 ("I", "Notiere die Töne: gis′, es′, b′, cis″, as′, fis″, des″.", 0, N("", breite=520)),
 ("II", "Gib zu jedem Ton den enharmonisch gleichen Ton an: fis, as, cis, b, dis, ges.", 3, ""),
 ("II", "Benenne alle Töne im Takt. Achte darauf, wie lange die Vorzeichen gelten.", 0, N("C#5/4 C5/4 D5/4 Cn5/4 | Bb4/4 B4/4 A4/4 B4/4 |", takt="4/4", zoom=1.5)),
 ("II", "Erkläre den Unterschied zwischen einem Versetzungszeichen und einem Generalvorzeichen.", 4, ""),
 ("III", "Sophie sagt: „Das b ist einfach das englische h.“ Nimm Stellung.", 4, ""),
],
"uebungen": [
 {"slug": "k5-lesen", "titel": "Noten lesen mit Vorzeichen", "kurz": "cis, es, b und Co. benennen", "typ": "notenlesen", "symbol": "vorzeichen",
  "anleitung": "Schreibe unter jede Note ihren Namen, z. B. „fis“ oder „es“. Ohne Oktavstriche.",
  "daten": {"aufgaben": lese_aufgaben([["F#4", "C#5", "G#4", "D#5", "A#4", "C#4"], ["Bb4", "Eb4", "Ab4", "Db5", "Gb4", "Eb5"], ["F#5", "Bb4", "C#5", "Ab4", "D5", "G#4"]])}},
 {"slug": "k5-notieren", "titel": "Noten mit Vorzeichen notieren", "kurz": "Töne mit Kreuz und b setzen", "typ": "notieren", "symbol": "notieren",
  "anleitung": "Wähle zuerst das Vorzeichen und klicke dann auf die richtige Stelle im Notensystem.",
  "daten": {"vorzeichen": True, "aufgaben": [{"frage": f"Notiere {T.name(t, True)}", "ziel": [t]} for t in ["F#4", "Bb4", "C#5", "Eb4", "G#4", "Ab4", "D#5", "Db5"]]}},
 {"slug": "k5-quiz", "titel": "Quiz: Vorzeichen", "kurz": "Wirkung, Gültigkeit und enharmonische Verwechslung", "typ": "notenquiz", "symbol": "quiz",
  "anleitung": "Wähle die richtige Antwort.",
  "daten": {"fragen": [
   {"frage": "Wie heißt der Ton?", "noten": "Ab4/1", "optionen": ["as′", "aes′", "ais′", "a′"], "richtig": 0, "erklaerung": "Ausnahme: a + es = as."},
   {"frage": "Wie heißt der Ton?", "noten": "Bb4/1", "optionen": ["b′", "hes′", "his′", "h′"], "richtig": 0, "erklaerung": "h mit b heißt b."},
   {"frage": "Wie heißt der Ton?", "noten": "D#5/1", "optionen": ["dis″", "des″", "dis′", "es″"], "richtig": 0, "erklaerung": "d + is, zweigestrichen."},
   {"frage": "Wie heißt der dritte Ton?", "noten": "F#4/4 G4/4 F4/4 A4/4 |", "spec": {"takt": "4/4"}, "optionen": ["fis′", "f′", "ges′", "fes′"], "richtig": 0, "erklaerung": "Das Kreuz gilt bis zum Taktende."},
   {"frage": "Wie heißt der vierte Ton?", "noten": "C#5/4 D5/4 Cn5/4 C5/4 |", "spec": {"takt": "4/4"}, "optionen": ["c″", "cis″", "ces″", "h′"], "richtig": 0, "erklaerung": "Das Auflösungszeichen gilt ebenfalls bis zum Taktende."},
   {"frage": "Welcher Ton klingt gleich wie fis?", "optionen": ["ges", "fes", "gis", "es"], "richtig": 0, "erklaerung": "Enharmonische Verwechslung: fis = ges."},
   {"frage": "Welcher Ton klingt gleich wie eis?", "optionen": ["f", "e", "es", "fis"], "richtig": 0, "erklaerung": "Zwischen e und f gibt es keine schwarze Taste."},
   {"frage": "Wie lange gilt ein Versetzungszeichen?", "optionen": ["bis zum Ende des Taktes", "für das ganze Stück", "nur für eine Note", "bis zur nächsten Pause"], "richtig": 0, "erklaerung": "Generalvorzeichen gelten für das ganze Stück."},
   {"frage": "Was bewirkt ein b?", "optionen": ["Es erniedrigt um einen Halbton.", "Es erhöht um einen Halbton.", "Es erniedrigt um einen Ganzton.", "Es hebt ein Kreuz auf."], "richtig": 0, "erklaerung": "Ein Kreuz würde erhöhen."},
   {"frage": "Wie heißt der Ton? (Generalvorzeichen beachten)", "noten": "F5/1", "spec": {"tonart": 1}, "optionen": ["fis″", "f″", "fis′", "ges″"], "richtig": 0, "erklaerung": "Das Generalvorzeichen fis gilt in allen Oktaven."}
  ]}},
],
}

# ======================================================================
KAPITEL[7] = {
"kurz": "Lautstärkezeichen von pianissimo bis fortissimo, crescendo und decrescendo, Akzente.",
"inhalt": f"""
<p class="lead">Dieselbe Melodie kann zart und leise oder kraftvoll und laut klingen. Wie laut gespielt wird, zeigen die <span class="fachwort">Dynamikzeichen</span>. <em>Dynamik</em> bedeutet die Lautstärke und ihre Veränderung.</p>

<h2>Lautstärkestufen</h2>
<p>Die Bezeichnungen stammen aus dem Italienischen. Sie stehen unter den Noten und gelten so lange, bis ein neues Zeichen kommt.</p>
<div class="tabelle-scroll"><table class="dynamik-tabelle">
  <thead><tr><th>Zeichen</th><th>italienisch</th><th>Bedeutung</th></tr></thead>
  <tbody>
    <tr><td class="dyn">ppp</td><td>pianissimo possibile</td><td>so leise wie möglich</td></tr>
    <tr><td class="dyn">pp</td><td>pianissimo</td><td>sehr leise</td></tr>
    <tr><td class="dyn">p</td><td>piano</td><td>leise</td></tr>
    <tr><td class="dyn">mp</td><td>mezzopiano</td><td>mittelleise (halbleise)</td></tr>
    <tr><td class="dyn">mf</td><td>mezzoforte</td><td>mittellaut (halblaut)</td></tr>
    <tr><td class="dyn">f</td><td>forte</td><td>laut</td></tr>
    <tr><td class="dyn">ff</td><td>fortissimo</td><td>sehr laut</td></tr>
    <tr><td class="dyn">fff</td><td>fortissimo possibile</td><td>so laut wie möglich</td></tr>
  </tbody>
</table></div>
<p>Merkhilfe: <em>piano</em> heißt leise, <em>forte</em> heißt laut, <em>mezzo</em> heißt halb oder mittel, die Endung <em>-issimo</em> heißt sehr.</p>

<h2>Lautstärke verändern</h2>
<ul>
  <li><span class="fachwort">crescendo</span> (cresc.): allmählich lauter werden. Zeichen: eine sich öffnende Gabel.</li>
  <li><span class="fachwort">decrescendo</span> (decresc.) oder <span class="fachwort">diminuendo</span> (dim.): allmählich leiser werden. Zeichen: eine sich schließende Gabel.</li>
</ul>
{N("!p C4/4 <( D4/4 E4/4 F4/4 | G4/4 A4/4 B4/4 <) !f C5/4 | C5/4 >( B4/4 A4/4 G4/4 | F4/4 E4/4 D4/4 >) !p C4/4 |.", "Leise beginnen, lauter werden bis forte, dann wieder leiser bis piano", takt="4/4", zoom=1.5)}

<h2>Einzelne Töne betonen</h2>
<ul>
  <li><span class="fachwort">sforzato</span> (sfz): ein einzelner Ton plötzlich stark betont</li>
  <li><span class="fachwort">fortepiano</span> (fp): laut anspielen und sofort leise weiter</li>
  <li><strong>Akzent</strong> (&gt; über oder unter der Note): diesen Ton hervorheben</li>
</ul>
{N("!mf C5/4 C5/4 !sfz C5/2 | !fp G4/1 |", "sforzato und fortepiano", takt="4/4", zoom=1.5)}

<h2>Wozu Dynamik?</h2>
<p>Dynamik macht Musik lebendig. Sie kann Spannung aufbauen (crescendo), Ruhe ausdrücken (piano) oder einen Höhepunkt markieren (fortissimo). Wie laut forte genau ist, legt das Zeichen nicht fest: Es kommt auf das Instrument, den Raum und das ganze Stück an. Dynamik ist also immer <strong>relativ</strong>.</p>

<div class="merke"><strong>Merke</strong>
<p>Die Dynamikzeichen reichen von ppp (so leise wie möglich) über p, mp, mf, f bis fff (so laut wie möglich). Crescendo bedeutet lauter werden, decrescendo oder diminuendo leiser werden. sfz und Akzente betonen einzelne Töne.</p></div>
""",
"aufgaben": [
 ("I", "Ordne die Zeichen von leise nach laut: f, pp, mf, p, ff, mp.", 2, ""),
 ("I", "Erkläre die Begriffe crescendo, decrescendo und sforzato.", 4, ""),
 ("II", "Beschreibe, wie sich die Lautstärke in diesem Ausschnitt verändert.", 4, N("!pp C4/4 <( E4/4 G4/4 C5/4 | E5/2 <) !ff G5/2 | !sfz C5/2 !p C5/2 |.", takt="4/4", zoom=1.4)),
 ("II", "Lies einen kurzen Text (z. B. ein Gedicht) mit verschiedener Dynamik vor. Notiere vorher über den Zeilen, wo du piano, forte, crescendo und decrescendo einsetzt.", 0, ""),
 ("III", "Hört euch ein Musikstück eurer Wahl an und zeichnet den Lautstärkeverlauf als Kurve. Beschriftet die Kurve mit passenden Dynamikzeichen und erklärt, welche Wirkung die Dynamik hat.", 0, ""),
],
"uebungen": [
 {"slug": "k6-zuordnen", "titel": "Zuordnen: Dynamikzeichen", "kurz": "Zeichen, Begriff und Bedeutung", "typ": "zuordnen", "symbol": "dynamik",
  "anleitung": "Wähle zu jedem Zeichen die passende Bedeutung.",
  "daten": {"paare": [
   {"links": "pp", "rechts": "pianissimo – sehr leise"}, {"links": "p", "rechts": "piano – leise"}, {"links": "mp", "rechts": "mezzopiano – mittelleise"},
   {"links": "mf", "rechts": "mezzoforte – mittellaut"}, {"links": "f", "rechts": "forte – laut"}, {"links": "ff", "rechts": "fortissimo – sehr laut"},
   {"links": "cresc.", "rechts": "allmählich lauter werden"}, {"links": "dim.", "rechts": "allmählich leiser werden"}, {"links": "sfz", "rechts": "einzelner Ton plötzlich stark betont"}
  ]}},
 {"slug": "k6-reihenfolge", "titel": "Reihenfolge: Von ganz leise bis ganz laut", "kurz": "Dynamikstufen ordnen", "typ": "reihenfolge", "symbol": "sortieren",
  "anleitung": "Bringe die Lautstärkestufen in die richtige Reihenfolge, von leise nach laut.",
  "daten": {"schritte": ["ppp – pianissimo possibile", "pp – pianissimo", "p – piano", "mp – mezzopiano", "mf – mezzoforte", "f – forte", "ff – fortissimo", "fff – fortissimo possibile"]}},
 {"slug": "k6-quiz", "titel": "Quiz: Dynamik im Notenbild", "kurz": "Dynamikzeichen in Noten erkennen", "typ": "notenquiz", "symbol": "quiz",
  "anleitung": "Sieh dir den Notenausschnitt an und wähle die richtige Antwort.",
  "daten": {"fragen": [
   {"frage": "Wie soll der Ausschnitt gespielt werden?", "noten": "!p C4/4 <( D4/4 E4/4 F4/4 <) | !f G4/1 |", "spec": {"takt": "4/4"}, "optionen": ["leise beginnen und lauter werden", "laut beginnen und leiser werden", "die ganze Zeit leise", "die ganze Zeit laut"], "richtig": 0, "erklaerung": "p, dann crescendo bis f."},
   {"frage": "Was bedeutet das Zeichen unter der dritten Note?", "noten": "!mf C5/4 B4/4 !sfz A4/4 G4/4 |", "spec": {"takt": "4/4"}, "optionen": ["plötzlich stark betonen", "sehr leise", "langsamer werden", "lauter werden"], "richtig": 0, "erklaerung": "sfz = sforzato."},
   {"frage": "Welche Gabel bedeutet „leiser werden“?", "optionen": [{"noten": "!f C5/4 >( B4/4 A4/4 G4/4 >) !p F4/4", "spec": {}}, {"noten": "!p C4/4 <( D4/4 E4/4 F4/4 <) !f G4/4", "spec": {}}], "richtig": 0, "erklaerung": "Die Gabel schließt sich: decrescendo."},
   {"frage": "Was ist lauter?", "optionen": ["mf", "mp", "p", "pp"], "richtig": 0, "erklaerung": "mezzoforte ist halblaut, alle anderen sind leiser."},
   {"frage": "Was bedeutet die Endung „-issimo“?", "optionen": ["sehr", "halb", "plötzlich", "langsam"], "richtig": 0, "erklaerung": "fortissimo = sehr laut."},
   {"frage": "Was bedeutet fp?", "optionen": ["laut anspielen, sofort leise", "erst leise, dann laut", "sehr laut", "halblaut"], "richtig": 0, "erklaerung": "fortepiano."},
   {"frage": "Was bedeutet „dim.“?", "optionen": ["diminuendo – leiser werden", "dynamisch – lauter", "dimmen – langsamer werden", "mittelleise"], "richtig": 0, "erklaerung": "diminuendo und decrescendo bedeuten dasselbe."},
   {"frage": "Aus welcher Sprache stammen die Dynamikbezeichnungen?", "optionen": ["Italienisch", "Latein", "Französisch", "Englisch"], "richtig": 0, "erklaerung": "Viele musikalische Fachbegriffe kommen aus dem Italienischen."}
  ]}},
],
}
