# Reproducibility guide

## Levels of reproducibility

The repository distinguishes three levels:

1. **Artifact audit** — reproducible locally with standard Python and synthetic
   data.
2. **Metric reproduction** — requires stored predictions and authorized
   reference summaries.
3. **Model reproduction** — requires the full authorized dataset, pretrained
   model downloads, a CUDA environment, and significant compute.

## Recommended environment

- Python 3.10 or 3.11
- CUDA-capable GPU with recent PyTorch support
- Hugging Face Transformers 4.44 or newer, below major version 5
- Fixed seed: 42

Create an environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-colab.txt
```

## Data validation

```bash
python scripts/audit_dataset.py data/private/train_ready_6144.jsonl \
  --output data/private/train_audit.json
```

The audit does not print source text. Resolve duplicate IDs and exact duplicate
inputs before freezing splits.

## Experiment controls

For every run, record:

- Git commit hash;
- data checksum and split manifest;
- model checkpoint and revision;
- package lock or environment export;
- hardware and precision mode;
- seed, batch size, gradient accumulation, and learning rate;
- decoding parameters;
- prediction file checksum;
- aggregate and per-example metrics.

## Evaluation protocol

Use one shared script for all models. Report each reference separately and then
state explicitly whether a multi-reference score is an average, maximum, or
metric-native multi-reference computation. Do not select the best reference per
sample without labeling that result as an oracle-style upper-bound statistic.

The stored notebooks calculate several of these variants. A paper should choose
one primary protocol before comparing systems.
