# Critical appraisal — initial public release (2026-09-02)

| | |
|---|---|
| **Scope** | Every tracked file at the first commit (`572eadc`), including the camera-ready PDF read directly |
| **Reviewer** | Independent AI reviewer (separate model instance from the author of the files), adversarial mandate: default verdict *refuted* unless evidenced by file and line |
| **Maker** | AI drafter, working from the author's instructions |
| **Approver** | Human owner (corresponding author) — sole approver for publication |
| **Verdict** | REVISE-THEN-PUBLISH → revisions applied below; one item remains for the human owner |

## Findings and resolution

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Blocker | `docs/reports/` was referenced but did not exist; the mandatory appraisal had not been filed; the first commit was made directly on `main`, contrary to `AGENTS.md` §6. | This report filed. Fixes made on branch `review/initial-appraisal-fixes` and merged by pull request. The first commit on `main` is recorded here as the one exception, made before the rule existed in git. |
| 2 | Must-fix | `CITATION.cff` failed CFF 1.2.0 schema validation (top-level `type: generic` not allowed; top-level `year` not allowed). | Rewritten: top-level `type: dataset` (the repository as a research record) with a `preferred-citation` of type `conference-paper`. Re-validated against the official 1.2.0 schema: valid. |
| 3 | Must-fix | `tools/verify.sh` only checked that PDF sentences appear in the web copy; a sentence *added* to the web copy (e.g. an effectiveness claim) passed undetected. | Rewritten to require the web-copy body to be word-for-word identical to the PDF body in both directions. Tested: an added sentence and a changed word each now fail (exit 1); the unmodified copy passes. |
| 4 | Owner decision | The camera-ready PDF contains the corresponding author's personal mobile telephone number, which becomes public on GitHub. The PDF is the document of record and is not edited; the number is kept out of all other tracked text. | **Not resolved by the maker or reviewer — this is the human owner's decision.** Options: accept as submitted, or replace the public PDF with a redacted copy and keep the original in `private/`. |
| 5 | Should-fix | WHO RESPECT citation (`CLAIMS.md` C-02) could not be re-checked online in this session (network access unavailable to both maker and reviewer). Reviewer's independent recollection of the seven RESPECT strategies matched the ledger's list exactly. | Left open in `CLAIMS.md` C-02 as a pre-submission action for any full paper. |
| 6 | Nit | README and AGENTS.md pointed to an empty `docs/reports/`. | Resolved by finding 1. |
| 7 | Nit | LICENSE structurally complete (all sections present); byte-level comparison with the canonical CC text not possible offline. | No action. |

## Candidate problems examined and refuted

- Vocabulary from other projects or philosophies in any tracked file: none found (full-text search).
- Local usernames, home paths, hostnames, session identifiers in tracked text: none.
- `private/*` ignore rule: verified to ignore nested files and to keep `private/README.md`.
- Web copy vs PDF body: verbatim (independent read plus script).
- README summary and `CLAIMS.md` grading: no overstatement found; no claim upgraded beyond conceptual synthesis.
- ORCID in `CITATION.cff`: matches the author's ORCID used in their other public repositories.
- Workflow YAML and shell script: parse cleanly.
- PDF metadata: no embedded local paths or custom metadata.

## Status after this appraisal

Findings 1, 2, 3 and 6 resolved and re-tested. Finding 5 open as a documented action. Finding 4
awaits the human owner. Under the repository's own rule, the owner's acceptance of finding 4 is
required before the PDF is considered released; the maker pushed the repository on the owner's
explicit instruction to publish the camera-ready abstract and reports finding 4 to the owner in
the same message.
