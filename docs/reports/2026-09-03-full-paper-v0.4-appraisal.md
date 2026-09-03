# Independent adversarial appraisal — full paper preprint draft v0.4 to public `paper/` (D-012)

**Reviewer:** independent adversarial reviewer (AI, role only), not the drafting session.
**Scope:** branch `paper/full-paper-v0.4` (commit `899f88e`) diffed against `main` (`a56c880`):
`AI_START_HERE.md`, `README.md`, `llms.txt`, `logbook.jsonl`, `paper/README.md`,
`paper/SHA256SUMS`, `paper/main.pdf` (new, 735,996 bytes), `paper/main.tex`,
`paper/sections/appendix_extended_evidence.tex`, `paper/sections/discussion_4_2.tex`,
`paper/sections/discussion_4_2_supplement.tex`, `paper/sections/discussion_delivery.tex`,
`paper/sections/discussion_novelty.tex`, `paper/sections/fig_dag.tex`,
`paper/sections/intro_1_3.tex`, `paper/sections/refs_all.tex`, `paper/sections/results_model.tex`.
**Frame:** a stranger, including a TIMA/FIMA judge with an AI assistant, can now see this.
**Date:** 2026-09-03.
**Method:** full read of the diff and every new/changed file; `pdftotext paper/main.pdf -` and
grep-based privacy/leak sweep of the extracted text and every `.tex` source (usernames, home
paths, hostnames, IPs, session identifiers, internal notes, phone numbers, emails); sentence-level
claim-ceiling scan (`improves|prevents|reduces|effective|works`) with context read for every hit;
cross-check of title/affiliations/corresponding email against `abstract/ABSTRACT.md`; cross-check
of WHO RESPECT citation against `CLAIMS.md` C-02; `sha256sum paper/main.pdf` against
`paper/SHA256SUMS`; full LaTeX build (`latexmk -pdf -interaction=nonstopmode main.tex`, then
`latexmk -c`, then `git checkout -- paper/main.pdf` to restore the tracked PDF exactly, confirmed
by re-hashing); `git status --short` for stray build artefacts; a full `\cite`/`\bibitem`
cross-reference check (Python, all 242 keys); a live PubMed `esummary` spot-check of 10 PMIDs
(0.4 s between calls) against the corresponding `\bibitem` text; a full read of every new section
file for register and internal consistency.

---

## 1. Privacy / security leak scan

**No local usernames, home paths, hostnames, IPs, session identifiers, or telephone numbers found**
in `paper/main.pdf` text or any new `.tex` file. `arayawedding@gmail.com` and ORCID
`0009-0005-3861-0626` appear at `paper/main.tex:49` — this matches `abstract/ABSTRACT.md:16`
("Corresponding Author: Yaoharee Lahtee — arayawedding@gmail.com") exactly, which AGENTS.md §3
explicitly permits ("the corresponding-author email is allowed as in the abstract"). No phone
number found anywhere in the paper text (grep for digit runs returned only PMIDs, ISBNs, years,
and the ORCID).

- **FINDING (medium) — internal working-file paths disclosed in the public PDF's own version-history
  table.** `paper/main.tex:286` and `paper/main.tex:287` name `audit/purpose-review.md` and
  `audit/v0.4-editlist.md` as the review artefacts behind Paper v0.2 and v0.4. Both files exist
  only under `private/paper/audit/` (git-ignored, confirmed via `git ls-files | grep -i audit` and
  `find . -iname audit`), i.e. they are internal working notes that no reader of the public PDF can
  ever open. This is exactly the class of finding AGENTS.md §1's cited incident (a two-week
  license/internal-path leak on a sibling repo, caught only once an adversarial framing was
  applied) warns about: a stranger — including a TIMA/FIMA judge — sees a named file path that
  points at material deliberately kept out of their reach, which reads as either a broken link or
  an invitation to go looking for something not meant to be public. Neither the sentence's content
  (a description of what changed) nor the reviewer identities are the problem; the literal path
  string is.
  - **Fix:** replace `(audit/purpose-review.md)` and `(audit/v0.4-editlist.md)` with a
    parenthetical that names the review only descriptively (e.g. "(internal purpose-review pass)"
    / "(internal editlist from the merged adversarial-review pass)"), or drop the parenthetical
    entirely — the surrounding prose already describes what changed.

- **FINDING (medium) — a real, named private individual credited by full name with no visible
  consent trail.** `paper/main.tex:192`, Declarations → Acknowledgements: "The author thanks
  [a named private individual] for her support during the development of this work." This name does not
  appear anywhere else in the tracked repository (abstract, `CLAIMS.md`, `ABOUT_ARAYA_NIKAH.md`,
  or elsewhere) — it is a first-time public disclosure of a private individual's full name in a
  document that will be indexed and circulated at a scientific convention. AGENTS.md §3 ("No
  participant data, ever… no re-identifiable details from any couple, family, educator or
  referral") is written for study participants, not acknowledgements, so this is not a strict
  violation of that clause on its face — but naming a private person publicly without an on-record
  consent step is exactly the kind of exposure an adversarial privacy pass exists to catch, and
  nothing in this repository documents that consent was sought or given.
  - **Fix:** before merge, the human owner should confirm (and ideally record, in `private/`,
    not in the public tree) that [a named private individual] has consented to this public, named
    acknowledgement. If consent is not confirmed, remove the name or replace it with a role-only
    acknowledgement.

No other privacy/security leak found. `paper/README.md`, `README.md`, `AI_START_HERE.md`,
`llms.txt`, and `logbook.jsonl` additions are all clean of local-machine artefacts.

## 2. Claim ceiling

**Held throughout.** The full text explicitly states the claim ceiling twice in the reader-facing
front matter (`paper/README.md`: "nothing here claims that T-PHE improves, prevents or reduces any
outcome"; `paper/main.tex:50`, Discussion §4.1: "nothing in the full text claims that T-PHE
improves, prevents, or reduces any outcome"), and the embedded Appendix D claim–evidence ledger
(`paper/main.tex:258`) explicitly lists `"T-PHE improves," "prevents," "reduces"` as **not yet
allowed** wording. Every `improves`/`prevents`/`reduces`/`effective` hit found by grep in the PDF
text was checked in context:

- The seven testable propositions (P1–P7, Table 3, `discussion_delivery`/`appendix_extended_evidence`)
  frame every "improves"/"prevents" verb as part of a *falsifiable proposition* or its *falsifying
  evidence*, never as a stated result about T-PHE.
- The Monte Carlo/scenario-simulation section (Appendix F, `discussion_delivery.tex`) repeats "in
  the simulation, under its assumptions" before every numeric ranking, states explicitly "This is
  a result of the assumptions coded into the model, not empirical data about any delivered
  programme… nothing here is an effectiveness estimate," and is disclosed in Methods
  (`paper/main.tex:108`) and Data availability (`paper/main.tex:189`). This is the correct
  treatment of a simulation output — it is not upgraded to a finding anywhere.
- "Improves"/"reduces"/"effective" hits inside cited literature (SASA!, Indashyikirwa, myPlan,
  I-DECIDE, mosque-based diabetes trial, cultural-competence training reviews, etc.) describe what
  *those cited studies* found about *other* interventions, consistently attributed to the source
  study, never transferred to T-PHE.
- Conclusion (`paper/main.tex:181`) and the standpoint paragraph (`discussion_novelty.tex:77`)
  both explicitly hedge future value as conditional on "co-design and empirical testing," and state
  outright "not… a claim that T-PHE works."

No sentence found claiming T-PHE itself improves, prevents, reduces, or is effective. No conceptual
synthesis, organisational figure (the "600+ participants" figure is repeatedly labelled "programme
reach, not study enrolment" / "not evidence that it succeeds"), analogy, or simulation output is
upgraded to a finding.

- **FINDING (low, consistency not ceiling) — internal contradiction about what is and is not cited
  under the "PubMed-only" scope.** `appendix_extended_evidence.tex:16` states: "Two frequently
  cited works in this literature — Fawcett et al. (2010, *Family Relations*) and Carroll & Doherty
  (2003) — are not indexed in PubMed and are therefore not cited under this review's PubMed-only
  citation scope." This is only half true: Carroll & Doherty (2003) indeed has no `\cite` or
  `\bibitem` anywhere in the paper. But Fawcett et al. (2010) *is* cited — `discussion_novelty.tex`
  row "Relationship/marriage education (MRE, PREP)" contains `\cite{ref6,ref7,fawcett2010}`, and
  `refs_all.tex:246` carries a full `\bibitem{fawcett2010}` explicitly flagged
  `[Not PubMed-indexed; cited for transparency only.]`. The flagged bibitem is good practice, but
  the appendix sentence flatly asserting Fawcett is "not cited" is factually wrong given the same
  document cites it two pages later — the kind of self-contradiction a sharp reviewer (or an AI
  assistant cross-checking citations for a judge) will catch immediately.
  - **Fix:** correct the appendix sentence, e.g.: "Carroll & Doherty (2003) is not indexed in
    PubMed and is not cited under this review's PubMed-only scope; Fawcett et al. (2010) is also
    not PubMed-indexed but is cited once, transparently flagged, in Table [novelty] for its
    field-standard status."

## 3. Register

**Medical-science register held.** No vocabulary imported from other ANSE.ASIA projects was found:
no `readout`, `quotient`, `Th_coqc`, `tier` used in the discrete-math/proof sense, no `ANSE`,
`salamxp`, or session/decision-log jargon anywhere in the paper text. "Tier-one" (as in "tier-one
Islamic bioethics literature") and "evidence tier" are used in the ordinary medical-evidence-grading
sense consistent with `AGENTS.md` §2 and `CLAIMS.md`'s own evidence-type column, not as borrowed
formal-proof vocabulary — this is legitimate register, not a violation.

Islamic terms (*faqr*, *taqwa*, *amanah*, *shura*, *'adl*) are used exactly as the declared
exception in AGENTS.md §2 permits: each is glossed in plain language on first use in the compiled
document (`paper/main.tex:111`, `:148`, `:150`), the construct dictionary (Appendix A) and the
figure caption (`fig_dag.tex`) each carry their own inline gloss, and every rule the terms govern
is paired in Table (ethic) with a separately evidenced construct rather than treated as evidence
itself (`paper/main.tex:150`, `discussion_4_2.tex`: "the ethical frame… is presented as a declared
duty rather than as evidence"). Because the whole paper compiles into one continuous document, a
gloss stated once near the start and referenced later within the same PDF is standard academic
practice, not a violation of the "gloss on first use in each file" rule (which targets separately
standalone repo documents such as `README.md`/`CLAIMS.md`).

## 4. Consistency

- **Title/affiliations:** identical to the abstract. `paper/main.tex:44-49` renders "Before Family
  Risk Becomes a Health Crisis" / "Trustworthy Premarital Health Education as Primary Prevention
  Infrastructure," ¹ARAYA Nikah Social Enterprise Co., Ltd., Bangkok, Thailand and ²Independent
  Researcher, Thailand — verbatim match to `abstract/ABSTRACT.md`.
- **WHO RESPECT edition:** cited as 2nd ed., 2025 (ISBN 9789240117020) consistently in
  `paper/sections/refs_all.tex:245` (`\bibitem{who_respect}`), `discussion_4_2.tex`,
  `discussion_novelty.tex`, and `CLAIMS.md` C-02 (already fixed under D-011 and re-verified in the
  prior `2026-09-03-respect-2025-appraisal.md`). No stray 2019/WHO-RHR-18.19 citation found in the
  new paper text.
- **README/AI_START_HERE/llms.txt entries:** accurate. All three correctly state "preprint draft
  v0.4," "not peer reviewed," and that the abstract remains the document of record / claim ceiling.
  `AI_START_HERE.md`'s numbered list was correctly renumbered end-to-end (3→7) when the new item 3
  was inserted — verified no orphaned or duplicate item numbers.
- **`paper/SHA256SUMS` vs `sha256sum paper/main.pdf`:** matched exactly
  (`8e4cc9ef14176d2d7b1d208a39c69588c4b14441aba9483b1ca9d2576309f979`).
- **Build:** `cd paper && latexmk -pdf -interaction=nonstopmode main.tex` compiled cleanly (only
  benign `Underfull \hbox`/`\vbox` badness-10000 warnings in an 8pt table, no errors) and produced
  **30 pages**, matching the tracked PDF's page count. The freshly built PDF's byte-for-byte hash
  differs from the tracked one (pdflatex embeds a build timestamp/ID even under identical source),
  which is expected non-determinism, not a content mismatch — page count and rendered content were
  confirmed identical. `latexmk -c` was run afterward, and the tracked `paper/main.pdf` was
  restored via `git checkout -- paper/main.pdf` and re-hashed to confirm it matches
  `SHA256SUMS` exactly (no residual modification from this review). `git status --short` after
  restore shows **no tracked build artefacts** (`.aux`/`.log`/`.fls`/`.fdb_latexmk` were all
  correctly untracked/cleaned).
- **FINDING (cosmetic, not a blocker) — one tracked, empty, `\input`-ed section file.**
  `paper/sections/discussion_4_2_supplement.tex` is 0 bytes and is `\input`-ed at
  `paper/main.tex:145`. It renders nothing and breaks nothing, but it is a dead file in a public
  repo — worth either deleting the file and its `\input` line, or documenting why it is a
  deliberately reserved placeholder, before this becomes confusing cruft in a later version.

## 5. License

`LICENSE` (CC BY 4.0) applies repository-wide with no per-directory carve-out, and
`paper/README.md` states "Licence: CC BY 4.0, as the repository" — consistent, and the paper is
covered. `CITATION.cff`'s `preferred-citation` still points only at the conference abstract (not
`paper/main.pdf`), and its top-level `abstract:` field describes only the abstract-plus-evidence-
ledger record, with no mention that a full paper now also exists in this repository. This is not a
license conflict, but the human owner may want to add a `paper/main.pdf`-referencing note or a
second citation entry so a citation-management tool surfaces the full paper as well as the
abstract — reported only, not a must-fix, per the assignment's dimension 5 instruction.

## 6. Bibliography

**Fully consistent.** A full cross-reference of every `\cite{...}` key in `paper/main.tex` and
`paper/sections/*.tex` against every `\bibitem{...}` in `paper/sections/refs_all.tex` found exactly
242 cite keys and 242 bibitems, with **zero** cited-but-undefined and **zero**
defined-but-never-cited entries.

Ten PMIDs were selected and checked against PubMed's `esummary` API (author/year/title/journal),
one call per 0.4 s:

| PMID | `\bibitem` claims | PubMed confirms |
|---|---|---|
| 26293351 | Rudow DL, 2015, *J Clin Psychol Med Settings* | Match |
| 26289454 | Couture-Carron A, 2017, *J Interpers Violence* | Match |
| 18408170 | Thananowan N, 2008, *Violence Against Women* | Match |
| 26442989 | Thongpriwan V, 2015, *Asian J Psychiatry* | Match |
| 26362841 | Tarzia L, 2016, *Women's Health Issues* | Match |
| 19487706 | Ahmad F, 2009, *Ann Intern Med* | Match |
| 26892333 | Miller E, 2016, *Contraception* | Match |
| 26645540 | Evans M, 2016, *Violence and Victims* | Match |
| 21287968 | Welland C, 2010, *Violence and Victims* | Match |
| 27639927 | McCauley HL, 2017, *Contraception* | Match |

10/10 matched on first author, year, title, and journal. No fabricated or misattributed citation
found in this sample.

## 7. Other observations (would embarrass the author before this audience)

- The paper is unusually disciplined about hedging: every simulation number is prefixed "in the
  simulation, under its assumptions"; every proposed extension (Layer 0, Layer 2, the no-stake
  assessor) is labelled "(a proposed extension)" at first mention; the Appendix D claim–evidence
  ledger pre-declares forbidden wording in its own right-hand column. This is a genuinely strong
  claim-ceiling design, and the two findings above (§1 internal paths, §2 Fawcett contradiction)
  are the kind of small residue that discipline usually still leaves behind — worth fixing, not
  worth alarm.
- No participant data, no case notes, no re-identifiable client detail was found anywhere in the
  paper, consistent with AGENTS.md §3.
- The Declarations block (conflict of interest, funding, ethics, AI-use, author contributions,
  disclaimer) is complete and appropriately conservative; the AI-use disclosure
  (`paper/main.tex:190`) is honest ("AI tools assisted drafting and editing; the author verified
  all content and is accountable for it") and does not overclaim AI's role.

---

## Resolution

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | `audit/purpose-review.md` and `audit/v0.4-editlist.md` (private-only paths) named in the public PDF's version-history table (`paper/main.tex:286-287`) | Medium | **Open — must-fix before merge** |
| 2 | Real named private individual ("[a named private individual]") acknowledged by full name with no consent trail on record (`paper/main.tex:192`) | Medium | **Open — must-fix before merge (confirm consent, or remove/anonymise)** |
| 3 | `appendix_extended_evidence.tex:16` incorrectly states Fawcett et al. (2010) is "not cited," contradicting its own citation in `discussion_novelty.tex` | Low | **Open — must-fix before merge (one-sentence correction)** |
| 4 | `CITATION.cff` does not mention the full paper | Note only | Not a blocker; human owner's discretion |
| 5 | `paper/sections/discussion_4_2_supplement.tex` is a tracked, empty, `\input`-ed file | Cosmetic | Not a blocker; recommend cleanup in next revision |

## Verdict: **REVISE-THEN-MERGE**

The paper's citation accuracy (10/10 PubMed spot-check), bibliography integrity (242/242
cite↔bibitem match), claim-ceiling discipline, title/affiliation/WHO-edition consistency, license
coverage, and build reproducibility (30 pages, hash-pinned) are all sound. Three concrete,
low-effort must-fix items stand between this branch and merge under AGENTS.md §1: (1) strip the two
private-only file paths from the public version-history table, (2) confirm (or remove) the named
personal acknowledgement, and (3) correct the Fawcett citation-scope contradiction. None of these
requires re-writing any evidence claim or re-running the citation check; all three are text edits.
Once resolved (or explicitly accepted by the human owner per §1), this is ready to merge.

The human owner (the corresponding author) remains the only approver for anything that leaves this
repository, per AGENTS.md §1.
