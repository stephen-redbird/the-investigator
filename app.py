"""
The Investigator — SOC Copilot (Week 8)

The Week 7 app, now with a fourth tab: Autonomous Investigation. The agent from
this week's CLI lab, brought home into the product — the SAME loop and the SAME
tools, now running in the browser on your deployed site. One Investigator, two
modes: you drive it (the first three tabs) or it drives itself (the fourth).

The pieces worth understanding are marked  #->
"""

import os
import json
import streamlit as st
from groq import Groq
from datetime import datetime

MODEL = "llama-3.3-70b-versatile"
REPORTS_DIR = "reports"
EVIDENCE_DIR = "evidence"

CORRELATION_SYSTEM_PROMPT = """You are a senior SOC analyst. You are given one or
more raw log files from a single environment. Correlate them into ONE incident and
produce a Markdown report with these exact sections:

## 1. Threat Analysis
What happened, the attack chain in order, and the hosts, accounts, and IPs involved.

## 2. MITRE ATT&CK Mapping
For each finding: tactic, technique name, and technique ID (e.g., T1059).

## 3. Severity
One of Low / Medium / High / Critical, with a one-line justification.

## 4. Investigation Plan
Concrete next steps to confirm scope.

## 5. Response Plan
Containment, eradication, and recovery steps.

Cite the specific log evidence for each claim. If something is uncertain, say so —
do not invent technique IDs or events that are not present in the logs."""


# #-> The key is read from st.secrets, never hard-coded. The first three tabs use this.
def ask_groq(messages):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        resp = client.chat.completions.create(model=MODEL, messages=messages)
        return resp.choices[0].message.content
    except KeyError:
        return "⚠️ No GROQ_API_KEY found. Add it in your app's Secrets."
    except Exception as e:
        return f"⚠️ Groq request failed: {e}"


# ===========================================================================
# AGENT MACHINERY — identical to the Week 8 CLI agent (agent.py).
# Same tools, same schema, same loop. Only the input/output changes: it reads
# the key from st.secrets and writes its trail to the page instead of the
# terminal. That's the whole point — an agent is the loop, not the interface.
# ===========================================================================
MITRE = {
    "T1110": "Brute Force — guessing credentials through many login attempts.",
    "T1078": "Valid Accounts — abusing existing legitimate credentials.",
    "T1136": "Create Account — creating a new account for persistence.",
    "T1021": "Remote Services — moving laterally using remote access (RDP/SMB).",
    "T1059": "Command and Scripting Interpreter — running commands via a shell.",
    "T1071": "Application Layer Protocol — C2 traffic over common protocols.",
    "T1105": "Ingress Tool Transfer — downloading tools/payloads onto a host.",
    "T1486": "Data Encrypted for Impact — ransomware encrypting files.",
    "T1562": "Impair Defenses — disabling security tools (e.g., antivirus).",
    "T1070": "Indicator Removal — clearing logs to hide activity.",
    "T1560": "Archive Collected Data — staging/compressing data before exfil.",
    "T1048": "Exfiltration Over Alternative Protocol — sending data to an attacker.",
}


def list_evidence():
    if not os.path.isdir(EVIDENCE_DIR):
        return "No evidence/ folder found."
    files = [f for f in os.listdir(EVIDENCE_DIR) if f.endswith((".log", ".txt"))]
    return "\n".join(files) if files else "evidence/ is empty."


def read_log(filename):
    path = os.path.join(EVIDENCE_DIR, os.path.basename(filename))
    if not os.path.isfile(path):
        return f"No such file: {filename}"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def lookup_mitre(technique_id):
    key = technique_id.upper().strip()
    return MITRE.get(key, f"{key}: not in local reference — verify at attack.mitre.org")


TOOLS = [
    {"type": "function", "function": {
        "name": "list_evidence",
        "description": "List the log files available in the evidence/ folder.",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "read_log",
        "description": "Read the full contents of one evidence log file.",
        "parameters": {"type": "object",
            "properties": {"filename": {"type": "string", "description": "The log file name, e.g. auth_events.log"}},
            "required": ["filename"]},
    }},
    {"type": "function", "function": {
        "name": "lookup_mitre",
        "description": "Look up what a MITRE ATT&CK technique ID means, e.g. T1110.",
        "parameters": {"type": "object",
            "properties": {"technique_id": {"type": "string", "description": "A technique ID like T1059."}},
            "required": ["technique_id"]},
    }},
]

AVAILABLE = {"list_evidence": list_evidence, "read_log": read_log, "lookup_mitre": lookup_mitre}

AGENT_SYSTEM = """You are an autonomous SOC analyst. Investigate the incident in the
evidence/ folder using the tools available to you. Decide for yourself which logs
to read and which technique IDs to verify. When you have enough to be sure, stop
calling tools and write a final report with: what happened (the attack chain in
order), the hosts/accounts/IPs involved, a MITRE ATT&CK mapping (tactic, technique
name, ID), and a severity (Low/Medium/High/Critical). Only cite evidence you have
actually read. Do not invent log lines or technique IDs."""


def run_agent(goal, max_steps=10):
    """The exact loop from agent.py — it just st.write()s the trail instead of print()."""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except KeyError:
        return "⚠️ No GROQ_API_KEY found. Add it in your app's Secrets."

    messages = [{"role": "system", "content": AGENT_SYSTEM},
                {"role": "user", "content": goal}]

    for step in range(max_steps):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto")
        msg = resp.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:               # no tool wanted => final verdict
            return msg.content

        for tc in msg.tool_calls:            # the agent CHOSE these — show the trail
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}") or {}
            st.write(f"🔧 **step {step + 1}** · `{name}({args})`")
            result = AVAILABLE[name](**args)
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "name": name, "content": str(result)})

    return "_(stopped: hit the step limit without a verdict)_"


st.set_page_config(page_title="The Investigator v1.2 — SOC Copilot", page_icon="🕵️")
st.title("🕵️ The Investigator v1.2 — SOC Copilot")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Correlate & Triage", "Ask the Investigator", "Case Files", "Autonomous Investigation"]
)

# ---------------------------------------------------------------------------
# TAB 1 — Correlate & Triage
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Correlate & Triage")
    st.caption("Upload one or more logs. The Copilot correlates them into a single verdict.")

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    uploaded = st.file_uploader(
        "Upload log files",
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.uploader_key}",
    )

    if st.button("Run correlation", disabled=not uploaded):
        combined = ""
        for f in uploaded:
            text = f.read().decode("utf-8", errors="ignore")
            combined += f"\n\n===== {f.name} =====\n{text}"
        with st.spinner("Correlating across sources..."):
            st.session_state.report = ask_groq([
                {"role": "system", "content": CORRELATION_SYSTEM_PROMPT},
                {"role": "user", "content": combined},
            ])

    if st.session_state.get("report"):
        st.markdown(st.session_state.report)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        st.download_button(
            "⬇️ Download report",
            st.session_state.report,
            file_name=f"triage_report_{stamp}.md",
        )
        if st.button("Start new analysis"):
            st.session_state.pop("report", None)
            st.session_state.uploader_key += 1
            st.rerun()

# ---------------------------------------------------------------------------
# TAB 2 — Ask the Investigator (chat)
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Ask the Investigator")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).markdown(msg["content"])

    question = st.chat_input("Ask about the case or SOC analysis...")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        st.chat_message("user").markdown(question)
        with st.spinner("Thinking..."):
            answer = ask_groq(
                [{"role": "system",
                  "content": "You are a senior SOC analyst helping a colleague. Be concise and precise."}]
                + st.session_state.chat
            )
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").markdown(answer)

# ---------------------------------------------------------------------------
# TAB 3 — Case Files (browse saved reports)
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Case Files")
    st.caption(f"Saved Markdown reports from the `{REPORTS_DIR}/` folder.")

    if os.path.isdir(REPORTS_DIR):
        md_files = sorted(
            (f for f in os.listdir(REPORTS_DIR) if f.endswith(".md")),
            reverse=True,
        )
    else:
        md_files = []

    if not md_files:
        st.info("No case files yet. Reports saved to `reports/` will appear here.")
    else:
        choice = st.selectbox("Pick a case file", md_files)
        with open(os.path.join(REPORTS_DIR, choice), "r", encoding="utf-8") as f:
            st.markdown(f.read())

# ---------------------------------------------------------------------------
# TAB 4 — Autonomous Investigation (the agent, in the browser)
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Autonomous Investigation")
    st.caption("Hand the Investigator a goal and watch it choose its own steps — then audit the trail.")
    st.write(
        f"It investigates the logs already in your **`{EVIDENCE_DIR}/`** folder, deciding for "
        "itself which to read and which techniques to verify. Read the trail, then check the verdict."
    )

    # #-> One button kicks off the loop. The trail streams into the status panel as
    #     each tool call happens; the verdict renders below when it finishes.
    if st.button("🕵️ Run autonomous investigation"):
        with st.status("The Investigator is working…", expanded=True):
            verdict = run_agent(
                "Investigate the incident in the evidence/ folder and report what happened."
            )
        st.markdown("### Verdict")
        st.markdown(verdict)
        st.caption("Supervise it: did it read every relevant log, verify its MITRE IDs, and invent nothing?")
