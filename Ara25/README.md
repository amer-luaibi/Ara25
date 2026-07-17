# Ara25

**An Arabic long-context, multi-document abstractive summarization dataset and benchmark.**

Ara25 groups Arabic news articles that describe the same event, merges each group into a traceable long-context input, and pairs the input with an abstractive Arabic summary. The accompanying benchmark evaluates five model families: mT5, LED, AraT5, AraBERT, and multilingual BERT.

> **Release status:** research preview. The code, documentation, synthetic schema example, and aggregate benchmark results are prepared for public review. Full news text is intentionally excluded pending source-licensing and redistribution review.

## Why Ara25

Arabic summarization resources are commonly designed around a single article, extractive targets, or short input windows. Ara25 explores a more demanding setting:

- multiple news articles per event;
- long merged Arabic inputs, configured for up to 6,144 tokens;
- abstractive target summaries;
- a dual-reference evaluation subset;
- long-context and encoder-decoder baselines;
- reproducible data and experiment auditing.

Ara25 should currently be described as **a new Arabic long-context multi-document abstractive summarization resource**, not as the first Arabic summarization dataset without qualification. Earlier Arabic extractive, single-document, and multilingual multi-document resources exist; the narrower novelty claim requires a formal literature review.

## Audited snapshot

| Property | Audited value |
|---|---:|
| Processed records | 713 |
| Unique record IDs | 438 |
| Source websites listed | 131 |
| Article slots detected from markers | 2,259 |
| Articles per record, median / maximum | 3 / 11 |
| Input words, median / maximum | 1,473 / 4,772 |
| Target-summary words, mean | 193 |
| Dual-reference evaluation records | 72 |
| Baseline model families | 5 |

The audit detected repeated IDs and 50 exact duplicate merged inputs. These are documented rather than silently removed. See [`docs/AUDIT_FINDINGS.md`](docs/AUDIT_FINDINGS.md) and run the audit tool before training.

## Benchmark snapshot

The table below reproduces the aggregate values stored with the submitted experiment artifacts. The experiments were **not retrained in this repository build**.

| Model | ROUGE-1 | ROUGE-2 | ROUGE-Lsum | BERTScore F1 | MoverScore |
|---|---:|---:|---:|---:|---:|
| mT5 | **0.1473** | **0.0516** | **0.1392** | **0.8402** | 0.9699 |
| LED | 0.1089 | 0.0257 | 0.1074 | 0.8333 | **0.9700** |
| AraBERT | 0.0142 | 0.0001 | 0.0128 | 0.7263 | 0.9569 |
| mBERT | 0.0000 | 0.0000 | 0.0000 | 0.7279 | 0.9540 |
| AraT5 | 0.0000 | 0.0000 | 0.0000 | 0.7101 | 0.9575 |

Values use the first human reference for ROUGE and the stored first-reference/best-reference summaries for semantic metrics, following the submitted result sheet. Evaluation counts differ: mT5 reports 72 items, while the other four baselines report 71. This discrepancy is an open reproducibility item.

## Repository layout

```text
Ara25/
├── configs/                 # model registry and experiment defaults
├── data/                    # dataset card, audit metadata, synthetic example
├── docs/                    # report, reproducibility notes, audit findings
├── notebooks/               # sanitized Colab experiment notebooks
├── results/                 # aggregate benchmark metrics
├── scripts/                 # notebook sanitizer and dataset audit CLI
├── src/ara25/               # reusable data-loading and audit utilities
└── tests/                   # lightweight unit tests
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m unittest discover -s tests -v
```

Audit a local Ara25 file without printing any article text:

```bash
python scripts/audit_dataset.py /path/to/train_ready_6144.jsonl
```

To reproduce model experiments, install the GPU/benchmark dependencies:

```bash
python -m pip install -r requirements-colab.txt
```

Then open a notebook, set the dataset and output paths in its configuration cell, and run it in a CUDA-enabled environment.

## Data schema

Training record:

```json
{
  "id": 1,
  "title": "Event title",
  "Merged_Articles": "<ARTICLE_1> ... <ARTICLE_2> ...",
  "target_summary": "Human abstractive summary"
}
```

The evaluation schema adds `target_summary_2` as a second human reference. A copyright-safe synthetic example is provided in [`data/sample/synthetic_sample.jsonl`](data/sample/synthetic_sample.jsonl).

## Data access and responsible release

The supplied research archive contains full articles collected from 131 news websites. Public redistribution rights were not included with the archive. Consequently:

- raw article text is excluded from this public-ready repository;
- source URLs and collection provenance should be retained privately;
- a release should include only content that is licensed, authorized, or otherwise legally redistributable;
- personal data, credentials, model checkpoints, and private Drive paths must not be committed.

See [`data/README.md`](data/README.md) for the proposed release process.

## Reproducibility notes

- The notebooks were developed for Google Colab and CUDA hardware.
- Public copies have outputs and volatile notebook metadata removed.
- Original experiments use fixed random seed `42`.
- Input and output budgets are generally 6,144 and 512 tokens.
- Exact package versions varied across the original sessions; the supplied requirements define a clean baseline environment.
- Stored metrics are reported transparently, including failed or zero-overlap baselines.

## Related Arabic summarization resources

- [EASC](https://github.com/ArabicNLP-UK/EASC): an early Arabic corpus with human extractive summaries.
- [MultiLing 2013 multi-document corpus](https://aclanthology.org/W13-3101/): multilingual multi-document summarization data including Arabic.
- [LANS](https://aclanthology.org/2023.arabicnlp-1.8/): a large-scale Arabic news summarization corpus primarily organized as article-summary pairs.

These resources motivate a careful novelty statement centered on Ara25's **combination** of event-level multi-document inputs, long context, abstractive summaries, multi-source Arabic news, and a dual-reference subset.

## Citation

Until a paper or DOI is available, cite the software artifact using [`CITATION.cff`](CITATION.cff). Replace the provisional citation when the associated manuscript is published.

## Author

**Amer A. Al-Dulame**  
AI Researcher and Machine Learning Engineer  
Permanent Member, Iraqi National Artificial Intelligence Team

## License

Copyright © 2026 Amer A. Al-Dulame. All rights reserved. A public open-source and dataset license has not yet been selected. See [`LICENSE`](LICENSE).
