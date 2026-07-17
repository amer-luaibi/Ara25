#!/usr/bin/env python3
"""Create public notebook copies with outputs and volatile metadata removed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


KEEP_NOTEBOOK_METADATA = {"kernelspec", "language_info", "colab"}


def sanitize(payload: dict[str, Any], title: str) -> dict[str, Any]:
    payload["metadata"] = {
        key: value
        for key, value in payload.get("metadata", {}).items()
        if key in KEEP_NOTEBOOK_METADATA
    }
    for cell in payload.get("cells", []):
        cell["metadata"] = {}
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    intro = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# {title}\n",
            "\n",
            "Public research-preview notebook. Outputs and volatile metadata were removed. ",
            "Set local dataset/output paths in the configuration cells before running.\n",
        ],
    }
    cells = payload.setdefault("cells", [])
    if not cells or cells[0].get("cell_type") != "markdown" or "Public research-preview" not in "".join(cells[0].get("source", [])):
        cells.insert(0, intro)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for source in args.inputs:
        payload = json.loads(source.read_text(encoding="utf-8"))
        cleaned = sanitize(payload, source.stem.replace("_", " — "))
        target = args.output_dir / source.name
        target.write_text(
            json.dumps(cleaned, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
