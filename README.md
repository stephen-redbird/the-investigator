# the-investigator

An AI-powered security & network analyst(being built over time)

## Skills so far

- Week 1: Thinks like a security analyst (prompt library)
- Week 2: Can triage suspicious emails — check headers (SPF/DKIM/DMARC, Reply-To), flag urgency/secrecy/authority, recommend out-of-band verification
- Week 3:Can audit server logs for failed-login and brute-force patterns (see audit.py).
- Week 4: Can hunt network beaconing (hunt.py) and reconstruct an incident timeline from multiple logs to guide response (timeline.py).
More coming each week.
- Week 5: Runs an automated triage pipeline (GitHub Actions + a local Llama 3.2 model via Ollama) that reads the IR runbook, maps findings to MITRE ATT&CK, and writes a verified incident report.
- Week 6: A Streamlit SOC Copilot that correlates four telemetry sources (firewall, Sysmon, Windows, Suricata) via Groq and returns a triaged report with MITRE mapping, severity, and response plan.
- Week 7: Case Files — browse saved Markdown reports from prior triage runs.
- Week 8: Agentic mode — give the Investigator a goal; it chooses tools, shows an auditable trail, and returns a supervised verdict (CLI via `agent.py`, same loop in the Streamlit Autonomous Investigation tab).
// Start the Investigator

## Live application

Streamlit App: https://the-investigator-yf4chngyyepi7ww7krozvp.streamlit.app/

**What it does**
- Correlate & Triage — upload logs; get one correlated incident report (MITRE, severity, investigation & response plans)
- Ask the Investigator — chat with a senior SOC analyst about the case
- Case Files — browse saved reports from prior runs in `reports/`
- Autonomous Investigation — agentic mode in the browser (see below)

**Agentic mode (Week 8)**
You hand it a goal (“investigate the incident in `evidence/`”); it decides the next steps — you supervise the trail instead of driving each click.

- Tools it can call: `list_evidence`, `read_log`, `lookup_mitre`
- Shows each tool call as it runs so you can audit what it chose
- Stops when it has enough evidence and writes a verdict: attack chain, hosts/accounts/IPs, MITRE mapping, and severity
- Same loop as `agent.py` (CLI) and the Autonomous Investigation tab (Streamlit)
- Only cites logs it actually read — verify the trail before you trust the verdict
