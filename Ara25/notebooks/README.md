# Experiment notebooks

| Notebook | Model family | Base checkpoint | Context strategy |
|---|---|---|---|
| `Ara25_mT5.ipynb` | mT5 | `csebuetnlp/mT5_multilingual_XLSum` | Seq2seq, 6,144-token configuration |
| `Ara25_LED.ipynb` | LED | `allenai/led-base-16384` | Native long-context encoder-decoder |
| `Ara25_AraT5.ipynb` | AraT5 | `UBC-NLP/AraT5-base` | Seq2seq |
| `Ara25_AraBERT.ipynb` | AraBERT | `aubmindlab/bert-base-arabertv02` | Hierarchical encoder-decoder |
| `Ara25_mBERT.ipynb` | mBERT | `bert-base-multilingual-cased` | Hierarchical encoder-decoder |

These public copies retain the submitted code but remove stored outputs and
volatile metadata. They still contain Colab-oriented configuration cells and
must be pointed at an authorized local dataset before execution.

The notebooks capture research history rather than a single production API.
Before publication, extract the shared preprocessing, generation, and evaluation
logic into tested modules and rerun all models from one locked environment.
