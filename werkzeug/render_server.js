// Liest pro Zeile eine JSON-Spezifikation und gibt das SVG als JSON-Zeile zurück.
const N = require("../assets/noten.js");
const rl = require("readline").createInterface({ input: process.stdin });
rl.on("line", (zeile) => {
  try { process.stdout.write(JSON.stringify(N.render(JSON.parse(zeile)).svg) + "\n"); }
  catch (e) { process.stdout.write(JSON.stringify("FEHLER: " + e.message) + "\n"); }
});
