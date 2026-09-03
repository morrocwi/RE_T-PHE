# Independent adversarial appraisal — "countries of origin" figure added to ABOUT_ARAYA_NIKAH.md

**Reviewer:** independent adversarial reviewer (AI, role only), not the drafting session.
**Scope:** branch `docs/about-countries` diffed against `main`: `ABOUT_ARAYA_NIKAH.md` (one row
added to the §9 operational-figures table) and `logbook.jsonl` (one appended line). 2 files
changed, 2 insertions, 0 deletions — confirmed by `git diff --stat main..docs/about-countries`.
**Frame:** a stranger — a TIMA/FIMA judge, a journal editor, a Thai clinician, a reader of the
public GitHub repository — can now see this.
**Date:** 2026-09-04.
**Method:** full read of the diff; read of §9 in full context (table header, footer note, and
surrounding §8/§10 text) to check internal consistency; grep of `CLAIMS.md` C-06 to compare
treatment of the analogous author-reported "more than 600" figure; repository-wide grep for
"countries" to confirm the new figure is not cited or relied on anywhere else; `python3 -m json`
line-by-line validation of `logbook.jsonl`; a privacy/leak read of the new logbook line and table
row (names, paths, phone numbers, session identifiers); confirmation that no other tracked file
changed.

## 1. Labelling consistency

The new row reads: "Countries of origin represented among international couples | more than 30
(reported directly by the author, 2026-09-04; not in the governance records listed under Sources;
organisation-reported reach, not an outcome)."

This sits inside §9's existing header, "*Not independently assured.* Figures reported by the
organisation in its own records", so the row inherits that qualifier and does not need to restate
it — consistent with the table's other rows, none of which repeat the header's caveat. The row
additionally carries its own three-part hedge (source attribution, absence from the governance
records under §"Sources", and an explicit "reach, not an outcome" label), which is the same
pattern already used for the adjacent "Premarital-programme participants since 2024" row citing
`CLAIMS.md` C-06. `CLAIMS.md` C-06 treats the analogous "more than 600" figure identically:
"Figure supplied by the organisation. **Not independently verified in this repository; no
participant-level data are held here.** Cite as 'organisation-reported.'" The new row's language
("reported directly by the author"; "organisation-reported reach, not an outcome") is register- and
substance-consistent with that precedent. No claim of independent verification, no upgrade to a
finding, and no outcome framing is present.

One asymmetry noted, not a blocker: the "600 participants" row cross-references `CLAIMS.md` C-06
by name; the new "30 countries" row does not point to a CLAIMS.md entry because none exists for it
— correctly, since this figure is not used in the abstract or anywhere in the claims table (see
§2 below), so it needs no claims-ledger entry under the repository's existing convention (only
abstract-cited figures are ledgered in `CLAIMS.md`).

## 2. Not used as evidence

A repository-wide grep for "countries" across all tracked `.md` files found only: (a) unrelated
hits in `library/` PubMed-source summaries (multi-country study characteristics of cited papers,
e.g. "59 studies, 22 countries"), (b) unrelated hits in `paper/evidence-map/prisma_counts.md`
mirroring the same library entries, and (c) the new row itself. No file cites "more than 30" or
references the new row as support for any claim, mechanism, or outcome. It does not appear in
`CLAIMS.md`, `abstract/ABSTRACT.md`, or anywhere in `paper/`. The finding is confirmed: the figure
is added once, to the operational-figures table, and used nowhere as evidence.

## 3. Register

The row uses plain organisational/administrative language ("countries of origin represented among
international couples," "reported directly by the author," "governance records," "organisation-
reported reach, not an outcome"). No marketing tone, no superlative beyond the organisation's own
"more than 30" figure (which is itself hedged, matching the pattern of every other row in the same
table). No imported non-medical vocabulary. Consistent with AGENTS.md §2.

## 4. Logbook

The appended line is valid JSON (confirmed by parsing every line in `logbook.jsonl`), append-only
(prior lines unchanged), and carries `ts`, `kind`, `by`, `what`, `source` fields consistent with
the file's existing schema. Content: records what was added and why, in the same descriptive style
as prior entries. No personal names, local paths, usernames, hostnames, or phone numbers present.
Author identification is by role ("by":"ai") only, consistent with AGENTS.md §1 and §3.

## 5. File scope

`git diff --name-only main..docs/about-countries` returns exactly `ABOUT_ARAYA_NIKAH.md` and
`logbook.jsonl`. No other file is touched.

## Verdict: **APPROVE**

The single added row is correctly and consistently labelled as organisation-reported, not
independently assured, and explicitly framed as reach rather than outcome — matching the table's
own header and the precedent set by `CLAIMS.md` C-06 for the structurally identical "600
participants" figure. It is not cited or relied on as evidence anywhere in the repository. The
register is medical-science/organisational throughout, with no marketing language. The logbook
line is valid, append-only, and free of personal names, paths, or phone numbers. No file outside
the declared scope changed. No must-fix items.

The human owner (the corresponding author) remains the only approver for anything that leaves this
repository, per AGENTS.md §1.
