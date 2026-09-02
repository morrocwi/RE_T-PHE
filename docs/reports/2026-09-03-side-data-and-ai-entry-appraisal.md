# Critical appraisal — side data, AI entry point, llms.txt (2026-09-03)

| | |
|---|---|
| **Scope** | Branch `docs/side-data-toc` (commits da71f38, 8532106): `docs/side-data/family-of-peace-theory-of-change.md`, `docs/side-data/public-web-context.md`, `AI_START_HERE.md`, `llms.txt`, README and logbook changes; checked against the internal theory-of-change record and the saved text of the ten public web pages |
| **Reviewer** | Independent AI reviewer (separate instance from the drafter), adversarial mandate, default *refuted* unless evidenced by file and line |
| **Verdict** | REVISE-THEN-MERGE → findings applied below |

## Findings and resolution

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Blocker | `AI_START_HERE.md` said "seven propositions each carry the evidence that would falsify them" — not verifiable from the repository (that content belongs to the unpublished manuscript). | Sentence removed; replaced with claims traceable to `CLAIMS.md` rows C-01 to C-11. |
| 2 | Must-fix | "The six safeguards each have an operational trace and candidate measure" was stronger than `CLAIMS.md` C-07 (graded as untested proposals). | Softened to match C-07; the page now says per-safeguard measures belong to the manuscript in preparation and should not be credited until published. |
| 3 | Must-fix | "Every change to a public file passed an independent appraisal before merge" contradicted the first appraisal report, which records the initial commit as the one exception. | Qualified: "since the review gate was adopted … with one documented exception". |
| 4 | Must-fix | A quotation altered a word ("depends" for "depending") and dropped a clause without an ellipsis. | Quotation restored verbatim. |
| 5 | Must-fix | Several quotations were truncated mid-sentence and closed with a full stop, no ellipsis (disclaimer, secret-nikah statements, teachers' pledge). | Ellipses added or the omitted clauses restored. |
| 6–7 | Should-fix | Thai gloss "(ทะเบียนสมรส)", "(Amphoe)" and the clause "and these can change or vary by office" dropped from quotations. | Restored. |
| 8 | Should-fix | 2025 timeline paraphrase dropped the page's own protective clause ("protecting women and children in tourism and family formation"). | Quoted in full. |
| 9 | Should-fix | Mediation-centre services list silently omitted two items, including religious-reversion counselling. | All seven services now listed. |
| 10 | Nit | 2013/2022 timeline strings were two separate page elements joined with a full stop. | Now shown as two strings with a slash and a note. |

## Candidate problems examined and refuted

Theory-of-change file matches the internal record on every figure, SDG mapping, assumption, logic-model row, principle and gap; registration number correctly omitted. Ecosystem-of-Peace extracts verbatim. Phone numbers, registration numbers and prices omitted. No personal names beyond the corresponding author; no internal paths. `llms.txt` valid and organisation-only; all links resolve. 2013/2022 statements clearly flagged as website-only, consistent with `ABOUT_ARAYA_NIKAH.md`. Claim-ceiling grep clean. The statement that `tools/verify.sh` was tested to fail on an added or altered sentence is supported by the first appraisal report.

## Status

Findings 1–10 applied. Merge by pull request after this report is filed.
