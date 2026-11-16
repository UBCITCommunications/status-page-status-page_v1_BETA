#!/usr/bin/env python3
"""Embed the status page snapshots into index.html, or check they match.

index.html carries a copy of every file in data/snapshots/ so it can be opened straight
from disk (browsers won't let a local page read other local files). The JSON files are
the source of truth; this script keeps the copy in sync.

    python3 scripts/embed-snapshots.py           # rewrite the embedded copy
    python3 scripts/embed-snapshots.py --check   # exit 1 if index.html differs from data/

Standard library only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
SNAP_DIR = ROOT / "data" / "snapshots"
TITLES = ROOT / "data" / "history-titles.json"


def load_sources():
    files = sorted(SNAP_DIR.glob("summary-*.json"))
    if not files:
        sys.exit(f"No snapshots found in {SNAP_DIR}")
    snaps = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    titles = json.loads(TITLES.read_text(encoding="utf-8")) if TITLES.exists() else {}
    return files, snaps, titles


def js_literal(value):
    # Compact JSON is valid JavaScript. Escape "</" so the data can never close the <script> tag.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


BLOCKS = {
    "SNAPSHOTS": ("const SNAPSHOTS = ", ";"),
    "TITLES": ("const HISTORY_TITLES = ", ";"),
}


def block_re(name):
    return re.compile(r"(/\* " + name + r":BEGIN[^\n]*\*/\n)(.*?)(\n/\* " + name + r":END \*/)", re.S)


def embedded(html, name):
    m = block_re(name).search(html)
    if not m:
        sys.exit(f"index.html has no {name} markers")
    prefix, suffix = BLOCKS[name]
    body = m.group(2).strip()
    return json.loads(body[len(prefix):-len(suffix)].replace("<\\/", "</"))


def main():
    files, snaps, titles = load_sources()
    html = PAGE.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        ok = embedded(html, "SNAPSHOTS") == snaps and embedded(html, "TITLES") == titles
        print("index.html matches data/" if ok else "index.html does NOT match data/ - run scripts/embed-snapshots.py")
        sys.exit(0 if ok else 1)
    for name, value in (("SNAPSHOTS", snaps), ("TITLES", titles)):
        prefix, suffix = BLOCKS[name]
        html = block_re(name).sub(lambda m: m.group(1) + prefix + js_literal(value) + suffix + m.group(3), html)
    PAGE.write_text(html, encoding="utf-8")
    print(f"Embedded {len(files)} snapshots ({', '.join(f.name for f in files)}) and {len(titles)} history titles into index.html")


if __name__ == "__main__":
    main()
