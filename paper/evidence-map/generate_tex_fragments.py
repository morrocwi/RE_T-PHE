#!/usr/bin/env python3
"""
generate_tex_fragments.py — builds the LaTeX table/bibliography fragments
that sr_main.tex \\input's, from the same logged JSON files build_prisma.py
reads. Run once (or whenever the underlying library/ data changes) and
commit the resulting .tex fragments alongside sr_main.tex, so the
manuscript itself compiles with plain latexmk and no Python step.

Every "finding" cell in the per-proposition tables is copied verbatim
from the admitted library entry's own 'finding' field (falling back to
'verifier_note' only when 'finding' is empty), per the task's honesty
rule: no finding sentence is rewritten with a new claim.

Outputs (written next to this script, all \\input by sr_main.tex):
  frag_prisma_flow_table.tex
  frag_search_queries_table.tex
  frag_prop_P1.tex ... frag_prop_P7.tex
  frag_evidence_gaps_table.tex
  frag_new_bibitems.tex        (bibitems for library records not already
                                 in paper/sections/refs_all.tex)
  frag_copied_bibitems.tex     (bibitems copied verbatim from refs_all.tex
                                 for the records this document cites)
"""
import collections
import glob
import json
import os
import re
import subprocess
import time
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LIBRARY_DIR = os.path.join(REPO_ROOT, "library")
DATA_DIR = os.path.join(LIBRARY_DIR, "data")
KG_PATH = os.path.join(LIBRARY_DIR, "kg", "graph.json")
LIBRARY_JSON_PATH = os.path.join(LIBRARY_DIR, "library.json")
REFS_ALL_PATH = os.path.join(REPO_ROOT, "paper", "sections", "refs_all.tex")
PUBMED_AUTHOR_CACHE_PATH = os.path.join(HERE, "pubmed_authors_cache.json")
PUBMED_ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_TOOL = "tphe_litreview"
PUBMED_EMAIL = "research@example.invalid"
PUBMED_BATCH_SIZE = 50
PUBMED_SLEEP_S = 0.4



def strip_verifier_block(text):
    """Remove a leading '[CORRECTION: ... FIX ...]' verifier block (bracket-balanced) from a charted
    finding and append a short marker, so the public table shows the charted finding text while the
    full verifier note stays in library/library.json. The finding text itself is not rewritten."""
    t = text.lstrip()
    if not t.startswith("[CORRECTION"):
        return text
    depth = 0
    for i, ch in enumerate(t):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                rest = t[i + 1:].strip()
                return (rest + " (Verifier correction recorded in the library entry.)").strip()
    return text


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


MATH_MARKER = {
    "≤": "",
    "≥": "",
    "±": "",
    "×": "",
    "→": "",
}
MATH_MARKER_TEX = {
    "": r"$\le$",
    "": r"$\ge$",
    "": r"$\pm$",
    "": r"$\times$",
    "": r"$\rightarrow$",
}


def tex_escape(s, seqsplit_long_tokens=True):
    if s is None:
        return ""
    s = str(s)
    # Pull out mathematical/comparison symbols Latin Modern's T1 text
    # encoding does not carry as a direct glyph, and stand-ins for
    # typographic dashes/quotes, BEFORE literal-character escaping runs
    # (so the "$" this substitution introduces is not itself escaped).
    for a, marker in MATH_MARKER.items():
        s = s.replace(a, marker)
    text_replacements_pre = [
        ("–", "--"),   # en dash
        ("—", "---"),  # em dash: avoid relying on the raw glyph
        ("‘", "`"),
        ("’", "'"),
        ("“", "``"),
        ("”", "''"),
    ]
    for a, b in text_replacements_pre:
        s = s.replace(a, b)
    # Order matters: backslash first.
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for a, b in replacements:
        s = s.replace(a, b)
    for marker, tex in MATH_MARKER_TEX.items():
        s = s.replace(marker, tex)
    s = s.replace("/", r"\slash{}")
    if seqsplit_long_tokens:
        # Caption text is a LaTeX "moving argument" (written to .aux/.lot);
        # \seqsplit is fragile there, so long-token wrapping is skipped for
        # any string passed with seqsplit_long_tokens=False (proposition
        # labels used inside \caption{...}).
        import re as _re
        s = _re.sub(r"(?<![\\{])\b[A-Za-z0-9]{11,}\b(?!\})", lambda m: "\\seqsplit{" + m.group(0) + "}", s)
    return s


def slugify(*parts):
    """Deterministic ASCII slug of the given text parts, joined with '-'.
    Mirrors build_prisma.py's slugify/dedupe_key exactly (kept as a
    second, independent copy here rather than a shared import, since each
    script is meant to run standalone) -- used only as the fallback
    document key for admitted entries whose library.json 'identifier'
    field is blank."""
    pieces = []
    for p in parts:
        s = str(p or "").strip().lower()
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        if s:
            pieces.append(s)
    return "-".join(pieces)


def document_key(entry):
    """The real-world-document identity of a library entry: PMID when
    present, else the entry's own non-blank 'identifier', else a
    deterministic fallback slug of first_author+year+title. Two
    library.json entries that share the same *raw* library id (e.g. both
    blank-identifier entries collapse to the literal raw id "REF:") but
    are genuinely different documents get distinct document_key() values
    here, so they are never silently collapsed into one row -- this is
    the same fix as build_prisma.py's dedupe_key, applied at fragment-
    generation time (Finding 2)."""
    pmid = entry.get("pmid")
    if pmid:
        return ("pmid", pmid)
    ident = entry.get("identifier")
    if ident:
        return ("identifier", ident)
    slug = slugify(entry.get("first_author"), entry.get("year"), entry.get("title"))
    return ("fallback_slug", slug or entry.get("id"))


AUTHOR_COMMENTARY_SPLIT_RE = re.compile(r"\s*(?:/| \(co-first authorship| \(Archdiocese)")

# Institutional/group authors (WHO, GBD Collaborators, US PSTF, etc.) are
# never a "Surname FirstName [Middle]" personal name -- collapsing them to
# initials would corrupt the name (e.g. "World Health Organization" ->
# "World HO"). Detected by a simple marker-word scan, case-insensitive.
INSTITUTIONAL_MARKERS = (
    "organization", "organisation", "collaborator", "task force",
    "committee", "council", "institute", "university",
    "ministry", "government", "who ", "who/", "department",
)


def looks_institutional(s):
    low = s.lower()
    return any(m in low for m in INSTITUTIONAL_MARKERS)


def clean_author_field(raw):
    """Best-effort Vancouver-style author normalisation applied at render
    time only (library.json itself is never edited -- Finding 5).

    - Strips any editorial/verifier commentary appended to the
      first_author field after a ' / ' separator or a parenthetical aside
      (e.g. "Kalichman SC / or commentary author per abstract." ->
      "Kalichman SC"), so no verifier commentary reaches the bibitem text.
    - Collapses a "Surname FirstName [Middle]" free-text name (no data
      loss versus the source string; the initials are derived from the
      very same string already present in library.json) into Vancouver
      "Surname XY" initials style, e.g. "Hill Amber L" -> "Hill AL".
    - A bare surname with no first name/initial at all (e.g. "Tiwari")
      is left as-is: no name-part data exists in library.json to derive
      an initial from without an external lookup, which is out of scope
      here (library.json is not edited and no live source is queried).
    """
    if not raw:
        return raw
    s = str(raw).strip()
    if looks_institutional(s):
        return s
    # Drop trailing editorial/verifier commentary appended after a
    # " / " separator or a parenthetical aside.
    s = AUTHOR_COMMENTARY_SPLIT_RE.split(s, maxsplit=1)[0].strip()
    s = s.rstrip(".").strip()
    if not s:
        return raw
    if looks_institutional(s):
        return s
    tokens = s.split()
    if len(tokens) >= 3:
        surname, rest = tokens[0], tokens[1:]
        # Already-Vancouver ("Surname AB") second token is a short
        # all-caps initials group -- leave untouched.
        if len(rest) == 1 and rest[0].isupper() and len(rest[0]) <= 3:
            return s
        initials = "".join(w[0].upper() for w in rest if w)
        return f"{surname} {initials}"
    return s


def load_pubmed_author_cache():
    if os.path.exists(PUBMED_AUTHOR_CACHE_PATH):
        return load_json(PUBMED_AUTHOR_CACHE_PATH)
    return {}


def save_pubmed_author_cache(cache):
    with open(PUBMED_AUTHOR_CACHE_PATH, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def fetch_pubmed_esummary_batch(pmids):
    """One esummary.fcgi call for up to PUBMED_BATCH_SIZE PMIDs. Returns the
    'result' dict of the parsed JSON response (keyed by PMID string), or an
    empty dict on any network/parse failure -- never raises, so a missing
    network connection degrades to "use clean_author_field() as before"
    rather than aborting the whole build."""
    ids_param = ",".join(pmids)
    cmd = [
        "curl", "-s", "-m", "30",
        PUBMED_ESUMMARY_URL,
        "--data-urlencode", "db=pubmed",
        "--data-urlencode", f"id={ids_param}",
        "--data-urlencode", "retmode=json",
        "--data-urlencode", f"tool={PUBMED_TOOL}",
        "--data-urlencode", f"email={PUBMED_EMAIL}",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if proc.returncode != 0 or not proc.stdout.strip():
            print(f"  esummary fetch failed for batch of {len(pmids)} pmids (curl rc={proc.returncode})")
            return {}
        data = json.loads(proc.stdout)
        return data.get("result", {})
    except Exception as exc:  # noqa: BLE001 -- deliberately broad: never abort the build
        print(f"  esummary fetch failed for batch of {len(pmids)} pmids ({exc})")
        return {}


def fetch_pubmed_authors_for(pmids):
    """Ensures every PMID in `pmids` has a cached esummary record in
    PUBMED_AUTHOR_CACHE_PATH, fetching only what is missing (batches of
    <=PUBMED_BATCH_SIZE, 0.4s sleep between calls), then returns the full
    cache dict (pmid -> esummary result dict). The cache file is committed
    alongside the .tex fragments so a rebuild with no network access is
    reproducible offline (every previously-fetched pmid is already there;
    only genuinely new pmids would need a live fetch)."""
    cache = load_pubmed_author_cache()
    missing = sorted({p for p in pmids if p and p not in cache})
    if missing:
        print(f"Fetching PubMed esummary for {len(missing)} new PMID(s) not in {os.path.basename(PUBMED_AUTHOR_CACHE_PATH)}...")
        for i in range(0, len(missing), PUBMED_BATCH_SIZE):
            batch = missing[i:i + PUBMED_BATCH_SIZE]
            result = fetch_pubmed_esummary_batch(batch)
            for pmid in batch:
                if pmid in result and isinstance(result[pmid], dict):
                    cache[pmid] = result[pmid]
                else:
                    cache[pmid] = {"_fetch_error": True}
            time.sleep(PUBMED_SLEEP_S)
        save_pubmed_author_cache(cache)
        print(f"Wrote {PUBMED_AUTHOR_CACHE_PATH} ({len(cache)} cached PMIDs)")
    return cache


def pubmed_author_field(pmid, cache, fallback_first_author):
    """Vancouver-style first-author field derived from a cached PubMed
    esummary record: 'Surname XY' for the first author, '+ et al.' when the
    record has more than one author, institutional/group authors (PubMed
    authtype 'CollectiveName', or a name matching INSTITUTIONAL_MARKERS)
    kept verbatim. Falls back to clean_author_field(fallback_first_author)
    (the library.json-derived value) when the PMID has no usable cached
    esummary record (fetch failure, or no 'authors' array), so a network
    outage degrades gracefully rather than corrupting the bibliography."""
    rec = cache.get(pmid) or {}
    authors = rec.get("authors")
    if not isinstance(authors, list) or not authors:
        return clean_author_field(fallback_first_author), False
    first = authors[0] or {}
    name = str(first.get("name", "")).strip()
    if not name:
        return clean_author_field(fallback_first_author), False
    is_group = first.get("authtype") == "CollectiveName" or looks_institutional(name)
    if is_group:
        return name, True
    if len(authors) > 1:
        return f"{name} et al.", True
    return name, True


def main():
    kg = load_json(KG_PATH)
    library = load_json(LIBRARY_JSON_PATH)
    refs_all_text = open(REFS_ALL_PATH, "r", encoding="utf-8").read()

    entries_by_pmid = {}
    for e in library.get("entries", []):
        pmid = e.get("pmid")
        if pmid and pmid not in entries_by_pmid:
            entries_by_pmid[pmid] = e
    # Group by raw library id first (this is what a kg/graph.json edge's
    # 'source' resolves to), then split each raw-id group into distinct
    # real-world documents via document_key(), keeping exactly one
    # representative entry per distinct document (Finding 2). For every
    # raw id that never collided this is a single-entry group, identical
    # in effect to the old {e["id"]: e} last-wins dict. For the one
    # illegitimate collision (raw id "REF:", two different WHO documents
    # both left with a blank 'identifier') this now yields two distinct
    # document groups instead of one, so the 2013 guideline's own finding
    # is no longer shadowed by the 2014 handbook's.
    raw_id_groups = collections.defaultdict(list)
    for e in library.get("entries", []):
        raw_id_groups[e["id"]].append(e)

    entries_by_recid = {}  # raw library id -> list of representative entries (1 per distinct document)
    for raw_id, group in raw_id_groups.items():
        seen_docs = {}
        for e in group:
            dk = document_key(e)
            if dk not in seen_docs:
                seen_docs[dk] = e
        entries_by_recid[raw_id] = list(seen_docs.values())

    # ---- map PMID -> existing \bibitem key + full bibitem text, from
    #      paper/sections/refs_all.tex (Vancouver style, source
    #      of truth already used by the T-PHE full paper) ----
    bibitem_blocks = re.findall(
        r"(\\bibitem\{([^}]+)\}.*?)(?=\\bibitem\{|\\end\{thebibliography\})",
        refs_all_text,
        flags=re.DOTALL,
    )
    pmid_to_key = {}
    key_to_text = {}
    for block_text, key in bibitem_blocks:
        block_text = block_text.strip()
        key_to_text[key] = block_text
        m = re.search(r"PMID:\s*(\d+)", block_text)
        if m:
            pmid_to_key.setdefault(m.group(1), key)

    # ---------------------------------------------------------------
    # Proposition tables
    # ---------------------------------------------------------------
    nodes = kg["nodes"]
    edges = kg["edges"]
    props = [n for n in nodes if n["type"] == "proposition"]

    direction_label = {
        "supports": "Supports",
        "complicates": "Complicates",
        "relates_to": "Relevant only",
        "contradicts": "Contradicts",
    }

    new_bibitem_keys = {}  # pmid -> generated key
    used_keys_in_order = []

    def cite_key_for_pmid(pmid):
        if pmid in pmid_to_key:
            key = pmid_to_key[pmid]
        elif pmid in new_bibitem_keys:
            key = new_bibitem_keys[pmid]
        else:
            key = f"srp{pmid}"
            new_bibitem_keys[pmid] = key
        if key not in used_keys_in_order:
            used_keys_in_order.append(key)
        return key

    for p in props:
        pid = p["id"]
        rows = []
        for e in edges:
            if e.get("target") != pid:
                continue
            rel = e.get("relation")
            if rel not in direction_label:
                continue
            rec_id = e.get("source")
            rec_node = next((n for n in nodes if n["id"] == rec_id), None)
            matched_entries = entries_by_recid.get(rec_id) or []
            if not matched_entries and rec_id and rec_id.startswith("PMID:"):
                pmid = rec_id.split("PMID:", 1)[1]
                pe = entries_by_pmid.get(pmid)
                if pe is not None:
                    matched_entries = [pe]
            if not matched_entries:
                # record referenced in the graph but not resolvable to an
                # admitted library entry (should not occur for P1-P7 given
                # the checked edge set, but fail closed rather than guess)
                rows.append(
                    {
                        "cite": rec_id or "UNRESOLVED",
                        "author_year": tex_escape(rec_node.get("label") if rec_node else rec_id),
                        "design": "not derivable from the logged files",
                        "population": "not derivable from the logged files",
                        "finding": "not derivable from the logged files",
                        "direction": direction_label[rel],
                    }
                )
                continue
            # One row per distinct document resolved under this edge's
            # source id (normally exactly one; two only for the former
            # blank-identifier collision, see document_key() above).
            for entry in matched_entries:
                pmid = entry.get("pmid")
                cite = f"\\cite{{{cite_key_for_pmid(pmid)}}}" if pmid else "(no PMID)"
                author = clean_author_field(entry.get("first_author", ""))
                author_year = tex_escape(f"{author} {entry.get('year','')}".strip())
                design = tex_escape(entry.get("design") or "not derivable from the logged files")
                population = tex_escape(entry.get("population_setting") or "not derivable from the logged files")
                finding = entry.get("finding") or entry.get("verifier_note") or "not derivable from the logged files"
                finding = strip_verifier_block(finding)
                finding = tex_escape(finding)
                rows.append(
                    {
                        "cite": cite,
                        "author_year": author_year,
                        "design": design,
                        "population": population,
                        "finding": finding,
                        "direction": direction_label[rel],
                    }
                )

        # stable order: supports, complicates, relevant-only, contradicts;
        # within each group, by first_author/year as charted
        order = {"Supports": 0, "Complicates": 1, "Relevant only": 2, "Contradicts": 3}
        rows.sort(key=lambda r: (order.get(r["direction"], 9), r["author_year"]))

        label = tex_escape(p.get("label", ""), seqsplit_long_tokens=False)
        out_path = os.path.join(HERE, f"frag_prop_{pid}.tex")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(f"% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
            fh.write(f"\\begin{{longtable}}{{@{{}}L{{2.0cm}}L{{2.0cm}}L{{2.1cm}}L{{6.2cm}}L{{1.9cm}}@{{}}}}\n")
            fh.write(
                f"\\caption{{{pid}: {label}. Record, design, population/setting, "
                f"finding as charted (verbatim from the library record), and direction "
                f"relative to the proposition. n={len(rows)} linked records "
                f"(kg/graph.json edges).}}\\label{{tab:{pid.lower()}}}\\\\\n"
            )
            fh.write("\\toprule\n")
            fh.write("\\textbf{Record} & \\textbf{Design} & \\textbf{Population\\slash{}setting} & \\textbf{Finding (as charted)} & \\textbf{Direction}\\\\\n")
            fh.write("\\midrule\n\\endfirsthead\n")
            fh.write(f"\\multicolumn{{5}}{{l}}{{\\textit{{{pid} continued}}}}\\\\\n")
            fh.write("\\toprule\n")
            fh.write("\\textbf{Record} & \\textbf{Design} & \\textbf{Population\\slash{}setting} & \\textbf{Finding (as charted)} & \\textbf{Direction}\\\\\n")
            fh.write("\\midrule\n\\endhead\n")
            fh.write("\\bottomrule\n\\endfoot\n")
            for r in rows:
                fh.write(
                    f"{r['author_year']} {r['cite']} & {r['design']} & {r['population']} & "
                    f"{r['finding']} & {r['direction']}\\\\\n"
                )
                fh.write("\\\\[3pt]\n")
            fh.write("\\end{longtable}\n")
        print(f"Wrote {out_path} ({len(rows)} rows)")

    # ---------------------------------------------------------------
    # New bibitems (records cited above but absent from refs_all.tex)
    # ---------------------------------------------------------------
    out_path = os.path.join(HERE, "frag_new_bibitems.tex")
    pubmed_cache = fetch_pubmed_authors_for(new_bibitem_keys.keys())
    n_from_pubmed = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
        fh.write(
            "% Vancouver-style bibitems for library records cited in this document that\n"
            "% are not among the \\bibitem entries copied verbatim from\n"
            "% paper/sections/refs_all.tex. Built directly from library/library.json\n"
            "% fields (title, journal, year, pmid); the author field is taken from a cached\n"
            "% PubMed esummary record (pubmed_authors_cache.json) keyed by PMID, first author\n"
            "% 'Surname XY' + ' et al.' when more than one author, institutional/group authors\n"
            "% kept verbatim, falling back to the library.json first_author field only when no\n"
            "% cached esummary record is available for that PMID.\n"
        )
        for pmid, key in sorted(new_bibitem_keys.items(), key=lambda kv: kv[1]):
            entry = entries_by_pmid.get(pmid)
            if entry is None:
                continue
            author_raw, from_pubmed = pubmed_author_field(pmid, pubmed_cache, entry.get("first_author", ""))
            if from_pubmed:
                n_from_pubmed += 1
            # author_raw may already end with '.' (e.g. "... et al."); the
            # template below adds its own trailing '.', so strip any
            # pre-existing one first to avoid a rendered "et al..".
            author = tex_escape(author_raw.rstrip("."))
            title_raw = str(entry.get("title", "")).strip()
            # Finding 4: ensure a period separates the article title from
            # the journal name even when the source 'title' field in
            # library.json itself has no trailing period -- previously
            # the template inserted only a bare space, so the journal name
            # read as if it were the tail of the title.
            if title_raw and not title_raw.endswith((".", "?", "!")):
                title_raw += "."
            title = tex_escape(title_raw)
            journal = tex_escape(entry.get("journal", ""))
            year = tex_escape(entry.get("year", ""))
            fh.write(
                f"\\bibitem{{{key}}} {author}. {title} {journal}. {year}. PMID: {pmid}.\n"
            )
    print(f"Wrote {out_path} ({len(new_bibitem_keys)} new bibitems, {n_from_pubmed} author fields from cached PubMed esummary)")

    # ---------------------------------------------------------------
    # Copied bibitems (verbatim, for keys already in refs_all.tex that
    # this document actually cites)
    # ---------------------------------------------------------------
    out_path = os.path.join(HERE, "frag_copied_bibitems.tex")
    copied_keys = [k for k in used_keys_in_order if k in key_to_text]
    # keep numeric-ish refN ordering stable and readable
    def sort_key(k):
        m = re.match(r"ref(\d+)", k)
        return (0, int(m.group(1))) if m else (1, k)

    copied_keys_sorted = sorted(set(copied_keys), key=sort_key)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
        fh.write(
            "% \\bibitem text copied verbatim from paper/sections/refs_all.tex\n"
            "% for every reference key this document cites.\n"
        )
        for k in copied_keys_sorted:
            fh.write(key_to_text[k] + "\n")
    print(f"Wrote {out_path} ({len(copied_keys_sorted)} copied bibitems)")

    # ---------------------------------------------------------------
    # Evidence-gaps table (from search-*.json 'gaps_noted' arrays,
    # grouped by the four themes the task specifies; text is
    # paraphrase-free excerpting of the logged gap statements)
    # ---------------------------------------------------------------
    write_gaps_table()

    # PRISMA flow + search-queries tables read prisma_counts.json (built
    # by build_prisma.py) so run that first if it has not been run.
    write_prisma_flow_table()
    write_search_queries_table()


def write_gaps_table():
    gap_files = sorted(glob.glob(os.path.join(DATA_DIR, "search-*.json")))
    themes = {
        "Thai / Thai-Muslim samples": [],
        "Premarital-specific trials": [],
        "Decision-control instruments": [],
        "Layer 0 / Layer 2 evidence": [],
    }
    theme_keywords = {
        "Thai / Thai-Muslim samples": ["thailand", "thai ", "muslim", "deep south", "southern border"],
        "Premarital-specific trials": ["premarital", "pre-nikah", "marriage preparation", "marriage-preparation"],
        "Decision-control instruments": ["decision-control", "decision control", "instrument", "measure", "scale", "validated"],
        "Layer 0 / Layer 2 evidence": ["self-check", "layer 0", "layer 2", "peer community", "moderat", "anonymous"],
    }
    for f in gap_files:
        d = load_json(f)
        angle = d.get("angle", os.path.basename(f))
        for g in d.get("gaps_noted", []) or []:
            low = g.lower()
            placed = False
            for theme, kws in theme_keywords.items():
                if any(kw in low for kw in kws):
                    themes[theme].append((angle, g))
                    placed = True
                    break
            if not placed:
                continue  # not one of the four requested gap themes

    out_path = os.path.join(HERE, "frag_evidence_gaps_table.tex")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
        fh.write("\\begin{longtable}{@{}L{3.0cm}L{2.4cm}L{9.0cm}@{}}\n")
        fh.write(
            "\\caption{Evidence gaps, excerpted from the gaps\\_noted field logged in each "
            "search-*.json angle file at the time of the search pass. Text is the search "
            "log's own statement, condensed to fit the table column, not a new claim.}"
            "\\label{tab:gaps}\\\\\n"
        )
        fh.write("\\toprule\n\\textbf{Gap theme} & \\textbf{Search angle} & \\textbf{Logged gap statement}\\\\\n\\midrule\n\\endfirsthead\n")
        fh.write("\\multicolumn{3}{l}{\\textit{Table \\thetable{} continued}}\\\\\n\\toprule\n")
        fh.write("\\textbf{Gap theme} & \\textbf{Search angle} & \\textbf{Logged gap statement}\\\\\n\\midrule\n\\endhead\n")
        fh.write("\\bottomrule\n\\endfoot\n")
        for theme, items in themes.items():
            for angle, g in items:
                g_short = g.strip()
                if len(g_short) > 420:
                    g_short = g_short[:417] + "..."
                fh.write(f"{tex_escape(theme)} & {tex_escape(angle)} & {tex_escape(g_short)}\\\\\n\\\\[3pt]\n")
        fh.write("\\end{longtable}\n")
    total = sum(len(v) for v in themes.values())
    print(f"Wrote {out_path} ({total} gap rows across {len(themes)} themes)")


def write_prisma_flow_table():
    counts_path = os.path.join(HERE, "prisma_counts.json")
    if not os.path.exists(counts_path):
        print("prisma_counts.json not found; run build_prisma.py first. Skipping flow table.")
        return
    d = load_json(counts_path)
    flow = d["prisma_flow"]
    n_angle_files = d["provenance"]["n_angle_files"]
    out_path = os.path.join(HERE, "frag_prisma_flow_table.tex")
    rows = [
        (f"Records identified through structured PubMed E-utilities searches and logged reading-list passes (sum of hits across {n_angle_files} search-*.json angle files)", flow["records_identified_total_sum_of_search_hits"]),
        ("Total logged PubMed E-utilities queries run (queries\\_run arrays)", flow["total_pubmed_queries_logged"]),
        ("Duplicate PMIDs removed across search files", flow["duplicates_removed_by_pmid"]),
        ("Unique PMIDs identified by search", flow["unique_identified_pmids"]),
        ("Records passed to the independent verifier", flow["records_verified_total"]),
        ("Verifier verdict: KEEP", flow["verifier_verdict_counts"].get("KEEP", 0)),
        ("Verifier verdict: FIX (correction applied, then admitted)", flow["verifier_verdict_counts"].get("FIX", 0)),
        ("Verifier verdict: DROP (not admitted)", flow["verifier_verdict_counts"].get("DROP", 0)),
        ("Verifier verdict: CONTEXT-ONLY (not PubMed-indexed; no evidential weight)", flow["verifier_verdict_counts"].get("CONTEXT-ONLY", 0)),
        ("Admitted entries, category-level rows (a record placed in more than one category counts once per category)", flow["admitted_entries_total_category_rows"]),
        ("Admitted unique records (PMID, or identifier for a non-PMID guidance document)", flow["admitted_unique_records_pmid_or_identifier"]),
        ("Admitted unique PMIDs", flow["admitted_unique_pmids"]),
        ("Admitted entries without a PMID (WHO/NICE/Cochrane/JAKIM/Malaysia-government guidance)", flow["admitted_entries_without_pmid_guidance_docs"]),
        ("Not admitted (DROP, library.json not\\_admitted list)", flow["not_admitted_dropped_count"]),
        ("Context-only sources logged (not PubMed-indexed, carry no evidential weight)", flow["context_only_source_count_not_pubmed"]),
    ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
        fh.write("\\begin{longtable}{@{}L{13.5cm}r@{}}\n")
        fh.write("\\caption{PRISMA-ScR flow counts, computed by build\\_prisma.py directly from library/data/search-*.json, library/data/verify-*.json and library/library.json.}\\label{tab:prismaflow}\\\\\n")
        fh.write("\\toprule\n\\textbf{Stage} & \\textbf{n}\\\\\n\\midrule\n\\endfirsthead\n")
        fh.write("\\multicolumn{2}{l}{\\textit{Table \\thetable{} continued}}\\\\\n\\toprule\n\\textbf{Stage} & \\textbf{n}\\\\\n\\midrule\n\\endhead\n")
        fh.write("\\bottomrule\n\\endfoot\n")
        for label, n in rows:
            fh.write(f"{label} & {n}\\\\\n")
        fh.write("\\end{longtable}\n")
    print(f"Wrote {out_path}")


def write_search_queries_table():
    search_files = sorted(glob.glob(os.path.join(DATA_DIR, "search-*.json")))
    out_path = os.path.join(HERE, "frag_search_queries_table.tex")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("% Auto-generated by generate_tex_fragments.py -- do not hand-edit.\n")
        fh.write("\\begin{longtable}{@{}L{3.4cm}L{11.0cm}@{}}\n")
        fh.write(
            "\\caption{Search strategy: the exact PubMed E-utilities query strings logged "
            "per angle (queries\\_run in each search-*.json file). Six angle files "
            "(external-culture, external-dossier, external-draft, external-multicultural, "
            "external-thailand, external-wellbeing) were supplied as logged external reading "
            "lists rather than a queries\\_run search log, and carry no query strings to "
            "reproduce here; this is stated, not estimated.}\\label{tab:queries}\\\\\n"
        )
        fh.write("\\toprule\n\\textbf{Search angle} & \\textbf{Query string}\\\\\n\\midrule\n\\endfirsthead\n")
        fh.write("\\multicolumn{2}{l}{\\textit{Table \\thetable{} continued}}\\\\\n\\toprule\n\\textbf{Search angle} & \\textbf{Query string}\\\\\n\\midrule\n\\endhead\n")
        fh.write("\\bottomrule\n\\endfoot\n")
        for f in search_files:
            d = load_json(f)
            angle = d.get("angle", os.path.basename(f))
            queries = d.get("queries_run")
            if not queries:
                fh.write(f"{tex_escape(angle)} & \\textit{{not derivable from the logged files (no queries\\_run log; supplied as an external reading list)}}\\\\\n\\\\[3pt]\n")
                continue
            for i, q in enumerate(queries):
                label = tex_escape(angle) if i == 0 else ""
                q_tex = tex_escape(q).replace("+", "+\\allowbreak{}")
                fh.write(f"{label} & \\texttt{{{q_tex}}}\\\\\n")
            fh.write("\\\\[3pt]\n")
        fh.write("\\end{longtable}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
