/* =========================================================
   Lernfortschritt: Stufen werden nacheinander freigeschaltet.
   Gespeichert wird nur im Browser auf diesem Gerät (localStorage),
   nichts wird übertragen. Benötigt: lernpfad.js (window.LERNPFAD)
   ========================================================= */
(function () {
  "use strict";
  var P = window.LERNPFAD || { stufenweise: false, stufen: {}, namen: {} };
  var SCHLUESSEL = "musik7-notenlehre-fortschritt", GRENZE = 0.8;
  var speicherOk = true, daten = { geloest: {} };
  try {
    var roh = window.localStorage.getItem(SCHLUESSEL);
    if (roh) daten = JSON.parse(roh) || daten;
    if (!daten.geloest) daten.geloest = {};
    window.localStorage.setItem(SCHLUESSEL + "-test", "1"); window.localStorage.removeItem(SCHLUESSEL + "-test");
  } catch (e) { speicherOk = false; }
  function sichern() { try { window.localStorage.setItem(SCHLUESSEL, JSON.stringify(daten)); } catch (e) { speicherOk = false; } }

  function geloest(slug) { return (daten.geloest[slug] || 0) >= GRENZE; }
  function stufenListe() { return Object.keys(P.stufen).map(Number).sort(function (a, b) { return a - b; }); }
  function stand(n) { var l = P.stufen[n] || []; return { gesamt: l.length, fertig: l.filter(geloest).length }; }
  function stufeFrei(n) {
    if (!P.stufenweise || !speicherOk) return true;
    var liste = stufenListe();
    for (var i = 0; i < liste.length && liste[i] < n; i++) { var s = stand(liste[i]); if (s.fertig < s.gesamt) return false; }
    return true;
  }
  function vorherigeOffen(n) {
    var liste = stufenListe();
    for (var i = 0; i < liste.length && liste[i] < n; i++) { var s = stand(liste[i]); if (s.fertig < s.gesamt) return liste[i]; }
    return null;
  }
  function stufeVon(slug) { for (var k in P.stufen) if (P.stufen[k].indexOf(slug) >= 0) return +k; return null; }

  function hinweis(text, gut) {
    var t = document.createElement("div");
    t.className = "toast" + (gut ? " gut" : "");
    t.setAttribute("role", "status");
    t.textContent = text;
    document.body.appendChild(t);
    setTimeout(function () { t.classList.add("weg"); }, 5200);
    setTimeout(function () { t.remove(); }, 6000);
  }

  function melden(el, anteil) {
    var box = el && el.closest ? el.closest(".uebung[data-id]") : null;
    if (!box) return;
    var slug = box.getAttribute("data-id"), n = stufeVon(slug);
    var vorher = geloest(slug), freiVorher = n != null ? stufeFrei(n + 1) : true;
    daten.geloest[slug] = Math.max(daten.geloest[slug] || 0, anteil);
    sichern();
    if (!speicherOk || n == null) return;
    if (!vorher && geloest(slug)) {
      var s = stand(n);
      var naechste = stufenListe().filter(function (x) { return x > n; })[0];
      if (P.stufenweise && naechste && !freiVorher && stufeFrei(naechste)) hinweis("Geschafft! Stufe " + n + " ist komplett. Stufe " + naechste + " („" + P.namen[naechste] + "“) ist jetzt freigeschaltet.", true);
      else hinweis("Übung geschafft ✓  In Stufe " + n + " hast du " + s.fertig + " von " + s.gesamt + " Übungen gelöst.", true);
    } else if (!geloest(slug) && anteil < GRENZE) {
      hinweis("Für den Lernpfad zählt die Übung ab " + Math.round(GRENZE * 100) + " Prozent richtig. Versuch es noch einmal!", false);
    }
  }

  function el(tag, attrs, text) { var e = document.createElement(tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; return e; }

  /* Seiten einer gesperrten Stufe abdecken */
  function seitenSperre() {
    var st = +document.body.getAttribute("data-stufe");
    if (!st || stufeFrei(st)) return;
    var offen = vorherigeOffen(st), main = document.getElementById("inhalt"), wurzel = document.body.getAttribute("data-wurzel") || "./";
    main.classList.add("stufe-gesperrt");
    var s = stand(offen);
    var kasten = el("section", { class: "sperr-kasten spalte", role: "alert" });
    kasten.appendChild(el("h1", {}, "Noch gesperrt"));
    kasten.appendChild(el("p", {}, "Diese Seite gehört zu Stufe " + st + ". Sie wird freigeschaltet, sobald du alle Übungen von Stufe " + offen + " („" + P.namen[offen] + "“) gelöst hast. Bisher: " + s.fertig + " von " + s.gesamt + "."));
    var a = el("a", { class: "knopf", href: wurzel + "index.html#stufe-" + offen }, "Zu Stufe " + offen);
    kasten.appendChild(a);
    main.parentNode.insertBefore(kasten, main);
  }

  /* Startseite und Kapitelseiten: Häkchen und Stufenstand */
  function markieren() {
    document.querySelectorAll("[data-uebung]").forEach(function (a) {
      if (geloest(a.getAttribute("data-uebung"))) a.classList.add("geloest");
    });
    document.querySelectorAll(".stufe[data-stufe]").forEach(function (sec) {
      var n = +sec.getAttribute("data-stufe"), s = stand(n), frei = stufeFrei(n);
      var anzeige = sec.querySelector(".stufe-stand");
      if (anzeige) anzeige.textContent = s.gesamt ? (s.fertig === s.gesamt ? "✓ alle " + s.gesamt + " Übungen gelöst" : s.fertig + " von " + s.gesamt + " Übungen gelöst") : "";
      if (!frei) {
        sec.classList.add("gesperrt");
        var offen = vorherigeOffen(n);
        var h = sec.querySelector(".stufe-sperre");
        if (h) { h.hidden = false; h.textContent = "🔒 Wird freigeschaltet, wenn alle Übungen von Stufe " + offen + " gelöst sind."; }
        sec.querySelectorAll("a.kap-karte").forEach(function (a) { a.setAttribute("aria-disabled", "true"); a.setAttribute("tabindex", "-1"); a.addEventListener("click", function (ev) { ev.preventDefault(); }); });
      }
    });
    var info = document.getElementById("fortschritt-info");
    if (info) {
      if (!P.stufenweise) info.hidden = true;
      else if (!speicherOk) info.textContent = "Dein Browser erlaubt hier keine Speicherung. Darum sind alle Stufen offen, der Fortschritt wird aber nicht gemerkt.";
    }
    var reset = document.getElementById("fortschritt-reset");
    if (reset) reset.addEventListener("click", function () {
      if (!window.confirm("Möchtest du deinen gesamten Lernfortschritt auf diesem Gerät löschen?")) return;
      daten = { geloest: {} }; sichern(); location.reload();
    });
  }

  window.Fortschritt = { melden: melden, stufeFrei: stufeFrei, geloest: geloest };
  function start() { seitenSperre(); markieren(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
