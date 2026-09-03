# Journal-format version (not peer reviewed)

`main_journal.pdf` presents the T-PHE programme theory in the format of a tier-one medical-journal
analysis article: plain descriptive headings, a structured abstract, key messages, a glossary, ≤4,300
words of main text and 56 references, written to be readable by clinicians and public-health officers.
`supplementary.pdf` carries the accepted conference abstract verbatim (S0, the claim ceiling), the
extended evidence review and evidence map (S1), the illustrative scenario modelling (S2), the outcome
matrix and claim–evidence ledger (S3), the operational checklist (S4) and the construct dictionary (S5).

- The abstract in `../../abstract/` remains the document of record; nothing here claims that T-PHE
  improves, prevents or reduces any outcome.
- Every reference carries its PubMed identifier; every citing sentence was checked against the source
  abstract before this version (review trail in `../../docs/reports/`).
- Build: `latexmk -pdf main_journal.tex` and `latexmk -pdf supplementary.tex`.
- `SHA256SUMS` pins both PDFs. Licence: CC BY 4.0, as the repository.
