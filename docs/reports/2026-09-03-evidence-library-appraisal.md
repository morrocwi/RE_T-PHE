# Critical appraisal — evidence library (2026-09-03)

| | |
|---|---|
| **Scope** | Branch `docs/evidence-library`: `tools/build_library.py`, `library/README.md`, category files 01–12, `library/library.json`, `library/kg/`, `library/data/*.json` (search and verification records for six PubMed search angles and seven externally supplied reading lists, all re-fetched by independent verifiers) |
| **Reviewer** | Independent AI reviewer (separate instance from the drafter and from the search/verification agents), adversarial mandate, default *refuted* unless evidenced by file and line |
| **Verdict** | REVISE-THEN-MERGE → findings applied below |

## Findings and resolution

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Must-fix | An internal-project label had leaked into four `evidence_level` fields of the source records and propagated into two category tables and `library.json`, contrary to the medical-register rule. | Removed from the source records; library rebuilt. |
| 2 | Must-fix | One knowledge-graph edge asserted "contradicts P1" for a record whose annotation says "rather than contradicting"; the classifier was a bare substring match. | Classifier made negation-aware; the false edge no longer exists (zero "contradicts" edges remain). |
| 3 | Must-fix | The build was not byte-reproducible (set iteration order in the graph builder). | Iteration sorted; two consecutive builds now produce identical output; CI rebuilds the library and fails on any diff. |
| 4 | Must-fix | The library was not linked from README, `llms.txt` or the AI entry page, and CI did not check it. | Linked from all three; CI step added. |
| 5 | Should-fix | The statement that findings and annotations are AI-drafted readings of abstracts appeared only in the graph overview. | Now stated in the index and in every category file header. |
| 6 | Should-fix | The index did not disclose that verification used PubMed E-utilities only, so WHO and other non-indexed guidance items were checked by identifier, not against the live document. | Disclosed in the index; affected rows already said so. |
| 7 | Nit | Category entries with no data pair were skipped silently. | Builder prints a notice. |

## Candidate problems examined and refuted

FIX-row corrections are real and substantive (spot-checked across categories 01, 02, 05, 06, 09, including the reversed care-seeking finding and the overstated 2018 evidence-report summary); DROP items are framed as "could not be resolved in PubMed", not "does not exist"; national-journal and official-programme sources appear only as context; no personal data, local paths or placeholder e-mail addresses in any library file; no claim-ceiling violation found.

## Status

Findings 1–7 applied and re-verified by rebuilding twice. Merge by pull request after this report is filed.
