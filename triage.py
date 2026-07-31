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
2. **Timeline** — chronological key events
3. **Root Cause** — most likely initial access vector and attack path
4. **MITRE ATT&CK Mapping** — for each finding, list tactic, technique name, and technique ID
5. **Runbook Compliance** — which runbook steps appear completed vs. missed
6. **Recommended Next Actions** — prioritized follow-up for the IR team
"""

# Step 1: Read every log file in the evidence/ folder
evidence_parts = []
for log_path in sorted(EVIDENCE_DIR.iterdir()):
    if log_path.is_file():
        evidence_parts.append(f"=== {log_path.name} ===\n{log_path.read_text()}")
evidence_text = "\n\n".join(evidence_parts)

# Step 2: Read the incident-response runbook
runbook_text = RUNBOOK_PATH.read_text()

# Step 3: Send evidence and runbook to the local Llama model via Ollama
user_prompt = f"""Review the following evidence logs and IR runbook, then write the incident report.

## Evidence Logs

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
report_content = response.message.content

# Step 4: Create reports/ if needed and write a timestamped Markdown report
REPORTS_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
report_path = REPORTS_DIR / f"report_{timestamp}.md"
report_path.write_text(report_content)

print(f"Incident report written to {report_path}")
