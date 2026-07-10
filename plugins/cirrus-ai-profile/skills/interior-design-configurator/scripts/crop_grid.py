#!/usr/bin/env python3
"""
crop_grid.py — Schneidet ein Rasterbild (z.B. wenn ChatGPT/Gemini alle 3 Varianten
eines Raums als ein einziges Collage-Bild statt als 3 Einzelbilder liefert) in
einzelne Zellen.

Usage:
    python crop_grid.py grid.png outdir/ --prefix wohnzimmer
    python crop_grid.py grid.png outdir/ --prefix wohnzimmer --rows 1 --cols 3
    python crop_grid.py grid.png outdir/ --prefix wohnzimmer --caption-frac 0.08

Ohne --rows/--cols wird automatisch anhand heller Zwischenräume (weiße/graue
Ränder zwischen den Zellen) gerastert. Bei unregelmäßigen Layouts --rows/--cols
manuell setzen. Ergebnisse danach immer visuell prüfen.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def find_gutters(is_bg, min_gap=6):
    """Findet zusammenhängende Bereiche von True-Werten mit Mindestlänge min_gap."""
    gutters = []
    start = None
    for i, v in enumerate(is_bg):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_gap:
                gutters.append((start, i))
            start = None
    if start is not None and len(is_bg) - start >= min_gap:
        gutters.append((start, len(is_bg)))
    return gutters


def segments_from_gutters(gutters, total_len):
    segments = []
    prev_end = 0
    for g_start, g_end in gutters:
        if g_start > prev_end:
            segments.append((prev_end, g_start))
        prev_end = g_end
    if prev_end < total_len:
        segments.append((prev_end, total_len))
    return segments


def auto_split(img: Image.Image, threshold=245):
    arr = np.array(img.convert("L"))
    is_bg_col = arr.min(axis=0) >= threshold
    is_bg_row = arr.min(axis=1) >= threshold
    col_segments = segments_from_gutters(find_gutters(is_bg_col), arr.shape[1])
    row_segments = segments_from_gutters(find_gutters(is_bg_row), arr.shape[0])
    return row_segments, col_segments


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("outdir")
    ap.add_argument("--prefix", default="cell")
    ap.add_argument("--rows", type=int, default=0, help="Zeilen manuell erzwingen (0 = Auto-Erkennung)")
    ap.add_argument("--cols", type=int, default=0, help="Spalten manuell erzwingen (0 = Auto-Erkennung)")
    ap.add_argument("--caption-frac", type=float, default=0.0,
                     help="Unteren Anteil jeder Zelle abschneiden (0.0-0.3), falls Bildunterschriften mit im Bild sind")
    args = ap.parse_args()

    img = Image.open(args.image)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    w, h = img.size

    if args.rows and args.cols:
        row_bounds = [(round(h * r / args.rows), round(h * (r + 1) / args.rows)) for r in range(args.rows)]
        col_bounds = [(round(w * c / args.cols), round(w * (c + 1) / args.cols)) for c in range(args.cols)]
    else:
        row_bounds, col_bounds = auto_split(img)
        if args.rows:
            row_bounds = [(round(h * r / args.rows), round(h * (r + 1) / args.rows)) for r in range(args.rows)]
        if args.cols:
            col_bounds = [(round(w * c / args.cols), round(w * (c + 1) / args.cols)) for c in range(args.cols)]

    print(f"Erkannt: {len(row_bounds)} Zeile(n) x {len(col_bounds)} Spalte(n)")

    count = 0
    for ri, (y0, y1) in enumerate(row_bounds):
        for ci, (x0, x1) in enumerate(col_bounds):
            cell_y1 = y1
            if args.caption_frac > 0:
                cell_y1 = y0 + int((y1 - y0) * (1 - args.caption_frac))
            cell = img.crop((x0, y0, x1, cell_y1))
            fname = outdir / f"{args.prefix}_{ri + 1}_{ci + 1}.png"
            cell.save(fname)
            print(f"  {fname.name}  ({cell.size[0]}x{cell.size[1]})")
            count += 1

    print(f"\n{count} Zelle(n) gespeichert in {outdir}/")
    print("Bitte jede Datei ansehen und sinnvoll umbenennen (z.B. wohnzimmer_v1.png), "
          "bevor sie in der config.json referenziert wird.")


if __name__ == "__main__":
    main()
