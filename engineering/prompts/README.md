# Prompts Directory

This directory contains prompt templates for AI-driven security analysis.

## Prompt Types

### Analysis Prompts
Prompts that analyze findings → risk, business impact, remediation.

### Triage Prompts
Prompts that classify findings (true/false positive, severity calibration).

### Report Prompts
Prompts that generate executive summaries and detailed reports.

### Code-Aware Prompts
Prompts for code analysis, configuration review, and remediation suggestions.

## Prompt Format

```yaml
# prompt.yml
id: triage-finding-v1
version: "1.0.0"
description: "Triage a single finding"
model: gpt-4o

inputs:
  finding_title: string (required)
  finding_description: string (required)
  asset_context: string (optional)

template: |
  You are a senior security analyst reviewing a finding.

  Finding: {{finding_title}}
  Description: {{finding_description}}
  Asset Context: {{asset_context}}

  Classify:
  - true_positive / false_positive
  - severity: critical / high / medium / low
  - prioritize: 1-5

  Return JSON only.
```

## Using Prompts

```python
from app.ai.prompts import load_prompt, render

template = load_prompt("triage-finding-v1")
prompt = render(template, {
    "finding_title": "Open SSH Port",
    "finding_description": "Port 22 is exposed with root login allowed",
})
```

## Adding a New Prompt

1. Create a new YAML file in `prompts/`
2. Follow the format above
3. Use Jinja2-style templating
4. Document expected outputs