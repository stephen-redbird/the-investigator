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
// Start the Investigator

