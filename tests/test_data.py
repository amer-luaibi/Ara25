import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ara25.data import (
    audit_records,
    count_article_slots,
    iter_json_records,
    normalize_article_markers,
    validate_record,
)


class DataUtilitiesTest(unittest.TestCase):
    def sample(self):
        return {
            "id": "x1",
            "title": "عنوان اصطناعي",
            "Merged_Articles": "<ARTICLE_1><ARTICLE_1>نص أول <ARTICLE_2>نص ثان",
            "target_summary": "ملخص اصطناعي",
            "target_summary_2": "مرجع اصطناعي ثان",
        }

    def test_marker_normalization_and_count(self):
        text = self.sample()["Merged_Articles"]
        self.assertEqual(count_article_slots(text), 2)
        self.assertEqual(normalize_article_markers(text).count("<ARTICLE_1>"), 1)

    def test_validation(self):
        self.assertEqual(validate_record(self.sample(), require_second_reference=True), [])
        broken = self.sample()
        broken["title"] = ""
        self.assertIn("empty:title", validate_record(broken))

    def test_backtick_wrapped_jsonl(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.jsonl"
            path.write_text("`" + json.dumps(self.sample(), ensure_ascii=False) + "\n", encoding="utf-8")
            records = list(iter_json_records(path))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "x1")

    def test_audit_suppresses_text(self):
        report = audit_records([self.sample(), self.sample()])
        rendered = json.dumps(report, ensure_ascii=False)
        self.assertEqual(report["records"], 2)
        self.assertEqual(report["exact_duplicate_merged_rows"], 1)
        self.assertNotIn("نص أول", rendered)


if __name__ == "__main__":
    unittest.main()
