#!/usr/bin/env python3
"""Convert the Kaggle vulnerable-programming-dataset into:
1. knowledge-base sources (markdown, one doc per language) so the researcher
   agent can ground code-audit findings on vulnerable code patterns.
2. training-data/vulnerable-programming-dataset/ — clean JSON + SFT-style
   instruction JSONL for fine-tuning a code-review LLM.

Usage: python3 training-data/vulnerable-programming-dataset/build.py
"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(
    ROOT, "training-data", "vulnerable-programming-dataset", "dataset.json"
)
KB_OUT = os.path.join(ROOT, "knowledge-base", "sources", "vulnerable-programming-dataset")
TRAIN_OUT = os.path.join(ROOT, "training-data", "vulnerable-programming-dataset")

INSTRUCTION_TMPL = (
    "Analyze the following {language} code for security vulnerabilities."
)


def md_escape(text: str) -> str:
    return text.replace("`", "\\`")


def main() -> None:
    with open(SRC, encoding="utf-8") as f:
        samples = json.load(f)

    os.makedirs(KB_OUT, exist_ok=True)
    os.makedirs(TRAIN_OUT, exist_ok=True)

    by_lang: dict[str, list[dict]] = {}
    for s in samples:
        by_lang.setdefault(s["language"], []).append(s)

    sft_rows = []
    for lang, rows in sorted(by_lang.items()):
        slug = lang.lower().replace("+", "p").replace("#", "sharp").replace(" ", "-")
        lines = [
            f"# Vulnerable Code Samples: {lang}",
            "",
            f"Secure-code-review training examples ({len(rows)} samples). "
            "Each sample is vulnerable code, the vulnerability class, and references.",
            "",
        ]
        for i, s in enumerate(rows, 1):
            lines.append(f"## Sample {i} — {s['vulnerability']}")
            lines.append("")
            lines.append(f"- **Language**: {s['language']}")
            lines.append(f"- **Vulnerability**: {s['vulnerability']}")
            lines.append(f"- **Description**: {s['description']}")
            lines.append("")
            lines.append("```")
            lines.append(s["code"])
            lines.append("```")
            lines.append("")
            if s.get("references"):
                lines.append("**References**:")
                for ref in s["references"]:
                    lines.append(f"- {ref}")
                lines.append("")
            sft_rows.append(
                {
                    "instruction": INSTRUCTION_TMPL.format(language=lang),
                    "input": s["code"],
                    "output": (
                        f"Vulnerability: {s['vulnerability']}\n"
                        f"Description: {s['description']}\n"
                        f"References: {'; '.join(s.get('references') or [])}"
                    ),
                }
            )
        with open(os.path.join(KB_OUT, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"KB: {slug}.md ({len(rows)} samples)")

    with open(os.path.join(TRAIN_OUT, "code_review_sft.jsonl"), "w", encoding="utf-8") as f:
        for row in sft_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"SFT: {len(sft_rows)} instruction rows -> code_review_sft.jsonl")


if __name__ == "__main__":
    main()
