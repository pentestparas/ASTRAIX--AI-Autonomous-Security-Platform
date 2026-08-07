#!/usr/bin/env bash
# Download all 22 Kaggle datasets in the curated batch using kagglehub.
#
# Prerequisites:
#   1. pip install kagglehub
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

# --- existing 3 datasets (already in cache) -----------------------------------
EXISTING=(
  "tannubarot/cybersecurity-attack-and-defence-dataset"
  "chuneeb/ai-agent-cybersecurity-dataset-2026"
  "hussainsheikh03/nlp-based-cyber-security-dataset"
)

# --- new batch (22 datasets) -------------------------------------------------
# Format: "<slug>|<theme>" where theme ∈ {cve, ids, malware, phish, siem, ai}
declare -a BATCH=(
  # A. CVE / exploit
  "sujaykapadnis/cybersecurity-cve-dataset|cve"
  "asad7an/cve-mitre-attack-mapping|cve"
  "aymane200/cve-vulnerabilities-dataset-2014-2024|cve"
  "ravikumarmn/cve-dataset-2002-2024|cve"
  "manavyadav25/cve-vulnerability-records|cve"
  "davidcampos/cve-database|cve"

  # B. Intrusion / malware
  "sampadab17/network-intrusion-detection|ids"
  "chethuhn/network-intrusion-detection|ids"
  "mrwells/cicids2017|ids"
  "mnassrib/cicids2017|ids"
  "ahmedhamdy0/network-intrusion-dataset|ids"
  "rohitgupta24/network-malware-detection|malware"
  "sgk1590/malware-detection|malware"
  "danielcompetition/cybersecurity-attacks|ids"

  # C. Phishing / URL / email
  "shantanudhakadd/email-spam-dataset|phish"
  "akashkr/phishing-url-detection|phish"
  "eswarchandt/phishing-website-detector|phish"
  "naserabdullah079/phishing-email-detection|phish"

  # D. Threat intel / SIEM / logs
  "casperribrib/siem-data|siem"
  "mkalimer/loghub-windows-event-log|siem"
  "mvonsteinkirch/loghub-zeek-http-logs|siem"

  # E. AI / LLM security
  "deepakcode21/llm-jailbreak-prompts|ai"
  "deepakcode21/prompt-injection-attacks|ai"
  "noahsiegel/prompt-injection-dataset|ai"
)

FILTER="${1:-}"  # optional substring filter on theme

echo "==> Verifying prerequisites"
if ! command -v kagglehub >/dev/null 2>&1; then
  if ! python3 -c "import kagglehub" 2>/dev/null; then
    echo "ERROR: kagglehub not installed. Run: pip install kagglehub" >&2
    exit 1
  fi
fi

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
  if kagglehub dataset_download "$slug" --force 2>&1 | tail -3; then
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
