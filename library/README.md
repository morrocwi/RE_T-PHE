# Evidence library — index

> Built by `tools/build_library.py` from `library/data/`. Every entry was produced by a literature-search
> pass over PubMed (NCBI E-utilities) or supplied as an external reading list, and then re-fetched and
> checked by an independent verifier. Entries marked **FIX** carry the verifier's correction verbatim;
> entries the verifier could not confirm are listed under *Not admitted*. This is a targeted, verified
> reading library, **not a systematic review**: no protocol registration, no duplicate screening, no
> risk-of-bias assessment. Scope rule: PubMed-indexed literature and global guidance (WHO, USPSTF, NICE,
> Cochrane, MRC). Sources outside that scope appear only as *context* and carry no evidential weight.

| # | Category | Admitted entries | File |
|---|---|---|---|
| 01 | Burden of intimate-partner violence and primary-prevention frameworks | 20 | [01-burden-of-intimate-partner-violence-and-primary-prevention-frameworks.md](01-burden-of-intimate-partner-violence-and-primary-prevention-frameworks.md) |
| 02 | Premarital and relationship education: measured outcomes | 20 | [02-premarital-and-relationship-education-measured-outcomes.md](02-premarital-and-relationship-education-measured-outcomes.md) |
| 03 | Screening, first-line response and referral | 21 | [03-screening-first-line-response-and-referral.md](03-screening-first-line-response-and-referral.md) |
| 04 | Couple-based work and coercive control | 20 | [04-couple-based-work-and-coercive-control.md](04-couple-based-work-and-coercive-control.md) |
| 05 | Decision autonomy, reproductive coercion and measurement instruments | 18 | [05-decision-autonomy-reproductive-coercion-and-measurement-instruments.md](05-decision-autonomy-reproductive-coercion-and-measurement-instruments.md) |
| 06 | Muslim populations, Thailand and Southeast Asia | 23 | [06-muslim-populations-thailand-and-southeast-asia.md](06-muslim-populations-thailand-and-southeast-asia.md) |
| 07 | Multicultural clinical safety and language access | 19 | [07-multicultural-clinical-safety-and-language-access.md](07-multicultural-clinical-safety-and-language-access.md) |
| 08 | Preconception medicine, premarital screening and adjacent guidance | 17 | [08-preconception-medicine-premarital-screening-and-adjacent-guidance.md](08-preconception-medicine-premarital-screening-and-adjacent-guidance.md) |
| 09 | Global guidance, frameworks and methods | 29 | [09-global-guidance-frameworks-and-methods.md](09-global-guidance-frameworks-and-methods.md) |
| 10 | Thailand and the southern border provinces | 12 | [10-thailand-and-the-southern-border-provinces.md](10-thailand-and-the-southern-border-provinces.md) |

Unique PubMed records admitted across categories: **171**.

## How an entry gets in

1. A search pass records the PMID, reads the abstract, and writes the finding and a relevance annotation.
2. An independent verifier re-fetches every PMID and checks title, year, numbers and whether the annotation overstates the abstract.
3. KEEP and FIX entries are published; FIX entries show the correction; DROP entries are listed as not admitted.
4. The raw search and verification files are kept in `library/data/` so any entry can be audited.

## Reading rule

Nothing in this library is evidence that T-PHE is effective. Entries position the proposal; the abstract remains the claim ceiling.

## Machine-readable

- `library.json` — every admitted entry in one schema, plus context sources and not-admitted identifiers.
- `kg/graph.json` — knowledge graph: nodes (records, categories, propositions P1–P7, safeguards, outcome domains) and edges (in_category; supports / complicates / contradicts / relates_to a proposition; informs a safeguard; measures_or_discusses an outcome domain).
- `kg/overview.md` — Mermaid overview of category → proposition edges.
