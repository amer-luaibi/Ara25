"""Safe, text-suppressing data utilities for Ara25 JSON/JSONL artifacts."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator, Mapping
from hashlib import sha256
import json
from pathlib import Path
import re
from statistics import mean, median
from typing import Any


REQUIRED_FIELDS = ("id", "title", "Merged_Articles", "target_summary")
_ARTICLE_MARKER = re.compile(r"<ARTICLE_(\d+)>")
_DUPLICATE_MARKER = re.compile(r"(<ARTICLE_(\d+)>)\s*(?:\1)+")


def _strip_notebook_fence(line: str) -> str:
    """Remove accidental one-character Markdown fences around JSON records."""

    value = line.strip().lstrip("\ufeff")
    if value.startswith("`"):
        value = value[1:]
    if value.endswith("`"):
        value = value[:-1]
    return value.strip()


def iter_json_records(path: str | Path) -> Iterator[dict[str, Any]]:
    """Yield objects from a JSON array or line-delimited JSON file.

    The supplied dual-reference artifact contains a leading Markdown backtick on
    each row. This loader removes that wrapper without modifying the source file.
    It never logs or prints record text.
    """

    source = Path(path)
    with source.open("r", encoding="utf-8-sig") as handle:
        first = ""
        while not first:
            first = handle.readline()
            if not first:
                return
            first = first.strip()

        candidate = _strip_notebook_fence(first)
        if candidate.startswith("["):
            remaining = handle.read()
            payload = candidate + remaining
            values = json.loads(payload)
            if not isinstance(values, list):
                raise ValueError(f"Expected a JSON list in {source}")
            for item in values:
                if not isinstance(item, dict):
                    raise ValueError(f"Expected objects in {source}")
                yield item
            return

        for line_number, raw in enumerate([first, *handle], start=1):
            value = _strip_notebook_fence(raw)
            if not value:
                continue
            try:
                item = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON record at {source}:{line_number}: {exc.msg}"
                ) from exc
            if not isinstance(item, dict):
                raise ValueError(f"Expected an object at {source}:{line_number}")
            yield item


def validate_record(record: Mapping[str, Any], require_second_reference: bool = False) -> list[str]:
    """Return validation messages without returning or exposing record text."""

    issues: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            issues.append(f"missing:{field}")
        elif not str(record[field]).strip():
            issues.append(f"empty:{field}")
    if require_second_reference and not str(record.get("target_summary_2", "")).strip():
        issues.append("missing:target_summary_2")
    return issues


def normalize_article_markers(text: str) -> str:
    """Collapse immediately repeated `<ARTICLE_n>` markers."""

    return _DUPLICATE_MARKER.sub(r"\1", text or "")


def count_article_slots(text: str) -> int:
    """Count distinct numbered article markers in a merged input."""

    return len(set(_ARTICLE_MARKER.findall(text or "")))


def _numeric_summary(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "median": None, "mean": None, "max": None}
    return {
        "min": min(values),
        "median": median(values),
        "mean": mean(values),
        "max": max(values),
    }


def audit_records(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Return aggregate, non-textual audit statistics for a record iterable."""

    rows = list(records)
    ids = [str(row.get("id", "")) for row in rows]
    merged = [str(row.get("Merged_Articles", "")) for row in rows]
    hashes = [sha256(value.encode("utf-8")).hexdigest() for value in merged]
    issues = Counter(
        issue
        for row in rows
        for issue in validate_record(row)
    )

    return {
        "records": len(rows),
        "unique_ids": len(set(ids)),
        "duplicate_id_rows": len(rows) - len(set(ids)),
        "exact_duplicate_merged_rows": len(rows) - len(set(hashes)),
        "records_with_second_reference": sum(
            bool(str(row.get("target_summary_2", "")).strip()) for row in rows
        ),
        "article_slots_total": sum(count_article_slots(value) for value in merged),
        "article_slots_per_record": _numeric_summary(
            [count_article_slots(value) for value in merged]
        ),
        "input_characters": _numeric_summary([len(value) for value in merged]),
        "input_words": _numeric_summary([len(value.split()) for value in merged]),
        "target_words": _numeric_summary(
            [len(str(row.get("target_summary", "")).split()) for row in rows]
        ),
        "validation_issues": dict(sorted(issues.items())),
    }
