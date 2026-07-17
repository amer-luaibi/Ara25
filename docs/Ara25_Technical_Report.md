# Ara25: Arabic Long-Context Multi-Document Abstractive Summarization

**Technical Report — Research Artifact Audit and Benchmark Documentation**  
**Version 0.1 · 15 July 2026**

**Author:** Amer A. Al-Dulame  
**Project areas:** Arabic NLP, long-context summarization, multi-document summarization, reproducible evaluation

## Abstract

Ara25 is an event-oriented Arabic summarization research artifact designed for long-context, multi-document abstractive summarization. It combines multiple Arabic news articles related to the same topic or event, preserves document boundaries with numbered markers, and pairs each merged input with an abstractive Arabic summary. A separate 72-record evaluation artifact contains a second reference summary. The submitted project includes five Google Colab experiment notebooks covering mT5, LED, AraT5, AraBERT, and multilingual BERT, together with stored aggregate results.

An audit of the supplied processed training artifact found 713 valid records, 2,259 numbered article slots, a median of three articles per record, a maximum input length of 4,772 whitespace-delimited words, and 131 listed source websites. The audit also found duplicate identifiers, 50 exact duplicate merged inputs, and overlap between evaluation identifiers and the processed training pool. These findings do not invalidate the research direction, but they must be resolved or explicitly documented before claiming a leakage-safe public benchmark. This report therefore separates verified artifact facts, submitted experimental results, and open release requirements.

## 1. Research objective

Ara25 addresses a difficult Arabic NLP setting: generating one coherent abstractive summary from several long, partially redundant, and potentially conflicting news reports. Compared with single-document summarization, the task requires a model to aggregate evidence across sources, reduce duplication, preserve entity and event consistency, and operate over a substantially larger input context.

The project has four practical goals:

1. construct event-level Arabic multi-document inputs from diverse news sources;
2. support long-context processing with a nominal 6,144-token input budget;
3. compare Arabic-specific, multilingual, long-context, and encoder-decoder model families;
4. evaluate generated summaries with lexical and semantic metrics and, for a subset, two human references.

## 2. Positioning and novelty

The broad statement “the first Arabic summarization dataset” is not supportable. Earlier resources include EASC, Arabic data in the MultiLing multi-document summarization corpus, and LANS. Ara25's defensible research contribution is narrower: the combination of event-level multi-document Arabic news, long merged inputs, abstractive summaries, broad source diversity, boundary-aware article packing, five baseline families, and a dual-reference subset.

A publication may use wording such as:

> Ara25 is a new Arabic long-context multi-document abstractive summarization dataset and benchmark. To the best of our knowledge, it is among the first Arabic resources to combine event-level multi-source article clusters, long-context inputs, abstractive targets, and dual-reference evaluation in one benchmark.

The “to the best of our knowledge” clause should remain until a systematic literature review confirms the precise novelty boundary.

## 3. Supplied artifacts

The project archive contained:

- nine raw collection bundles in word-processing format;
- nine intermediate text bundles labeled as JSON/JASON artifacts;
- one processed 713-record JSONL file configured for 6,144-token experiments;
- one 72-record dual-reference evaluation file;
- five Google Colab notebooks;
- one aggregate result document;
- one list of 131 source websites.

The repository preparation retains sanitized notebooks, aggregate metrics, a synthetic schema example, audit utilities, and documentation. Full news text is not copied into the public-ready repository because redistribution permissions were not supplied.

## 4. Dataset structure and audited statistics

Each training record contains an identifier, an event title, a merged sequence of numbered articles, and a primary abstractive summary. Evaluation records add a second reference summary.

| Statistic | Processed pool | Dual-reference artifact |
|---|---:|---:|
| Records | 713 | 72 |
| Unique IDs | 438 | 70 |
| Article slots | 2,259 | 251 |
| Articles per record, median | 3 | 3 |
| Articles per record, maximum | 11 | 5 |
| Input words, median | 1,473 | 1,898.5 |
| Input words, maximum | 4,772 | 4,354 |
| Target words, mean | 193.2 | 192.5 |
| Records with second reference | 0 | 72 |

Article-slot counts are inferred from distinct `<ARTICLE_n>` markers. The processed file contains duplicated adjacent markers such as `<ARTICLE_1><ARTICLE_1>`; the supplied models include normalization code to collapse these repetitions.

Project notes previously described 2,266 collected articles. The processed audit finds 2,259 article slots, a difference of seven. The public dataset paper should reconcile that difference using a canonical raw-document manifest.

## 5. Dataset pipeline

| Stage | Function | Current artifact status |
|---|---|---|
| Source collection | Acquire Arabic reports from multiple publishers | Raw document bundles supplied |
| Event grouping | Associate reports describing the same topic or event | Encoded in titles and merged records; grouping method not yet documented |
| Cleaning | Remove page noise and normalize Arabic text | Partially visible in notebooks; raw captures retain some page chrome |
| Boundary preservation | Insert `<ARTICLE_n>` markers | Present; adjacent duplicates require normalization |
| Summary pairing | Attach primary and optional second abstractive references | Present |
| Split creation | Create train, validation, and test partitions | Relationship among artifacts requires clarification |
| Audit | Validate schema, lengths, duplicates, and leakage | Added in this repository |

## 6. Baseline systems

Five submitted notebooks implement the following families:

| Label | Pretrained checkpoint | Design role |
|---|---|---|
| mT5 | `csebuetnlp/mT5_multilingual_XLSum` | multilingual sequence-to-sequence baseline |
| LED | `allenai/led-base-16384` | native long-context encoder-decoder baseline |
| AraT5 | `UBC-NLP/AraT5-base` | Arabic-focused sequence-to-sequence baseline |
| AraBERT | `aubmindlab/bert-base-arabertv02` | Arabic encoder-decoder with hierarchical inference |
| mBERT | `bert-base-multilingual-cased` | multilingual encoder-decoder with hierarchical inference |

Common controls include random seed 42, beam search, no-repeat n-gram constraints, checkpointing, mixed-precision support, and a nominal 6,144-token input / 512-token output budget. The exact effective context differs by model: BERT-based encoders are constrained by their native window and therefore use chunking or hierarchical inference.

## 7. Evaluation design

The notebooks evaluate lexical overlap and semantic similarity using ROUGE, SacreBLEU, chrF, METEOR, BERTScore, and MoverScore-style calculations. Several reference protocols appear in the experiments:

- score against reference 1;
- score against reference 2;
- average the two reference-level scores;
- use a metric's native multi-reference mode;
- select the better reference for each example.

These measures answer different questions and should not be mixed under one unlabeled score. Selecting the best reference per example is an oracle-style statistic and is normally higher than a fixed-reference score. A final benchmark should designate one primary protocol and report alternative protocols separately.

## 8. Submitted benchmark results

The following values are transcribed from the supplied aggregate result document. They were not regenerated during repository preparation.

| Model | Count | ROUGE-1 | ROUGE-2 | ROUGE-Lsum | BERTScore F1 | MoverScore |
|---|---:|---:|---:|---:|---:|---:|
| mT5 | 72 | **0.1473** | **0.0516** | **0.1392** | **0.8402** | 0.9699 |
| LED | 71 | 0.1089 | 0.0257 | 0.1074 | 0.8333 | **0.9700** |
| AraBERT | 71 | 0.0142 | 0.0001 | 0.0128 | 0.7263 | 0.9569 |
| mBERT | 71 | 0.0000 | 0.0000 | 0.0000 | 0.7279 | 0.9540 |
| AraT5 | 71 | 0.0000 | 0.0000 | 0.0000 | 0.7101 | 0.9575 |

ROUGE values in this table use the first reference. BERTScore is first-reference F1. MoverScore uses the stored best-over-references field. The differing counts prevent a fully controlled ranking. AraT5 and mBERT show zero lexical overlap but non-zero semantic metrics; their generated outputs, decoding constraints, and tokenization should be inspected before publication.

The mT5 notebook also contains later exploratory decoding runs with different metrics. They are valuable experiment history but are not substituted into this primary table because the supplied result sheet identifies the table above as the overall comparison.

## 9. Reproducibility assessment

### Strengths

- fixed random seed in the main notebooks;
- explicit model checkpoints and context budgets;
- stored predictions, metrics, and output paths in the executed artifacts;
- multi-metric and dual-reference evaluation code;
- checkpointing, automatic resume, and mixed-precision controls;
- clear model-family separation across notebooks.

### Open issues

- execution counts were cleared while outputs remained;
- sessions installed different library versions;
- absolute Google Drive paths are embedded in experiment code;
- train/test terminology and split provenance are ambiguous;
- duplicate identifiers and exact duplicate inputs exist;
- evaluation counts differ across models;
- raw and processed checksums were not supplied;
- full model checkpoints and prediction files were not included in the archive.

The repository adds a standard-library audit tool, sanitized notebooks, synthetic schema data, unit tests, aggregate metric files, a model registry, and a reproducibility checklist. Full scientific reproduction still requires authorized data, checkpoints or retraining compute, and one frozen evaluation protocol.

## 10. Data quality, ethics, and release risk

News aggregation can preserve publisher text, personal information, political content, traumatic events, and page-level noise. A responsible public release should:

- record source URL, publisher, timestamp, collection method, and rights basis;
- remove login prompts, navigation text, advertisements, and unrelated snippets;
- offer correction and takedown procedures;
- document geographic, political, topical, and publisher-selection biases;
- separate code, metadata, summaries, source text, and model artifacts under appropriate licenses;
- avoid publishing full third-party articles until redistribution is authorized.

The repository therefore includes only a synthetic sample and non-textual audit metadata.

## 11. Required work before publication

1. Build a canonical manifest with unique event and document IDs.
2. Reconcile 2,259 processed article slots with the reported 2,266 collected articles.
3. Explain or remove repeated IDs and exact duplicate inputs.
4. Freeze leakage-safe train, validation, and test splits.
5. Document event clustering and human-summary creation protocols.
6. Run all baselines from one environment and shared evaluation script.
7. Add human evaluation for factuality, coverage, fluency, and cross-document synthesis.
8. Complete source-rights and dataset-license review.
9. Publish checksums, run manifests, code revision, hardware, and per-example predictions where permitted.
10. Replace the provisional citation with a paper, preprint, or DOI.

## 12. Conclusion

Ara25 is a substantial Arabic NLP research asset with a distinctive long-context, multi-document, abstractive design and a useful collection of model experiments. Its strongest current value is not an unqualified “first” claim, but the concrete combination of event-level multi-source inputs, long context, human summaries, dual-reference evaluation, and transparent baseline work. The audit findings provide a credible path from an ambitious private research archive to a defensible public benchmark and portfolio artifact.

## References

1. El-Haj, M., Kruschwitz, U., and Fox, C. EASC: Essex Arabic Summaries Corpus. Repository: https://github.com/ArabicNLP-UK/EASC
2. Li, L. et al. (2013). *Multi-document multilingual summarization corpus preparation, Part 1: Arabic, English, Greek, Chinese, Romanian.* MultiLing 2013. https://aclanthology.org/W13-3101/
3. Alhamadani, A. et al. (2023). *LANS: Large-scale Arabic News Summarization Corpus.* ArabicNLP 2023. https://aclanthology.org/2023.arabicnlp-1.8/
4. Wolhandler, R. et al. (2022). *How “Multi” is Multi-Document Summarization?* EMNLP 2022. https://aclanthology.org/2022.emnlp-main.389/
