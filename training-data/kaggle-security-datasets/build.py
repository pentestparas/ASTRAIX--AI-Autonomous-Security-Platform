"""Convert Kaggle security datasets into KB markdown docs + SFT training rows.

Batch 1 (commit c23535c — already ingested):
  1. tannubarot/cybersecurity-attack-and-defence-dataset  -> 14,180 attack rows
  2. chuneeb/ai-agent-cybersecurity-dataset-2026          -> 147 AI-agent threats + 21 aux CSVs
  3. hussainsheikh03/nlp-based-cyber-security-dataset     -> NLP threat/defense rows

Batch 2 (this script — 20+ datasets, see KAGGLE_DATASETS.md):
  A. CVE / exploit            (6 datasets)
  B. Network intrusion / malware (8 datasets)
  C. Phishing / URL / email   (4 datasets)
  D. Threat intel / SIEM / logs (3 datasets)
  E. AI / LLM security        (3 datasets)

Outputs:
  knowledge-base/sources/kaggle-security-datasets/*.md     (KB docs)
  training-data/kaggle-security-datasets/security_knowledge_sft.jsonl
  training-data/kaggle-security-datasets/security_knowledge_sft_batch2.jsonl

Usage:
  python3 build.py                # everything
  python3 build.py --dry-run      # only print what would be produced
  python3 build.py --dataset slug # only one dataset (e.g. --dataset mrwells/cicids2017)
"""
import argparse
import csv
import json
import os
import re
from pathlib import Path

CACHE = Path.home() / ".cache" / "kagglehub" / "datasets"
KB_OUT = Path("knowledge-base/sources/kaggle-security-datasets")
TRAIN_OUT = Path("training-data/kaggle-security-datasets")

# --------------------------------------------------------------------------- helpers

def read_csv(path: Path, max_rows: int | None = None):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        rows = []
        for i, r in enumerate(reader):
            if max_rows and i >= max_rows:
                break
            rows.append(r)
        return rows


def read_jsonl(path: Path, max_rows: int | None = None):
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if max_rows and i >= max_rows:
                break
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def slugify(s: str) -> str:
    s = s.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    return s


def write_kb_doc(name: str, content: str, dry_run: bool = False):
    path = KB_OUT / f"{name}.md"
    if dry_run:
        print(f"  [dry] KB doc: {path.name} ({len(content)} chars)")
        return
    path.write_text(content, encoding="utf-8")


def write_sft(rows: list[dict], name: str, dry_run: bool = False):
    path = TRAIN_OUT / name
    if dry_run:
        print(f"  [dry] SFT: {path.name} ({len(rows)} rows)")
        return
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ dataset handlers
# Each handler receives the local cache path (post-kagglehub-download) and returns
# (kb_docs: list[(name, content)], sft_rows: list[dict]).

def handle_cve_generic(cache_path: Path, name: str, title: str, dry_run: bool):
    """Generic CVE CSV → per-CWE KB docs + SFT rows."""
    sft = []
    cwe_groups = {}
    for p in sorted(cache_path.rglob("*.csv")):
        rows = read_csv(p, max_rows=100_000)
        print(f"  {p.name}: {len(rows)} rows")
        for r in rows:
            cwe = (r.get("CWE") or r.get("Weakness") or r.get("CWE_ID") or "General").strip() or "General"
            cwe_groups.setdefault(cwe, []).append(r)
    for cwe, items in sorted(cwe_groups.items()):
        slug = slugify(cwe)
        content = [f"# {cwe} — CVE References ({title})", ""]
        for r in items:
            content.append(f"## {r.get('CVE_ID') or r.get('CVE ID') or r.get('CVE') or 'CVE'}\n")
            content.append(f"- **Description**: {r.get('Description') or r.get('description') or ''}\n")
            content.append(f"- **CWE**: {r.get('CWE') or r.get('Weakness') or ''}\n")
            content.append(f"- **CVSS**: {r.get('CVSS Score') or r.get('cvss') or r.get('base_score') or ''}\n")
            content.append(f"- **Severity**: {r.get('Severity') or r.get('severity') or ''}\n")
            content.append(f"- **Affected**: {r.get('Affected Product') or r.get('affected_product') or ''}\n")
            content.append(f"- **References**: {r.get('References') or r.get('reference') or ''}\n\n")
            sft.append({
                "instruction": f"What is CVE {r.get('CVE_ID') or r.get('CVE') or ''}?",
                "output": (
                    f"{r.get('Description') or r.get('description') or 'No description'}\n"
                    f"CWE: {r.get('CWE') or r.get('Weakness') or 'N/A'}\n"
                    f"CVSS: {r.get('CVSS Score') or r.get('cvss') or 'N/A'}\n"
                    f"Severity: {r.get('Severity') or r.get('severity') or 'N/A'}"
                ),
            })
        write_kb_doc(f"cve-{name}-{slug}", "\n".join(content), dry_run)
    print(f"  -> {len(sft)} SFT rows")
    return sft


def handle_ids_generic(cache_path: Path, name: str, title: str, dry_run: bool):
    """Network intrusion detection CSV → per-class KB docs + SFT rows."""
    sft = []
    for p in sorted(cache_path.rglob("*.csv")):
        rows = read_csv(p, max_rows=50_000)
        print(f"  {p.name}: {len(rows)} rows")
        if not rows:
            continue
        # find the label column
        label_col = None
        for cand in ("Label", "label", "Class", "class", "Attack Type", "Attack", "Category"):
            if cand in rows[0]:
                label_col = cand
                break
        if not label_col:
            continue
        groups = {}
        for r in rows:
            lab = (r.get(label_col) or "Benign").strip()
            groups.setdefault(lab, []).append(r)
        content = [f"# {title} — Intrusion Detection by Class", ""]
        for lab, items in sorted(groups.items()):
            slug = slugify(lab)
            content.append(f"## {lab} ({len(items)} samples)\n")
            # summarize features rather than dumping all rows
            feats = {}
            for r in items[:200]:
                for k, v in r.items():
                    if k != label_col and v not in (None, "", "0", "0.0"):
                        feats.setdefault(k, set()).add(str(v)[:40])
            for k, vals in sorted(feats.items()):
                content.append(f"- **{k}**: {', '.join(sorted(vals)[:6])}\n")
            content.append("\n")
            sft.append({
                "instruction": f"Describe the network attack class '{lab}' from {title}",
                "output": (
                    f"Class: {lab}\n"
                    f"Sample features: {', '.join(sorted(feats)[:8])}\n"
                    f"Distinct values: {len(feats)} features observed in {len(items)} samples"
                ),
            })
        write_kb_doc(f"ids-{name}-{slugify(title)}", "\n".join(content), dry_run)
    print(f"  -> {len(sft)} SFT rows")
    return sft


def handle_phish_generic(cache_path: Path, name: str, title: str, dry_run: bool):
    """Phishing/URL/email CSV → KB docs + SFT rows."""
    sft = []
    for p in sorted(cache_path.rglob("*.csv")):
        rows = read_csv(p, max_rows=30_000)
        print(f"  {p.name}: {len(rows)} rows")
        if not rows:
            continue
        label_col = None
        for cand in ("Label", "label", "Phishing", "Result", "class", "Type", "is_phishing"):
            if cand in rows[0]:
                label_col = cand
                break
        groups = {}
        for r in rows:
            lab = (r.get(label_col) or "unknown").strip()
            groups.setdefault(lab, []).append(r)
        content = [f"# {title} — Phishing Detection", ""]
        for lab, items in sorted(groups.items()):
            content.append(f"## {lab} ({len(items)} samples)\n")
            for r in items[:50]:
                content.append(f"- **URL/Email**: {r.get('URL') or r.get('url') or r.get('Email') or r.get('email') or ''}\n")
                content.append(f"  - {', '.join(f'{k}: {v}' for k, v in r.items() if k not in ('URL','url','Email','email',label_col) and v)}\n")
            content.append("\n")
            sft.append({
                "instruction": f"How do I identify a phishing {lab} sample?",
                "output": "\n".join(
                    f"{k}: {v}" for k, v in (items[0].items() if items else []) if k != label_col and v
                )[:2000],
            })
        write_kb_doc(f"phish-{name}-{slugify(title)}", "\n".join(content), dry_run)
    print(f"  -> {len(sft)} SFT rows")
    return sft


def handle_siem_generic(cache_path: Path, name: str, title: str, dry_run: bool):
    """SIEM / log CSV → KB docs + SFT rows."""
    sft = []
    for p in sorted(cache_path.rglob("*.csv")):
        rows = read_csv(p, max_rows=50_000)
        print(f"  {p.name}: {len(rows)} rows")
        if not rows:
            continue
        content = [f"# {title} — SIEM Log Data", ""]
        for r in rows[:2000]:
            content.append(f"- {' | '.join(f'{k}: {v}' for k, v in r.items() if v)}\n")
        write_kb_doc(f"siem-{name}-{slugify(title)}", "\n".join(content), dry_run)
        for r in rows[:200]:
            sft.append({
                "instruction": f"Parse this {title} log entry",
                "output": "\n".join(f"{k}: {v}" for k, v in r.items() if v)[:2000],
            })
    print(f"  -> {len(sft)} SFT rows")
    return sft


def handle_ai_generic(cache_path: Path, name: str, title: str, dry_run: bool):
    """AI/LLM security CSV/JSONL → KB docs + SFT rows."""
    sft = []
    for p in sorted(cache_path.rglob("*.csv")) + sorted(cache_path.rglob("*.jsonl")):
        rows = read_csv(p, max_rows=30_000) if p.suffix == ".csv" else read_jsonl(p, max_rows=30_000)
        print(f"  {p.name}: {len(rows)} rows")
        if not rows:
            continue
        content = [f"# {title} — AI/LLM Security", ""]
        for r in rows[:1000]:
            desc = r.get("prompt") or r.get("instruction") or r.get("text") or r.get("description") or ""
            if desc:
                content.append(f"- **Prompt**: {desc[:500]}\n")
        write_kb_doc(f"ai-{name}-{slugify(title)}", "\n".join(content), dry_run)
        for r in rows[:500]:
            sft.append({
                "instruction": "What does this AI/LLM security sample demonstrate?",
                "output": (r.get("output") or r.get("response") or r.get("category") or "")[:2000],
            })
    print(f"  -> {len(sft)} SFT rows")
    return sft


# ------------------------------------------------------------------- dataset registry
# slug -> (handler, name, title)
DATASETS: dict[str, tuple] = {
    # A. CVE / exploit
    "sujaykapadnis/cybersecurity-cve-dataset": (handle_cve_generic, "cysec-cve", "Cybersecurity CVE Dataset"),
    "asad7an/cve-mitre-attack-mapping": (handle_cve_generic, "mitre-cve", "CVE MITRE ATT&CK Mapping"),
    "aymane200/cve-vulnerabilities-dataset-2014-2024": (handle_cve_generic, "cve-2014-2024", "CVE Vulnerabilities 2014-2024"),
    "ravikumarmn/cve-dataset-2002-2024": (handle_cve_generic, "cve-2002-2024", "CVE Dataset 2002-2024"),
    "manavyadav25/cve-vulnerability-records": (handle_cve_generic, "cve-records", "CVE Vulnerability Records"),
    "davidcampos/cve-database": (handle_cve_generic, "cve-db", "CVE Database"),
    # B. Network intrusion / malware
    "sampadab17/network-intrusion-detection": (handle_ids_generic, "ids-sampadab", "Network Intrusion Detection"),
    "chethuhn/network-intrusion-detection": (handle_ids_generic, "ids-chethuhn", "Network Intrusion Detection UNSW"),
    "mrwells/cicids2017": (handle_ids_generic, "ids-cicids2017", "CICIDS2017"),
    "mnassrib/cicids2017": (handle_ids_generic, "ids-cicids2017-alt", "CICIDS2017 Alternate"),
    "ahmedhamdy0/network-intrusion-dataset": (handle_ids_generic, "ids-ahmedhamdy", "Network Intrusion Dataset"),
    "rohitgupta24/network-malware-detection": (handle_ids_generic, "malware-rohit", "Network Malware Detection"),
    "sgk1590/malware-detection": (handle_ids_generic, "malware-sgk", "Malware Detection"),
    "danielcompetition/cybersecurity-attacks": (handle_ids_generic, "attacks-daniel", "Cybersecurity Attacks"),
    # C. Phishing
    "shantanudhakadd/email-spam-dataset": (handle_phish_generic, "spam-shantanu", "Email Spam Dataset"),
    "akashkr/phishing-url-detection": (handle_phish_generic, "phish-akashkr", "Phishing URL Detection"),
    "eswarchandt/phishing-website-detector": (handle_phish_generic, "phish-eswarchandt", "Phishing Website Detector"),
    "naserabdullah079/phishing-email-detection": (handle_phish_generic, "phish-naser", "Phishing Email Detection"),
    # D. SIEM / logs
    "casperribrib/siem-data": (handle_siem_generic, "siem-casper", "SIEM Data"),
    "mkalimer/loghub-windows-event-log": (handle_siem_generic, "windows-events", "LogHub Windows Event Log"),
    "mvonsteinkirch/loghub-zeek-http-logs": (handle_siem_generic, "zeek-http", "LogHub Zeek HTTP Logs"),
    # E. AI / LLM
    "deepakcode21/llm-jailbreak-prompts": (handle_ai_generic, "jailbreak", "LLM Jailbreak Prompts"),
    "deepakcode21/prompt-injection-attacks": (handle_ai_generic, "prompt-injection", "Prompt Injection Attacks"),
    "noahsiegel/prompt-injection-dataset": (handle_ai_generic, "prompt-injection-2", "Prompt Injection Dataset"),
}


def find_dataset_dir(slug: str) -> Path | None:
    owner, name = slug.split("/", 1)
    base = CACHE / owner / name
    if not base.exists():
        return None
    versions = sorted(base.glob("versions/*"))
    return versions[-1] if versions else base


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print what would be produced")
    parser.add_argument("--dataset", type=str, help="only process one dataset slug (e.g. mrwells/cicids2017)")
    args = parser.parse_args()

    KB_OUT.mkdir(parents=True, exist_ok=True)
    TRAIN_OUT.mkdir(parents=True, exist_ok=True)

    selected = {slug: meta for slug, meta in DATASETS.items()
                if not args.dataset or slug.endswith(args.dataset)}

    all_sft = []
    for slug, (handler, name, title) in sorted(selected.items()):
        d = find_dataset_dir(slug)
        if not d:
            print(f"\n### {slug} — NOT DOWNLOADED (skipping; run download.sh first)")
            continue
        print(f"\n### {slug} — {title}")
        try:
            sft = handler(d, name, title, args.dry_run)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        all_sft.extend(sft)

    # merge into batch-2 SFT file (never clobbers batch 1)
    if all_sft:
        write_sft(all_sft, "security_knowledge_sft_batch2.jsonl", args.dry_run)
        print(f"\nTotal new SFT rows: {len(all_sft)}")
    else:
        print("\nNo SFT rows produced.")


if __name__ == "__main__":
    main()
