# Independent adversarial appraisal — WHO RESPECT citation update to 2nd edition, 2025 (C-02, D-011)

**Reviewer:** independent adversarial reviewer (AI, role only), not the drafting session.
**Scope:** branch `docs/respect-2025`, commit `a73dacf` at HEAD, diffed against `main`. One row
changed in `CLAIMS.md` (C-02), one line appended to `logbook.jsonl` (D-011).
**Date:** 2026-09-03.
**Method:** full read of the diff; live re-fetch of the WHO publication page for ISBN
9789240117020; direct read (via saved PDF, page-by-page) of the 2019 first edition source document
(WHO/RHR/18.19) to compare its stated seven strategies against the 2025 edition's; JSON validation
and append-only check of `logbook.jsonl`; grep-based privacy/leak sweep of the diff; cross-check
against `abstract/ABSTRACT.md`.

---

## 1. Does the WHO RESPECT second edition (2025), ISBN 9789240117020, exist, and are its seven
strategies the same as the 2019 first edition?

**Verified — exists, and the seven strategies are identical in wording.**

- `https://www.who.int/publications/i/item/9789240117020` was fetched live. It shows: title
  "RESPECT women: preventing violence against women, 2nd ed."; edition 2nd; publication year 2025
  (page also cross-referenced against the WHO news item dated 19 November 2025); publisher World
  Health Organization; ISBN 978-92-4-011702-0. It lists the seven strategies as: Relationship
  skills strengthened; Empowerment of women; Services ensured; Poverty reduced; Environments made
  safe; Child and adolescent abuse prevented; Transformed attitudes, beliefs and norms.
- The 2019 first edition (WHO/RHR/18.19, © World Health Organization 2019) was obtained directly
  as a PDF (from a UN Women mirror, since the WHO/IRIS bitstream returned 403 to both `curl` and
  `WebFetch` — IRIS serves a JS front end over the same handle) and read page-by-page with the PDF
  reader, not summarized by a search engine. Its own colophon page confirms `WHO/RHR/18.19`, ©
  WHO 2019, suggested citation "RESPECT women: Preventing violence against women. Geneva: World
  Health Organization; 2019 (WHO/RHR/18.19)". Page 9 of that same PDF lists, word for word: **R**
  elationship skills strengthened, **E**mpowerment of women, **S**ervices ensured, **P**overty
  reduced, **E**nvironments made safe, **C**hild and adolescent abuse prevented, **T**ransformed
  attitudes, beliefs, and norms — each with the identical one-sentence gloss reproduced in
  `CLAIMS.md`'s parenthetical list.
- Comparing the two directly: the seven strategy names and their order are identical between the
  2019 first edition (read directly from the source PDF) and the 2025 second edition (read from
  WHO's own live publication page). **This is a first-hand comparison of the primary source text
  in both cases, not a secondary summary of either.**
- **What I could not verify:** I did not obtain and read the full text of the 2025 second edition
  PDF itself (only its WHO.int landing/metadata page, which independently lists the same seven
  strategies) — IRIS's front end blocked direct PDF retrieval for both editions, and I did not
  pursue a mirror copy of the 2025 edition the way I did for 2019. So the *metadata and
  strategy-list* match is verified against WHO's own live page; a sentence-for-sentence read of the
  2025 edition's own strategy-gloss text (to catch any wording drift beyond the seven strategy
  names themselves) was not performed. This is a minor residual gap, not a basis for revise, since
  `CLAIMS.md`'s C-02 claim is only about the strategy names/count matching, which is confirmed.

**No finding.** The citation target, edition, year, ISBN, and the "seven strategies unchanged from
2019" claim in the new C-02 text are all supported by what I directly read.

## 2. Register and evidence category

`CLAIMS.md` C-02 remains in medical-science / public-health register throughout the added text
("citation target fixed by the author", "the presentation and the full paper cite the 2025
edition") — no non-medical vocabulary introduced, consistent with `AGENTS.md` §2. The evidence
category column is unchanged: **External guideline / framework**. This is the correct category for
a WHO framework document and was not altered by this diff — no finding.

## 3. Logbook line — valid JSON, correct schema, append-only

```
$ python3 -c "import json; d=json.loads(open('logbook.jsonl').readlines()[-1]); print(sorted(d.keys()))"
['alternatives', 'by', 'id', 'kind', 'ts', 'what', 'why']
```

The appended line (`D-011`) is valid JSON and carries `ts`, `kind`, `what`, `by`, `why`,
`alternatives` (plus `id`, consistent with other decision-kind rows in the file). `git diff`
confirms the change to `logbook.jsonl` is a pure append (one line added, nothing removed or
rewritten) — consistent with `AGENTS.md` §6's append-only rule. No finding.

## 4. Privacy / leak scan of the diff

```
$ git diff main..docs/respect-2025 | grep -Ei "yaoharee-lt|/home/|192\.168|session_|arayawedding@gmail|hostname"
(no output)
```
No local paths, usernames, internal IPs, session identifiers, or contact details in either changed
file. No finding.

## 5. Consistency with `abstract/ABSTRACT.md`

`ABSTRACT.md` line 20 reads: "Prevention frameworks such as WHO's RESPECT cover relationship
skills, empowerment, safe environments, and services" — it names RESPECT without citing an edition
or year at all. The new C-02 text states the citation *target* for the presentation and full paper
is the 2025 second edition, while leaving the abstract itself untouched. Since the abstract makes
no edition-specific claim, and the 2019/2025 strategy lists are identical in substance (§1 above),
there is no factual contradiction between the abstract's unedited text and C-02's new citation
target — no finding.

## 6. Documentation scope note

`CLAIMS.md`'s revised C-02 cell is now noticeably denser (original strategy-consistency caveat +
new citation-fix sentence in one cell). This is not a defect — the ledger format tolerates a
growing "what would strengthen it" column — but a future full-paper draft citing this row should
pull the final citation string verbatim rather than re-typing it, to avoid a transcription drift
between `CLAIMS.md`'s ISBN/edition text and the manuscript's reference list. **NIT**, not a
finding requiring action before merge.

---

## Findings index

| # | Severity | Location | Summary |
|---|---|---|---|
| — | — | — | No MUST-FIX or SHOULD-FIX findings. |

**NIT:** future full-paper drafts should copy the C-02 citation string verbatim rather than
re-typing it, to avoid drift between `CLAIMS.md` and the manuscript reference list.

## REFUTED candidates (checked and not upheld)

- "The 2025 second edition does not exist / ISBN is fabricated" — REFUTED; confirmed live on
  `who.int` with matching title, edition, year, publisher and ISBN.
- "The seven strategies changed between 2019 and 2025" — REFUTED; both primary sources (2019 PDF
  read directly, 2025 landing page read directly) list the identical seven strategy names in the
  identical order.
- "The citation update pulls the abstract or C-02 out of medical-science register" — REFUTED; all
  added text uses public-health/guideline vocabulary consistent with `AGENTS.md` §2.
- "The change contradicts `ABSTRACT.md`" — REFUTED; the abstract names RESPECT without an edition,
  so there is nothing for the new citation target to contradict.

## Verdict: **APPROVE**

No blocker was found. The WHO RESPECT second edition (2025, ISBN 9789240117020) is real and
independently confirmed; its seven strategies are identical to the 2019 first edition's, confirmed
by a first-hand read of both primary sources rather than a secondary summary of either; the row
stays in medical-science register and its evidence category is unchanged; the logbook append is
valid JSON with the required fields and is a pure append; no privacy or leak exposure was found in
the diff; and the change is consistent with the unedited abstract text. This branch is ready to
merge under §1 without further revision, pending the human owner's sign-off per §1.

## Resolution
No must-fix items were raised; none require resolution. The human owner (corresponding author) may
merge under §1 on the strength of this appraisal.
