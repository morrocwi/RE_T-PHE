#!/usr/bin/env python3
"""Build the evidence library (library/*.md) from verified search records in library/data/.

Inputs (library/data/):
  search-<angle>.json   records produced by a literature-search pass (one per angle)
  verify-<angle>.json   independent re-fetch verification of every record in that angle

Only records whose verifier verdict is KEEP or FIX are published; FIX records carry the verifier's
correction note verbatim. DROP records are listed by identifier in a "not admitted" section so the
exclusion is visible. Records are de-duplicated by PMID across angles (first category wins; the
other angles are noted).

Run:  python3 tools/build_library.py
"""
import glob
import json
import os
import re
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "library", "data")
OUT = os.path.join(ROOT, "library")

# angle key -> (file number, category title, scope note)
CATEGORIES = OrderedDict([
    ("primary-prevention-frameworks", ("01", "Burden of intimate-partner violence and primary-prevention frameworks",
        "Global burden estimates, WHO RESPECT-related evidence, community and faith-based prevention trials.")),
    ("premarital-education-outcomes", ("02", "Premarital and relationship education: measured outcomes",
        "What relationship and premarital education has and has not measured; meta-analyses and trials.")),
    ("ipv-screening-response", ("03", "Screening, first-line response and referral",
        "Identification versus outcome change; USPSTF, Cochrane and WHO guidance; first-line response trials.")),
    ("couple-work-safety-coercive-control", ("04", "Couple-based work and coercive control",
        "When joint work is contraindicated; coercive-control measurement.")),
    ("decision-autonomy-measures", ("05", "Decision autonomy, reproductive coercion and measurement instruments",
        "Constructs and scales adjacent to decision control; where they have and have not been validated.")),
    ("muslim-thailand-southeast-asia", ("06", "Muslim populations, Thailand and Southeast Asia",
        "Regional and population-specific evidence; explicitly labelled where not Thai.")),
    ("external-multicultural", ("07", "Multicultural clinical safety and language access",
        "Cultural humility, cultural safety, interpreter and language-discordance evidence; Thai health-system studies.")),
    ("external-draft", ("08", "Preconception medicine, premarital screening and adjacent guidance",
        "Preconception care, premarital genetic screening, coercive-control and reproductive-coercion reviews, decision aids.")),
    ("external-dossier", ("09", "Global guidance, frameworks and methods",
        "WHO, USPSTF, NICE, Cochrane, MRC complex-intervention and adaptation guidance; major reviews.")),
    ("external-thailand", ("10", "Thailand and the southern border provinces",
        "Thai epidemiology and health-system evidence; national-journal sources separated as context.")),
    ("external-wellbeing", ("11", "Premarital knowledge and well-being pathways",
        "Premarital and relationship education meta-analyses; reproductive-health literacy trials; marital quality and health associations.")),
    ("external-culture", ("12", "Culture as a health determinant and intercultural coexistence",
        "Lancet commissions and series on culture, racism and migration; cultural-competence training reviews; culturally adapted interventions; language concordance; social cohesion; group family programmes in diverse populations.")),
    ("digital-self-assessment", ("13", "Digital self-assessment and safety decision aids for intimate-partner violence",
        "Web, app and online self-assessment or decision-aid trials used by the person alone; anonymous self-screening; safety of technology-delivered tools.")),
    ("peer-online-support", ("14", "Peer online support, moderated communities and digital safe spaces",
        "Online peer support for relationship safety and young people's mental health; moderation; technology-facilitated abuse and surveillance risks.")),
    ("assessor-checkin", ("15", "Assessor independence, risk assessment and check-in models",
        "Conflict of interest and independence in safeguarding decisions; structured IPV risk assessment; warm handoff, navigation, brief-contact and single-session models.")),
    ("manipulation-literacy", ("16", "Recognition of coercive control and psychological manipulation; inoculation",
        "Psychological inoculation and prebunking trials; recognition of coercive control, gaslighting and emotional abuse; dating-violence prevention with recognition outcomes; labelling abuse and help-seeking.")),
    ("humility-compassion", ("17", "Humility, compassion, self-regulation and responsibility: psychological and health evidence",
        "Intellectual and relational humility, cultural humility, self-compassion and empathy, self-regulation/conscientiousness, trustworthiness; Islamic psychology and religiosity in relation to relationship safety and health. These constructs are the medical-science counterparts of the abstract's ethic: limited knowledge (faqr), conscientious restraint (taqwa), entrusted responsibility (amanah), justice (ʿadl) — the ethic names the duty; the evidence here says what is known about the construct.")),
    ("islamic-medical-ethics", ("18", "Islamic medical ethics and spirituality in Muslim health care (tier-one sources only)",
        "PubMed-indexed systematic reviews, guidelines and leading-journal articles on Islamic bioethics, patient autonomy and consent in Muslim contexts, spirituality and health outcomes in Muslim populations, and faith-sensitive care; lower-tier sources excluded.")),
])

PROPOSITIONS = [
    "A governance layer improves decision control beyond content-only education",
    "A routine private channel makes materially relevant concerns more visible",
    "Cultural intelligibility helps only when culture cannot override consent or safety",
    "A stop rule prevents routine joint education from worsening risk when fear or coercion appears",
    "Referral quality depends on timeliness, accessibility and follow-through, not offer alone",
    "Conventional programme success can coexist with T-PHE failure",
    "Repairability is necessary because relevant information emerges over time",
]
SAFEGUARDS = ["epistemic humility", "cultural intelligibility", "affected-person visibility", "dignity and consent",
              "bounded authority and referral", "repairability"]
OUTCOME_DOMAINS = ["decision control", "coercion recognition", "reproductive coercion", "help-seeking", "referral",
                   "mental-health literacy", "reproductive-health literacy", "harms", "stop rule", "private channel",
                   "self-assessment", "decision aid", "peer support", "online community", "technology-facilitated abuse",
                   "independent assessor", "conflict of interest", "check-in", "warm handoff", "single-session",
                   "inoculation", "prebunking", "gaslighting", "emotional abuse", "recognition of abuse", "dating violence",
                   "humility", "self-compassion", "empathy", "self-regulation", "conscientiousness", "trustworthiness", "religiosity"]

VERDICT_ORDER = {"KEEP": 0, "FIX": 1, "CONTEXT-ONLY": 2, "DROP": 3}


def load(angle):
    s = os.path.join(DATA, f"search-{angle}.json")
    v = os.path.join(DATA, f"verify-{angle}.json")
    if not (os.path.exists(s) and os.path.exists(v)):
        return None, None
    return json.load(open(s, encoding="utf-8")), json.load(open(v, encoding="utf-8"))


def ident(rec):
    return rec.get("pmid") or rec.get("id") or ""


def norm_pmid(x):
    x = str(x).strip()
    return x if re.fullmatch(r"\d{6,9}", x) else None


def main():
    seen = {}          # pmid -> category number
    per_cat = {}
    not_admitted = defaultdict(list)
    context_only = defaultdict(list)
    totals = defaultdict(int)

    for angle, (num, title, scope) in CATEGORIES.items():
        S, V = load(angle)
        if S is None:
            print(f"notice: no search/verify pair for angle '{angle}' (category {num}); skipped")
            continue
        vmap = {}
        for vr in V.get("verified", []):
            for k in (vr.get("id"), vr.get("pmid")):
                if k:
                    vmap[str(k)] = vr
        rows = []
        vlist = V.get("verified", [])
        for i, rec in enumerate(S.get("records", [])):
            key = str(ident(rec))
            if key in ("", "None", "null"):
                key = "NOPMID:" + re.sub(r"[^A-Za-z0-9]+", "-", str(rec.get("title", ""))[:50]).strip("-")
            vr = vmap.get(str(ident(rec))) or vmap.get(str(rec.get("id", ""))) or vmap.get(str(rec.get("pmid", "")))
            if (vr is None or str(vr.get("pmid")) in ("None", "")) and i < len(vlist) and str(vlist[i].get("pmid")) in ("None", "", "null") and str(ident(rec)) in ("", "None", "null"):
                vr = vlist[i]
            verdict = (vr or {}).get("verdict", "UNVERIFIED")
            if verdict == "DROP" or vr is None:
                not_admitted[num].append((key, (vr or {}).get("note", "no verification record")))
                continue
            if verdict == "CONTEXT-ONLY":
                context_only[num].append((key, rec.get("claim") or rec.get("key_finding", ""), (vr or {}).get("note", "")))
                continue
            pm = norm_pmid((vr or {}).get("pmid") or key)
            dup = seen.get(pm) if pm else None
            rows.append((rec, vr, dup))
            if pm and not dup:
                seen[pm] = num
        per_cat[num] = (title, scope, angle, rows, S.get("queries_run", []), S.get("limits_of_this_search", ""), S.get("source", ""))
        totals[num] = len(rows)

    index = ["# Evidence library — index", "",
             "> Built by `tools/build_library.py` from `library/data/`. Every entry was produced by a literature-search",
             "> pass over PubMed (NCBI E-utilities) or supplied as an external reading list, and then re-fetched and",
             "> checked by an independent verifier. Entries marked **FIX** carry the verifier's correction verbatim;",
             "> entries the verifier could not confirm are listed under *Not admitted*. This is a targeted, verified",
             "> reading library, **not a systematic review**: no protocol registration, no duplicate screening, no",
             "> risk-of-bias assessment. Scope rule: PubMed-indexed literature and global guidance (WHO, USPSTF, NICE,",
             "> Cochrane, MRC). Sources outside that scope appear only as *context* and carry no evidential weight.",
             "", "| # | Category | Admitted entries | File |", "|---|---|---|---|"]
    for num, (title, scope, angle, rows, q, lim, src) in sorted(per_cat.items()):
        fn = f"{num}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}.md"
        index.append(f"| {num} | {title} | {len(rows)} | [{fn}]({fn}) |")
        md = [f"# {num}. {title}", "", f"*Scope:* {scope}", "",
              "*Provenance of the text in this table:* the **Finding** and **Relevance annotation** columns are AI-drafted readings of the PubMed abstract, checked by an independent verifier; they are not the authors' own wording. The **Verifier** column shows the verdict and, for FIX entries, the correction that must be applied before citing.", ""]
        if src:
            md += [f"*Origin:* {src}. Citations were supplied as a reading list and then verified; annotations below are limited to what the verifier confirmed.", ""]
        if q:
            md += ["*Search queries run (PubMed E-utilities):*", ""] + [f"- `{x}`" for x in q] + [""]
        if lim:
            md += [f"*Limits stated by the searcher:* {lim}", ""]
        md += ["| ID | Reference | Design / evidence level | Finding as supported by the abstract | Relevance annotation | Verifier |",
               "|---|---|---|---|---|---|"]
        for rec, vr, dup in sorted(rows, key=lambda r: (VERDICT_ORDER.get((r[1] or {}).get("verdict", "KEEP"), 9), str(r[0].get("year", "")))):
            key = str(ident(rec))
            pm = norm_pmid((vr or {}).get("pmid") or key)
            link = f"[{pm}](https://pubmed.ncbi.nlm.nih.gov/{pm}/)" if pm else key
            fa = (vr or {}).get("first_author") or rec.get("first_author", "")
            title_ = (vr or {}).get("resolved_title") or rec.get("title", "")
            year = (vr or {}).get("year") or rec.get("year", "")
            journal = (vr or {}).get("journal") or rec.get("journal", "")
            ref = f"{fa}. {title_}. *{journal}* {year}.".replace("..", ".")
            design = rec.get("design", "") or ""
            lvl = rec.get("evidence_level", "")
            dl = f"{design}" + (f" — {lvl}" if lvl and lvl != design else "")
            finding = rec.get("key_finding") or rec.get("claim", "")
            rel = rec.get("relevance_to_tphe", "") or (vr or {}).get("relevance_caution", "")
            verdict = (vr or {}).get("verdict", "")
            note = (vr or {}).get("note", "")
            if verdict == "FIX" and note:
                # the verifier's correction leads; the drafted text follows, marked, so the wrong reading is never shown first
                finding = f"**Read with correction:** {note} — *as drafted:* {finding}"
                if rel:
                    rel = f"*as drafted, subject to the correction:* {rel}"
            vcell = f"**{verdict}**"
            if dup:
                vcell += f" (also listed in {dup})"
            cell = lambda t: str(t).replace("|", "\\|").replace("\n", " ")
            md.append(f"| {link} | {cell(ref)} | {cell(dl)} | {cell(finding)} | {cell(rel)} | {cell(vcell)} |")
        if context_only.get(num):
            md += ["", "## Context sources (not admitted as medical evidence)", "",
                   "Not PubMed-indexed or not a global-guidance body; listed so the setting can be understood, never cited for effect or prevalence.", "",
                   "| ID | Description | Verifier note |", "|---|---|---|"]
            for k, c, n in context_only[num]:
                md.append(f"| {k} | {str(c).replace('|','\\|')} | {str(n).replace('|','\\|')} |")
        if not_admitted.get(num):
            md += ["", "## Not admitted", "", "| ID | Reason |", "|---|---|"]
            for k, n in not_admitted[num]:
                md.append(f"| {k} | {str(n).replace('|','\\|')} |")
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write("\n".join(md) + "\n")
    index += ["", f"Unique PubMed records admitted across categories: **{len(seen)}**.", "",
              "## How an entry gets in", "",
              "1. A search pass records the PMID, reads the abstract, and writes the finding and a relevance annotation.",
              "2. An independent verifier re-fetches every PMID and checks title, year, numbers and whether the annotation overstates the abstract.",
              "3. KEEP and FIX entries are published; FIX entries show the correction; DROP entries are listed as not admitted.",
              "4. The raw search and verification files are kept in `library/data/` so any entry can be audited.",
              "5. Verification used NCBI E-utilities only (no web fetch). WHO, USPSTF, NICE and Cochrane items that are not PubMed-indexed were checked by title or identifier search, not against the live document; their rows say so.",
              "6. The *Finding* and *Relevance annotation* text is AI-drafted from abstracts and verifier-checked; it is not the authors' wording and not a substitute for reading the paper.", "",
              "## Reading rule", "",
              "Nothing in this library is evidence that T-PHE is effective. Entries position the proposal; the abstract remains the claim ceiling."]
    # ---- unified JSON (one schema for every admitted entry) ----
    unified = {"built_from": "library/data/", "scope": "PubMed-indexed literature and global guidance; context sources separated",
               "not_a_systematic_review": True, "categories": [], "entries": [], "context_sources": [], "not_admitted": []}
    kg_nodes, kg_edges = OrderedDict(), []
    def node(nid, ntype, label, **attrs):
        if nid not in kg_nodes:
            kg_nodes[nid] = {"id": nid, "type": ntype, "label": label, **attrs}
    for p in range(1, 8):
        node(f"P{p}", "proposition", PROPOSITIONS[p-1])
    for sg in SAFEGUARDS:
        node("SG:" + sg, "safeguard", sg)
    for od in OUTCOME_DOMAINS:
        node("OD:" + od, "outcome_domain", od)
    for num, (title, scope, angle, rows, q, lim, src) in sorted(per_cat.items()):
        unified["categories"].append({"number": num, "title": title, "scope": scope, "angle": angle, "admitted": len(rows)})
        node("CAT:" + num, "category", title)
        for rec, vr, dup in rows:
            key = str(ident(rec)); pm = norm_pmid((vr or {}).get("pmid") or key)
            rid = f"PMID:{pm}" if pm else f"REF:{key}"
            e = {"id": rid, "pmid": pm, "identifier": key, "category": num,
                 "first_author": (vr or {}).get("first_author") or rec.get("first_author", ""),
                 "title": (vr or {}).get("resolved_title") or rec.get("title", ""),
                 "year": (vr or {}).get("year") or rec.get("year", ""),
                 "journal": (vr or {}).get("journal") or rec.get("journal", ""),
                 "design": rec.get("design", ""), "evidence_level": rec.get("evidence_level", ""),
                 "population_setting": rec.get("population_setting", ""),
                 "finding": (f"[CORRECTION: {(vr or {}).get('note','')}] " if (vr or {}).get("verdict") == "FIX" and (vr or {}).get("note") else "") + (rec.get("key_finding") or rec.get("claim", "")),
                 "relevance_annotation": (("[read with the correction above] ") if (vr or {}).get("verdict") == "FIX" and (vr or {}).get("note") else "") + rec.get("relevance_to_tphe", ""),
                 "verifier_verdict": (vr or {}).get("verdict", ""), "verifier_note": (vr or {}).get("note", ""),
                 "also_in_category": dup, "abstract_read": rec.get("abstract_read", None)}
            unified["entries"].append(e)
            node(rid, "record", f"{e['first_author']} {e['year']}".strip(), year=e["year"], category=num)
            kg_edges.append({"source": rid, "target": "CAT:" + num, "relation": "in_category"})
            ann = (e["relevance_annotation"] or "").lower()
            def has(word):
                # negation-aware cue: ignore "rather than contradicting", "not contradict", "does not support", "no support"
                return bool(re.search(r"\b" + word, ann)) and not re.search(r"(rather than|not|does not|no|without)\s+(\w+\s+)?" + word, ann)
            stance = "contradicts" if has("contradict") else ("complicates" if has("complicat") else ("supports" if has("support") else "relates_to"))
            for p in sorted(set(re.findall(r"\bp([1-7])\b", ann))):
                kg_edges.append({"source": rid, "target": f"P{p}", "relation": stance})
            for sg in SAFEGUARDS:
                if sg.lower() in ann:
                    kg_edges.append({"source": rid, "target": "SG:" + sg, "relation": "informs"})
            for od in OUTCOME_DOMAINS:
                txt = ann + " " + (e["finding"] or "").lower()
                # negation-aware: skip if a negation appears within 80 characters before the term
                hit = False
                for m in re.finditer(re.escape(od.lower()), txt):
                    window = txt[max(0, m.start() - 80):m.start()]
                    if not re.search(r"\b(not|no|never|rather than|does not|is not|are not|neither)\b", window):
                        hit = True; break
                if hit:
                    kg_edges.append({"source": rid, "target": "OD:" + od, "relation": "measures_or_discusses"})
    for num, items in context_only.items():
        for k, c, n in items:
            unified["context_sources"].append({"identifier": k, "category": num, "description": c, "verifier_note": n})
    for num, items in not_admitted.items():
        for k, n in items:
            unified["not_admitted"].append({"identifier": k, "category": num, "reason": n})
    os.makedirs(os.path.join(OUT, "kg"), exist_ok=True)
    json.dump(unified, open(os.path.join(OUT, "library.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump({"nodes": list(kg_nodes.values()), "edges": kg_edges}, open(os.path.join(OUT, "kg", "graph.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # Mermaid overview: category -> proposition edges weighted by record count
    from collections import Counter
    cnt = Counter()
    for ed in kg_edges:
        if ed["target"].startswith("P") and ed["target"][1:].isdigit():
            cat = kg_nodes[ed["source"]].get("category")
            cnt[(cat, ed["target"], ed["relation"])] += 1
    mm = ["```mermaid", "graph LR"]
    for num, (title, *_r) in sorted(per_cat.items()):
        mm.append(f'  C{num}["{num} {title}"]')
    for p in range(1, 8):
        mm.append(f'  P{p}["P{p}: {PROPOSITIONS[p-1]}"]')
    for (cat, tgt, rel), n in sorted(cnt.items()):
        style = "-->" if rel == "supports" else ("-.->" if rel in ("complicates", "contradicts") else "---")
        mm.append(f"  C{cat} {style}|{rel} x{n}| {tgt}")
    mm.append("```")
    open(os.path.join(OUT, "kg", "overview.md"), "w", encoding="utf-8").write(
        "# Knowledge graph — overview\n\nCategory-to-proposition edges aggregated from per-record annotations in `graph.json` "
        "(solid = supports, dashed = complicates/contradicts, plain = relates). Edge labels give the record count. "
        "Annotations are AI-drafted and verifier-checked readings of abstracts, not the authors' own claims.\n\n" + "\n".join(mm) + "\n")
    index += ["", "## Machine-readable", "", "- `library.json` — every admitted entry in one schema, plus context sources and not-admitted identifiers.",
              "- `kg/graph.json` — knowledge graph: nodes (records, categories, propositions P1–P7, safeguards, outcome domains) and edges (in_category; supports / complicates / contradicts / relates_to a proposition; informs a safeguard; measures_or_discusses an outcome domain).",
              "- `kg/overview.md` — Mermaid overview of category → proposition edges."]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    print("categories:", len(per_cat), "unique PMIDs:", len(seen), {k: v for k, v in totals.items()}, "kg nodes", len(kg_nodes), "edges", len(kg_edges))


if __name__ == "__main__":
    main()
