#!/usr/bin/env python3
"""Prepare the editable Story SVG for production raster export."""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


SITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = SITE_ROOT / "static" / "brand" / "templates" / "social-story-1080x1920.svg"
EXPORT_MARKER = "exclude"


def remove_editor_only_groups(root):
    removed_ids = []
    for parent in root.iter():
        for child in list(parent):
            if child.get("data-export") == EXPORT_MARKER:
                removed_ids.append(child.get("id"))
                parent.remove(child)
    return removed_ids


def export_story(source, destination):
    source = Path(source)
    destination = Path(destination)
    tree = ET.parse(source)
    root = tree.getroot()
    removed_ids = remove_editor_only_groups(root)
    if removed_ids != ["editor-guide"]:
        raise ValueError(
            "Story export must remove exactly the editor-guide group; "
            f"removed {removed_ids!r}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree, space="  ")
    tree.write(destination, encoding="utf-8", xml_declaration=True)
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Strip editor-only layers from the School of Code Story master"
    )
    parser.add_argument("destination", type=Path, help="production SVG output path")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args(argv)
    output = export_story(args.source, args.destination)
    print(f"Prepared guide-free Story SVG: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
