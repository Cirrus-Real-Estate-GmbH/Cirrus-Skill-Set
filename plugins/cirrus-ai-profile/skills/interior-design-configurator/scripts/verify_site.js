#!/usr/bin/env node
/**
 * verify_site.js — Strukturelle Prüfung der generierten Konfigurator-Seite
 * (kein visueller Check — nur ob die Seite technisch korrekt aufgebaut ist).
 *
 * Prüft:
 *  - Seite lädt ohne JS-Fehler
 *  - window.DATA ist vorhanden und wurde korrekt eingebettet
 *  - Anzahl Tabs entspricht Anzahl Räume in der Config
 *  - Anzahl Swatches pro Raum entspricht Anzahl Items in der Config
 *  - Alle <img>-Quellen sind Base64 eingebettet (kein kaputter Dateipfad)
 *
 * Benötigt das npm-Paket "jsdom" (npm install jsdom, falls nicht vorhanden).
 *
 * Usage: node verify_site.js output.html
 */
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const file = process.argv[2];
if (!file) {
  console.error("Usage: node verify_site.js output.html");
  process.exit(1);
}

const html = fs.readFileSync(file, "utf-8");
const errors = [];

const dom = new JSDOM(html, {
  url: "file://" + path.resolve(file),
  runScripts: "dangerously",
  resources: "usable",
  pretendToBeVisual: true,
});

dom.window.addEventListener("error", (e) => {
  errors.push("JS-Fehler: " + (e.error ? e.error.message : e.message));
});

setTimeout(() => {
  const { document } = dom.window;
  const DATA = dom.window.DATA;

  if (!DATA || !Array.isArray(DATA.rooms)) {
    errors.push("window.DATA fehlt oder enthält kein 'rooms'-Array — Config wurde evtl. nicht korrekt eingebettet.");
  } else {
    const tabs = document.querySelectorAll("[data-room-tab]");
    if (tabs.length !== DATA.rooms.length) {
      errors.push(`Tab-Anzahl stimmt nicht: erwartet ${DATA.rooms.length}, gefunden ${tabs.length}`);
    }

    DATA.rooms.forEach((room) => {
      const panel = document.querySelector(`[data-room="${room.key}"]`);
      if (!panel) {
        errors.push(`Kein Panel für Raum "${room.key}" gefunden.`);
        return;
      }
      const swatches = panel.querySelectorAll("[data-swatch]");
      if (swatches.length !== room.items.length) {
        errors.push(`Swatch-Anzahl für "${room.key}" stimmt nicht: erwartet ${room.items.length}, gefunden ${swatches.length}`);
      }
    });
  }

  const imgs = document.querySelectorAll("img");
  let checkedImgs = 0;
  imgs.forEach((img) => {
    const src = img.getAttribute("src") || "";
    if (src) {
      checkedImgs++;
      if (!src.startsWith("data:")) {
        errors.push("Bild nicht als Base64 eingebettet: " + src.slice(0, 80));
      }
    }
  });

  if (errors.length) {
    console.error("FEHLER:");
    errors.forEach((e) => console.error("  - " + e));
    process.exit(1);
  } else {
    console.log(`OK: Seite lädt ohne Fehler. ${DATA.rooms.length} Räume, ${checkedImgs} Bilder — alle als Base64 eingebettet, Tabs/Swatches stimmen mit Config überein.`);
    process.exit(0);
  }
}, 500);
