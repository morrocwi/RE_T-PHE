#!/usr/bin/env bash
# Integrity check for the document of record.
#  1. The camera-ready PDF matches its recorded SHA-256.
#  2. The body of the web copy (abstract/ABSTRACT.md, from "Background" to the end) is
#     word-for-word IDENTICAL to the body of the PDF text — nothing missing, nothing added.
#     The title/contact block above "Background" is checked by eye; the telephone line is
#     intentionally absent from the web copy.
# Requires: sha256sum, pdftotext (poppler-utils).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/2] SHA-256 of abstract/*.pdf"
(cd abstract && sha256sum -c SHA256SUMS)

echo "[2/2] Web copy body vs PDF body (exact, both directions)"
command -v pdftotext >/dev/null || { echo "pdftotext not found (install poppler-utils)"; exit 2; }
PDF=$(ls abstract/*.pdf | head -1)
# normalise: drop zero-width spaces, collapse all whitespace to single spaces, trim
norm() { tr -d '\r' | sed 's/\xe2\x80\x8b//g' | tr -s '[:space:]' ' ' | sed 's/^ *//; s/ *$//'; }

pdf_body=$(pdftotext "$PDF" - | sed -n '/^Background/,$p' | norm)
md_body=$(sed -n '/^### Background/,$p' abstract/ABSTRACT.md | sed 's/^#* *//; s/\*\*//g' | norm)

if [ "$pdf_body" = "$md_body" ]; then
  echo "OK: web copy body is identical to the PDF body"
  exit 0
fi

echo "FAIL: web copy body differs from PDF body. Word-level diff (< PDF, > web copy):"
diff <(tr ' ' '\n' <<<"$pdf_body") <(tr ' ' '\n' <<<"$md_body") | head -40 || true
exit 1
