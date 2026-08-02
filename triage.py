import re
from datetime import datetime
from pathlib import Path

import ollama

EVIDENCE_DIR = Path("evidence")
RUNBOOK_PATH = Path("ir_runbook.md")
REPORTS_DIR = Path("reports")
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """You are a senior SOC analyst conducting incident triage.
Analyze the provided log evidence and incident-response runbook carefully.
Base your findings only on the evidence supplied — do not invent facts.

Produce a Markdown incident report with these sections:

1. **Summary** — executive overview of the incident
2. **Timeline** — chronological key events; each entry must include a confidence tag
3. **Root Cause** — most likely initial access vector and attack path
4. **MITRE ATT&CK Mapping** — for each technique, list tactic, technique name, technique ID, and confidence
5. **Runbook Compliance** — which runbook steps appear completed vs. missed
6. **Recommended Next Actions** — prioritized follow-up for the IR team
7. **Uncertainties & Low-Confidence Items** — anything you cannot confirm from the evidence, assumptions made, ambiguous log data, or findings that need human verification

## Confidence tagging rules

For every finding in sections 2–6, append a confidence block immediately after the finding:

- **Confidence:** High | Medium | Low
- **Confidence note:** one sentence citing the log line(s) that support the finding, or explaining why it is inferred

Use these definitions:
- **High** — directly observed in the supplied logs (exact timestamp, IP, user, or action)
- **Medium** — strongly implied by multiple log entries but not explicitly stated
- **Low** — hypothesis or inference with limited or no direct evidence; requires analyst verification

Section 7 must collect every Low-confidence item and any Medium-confidence item where the evidence is ambiguous (e.g., logs from different dates, missing context, or conflicting indicators). Flag these clearly for human review.

Do not omit confidence tags. When unsure, choose Low and explain why in the confidence note rather than guessing.
"""

CONFIDENCE_LEGEND = """\
---
*Report generated with per-finding confidence tags (High / Medium / Low). Review section 7 and all Low-confidence items before acting.*
"""


def build_evidence_grounding(evidence_dir: Path) -> tuple[str, list[str]]:
    """Extract observable log lines and auto-detect ambiguities for the model."""
    observed_lines: list[str] = []
    auto_flags: list[str] = []
    dates_by_file: dict[str, tuple[str, str]] = {}
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")

    for log_path in sorted(evidence_dir.iterdir()):
        if not log_path.is_file():
            continue
        content = log_path.read_text()
        dates = date_pattern.findall(content)
        if dates:
            dates_by_file[log_path.name] = (min(dates), max(dates))

        observed_lines.append(f"=== {log_path.name} ===")
        for line in content.strip().splitlines():
            line = line.strip()
            if line:
                observed_lines.append(f"  OBSERVED: {line}")

    unique_dates = {dmin for dmin, _ in dates_by_file.values()}
    if len(unique_dates) > 1:
        auto_flags.append(
            "Log files span different dates — do not merge into one timeline without noting uncertainty:"
        )
        for name, (dmin, dmax) in dates_by_file.items():
            range_label = dmin if dmin == dmax else f"{dmin} to {dmax}"
            auto_flags.append(f"  - {name}: {range_label}")

    return "\n".join(observed_lines), auto_flags


# Step 1: Read every log file in the evidence/ folder
evidence_parts = []
for log_path in sorted(EVIDENCE_DIR.iterdir()):
    if log_path.is_file():
        evidence_parts.append(f"=== {log_path.name} ===\n{log_path.read_text()}")
evidence_text = "\n\n".join(evidence_parts)

grounding_text, auto_flags = build_evidence_grounding(EVIDENCE_DIR)

# Step 2: Read the incident-response runbook
runbook_text = RUNBOOK_PATH.read_text()

# Step 3: Send evidence and runbook to the local Llama model via Ollama
auto_flag_block = ""
if auto_flags:
    auto_flag_block = (
        "\n## Auto-detected ambiguities (flag these in section 7)\n\n"
        + "\n".join(auto_flags)
        + "\n"
    )

user_prompt = f"""Review the following evidence logs and IR runbook, then write the incident report.
Use the structured grounding block to separate directly observed facts from inferences.
Tag every finding with High, Medium, or Low confidence and a one-line confidence note.

## Structured Evidence Grounding

{grounding_text}
{auto_flag_block}
## Raw Evidence Logs

{evidence_text}

## Incident Response Runbook

{runbook_text}
"""

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
)
report_content = response.message.content.strip()
if CONFIDENCE_LEGEND not in report_content:
    report_content = f"{report_content}\n\n{CONFIDENCE_LEGEND}"

# Step 4: Create reports/ if needed and write a timestamped Markdown report
REPORTS_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
report_path = REPORTS_DIR / f"report_{timestamp}.md"
report_path.write_text(report_content)

print(f"Incident report written to {report_path}")
