/* =========================================================
   Musik Klasse 10: Klang, Notenübungen und Werkzeuge
   Benötigt: glyphen.js, noten.js (window.Noten)
   ========================================================= */
(function () {
  "use strict";
  var N = window.Noten;
  var NS = "http://www.w3.org/2000/svg";

  /* ---------------------------------------------------------
     Hilfen
     --------------------------------------------------------- */
  function el(tag, attrs, kinder) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "text") e.textContent = attrs[k];
      else if (k === "html") e.innerHTML = attrs[k];
      else if (k === "class") e.className = attrs[k];
      else if (k.indexOf("on") === 0) e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    (kinder || []).forEach(function (k) { if (k) e.appendChild(typeof k === "string" ? document.createTextNode(k) : k); });
    return e;
  }
  function mischen(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function zufall(a) { return a[Math.floor(Math.random() * a.length)]; }
  function lob(anteil) {
    if (anteil === 1) return "Alles richtig – stark!";
    if (anteil >= 0.75) return "Sehr gut, fast alles richtig.";
    if (anteil >= 0.5) return "Gut! Schau dir die markierten Stellen noch einmal an.";
    return "Lies das Kapitel noch einmal und versuche es erneut.";
  }
  function noten(text, spec) { var s = Object.assign({}, spec || {}); s.noten = text; return N.render(s); }
  function svgElement(html) { var d = document.createElement("div"); d.innerHTML = html; return d.firstChild; }

  /* ---------------------------------------------------------
     Theorie
     --------------------------------------------------------- */
  var STAMM = "CDEFGAB", HALB = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }, DT = { C: "c", D: "d", E: "e", F: "f", G: "g", A: "a", B: "h" };
  function zerlege(t) { var m = /^([A-G])(#|b|n)?(\d)$/.exec(t); return { b: m[1], v: (m[2] || "").replace("n", ""), o: +m[3] }; }
  function midi(t) { var z = zerlege(t); return 12 * (z.o + 1) + HALB[z.b] + (z.v === "#" ? 1 : z.v === "b" ? -1 : 0); }
  function stufeVon(t) { var z = zerlege(t); return STAMM.indexOf(z.b) + 7 * z.o; }
  function tonname(t, okt) {
    var z = zerlege(t), n = DT[z.b];
    if (z.v === "#") n += "is";
    else if (z.v === "b") n = { E: "es", A: "as", B: "b" }[z.b] || n + "es";
    if (okt) { if (z.o <= 2) n = n.charAt(0).toUpperCase() + n.slice(1); n += { 3: "", 4: "′", 5: "″", 6: "‴" }[z.o] || ""; }
    return n;
  }
  function tonAus(st, m) {
    var b = STAMM[((st % 7) + 7) % 7], o = Math.floor(st / 7), d = m - (12 * (o + 1) + HALB[b]);
    var v = { "0": "", "1": "#", "-1": "b" }[String(d)];
    return v == null ? null : b + v + o;
  }
  var DUR = [2, 2, 1, 2, 2, 2, 1], MOLL = [2, 1, 2, 2, 1, 2, 2], MOLL_H = [2, 1, 2, 2, 1, 3, 1];
  function tonleiter(g, schritte) { var r = [g], st = stufeVon(g), m = midi(g); schritte.forEach(function (s) { st++; m += s; r.push(tonAus(st, m)); }); return r; }
  var INTERVALLE = { "0,0": "reine Prime", "1,1": "kleine Sekunde", "1,2": "große Sekunde", "2,3": "kleine Terz", "2,4": "große Terz", "3,5": "reine Quarte", "3,6": "übermäßige Quarte",
    "4,6": "verminderte Quinte", "4,7": "reine Quinte", "5,8": "kleine Sexte", "5,9": "große Sexte", "6,10": "kleine Septime", "6,11": "große Septime", "7,12": "reine Oktave" };
  function intervall(a, b) { return INTERVALLE[(stufeVon(b) - stufeVon(a)) + "," + (midi(b) - midi(a))] || null; }
  function dreiklang(g, art) { var iv = { Dur: [4, 7], Moll: [3, 7], vermindert: [3, 6], "übermäßig": [4, 8] }[art]; return [g, tonAus(stufeVon(g) + 2, midi(g) + iv[0]), tonAus(stufeVon(g) + 4, midi(g) + iv[1])]; }
  var TONARTEN = { "0": ["C-Dur", "a-Moll", "C4"], "1": ["G-Dur", "e-Moll", "G4"], "2": ["D-Dur", "h-Moll", "D4"], "3": ["A-Dur", "fis-Moll", "A4"], "4": ["E-Dur", "cis-Moll", "E4"], "5": ["H-Dur", "gis-Moll", "B3"],
    "6": ["Fis-Dur", "dis-Moll", "F#4"], "-1": ["F-Dur", "d-Moll", "F4"], "-2": ["B-Dur", "g-Moll", "Bb3"], "-3": ["Es-Dur", "c-Moll", "Eb4"], "-4": ["As-Dur", "f-Moll", "Ab3"], "-5": ["Des-Dur", "b-Moll", "Db4"], "-6": ["Ges-Dur", "es-Moll", "Gb3"] };

  /* ---------------------------------------------------------
     Klang (Web Audio, wird erst beim ersten Klick gestartet)
     --------------------------------------------------------- */
  var ctx = null, laufend = [];
  function audio() {
    if (!ctx) { var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; ctx = new AC(); }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }
  function stopp() { laufend.forEach(function (o) { try { o.stop(); } catch (e) {} }); laufend = []; }
  function ton(m, start, dauer, laut) {
    var c = audio(); if (!c) return;
    var f = 440 * Math.pow(2, (m - 69) / 12), t0 = c.currentTime + start, g = c.createGain();
    g.connect(c.destination);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime((laut || 0.22), t0 + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0008, t0 + Math.max(0.25, dauer * 1.1));
    [[1, "triangle", 1], [2, "sine", 0.35], [3, "sine", 0.12]].forEach(function (p) {
      var o = c.createOscillator(), gg = c.createGain();
      o.type = p[1]; o.frequency.value = f * p[0]; gg.gain.value = p[2];
      o.connect(gg); gg.connect(g); o.start(t0); o.stop(t0 + Math.max(0.3, dauer * 1.15)); laufend.push(o);
    });
  }
  function klick(start, betont) {
    var c = audio(); if (!c) return;
    var t0 = c.currentTime + start, o = c.createOscillator(), g = c.createGain();
    o.type = "square"; o.frequency.value = betont ? 1600 : 1100;
    g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.18, t0 + 0.003); g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.07);
    o.connect(g); g.connect(c.destination); o.start(t0); o.stop(t0 + 0.08); laufend.push(o);
  }
  function holz(start, dauer) {
    var c = audio(); if (!c) return;
    var t0 = c.currentTime + start, o = c.createOscillator(), g = c.createGain();
    o.type = "sine"; o.frequency.value = 880;
    g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.3, t0 + 0.005);
    g.gain.exponentialRampToValueAtTime(0.02, t0 + Math.min(0.15, dauer * 0.8)); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dauer * 0.95);
    o.connect(g); g.connect(c.destination); o.start(t0); o.stop(t0 + dauer); laufend.push(o);
  }
  var KREUZE = ["F", "C", "G", "D", "A", "E", "B"], BES = ["B", "E", "A", "D", "G", "C", "F"];
  /* Spielt eine Notenzeile in Kurzschrift. Gibt die Gesamtdauer zurück. */
  function spiele(text, opt) {
    opt = opt || {}; stopp();
    var el = N.parse(text), viertel = 60 / (opt.tempo || 92), t = 0.05, tonart = opt.tonart || 0, takt = {}, trio = null;
    var gen = {};
    for (var k = 0; k < Math.abs(tonart); k++) gen[(tonart > 0 ? KREUZE : BES)[k]] = tonart > 0 ? 1 : -1;
    var ereignisse = [], gebunden = false;
    el.forEach(function (e) {
      if (e.typ === "strich") { takt = {}; return; }
      if (e.typ === "bindung") { gebunden = true; return; }
      if (e.typ !== "note" || e.frage) return;
      var d = 4 / e.dauer * viertel; if (e.punkt) d *= 1.5;
      if (e.gruppe && e.gruppe.triole) d *= 2 / 3;
      if (gebunden && ereignisse.length && !e.pause) { ereignisse[ereignisse.length - 1].d += d; gebunden = false; t += d; return; }
      gebunden = false;
      if (!e.pause) {
        var ms = opt.rhythmus ? [] : e.toene.map(function (tt) {
          var b = STAMM[tt.st % 7], o = Math.floor(tt.st / 7), acc;
          if (tt.vz) { acc = { "#": 1, b: -1, n: 0 }[tt.vz]; takt[tt.st] = acc; }
          else if (takt[tt.st] != null) acc = takt[tt.st];
          else acc = gen[b] || 0;
          return 12 * (o + 1) + HALB[b] + acc;
        });
        ereignisse.push({ t: t, d: d, ms: ms });
      }
      t += d;
    });
    ereignisse.forEach(function (ev) {
      if (opt.rhythmus) holz(ev.t, ev.d);
      else ev.ms.forEach(function (m) { ton(m, ev.t, ev.d * 0.95); });
    });
    return t;
  }
  function spielKnopf(text, opt, beschriftung) {
    return el("button", { class: "knopf leise spiel", type: "button", text: "▶ " + (beschriftung || "Anhören"), onclick: function () { spiele(text, opt); } });
  }
  window.MusikKlang = { spiele: spiele, ton: ton, stopp: stopp, klick: klick };

  /* Anhören-Knöpfe an allen Notenbeispielen */
  function notenbeispiele() {
    document.querySelectorAll("figure.notenbeispiel[data-spiel]").forEach(function (f) {
      var d; try { d = JSON.parse(f.getAttribute("data-spiel")); } catch (e) { return; }
      var b = spielKnopf(d.noten, { tonart: d.tonart, rhythmus: d.rhythmus });
      b.classList.add("klein");
      (f.querySelector("figcaption") || f).appendChild(b);
    });
  }

  /* ---------------------------------------------------------
     Sperre: Prüfen und Lösung erst nach vollständiger Bearbeitung
     --------------------------------------------------------- */
  function sperre(knoepfe, hinweis, offen, einzahl, mehrzahl) {
    var n = offen();
    knoepfe.forEach(function (k) { k.disabled = n > 0; k.title = n > 0 ? "Bearbeite zuerst die ganze Aufgabe." : ""; });
    hinweis.textContent = n > 0 ? knoepfe.map(function (k) { return "„" + k.textContent + "“"; }).join(" und ") + (knoepfe.length > 1 ? " gehen" : " geht") +
      " erst, wenn du alles bearbeitet hast. Noch " + n + " " + (n === 1 ? einzahl : mehrzahl) + " offen." : "";
    hinweis.hidden = n === 0;
  }
  function knopfreihe(pruefen, loesung, neu) {
    var p = el("button", { class: "knopf", type: "button", text: "Prüfen", onclick: pruefen });
    var l = el("button", { class: "knopf leise", type: "button", text: "Lösung zeigen", onclick: loesung });
    var n = el("button", { class: "knopf leise", type: "button", text: "Neu starten", onclick: neu });
    return { reihe: el("div", { class: "knopfreihe" }, [p, l, n]), pruefen: p, loesung: l };
  }
  function rueckmeldung(rueck, n, gesamt) {
    if (window.Fortschritt) window.Fortschritt.melden(rueck, n / gesamt);
    rueck.innerHTML = "";
    rueck.appendChild(el("strong", { class: n === gesamt ? "gut" : "schlecht", text: n + " von " + gesamt + " richtig. " }));
    rueck.appendChild(document.createTextNode(lob(n / gesamt)));
  }

  /* ---------------------------------------------------------
     Übung: Notenquiz (Fragen mit Notenbildern)
     --------------------------------------------------------- */
  function notenquiz(box, daten) {
    var fragen = mischen(daten.fragen), beantwortet = 0, richtig = 0;
    var stand = el("div", { class: "punktestand", role: "status", "aria-live": "polite" }, [el("span"), el("button", { class: "knopf", type: "button", text: "Neu starten", onclick: function () { box.innerHTML = ""; notenquiz(box, daten); } })]);
    function standText() { stand.firstChild.textContent = richtig + " von " + beantwortet + " richtig" + (beantwortet < fragen.length ? " (" + (fragen.length - beantwortet) + " offen)" : " – " + lob(richtig / fragen.length)); }
    fragen.forEach(function (f, nr) {
      var karte = el("div", { class: "frage-karte" });
      karte.appendChild(el("p", { class: "frage", text: (nr + 1) + ". " + f.frage }));
      if (f.noten != null && (f.noten !== "" || (f.spec && f.spec.tonart))) {
        var bild = el("div", { class: "frage-noten", html: noten(f.noten, f.spec).svg });
        karte.appendChild(bild);
        if (daten.hoeren && f.noten && f.noten.indexOf("?") < 0) karte.appendChild(spielKnopf(f.noten.replace(/^\[([^\]]+)\]\/1$/, function (_, inn) { return inn.split(" ").map(function (t) { return t + "/2"; }).join(" ") + " [" + inn + "]/1"; }), { tonart: (f.spec || {}).tonart }));
      }
      var opts = el("div", { class: "optionen" + (f.optionen.some(function (o) { return typeof o === "object"; }) ? " noten-optionen" : "") });
      var reihenfolge = mischen(f.optionen.map(function (o, i) { return { o: o, i: i }; }));
      var erkl = el("p", { class: "erklaerung", hidden: "" });
      reihenfolge.forEach(function (r) {
        var inhalt = typeof r.o === "object" ? el("span", { class: "opt-noten", html: noten(r.o.noten, r.o.spec).svg }) : el("span", { text: r.o });
        var b = el("button", { type: "button", class: "option" }, [inhalt]);
        if (typeof r.o === "object") b.setAttribute("aria-label", "Notenbild " + (reihenfolge.indexOf(r) + 1));
        b.addEventListener("click", function () {
          Array.prototype.forEach.call(opts.children, function (k) { k.disabled = true; });
          var ok = r.i === f.richtig;
          b.classList.add(ok ? "ist-richtig" : "ist-falsch");
          if (!ok) Array.prototype.forEach.call(opts.children, function (k, idx) { if (reihenfolge[idx].i === f.richtig) k.classList.add("ist-richtig"); });
          erkl.hidden = false;
          erkl.textContent = (ok ? "Richtig! " : "Leider falsch. ") + (f.erklaerung || "");
          erkl.className = "erklaerung " + (ok ? "gut" : "schlecht");
          beantwortet++; if (ok) richtig++; standText();
          if (beantwortet === fragen.length && window.Fortschritt) window.Fortschritt.melden(box, richtig / fragen.length);
        });
        opts.appendChild(b);
      });
      karte.appendChild(opts); karte.appendChild(erkl);
      box.appendChild(karte);
    });
    box.appendChild(stand); standText();
  }

  /* ---------------------------------------------------------
     Übung: Noten lesen (Namen eintragen)
     --------------------------------------------------------- */
  function norm(s, oktave) {
    s = String(s).replace(/\s+/g, "").replace(/[’′´`‘]/g, "'").replace(/″/g, "''");
    if (!oktave) s = s.replace(/['0-9]/g, "").toLowerCase();
    else s = s.charAt(0) + s.slice(1).toLowerCase();
    return s;
  }
  function notenlesen(box, daten) {
    var felder = [];
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" }), hinweis = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    daten.aufgaben.forEach(function (a, nr) {
      var r = noten(a.noten, Object.assign({ zoom: 1.9 }, a.spec || {}));
      var karte = el("div", { class: "lese-karte" }), buehne = el("div", { class: "lese-buehne" });
      buehne.appendChild(svgElement(r.svg));
      var zeile = el("div", { class: "lese-felder" });
      r.noten.forEach(function (n, i) {
        var f = el("input", { type: "text", autocomplete: "off", autocapitalize: "off", spellcheck: "false", "aria-label": "Zeile " + (nr + 1) + ", Note " + (i + 1) });
        f.style.left = (n.mitteX / r.breite * 100) + "%";
        f.dataset.antworten = JSON.stringify(a.antworten[i]);
        zeile.appendChild(f); felder.push(f);
      });
      buehne.appendChild(zeile);
      karte.appendChild(buehne);
      karte.appendChild(spielKnopf(a.noten, { tonart: (a.spec || {}).tonart }, "Anhören"));
      box.appendChild(karte);
    });
    var k = knopfreihe(pruefen, loesung, function () { box.innerHTML = ""; notenlesen(box, daten); });
    box.appendChild(k.reihe); box.appendChild(hinweis); box.appendChild(rueck);
    function offen() { return felder.filter(function (f) { return !f.value.trim(); }).length; }
    function aktual() { sperre([k.pruefen, k.loesung], hinweis, offen, "Feld", "Felder"); }
    felder.forEach(function (f) { f.addEventListener("input", function () { f.classList.remove("ist-richtig", "ist-falsch"); aktual(); }); });
    aktual();
    function pruefen() {
      if (offen()) return;
      var n = 0;
      felder.forEach(function (f) {
        var ok = JSON.parse(f.dataset.antworten).some(function (a) { return norm(a, daten.oktave) === norm(f.value, daten.oktave); });
        f.classList.toggle("ist-richtig", ok); f.classList.toggle("ist-falsch", !ok); if (ok) n++;
      });
      rueckmeldung(rueck, n, felder.length);
    }
    function loesung() {
      if (offen()) return;
      pruefen();
      felder.forEach(function (f) {
        var alt = f.nextElementSibling; if (alt && alt.classList.contains("lese-loesung")) alt.remove();
        if (f.classList.contains("ist-falsch")) {
          var l = el("span", { class: "lese-loesung", text: JSON.parse(f.dataset.antworten)[0] }); l.style.left = f.style.left; f.insertAdjacentElement("afterend", l);
        }
      });
      rueck.appendChild(document.createTextNode(" Unter falschen Antworten steht jetzt die richtige Lösung."));
    }
  }

  /* ---------------------------------------------------------
     Notensystem zum Anklicken (für „notieren“)
     --------------------------------------------------------- */
  var VZ_ZEICHEN = { "": "kein", "#": "♯", b: "♭" };
  function stufeZuTon(st, vz) { return STAMM[((st % 7) + 7) % 7] + vz + Math.floor(st / 7); }
  function klickSystem(opts) {
    // opts: vorgabe [Töne], akkord, max, onAenderung, vorzeichen
    var gesetzt = [], vz = "", gesperrt = false, loesung = null, markierung = null;
    var huelle = el("div", { class: "klick-system" });
    var buehne = el("div", { class: "klick-buehne", tabindex: "0", role: "application", "aria-label": "Notensystem: Klicke, um eine Note zu setzen. Mit den Pfeiltasten hoch und runter, Enter setzt die Note." });
    var vzWahl = el("div", { class: "wahl vz-wahl", role: "group", "aria-label": "Vorzeichen" });
    var BASIS = opts.schluessel === "bass" ? 18 : 30, vorschauSt = BASIS, MIN = BASIS - 7, MAX = BASIS + 15;
    if (opts.vorzeichen) ["", "#", "b"].forEach(function (v) {
      var b = el("button", { type: "button", "aria-pressed": v === "" ? "true" : "false", text: VZ_ZEICHEN[v], title: v === "" ? "ohne Vorzeichen" : v === "#" ? "Kreuz" : "b" });
      b.addEventListener("click", function () { vz = v; Array.prototype.forEach.call(vzWahl.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); zeichne(); });
      vzWahl.appendChild(b);
    });
    var zurueck = el("button", { class: "knopf leise klein", type: "button", text: "↶ Zurück", onclick: function () { if (gesperrt || !gesetzt.length) return; gesetzt.pop(); markierung = null; zeichne(); opts.onAenderung(); } });
    var steuer = el("div", { class: "klick-steuer" }, [opts.vorzeichen ? vzWahl : null, zurueck]);
    huelle.appendChild(buehne); huelle.appendChild(steuer);
    var letztes = null;

    function text() {
      var toene = (opts.vorgabe || []).concat(gesetzt);
      var platz = gesetzt.length < opts.max;
      if (opts.akkord) {
        var alle = toene.slice();
        var t = alle.length ? "[" + alle.join(" ") + "]/1" : "";
        if (loesung) t += " _ [" + (opts.vorgabe || []).concat(loesung).join(" ") + "]/1@Lösung";
        return t + " _";
      }
      var teile = toene.map(function (t, i) {
        var nr = i - (opts.vorgabe || []).length;
        var hl = markierung && nr >= 0 && markierung[nr] === false;
        return (hl ? "*" : "") + t + "/1";
      });
      if (platz) teile.push("_ _");
      return teile.join(" ") + (loesung ? " || " + loesung.map(function (t) { return t + "/1"; }).join(" ") : "");
    }
    function zeichne() {
      letztes = noten(text(), { zoom: 2.2, schluessel: opts.schluessel, breite: opts.akkord ? 150 : Math.max(220, 90 + ((opts.vorgabe || []).length + opts.max) * 44 + (loesung ? opts.max * 44 + 30 : 0)) });
      buehne.innerHTML = letztes.svg;
      var s = buehne.firstChild;
      if (!gesperrt && gesetzt.length < opts.max) {
        // Vorschau-Note
        var x = opts.akkord ? letztes.start + 4 : (letztes.noten.length ? letztes.noten[letztes.noten.length - 1].x + (gesetzt.length || (opts.vorgabe || []).length ? 44 : 0) : letztes.start + 6);
        if (!opts.akkord && !letztes.noten.length) x = letztes.start + 6;
        var g = document.createElementNS(NS, "g"); g.setAttribute("class", "vorschau");
        var y = letztes.y(vorschauSt);
        var hl = "";
        for (var st = BASIS - 2; st >= vorschauSt; st -= 2) hl += '<line class="hl-linie" x1="' + (x - 4) + '" y1="' + letztes.y(st) + '" x2="' + (x + 16) + '" y2="' + letztes.y(st) + '"/>';
        for (st = BASIS + 10; st <= vorschauSt; st += 2) hl += '<line class="hl-linie" x1="' + (x - 4) + '" y1="' + letztes.y(st) + '" x2="' + (x + 16) + '" y2="' + letztes.y(st) + '"/>';
        g.innerHTML = hl + N.glyph("noteheadWhole", x, y, 1, "ng") + (vz ? N.glyph(vz === "#" ? "accidentalSharp" : "accidentalFlat", x - 13, y, 1, "ng") : "");
        g.style.display = buehne.dataset.hover === "1" || document.activeElement === buehne ? "" : "none";
        s.appendChild(g);
        letztes.vorschau = g; letztes.vorschauX = x;
      }
    }
    function stufeAus(ev) {
      var s = buehne.firstChild, pt = s.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
      var p = pt.matrixTransform(s.getScreenCTM().inverse());
      var st = Math.round(BASIS + (letztes.yUnten - p.y) / (N.SP / 2));
      return Math.max(MIN, Math.min(MAX, st));
    }
    function setzen(st) {
      if (gesperrt || gesetzt.length >= opts.max) return;
      var t = stufeZuTon(st, vz);
      if (opts.akkord && (opts.vorgabe || []).concat(gesetzt).indexOf(t) >= 0) return;
      gesetzt.push(t);
      try { ton(midi(t), 0, 0.6); } catch (e) {}
      if (opts.vorzeichen) { vz = ""; Array.prototype.forEach.call(vzWahl.children, function (x, i) { x.setAttribute("aria-pressed", i === 0 ? "true" : "false"); }); }
      markierung = null;
      zeichne(); opts.onAenderung();
    }
    buehne.addEventListener("pointermove", function (ev) { buehne.dataset.hover = "1"; vorschauSt = stufeAus(ev); zeichne(); });
    buehne.addEventListener("pointerleave", function () { buehne.dataset.hover = ""; zeichne(); });
    buehne.addEventListener("click", function (ev) { setzen(stufeAus(ev)); });
    buehne.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowUp") { vorschauSt = Math.min(MAX, vorschauSt + 1); ev.preventDefault(); zeichne(); }
      else if (ev.key === "ArrowDown") { vorschauSt = Math.max(MIN, vorschauSt - 1); ev.preventDefault(); zeichne(); }
      else if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); setzen(vorschauSt); }
      else if (ev.key === "Backspace") { ev.preventDefault(); zurueck.click(); }
    });
    buehne.addEventListener("focus", zeichne); buehne.addEventListener("blur", zeichne);
    zeichne();
    return {
      el: huelle, gesetzt: function () { return gesetzt; }, voll: function () { return gesetzt.length >= opts.max; },
      sperren: function (b) { gesperrt = b; zeichne(); },
      markieren: function (m) { markierung = m; zeichne(); },
      loesung: function (l) { loesung = l; zeichne(); },
      neu: zeichne
    };
  }

  /* ---------------------------------------------------------
     Übung: Notieren
     --------------------------------------------------------- */
  function notieren(box, daten) {
    var systeme = [];
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" }), hinweis = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    var k;
    daten.aufgaben.forEach(function (a, nr) {
      var karte = el("div", { class: "notier-karte" });
      karte.appendChild(el("p", { class: "frage", text: (nr + 1) + ". " + a.frage }));
      var ergebnis = el("p", { class: "notier-ergebnis", "aria-live": "polite" });
      var sys = klickSystem({ schluessel: daten.schluessel || a.schluessel, vorgabe: a.vorgabe || [], akkord: !!a.akkord, max: a.ziel.length, vorzeichen: !!daten.vorzeichen, onAenderung: function () { ergebnis.textContent = ""; aktual(); } });
      sys.ziel = a.ziel; sys.ergebnis = ergebnis; sys.akkord = !!a.akkord; sys.vorgabe = a.vorgabe || [];
      karte.appendChild(sys.el); karte.appendChild(ergebnis);
      box.appendChild(karte); systeme.push(sys);
    });
    k = knopfreihe(pruefen, loesung, function () { box.innerHTML = ""; notieren(box, daten); });
    box.appendChild(k.reihe); box.appendChild(hinweis); box.appendChild(rueck);
    function offen() { return systeme.filter(function (s) { return !s.voll(); }).length; }
    function aktual() { sperre([k.pruefen, k.loesung], hinweis, offen, "Aufgabe", "Aufgaben"); }
    aktual();
    function bewerte(s) {
      var g = s.gesetzt();
      if (s.akkord) {
        var soll = s.ziel.slice().sort(), ist = g.slice().sort();
        var ok = soll.every(function (t, i) { return t === ist[i]; });
        return { ok: ok, einzeln: null };
      }
      var einzeln = g.map(function (t, i) { return t === s.ziel[i]; });
      return { ok: einzeln.every(Boolean), einzeln: einzeln };
    }
    function pruefen() {
      if (offen()) return;
      var n = 0;
      systeme.forEach(function (s) {
        var b = bewerte(s); if (b.ok) n++;
        if (b.einzeln) s.markieren(b.einzeln);
        s.ergebnis.className = "notier-ergebnis " + (b.ok ? "gut" : "schlecht");
        s.ergebnis.textContent = b.ok ? "Richtig!" : "Noch nicht richtig" + (b.einzeln ? " – falsche Töne sind rot markiert." : ".");
      });
      rueckmeldung(rueck, n, systeme.length);
    }
    function loesung() {
      if (offen()) return;
      pruefen();
      systeme.forEach(function (s) {
        if (bewerte(s).ok) return;
        s.loesung(s.ziel);
        s.ergebnis.textContent = "Richtig wäre: " + s.vorgabe.concat(s.ziel).map(function (t) { return tonname(t, true); }).join(" – ");
      });
    }
  }

  /* ---------------------------------------------------------
     Übung: Halbtöne markieren
     --------------------------------------------------------- */
  function halbtoene(box, daten) {
    var karten = [];
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" }), hinweis = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    daten.aufgaben.forEach(function (a, nr) {
      var r = noten(a.noten, Object.assign({ zoom: 1.9 }, a.spec || {}));
      var karte = el("div", { class: "lese-karte" });
      karte.appendChild(el("p", { class: "frage", text: (nr + 1) + ". " + a.frage }));
      var buehne = el("div", { class: "lese-buehne ht-buehne" });
      buehne.appendChild(svgElement(r.svg));
      var luecken = [];
      for (var i = 0; i < r.noten.length - 1; i++) {
        var x = (r.noten[i].mitteX + r.noten[i + 1].mitteX) / 2 / r.breite * 100;
        var b = el("button", { type: "button", class: "ht-knopf", "aria-pressed": "false", "aria-label": "Halbton zwischen Note " + (i + 1) + " und " + (i + 2), text: "?" });
        b.style.left = x + "%";
        (function (b) { b.addEventListener("click", function () { var an = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", an ? "true" : "false"); b.textContent = an ? "½" : "?"; b.classList.remove("ist-richtig", "ist-falsch"); aktual(); }); })(b);
        buehne.appendChild(b); luecken.push(b);
      }
      karte.appendChild(buehne);
      karte.appendChild(spielKnopf(a.noten.replace(/\/1/g, "/4"), {}, "Tonleiter anhören"));
      box.appendChild(karte);
      karten.push({ luecken: luecken, loesung: a.loesung });
    });
    var k = knopfreihe(pruefen, loesung, function () { box.innerHTML = ""; halbtoene(box, daten); });
    box.appendChild(k.reihe); box.appendChild(hinweis); box.appendChild(rueck);
    function offen() { return karten.filter(function (c) { return c.luecken.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; }).length !== c.loesung.length; }).length; }
    function aktual() {
      sperre([k.pruefen, k.loesung], hinweis, offen, "Tonleiter", "Tonleitern");
      if (offen()) hinweis.textContent += " Markiere in jeder Tonleiter genau zwei Halbtöne.";
    }
    aktual();
    function pruefen() {
      if (offen()) return;
      var n = 0;
      karten.forEach(function (c) {
        var ok = true;
        c.luecken.forEach(function (b, i) {
          var an = b.getAttribute("aria-pressed") === "true", soll = c.loesung.indexOf(i) >= 0;
          if (an) { b.classList.toggle("ist-richtig", soll); b.classList.toggle("ist-falsch", !soll); }
          if (an !== soll) ok = false;
        });
        if (ok) n++;
      });
      rueckmeldung(rueck, n, karten.length);
    }
    function loesung() {
      if (offen()) return;
      pruefen();
      karten.forEach(function (c) { c.luecken.forEach(function (b, i) { if (c.loesung.indexOf(i) >= 0 && b.getAttribute("aria-pressed") !== "true") { b.classList.add("ist-loesung"); b.textContent = "½"; } }); });
      rueck.appendChild(document.createTextNode(" Fehlende Halbtöne sind jetzt grün umrandet."));
    }
  }


  /* ---------------------------------------------------------
     Übung: Taktstriche setzen
     --------------------------------------------------------- */
  function taktstriche(box, daten) {
    var karten = [];
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" }), hinweis = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    daten.aufgaben.forEach(function (a, nr) {
      var r = noten(a.noten + " |.", { rhythmus: true, takt: a.takt, zoom: 2 });
      var n = a.loesung.length;
      var karte = el("div", { class: "lese-karte" });
      karte.appendChild(el("p", { class: "frage", text: (nr + 1) + ". " + a.takt + "-Takt: Setze die " + n + " fehlenden Taktstriche." }));
      var buehne = el("div", { class: "lese-buehne ts-buehne" });
      buehne.appendChild(svgElement(r.svg));
      var mitteY = ((r.y0 + 2 * N.SP) - r.top) / r.hoehe * 100;
      var luecken = [];
      for (var i = 0; i < r.noten.length - 1; i++) {
        var x = (r.noten[i].mitteX + r.noten[i + 1].mitteX) / 2 / r.breite * 100;
        var b = el("button", { type: "button", class: "ts-knopf", "aria-pressed": "false", "aria-label": "Taktstrich zwischen Note " + (i + 1) + " und " + (i + 2) });
        b.style.left = x + "%"; b.style.top = mitteY + "%";
        (function (b) { b.addEventListener("click", function () { b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true"); b.classList.remove("ist-richtig", "ist-falsch", "ist-loesung"); aktual(); }); })(b);
        buehne.appendChild(b); luecken.push(b);
      }
      karte.appendChild(buehne);
      karte.appendChild(spielKnopf(a.noten, { rhythmus: true }, "Rhythmus anhören"));
      box.appendChild(karte);
      karten.push({ luecken: luecken, loesung: a.loesung });
    });
    var k = knopfreihe(pruefen, loesung, function () { box.innerHTML = ""; taktstriche(box, daten); });
    box.appendChild(k.reihe); box.appendChild(hinweis); box.appendChild(rueck);
    function an(c) { return c.luecken.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; }).length; }
    function offen() { return karten.filter(function (c) { return an(c) !== c.loesung.length; }).length; }
    function aktual() {
      sperre([k.pruefen, k.loesung], hinweis, offen, "Aufgabe", "Aufgaben");
      if (offen()) hinweis.textContent += " Setze in jeder Aufgabe genau so viele Taktstriche, wie angegeben.";
    }
    aktual();
    function pruefen() {
      if (offen()) return;
      var n = 0;
      karten.forEach(function (c) {
        var ok = true;
        c.luecken.forEach(function (b, i) {
          var gesetzt = b.getAttribute("aria-pressed") === "true", soll = c.loesung.indexOf(i) >= 0;
          if (gesetzt) { b.classList.toggle("ist-richtig", soll); b.classList.toggle("ist-falsch", !soll); }
          if (gesetzt !== soll) ok = false;
        });
        if (ok) n++;
      });
      rueckmeldung(rueck, n, karten.length);
    }
    function loesung() {
      if (offen()) return;
      pruefen();
      karten.forEach(function (c) { c.luecken.forEach(function (b, i) { if (c.loesung.indexOf(i) >= 0 && b.getAttribute("aria-pressed") !== "true") b.classList.add("ist-loesung"); }); });
      rueck.appendChild(document.createTextNode(" Fehlende Taktstriche sind jetzt grün gestrichelt eingezeichnet."));
    }
  }

  /* =========================================================
     Werkzeug: Klaviatur
     ========================================================= */
  function klaviatur(box) {
    var modus = "toene", auswahl = [], VON = 48 + 12, BIS = 84;   // c′ bis c‴
    var tabs = el("div", { class: "wahl", role: "group", "aria-label": "Modus" });
    var erlaubt = (box.getAttribute("data-modi") || "").split(",").filter(Boolean);
    [["toene", "Töne"], ["intervall", "Intervalle"], ["leiter", "Tonleitern und Dreiklänge"]].filter(function (m) { return !erlaubt.length || erlaubt.indexOf(m[0]) >= 0; }).forEach(function (m) {
      var b = el("button", { type: "button", "aria-pressed": m[0] === modus ? "true" : "false", text: m[1] });
      b.addEventListener("click", function () { modus = m[0]; auswahl = []; Array.prototype.forEach.call(tabs.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); leiterBox.hidden = modus !== "leiter"; zeichne(); });
      tabs.appendChild(b);
    });
    if (tabs.children.length < 2) tabs.hidden = true;
    var leiterBox = el("div", { class: "modell-steuerung", hidden: "" });
    var grund = el("select", { "aria-label": "Grundton" });
    [["C4", "c"], ["D4", "d"], ["E4", "e"], ["F4", "f"], ["G4", "g"], ["A4", "a"], ["B4", "h"], ["Bb4", "b"], ["Eb4", "es"], ["F#4", "fis"], ["C#4", "cis"], ["Ab4", "as"]].forEach(function (g) { grund.appendChild(el("option", { value: g[0], text: g[1] })); });
    var art = el("select", { "aria-label": "Art" });
    ["Dur-Tonleiter", "Moll-Tonleiter (natürlich)", "Moll-Tonleiter (harmonisch)", "Dur-Dreiklang", "Moll-Dreiklang", "verminderter Dreiklang", "übermäßiger Dreiklang"].forEach(function (a) { art.appendChild(el("option", { text: a })); });
    var spielL = el("button", { class: "knopf", type: "button", text: "▶ Abspielen" });
    leiterBox.appendChild(el("label", { text: "Grundton " }, [grund])); leiterBox.appendChild(el("label", { text: " Art " }, [art])); leiterBox.appendChild(spielL);
    var tasten = el("div", { class: "tasten", role: "group", "aria-label": "Klaviatur" });
    var staff = el("div", { class: "klav-noten" }), info = el("div", { class: "schritt-text", "aria-live": "polite" });
    box.appendChild(tabs); box.appendChild(leiterBox); box.appendChild(tasten); box.appendChild(staff); box.appendChild(info);
    var WEISS = [0, 2, 4, 5, 7, 9, 11], NAMEN_K = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "h"], NAMEN_B = ["c", "des", "d", "es", "e", "f", "ges", "g", "as", "a", "b", "h"];
    var knoepfe = {};
    var wi = 0;
    for (var m = VON; m <= BIS; m++) {
      var pc = m % 12, w = WEISS.indexOf(pc) >= 0;
      var b = el("button", { type: "button", class: "taste " + (w ? "weiss" : "schwarz"), "aria-label": (w ? NAMEN_K[pc] : NAMEN_K[pc] + " oder " + NAMEN_B[pc]) + " (" + (m < 72 ? "eingestrichen" : m < 84 ? "zweigestrichen" : "dreigestrichen") + ")" });
      if (w) { b.style.left = (wi * 100 / 15) + "%"; wi++; b.appendChild(el("span", { text: NAMEN_K[pc] })); }
      else b.style.left = (wi * 100 / 15 - 100 / 15 * 0.3) + "%";
      (function (m) { b.addEventListener("click", function () { druecke(m); }); })(m);
      tasten.appendChild(b); knoepfe[m] = b;
    }
    function tonVon(m, b) {
      var o = Math.floor(m / 12) - 1, pc = m % 12;
      var stamm = b ? ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"][pc] : ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][pc];
      return stamm + o;
    }
    function druecke(m) {
      ton(m, 0, 0.9);
      if (modus === "toene") auswahl = [m];
      else if (modus === "intervall") { auswahl.push(m); if (auswahl.length > 2) auswahl = [m]; if (auswahl.length === 2) { auswahl.sort(function (a, b) { return a - b; }); ton(auswahl[0], 0.5, 0.8); ton(auswahl[1], 0.5, 0.8); } }
      else auswahl = [m];
      zeichne();
    }
    function zeichne() {
      Object.keys(knoepfe).forEach(function (k) { knoepfe[k].classList.toggle("an", auswahl.indexOf(+k) >= 0); });
      info.innerHTML = "";
      if (modus === "toene") {
        if (!auswahl.length) { staff.innerHTML = ""; info.appendChild(el("p", { text: "Tippe auf eine Taste. Du siehst die Note und ihren Namen." })); return; }
        var m = auswahl[0], pc = m % 12, schwarz = WEISS.indexOf(pc) < 0;
        var t1 = tonVon(m, false), t2 = tonVon(m, true);
        staff.innerHTML = noten(schwarz ? t1 + "/1@" + tonname(t1, true) + " " + t2 + "/1@" + tonname(t2, true) : t1 + "/1@" + tonname(t1, true), { zoom: 2 }).svg;
        info.appendChild(el("p", { text: schwarz ? "Schwarze Taste: Sie hat zwei Namen, " + tonname(t1, true) + " (mit Kreuz) oder " + tonname(t2, true) + " (mit b)." : "Weiße Taste: der Stammton " + tonname(t1, true) + "." }));
      } else if (modus === "intervall") {
        if (auswahl.length < 2) { staff.innerHTML = auswahl.length ? noten(tonVon(auswahl[0]) + "/1", { zoom: 2 }).svg : ""; info.appendChild(el("p", { text: auswahl.length ? "Tippe jetzt auf eine zweite Taste." : "Tippe nacheinander auf zwei Tasten. Du siehst, wie viele Halbtöne dazwischen liegen." })); return; }
        var a = tonVon(auswahl[0]), h = auswahl[1] - auswahl[0];
        // passenden zweiten Ton mit sinnvoller Schreibweise suchen
        var namen = [];
        for (var d = 0; d <= 7; d++) { var t = tonAus(stufeVon(a) + d, auswahl[1]); if (t && intervall(a, t)) namen.push({ t: t, n: intervall(a, t) }); }
        if (!namen.length) namen.push({ t: tonVon(auswahl[1]), n: "" });
        staff.innerHTML = noten("[" + a + " " + namen[0].t + "]/1 _ " + a + "/2 " + namen[0].t + "/2", { zoom: 2 }).svg;
        info.appendChild(el("p", { html: "<strong>" + h + " Halbtöne</strong>" + (namen[0].n ? ": " + namen.map(function (x) { return x.n + " (" + tonname(a) + " – " + tonname(x.t) + ")"; }).join(" oder ") : "") }));
      } else {
        var g = grund.value, artW = art.value, toene;
        if (/Tonleiter/.test(artW)) toene = tonleiter(g, /harmonisch/.test(artW) ? MOLL_H : /Moll/.test(artW) ? MOLL : DUR);
        else toene = dreiklang(g, artW.split(/[- ]/)[0].replace("verminderter", "vermindert").replace("übermäßiger", "übermäßig"));
        auswahl = toene.map(midi);
        Object.keys(knoepfe).forEach(function (k) { knoepfe[k].classList.toggle("an", auswahl.indexOf(+k) >= 0); });
        var txt = /Tonleiter/.test(artW) ? toene.map(function (t, i) { return (i ? (midi(t) - midi(toene[i - 1]) === 1 ? "{HT} " : midi(t) - midi(toene[i - 1]) === 2 ? "{GT} " : "{1½} ") : "") + t + "/1@" + tonname(t); }).join(" ")
          : "[" + toene.join(" ") + "]/1 _ " + toene.map(function (t) { return t + "/2@" + tonname(t); }).join(" ");
        staff.innerHTML = noten(txt, { zoom: 1.7 }).svg;
        info.appendChild(el("p", { text: toene.map(function (t) { return tonname(t); }).join(" – ") }));
      }
    }
    function spielAuswahl() {
      var artW = art.value;
      zeichne();
      var toene = auswahl.map(function (m) { return m; });
      if (/Tonleiter/.test(artW)) toene.forEach(function (m, i) { ton(m, i * 0.42, 0.5); });
      else { toene.forEach(function (m, i) { ton(m, i * 0.45, 0.5); }); toene.forEach(function (m) { ton(m, toene.length * 0.45, 1.4); }); }
    }
    spielL.addEventListener("click", spielAuswahl);
    grund.addEventListener("change", zeichne); art.addEventListener("change", zeichne);
    zeichne();
  }

  /* =========================================================
     Werkzeug: Quintenzirkel
     ========================================================= */
  function quintenzirkel(box) {
    var KREIS = [0, 1, 2, 3, 4, 5, 6, -5, -4, -3, -2, -1], aktiv = 0, moll = false;
    var flaeche = el("div", { class: "qz-flaeche" });
    var schalter = el("div", { class: "wahl", role: "group", "aria-label": "Dur oder Moll" });
    [["Dur", false], ["Moll", true]].forEach(function (d) {
      var b = el("button", { type: "button", "aria-pressed": d[1] === moll ? "true" : "false", text: d[0] });
      b.addEventListener("click", function () { moll = d[1]; Array.prototype.forEach.call(schalter.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); zeichne(); });
      schalter.appendChild(b);
    });
    var details = el("div", { class: "qz-details", "aria-live": "polite" });
    box.appendChild(schalter); box.appendChild(flaeche); box.appendChild(details);
    function sektor(cx, cy, r1, r2, a1, a2) {
      function p(r, a) { var w = (a - 90) * Math.PI / 180; return (cx + Math.cos(w) * r).toFixed(1) + " " + (cy + Math.sin(w) * r).toFixed(1); }
      return "M" + p(r1, a1) + " A" + r1 + " " + r1 + " 0 0 1 " + p(r1, a2) + " L" + p(r2, a2) + " A" + r2 + " " + r2 + " 0 0 0 " + p(r2, a1) + "Z";
    }
    function zeichne() {
      var cx = 230, cy = 230, s = '<svg class="ill qz" viewBox="0 0 460 460" role="group" aria-label="Quintenzirkel">';
      KREIS.forEach(function (vz, k) {
        var a1 = k * 30 - 15, a2 = k * 30 + 15, w = (k * 30 - 90) * Math.PI / 180;
        var ta = TONARTEN[String(vz)], nachbar = Math.abs(KREIS.indexOf(aktiv) - k) === 1 || Math.abs(KREIS.indexOf(aktiv) - k) === 11;
        var kl = vz === aktiv ? "qz-sektor aktiv" : nachbar ? "qz-sektor nachbar" : "qz-sektor";
        s += '<g class="' + kl + '" data-vz="' + vz + '" tabindex="0" role="button" aria-label="' + (vz === 6 ? "Fis-Dur / Ges-Dur, dis-Moll / es-Moll" : ta[0] + ", " + ta[1]) + '">';
        s += '<path class="s2 qz-aussen" d="' + sektor(cx, cy, 210, 140, a1, a2) + '"/><path class="s2 qz-innen" d="' + sektor(cx, cy, 140, 82, a1, a2) + '"/>';
        var dur = vz === 6 ? "Fis/Ges" : ta[0].replace("-Dur", ""), mo = vz === 6 ? "dis/es" : ta[1].replace("-Moll", "");
        s += '<text class="h qz-t" x="' + (cx + Math.cos(w) * 175).toFixed(1) + '" y="' + (cy + Math.sin(w) * 175 + 2).toFixed(1) + '" text-anchor="middle">' + dur + "</text>";
        s += '<text class="hk qz-vz" x="' + (cx + Math.cos(w) * 175).toFixed(1) + '" y="' + (cy + Math.sin(w) * 175 + 22).toFixed(1) + '" text-anchor="middle">' + (vz === 0 ? "–" : vz === 6 ? "6♯/6♭" : Math.abs(vz) + (vz > 0 ? "♯" : "♭")) + "</text>";
        s += '<text class="hk qz-m" x="' + (cx + Math.cos(w) * 111).toFixed(1) + '" y="' + (cy + Math.sin(w) * 111 + 6).toFixed(1) + '" text-anchor="middle">' + mo + "</text></g>";
      });
      s += '<circle class="s2 f-papier" cx="' + cx + '" cy="' + cy + '" r="82"/><text class="h" x="' + cx + '" y="' + (cy - 4) + '" text-anchor="middle">' + (moll ? TONARTEN[String(aktiv)][1] : TONARTEN[String(aktiv)][0]) + '</text><text class="hk" x="' + cx + '" y="' + (cy + 22) + '" text-anchor="middle">antippen zum Wechseln</text></svg>';
      flaeche.innerHTML = s;
      flaeche.querySelectorAll(".qz-sektor").forEach(function (g) {
        function w() { aktiv = +g.getAttribute("data-vz"); zeichne(); var f = flaeche.querySelector('.qz-sektor[data-vz="' + aktiv + '"]'); if (f) f.focus(); }
        g.addEventListener("click", w);
        g.addEventListener("keydown", function (ev) {
          if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); w(); }
          if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") { ev.preventDefault(); var i = KREIS.indexOf(aktiv); aktiv = KREIS[(i + (ev.key === "ArrowRight" ? 1 : 11)) % 12]; zeichne(); flaeche.querySelector('.qz-sektor[data-vz="' + aktiv + '"]').focus(); }
        });
      });
      details.innerHTML = "";
      var ta = TONARTEN[String(aktiv)], g = ta[2];
      if (moll) g = tonAus(stufeVon(g) - 2, midi(g) - 3);
      var leiter = tonleiter(g, moll ? MOLL : DUR);
      var vzListe = aktiv > 0 ? ["fis", "cis", "gis", "dis", "ais", "eis"].slice(0, aktiv) : ["b", "es", "as", "des", "ges", "ces"].slice(0, -aktiv);
      details.appendChild(el("h3", { text: moll ? ta[1] + " (parallel zu " + ta[0] + ")" : ta[0] + " (parallel: " + ta[1] + ")" }));
      details.appendChild(el("p", { text: aktiv === 0 ? "Keine Vorzeichen." : "Vorzeichen: " + vzListe.join(", ") + (aktiv === 6 ? " – enharmonisch gleich: Ges-Dur mit 6 b (b, es, as, des, ges, ces)" : "") }));
      details.appendChild(el("div", { class: "qz-noten", html: noten(leiter.map(function (t) { return t.replace(/^([A-G])[#b]/, "$1") + "/4"; }).join(" "), { tonart: aktiv, zoom: 1.6 }).svg }));
      var txt = leiter.map(function (t) { return t + "/4"; }).join(" ");
      details.appendChild(el("div", { class: "knopfreihe" }, [spielKnopf(txt, { tonart: 0 }, "Tonleiter anhören")]));
      // Hauptdreiklänge
      var stufen = moll ? [["t", 0, "Moll"], ["s", 3, "Moll"], ["d", 4, "Moll"]] : [["T", 0, "Dur"], ["S", 3, "Dur"], ["D", 4, "Dur"]];
      var ak = stufen.map(function (x) { return { n: x[0], t: dreiklang(leiter[x[1]], x[2]) }; });
      details.appendChild(el("p", { html: "<strong>Hauptdreiklänge:</strong> " + ak.map(function (a) { var n = tonname(a.t[0]); return a.n + " = " + (moll ? n : n.charAt(0).toUpperCase() + n.slice(1)) + (moll ? "-Moll" : "-Dur"); }).join(", ") + ". Subdominante und Dominante sind die Nachbarn im Kreis." }));
      var akText = ak.map(function (a) { return "[" + a.t.join(" ") + "]/2@" + a.n; }).join(" ") + " [" + ak[0].t.join(" ") + "]/2@" + ak[0].n;
      details.appendChild(el("div", { class: "qz-noten", html: noten(akText, { zoom: 1.6 }).svg }));
      details.appendChild(el("div", { class: "knopfreihe" }, [spielKnopf(akText.replace(/@\w/g, ""), {}, "Kadenz anhören")]));
    }
    zeichne();
  }

  /* =========================================================
     Werkzeug: Taktbaukasten
     ========================================================= */
  function taktbaukasten(box) {
    var TAKTE = { "2/4": 8, "3/4": 12, "4/4": 16, "6/8": 12 };   // in Sechzehnteln
    var takt = "4/4", folge = [], maxTakte = 4;
    var BAUSTEINE = [
      { t: "C4/1", w: 16, n: "ganze Note" }, { t: "C4/2.", w: 12, n: "punktierte Halbe" }, { t: "C4/2", w: 8, n: "halbe Note" }, { t: "C4/4.", w: 6, n: "punktierte Viertel" },
      { t: "C4/4", w: 4, n: "Viertel" }, { t: "C4/8.", w: 3, n: "punktierte Achtel" }, { t: "C4/8", w: 2, n: "Achtel" }, { t: "C4/16", w: 1, n: "Sechzehntel" },
      { t: "3( C4/8 C4/8 C4/8 )", w: 4, n: "Achteltriole" },
      { t: "R/1", w: 16, n: "ganze Pause" }, { t: "R/2", w: 8, n: "halbe Pause" }, { t: "R/4", w: 4, n: "Viertelpause" }, { t: "R/8", w: 2, n: "Achtelpause" }, { t: "R/16", w: 1, n: "Sechzehntelpause" }
    ];
    var wahl = el("div", { class: "wahl", role: "group", "aria-label": "Taktart" });
    Object.keys(TAKTE).forEach(function (t) {
      var b = el("button", { type: "button", "aria-pressed": t === takt ? "true" : "false", text: t + "-Takt" });
      b.addEventListener("click", function () { takt = t; folge = []; Array.prototype.forEach.call(wahl.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); zeichne(); });
      wahl.appendChild(b);
    });
    var palette = el("div", { class: "palette", role: "group", "aria-label": "Notenwerte und Pausen" });
    BAUSTEINE.forEach(function (b) {
      var k = el("button", { type: "button", class: "baustein", title: b.n, "aria-label": b.n + " hinzufügen", html: noten(b.t, b.t[0] === "R" ? { schluessel: false, oben: 4, unten: 1, zoom: 1.2 } : { rhythmus: true, zoom: 1.2 }).svg });
      k.addEventListener("click", function () { hinzu(b); });
      palette.appendChild(k);
    });
    var bild = el("div", { class: "takt-bild" }), status = el("p", { class: "vh-zahl", "aria-live": "polite" });
    var steuer = el("div", { class: "knopfreihe" }, [
      el("button", { class: "knopf", type: "button", text: "▶ Abspielen", onclick: abspielen }),
      el("button", { class: "knopf leise", type: "button", text: "↶ Zurück", onclick: function () { folge.pop(); zeichne(); } }),
      el("button", { class: "knopf leise", type: "button", text: "Alles löschen", onclick: function () { folge = []; zeichne(); } })
    ]);
    var metro = el("label", { class: "schalter" }, [el("input", { type: "checkbox", checked: "" }), document.createTextNode(" Metronom mitklicken")]);
    box.appendChild(wahl); box.appendChild(palette); box.appendChild(bild); box.appendChild(status); box.appendChild(steuer); box.appendChild(metro);
    function belegt() { var s = 0; folge.forEach(function (b) { s += b.w; }); return s; }
    function hinzu(b) {
      var L = TAKTE[takt], s = belegt(), imTakt = s % L, frei = L - imTakt;
      if (s >= L * maxTakte) { status.textContent = "Es sind schon " + maxTakte + " Takte voll. Lösche etwas oder starte neu."; return; }
      if (b.w > frei) { status.textContent = "„" + b.n + "“ passt nicht mehr in diesen Takt: Es ist nur noch Platz für " + platzText(frei) + "."; return; }
      folge.push(b); zeichne();
    }
    function platzText(w) {
      var t = { 1: "eine Sechzehntel", 2: "eine Achtel", 3: "eine punktierte Achtel", 4: "eine Viertel", 6: "eine punktierte Viertel", 8: "eine Halbe", 12: "eine punktierte Halbe", 16: "eine Ganze" }[w];
      return t || w + " Sechzehntel";
    }
    function text() {
      var L = TAKTE[takt], s = 0, teile = [];
      folge.forEach(function (b) { teile.push(b.t); s += b.w; if (s % L === 0) teile.push(s === L * maxTakte ? "|." : "|"); });
      return teile.join(" ");
    }
    function zeichne() {
      var L = TAKTE[takt], s = belegt();
      bild.innerHTML = noten(text() || "_", { rhythmus: true, takt: takt, zoom: 1.7, breite: 200 }).svg;
      if (!folge.length) { status.textContent = "Tippe auf Notenwerte und Pausen, um Takte zu bauen."; return; }
      var imTakt = s % L, nr = Math.floor(s / L) + (imTakt ? 1 : 0);
      status.textContent = imTakt === 0 ? (nr + (nr === 1 ? " Takt" : " Takte") + " fertig." + (s < L * maxTakte ? " Weiter geht’s mit dem nächsten Takt." : "")) :
        "Takt " + nr + ": noch Platz für " + platzText(L - imTakt) + ".";
    }
    function abspielen() {
      var t = text(); if (!t) return;
      var dauer = spiele(t, { rhythmus: true, tempo: 92 });
      if (metro.querySelector("input").checked) {
        var schlag = takt === "6/8" ? 60 / 92 / 2 : 60 / 92, n = Math.ceil(dauer / schlag), proTakt = takt === "6/8" ? 6 : +takt[0];
        for (var i = 0; i < n; i++) klick(0.05 + i * schlag, i % proTakt === 0);
      }
    }
    zeichne();
  }

  /* =========================================================
     Werkzeug: Notentrainer
     ========================================================= */
  function notentrainer(box) {
    var MODI = {
      stamm: "Stammtöne c′ bis a″", bass: "Bassschlüssel", vorzeichen: "Töne mit Vorzeichen", intervall: "Intervalle", tonart: "Tonarten an den Vorzeichen", dreiklang: "Dreiklänge"
    };
    var erlaubt = (box.getAttribute("data-modi") || "").split(",").filter(Boolean);
    if (erlaubt.length) Object.keys(MODI).forEach(function (m) { if (erlaubt.indexOf(m) < 0) delete MODI[m]; });
    var modus = Object.keys(MODI)[0], nr = 0, richtig = 0, RUNDE = 10, aktuell = null;
    var wahl = el("div", { class: "wahl", role: "group", "aria-label": "Was möchtest du üben?" });
    Object.keys(MODI).forEach(function (m) {
      var b = el("button", { type: "button", "aria-pressed": m === modus ? "true" : "false", text: MODI[m] });
      b.addEventListener("click", function () { modus = m; Array.prototype.forEach.call(wahl.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); start(); });
      wahl.appendChild(b);
    });
    var bild = el("div", { class: "trainer-bild" }), frage = el("p", { class: "frage" }), antworten = el("div", { class: "optionen trainer-optionen" });
    var rueck = el("p", { class: "erklaerung", "aria-live": "polite" }), stand = el("p", { class: "vh-zahl", "aria-live": "polite" });
    var weiter = el("button", { class: "knopf", type: "button", text: "Nächste Aufgabe", onclick: naechste });
    var hoer = el("button", { class: "knopf leise", type: "button", text: "▶ Anhören", onclick: function () { if (aktuell) spiele(aktuell.spiel, { tonart: aktuell.tonart || 0 }); } });
    box.appendChild(wahl); box.appendChild(stand); box.appendChild(frage); box.appendChild(bild); box.appendChild(el("div", { class: "knopfreihe" }, [hoer])); box.appendChild(antworten); box.appendChild(rueck); box.appendChild(el("div", { class: "knopfreihe" }, [weiter]));
    var STAMMT = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5"];
    var VZT = ["C#4", "D#4", "F#4", "G#4", "A#4", "C#5", "D#5", "F#5", "G#5", "Db4", "Eb4", "Gb4", "Ab4", "Bb4", "Db5", "Eb5", "Gb5", "Ab5"];
    function erzeuge() {
      if (modus === "bass") {
        var tb = zufall(["C2", "D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]);
        return { frage: "Wie heißt dieser Ton im Bassschlüssel?", noten: tb + "/1", spec: { schluessel: "bass" }, spiel: tb + "/2", richtig: tonname(tb), optionen: ["c", "d", "e", "f", "g", "a", "h"], erkl: "Das ist " + tonname(tb, true) + "." };
      }
      if (modus === "stamm" || modus === "vorzeichen") {
        var t = zufall(modus === "stamm" ? STAMMT : VZT), n = tonname(t);
        var pool = modus === "stamm" ? ["c", "d", "e", "f", "g", "a", "h"] : ["cis", "dis", "fis", "gis", "ais", "des", "es", "ges", "as", "b"];
        return { frage: "Wie heißt dieser Ton?", noten: t + "/1", spiel: t + "/2", richtig: n, optionen: pool, erkl: "Das ist " + tonname(t, true) + "." };
      }
      if (modus === "intervall") {
        var ivs = ["kleine Sekunde", "große Sekunde", "kleine Terz", "große Terz", "reine Quarte", "reine Quinte", "kleine Sexte", "große Sexte", "kleine Septime", "große Septime", "reine Oktave"];
        var a, b, name, versuche = 0;
        do {
          a = zufall(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5"]); name = zufall(ivs);
          var halb = { "kleine Sekunde": [1, 1], "große Sekunde": [1, 2], "kleine Terz": [2, 3], "große Terz": [2, 4], "reine Quarte": [3, 5], "reine Quinte": [4, 7], "kleine Sexte": [5, 8], "große Sexte": [5, 9], "kleine Septime": [6, 10], "große Septime": [6, 11], "reine Oktave": [7, 12] }[name];
          b = tonAus(stufeVon(a) + halb[0], midi(a) + halb[1]); versuche++;
        } while ((!b || stufeVon(b) > 41) && versuche < 50);
        return { frage: "Welches Intervall ist das?", noten: "[" + a + " " + b + "]/1", spiel: a + "/2 " + b + "/2 [" + a + " " + b + "]/1", richtig: name, optionen: ivs, erkl: tonname(a, true) + " – " + tonname(b, true) + ": " + name + " (" + (midi(b) - midi(a)) + " Halbtöne)." };
      }
      if (modus === "tonart") {
        var vz = zufall([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]), ta = TONARTEN[String(vz)];
        return { frage: "Welche Dur-Tonart hat diese Vorzeichen?", noten: "", spec: { tonart: vz, breite: 130 }, spiel: tonleiter(ta[2], DUR).map(function (t) { return t + "/8"; }).join(" "), richtig: ta[0],
          optionen: ["C-Dur", "G-Dur", "D-Dur", "A-Dur", "E-Dur", "H-Dur", "Fis-Dur", "F-Dur", "B-Dur", "Es-Dur", "As-Dur", "Des-Dur"], erkl: ta[0] + " (parallel: " + ta[1] + ")." };
      }
      var g = zufall(["C4", "D4", "E4", "F4", "G4", "A4", "B4"]), art = zufall(["Dur", "Moll", "Dur", "Moll", "vermindert", "übermäßig"]), dk = dreiklang(g, art);
      if (dk.some(function (t) { return !t; })) return erzeuge();
      return { frage: "Welcher Dreiklang ist das?", noten: "[" + dk.join(" ") + "]/1", spiel: dk.map(function (t) { return t + "/4"; }).join(" ") + " [" + dk.join(" ") + "]/1", richtig: art, optionen: ["Dur", "Moll", "vermindert", "übermäßig"], erkl: dk.map(function (t) { return tonname(t); }).join(" – ") + ": " + art + "." };
    }
    function start() { nr = 0; richtig = 0; naechste(); }
    function naechste() {
      if (nr >= RUNDE) {
        stand.textContent = "Runde beendet: " + richtig + " von " + RUNDE + " richtig. " + lob(richtig / RUNDE);
        frage.textContent = ""; bild.innerHTML = ""; antworten.innerHTML = ""; rueck.textContent = ""; weiter.textContent = "Neue Runde"; weiter.onclick = function () { weiter.onclick = null; weiter.textContent = "Nächste Aufgabe"; start(); };
        return;
      }
      weiter.onclick = null;
      nr++; aktuell = erzeuge(); rueck.textContent = ""; rueck.className = "erklaerung";
      stand.textContent = "Aufgabe " + nr + " von " + RUNDE + " · " + richtig + " richtig";
      frage.textContent = aktuell.frage;
      bild.innerHTML = noten(aktuell.noten, Object.assign({ zoom: 2.2 }, aktuell.spec || {})).svg;
      antworten.innerHTML = ""; weiter.disabled = true;
      aktuell.optionen.forEach(function (o) {
        var b = el("button", { type: "button", class: "option", text: o });
        b.addEventListener("click", function () {
          Array.prototype.forEach.call(antworten.children, function (k) { k.disabled = true; if (k.textContent === aktuell.richtig) k.classList.add("ist-richtig"); });
          var ok = o === aktuell.richtig; if (!ok) b.classList.add("ist-falsch"); else richtig++;
          rueck.textContent = (ok ? "Richtig! " : "Leider falsch. ") + aktuell.erkl; rueck.className = "erklaerung " + (ok ? "gut" : "schlecht");
          stand.textContent = "Aufgabe " + nr + " von " + RUNDE + " · " + richtig + " richtig";
          weiter.disabled = false; weiter.focus();
        });
        antworten.appendChild(b);
      });
    }
    start();
  }

  /* ---------------------------------------------------------
     Start
     --------------------------------------------------------- */
  var TYPEN = { notenquiz: notenquiz, notenlesen: notenlesen, notieren: notieren, halbtoene: halbtoene, taktstriche: taktstriche };
  var WERKZEUGE = { klaviatur: klaviatur, quintenzirkel: quintenzirkel, taktbaukasten: taktbaukasten, notentrainer: notentrainer };
  function start() {
    notenbeispiele();
    document.querySelectorAll(".uebung[data-typ]").forEach(function (box) {
      var typ = box.getAttribute("data-typ"); if (!TYPEN[typ]) return;
      var q = box.querySelector('script[type="application/json"]'), daten;
      try { daten = JSON.parse(q.textContent); } catch (e) { box.textContent = "Diese Übung konnte nicht geladen werden."; return; }
      var ziel = el("div", { class: "uebung-inhalt" }); box.appendChild(ziel); TYPEN[typ](ziel, daten);
    });
    document.querySelectorAll("[data-werkzeug]").forEach(function (box) { var w = WERKZEUGE[box.getAttribute("data-werkzeug")]; if (w) w(box); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
