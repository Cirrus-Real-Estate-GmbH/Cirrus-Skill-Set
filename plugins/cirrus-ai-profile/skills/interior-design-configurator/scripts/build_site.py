#!/usr/bin/env python3
"""
build_site.py — Baut aus einer config.json und Raumfotos eine einzelne interaktive
HTML-Datei (Einrichtungs-Konfigurator: Vorher/Nachher-Regler pro Raum, Tabs zwischen Räumen).

Usage:
    python build_site.py config.json output.html [--max-width 1100]

Die config.json referenziert Bilder relativ zu ihrem eigenen Speicherort.
Alle Bilder werden als Base64 in die HTML-Datei eingebettet (kein Hosting nötig).
"""
import argparse
import base64
import io
import json
import mimetypes
import sys
from pathlib import Path

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def encode_image(path: Path, max_width: int) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "image/jpeg"
    raw = path.read_bytes()

    if HAVE_PIL:
        try:
            img = Image.open(io.BytesIO(raw))
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, max(1, int(img.height * ratio)))
                img = img.resize(new_size, Image.LANCZOS)
            buf = io.BytesIO()
            if mime == "image/png" and img.mode == "RGBA":
                img.save(buf, format="PNG", optimize=True)
                mime = "image/png"
            else:
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(buf, format="JPEG", quality=85, optimize=True)
                mime = "image/jpeg"
            raw = buf.getvalue()
        except Exception as e:
            print(f"  Warnung: konnte {path.name} nicht mit Pillow verarbeiten ({e}), verwende Original.",
                  file=sys.stderr)

    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="Pfad zur config.json")
    ap.add_argument("output", help="Pfad zur Ausgabe-HTML-Datei")
    ap.add_argument("--max-width", type=int, default=1100, help="Max. Bildbreite in Pixeln (Standard: 1100)")
    args = ap.parse_args()

    if not HAVE_PIL:
        print("Warnung: Pillow ist nicht installiert — Bilder werden unskaliert eingebettet "
              "(pip install pillow --break-system-packages für kleinere Dateien).", file=sys.stderr)

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        print(f"Fehler: {config_path} nicht gefunden.", file=sys.stderr)
        sys.exit(1)
    base_dir = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))

    rooms = config.get("rooms")
    if not rooms:
        print("Fehler: config.json muss ein Feld 'rooms' (Liste) enthalten.", file=sys.stderr)
        sys.exit(1)

    total_images = 0
    for room in rooms:
        if "key" not in room or "items" not in room:
            print(f"Fehler: Raum ohne 'key' oder 'items': {room}", file=sys.stderr)
            sys.exit(1)
        for item in room["items"]:
            if "image" not in item:
                print(f"Fehler: Item ohne 'image'-Feld in Raum '{room['key']}': {item}", file=sys.stderr)
                sys.exit(1)
            img_path = (base_dir / item["image"]).resolve()
            if not img_path.exists():
                print(f"Fehler: Bild nicht gefunden: {img_path}", file=sys.stderr)
                sys.exit(1)
            label = room.get("label", room["key"])
            print(f"  Einbetten: {label} / {item.get('short', item['image'])}")
            item["src"] = encode_image(img_path, args.max_width)
            total_images += 1

    template_path = Path(__file__).resolve().parent.parent / "assets" / "template.html"
    if not template_path.exists():
        print(f"Fehler: Template nicht gefunden unter {template_path}", file=sys.stderr)
        sys.exit(1)
    html = template_path.read_text(encoding="utf-8")

    data_payload = {"title": config.get("title", "Wohnungs-Exposé"), "rooms": rooms}
    data_json = json.dumps(data_payload, ensure_ascii=False)

    marker = "/*__DATA__*/"
    if marker not in html:
        print("Fehler: Platzhalter __DATA__ nicht im Template gefunden.", file=sys.stderr)
        sys.exit(1)
    html = html.replace(marker, f"const DATA = {data_json};")

    out_path = Path(args.output)
    out_path.write_text(html, encoding="utf-8")
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\nFertig: {out_path} ({total_images} Bilder, {len(rooms)} Räume, {size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
