"""Convert Kaggle security datasets into KB markdown docs + SFT training rows.

Datasets (downloaded via kagglehub into ~/.cache/kagglehub):
  1. tannubarot/cybersecurity-attack-and-defence-dataset  -> 14,180 attack rows
  2. chuneeb/ai-agent-cybersecurity-dataset-2026          -> 147 AI-agent threats + 21 aux CSVs
  3. hussainsheikh03/nlp-based-cyber-security-dataset     -> NLP threat/defense rows

Outputs:
  knowledge-base/sources/kaggle-security-datasets/*.md     (KB docs)
  training-data/kaggle-security-datasets/security_knowledge_sft.jsonl
"""
import csv
import json
import os
from pathlib import Path

CACHE = Path.home() / ".cache" / "kagglehub" / "datasets"
KB_OUT = Path("knowledge-base/sources/kaggle-security-datasets")
TRAIN_OUT = Path("training-data/kaggle-security-datasets")

ATTACK_CSV = CACHE / "tannubarot/cybersecurity-attack-and-defence-dataset/versions/2/Attack_Dataset.csv"
AGENT_DIR = CACHE / "chuneeb/ai-agent-cybersecurity-dataset-2026/versions/1/data"
NLP_CSV = CACHE / "hussainsheikh03/nlp-based-cyber-security-dataset/versions/1/Cybersecurity_Dataset.csv"


def read_csv(path: Path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))


def main():
    KB_OUT.mkdir(parents=True, exist_ok=True)
    TRAIN_OUT.mkdir(parents=True, exist_ok=True)
    sft = []

    # ------------------------------------------------------------- attacks
    rows = read_csv(ATTACK_CSV)
    print(f"attack rows: {len(rows)}")
    by_cat = {}
    for r in rows:
        cat = (r.get("Category") or "General").strip() or "General"
        by_cat.setdefault(cat, []).append(r)

    for cat, items in sorted(by_cat.items()):
        slug = cat.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
        with open(KB_OUT / f"attacks-{slug}.md", "w") as f:
            f.write(f"# {cat} Attacks\n\n")
            for r in items:
                f.write(f"## {r.get('Title','')}\n\n")
                f.write(f"- **Attack Type**: {r.get('Attack Type','')}\n")
                f.write(f"- **Target**: {r.get('Target Type','')}\n")
                f.write(f"- **Vulnerability**: {r.get('Vulnerability','')}\n")
                f.write(f"- **MITRE**: {r.get('MITRE Technique','')}\n")
                f.write(f"- **Impact**: {r.get('Impact','')}\n")
                f.write(f"- **Tools**: {r.get('Tools Used','')}\n")
                f.write(f"- **Scenario**: {r.get('Scenario Description','')}\n")
                f.write(f"- **Attack Steps**: {r.get('Attack Steps ','').strip() or r.get('Attack Steps','')}\n")
                f.write(f"- **Detection**: {r.get('Detection Method','')}\n")
                f.write(f"- **Solution**: {r.get('Solution','')}\n")
                f.write(f"- **Tags**: {r.get('Tags','')}\n\n")
                sft.append({
                    "instruction": f"Describe the {r.get('Attack Type','cybersecurity')} attack: {r.get('Title','')}",
                    "output": (
                        f"{r.get('Scenario Description','')}\n"
                        f"Vulnerability: {r.get('Vulnerability','')}\n"
                        f"Impact: {r.get('Impact','')}\n"
                        f"Detection: {r.get('Detection Method','')}\n"
                        f"Remediation: {r.get('Solution','')}"
                    ),
                })

    # ---------------------------------------------------------- AI agents
    agent_master = AGENT_DIR / "master_ai_agent_cybersecurity.csv"
    if agent_master.exists():
        arows = read_csv(agent_master)
        print(f"ai-agent rows: {len(arows)}")
        with open(KB_OUT / "ai-agent-security.md", "w") as f:
            f.write("# AI Agent Cybersecurity Threats (Kaggle AI-Agent 2026)\n\n")
            for r in arows:
                f.write(f"## {r.get('attack_name','')} ({r.get('category','')})\n\n")
                f.write(f"- **Subcategory**: {r.get('subcategory','')}\n")
                f.write(f"- **Severity**: {r.get('severity','')}\n")
                f.write(f"- **Source**: {r.get('source','')} ({r.get('year','')})\n")
                f.write(f"- **Description**: {r.get('description','')}\n\n")
                sft.append({
                    "instruction": f"Describe the AI agent security threat: {r.get('attack_name','')}",
                    "output": f"{r.get('description','')} (severity {r.get('severity','')}, {r.get('source','')})",
                })
        # aux CSVs -> compact docs
        for p in sorted(AGENT_DIR.glob("**/*.csv")):
            if p.name == "master_ai_agent_cybersecurity.csv":
                continue
            try:
                r2 = read_csv(p)
            except Exception:
                continue
            if not r2:
                continue
            with open(KB_OUT / f"ai-agent-{p.stem}.md", "w") as f:
                f.write(f"# AI Agent Cybersecurity - {p.stem}\n\n")
                for row in r2[:500]:
                    vals = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
                    f.write(f"- {vals}\n")
            print(f"  aux: {p.name} -> {len(r2)} rows")

    # --------------------------------------------------------------- NLP
    if NLP_CSV.exists():
        nrows = read_csv(NLP_CSV)
        print(f"nlp rows: {len(nrows)}")
        with open(KB_OUT / "nlp-threat-intel.md", "w") as f:
            f.write("# NLP-Based Threat Intelligence (Kaggle)\n\n")
            for r in nrows:
                f.write(f"## {r.get('Threat Category','')}\n\n")
                f.write(f"- **Threat Actor**: {r.get('Threat Actor','')}\n")
                f.write(f"- **Attack Vector**: {r.get('Attack Vector','')}\n")
                f.write(f"- **IOCs**: {r.get('IOCs (Indicators of Compromise)','')}\n")
                f.write(f"- **Severity**: {r.get('Severity Score','')}\n")
                f.write(f"- **Risk Level**: {r.get('Risk Level Prediction','')}\n")
                f.write(f"- **Defense**: {r.get('Suggested Defense Mechanism','')}\n")
                f.write(f"- **Description**: {r.get('Cleaned Threat Description','')}\n\n")

    # ------------------------------------------------------------- output
    with open(TRAIN_OUT / "security_knowledge_sft.jsonl", "w") as f:
        for row in sft:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(sft)} SFT rows -> {TRAIN_OUT / 'security_knowledge_sft.jsonl'}")
    print(f"KB docs -> {KB_OUT}")


if __name__ == "__main__":
    main()
