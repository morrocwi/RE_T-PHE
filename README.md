# RE_T-PHE — Research programme: Trustworthy Premarital Health Education

[![verify](https://github.com/morrocwi/RE_T-PHE/actions/workflows/verify.yml/badge.svg)](https://github.com/morrocwi/RE_T-PHE/actions/workflows/verify.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey.svg)](LICENSE)

> **AI or human reader arriving from a QR code?** Start at [`AI_START_HERE.md`](AI_START_HERE.md) (ten-minute reading order, how to verify this repository, what not to conclude). Machine-readable index: [`llms.txt`](llms.txt).

Public research record for **Trustworthy Premarital Health Education (T-PHE)**, a proposed
primary-prevention intervention for intimate-partner harm, positioned at the transition into
marriage. The programme theory is set out in a conference abstract accepted for presentation at
the TIMA/FIMA Scientific Convention 2026.

| | |
|---|---|
| **Field** | Public health · preventive medicine · health promotion · safeguarding |
| **Study type** | Practitioner-led, document-informed conceptual synthesis (programme theory). **No effectiveness testing has been undertaken.** |
| **Author** | Yaoharee Lahtee (ARAYA Nikah Social Enterprise Co., Ltd., Bangkok; Independent Researcher, Thailand) |
| **Document of record** | [`abstract/TIMA-FIMA_2026_Abstract_FINAL_Yaoharee_Lahtee.pdf`](abstract/TIMA-FIMA_2026_Abstract_FINAL_Yaoharee_Lahtee.pdf) (camera-ready, SHA-256 in [`abstract/SHA256SUMS`](abstract/SHA256SUMS)) |
| **Web copy** | [`abstract/ABSTRACT.md`](abstract/ABSTRACT.md) |
| **Evidence ledger** | [`CLAIMS.md`](CLAIMS.md) — every statement in the abstract graded by the type of evidence behind it |
| **Evidence library** | [`library/README.md`](library/README.md) — verified PubMed and global-guidance records in twelve categories, with a unified JSON and a knowledge graph; context sources separated; not a systematic review |
| **Setting** | [`ABOUT_ARAYA_NIKAH.md`](ABOUT_ARAYA_NIKAH.md) — background on the originating organisation, each statement labelled by source status; context for readers, not part of the paper |
| **Side data** | [`docs/side-data/family-of-peace-theory-of-change.md`](docs/side-data/family-of-peace-theory-of-change.md) — the organisation's theory of change in logic-model form; T-PHE does not adopt it |
| **License** | [CC BY 4.0](LICENSE) |

## What the abstract claims, in one paragraph

Whether a family becomes a place of physical, psychological and economic safety is shaped at the
transition into marriage. T-PHE is proposed as infrastructure for primary prevention whose single
mechanism is to increase each participant's control over whether to proceed with, delay or refuse
marriage, and over when and how to seek help. Six safeguards protect that choice. The intervention
has an explicit failure criterion: it fails if it raises knowledge scores, attendance, satisfaction
or marriage completion while leaving informed choice, recognition of coercion, reproductive and
mental-health literacy, safe help-seeking and accountable referral unchanged. Where violence, fear
or coercive control is suspected or disclosed, joint work stops pending confidential assessment and
does not resume where coercive control is confirmed.

## What this repository does not claim

- **No effectiveness evidence.** The abstract is a conceptual synthesis and programme theory. It
  reports no outcome data, no comparison group, and no effect estimate.
- **No participant data.** Nothing in this repository is derived from, or contains, individual
  participant records. The participant count quoted in the abstract is an organisational figure,
  not a dataset held here (see [`CLAIMS.md`](CLAIMS.md), C-06).
- **No clinical guidance.** This is not advice for any individual, couple, clinician or educator.
  Suspected or disclosed violence or coercive control requires qualified, survivor-centred services.

## How this repository is governed

Every change to a public-facing file passes an **independent critical appraisal** before it is
merged. The author of a change is never its sole reviewer. The rule, the review checklist and the
language standard are in [`AGENTS.md`](AGENTS.md); each completed appraisal is filed under
[`docs/reports/`](docs/reports/).

The language of this repository is the language of medical and public-health science
(intervention, programme theory, outcome domain, level of evidence, safeguarding, referral).
Internal working vocabulary from other projects is not used here.

## Reproducing the integrity check

```bash
sudo apt-get install -y poppler-utils   # provides pdftotext
bash tools/verify.sh
```

The script confirms that the PDF matches its recorded SHA-256 and that the web copy of the
abstract matches the text extracted from the PDF (telephone line excepted).

## Citation

See [`CITATION.cff`](CITATION.cff). Suggested form:

> Lahtee, Y. (2026). *Before Family Risk Becomes a Health Crisis: Trustworthy Premarital Health
> Education as Primary Prevention Infrastructure.* Abstract, TIMA/FIMA Scientific Convention 2026.
> https://github.com/morrocwi/RE_T-PHE

## Repository layout

```
AI_START_HERE.md  entry point for readers who scanned the QR code (human or AI)
llms.txt        machine-readable index of this repository
abstract/       camera-ready PDF (document of record), SHA256SUMS, web copy
CLAIMS.md       evidence ledger for every statement in the abstract
ABOUT_ARAYA_NIKAH.md  organisational setting, source-status labelled (context, not evidence)
library/        evidence library by category (verified records, library.json, kg/graph.json); tools/build_library.py rebuilds it
docs/side-data/  the organisation's own theory of change, logic-model form (side data; not adopted by the paper)
AGENTS.md       rules for any human or AI contributor (review gate, language standard)
GOAL.md         what this research programme is trying to achieve, and how it will know
logbook.jsonl   append-only record of what was actually done
docs/reports/   dated critical-appraisal reports
tools/          integrity check
private/        git-ignored working area (data, strategy, drafts) — never published
```
