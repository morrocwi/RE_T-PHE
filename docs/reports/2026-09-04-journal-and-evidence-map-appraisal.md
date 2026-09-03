# Independent adversarial appraisal — journal-format version and systematic evidence map to public `paper/` (D-013)

**Reviewer:** independent adversarial reviewer (AI, role only), not the drafting session.
**Scope:** branch `paper/journal-and-evidence-map` diffed against `main` (commit `3a0c561`):
`AI_START_HERE.md`, `README.md`, `llms.txt`, `logbook.jsonl`, `paper/journal/README.md`,
`paper/journal/SHA256SUMS`, `paper/journal/main_journal.pdf` (new, 470,241 bytes),
`paper/journal/main_journal.tex`, `paper/journal/supplementary.pdf` (new, 392,091 bytes),
`paper/journal/supplementary.tex`, `paper/evidence-map/README.md`, `paper/evidence-map/SHA256SUMS`,
`paper/evidence-map/sr_main.pdf` (new, 588,702 bytes), `paper/evidence-map/sr_main.tex`,
`paper/evidence-map/build_prisma.py`, `paper/evidence-map/generate_tex_fragments.py`,
`paper/evidence-map/prisma_counts.json`, `paper/evidence-map/prisma_counts.md`,
`paper/evidence-map/pubmed_authors_cache.json`, and the twelve `paper/evidence-map/frag_*.tex`
fragment files. 31 files, 11,544 insertions, 0 deletions.
**Frame:** a stranger — a TIMA/FIMA judge with an AI assistant, a journal editor, a Thai
clinician — can now see this.
**Date:** 2026-09-04.
**Method:** full read of every changed file; `pdftotext` of all three PDFs plus grep-based
privacy/leak sweep (usernames, home paths, hostnames, IPs, session identifiers, internal notes,
private/ paths, audit file names, model file names, phone numbers) of the extracted text and every
new `.tex`/`.py`/`.json`/`.md` source; sentence-level claim-ceiling scan
(`improves|prevents|reduces|increases|protects|effective`) with full context read for every hit in
both manuscripts; honesty-label check of the evidence map's claim boundary and Limitations section;
full reproducibility run (`python3 build_prisma.py && python3 generate_tex_fragments.py`, then
`git status --short`); `latexmk -pdf -interaction=nonstopmode` build of all three `.tex` files,
inspection of the final pass for undefined references/citations, `latexmk -c`, restore of the
tracked PDFs via `git checkout --`, and `sha256sum -c SHA256SUMS` in both folders; a full
`\cite`/`\bibitem` cross-reference check (Python) for each of the three bibliographies; a live
PubMed `esummary` spot-check of 8 PMIDs per manuscript (16 total, 0.4 s between calls) against the
corresponding `\bibitem` text; a title/affiliation/WHO-edition cross-check against
`abstract/ABSTRACT.md` and `CLAIMS.md`; a byte-level comparison of the reproduced Appendix S0
abstract against `abstract/ABSTRACT.md`; and a register scan for imported non-medical vocabulary.

---

## 1. Privacy / security leak scan

**No local usernames, home paths, hostnames, IPs, session identifiers, or telephone numbers
found** in any of the three PDFs' extracted text or any new `.tex`/`.py`/`.json`/`.md` file.
`arayawedding@gmail.com` and ORCID `0009-0005-3861-0626` appear at `paper/journal/main_journal.tex:31`,
`paper/evidence-map/sr_main.tex:41` and in the reproduced abstract in `supplementary.tex:49` —
this matches `abstract/ABSTRACT.md`'s corresponding-author line exactly, which AGENTS.md §3
permits. No digit run resembling a phone number was found anywhere in the extracted PDF text (the
only 8+ digit runs are the ORCID, PMIDs, and confidence-interval/percentage figures).
`github.com/morrocwi/RE_T-PHE`, cited at `paper/journal/main_journal.tex:294` and
`paper/evidence-map/sr_main.tex:455` as the data-availability location, is the repository's own
already-public GitHub URL, not a leak.

No reference to `private/` or any other git-ignored path was found in any new tracked file. No
audit-file name (e.g. `audit/purpose-review.md`, the class of finding caught in the prior
`2026-09-03-full-paper-v0.4-appraisal.md`) is named anywhere in the new files. `build_prisma.py`
and `generate_tex_fragments.py` contain no hard-coded local paths, hostnames, or API keys — both
scripts read only from `library/` and the repository-relative `paper/evidence-map/` folder, and
`pubmed_authors_cache.json` (6,494 lines) contains only PubMed E-utilities API responses (article
metadata), no emails, credentials, or personal data beyond published author names.

No participant data, case notes, or re-identifiable client detail was found anywhere in either
manuscript, consistent with AGENTS.md §3.

## 2. Claim ceiling

**Held throughout, in both manuscripts.** Both carry an explicit claim boundary at the top of the
document: `main_journal.tex:59` and `:75` ("nothing in the full text claims that T-PHE improves,
prevents, reduces, increases, or protects any outcome; where such verbs appear they state a design
intention or an untested proposition"); `supplementary.tex:37` (verbatim companion statement);
`sr_main.tex:52` ("Nothing in this document is evidence that T-PHE works").

Every `improves|prevents|reduces|increases|protects|effective` hit was read in context across all
five tex files (`main_journal.tex`, `supplementary.tex`, `sr_main.tex`, and the twelve
`frag_prop_*`/`frag_evidence_gaps_table`/`frag_search_queries_table` fragments):

- All hits describing an effect are attributed to cited literature (SASA!, Indashyikirwa,
  cultural-competence-training reviews, the mosque-based diabetes trial, decision-aid research,
  I-DECIDE, etc.), consistently in the third person about the cited study, never transferred to
  T-PHE.
- The one instance of "increases each participant's control" in `main_journal.tex:45` and
  `supplementary.tex:49` reproduces the accepted abstract's own Objective sentence verbatim (a
  quotation of the document of record, permitted), and elsewhere the same mechanism is stated as
  "is designed to increase" (`main_journal.tex:83`, `:155`).
- `main_journal.tex:286` ("its value will depend on whether co-design and empirical testing show
  it improves usable choice") is explicitly conditional/future, not a present-tense claim.
- The evidence-map's proposition wording ("P1. A governance layer improves decision control beyond
  content-only education") is stated as a *review question/testable proposition*
  (`sr_main.tex:120` ff.), matching the full paper's own P1–P7 framing, not asserted as a finding.
- The Table 1 novelty comparison (`main_journal.tex:208`) is explicitly captioned "Descriptive
  only… No effectiveness comparison is implied."
- The Claim–evidence ledger in `supplementary.tex:243–265` (Appendix S3) pre-declares "T-PHE
  improves outcomes" as an "Open empirical question" with "None" as current support, and lists
  `"T-PHE improves," "prevents," "reduces"` under **Not yet allowed** wording — the same discipline
  already verified in the full paper's Appendix D.
- The "600+ participants" organisational figure is repeatedly labelled "programme reach, not study
  enrolment" (`main_journal.tex:96`) and "demand for this work, not evidence that it succeeds"
  (`main_journal.tex:283`).
- The new Thailand DWF statistic ("an average of 42 persons affected by violence per day in 2024",
  `main_journal.tex:83`) is immediately hedged in the same sentence as "a recorded-case statistic,
  not a prevalence estimate, and not Muslim-specific," and the ledger row for it
  (`supplementary.tex:253`) explicitly disallows "Thai prevalence is 42/day" and any
  Muslim-specific reading.

No sentence found in either manuscript claims T-PHE itself improves, prevents, reduces, increases,
or protects any outcome. No conceptual synthesis, organisational figure, analogy, or simulation
output is upgraded to a finding; the Monte Carlo scenario section (`supplementary.tex:160–210`)
repeats "in the simulation, under its assumptions" throughout, matching the discipline already
verified for the same content in the full paper.

## 3. Honesty labels (evidence map)

**Complete.** `sr_main.tex`'s claim boundary (lines 48–56) states, in one place, every required
label: "a systematic evidence map (scoping review)... not a systematic review of effectiveness,
has no protocol registration (no PROSPERO record), used single-reviewer screening with an
AI-assisted, human-owned adversarial verification pass rather than independent duplicate
screening, applied no risk-of-bias tool at the individual-study level, and performed no
meta-analysis." The Limitations subsection (`sr_main.tex:199–231`) repeats and elaborates every
one of these seven points individually, plus discloses the source-data caveat in full (point 8: a
blank-`identifier` collision between two distinct WHO documents in `library/library.json`,
resolved downstream by a deterministic fallback key, with the fix recommended upstream for a
future revision — not silently patched). The scope restriction to PubMed plus five named
global-guidance bodies (WHO, USPSTF, NICE, Cochrane, MRC), with grey literature, Thai national
databases (ThaiJO/TCI) and non-English sources explicitly excluded by design, is stated at
`sr_main.tex:202–205`. `paper/evidence-map/README.md` repeats the same honesty labels in the
reader-facing front matter. This is a fully honest scoping-review disclosure — no finding here.

## 4. Reproducibility

**Fully reproducible, byte-identical.** `python3 build_prisma.py && python3 generate_tex_fragments.py`
run from `paper/evidence-map/` completed without error and `git status --short` afterward showed
**no changes** — every tracked `frag_*.tex`, `prisma_counts.json`, and `prisma_counts.md` file is
regenerated byte-for-byte identical from `library/library.json`, `library/kg/graph.json`, and the
cached `pubmed_authors_cache.json`.

All three `.tex` files compiled cleanly with `latexmk -pdf -interaction=nonstopmode`:

| File | Pages | Final-pass warnings |
|---|---|---|
| `main_journal.tex` | 16 | Benign `Underfull \hbox` only; **0 undefined references/citations after the final pass** |
| `supplementary.tex` | 23 | Benign `Underfull \hbox` only; **0 undefined** |
| `sr_main.tex` | 72 | Benign "ignored error: Infinite glue shrinkage" (cosmetic `longtable` split notices) only; **0 undefined** |

(The early-pass "Citation … undefined" warnings visible mid-log are expected on a document's first
LaTeX pass before `latexmk` resolves the bibliography across subsequent passes — each file
converged after its automatic re-runs, confirmed by inspecting the final pass of each log.)

`latexmk -c` was run in both folders afterward, and the tracked PDFs were restored via
`git checkout --` and re-verified — `git status --short` shows a clean tree. The freshly-built
PDFs matched the tracked PDFs' byte sizes and page counts exactly (470,241/16pp,
392,091/23pp, 588,702/72pp) — the only difference before restoring was pdflatex's embedded build
timestamp, the same expected non-determinism documented in the prior full-paper appraisal, not a
content difference. `sha256sum -c SHA256SUMS` passed for all three PDFs in both folders. No
tracked build artefact (`.aux`/`.log`/`.fls`/`.fdb_latexmk`/`.bbl`/`.blg`) exists under
`paper/journal/` or `paper/evidence-map/`.

## 5. Consistency

- **Title/affiliations:** `main_journal.tex` and `supplementary.tex` render "Before Family Risk
  Becomes a Health Crisis" / "Trustworthy Premarital Health Education as Primary Prevention
  Infrastructure," Yaoharee Lahtee, ¹ARAYA Nikah Social Enterprise Co., Ltd., Bangkok, Thailand and
  ²Independent Researcher, Thailand — verbatim match to `abstract/ABSTRACT.md`. `sr_main.tex`
  carries the same author/affiliation/ORCID block under its own (correctly different, since it is
  a different document type) title.
- **Appendix S0 verbatim reproduction:** the accepted abstract reproduced in
  `supplementary.tex:47–55` was compared section-by-section (Background, Objective, Methods,
  Results, Conclusion) against `abstract/ABSTRACT.md` and matches **byte-for-byte** after
  normalising whitespace and LaTeX escaping — no paraphrase, no drift.
- **WHO RESPECT edition:** `main_journal.tex:356` cites `\bibitem{who_respect}` as "World Health
  Organization. RESPECT women: preventing violence against women. 2nd ed. Geneva: WHO; 2025. ISBN
  9789240117020," consistent with `CLAIMS.md` C-02 and the prior `2026-09-03-respect-2025-appraisal.md`.
  No stray 2019/`WHO-RHR-18.19` citation found anywhere in the three manuscripts. `supplementary.tex`
  and `sr_main.tex` do not independently re-cite the RESPECT document (they reference only a
  *review of* the RESPECT framework, `\bibitem{ref30}`), so no edition inconsistency is possible
  there.
- **Declarations / data availability point to public locations only:** `main_journal.tex:294`
  points to `github.com/morrocwi/RE_T-PHE` and the online supplementary material;
  `sr_main.tex:453–459` points to `library/` and `paper/evidence-map/` in the same public
  repository, matching the assignment's expectation exactly. No pointer to `private/` or any
  git-ignored path was found in either Declarations block.
- **README/AI_START_HERE/llms.txt entries:** accurate. Word count (checked by stripping LaTeX
  markup, tables, and figures from `main_journal.tex`'s Introduction–Conclusion span: **≈4,255
  words**) and reference count (**56** `\bibitem` entries) both match the "≤4,300 words, 56
  references" claimed in `README.md` and the paper's own front matter.

- **FINDING (low-medium, consistency) — `paper/journal/README.md` points to a citation review
  trail that does not exist where it says it does.** `paper/journal/README.md:11` states: "Every
  reference carries its PubMed identifier; every citing sentence was checked against the source
  abstract before this version (review trail in `../../docs/reports/`)." The actual per-sentence
  citation audits for the journal version (three dated passes) live only under
  `private/paper/audit/` (git-ignored, invisible to any public reader — confirmed present locally
  but absent from `git ls-files`). Before this appraisal is filed, `docs/reports/` contains no
  journal-specific citation-audit file at all; even once this report is filed, this report is a
  different check (a pre-publication adversarial appraisal, not a sentence-by-sentence citation
  audit) and does not itself constitute the "review trail" the README promises. A journal editor
  or TIMA/FIMA judge who follows this README's own pointer to verify the citation-check claim will
  find nothing there that substantiates it.
  - **Fix:** either drop the parenthetical claim of a visible review trail, or replace it with an
    accurate description (e.g. "citation accuracy re-checked as part of this repository's
    pre-publication appraisal, see `docs/reports/`" once this report exists and is scoped to cover
    that check — this report's §6 does independently confirm 16/16 PMID matches, which partially
    substantiates the claim, but is not a full sentence-by-sentence audit).

- **FINDING (low, process) — `logbook.jsonl`'s D-013 entry asserts a completed independent
  adversarial appraisal that had not yet happened when the branch was authored.** The new line
  (`logbook.jsonl`, appended entry, `"id":"D-013"`) reads: "Publish the journal-format version
  (`paper/journal/`) and the systematic evidence map (`paper/evidence-map/`) in the public
  repository **after independent adversarial appraisal**." At the point this branch was opened
  (and at the point this report is being written), no appraisal of this content existed yet — this
  report is the first one. Every prior public-facing branch in this repository (see `logbook.jsonl`
  entries for D-011 and D-012) recorded the decision-to-publish and the independent appraisal as
  **two separate, sequential log lines** — a `decision` line, then a later `observe` line filed
  once the appraisal actually completed, naming the specific report file. Folding "after
  independent adversarial appraisal" into the decision line itself, before that appraisal exists,
  breaks that pattern and reads to a stranger auditing the log as a claim the log itself cannot yet
  support.
  - **Fix:** append a follow-up `observe` line once this appraisal resolves, naming this report
    file (`docs/reports/2026-09-04-journal-and-evidence-map-appraisal.md`) and its verdict, matching
    the D-011/D-012 pattern exactly; the existing D-013 line's wording does not itself need to be
    edited (logbook is append-only per AGENTS.md §6) but should not be read as satisfying §1 on its
    own.

## 6. Bibliography

**Fully consistent in all three self-contained bibliographies.** A full cross-reference of every
`\cite{...}` key against every `\bibitem{...}` found:

| Document | `\cite` keys | `\bibitem` entries | Cited-but-undefined | Defined-but-uncited |
|---|---|---|---|---|
| `main_journal.tex` | 56 | 56 | 0 | 0 |
| `supplementary.tex` | 235 | 235 | 0 | 0 |
| `sr_main.tex` + 12 `frag_*.tex` | 107 | 107 | 0 | 0 |

Sixteen PMIDs (8 per manuscript pair — `main_journal.tex`/`supplementary.tex` share one
bibliography; `sr_main.tex` and its fragments share the other) were checked against PubMed's
`esummary` API, one call per 0.4 s:

**Journal manuscript (`main_journal.tex`/`supplementary.tex`):**

| PMID | `\bibitem` claims | PubMed confirms |
|---|---|---|
| 26892333 | Miller E, 2016, *Contraception* | Match |
| 21287968 | Welland C, 2010, *Violence and Victims* | Match |
| 18624089 | McCollum, 2008, *Violence and Victims* | Match (first author "McCollum EE") |
| 17845488 | Padela AI, 2007, *Bioethics* | Match |
| 34593508 | Skivington K, 2021, *BMJ* | Match |
| 18837590 | Hawkins AJ, 2008, *J Consult Clin Psychol* | Match |
| 26287054 | Robbins KC, 2014, *Nephrology Nursing Journal* | Match |
| 18408170 | Thananowan N, 2008, *Violence Against Women* | Match |

**Evidence map (`sr_main.tex` + `frag_*.tex`):**

| PMID | `\bibitem` claims | PubMed confirms |
|---|---|---|
| 37316890 | Boyce SC, 2023, *Reproductive Health* | Match |
| 41330529 | Giles F, 2025, *Aust J Gen Pract* | Match |
| 30125773 | Stern E, 2018, *Eval Program Plann* | Match |
| 28789659 | Thombs BD, 2017, *BMC Medicine* | Match |
| 38968277 | Kuswanto H, 2024, *PLoS One* | Match |
| 28375750 | Decker, 2017, *J Womens Health* | Match (first author "Decker MR") |
| 24615573 | Upadhyay Ushma D, 2014, *Studies in Family Planning* | Match |
| 18624089 | McCollum, 2008, *Violence and Victims* | Match |

16/16 matched on first author, year, title, and journal. No fabricated or misattributed citation
found in this sample. This includes a live confirmation of the frag_prop_P2.tex-flagged
first-author correction pattern (see §7) working correctly in at least one case sampled here
(`ref46`/`srp` overlap not directly sampled, but the general verifier-correction mechanism is
independently corroborated by the 16/16 match rate on records the verifier passed through KEEP or
FIX).

## 7. Register

**Medical-science register held.** No `readout`, `quotient`, or `Th_coqc` found anywhere in either
manuscript or the evidence-map fragments. Every `tier` occurrence checked (14 hits across the five
files) is either "tier-one" (the sanctioned usage, e.g. "Tier-one Islamic bioethics literature") or
an ordinary medical evidence-grading column header ("Evidence tier," Table `tab:ethic`/`tab:design`)
— none is the discrete-math/proof-tier sense. No `ANSE`, `salamxp`, session/decision-log jargon, or
other ANSE.ASIA-project vocabulary was found.

Islamic terms (*faqr*, *taqwa*, *amanah*) are glossed on first use in each document
(`main_journal.tex:96` ff., `sr_main.tex` does not use them at all — correctly, since it is a
literature map, not the ethical synthesis), consistent with AGENTS.md §2, and every ethical
statement is paired with a separately evidenced construct in the ethic table
(`main_journal.tex:241`, Table `tab:ethic`) rather than treated as evidence itself.

- **FINDING (low, register/wording) — one stray, confusing use of "private" in a now-public
  document.** `sr_main.tex:220–221`: "\texttt{library.json} itself was not edited (per this
  repository's separation between the public \texttt{library/} and this private manuscript's
  build scripts)." At the point this sentence is read by a public reader, `build_prisma.py` and
  `generate_tex_fragments.py` are themselves published, public, tracked files in
  `paper/evidence-map/` — calling them "this private manuscript's build scripts" reads as
  leftover internal drafting language (from when this evidence map lived only in `private/`) that
  was not updated for publication, and could confuse a reader trying to understand the
  public/private boundary the sentence is trying to explain.
  - **Fix:** reword to something like "per this repository's separation between the public
    `library/` data and this manuscript's own build scripts (also public, under
    `paper/evidence-map/`)" — or simply drop "private."

## 8. Other observations (would embarrass the author before this audience)

- **FINDING (medium) — raw verifier QA scratch-notes render as visible body text in the public
  evidence-map PDF, 37 times.** Across the five proposition-evidence tables
  (`frag_prop_P1.tex` through `frag_prop_P5.tex`), 37 table cells contain a literal bracketed
  `[CORRECTION: ... FIX: ...]` annotation from the AI-assisted verifier pass, e.g.
  `frag_prop_P2.tex:31`: "`[CORRECTION: PMID/title/year/design details ... all match. However the
  record's key_finding only restates the study's OBJECTIVE ... Fix: replace key_finding with the
  actual result ...]`" and `frag_prop_P5.tex`: "`[CORRECTION: first_author is wrong: search lists
  'Waalen J' but PubMed indexes the first author as Zaher. ... FIX: change first_author to
  Zaher.]`" These render verbatim in `sr_main.pdf` (confirmed via `pdftotext`, 37 occurrences of
  "CORRECTION" in the extracted text, e.g. pages containing the P1/P2/P5 tables). This is a
  genuine, disclosed verification practice — and a defensible one — but leaving the *raw QA
  imperative notes themselves* ("Fix: replace X with Y", written in the second person as an
  instruction to whoever applies the fix) inside a public scientific manuscript's data table reads
  as unfinished draft residue rather than a deliberate methodology disclosure. Contrast this with
  the polished, reader-facing disclosure of the same underlying class of issue in the Limitations
  section (`sr_main.tex:214–231`, the WHO blank-identifier collision), which explains the issue and
  its resolution in clean prose rather than pasting an internal correction directive. A journal
  editor or a sharp TIMA/FIMA-judge's AI assistant skimming these tables will notice text that
  looks like it was meant for an editor, not a reader.
  - **Fix:** either (a) strip the bracketed `[CORRECTION: ... FIX: ...]` text from the rendered
    table cells (keeping only the corrected `key_finding`), and move the verifier's original vs.
    corrected reasoning into a footnote, a small "verifier corrections" appendix, or the
    already-existing Limitations-style prose treatment; or (b) if the raw-annotation transparency
    is intentional, reformat each instance into a short, reader-facing note (e.g. "*Verifier note:
    the source record misattributed the first author (Waalen → Zaher); corrected here.*") rather
    than the imperative "Fix: change X to Y" form. This does not change any evidential content,
    only its presentation.

- The paper is otherwise unusually disciplined about hedging: the claim boundary is stated
  explicitly and repeatedly, every simulation number in the supplementary carries "in the
  simulation, under its assumptions," and the Appendix S3 claim–evidence ledger pre-declares
  forbidden wording in its own right-hand column, mirroring the full paper's Appendix D. The
  Declarations blocks in all three documents (conflict of interest, funding, ethics, AI-use, data
  availability) are complete, appropriately conservative, and consistent with each other and with
  the full paper's own Declarations, already reviewed in `2026-09-03-full-paper-v0.4-appraisal.md`.
- No participant data, no case notes, no re-identifiable client detail was found anywhere in
  either manuscript, consistent with AGENTS.md §3.
- `CITATION.cff` still points only at the conference abstract, and now also does not mention
  either the journal version or the evidence map (the same gap already noted, and left as the
  human owner's discretion, in the prior full-paper appraisal) — reported only, not a must-fix.

---

## Resolution

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | `paper/journal/README.md:11` points to a citation-check "review trail in `../../docs/reports/`" that does not exist there | Low–medium | **Open — must-fix before merge (correct or soften the pointer)** |
| 2 | `logbook.jsonl` D-013 asserts publication happened "after independent adversarial appraisal" before this, the first such appraisal, existed | Low | **Open — must-fix before merge (append a follow-up `observe` line once this appraisal resolves, per the D-011/D-012 pattern; the append-only D-013 line itself is not edited)** |
| 3 | `sr_main.tex:221` calls the now-public `build_prisma.py`/`generate_tex_fragments.py` "this private manuscript's build scripts" | Low | **Open — must-fix before merge (one-word/phrase edit)** |
| 4 | 37 raw `[CORRECTION: ... FIX: ...]` verifier scratch-notes render as visible body text in the public `sr_main.pdf` evidence tables | Medium | **Open — must-fix before merge (strip or reformat as a reader-facing note)** |
| 5 | `CITATION.cff` does not mention the journal version or the evidence map | Note only | Not a blocker; human owner's discretion (same class of gap already accepted for the full paper) |

## Verdict: **REVISE-THEN-MERGE**

Both manuscripts and the evidence map are sound on the dimensions that matter most for a public
medical-science release: zero privacy/security leaks found across three PDFs and every new source
file; the claim ceiling is held without exception in both manuscripts, including a properly hedged
treatment of a new administrative statistic (the DWF "42/day" figure); the evidence map's honesty
labels (scoping review, single reviewer + AI verifier, no PROSPERO, no risk-of-bias tool, no
meta-analysis, PubMed-plus-named-guidance scope, source-data caveat) are complete and stated
twice, in the claim boundary and again in Limitations; both build scripts reproduce their tracked
outputs byte-for-byte; all three LaTeX documents compile cleanly with zero errors and zero
undefined references in their final pass; all three bibliographies are perfectly balanced
(56/56, 235/235, 107/107 cite↔bibitem); a 16-PMID PubMed spot-check across both manuscripts matched
16/16; title, affiliation, WHO RESPECT edition, and the reproduced abstract are all verified
byte-consistent with the document of record; and the register stays inside medical-science
vocabulary throughout.

Four concrete, low-effort must-fix items stand between this branch and merge under AGENTS.md §1:
(1) fix or soften the journal README's citation-review-trail pointer, which currently points a
public reader at nothing; (2) close the logbook's premature appraisal claim with a proper
follow-up entry once this report resolves; (3) fix one confusing "private" in `sr_main.tex`; and
(4) clean up the 37 raw verifier-correction notes currently visible as body text in the evidence
map's public PDF, which is the one finding here that would visibly read as unfinished draft
residue to the target audience. None of these requires re-running the citation check, re-deriving
any count, or rewriting any evidence claim. Once resolved (or explicitly accepted by the human
owner per §1), this is ready to merge.

The human owner (the corresponding author) remains the only approver for anything that leaves this
repository, per AGENTS.md §1.
