# Independent adversarial appraisal — Islamic medical ethics (AGENTS.md §2 amendment + category 18)

**Reviewer:** independent adversarial reviewer (AI, role only), not the drafting session.
**Scope:** branch `docs/islamic-medical-ethics`, commits `2088472` (AGENTS.md §2) and `e96e9d6`
(library category 18, 20 records) at HEAD.
**Date:** 2026-09-02.
**Method:** build reproduction; full read of `AGENTS.md` §2 and `library/17-*.md` scope line; full
read of all 20 rows of `library/18-*.md` and the underlying `library/data/search-islamic-medical-ethics.json`;
live re-fetch of 8 of the 20 PMIDs directly from NCBI E-utilities (`efetch`/pubtype XML) as an
independent check against the file's own claims; grep-based privacy/path sweep; README/llms.txt
consistency check.

---

## 1. Build reproducibility — PASS

```
$ python3 tools/build_library.py
categories: 18 unique PMIDs: 313 {...'18': 20}
$ git status --porcelain
(empty)
```
Clean rebuild, no diff. No finding.

---

## 2. AGENTS.md §2 internal consistency — MUST-FIX

`AGENTS.md:24-25` (pre-existing, unmodified by this change):

> Do **not** import working vocabulary from other projects or philosophies into this repository.
> A reader from a medical faculty must be able to read every file without a glossary.

`AGENTS.md:26-31` (new, this branch):

> **Islamic ethical terms are part of this work's declared framework** … They may be used, always
> with a plain-language gloss, as the named ethical frame — never as evidence. … Islamic
> medical-ethics literature may be cited only when it is PubMed-indexed and of high quality
> (systematic review, guideline, or leading journal).

**Finding 2a (MUST-FIX).** The new bullet is a direct, unflagged exception to the bullet immediately
above it — it imports named theological vocabulary (`faqr`, `taqwa`, `amanah`, `ʿadl`) from a
philosophy external to public-health/medical-science register, which is exactly what line 24-25
forbids. Nothing in line 24-25 says "except as provided below," and nothing in the new bullet says
"as an exception to the rule above." A reader auditing §2 top-to-bottom hits a flat contradiction,
not a scoped carve-out. This is exactly the kind of self-contradicting policy language the
project's own README review process (item 6 below) exists to catch.
**Minimal fix:** amend line 24 to read *"Do not import working vocabulary from other projects or
philosophies into this repository, except the Islamic ethical frame named and bounded below."* — one
clause, cross-referencing forward — or merge the two bullets into one so the exception is visible at
the point the general rule is stated.

**Finding 2b (MUST-FIX — auditability).** The rule text names three admission tiers: "systematic
review, guideline, or leading journal." The actual admission logic used to build category 18 (per
`library/data/search-islamic-medical-ethics.json` and the row-level "Tier one …" language in
`library/18-*.md`) additionally and materially relies on:
- **RCT design** as an independent admission tier (rows for PMID 39186273, 41114978) — not named in
  §2's three tiers (arguably subsumable under "leading journal" since both are in *JAMA Network
  Open*, but the rule text doesn't say so).
- **A named two-record carve-out for *The Journal of IMA*** (PMID 23864762, 23610513), explicitly
  because it is IMANA's official journal — a fourth, unnamed tier not present in §2 at all.
- **"Leading journal" resolved by an unpublished, self-authored "search brief"** that pre-names
  which journals count (the row text repeatedly cites "flagship specialty journal named in the
  search brief" for *Bioethics* and *Journal of Medical Ethics*, and queries Q13-Q15 in
  `library/18-*.md:23-25` search by `[Journal]` field directly against a pre-chosen list). That
  brief is not itself a tracked, public file in this repository — it exists only as the search
  agent's working assumption, reconstructed after the fact in the row commentary. §2 gives a reader
  no way to know, ahead of any given citation, which journals will count as "leading" — the
  criterion is applied, not stated.
**Minimal fix:** either (a) name the four actual tiers in §2 verbatim — SR/MA, guideline, RCT in a
named high-tier journal, and the Journal-of-IMA carve-out by name and count — or (b) commit the
"search brief" journal list as a tracked file (e.g. `library/TIER_ONE_JOURNALS.md`) that §2
references, so "leading journal" is an auditable, pre-committed list rather than a judgment made
and justified after the fact by the same party doing the searching.

---

## 3. Category 18 tier claims — mostly sound, one real overclaim already self-caught, one structural gap

**Live verification (8/20 rows re-fetched from NCBI E-utilities directly, independent of the
file's own text):** PMID 39186273 (Zoellner RCT, JAMA Netw Open), 41114978 (Bhowmik RCT, JAMA Netw
Open), 38600776 (Gendler quasi-experimental, Med Decis Making), 41458120 (Mittal, Front Neurol),
17845488 (Padela primer, Bioethics), 23975951 (Mustafa, J Med Ethics), 41139992 (Mohamed Mahdi SR,
Trauma Violence Abuse), 41651650 (Doedes qualitative, J Med Ethics). All eight matched the file's
journal, year, design and (where numeric) effect-size claims **exactly**, including:
- PMID 41458120: PubMed's own `<PublicationType>` tag is confirmed `Review` (not `Practice
  Guideline`) — the row's own downgrade-correction (line 50, "TIER OVERCLAIM … PubMed's own
  PublicationType tag is 'Review', not 'Practice Guideline'") is independently verified accurate.
- PMID 38600776: abstract confirms OR=0.23/0.43 are **not** stated as adjusted and the design is
  quasi-experimental (pre/post, no randomization) — the row's FIX correction (dropping "adjusted",
  adding the Muslim-Arab OR=3.12 subgroup) is independently verified accurate.
- PMID 39186273 / 41114978: Cohen's-d and hazard-ratio/ARR/RRR/NNT figures quoted in the library
  row match the live PubMed abstract verbatim.

This is genuine evidence the verifier pass did real, careful re-fetch work, not a rubber stamp —
noted as a positive, not merely absence-of-finding.

**Finding 3a (MUST-FIX).** PMID 39186273 (Zoellner, *JAMA Netw Open* 2024) carries **two published
errata** (2024 Sep 3 and 2024 Oct 1, per the live PubMed record's `<CommentsCorrectionsList>` /
header) that are not mentioned anywhere in `library/18-*.md:47` or the underlying JSON record. The
cited d-values (PTSD d=-0.67, depression d=-0.66, well-being d=0.71) were not checked against the
erratum text by this reviewer either (out of scope for a text-only E-utilities fetch), so this is
flagged, not resolved either way. **Minimal fix:** before this record is cited in the manuscript,
pull the erratum text and confirm whether it touches the cited effect sizes; add one line to the
row noting the erratum exists and was checked.

**Finding 3b (SHOULD-FIX — tier basis, not fabrication).** For rows admitted purely on "leading
journal" standing with no SR/MA/RCT/guideline design underneath — PMID 17845488 (narrative primer),
23975951 (conceptual analysis), 21041237 (bioethical analysis), 22845721 (ethico-legal analysis),
41651650 (qualitative interview study), and the two Journal-of-IMA carve-outs — the "leading
journal" designation is asserted, not evidenced: no impact-factor, JCR-quartile, Scopus-CiteScore
or comparable external metric is cited anywhere in the row, the JSON record, or `AGENTS.md`. *Bioethics*
and *Journal of Medical Ethics* are genuinely well-regarded specialty bioethics journals by
reputation, so this reviewer is not disputing the underlying judgment — but "tier one" is a claim
about evidentiary standing, and right now that claim rests entirely on the same party's own say-so,
which is precisely the "no independent check" pattern the repository's own §1 maker-checker rule
(`AGENTS.md:9`, "An AI that drafted a change does not review that change") exists to prevent for
public-facing text. **Minimal fix:** cite one external, checkable proxy per journal (e.g. Scopus
CiteScore/quartile, or "official journal of [named society]" where verifiably true) in the row or in
a single shared footnote, rather than leaving "leading journal" as an unsourced adjective.

**No fabricated PMIDs, no invented effect sizes, no misattributed years/journals found in the eight
verified rows or in a skim of the remaining twelve.** REFUTED as a class: "records are not really
tier one" — not supported; the tier-one claim is *thin on external sourcing* (3b) but not false for
the sampled rows, and the file's own self-corrections (rows 46, 48, 50) show the verifier pass
already caught and fixed three real overclaims before this appraisal — worth crediting.

---

## 4. Ethics-paper-as-outcome-evidence / term-to-finding mapping — one real finding

Sampled the same 8 rows plus a full read of all 20 for this check specifically.

**Finding 4a (MUST-FIX — selective reporting).** PMID 41139992 (Mohamed Mahdi, *Trauma Violence
Abuse* 2025, PRISMA systematic review). Live abstract, ecological-level risk/protective factors:

> At the individual level … spirituality and knowledge of rights were protective. … At the
> exosystem level, **the negative role of religious leaders was a risk factor** … At the macrosystem
> level, **cultural and religious norms that legitimize violence** … were risk factors.

`library/18-*.md:42`'s Finding column reports only the individual-level "spirituality … protective"
and microsystem-level "husband's control … risk" results, and the Relevance column uses this to
argue the record "supports T-PHE's premise that faith-grounded education (taqwa, 'adl/justice
safeguards) can be protective." **It omits the same abstract's exosystem/macrosystem findings that
religious leaders and religious/cultural norms are themselves documented risk factors for the same
outcome (gender-based violence) in the same review** — the more directly complicating result for a
programme that names Islamic religious concepts (taqwa, 'adl) as its own protective safeguard. This
is not a fabrication (nothing stated is false), but it is a one-sided extraction from a
multi-level finding that, read in full, cuts both toward and against the "faith framing is
protective" reading the relevance annotation draws. Every other complicating record in category 18
(rows 40, 41, 44, 48) is handled with the honest hedging the repository's own reading rule requires;
this row is the exception.
**Minimal fix:** add the exosystem/macrosystem risk-factor findings ("negative role of religious
leaders," "cultural and religious norms that legitimize violence") to the Finding column, and revise
the Relevance annotation to note the record cuts both ways — spirituality protective at the
individual level, religious-leader/norm risk at higher ecological levels — consistent with how row
40 (self-immolation) and row 44 (moral distress) are already framed.

**No other case found (7 sampled + skim of remaining 12) of an ethics/normative paper being cited
as if it were outcome evidence.** Conceptual/normative essays (rows 31, 32, 33, 34, 35, 43) are
consistently framed as positioning or grounding the vocabulary, with explicit language such as
"without itself validating T-PHE's programme," "a narrative argument, not empirical evidence of
outcomes," "a structural analogy" — this discipline is real and holds up under sampling.

---

## 5. Claim ceiling and privacy sweep — PASS

- File-level reading rule present and correctly worded: `library/18-*.md:27` — "does not, and must
  not be read to, establish that T-PHE itself is effective, validated, or endorsed by any of the
  cited sources." Matches the library-wide rule at `library/README.md:45`.
- `grep` sweep of `library/18-*.md`, `AGENTS.md`, `README.md`, `llms.txt`,
  `library/data/search-islamic-medical-ethics.json` for local usernames, `[repo]` paths, internal
  hostnames/IPs, session identifiers, and the maintainer's email: **no hits**.
- `private/*` is git-ignored (`.gitignore:2-3`, `!private/README.md` carve-out only); the
  `private/paper/litreview/search-islamic-medical-ethics.json` mirror is byte-identical to the
  tracked `library/data/` copy — a working-copy duplicate, not a leak, and not committed as a new
  exposure by this change (git-ignored, confirmed via `git check-ignore -v`).
- No participant-level or re-identifiable content in any of the 20 new rows — all are third-party
  published literature.

No findings.

---

## 6. Category 17 scope line — honest; category 18 lacks the equivalent framing — SHOULD-FIX

`library/17-*.md:1` already carries the exact honesty discipline the task asked to check for:

> These constructs are the medical-science counterparts of the abstract's ethic … — **the ethic
> names the duty; the evidence here says what is known about the construct.**

This line is doing real work: it pre-empts exactly the failure mode checked in §4 above (treating a
construct-level finding as if it were direct evidence for the named ethical term). **Category 18's
own scope line (`library/18-*.md:3`) does not carry an equivalent sentence** — it states admission
criteria (PubMed-indexed, SR/guideline/leading-journal) but not the same "term names the duty, the
literature says what is known about the construct/practice" caveat, even though most of category
18's rows individually reconstruct this caveat inline (e.g. row 37: "an 'adl/justice-of-the-marital-
contract *framing*"; row 40: "starkly complicates any romanticized framing"). Finding 4a above is
exactly the kind of row that a category-level version of this sentence would have caught before
publication.
**Minimal fix:** append one sentence to `library/18-*.md:3`, e.g. *"The named ethical terms
(faqr/taqwa/amanah/'adl/shura) are T-PHE's own framing; the cited literature is evidence about the
underlying bioethical, clinical or population construct, not a test of the Islamic term itself."*

---

## 7. README / llms.txt consistency — PASS

`README.md:21` and `llms.txt:16` both point to `library/README.md` and describe it as "by category
(see the index for the current count)" — neither file hardcodes a stale category count or record
total, so the addition of category 18 (18 categories, 313 unique PMIDs per the rebuilt
`library/README.md:32`) required no edit to either file and introduces no drift. No finding.

---

## Findings index

| # | Severity | Location | Summary |
|---|---|---|---|
| 2a | MUST-FIX | `AGENTS.md:24-31` | New Islamic-terms bullet directly contradicts the unamended "no imported vocabulary" bullet immediately above it; no cross-reference. |
| 2b | MUST-FIX | `AGENTS.md:26-31` | §2's rule text names 3 tiers; actual admission logic used in category 18 uses 4+ (RCT, named Journal-of-IMA carve-out, self-authored unpublished "search brief" journal list) not disclosed in the rule. |
| 3a | MUST-FIX | `library/18-*.md:47` | PMID 39186273 has two live PubMed errata, undisclosed in the row; not checked against the cited effect sizes. |
| 3b | SHOULD-FIX | `library/18-*.md` rows 31,33,35,36,44 + JSON | "Leading journal" tier basis is asserted, not evidenced by any external, checkable metric. |
| 4a | MUST-FIX | `library/18-*.md:42` (PMID 41139992) | Selective extraction: omits the same abstract's exosystem/macrosystem findings that religious leaders/norms are risk factors, producing a one-sided "religion protective" reading. |
| 6 | SHOULD-FIX | `library/18-*.md:3` | Category 18's scope line lacks category 17's "ethic names the duty; evidence says what is known about the construct" honesty sentence. |

**NIT:** none rising to the level of a separate line item; the FIX-row internal table layout (the
"Design / evidence level" and "Finding" columns visually swap roles for FIX rows, since the
correction narrative is written into the Finding cell rather than the Design cell) is mildly
confusing to a first-time reader but does not misstate anything — cosmetic only.

## REFUTED candidates (checked and not upheld)

- "Records in category 18 are not genuinely PubMed-indexed / fabricated" — REFUTED; all 8 sampled
  PMIDs independently re-fetched and match on journal, year, design, and numeric claims.
- "The two Journal of IMA entries are an unlabelled carve-out" — REFUTED; both rows (32, 34)
  explicitly and correctly label themselves as the search brief's carve-out, and exactly two such
  records exist in the file, matching the JSON's own `gaps_noted` description.
- "Category 17's scope sentence dishonestly collapses ethic into evidence" — REFUTED; the sentence
  reviewed is the correct, careful formulation and should be the template category 18 is missing.
- "README/llms.txt are stale relative to category 18" — REFUTED; no hardcoded counts to go stale.

## Verdict: **REVISE-THEN-MERGE**

No blocker was found — nothing here is a fabricated citation, a privacy leak, or a claim that T-PHE
itself is validated. But three MUST-FIX items (2a, 2b, 4a) are real, evidenced, and each is a small,
mechanical edit (one clause in AGENTS.md, one erratum check, one row correction) — this should not
merge as-is, but does not need a rework, only these fixes plus the two SHOULD-FIX items before the
independent human owner signs off per §1.

## Resolution (maker, 2026-09-03)
- AGENTS.md §2 rewritten: the "no imported vocabulary" rule now states its one declared exception, and the admission tiers for category 18 are enumerated (SR/MA; guideline; RCT; leading journal with reason; labelled Journal of IMA carve-out).
- PMID 39186273: the two published errata are now noted in the record; effect sizes flagged for re-check against the corrected article before citation.
- PMID 41139992: record now reports the full risk/protective profile from the abstract, including the negative role of religious leaders and husband control as risk factors.
- Category 18 scope line carries the same honesty sentence as category 17.
- Library rebuilt; reproducible.
