# Ara25 audit findings

This audit describes the supplied processed artifacts. It is not a judgment on
the intended sampling design; repeated records may have been introduced for a
training or packing purpose that was not documented in the archive.

## Processed training file

- 713 valid JSONL records.
- 438 unique values in the `id` field.
- 50 exact duplicate `Merged_Articles` strings.
- 2,259 article slots inferred from distinct `<ARTICLE_n>` markers.
- Median of 3 and maximum of 11 article slots per record.
- Median input length of 1,473 whitespace-delimited words; maximum 4,772.
- Mean target-summary length of approximately 193 words.

The project description previously referenced 2,266 collected articles. The
processed marker audit finds 2,259 article slots, so the seven-item difference
should be reconciled against the raw collection manifest before publication.

## Dual-reference evaluation file

- 72 parseable records after removing a leading Markdown backtick.
- 70 unique IDs.
- All evaluation IDs occur in the processed training artifact.
- All 72 records include `target_summary_2`.

The relationship between the 72-item evaluation file and the 713-record artifact
must be documented clearly. If it is intended as a held-out test set, it should
not also appear in the training pool. If it is the validation split generated
inside the notebooks, call it validation rather than test.

## Experiment artifacts

- Five notebooks are valid notebook JSON files.
- Execution counts are cleared, but stored outputs remain in the supplied copies.
- The result sheet reports 72 evaluated items for mT5 and 71 for the other models.
- Several sessions installed different package versions.
- mT5 contains multiple evaluation runs; the repository benchmark table uses the
  values recorded in the supplied `Row Results.docx`.
- AraT5 and mBERT report zero lexical overlap despite non-zero semantic metrics;
  generated text and tokenization should be inspected before treating these as
  final benchmark values.

## Required actions before a paper or public dataset release

1. Define the canonical unit: record, event, document cluster, or packed sample.
2. Assign stable unique event and document identifiers.
3. Reconcile the 2,259 / 2,266 article counts.
4. Remove or explicitly justify duplicate records.
5. create leakage-safe, immutable train/validation/test splits.
6. Re-run all baselines from one environment and one evaluation script.
7. Publish per-run manifests, checksums, hardware, runtime, and random seeds.
8. Complete copyright, publisher-terms, and dataset-license review.
