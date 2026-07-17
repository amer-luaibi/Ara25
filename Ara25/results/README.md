# Stored benchmark results

`baseline_metrics.csv` transcribes the values in the supplied `Row Results.docx`.
They are preserved as submitted evidence and were not independently regenerated
during repository preparation.

Important comparison notes:

- mT5 reports 72 examples; all other model entries report 71.
- The CSV uses first-reference ROUGE values and the stored best-reference
  MoverScore field.
- mT5 has additional exploratory decoding runs embedded in its original notebook;
  those are not substituted into the primary table.
- A final paper should rerun every model against one frozen split and one shared
  evaluation implementation.
