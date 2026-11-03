/* =========================================================
   Notensatz: zeichnet Noten als SVG (Glyphen aus Bravura, SIL OFL)
   Läuft im Browser (window.Noten) und in Node (module.exports).
   ---------------------------------------------------------
   Kurzschrift für spec.noten (Tokens durch Leerzeichen getrennt):
     C4/4      Note c' als Viertel   (Oktave 4 = eingestrichen, 5 = zweigestrichen)
     F#4/8.    fis' als punktierte Achtel;  Bb4 = b',  Bn4 = h' mit Auflösungszeichen
     R/2       halbe Pause
     [C4 E4 G4]/2  Akkord
     ( ... )   Balkengruppe          3( ... )  Triole mit Balken
     3[ ... ]  Triole mit Klammer (z. B. Viertel-Triolen)
     |  ||  |. Taktstrich, Doppelstrich, Schlussstrich
     !p !mf !ff ...  Dynamikzeichen unter der folgenden Note
     <( <)  >( >)    Crescendo- bzw. Decrescendo-Gabel Anfang/Ende
     {HT} {GT} {txt}  Bogen mit Beschriftung zwischen vorheriger und nächster Note
     *C4/4     hervorgehobene Note
     C4/4@c'   Beschriftung unter der Note (_ = Leerzeichen)
     ?/4       Platzhalter (Kästchen mit Fragezeichen)
     _         etwas Abstand
   ========================================================= */
(function (wurzel, fabrik) {
  if (typeof module === "object" && module.exports) module.exports = fabrik(require("../werkzeug/glyphen.json"));
  else wurzel.Noten = fabrik(wurzel.NOTEN_GLYPHEN);
})(this, function (G) {
  "use strict";
  var SP = 10;                         // Linienabstand in px
  var BUCHST = { C: 0, D: 1, E: 2, F: 3, G: 4, A: 5, B: 6 };
  var BREITE = { 1: 5.2, 2: 4.2, 4: 3.3, 8: 2.6, 16: 2.3 };
  var KREUZ_POS = ["F5", "C5", "G5", "D5", "A4", "E5", "B4"];
  var B_POS = ["B4", "E5", "A4", "D5", "G4", "C5", "F4"];

  function r(x) { return Math.round(x * 100) / 100; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function glyph(name, x, y, skala, klasse) {
    var g = G[name]; if (!g) return "";
    return '<path class="' + (klasse || "ng") + '" transform="translate(' + r(x) + " " + r(y) + ") scale(" + r((skala || 1) * SP) + ')" d="' + g.d + '"/>';
  }
  function stufe(ton) {             // diatonische Stufe: C4 = 28, E4 = 30
    var m = /^([A-G])(#|b|n|x)?(\d)$/.exec(ton);
    if (!m) throw new Error("Unbekannter Ton: " + ton);
    return { st: BUCHST[m[1]] + 7 * +m[3], vz: m[2] || "" };
  }

  function parse(text) {
    var tok = text.trim().split(/\s+/), out = [], gruppe = null, i;
    var dyn = null, beschr = null;
    for (i = 0; i < tok.length; i++) {
      var t = tok[i];
      if (!t) continue;
      if (t === "(" || t === "3(") { gruppe = { balken: true, triole: t === "3(", id: out.length }; continue; }
      if (t === "3[") { gruppe = { balken: false, triole: true, klammer: true, id: out.length }; continue; }
      if (t === ")" || t === "]") { gruppe = null; continue; }
      if (t === "|" || t === "||" || t === "|.") { out.push({ typ: "strich", art: t }); continue; }
      if (t === "_") { out.push({ typ: "abstand" }); continue; }
      if (t[0] === "!") { dyn = t.slice(1); continue; }
      if (t === "<(" || t === ">(" || t === "<)" || t === ">)") { out.push({ typ: "gabel", art: t }); continue; }
      if (t[0] === "{") { out.push({ typ: "bogen", text: t.slice(1, -1) }); continue; }
      var e = { typ: "note", gruppe: gruppe, dyn: dyn };
      dyn = null;
      if (t[0] === "*") { e.hl = true; t = t.slice(1); }
      var at = t.indexOf("@");
      if (at >= 0) { e.label = t.slice(at + 1).replace(/_/g, " "); t = t.slice(0, at); }
      var teile = t.split("/");
      var dauer = teile[1] || "4";
      e.punkt = (dauer.match(/\./g) || []).length;
      e.dauer = parseInt(dauer, 10);
      var kopf = teile[0];
      if (kopf === "R") e.pause = true;
      else if (kopf === "?") e.frage = true;
      else if (kopf[0] === "[") e.toene = kopf.slice(1, -1).split(",").map(stufe);
      else e.toene = [stufe(kopf)];
      out.push(e);
    }
    return out;
  }

  /* Akkorde in eckigen Klammern enthalten Leerzeichen: vorher zusammenziehen */
  function vorbereiten(text) {
    return text.replace(/\[([A-G][^\]]*)\]/g, function (_, inn) { return "[" + inn.trim().split(/\s+/).join(",") + "]"; });
  }

  function render(spec) {
    spec = spec || {};
    var rhythmus = !!spec.rhythmus;
    var elemente = parse(vorbereiten(spec.noten || ""));
    var oben = (spec.oben != null ? spec.oben : 5) * SP;
    var y0 = oben, yUnten = y0 + 4 * SP;          // obere und untere Notenlinie
    var mitte = rhythmus ? y0 + 2 * SP : null;
    var bass = spec.schluessel === "bass", BASIS = bass ? 18 : 30, MID = BASIS + 4;
    function y(st) { return rhythmus ? mitte : yUnten - (st - BASIS) * SP / 2; }
    var svg = [], x = SP * 0.8, notenX = [], hairpins = [], dyns = [], boegen = [], gruppen = {};
    var hatLabel = elemente.some(function (e) { return e.label; });
    var hatDyn = elemente.some(function (e) { return e.dyn; }) || elemente.some(function (e) { return e.typ === "gabel"; });

    // Schlüssel, Vorzeichen, Takt
    if (!rhythmus && spec.schluessel !== false) { if (bass) { svg.push(glyph("fClef", x, y0 + SP, 1)); x += 3.8 * SP; } else { svg.push(glyph("gClef", x, yUnten - SP, 1)); x += 3.6 * SP; } }
    else if (rhythmus) x += 0.6 * SP;
    var tonart = spec.tonart || 0;
    for (var k = 0; k < Math.abs(tonart); k++) {
      var pos = stufe(tonart > 0 ? KREUZ_POS[k] : B_POS[k]).st - (bass ? 14 : 0);
      svg.push(glyph(tonart > 0 ? "accidentalSharp" : "accidentalFlat", x, y(pos), 1));
      x += 1.1 * SP;
    }
    if (tonart) x += 0.8 * SP;
    if (spec.takt) {
      if (spec.takt === "C") svg.push(glyph("timeSigCommon", x, y0 + 2 * SP, 1));
      else {
        var tt = spec.takt.split("/");
        [tt[0], tt[1]].forEach(function (zahl, j) {
          var zx = x + (zahl.length === 1 ? 0.15 * SP : 0);
          zahl.split("").forEach(function (z) { svg.push(glyph("timeSig" + z, zx, y0 + (j ? 3 : 1) * SP, 1)); zx += 1.8 * SP; });
        });
      }
      x += 3 * SP;
    }
    x += 0.8 * SP;
    var startNoten = x;

    // Noten setzen
    elemente.forEach(function (e, idx) {
      if (e.typ === "strich") {
        x += 0.4 * SP;
        e.x = x;
        x += (e.art === "|" ? 1.6 : 1.8) * SP;
        return;
      }
      if (e.typ === "abstand") { x += 1.5 * SP; return; }
      if (e.typ === "gabel") { e.x = x; hairpins.push(e); return; }
      if (e.typ === "bogen") { boegen.push({ idx: idx, text: e.text }); return; }
      var vzBreite = 0;
      if (e.toene) e.toene.forEach(function (t) { if (t.vz) vzBreite = 1.4 * SP; });
      x += vzBreite;
      e.x = x;
      notenX.push(e);
      var b = (BREITE[e.dauer] || 3.3) * SP * (e.punkt ? 1.25 : 1);
      if (e.gruppe && e.gruppe.triole) b *= 0.9;
      if (e.label) b = Math.max(b, e.label.length * 0.85 * SP + 1.6 * SP);
      if (e.dyn) b = Math.max(b, 3.6 * SP);
      x += b;
    });
    var ende = x + 0.4 * SP;
    var breite = Math.max(ende, spec.breite || 0);

    // Notenlinien
    var linien = "";
    if (rhythmus) linien = '<line class="nl" x1="0" y1="' + mitte + '" x2="' + r(breite) + '" y2="' + mitte + '"/>';
    else for (var l = 0; l < 5; l++) linien += '<line class="nl" x1="0" y1="' + (y0 + l * SP) + '" x2="' + r(breite) + '" y2="' + (y0 + l * SP) + '"/>';

    // Striche
    elemente.forEach(function (e) {
      if (e.typ !== "strich") return;
      var ya = rhythmus ? mitte - 2 * SP : y0, yb = rhythmus ? mitte + 2 * SP : yUnten;
      if (e.art === "|") svg.push('<line class="ts" x1="' + r(e.x) + '" y1="' + ya + '" x2="' + r(e.x) + '" y2="' + yb + '"/>');
      else if (e.art === "||") svg.push('<line class="ts" x1="' + r(e.x) + '" y1="' + ya + '" x2="' + r(e.x) + '" y2="' + yb + '"/><line class="ts" x1="' + r(e.x + 0.5 * SP) + '" y1="' + ya + '" x2="' + r(e.x + 0.5 * SP) + '" y2="' + yb + '"/>');
      else svg.push('<line class="ts" x1="' + r(e.x) + '" y1="' + ya + '" x2="' + r(e.x) + '" y2="' + yb + '"/><rect class="ng" x="' + r(e.x + 0.4 * SP) + '" y="' + ya + '" width="' + r(0.5 * SP) + '" height="' + (yb - ya) + '"/>');
    });

    // Gruppen sammeln
    notenX.forEach(function (e) {
      if (e.gruppe) { var id = e.gruppe.id; (gruppen[id] = gruppen[id] || { g: e.gruppe, n: [] }).n.push(e); }
    });

    // Halsrichtung
    notenX.forEach(function (e) {
      if (e.pause || e.frage) return;
      var st = e.toene.map(function (t) { return t.st; });
      e.hoch = Math.max.apply(null, st); e.tief = Math.min.apply(null, st);
      e.unten = rhythmus ? false : (e.hoch - MID) + (e.tief - MID) >= 0;       // Hals nach unten
    });
    Object.keys(gruppen).forEach(function (id) {
      var n = gruppen[id].n.filter(function (e) { return !e.pause; });
      if (!n.length) return;
      var summe = 0; n.forEach(function (e) { summe += (e.hoch - MID) + (e.tief - MID); });
      n.forEach(function (e) { e.unten = rhythmus ? false : summe >= 0; });
    });

    function kopfName(d) { return d === 1 ? "noteheadWhole" : d === 2 ? "noteheadHalf" : "noteheadBlack"; }
    function halsEnde(e) { return e.unten ? y(e.tief) + 3.5 * SP : y(e.hoch) - 3.5 * SP; }

    // Notenköpfe, Pausen, Hälse
    notenX.forEach(function (e) {
      var kl = e.hl ? "ng hl" : "ng";
      if (e.frage) {
        svg.push('<rect class="frage" x="' + r(e.x - 0.3 * SP) + '" y="' + r(y0 - 0.5 * SP) + '" width="' + r(2.4 * SP) + '" height="' + r(5 * SP) + '" rx="4"/>' +
          '<text class="frage-t" x="' + r(e.x + 0.9 * SP) + '" y="' + r(y0 + 2.6 * SP) + '" text-anchor="middle">?</text>');
        return;
      }
      if (e.pause) {
        var py = { 1: y0 + SP, 2: y0 + 2 * SP, 4: y0 + 2 * SP, 8: y0 + 2 * SP, 16: y0 + 2 * SP }[e.dauer];
        if (rhythmus) py = { 1: mitte - 0.0, 2: mitte, 4: mitte, 8: mitte, 16: mitte }[e.dauer] + (e.dauer === 1 ? 0 : 0);
        var pn = { 1: "restWhole", 2: "restHalf", 4: "restQuarter", 8: "rest8th", 16: "rest16th" }[e.dauer];
        if (rhythmus && e.dauer === 1) py = mitte + 0.0;
        if (rhythmus && e.dauer === 2) py = mitte;
        svg.push(glyph(pn, e.x, py, 1, kl));
        if (e.punkt) svg.push(glyph("augmentationDot", e.x + 1.6 * SP, y0 + 1.5 * SP + (rhythmus ? 0.5 * SP : 0), 1, kl));
        e.mitteX = e.x + 0.55 * SP;
        return;
      }
      var kn = kopfName(e.dauer), kb = G[kn].w;
      var sts = e.toene.map(function (t) { return t.st; }).sort(function (a, b) { return a - b; });
      // Hilfslinien
      if (!rhythmus) {
        var hl = [];
        for (var s = BASIS - 2; s >= e.tief; s -= 2) hl.push(s);
        for (s = BASIS + 10; s <= e.hoch; s += 2) hl.push(s);
        hl.forEach(function (s) { svg.push('<line class="hl-linie" x1="' + r(e.x - 0.4 * SP) + '" y1="' + r(y(s)) + '" x2="' + r(e.x + (kb + 0.4) * SP) + '" y2="' + r(y(s)) + '"/>'); });
      }
      e.toene.forEach(function (t, j) {
        var versatz = 0;
        if (e.toene.some(function (u) { return u !== t && Math.abs(u.st - t.st) === 1 && (e.unten ? u.st > t.st : u.st < t.st); }) && j % 2) versatz = (e.unten ? -1 : 1) * kb * SP;
        svg.push(glyph(kn, e.x + versatz, y(t.st), 1, kl));
        if (t.vz) svg.push(glyph({ "#": "accidentalSharp", b: "accidentalFlat", n: "accidentalNatural" }[t.vz], e.x - 1.35 * SP, y(t.st), 1, kl));
        for (var p = 0; p < e.punkt; p++) {
          var dy = (t.st % 2 === 0 && !rhythmus) ? -0.5 * SP : 0;
          svg.push(glyph("augmentationDot", e.x + (kb + 0.45 + p * 0.6) * SP, y(t.st) + dy, 1, kl));
        }
      });
      e.mitteX = e.x + kb * SP / 2;
      if (e.dauer >= 2) {
        e.halsX = e.unten ? e.x + 0.06 * SP : e.x + (kb - 0.06) * SP;
        e.halsA = e.unten ? y(e.hoch) + 0.17 * SP : y(e.tief) - 0.17 * SP;
        e.halsB = halsEnde(e);
      }
    });

    // Balken angleichen
    Object.keys(gruppen).forEach(function (id) {
      var gr = gruppen[id], n = gr.n.filter(function (e) { return !e.pause && e.halsX != null; });
      if (!gr.g.balken || n.length < 2) return;
      var unten = n[0].unten, a = n[0], z = n[n.length - 1];
      var ya = a.halsB, yz = z.halsB;
      var steig = Math.max(-SP, Math.min(SP, (yz - ya) * 0.5));
      function bY(xx) { return ya + (xx - a.halsX) / (z.halsX - a.halsX || 1) * steig; }
      // Mindestlänge
      var korr = 0;
      n.forEach(function (e) {
        var soll = unten ? (y(e.tief) + 3 * SP) : (y(e.hoch) - 3 * SP);
        var ist = bY(e.halsX) + korr;
        if (unten && ist < soll) korr += soll - ist;
        if (!unten && ist > soll) korr -= ist - soll;
      });
      n.forEach(function (e) { e.halsB = bY(e.halsX) + korr; e.imBalken = true; });
      var dick = 0.5 * SP, dir = unten ? -1 : 1;
      svg.push('<path class="ng' + (a.hl && z.hl ? " hl" : "") + '" d="M' + r(a.halsX - (unten ? 0 : 0.06 * SP)) + " " + r(a.halsB) + " L" + r(z.halsX + (unten ? 0.06 * SP : 0)) + " " + r(z.halsB) + " l0 " + r(dir * dick) + " L" + r(a.halsX - (unten ? 0 : 0.06 * SP)) + " " + r(a.halsB + dir * dick) + 'Z"/>');
      // zweiter Balken für Sechzehntel
      var off = dir * 0.75 * SP;
      for (var i = 0; i < n.length; i++) {
        if (n[i].dauer < 16) continue;
        var nach = n[i + 1] && n[i + 1].dauer >= 16, vor = n[i - 1] && n[i - 1].dauer >= 16;
        var xa, xb;
        if (nach) { xa = n[i].halsX; xb = n[i + 1].halsX; }
        else if (vor) continue;
        else if (i > 0) { xa = n[i].halsX - 1.1 * SP; xb = n[i].halsX; }
        else { xa = n[i].halsX; xb = n[i].halsX + 1.1 * SP; }
        var ya2 = bY(xa) + korr + off, yb2 = bY(xb) + korr + off;
        svg.push('<path class="ng" d="M' + r(xa) + " " + r(ya2) + " L" + r(xb) + " " + r(yb2) + " l0 " + r(dir * dick) + " L" + r(xa) + " " + r(ya2 + dir * dick) + 'Z"/>');
      }
      gr.balkenMitte = { x: (a.halsX + z.halsX) / 2, y: (a.halsB + z.halsB) / 2 + korr * 0, unten: unten };
    });

    // Hälse und Fähnchen
    notenX.forEach(function (e) {
      if (e.halsX == null) return;
      var kl = e.hl ? "ng hl" : "ng";
      svg.push('<line class="hals' + (e.hl ? " hl" : "") + '" x1="' + r(e.halsX) + '" y1="' + r(e.halsA) + '" x2="' + r(e.halsX) + '" y2="' + r(e.halsB) + '"/>');
      if (!e.imBalken && e.dauer >= 8) {
        var fn = (e.dauer === 8 ? "flag8th" : "flag16th") + (e.unten ? "Down" : "Up");
        svg.push(glyph(fn, e.halsX - 0.06 * SP, e.halsB, 1, kl));
      }
    });

    // Triolen
    Object.keys(gruppen).forEach(function (id) {
      var gr = gruppen[id];
      if (!gr.g.triole) return;
      var n = gr.n, a = n[0], z = n[n.length - 1];
      var unten = n.some(function (e) { return e.unten; }) && n.every(function (e) { return e.unten !== false; });
      var xm = (a.x + z.x + (G.noteheadBlack.w * SP)) / 2;
      if (gr.g.balken && gr.balkenMitte) {
        var yy = gr.balkenMitte.unten ? gr.balkenMitte.y + 2.2 * SP : gr.balkenMitte.y - 0.9 * SP;
        svg.push(glyph("tuplet3", xm - 0.6 * SP, yy, 1));
      } else {
        var minY = Math.min.apply(null, n.map(function (e) { return e.halsB != null && !e.unten ? e.halsB : (e.pause ? y0 : y(e.hoch || MID)) - SP; }));
        var yk = Math.min(minY, y0) - 1.2 * SP;
        var xa = a.x - 0.2 * SP, xb = z.x + 1.4 * SP;
        svg.push('<path class="klammer" d="M' + r(xa) + " " + r(yk + 0.8 * SP) + " V" + r(yk) + " H" + r(xm - 1 * SP) + " M" + r(xm + 1 * SP) + " " + r(yk) + " H" + r(xb) + " V" + r(yk + 0.8 * SP) + '"/>');
        svg.push(glyph("tuplet3", xm - 0.6 * SP, yk + 0.7 * SP, 1));
      }
    });

    // Bögen (Halbton/Ganzton)
    boegen.forEach(function (bo) {
      var vor = null, nach = null;
      for (var i = bo.idx - 1; i >= 0; i--) if (elemente[i].typ === "note") { vor = elemente[i]; break; }
      for (i = bo.idx + 1; i < elemente.length; i++) if (elemente[i].typ === "note") { nach = elemente[i]; break; }
      if (!vor || !nach) return;
      var xa = vor.mitteX, xb = nach.mitteX;
      var yb = Math.min(y0, vor.halsB != null && !vor.unten ? vor.halsB : y0, nach.halsB != null && !nach.unten ? nach.halsB : y0, y(vor.hoch || MID) - SP, y(nach.hoch || MID) - SP) - 0.8 * SP;
      var kl = /^(HT|½)$/.test(bo.text) ? "bogen ht" : "bogen";
      var t = bo.text === "HT" ? "½" : bo.text === "GT" ? "1" : bo.text;
      svg.push('<path class="' + kl + '" d="M' + r(xa) + " " + r(yb) + " Q" + r((xa + xb) / 2) + " " + r(yb - 1.6 * SP) + " " + r(xb) + " " + r(yb) + '"/>');
      svg.push('<text class="bogen-t' + (kl === "bogen ht" ? " ht" : "") + '" x="' + r((xa + xb) / 2) + '" y="' + r(yb - 1.2 * SP) + '" text-anchor="middle">' + esc(t) + "</text>");
    });

    // Dynamik und Gabeln
    var yDyn = yUnten + (rhythmus ? 1 : 3.4) * SP + 1.4 * SP;
    notenX.forEach(function (e) {
      if (!e.dyn) return;
      var buchst = { p: "dynamicPiano", m: "dynamicMezzo", f: "dynamicForte", s: "dynamicSforzando", z: "dynamicZ", r: "dynamicRinforzando" };
      var dx = e.x - 0.4 * SP;
      e.dyn.split("").forEach(function (c) { var n = buchst[c]; if (!n) return; svg.push(glyph(n, dx, yDyn, 1)); dx += (G[n].w - 0.15) * SP; });
    });
    for (var h = 0; h + 1 < hairpins.length; h += 2) {
      var a1 = hairpins[h], a2 = hairpins[h + 1], cres = a1.art[0] === "<";
      var xa = a1.x - 0.2 * SP, xb = a2.x - 1.2 * SP, ym = yDyn - 0.4 * SP, o = 0.75 * SP;
      svg.push('<path class="gabel" d="' + (cres ? "M" + r(xb) + " " + r(ym - o) + " L" + r(xa) + " " + r(ym) + " L" + r(xb) + " " + r(ym + o) : "M" + r(xa) + " " + r(ym - o) + " L" + r(xb) + " " + r(ym) + " L" + r(xa) + " " + r(ym + o)) + '"/>');
    }

    // Beschriftungen
    var yLab = (hatDyn ? yDyn + 2.6 * SP : yUnten + (rhythmus ? 2.6 : 3.6) * SP);
    notenX.forEach(function (e) {
      if (!e.label) return;
      svg.push('<text class="nlabel' + (e.hl ? " hl" : "") + '" x="' + r(e.mitteX) + '" y="' + r(yLab) + '" text-anchor="middle">' + esc(e.label) + "</text>");
    });

    var hoehe = (hatLabel ? yLab + 0.8 * SP : (hatDyn ? yDyn + 1.4 * SP : yUnten + (spec.unten != null ? spec.unten : 4.5) * SP));
    if (rhythmus && !hatLabel && !hatDyn) hoehe = mitte + 4.2 * SP;
    var top = rhythmus ? mitte - 4.5 * SP : 0;
    if (rhythmus) { hoehe -= top; }
    var titel = spec.titel ? "<title>" + esc(spec.titel) + "</title>" : "";
    var maxB = Math.round(breite * (spec.zoom || 1.6));
    var html = '<svg class="noten" viewBox="0 ' + r(top) + " " + r(breite) + " " + r(hoehe) + '" style="max-width:' + maxB + 'px" role="img"' +
      (spec.titel ? ' aria-label="' + esc(spec.titel) + '"' : ' aria-hidden="true"') + ' xmlns="http://www.w3.org/2000/svg">' + titel + linien + svg.join("") + "</svg>";
    return { svg: html, noten: notenX, breite: breite, hoehe: hoehe, y: y, y0: y0, yUnten: yUnten, start: startNoten, top: top, basis: BASIS };
  }

  return { render: render, stufe: stufe, SP: SP, glyph: glyph, parse: function (t) { return parse(vorbereiten(t)); } };
});
