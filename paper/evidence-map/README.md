# Systematic evidence map (scoping review, PRISMA-ScR)

`sr_main.pdf` maps the evidence library in `../../library/` against the seven propositions of the
T-PHE programme theory. It is a scoping review: structured, logged PubMed searches per category, a
single reviewer with an AI-assisted adversarial verifier pass, no protocol registration, no
risk-of-bias assessment at study level, no meta-analysis, and no inference about the effectiveness
of T-PHE.

- Every number in the manuscript is produced by `build_prisma.py` (counts → `prisma_counts.json`,
  `prisma_counts.md`) and `generate_tex_fragments.py` (tables and bibliography fragments →
  `frag_*.tex`) from `library/library.json`, `library/kg/graph.json` and `library/data/*.json`.
  Author fields for newly cited records come from PubMed and are cached in
  `pubmed_authors_cache.json`, so the build reproduces offline.
- Rebuild: run the two scripts from this folder, then `latexmk -pdf sr_main.tex`.
- Known source-data issue: two WHO documents share a blank identifier in `library.json`; the scripts
  use a fallback key and the manuscript discloses it in Limitations.
- `SHA256SUMS` pins the PDF. Licence: CC BY 4.0, as the repository.
