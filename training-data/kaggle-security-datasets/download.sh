#!/usr/bin/env bash
# Download all 22 Kaggle datasets in the curated batch using kagglehub.
#
# Prerequisites:
#   1. pip install kagglehub   (or: backend/venv/bin/pip install kagglehub)
#   2. Place your Kaggle API token at ~/.kaggle/kaggle.json
#      (get it from https://www.kaggle.com/settings -> API -> Create New Token)
#   3. chmod 600 ~/.kaggle/kaggle.json
#
# All datasets are downloaded into ~/.cache/kagglehub/datasets/<owner>/<name>/versions/<n>/...
# `build.py` reads from that cache.
#
# Usage:
#   ./download.sh                # download all 22
#   ./download.sh cve phish      # only download datasets whose theme matches (case-insensitive substring)
#
set -euo pipefail

# --- locate a python with kagglehub ------------------------------------------
if command -v kagglehub >/dev/null 2>&1 && kagglehub --help >/dev/null 2>&1; then
  # kagglehub CLI (legacy 0.x)
  download_one() { kagglehub dataset_download "$1" --force; }
else
  PY=""
  for cand in backend/venv/bin/python .venv/bin/python python3; do
    if $cand -c "import kagglehub" >/dev/null 2>&1; then PY="$cand"; break; fi
  done
  if [ -z "$PY" ]; then
    echo "ERROR: kagglehub not installed. Run: pip install kagglehub" >&2
    echo "       (or: backend/venv/bin/pip install kagglehub)" >&2
    exit 1
  fi
  echo "Using python: $PY"
  download_one() { "$PY" -c "import kagglehub, sys; print(kagglehub.dataset_download('$1'))"; }
fi

# --- existing 3 datasets (already in cache) -----------------------------------
EXISTING=(
  "tannubarot/cybersecurity-attack-and-defence-dataset"
  "chuneeb/ai-agent-cybersecurity-dataset-2026"
  "hussainsheikh03/nlp-based-cyber-security-dataset"
)

# --- new batch (22 datasets, ALL verified via GET /api/v1/datasets/view on 2026-08-10) ---
# Format: "<slug>|<theme>" where theme ∈ {cve, ids, malware, phish, siem, ai}
declare -a BATCH=(
  # A. CVE / exploit
  "krooz0/cve-and-cwe-mapping-dataset|cve"
  "andrewkronser/cve-common-vulnerabilities-and-exposures|cve"
  "um3rfar00q/2021-2025-all-cves-cleaned-dataset|cve"
  "stanislavvinokur/cve-and-cwe-dataset-1999-2025|cve"
  "junaidmohammad9248/cisa-cve-vulnrichment|cve"

  # B. Network intrusion
  "dhoogla/unswnb15|ids"
  "dhoogla/nslkdd|ids"
  "dhoogla/cicddos2019|ids"
  "sampadab17/network-intrusion-detection|ids"
  "arnobbhowmik/ton-iot-network-dataset|ids"

  # C. Malware
  "subhajournal/malware-detection-from-memory-dump|malware"
  "luccagodoy/obfuscated-malware-memory-2022-cic|malware"
  "amdj3dax/ransomware-detection-data-set|malware"

  # D. Phishing / URL / email
  "subhajournal/phishingemails|phish"
  "shashwatwork/web-page-phishing-detection-dataset|phish"
  "hasibur013/phishing-data|phish"
  "eswarchandt/phishing-website-detector|phish"

  # E. Threat intel / SIEM / logs
  "rawaldelhi/secureops-security-incident-logs-dataset|siem"
  "jacobvs/ddos-attack-network-logs|siem"
  "solvedinfoam/2022-04-20-emotet-epoch4-zeek-logs|siem"

  # F. AI / LLM security
  "awwdudee/llm-safety-dataset-for-chatbot-applications|ai"
  "krishnayadav456wrsty/prompt-injection-and-jailbreak-detection-dataset|ai"
  "shreyashautomation/llm-jailbreak-prompt-dataset|ai"
  "cyberprince/prompt-injection-and-benign-prompt-dataset|ai"
)

FILTER="${1:-}"  # optional substring filter on theme

if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
  echo "ERROR: ~/.kaggle/kaggle.json not found." >&2
  echo "  1. Go to https://www.kaggle.com/settings -> API -> Create New Token" >&2
  echo "  2. Save as ~/.kaggle/kaggle.json" >&2
  echo "  3. chmod 600 ~/.kaggle/kaggle.json" >&2
  exit 1
fi

mkdir -p "$HOME/.cache/kagglehub/datasets"

run_one() {
  local slug="$1"
  local theme="$2"
  echo "==> [$theme] $slug"
  if download_one "$slug" 2>&1 | tail -3; then
    echo "    OK"
  else
    echo "    FAILED (slug may have been renamed or deleted — verify on kaggle.com)"
    return 0   # do not abort the whole batch on a single failure
  fi
}

echo
echo "==> Skipping existing 3 (already in cache):"
for s in "${EXISTING[@]}"; do echo "    - $s"; done

echo
echo "==> Downloading new batch"
for entry in "${BATCH[@]}"; do
  slug="${entry%%|*}"
  theme="${entry##*|}"
  if [ -z "$FILTER" ] || [[ "${theme}${slug}" == *"$FILTER"* ]]; then
    run_one "$slug" "$theme" || true
  fi
done

echo
echo "==> Cache summary"
ls -1 "$HOME/.cache/kagglehub/datasets/" | wc -l | xargs echo "Total dataset owners in cache:"
du -sh "$HOME/.cache/kagglehub/datasets/" 2>/dev/null

echo
echo "Done. Next step: python3 build.py"
