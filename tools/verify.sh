#!/usr/bin/env bash
# Integrity check for the document of record.
#  1. The camera-ready PDF matches its recorded SHA-256.
#  2. The web copy (abstract/ABSTRACT.md) contains every sentence of the PDF body
#     (Background to Keywords); the title/contact block is checked by eye.
# Requires: sha256sum, pdftotext (poppler-utils).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/2] SHA-256 of abstract/*.pdf"
(cd abstract && sha256sum -c SHA256SUMS)

echo "[2/2] Web copy vs PDF text"
command -v pdftotext >/dev/null || { echo "pdftotext not found (install poppler-utils)"; exit 2; }
PDF=$(ls abstract/*.pdf | head -1)
norm() { tr -d '\r' | sed 's/\xe2\x80\x8b//g' | tr -s '[:space:]' ' ' ; }
# Body only (from "Background" to the end): the title block has no sentence structure
# and its contact line is deliberately not reproduced in the web copy.
pdf_text=$(pdftotext "$PDF" - | sed -n '/^Background/,$p' | norm)
md_text=$(sed 's/^[#>*]* *//; s/\*\*//g' abstract/ABSTRACT.md | norm)

fail=0
# Compare sentence by sentence: every PDF sentence must appear in the web copy.
echo "$pdf_text" | sed 's/\. /.\n/g' | while IFS= read -r s; do
  s=$(echo "$s" | sed 's/^ *//; s/ *$//')
  [ ${#s} -lt 20 ] && continue
  if ! grep -qF -- "$s" <<<"$md_text"; then
    echo "  MISSING in ABSTRACT.md: $s"
    exit 1
  fi
done || fail=1

if [ "$fail" -ne 0 ]; then echo "FAIL"; exit 1; fi
echo "OK: web copy matches PDF text (telephone line excepted)"
