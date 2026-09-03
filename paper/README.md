# Full paper — preprint draft v0.4 (not peer reviewed)

`main.pdf` expands the accepted TIMA/FIMA 2026 abstract into a full programme-theory paper (IMRAD,
two-column). The abstract in `../abstract/` remains the document of record and the claim ceiling:
nothing here claims that T-PHE improves, prevents or reduces any outcome.

- Build: `latexmk -pdf main.tex` (TeX Live with tikz, tabularx, booktabs, hyperref).
- Every reference carries its PubMed identifier; citation accuracy was checked sentence by sentence
  against the PubMed abstracts before this version. The review trail is in `../docs/reports/`.
- `SHA256SUMS` pins the PDF of this version. A revised paper is a new version line in the paper's own
  version history and a new SHA-256 line here.
- Licence: CC BY 4.0, as the repository.
