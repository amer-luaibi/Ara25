#!/usr/bin/env python3
"""Audit an Ara25 JSON/JSONL artifact without printing source text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ara25 import audit_records, iter_json_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="JSON or JSONL artifact to audit")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = {
        "file_name": args.dataset.name,
        "audit": audit_records(iter_json_records(args.dataset)),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
