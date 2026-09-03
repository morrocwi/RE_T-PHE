#!/usr/bin/env python3
"""
build_prisma.py — PRISMA-ScR flow counts and evidence-map counts for the
T-PHE systematic evidence map (scoping review), computed ONLY from the
logged JSON files under library/. No number in this script's output is
estimated or hand-typed; every figure is a direct count or sum over the
JSON structures already in the repository. If a requested count cannot be
derived from these files, the script records the string
"not derivable from the logged files" rather than guessing.

Inputs (relative to the repository root):
  library/library.json           - admitted entries, categories, context
                                    sources, not-admitted identifiers
  library/kg/graph.json          - knowledge-graph nodes + edges
                                    (records, categories, propositions
                                    P1-P7, safeguards, outcome domains)
  library/data/search-*.json     - one file per search angle: the
                                    "records" list is what that search
                                    pass identified (candidates), before
                                    verification
  library/data/verify-*.json     - one file per search angle: the
                                    "verified" list is what the
                                    independent verifier pass processed,
                                    each with a verdict
                                    (KEEP / FIX / DROP / CONTEXT-ONLY)

Outputs (written next to this script):
  prisma_counts.json             - machine-readable counts
  prisma_counts.md               - the same counts as Markdown tables,
                                    for direct inclusion in the manuscript
"""
from __future__ import annotations

import collections
import glob
import json
import os
import re
import unicodedata

NOT_DERIVABLE = "not derivable from the logged files"
YEAR_NOT_PARSED = "year not parsed"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LIBRARY_DIR = os.path.join(REPO_ROOT, "library")
DATA_DIR = os.path.join(LIBRARY_DIR, "data")
KG_PATH = os.path.join(LIBRARY_DIR, "kg", "graph.json")
LIBRARY_JSON_PATH = os.path.join(LIBRARY_DIR, "library.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def slugify(*parts):
    """Deterministic ASCII slug of the given text parts, joined with '-'.
    Used only as the fallback dedup key for admitted entries whose
    library.json 'identifier' field is blank (see dedupe_key)."""
    pieces = []
    for p in parts:
        s = str(p or "").strip().lower()
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        if s:
            pieces.append(s)
    return "-".join(pieces)


def dedupe_key(entry):
    """Dedup key for an admitted library entry.

    Priority (per the adversarial appraisal, Finding 2 -- library.json is
    NOT edited; the fix lives entirely here):
      1. PMID, when present.
      2. The entry's own non-blank 'identifier' field (e.g. a WHO ISBN,
         DOI, Cochrane ID, PMC id -- a real, document-specific string).
      3. A deterministic fallback slug of first_author+year+title, used
         ONLY when 'identifier' is blank/absent. Two library.json entries
         that are genuinely different documents but both carry a blank
         identifier (and would otherwise collide on the literal string
         "REF:") get distinct fallback keys here, one per document, so
         neither is silently merged into the other.
    """
    pmid = entry.get("pmid")
    if pmid:
        return ("pmid", pmid)
    ident = entry.get("identifier")
    if ident:
        return ("identifier", ident)
    slug = slugify(entry.get("first_author"), entry.get("year"), entry.get("title"))
    return ("fallback_slug", slug or entry.get("id"))


def parsed_year(entry):
    """Numeric-year parsing rule (explicit, per Finding 3): a 'year' value
    counts toward the year distribution only if it is an int, or a string
    that is exactly four digits once stripped of surrounding whitespace.
    Anything else (blank string, a range/annotated string such as
    "2021 (base report); 2023/2024 update per draft claim", etc.) is
    bucketed as YEAR_NOT_PARSED and shown as its own row -- never silently
    folded into any single numeric year."""
    y = entry.get("year")
    if isinstance(y, bool):
        return None
    if isinstance(y, int):
        return y
    if isinstance(y, str) and re.fullmatch(r"\d{4}", y.strip()):
        return int(y.strip())
    return None


def main():
    library = load_json(LIBRARY_JSON_PATH)
    kg = load_json(KG_PATH)

    search_files = sorted(glob.glob(os.path.join(DATA_DIR, "search-*.json")))
    verify_files = sorted(glob.glob(os.path.join(DATA_DIR, "verify-*.json")))
    n_angle_files = len(search_files)

    # ---------------------------------------------------------------
    # 1. Records identified per search file (search pass candidates)
    # ---------------------------------------------------------------
    identified_by_file = {}
    identified_pmids_by_file = {}
    all_identified_pmids = []
    total_queries_run = 0
    for f in search_files:
        d = load_json(f)
        name = os.path.basename(f)
        records = d.get("records", [])
        identified_by_file[name] = len(records)
        pmids = [r.get("pmid") for r in records if r.get("pmid")]
        identified_pmids_by_file[name] = pmids
        all_identified_pmids.extend(pmids)
        total_queries_run += len(d.get("queries_run", []))

    records_identified_total = sum(identified_by_file.values())
    unique_identified_pmids = set(all_identified_pmids)
    duplicates_removed_by_pmid = len(all_identified_pmids) - len(unique_identified_pmids)

    # ---------------------------------------------------------------
    # 2. Records verified + verdict counts (from verify-*.json)
    # ---------------------------------------------------------------
    verified_by_file = {}
    verdict_counts = collections.Counter()
    for f in verify_files:
        d = load_json(f)
        name = os.path.basename(f)
        verified = d.get("verified", [])
        verified_by_file[name] = len(verified)
        for r in verified:
            verdict_counts[r.get("verdict", "UNSPECIFIED")] += 1

    records_verified_total = sum(verified_by_file.values())

    # ---------------------------------------------------------------
    # 3. Admitted entries (library.json) — total rows and unique records
    # ---------------------------------------------------------------
    entries = library.get("entries", [])
    admitted_entries_total = len(entries)  # category-level rows; a record
    # placed in >1 category (also_in_category) counts once per category
    admitted_unique_keys = set(dedupe_key(e) for e in entries)
    admitted_unique_total = len(admitted_unique_keys)

    admitted_with_pmid = [e for e in entries if e.get("pmid")]
    admitted_unique_pmids = set(e["pmid"] for e in admitted_with_pmid)
    admitted_without_pmid = [e for e in entries if not e.get("pmid")]
    # Unique *documents* among the non-PMID rows, using dedupe_key's
    # identifier-or-fallback-slug rule (Finding 2). This correctly merges
    # the one legitimate same-document-two-categories pair that already
    # carries a real, matching, non-blank identifier (WHO RESPECT women,
    # categories 08+09) while no longer wrongly merging the two distinct
    # WHO documents (2013 guideline, 2014 handbook) that previously
    # collided only because both left 'identifier' blank.
    admitted_without_pmid_unique_keys = set(dedupe_key(e) for e in admitted_without_pmid)
    admitted_without_pmid_unique_count = len(admitted_without_pmid_unique_keys)

    library_verdict_counts = collections.Counter(
        e.get("verifier_verdict", "UNSPECIFIED") for e in entries
    )

    not_admitted = library.get("not_admitted", [])
    context_sources = library.get("context_sources", [])

    # ---------------------------------------------------------------
    # 4. Per-category counts (from library.json 'categories' + a direct
    #    recount over 'entries' as a cross-check)
    # ---------------------------------------------------------------
    categories_declared = library.get("categories", [])
    per_category_declared = {
        c["number"]: {"title": c.get("title", ""), "admitted": c.get("admitted")}
        for c in categories_declared
    }
    per_category_recount = collections.Counter(e.get("category") for e in entries)

    # ---------------------------------------------------------------
    # 5. Design / evidence-level / year distributions (admitted entries)
    # ---------------------------------------------------------------
    design_counts = collections.Counter(e.get("design", "UNSPECIFIED") for e in entries)
    evidence_level_counts = collections.Counter(
        e.get("evidence_level", "UNSPECIFIED") for e in entries
    )
    # Explicit year-bucketing rule (Finding 3): numeric year only (int, or
    # a clean 4-digit string) is bucketed under that year; every other
    # value (blank, annotated/range strings) is bucketed under
    # YEAR_NOT_PARSED and shown as its own row, never folded into a
    # numeric year.
    year_counts = collections.Counter()
    numeric_years = []
    for e in entries:
        py = parsed_year(e)
        if py is None:
            year_counts[YEAR_NOT_PARSED] += 1
        else:
            year_counts[py] += 1
            numeric_years.append(py)
    year_not_parsed_count = year_counts.get(YEAR_NOT_PARSED, 0)
    year_span = f"{min(numeric_years)}-{max(numeric_years)}" if numeric_years else NOT_DERIVABLE
    count_2024_2025 = sum(v for y, v in year_counts.items() if isinstance(y, int) and y in (2024, 2025))
    count_2026 = year_counts.get(2026, 0)

    # ---------------------------------------------------------------
    # 6. Share of systematic reviews / guidelines / RCTs
    #    (keyword match over the free-text design + evidence_level
    #    fields; conservative substring match, case-insensitive, on the
    #    two fields actually present in library.json — no field in the
    #    logged data classifies design with a closed vocabulary, so this
    #    is a keyword count over free text, stated as such)
    # ---------------------------------------------------------------
    def text_of(e):
        return " ".join(
            str(e.get(k, "")) for k in ("design", "evidence_level")
        ).lower()

    kw_groups = {
        "systematic_review_or_meta_analysis": [
            "systematic review",
            "meta-analysis",
            "meta analysis",
            "scoping review",
            "cochrane",
        ],
        # Finding 1 (MUST): the keyword group is defined by, and only by,
        # the two terms the manuscript's row label and prose promise --
        # "guideline" and "recommendation statement". The earlier version
        # of this list also matched the bare substring "guidance", an
        # undisclosed third term that swept in a trial protocol and
        # narrative reviews; it has been removed, not renamed, so the
        # table row now means exactly what its label says.
        "guideline_or_recommendation": [
            "guideline",
            "recommendation statement",
        ],
        "randomised_or_randomized_controlled_trial": [
            "randomised controlled trial",
            "randomized controlled trial",
            "rct",
            "cluster randomi",
            "randomised trial",
            "randomized trial",
        ],
    }
    keyword_share = {}
    for label, kws in kw_groups.items():
        n = sum(1 for e in entries if any(kw in text_of(e) for kw in kws))
        keyword_share[label] = {
            "n_entries": n,
            "share_of_admitted_entries": round(n / admitted_entries_total, 4)
            if admitted_entries_total
            else NOT_DERIVABLE,
        }

    # ---------------------------------------------------------------
    # 7. Per-proposition (P1-P7) record counts from kg/graph.json edges
    #
    # A kg/graph.json edge's 'source' is a library entry's raw 'id'
    # field. For every raw id except the one former blank-identifier
    # collision ("REF:"), that raw id resolves to exactly one distinct
    # document. For "REF:" it resolves to two (the 2013 WHO guideline and
    # the 2014 WHO handbook, see dedupe_key/Finding 2) -- so an edge whose
    # source is "REF:" is counted as linking 2 distinct records, matching
    # generate_tex_fragments.py's per-document fan-out in the rendered
    # proposition tables (frag_prop_P*.tex), not just 1 graph edge.
    # ---------------------------------------------------------------
    nodes = kg.get("nodes", [])
    edges = kg.get("edges", [])
    proposition_ids = [n["id"] for n in nodes if n.get("type") == "proposition"]
    proposition_labels = {n["id"]: n.get("label", "") for n in nodes if n.get("type") == "proposition"}

    entries_by_raw_id = collections.defaultdict(list)
    for e in entries:
        entries_by_raw_id[e["id"]].append(e)
    distinct_documents_per_raw_id = {
        raw_id: len(set(dedupe_key(e) for e in group))
        for raw_id, group in entries_by_raw_id.items()
    }

    def documents_for_source(raw_id):
        """Number of distinct documents an edge's source id represents
        (>1 only for the former "REF:" collision)."""
        return max(1, distinct_documents_per_raw_id.get(raw_id, 1))

    per_proposition = {}
    for pid in proposition_ids:
        rel_counts = collections.Counter()
        rel_records = collections.defaultdict(list)
        for e in edges:
            if e.get("target") == pid and e.get("relation") in (
                "supports",
                "complicates",
                "relates_to",
                "contradicts",
            ):
                source = e.get("source")
                rel_counts[e["relation"]] += documents_for_source(source)
                rel_records[e["relation"]].append(source)
        per_proposition[pid] = {
            "label": proposition_labels.get(pid, ""),
            "supports": rel_counts.get("supports", 0),
            "complicates": rel_counts.get("complicates", 0),
            "relates_to_relevant_only": rel_counts.get("relates_to", 0),
            "contradicts": rel_counts.get("contradicts", 0),
            "total_linked_records": sum(rel_counts.values()),
            "record_ids": {rel: sorted(set(v)) for rel, v in rel_records.items()},
        }

    # Unique records (documents, not raw ids) linked to >=1 of P1-P7,
    # across all propositions -- expands the "REF:" collision source id
    # into its 2 distinct documents wherever it is linked, same rule as
    # above and as generate_tex_fragments.py.
    linked_document_keys = set()
    for pid in proposition_ids:
        for e in edges:
            if e.get("target") != pid or e.get("relation") not in (
                "supports", "complicates", "relates_to", "contradicts",
            ):
                continue
            raw_id = e.get("source")
            group = entries_by_raw_id.get(raw_id, [])
            if group:
                for entry in group:
                    linked_document_keys.add(dedupe_key(entry))
            else:
                linked_document_keys.add(("raw_id", raw_id))
    records_linked_to_ge1_proposition = len(linked_document_keys)

    # ---------------------------------------------------------------
    # Assemble output
    # ---------------------------------------------------------------
    out = {
        "provenance": {
            "search_files": [os.path.basename(f) for f in search_files],
            "n_angle_files": n_angle_files,
            "verify_files": [os.path.basename(f) for f in verify_files],
            "library_json": os.path.relpath(LIBRARY_JSON_PATH, REPO_ROOT),
            "kg_graph_json": os.path.relpath(KG_PATH, REPO_ROOT),
        },
        "prisma_flow": {
            "records_identified_total_sum_of_search_hits": records_identified_total,
            "records_identified_by_search_file": identified_by_file,
            "total_pubmed_queries_logged": total_queries_run,
            "duplicates_removed_by_pmid": duplicates_removed_by_pmid,
            "unique_identified_pmids": len(unique_identified_pmids),
            "records_verified_total": records_verified_total,
            "records_verified_by_file": verified_by_file,
            "verifier_verdict_counts": dict(verdict_counts),
            "admitted_entries_total_category_rows": admitted_entries_total,
            "admitted_unique_records_pmid_or_identifier": admitted_unique_total,
            "admitted_unique_pmids": len(admitted_unique_pmids),
            "admitted_entries_without_pmid_guidance_docs": len(admitted_without_pmid),
            "admitted_unique_nonpmid_documents": admitted_without_pmid_unique_count,
            "admitted_unique_records_total_recomputed": len(admitted_unique_pmids) + admitted_without_pmid_unique_count,
            "not_admitted_dropped_count": len(not_admitted),
            "context_only_source_count_not_pubmed": len(context_sources),
            "library_json_verdict_counts_admitted_only": dict(library_verdict_counts),
        },
        "per_category": {
            "declared_in_library_json": per_category_declared,
            "recount_from_entries": dict(per_category_recount),
        },
        "design_distribution": dict(design_counts),
        "evidence_level_distribution": dict(evidence_level_counts),
        "year_distribution": dict(sorted(year_counts.items(), key=lambda kv: str(kv[0]))),
        "year_bucketing_rule": (
            "A 'year' value is bucketed under a numeric year only if it is an "
            "int, or a string that is exactly four digits after stripping "
            "whitespace; every other value (blank string, or an annotated/"
            "range string such as '2021 (base report); 2023/2024 update per "
            "draft claim') is bucketed under the row 'year not parsed' and "
            "never folded into any single numeric year."
        ),
        "year_span_numeric_only": year_span,
        "year_not_parsed_count": year_not_parsed_count,
        "count_2024_plus_2025_numeric_only": count_2024_2025,
        "count_2026_numeric_only": count_2026,
        "keyword_share_systematic_review_guideline_rct": keyword_share,
        "per_proposition_P1_P7": per_proposition,
        "records_linked_to_ge1_proposition": records_linked_to_ge1_proposition,
    }

    counts_json_path = os.path.join(HERE, "prisma_counts.json")
    with open(counts_json_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    write_markdown(out, os.path.join(HERE, "prisma_counts.md"))

    print(f"Wrote {counts_json_path}")
    print(f"Wrote {os.path.join(HERE, 'prisma_counts.md')}")
    print()
    print(json.dumps(out["prisma_flow"], indent=2))


def write_markdown(out, path):
    flow = out["prisma_flow"]
    n_angle = out["provenance"]["n_angle_files"]
    lines = []
    lines.append("# PRISMA-ScR counts — computed from library/ (not estimated)\n")

    lines.append("## Flow\n")
    lines.append("| Stage | Count |")
    lines.append("|---|---|")
    lines.append(f"| Records identified through search-*.json (sum of hits, {n_angle} angle files) | {flow['records_identified_total_sum_of_search_hits']} |")
    lines.append(f"| Total logged PubMed E-utilities queries (queries_run, search files with a search log) | {flow['total_pubmed_queries_logged']} |")
    lines.append(f"| Duplicate PMIDs removed across search files | {flow['duplicates_removed_by_pmid']} |")
    lines.append(f"| Unique PMIDs identified by search | {flow['unique_identified_pmids']} |")
    lines.append(f"| Records verified (verify-*.json, {n_angle} angle files) | {flow['records_verified_total']} |")
    for verdict in ("KEEP", "FIX", "DROP", "CONTEXT-ONLY"):
        lines.append(f"| Verifier verdict: {verdict} | {flow['verifier_verdict_counts'].get(verdict, 0)} |")
    lines.append(f"| Admitted entries (category-level rows; a record placed in >1 category counts once per category) | {flow['admitted_entries_total_category_rows']} |")
    lines.append(f"| Admitted unique records (PMID or, for non-PMID guidance documents, identifier) | {flow['admitted_unique_records_pmid_or_identifier']} |")
    lines.append(f"| Admitted unique PMIDs | {flow['admitted_unique_pmids']} |")
    lines.append(f"| Admitted entries without a PMID (guidance documents: WHO/NICE/Cochrane/JAKIM/Malaysia-government etc.) | {flow['admitted_entries_without_pmid_guidance_docs']} |")
    lines.append(f"| Admitted unique non-PMID documents (identifier-or-fallback-slug dedup; see Finding 2) | {flow['admitted_unique_nonpmid_documents']} |")
    lines.append(f"| Admitted unique records, recomputed total (unique PMIDs + unique non-PMID documents) | {flow['admitted_unique_records_total_recomputed']} |")
    lines.append(f"| Not admitted (DROP, logged in library.json not_admitted) | {flow['not_admitted_dropped_count']} |")
    lines.append(f"| Context-only sources (not PubMed-indexed, no evidential weight) | {flow['context_only_source_count_not_pubmed']} |")
    lines.append("")

    lines.append("## Per category (as declared in library.json)\n")
    lines.append("| Category | Title | Admitted (declared) | Admitted (recount from entries) |")
    lines.append("|---|---|---|---|")
    decl = out["per_category"]["declared_in_library_json"]
    recount = out["per_category"]["recount_from_entries"]
    for num in sorted(decl.keys()):
        d = decl[num]
        lines.append(f"| {num} | {d['title']} | {d['admitted']} | {recount.get(num, 0)} |")
    lines.append("")

    lines.append("## Design distribution (admitted entries, free text as logged)\n")
    lines.append("| Design | n |")
    lines.append("|---|---|")
    for k, v in sorted(out["design_distribution"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines.append("## Evidence-level distribution (admitted entries, free text as logged)\n")
    lines.append("| Evidence level | n |")
    lines.append("|---|---|")
    for k, v in sorted(out["evidence_level_distribution"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines.append("## Year distribution (admitted entries)\n")
    lines.append(f"Bucketing rule: {out['year_bucketing_rule']}\n")
    lines.append("| Year | n |")
    lines.append("|---|---|")
    for k, v in out["year_distribution"].items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append(f"Numeric year span: {out['year_span_numeric_only']}. "
                  f"Year not parsed: {out['year_not_parsed_count']} entries. "
                  f"2024+2025 (numeric only): {out['count_2024_plus_2025_numeric_only']}. "
                  f"2026 (numeric only): {out['count_2026_numeric_only']}.\n")

    lines.append("## Keyword share: systematic review / guideline / RCT (over design+evidence_level free text)\n")
    lines.append("| Group | n entries | Share of admitted entries |")
    lines.append("|---|---|---|")
    for k, v in out["keyword_share_systematic_review_guideline_rct"].items():
        lines.append(f"| {k} | {v['n_entries']} | {v['share_of_admitted_entries']} |")
    lines.append("")

    lines.append(f"Records linked to at least one of P1-P7 (unique documents, deduped per Finding 2): {out['records_linked_to_ge1_proposition']}\n")

    lines.append("## Per-proposition (P1-P7) linked-record counts (kg/graph.json edges)\n")
    lines.append("| Proposition | Label | Supports | Complicates | Relevant-only | Contradicts | Total linked records |")
    lines.append("|---|---|---|---|---|---|---|")
    for pid, d in out["per_proposition_P1_P7"].items():
        lines.append(
            f"| {pid} | {d['label']} | {d['supports']} | {d['complicates']} | "
            f"{d['relates_to_relevant_only']} | {d['contradicts']} | {d['total_linked_records']} |"
        )
    lines.append("")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
