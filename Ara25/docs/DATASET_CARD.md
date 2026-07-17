# Dataset card: Ara25 research preview

## Dataset summary

Ara25 is an event-oriented Arabic news summarization resource. Each processed
record combines multiple articles about a shared topic or event and pairs the
merged input with an abstractive Arabic summary. A 72-record artifact adds a
second reference summary.

## Intended uses

- Arabic long-context summarization research;
- multi-document summarization and evidence aggregation;
- robustness and factual-consistency evaluation;
- benchmarking long-context and hierarchical generation systems.

## Out-of-scope uses

- production deployment without factuality and safety validation;
- redistributing publisher text without authorization;
- inferring sensitive attributes or profiling individuals;
- presenting generated summaries as verified journalism.

## Languages and domains

- Language: primarily Modern Standard Arabic, with noisy multilingual page text
  in some collected articles.
- Domain: news and web-published current-affairs content.
- Sources: 131 websites listed in the supplied provenance document.

## Structure

Inputs contain numbered `<ARTICLE_n>` markers. The processed data is configured
for a 6,144-token model budget. Summaries are abstractive and substantially
shorter than the merged inputs.

## Known limitations

- duplicate IDs and duplicate merged inputs;
- uncertain separation between the 713-record pool and 72-record evaluation set;
- page chrome and unrelated site text in some raw captures;
- publisher and redistribution rights require review;
- topic, geography, political-event, and source-selection biases;
- possible temporal and entity leakage between related events;
- limited human-reference count outside the 72-record artifact.

## Personal and sensitive information

News articles can mention identifiable people and sensitive events. A release
must document the collection basis, minimize unnecessary personal data, and
provide a correction or takedown process.

## Licensing

No dataset license is asserted in this research preview. Source-code licensing,
dataset licensing, publisher rights, pretrained-model licenses, and report
licensing should be handled separately.
