# AGENTS.md — rules for every contributor (human or AI) to RE_T-PHE

This is a **public medical-science research repository**. Read this file before changing anything.

## 1. Independent critical appraisal before every merge — no exceptions

- Every change that touches a public-facing file (`README.md`, `CLAIMS.md`, `abstract/`,
  `CITATION.cff`, `docs/`) is reviewed by someone other than its author before it merges.
  An AI that drafted a change does not review that change. Self-review has no standing as a gate.
- The reviewer's mandate is adversarial: find what is wrong, missing, overstated, unsupported,
  unsafe, or a privacy exposure. Default verdict is *revise* until each finding is resolved or
  explicitly accepted by the human owner.
- Each completed appraisal is filed as a dated report in `docs/reports/` with: scope reviewed,
  findings, resolution of each finding, and the reviewer's identity (role, not personal name for
  AI reviewers).
- The human owner (the corresponding author) is the only approver for anything that leaves this
  repository: a conference submission, a manuscript, a public statement.

## 2. Language standard: medical science only

- Write in the register of public health, preventive medicine and health-promotion research:
  intervention, programme theory, mechanism, outcome domain, process measure, level of evidence,
  safeguarding, referral, critical appraisal, prospective evaluation.
- Do **not** import working vocabulary from other projects or philosophies into this repository
  (with the one declared exception below). A reader from a medical faculty must be able to read every
  file without a glossary.
- **Declared exception — the work's own Islamic ethical frame.** The abstract names limited knowledge,
  entrusted responsibility, human dignity, just boundaries and repair; the manuscript names them as
  *faqr*, *taqwa*, *amanah*, *ʿadl* (and *shura* for consultation). These terms may be used as the named
  ethical frame, always with a plain-language gloss on first use in each file, and never as evidence: every
  ethical statement is paired with the medical or public-health evidence it governs.
- **Admission tiers for Islamic medical-ethics and Muslim-health sources** (library category 18), all of
  which must be PubMed-indexed: (i) systematic review or meta-analysis; (ii) clinical or professional
  guideline recorded by PubMed as such; (iii) randomised trial; (iv) article in a leading general,
  specialty or medical-ethics journal (the category file names the journal and the reason);
  (v) a labelled carve-out for the professional-association journal of the convention's umbrella body
  (Journal of the Islamic Medical Association), shown as "carve-out" in the record. Opinion pieces and
  lower-tier journals are excluded.
- Grade every claim by evidence type as in `CLAIMS.md`. Never upgrade a conceptual synthesis to
  a finding, or an organisational figure to a verified count.

## 3. Privacy and safeguarding

- **No participant data, ever.** No names, records, case notes, quotes, or re-identifiable details
  from any couple, family, educator or referral. Aggregate organisational figures only, labelled as
  organisation-reported.
- No personal telephone numbers in tracked text files. (The camera-ready PDF is kept as the
  document of record exactly as submitted; do not add its contact details elsewhere.)
- No local file paths, usernames, hostnames, session identifiers or internal notes in tracked
  files. Working material belongs in `private/` (git-ignored) — see §5.
- Nothing here is clinical advice. Where content touches suspected violence or coercive control,
  the only acceptable direction is to qualified, survivor-centred services.

## 4. Document of record

- `abstract/TIMA-FIMA_2026_Abstract_FINAL_Yaoharee_Lahtee.pdf` is the camera-ready submission.
  Do not edit or replace it. A revised abstract is a new file with a new SHA-256 line, and the
  old file stays.
- `abstract/ABSTRACT.md` is a verbatim web copy. `tools/verify.sh` checks it against the PDF; run
  it before every commit that touches `abstract/`.

## 5. Working area

- `private/` is git-ignored. Put data, strategy notes, drafts, reviewer correspondence and anything
  not ready for the public there. It is never committed. Back it up outside git.

## 6. Git workflow

- Never commit directly to `main`. Branch, open a pull request, obtain the independent appraisal
  (§1), then merge.
- `logbook.jsonl` is append-only. Record what was done while doing it; correct an earlier line with
  a new `correction` line, never by editing.

## 7. When in doubt

Round up: if a change might reach a reader outside this repository, treat it as public-facing and
apply §1 in full.
