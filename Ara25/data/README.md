# Data access and release policy

The full Ara25 research archive supplied to the project owner contains merged
news text collected from 131 websites. The archive is not copied into this
public-ready repository because redistribution rights were not included with
the source files.

## Expected local files

- `train_ready_6144.jsonl`: 713 processed records.
- `test_set_dual_reference.jsonl`: 72 evaluation records with a second summary.

Place restricted copies under `data/private/`; that path is ignored by Git.

## Record fields

| Field | Purpose |
|---|---|
| `id` | Project record identifier |
| `title` | Event or topic title |
| `Merged_Articles` | Multiple articles separated with `<ARTICLE_n>` markers |
| `target_summary` | Primary abstractive summary |
| `target_summary_2` | Optional second reference used for evaluation |

## Public release checklist

1. Retain the source URL and collection date for every article.
2. Verify each publisher's terms and the legal basis for redistribution.
3. Remove page chrome, login text, unrelated snippets, and personal data.
4. Deduplicate at event, article, and merged-input levels.
5. Freeze train/validation/test splits before model development.
6. Publish checksums and a machine-readable dataset card.
7. Select a dataset license independently from the source-code license.
8. If full text cannot be redistributed, release metadata, URLs, scripts, and
   authorized summaries instead.

The synthetic example in `sample/` demonstrates the schema without reproducing
third-party news content.
