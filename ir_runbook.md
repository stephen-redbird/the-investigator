# Ransomware Incident Response Runbook

Concise playbook aligned with **NIST SP 800-61** phases. Use checkboxes to track progress. Verify findings before acting — document decisions, times, and owners.

---

## 1. Preparation

1. [ ] Maintain an up-to-date contact list (IR lead, IT, legal, PR, executives, cyber insurance, law enforcement).
2. [ ] Define ransomware severity levels and escalation thresholds (single host vs. domain-wide encryption).
3. [ ] Pre-stage offline backups and test restore procedures at least quarterly.
4. [ ] Segment critical systems (AD, backups, finance, EDR console) from general user networks.
5. [ ] Deploy and tune EDR, email filtering, MFA, and centralized logging (auth, DNS, proxy, file).
6. [ ] Document asset inventory, data classification, and crown-jewel systems.
7. [ ] Store IR tools offline (boot media, forensic kits, spare admin workstation, out-of-band comms).
8. [ ] Train staff on phishing/reporting; run tabletop exercises for ransomware scenarios.
9. [ ] Pre-negotiate retainers with forensics/legal counsel; know cyber insurance claim requirements.
10. [ ] Keep runbooks, network diagrams, and credential-recovery procedures accessible **offline**.

---



## 2. Detection & Analysis

1. [ ] Confirm the alert: ransom note, mass file renames, EDR/detection hits, user report, or backup failure.
2. [ ] Record initial indicators — time first seen, affected hosts/users, ransom note text, file extensions, contact addresses.
3. [ ] Activate the IR team and assign roles (lead, comms, forensics, containment, scribe).
4. [ ] Preserve evidence before changes: snapshot VMs, export EDR alerts, pull auth/file/network logs, photograph ransom screens.
5. [ ]Capture volatile memory before shutdown or reboot where feasible.
6. [ ] Record active network connections and running processes.
7. [ ] Identify patient zero and initial access vector (phish, RDP, VPN, supply chain, stolen creds).
8. [ ] Determine scope: count encrypted hosts, mapped shares, cloud sync folders, and backup targets touched.
9. [ ] Verify whether encryption is still actively occurring.
10. [ ] Determine whether the threat actor still has interactive access.
11. [ ] Check for double extortion — exfiltration to unknown IPs, large outbound transfers, attacker staging folders.
12. [ ] Hunt for persistence (new admin accounts, scheduled tasks, services, GPO changes, disabled AV/EDR).
13. [ ] Map lateral movement (PsExec, WMI, RDP hops, Cobalt Strike beacons, abnormal Kerberos activity).
14. [ ] Assess whether data theft occurred in addition to encryption.
15. [ ] Classify the ransomware family where possible (note extension, ransom note, sample hash) to inform response.
16. [ ] Brief leadership with facts only: scope, business impact, backup status, and recommended next phase.

---



## 3. Containment, Eradication & Recovery



### Containment

1. [ ]Identify critical systems that should remain online for evidence collection.
2. [][ Isolate affected endpoints from the network (disable NIC / VLAN quarantine — avoid powering off if memory forensics needed).
3. [ ] Block known malicious IPs, domains, and hashes at firewall, DNS, proxy, and email gateways.
4. [ ] Consider temporarily disabling privileged administrative accounts that may be under attacker control.
5. [ ] Disable compromised accounts; force password resets and revoke active sessions/tokens.
6. [ ] Stop lateral spread: restrict RDP/SMB between segments, disable unused admin shares, pause GPO replication if poisoned.
7. [ ] Protect backups — disconnect immutable/offline copies; verify backup servers are not encrypted or reachable by attackers.
8. [ ] Preserve business-critical systems that are still clean; do not reconnect isolated hosts until eradication is complete.



### Eradication

1. [ ] Remove malware, backdoors, and attacker tools from all identified systems (reimage preferred over clean-in-place).
2. [ ] Delete unauthorized accounts, API keys, certificates, and persistence mechanisms across AD and SaaS.
3. [ ] Patch the initial-access vulnerability and close exposed services (RDP, VPN, unpatched edge devices).
4. [ ] Rotate all privileged credentials, KRBTGT (if AD compromised), service accounts, and application secrets.
5. [ ] Rebuild domain controllers and critical servers from **known-good** media if trust cannot be restored.



### Recovery

1. [ ] Restore from verified clean backups; validate file integrity and malware-free snapshots before cutover.
2. [ ] Reconnect systems in phases — start with isolated test VLAN; confirm no re-encryption or beaconing.
3. [ ]Validate business applications and dependencies before reconnecting to production networks.
4. [ ] Re-enable MFA, EDR, logging, and monitoring on recovered hosts before returning to production.
5. [ ] Communicate service restoration status to users and stakeholders; watch for recurrence in the first 72 hours.
6. [ ] **Do not pay ransom as default policy.** If payment is considered, involve legal, insurance, and law enforcement first.

---



## 4. Post-Incident

1. [ ] Hold a blameless post-incident review within 5–10 business days; capture timeline, root cause, and control gaps.
2. [ ] Document lessons learned and assign owners with due dates for each corrective action.
3. [ ] Update this runbook, contact lists, and detection rules based on observed TTPs.
4. [ ] Report to regulators, customers, or partners if required (breach notification timelines vary by sector/region).
5. [ ] File reports with law enforcement and relevant ISACs; share IOCs (hashes, IPs, domains, email addresses).
6. [ ] Improve backups (3-2-1 rule, immutability, offsite, restore testing) and network segmentation.
7. [ ] Retrain users on phishing and incident reporting; adjust email filtering and MFA coverage.
8. [ ] Conduct a follow-up tabletop or purple-team exercise to validate fixes.
9. [ ] Archive evidence chain-of-custody records, executive decisions, and insurance documentation.
10. [ ] Monitor for attacker re-entry using retained IOCs for at least 90 days.

---



## Quick Reference


| Phase                               | Primary goal                                   |
| ----------------------------------- | ---------------------------------------------- |
| Preparation                         | Be ready before an attack                      |
| Detection & Analysis                | Confirm, scope, and understand the incident    |
| Containment, Eradication & Recovery | Stop spread, remove threat, restore operations |
| Post-Incident                       | Learn, improve, and meet reporting obligations |


**Remember:** Isolate → preserve evidence → scope → contain → eradicate → recover → review. When in doubt, escalate and verify before reconnecting systems or paying ransom.