/* =========================================================
   Übungsbausteine für Biologie Klasse 8
   Eine Übung wird so in eine Seite eingebaut:

   <div class="uebung" data-typ="quiz">
     <script type="application/json"> { ...Inhalt... } </script>
   </div>

   Typen: quiz, zuordnen, sortieren, lueckentext
   Es werden keine Daten gespeichert oder verschickt.
   ========================================================= */
(function () {
  "use strict";

  function el(tag, attrs, kinder) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") e.textContent = attrs[k];
        else if (k === "html") e.innerHTML = attrs[k];
        else if (k === "class") e.className = attrs[k];
        else if (k.indexOf("on") === 0) e.addEventListener(k.slice(2), attrs[k]);
        else e.setAttribute(k, attrs[k]);
      });
    }
    (kinder || []).forEach(function (k) { if (k) e.appendChild(k); });
    return e;
  }

  function mischen(liste) {
    var a = liste.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function melde(container, anteil) { if (window.Fortschritt) window.Fortschritt.melden(container, anteil); }

  function lob(anteil) {
    if (anteil === 1) return "Alles richtig – stark!";
    if (anteil >= 0.75) return "Sehr gut, fast alles richtig.";
    if (anteil >= 0.5) return "Gut! Schau dir die markierten Stellen noch einmal an.";
    return "Lies den Lerntext noch einmal und versuche es erneut.";
  }

  function punkteleiste(container, text, neustart) {
    var leiste = el("div", { class: "punktestand", role: "status", "aria-live": "polite" }, [
      el("span", { text: text }),
      el("button", { class: "knopf", type: "button", text: "Neu starten", onclick: neustart })
    ]);
    container.appendChild(leiste);
    return leiste;
  }

  /* ---------- Quiz (Multiple Choice) ---------- */
  function quiz(container, daten) {
    var fragen = daten.mischen === false ? daten.fragen : mischen(daten.fragen);
    var beantwortet = 0, richtig = 0;
    var leiste;

    fragen.forEach(function (f, nr) {
      var box = el("div", { class: "frage" });
      box.appendChild(el("h3", {}, [el("span", { class: "nummer", text: (nr + 1) + "." }), document.createTextNode(f.frage)]));
      var opts = el("div", { class: "optionen", role: "group", "aria-label": "Antwortmöglichkeiten" });
      var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" });
      var reihenfolge = f.optionen.map(function (o, i) { return { text: o, i: i }; });
      reihenfolge = mischen(reihenfolge);
      reihenfolge.forEach(function (o) {
        var b = el("button", { class: "option", type: "button", text: o.text });
        b.addEventListener("click", function () {
          var istRichtig = o.i === f.richtig;
          Array.prototype.forEach.call(opts.children, function (k) { k.disabled = true; });
          b.classList.add(istRichtig ? "ist-richtig" : "ist-falsch");
          if (!istRichtig) {
            Array.prototype.forEach.call(opts.children, function (k, idx) {
              if (reihenfolge[idx].i === f.richtig) k.classList.add("ist-richtig");
            });
          }
          rueck.innerHTML = "";
          rueck.appendChild(el("strong", { class: istRichtig ? "gut" : "schlecht", text: istRichtig ? "Richtig. " : "Leider falsch. " }));
          if (f.erklaerung) rueck.appendChild(document.createTextNode(f.erklaerung));
          beantwortet++; if (istRichtig) richtig++;
          leiste.firstChild.textContent = punkteText();
          if (beantwortet === fragen.length) melde(container, richtig / fragen.length);
        });
        opts.appendChild(b);
      });
      box.appendChild(opts); box.appendChild(rueck);
      container.appendChild(box);
    });

    function punkteText() {
      var t = richtig + " von " + fragen.length + " richtig";
      if (beantwortet === fragen.length) t += " – " + lob(richtig / fragen.length);
      else t += " (" + (fragen.length - beantwortet) + " offen)";
      return t;
    }
    leiste = punkteleiste(container, punkteText(), function () { neuAufbauen(container, "quiz", daten); });
  }

  /* ---------- Zuordnen ---------- */
  function zuordnen(container, daten) {
    var paare = mischen(daten.paare);
    var rechts = mischen(daten.paare.map(function (p) { return p.rechts; }));
    var zeilen = [];
    paare.forEach(function (p, nr) {
      var id = "z" + Math.random().toString(36).slice(2, 8) + nr;
      var sel = el("select", { id: id });
      sel.appendChild(el("option", { value: "", text: "– bitte wählen –" }));
      rechts.forEach(function (r) { sel.appendChild(el("option", { value: r, text: r })); });
      var zeile = el("div", { class: "paar" }, [el("label", { class: "begriff", for: id, text: p.links }), sel]);
      zeilen.push({ zeile: zeile, sel: sel, loesung: p.rechts });
      container.appendChild(zeile);
    });
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" });
    var loesungKnopf = el("button", { class: "knopf leise", type: "button", text: "Lösung zeigen", onclick: loesung });
    var sperre = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    var pruefKnopf = el("button", { class: "knopf", type: "button", text: "Prüfen", onclick: pruefen });
    var knoepfe = el("div", { class: "knopfreihe" }, [
      pruefKnopf,
      loesungKnopf,
      el("button", { class: "knopf leise", type: "button", text: "Neu starten", onclick: function () { neuAufbauen(container, "zuordnen", daten); } })
    ]);
    container.appendChild(knoepfe); container.appendChild(sperre); container.appendChild(rueck);
    function offen() { return zeilen.filter(function (z) { return !z.sel.value; }).length; }
    function sperre_() { sperreAktualisieren([pruefKnopf, loesungKnopf], sperre, offen, "Zuordnung", "Zuordnungen"); }
    sperre_();
    zeilen.forEach(function (z) { z.sel.addEventListener("change", function () { z.zeile.classList.remove("ist-richtig", "ist-falsch"); sperre_(); }); });

    function pruefen() {
      if (offen()) return;
      var n = 0;
      zeilen.forEach(function (z) {
        var ok = z.sel.value === z.loesung;
        z.zeile.classList.toggle("ist-richtig", ok);
        z.zeile.classList.toggle("ist-falsch", !ok);
        if (ok) n++;
      });
      rueck.innerHTML = "";
      rueck.appendChild(el("strong", { class: n === zeilen.length ? "gut" : "schlecht", text: n + " von " + zeilen.length + " richtig. " }));
      rueck.appendChild(document.createTextNode(lob(n / zeilen.length))); melde(container, n / zeilen.length);
    }
    // Eigene Antworten bleiben stehen; unter falschen erscheint die richtige Lösung.
    function loesung() {
      if (offen()) return;
      pruefen();
      zeilen.forEach(function (z) {
        var alt = z.zeile.querySelector(".loesung-zeile");
        if (alt) alt.remove();
        if (z.zeile.classList.contains("ist-falsch")) z.zeile.appendChild(el("span", { class: "loesung-zeile", text: "Richtig wäre: " + z.loesung }));
      });
      rueck.appendChild(document.createTextNode(" Unter deinen falschen Antworten steht jetzt die richtige Lösung."));
    }
  }

  /* ---------- Sortieren in Kategorien ---------- */
  function sortieren(container, daten) {
    var eintraege = mischen(daten.eintraege);
    var zeilen = [];
    eintraege.forEach(function (e) {
      var wahl = el("div", { class: "wahl", role: "group", "aria-label": "Zuordnung für: " + e.text });
      var loesungText = el("div", { class: "loesung", hidden: "" });
      var zeile = el("div", { class: "sortier-eintrag" }, [el("span", { text: e.text }), wahl, loesungText]);
      var z = { zeile: zeile, gewaehlt: null, loesung: e.kategorie, erklaerung: e.erklaerung, loesungText: loesungText, knoepfe: [] };
      daten.kategorien.forEach(function (k) {
        var b = el("button", { type: "button", "aria-pressed": "false", text: k });
        b.addEventListener("click", function () {
          z.gewaehlt = k;
          z.knoepfe.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          zeile.classList.remove("ist-richtig", "ist-falsch");
          loesungText.hidden = true;
        });
        z.knoepfe.push(b); wahl.appendChild(b);
      });
      zeilen.push(z); container.appendChild(zeile);
    });
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" });
    var pruefKnopf = el("button", { class: "knopf", type: "button", text: "Prüfen", onclick: pruefen });
    var sperre = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    container.appendChild(el("div", { class: "knopfreihe" }, [
      pruefKnopf,
      el("button", { class: "knopf leise", type: "button", text: "Neu starten", onclick: function () { neuAufbauen(container, "sortieren", daten); } })
    ]));
    container.appendChild(sperre); container.appendChild(rueck);
    function offenZahl() { return zeilen.filter(function (z) { return !z.gewaehlt; }).length; }
    function sperre_() { sperreAktualisieren(pruefKnopf, sperre, offenZahl, "Aussage", "Aussagen", "nicht zugeordnet"); }
    zeilen.forEach(function (z) { z.knoepfe.forEach(function (b) { b.addEventListener("click", sperre_); }); });
    sperre_();

    function pruefen() {
      var n = 0, offen = offenZahl();
      if (offen) return;
      zeilen.forEach(function (z) {
        var ok = z.gewaehlt === z.loesung;
        z.zeile.classList.toggle("ist-richtig", ok);
        z.zeile.classList.toggle("ist-falsch", !ok);
        if (ok) n++;
        else {
          z.loesungText.textContent = "Richtig wäre: " + z.loesung + (z.erklaerung ? ". " + z.erklaerung : "");
          z.loesungText.hidden = false;
        }
      });
      rueck.innerHTML = "";
      rueck.appendChild(el("strong", { class: n === zeilen.length ? "gut" : "schlecht", text: n + " von " + zeilen.length + " richtig. " }));
      rueck.appendChild(document.createTextNode(lob(n / zeilen.length))); melde(container, n / zeilen.length);
    }
  }

  /* ---------- Lückentext ----------
     Lücken im Text: [[Antwort]] oder [[Antwort|andere erlaubte Schreibweise]] */
  function lueckentext(container, daten) {
    var luecken = [];
    var html = daten.text.replace(/\[\[([^\]]+)\]\]/g, function (_, inhalt) {
      var moeglich = inhalt.split("|").map(function (s) { return s.trim(); });
      luecken.push(moeglich);
      return '<input type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Lücke ' + luecken.length + '" data-nr="' + (luecken.length - 1) + '">';
    });
    if (daten.wortspeicher !== false) {
      var speicher = el("div", { class: "wortspeicher", "aria-label": "Wortspeicher" });
      mischen(luecken.map(function (l) { return l[0]; })).forEach(function (w) { speicher.appendChild(el("span", { text: w })); });
      container.appendChild(speicher);
    }
    var text = el("div", { class: "lueckentext", html: html });
    container.appendChild(text);
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" });
    var loesungKnopf = el("button", { class: "knopf leise", type: "button", text: "Lösung zeigen", onclick: loesung });
    var sperre = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    var pruefKnopf = el("button", { class: "knopf", type: "button", text: "Prüfen", onclick: pruefen });
    container.appendChild(el("div", { class: "knopfreihe" }, [
      pruefKnopf,
      loesungKnopf,
      el("button", { class: "knopf leise", type: "button", text: "Neu starten", onclick: function () { neuAufbauen(container, "lueckentext", daten); } })
    ]));
    container.appendChild(sperre); container.appendChild(rueck);
    function offen() { return Array.prototype.filter.call(text.querySelectorAll("input"), function (f) { return !f.value.trim(); }).length; }
    function sperre_() { sperreAktualisieren([pruefKnopf, loesungKnopf], sperre, offen, "Lücke", "Lücken"); }
    sperre_();
    text.addEventListener("input", function (ev) { if (ev.target.classList) ev.target.classList.remove("ist-richtig", "ist-falsch"); sperre_(); });

    function norm(s) { return s.toLowerCase().replace(/\s+/g, " ").trim(); }
    function pruefen() {
      if (offen()) return;
      var n = 0, felder = text.querySelectorAll("input");
      Array.prototype.forEach.call(felder, function (f) {
        var ok = luecken[+f.dataset.nr].some(function (m) { return norm(m) === norm(f.value); });
        f.classList.toggle("ist-richtig", ok); f.classList.toggle("ist-falsch", !ok);
        if (ok) n++;
      });
      rueck.innerHTML = "";
      rueck.appendChild(el("strong", { class: n === felder.length ? "gut" : "schlecht", text: n + " von " + felder.length + " richtig. " }));
      rueck.appendChild(document.createTextNode(lob(n / felder.length))); melde(container, n / felder.length);
    }
    // Eigene Antworten bleiben stehen; neben falschen erscheint die richtige Lösung.
    function loesung() {
      if (offen()) return;
      pruefen();
      Array.prototype.forEach.call(text.querySelectorAll("input"), function (f) {
        var alt = f.nextElementSibling;
        if (alt && alt.classList.contains("loesung-wort")) alt.remove();
        if (f.classList.contains("ist-falsch")) f.insertAdjacentElement("afterend", el("span", { class: "loesung-wort", text: luecken[+f.dataset.nr][0] }));
      });
      rueck.appendChild(document.createTextNode(" Die richtigen Lösungen stehen jetzt grün neben deinen falschen Antworten."));
    }
  }

  /* ---------- Reihenfolge ----------
     daten.schritte: Texte in der richtigen Reihenfolge */
  function reihenfolge(container, daten) {
    var richtig = daten.schritte.slice(), liste;
    do { liste = mischen(richtig); } while (liste.every(function (t, i) { return t === richtig[i]; }));
    var geprueft = false;
    var ol = el("ol", { class: "reihen-liste" });
    var rueck = el("p", { class: "rueckmeldung", "aria-live": "polite" });
    var loesungKnopf = el("button", { class: "knopf leise", type: "button", text: "Lösung zeigen", onclick: loesung, disabled: "" });
    var sperre = el("p", { class: "legende loesung-sperre", "aria-live": "polite" });
    var pruefKnopf = el("button", { class: "knopf", type: "button", text: "Prüfen", onclick: pruefen });
    var bewegt = {};
    function offen() { return liste.filter(function (t) { return !bewegt[t]; }).length; }
    function sperre_() {
      var n = offen();
      pruefKnopf.disabled = n > 0;
      pruefKnopf.title = n > 0 ? "Bearbeite zuerst die ganze Aufgabe." : "";
      sperre.textContent = n > 0
        ? "„Prüfen“ geht erst, wenn du jeden Schritt mindestens einmal verschoben hast. Noch " + n + (n === 1 ? " Schritt" : " Schritte") + " nicht verschoben."
        : (geprueft ? "" : "Die Lösung kannst du ansehen, nachdem du deine Reihenfolge geprüft hast.");
      sperre.hidden = !sperre.textContent;
    }
    container.appendChild(ol);
    container.appendChild(el("div", { class: "knopfreihe" }, [
      pruefKnopf,
      loesungKnopf,
      el("button", { class: "knopf leise", type: "button", text: "Neu starten", onclick: function () { neuAufbauen(container, "reihenfolge", daten); } })
    ]));
    container.appendChild(sperre); container.appendChild(rueck);

    function zeichnen(fokusText, richtung) {
      ol.innerHTML = "";
      liste.forEach(function (t, i) {
        var hoch = el("button", { class: "rf-pfeil", type: "button", "aria-label": "„" + t + "“ nach oben", text: "▲" });
        var runter = el("button", { class: "rf-pfeil", type: "button", "aria-label": "„" + t + "“ nach unten", text: "▼" });
        hoch.disabled = i === 0; runter.disabled = i === liste.length - 1;
        hoch.addEventListener("click", function () { tausche(i, i - 1, t, "hoch"); });
        runter.addEventListener("click", function () { tausche(i, i + 1, t, "runter"); });
        var li = el("li", { class: "rf-eintrag" }, [el("span", { class: "rf-nr", text: (i + 1) + "." }), el("span", { class: "rf-text", text: t }), el("span", { class: "rf-knoepfe" }, [hoch, runter])]);
        ol.appendChild(li);
        if (t === fokusText) { var ziel = richtung === "hoch" ? (i === 0 ? runter : hoch) : (i === liste.length - 1 ? hoch : runter); setTimeout(function () { ziel.focus(); }, 0); }
      });
    }
    function tausche(a, b, t, richtung) {
      var x = liste[a]; liste[a] = liste[b]; liste[b] = x;
      bewegt[liste[a]] = true; bewegt[liste[b]] = true;
      Array.prototype.forEach.call(ol.children, function (li) { li.classList.remove("ist-richtig", "ist-falsch"); });
      rueck.textContent = ""; zeichnen(t, richtung); sperre_();
    }
    function pruefen() {
      if (offen()) return;
      var n = 0;
      Array.prototype.forEach.call(ol.children, function (li, i) {
        var ok = liste[i] === richtig[i];
        li.classList.toggle("ist-richtig", ok); li.classList.toggle("ist-falsch", !ok);
        if (ok) n++;
      });
      geprueft = true; loesungKnopf.disabled = false; sperre_();
      rueck.innerHTML = "";
      rueck.appendChild(el("strong", { class: n === liste.length ? "gut" : "schlecht", text: n + " von " + liste.length + " an der richtigen Stelle. " }));
      rueck.appendChild(document.createTextNode(lob(n / liste.length))); melde(container, n / liste.length);
    }
    function loesung() {
      if (!geprueft) return;
      liste = richtig.slice(); zeichnen();
      Array.prototype.forEach.call(ol.children, function (li) { li.classList.add("ist-richtig"); });
      rueck.textContent = "So ist die richtige Reihenfolge. Vergleiche sie mit deinem Versuch.";
    }
    zeichnen(); sperre_();
  }

  /* ---------- Schreibtraining ----------
     daten.aufgaben: [{ frage, checkliste: [...], muster, minWoerter }] */
  function schreiben(container, daten) {
    daten.aufgaben.forEach(function (a, nr) {
      var box = el("div", { class: "frage schreib-aufgabe" });
      var id = "s" + Math.random().toString(36).slice(2, 8);
      box.appendChild(el("h3", {}, [el("span", { class: "nummer", text: (nr + 1) + "." }), document.createTextNode(a.frage)]));
      if (a.hinweis) box.appendChild(el("p", { class: "legende", text: a.hinweis }));
      var feld = el("textarea", { id: id, rows: "8", class: "schreibfeld", "aria-label": "Deine Antwort zu Aufgabe " + (nr + 1) });
      var zaehler = el("p", { class: "legende", "aria-live": "polite" });
      var knopf = el("button", { class: "knopf leise", type: "button", text: "Mit Musterlösung vergleichen", disabled: "" });
      var ausgabe = el("div", { class: "schreib-vergleich", hidden: "" });
      var min = a.minWoerter || 40;
      function woerter() { var t = feld.value.trim(); return t ? t.split(/\s+/).length : 0; }
      // verschiedene Wörter zählen, damit Wiederholungen nicht reichen
      function verschiedene() { var m = {}; feld.value.toLowerCase().split(/[^a-zäöüß0-9-]+/).forEach(function (x) { if (x.length > 2) m[x] = 1; }); return Object.keys(m).length; }
      function bereit() { return woerter() >= min && verschiedene() >= Math.round(min * 0.55); }
      function aktualisieren() {
        var w = woerter();
        knopf.disabled = !bereit();
        if (w < min) zaehler.textContent = w + " Wörter. Schreib mindestens " + min + " Wörter, dann kannst du mit der Musterlösung vergleichen.";
        else if (!bereit()) zaehler.textContent = w + " Wörter, aber viele davon wiederholen sich. Beschreibe die Krankheit mit eigenen Sätzen.";
        else zaehler.textContent = w + " Wörter.";
      }
      feld.addEventListener("input", aktualisieren);
      knopf.addEventListener("click", function () {
        if (!bereit()) return;
        ausgabe.innerHTML = "";
        ausgabe.appendChild(el("h4", { text: "Hast du an alles gedacht? Hake ab, was in deinem Text vorkommt." }));
        var ul = el("ul", { class: "checkliste" });
        a.checkliste.forEach(function (c, i) {
          var cid = id + "c" + i;
          ul.appendChild(el("li", {}, [el("input", { type: "checkbox", id: cid }), el("label", { for: cid, text: c })]));
        });
        ausgabe.appendChild(ul);
        ausgabe.appendChild(el("h4", { text: "Musterlösung" }));
        ausgabe.appendChild(el("p", { class: "muster", text: a.muster }));
        ausgabe.hidden = false;
        ul.querySelector("input").focus();
      });
      box.appendChild(feld); box.appendChild(zaehler);
      box.appendChild(el("div", { class: "knopfreihe" }, [knopf])); box.appendChild(ausgabe);
      container.appendChild(box);
      aktualisieren();
    });
    container.appendChild(el("p", { class: "legende", text: "Dein Text wird nicht gespeichert. Wenn du die Seite neu lädst, ist er weg." }));
  }

  /* Lösung erst freigeben, wenn alle Felder ausgefüllt sind */
  /* Prüfen und Lösung erst freigeben, wenn die Aufgabe vollständig bearbeitet ist */
  function sperreAktualisieren(knoepfe, hinweis, offen, einzahl, mehrzahl, rest) {
    var n = offen();
    [].concat(knoepfe).forEach(function (k) {
      k.disabled = n > 0;
      k.title = n > 0 ? "Bearbeite zuerst die ganze Aufgabe." : "";
    });
    hinweis.textContent = n > 0
      ? [].concat(knoepfe).map(function (k) { return "„" + k.textContent + "“"; }).join(" und ") + ([].concat(knoepfe).length > 1 ? " gehen" : " geht") + " erst, wenn du alles bearbeitet hast. Noch " + n + " " + (n === 1 ? einzahl : mehrzahl) + " " + (rest || "offen") + "."
      : "";
    hinweis.hidden = n === 0;
  }

  var typen = { quiz: quiz, zuordnen: zuordnen, sortieren: sortieren, lueckentext: lueckentext, reihenfolge: reihenfolge, schreiben: schreiben };

  function neuAufbauen(container, typ, daten) {
    container.innerHTML = "";
    typen[typ](container, daten);
  }

  function start() {
    document.querySelectorAll(".uebung[data-typ]").forEach(function (box) {
      var typ = box.getAttribute("data-typ");
      var quelle = box.querySelector('script[type="application/json"]');
      if (!typen[typ] || !quelle) return;
      var daten;
      try { daten = JSON.parse(quelle.textContent); }
      catch (err) { box.textContent = "Diese Übung konnte nicht geladen werden (Fehler im Inhalt)."; return; }
      var ziel = el("div", { class: "uebung-inhalt" });
      box.appendChild(ziel);
      typen[typ](ziel, daten);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
