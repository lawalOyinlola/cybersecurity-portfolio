# Phishing incident response: playbook-driven triage and IoC analysis

End-to-end level-one SOC response to a phishing alert (ticket A-2703) at a
financial services company. I worked a defined phishing playbook to an
escalate-vs-close decision, documented it in an auditable ticket, then analysed
the malicious attachment in VirusTotal and mapped its indicators of compromise
onto the Pyramid of Pain. This is hands-on incident response: a defensible
decision backed by layered evidence, and durable detection derived from it.

## 📖 Context

A phishing alert was raised for ticket A-2703. An email sent to the HR mailbox
carried a password-protected executable attachment (`bfsvc.exe`) presented as a
job applicant's resume and cover letter, and the recipient may have opened it. The
attachment's file hash had already been verified malicious. My task was two-fold:
follow the organization's phishing playbook to investigate the alert and resolve
the ticket with the correct status and documented reasoning, then analyse the file
itself to extract indicators of compromise for detection.

## ⚙️ Action

**Phase 1 — playbook-driven triage.** I worked the alert through the playbook and
flowchart in order, evaluating the alert against its criteria — severity, sender
and receiver details, subject line, message body, and attachments — then followed
the decision branch: Step 3.0 confirmed an attachment was present, Step 3.1
confirmed it malicious on the basis of the verified hash, which routes to Step 3.2:
escalate. I recorded the investigation in the incident handler's journal and
updated the alert ticket from Open → Investigating → Escalated, with comments
drawing the escalation reasons from specific ticket details.

**Phase 2 — IoC analysis in VirusTotal.** I searched the file hash and reviewed
four tabs — Detection (vendor flags), Details (static properties and other
hashes), Relations (contacted domains, URLs, IPs), and Behavior (sandbox activity
as MITRE ATT&CK techniques). I then chose three indicators of compromise,
deliberately one each from the base, middle, and top of the Pyramid of Pain, so
the framework is visible in the result.

## ✅ Result

**The alert is a genuine, malicious phishing attempt — escalated to a level-two
analyst, not closed.** The evidence is specific and layered: a confirmed-malicious
file hash, a spoofed non-corporate sender on a `.su` domain with a mismatched
display name, spelling and grammar errors throughout the subject and body, and a
password-protected executable posing as a resume. The password protection is the
sharpest indicator — a deliberate technique to evade email malware scanning, with
no legitimate reason to accompany a job application, and the password itself was
supplied in the email body. HR was targeted precisely because the role routinely
opens attachments from strangers.

[![Alert ticket, escalated, with documented reasoning](./preview.png)](./alert-ticket.pdf)

_Auditable decision: [Alert Ticket (PDF)](./alert-ticket.pdf) · running
[Incident Handler's Journal (PDF)](./incident-handlers-journal.pdf)_

**The file is malicious, confirmed by agreeing signals**, not one number: 51 of 69
vendors flagged it, the community score is -297, and the threat label
`trojan.flagpro/fragtor` ties it to the BlackTech threat actor. It masquerades as a
legitimate Windows binary (`bfsvc.exe`, Boot File Servicing Utility) but is
unsigned, and the sandbox observed process injection, sandbox evasion, and
command-and-control traffic. Three indicators of compromise, from the bottom,
middle, and top of the pyramid:

- **Hash values (bottom, easiest to change):** additional MD5/SHA-1 hashes for the
  same file. Blocking a hash stops this exact file but not a recompiled copy.
- **Domain names (middle):** `org.misecure.com`, a contacted domain matching an
  IDS rule for dynamic-DNS C2 traffic. Blocking it forces the attacker to stand up
  new infrastructure.
- **Tactics, techniques, procedures (top, hardest to change):** process injection
  (T1055), masquerading (T1036), virtualization/sandbox evasion (T1497), and
  application-layer C2 (T1071). Detecting on behaviour is the most durable defence.

_Full IoC breakdown: [Pyramid of Pain / VirusTotal analysis (PDF)](./ioc-analysis-pyramid-of-pain.pdf)_

Recommended tier-two follow-up: confirm whether the endpoint executed the file,
review EDR for compromise or lateral movement, and isolate the affected host
pending that review.

## 🧠 What this demonstrates

This is the difference between *documenting* an incident and *working* one. The
lab shows a defensible escalate-vs-close decision reached by weighing specific,
layered evidence against a defined playbook — the judgment a SOC or IR reviewer
looks for — and made auditable through ticket comments and a journal entry. It then
shows threat-intelligence skill: confirming maliciousness from several agreeing
signals rather than one metric, separating genuinely malicious indicators from the
benign noise a VirusTotal report also contains, and reasoning about detection
durability with the Pyramid of Pain and MITRE ATT&CK — the higher up the pyramid a
defender detects, the more costly the attack becomes to sustain. The
phishing-and-attachment root cause is a recurring human-entry-point theme across
the incident-analysis work, the same pattern that opens the USB baiting and
ransomware scenarios.

## 📂 Source materials

**Scenario and attribution**

The phishing scenario, the alert ticket, the incident handler's journal, and the
response playbook are adapted from the Google Cybersecurity Certificate, Module 6:
Sound the Alarm, Detection and Response (Coursera). The playbook-driven triage, the
escalation decision and its documented reasoning, the VirusTotal IoC analysis, and
the write-up documented in this lab are my own work.

Artifacts in this folder:

- **[alert-ticket.pdf](./alert-ticket.pdf):** the auditable ticket, escalated Open → Investigating → Escalated with documented reasoning.
- **[ioc-analysis-pyramid-of-pain.pdf](./ioc-analysis-pyramid-of-pain.pdf):** the VirusTotal IoC analysis mapped onto the Pyramid of Pain.
- **[incident-handlers-journal.pdf](./incident-handlers-journal.pdf):** the running incident handler's journal.

The editable sources and the provided playbook live in [`source/`](./source/):

- **alert-ticket.docx:** editable source of the completed alert ticket.
- **ioc-analysis-pyramid-of-pain.pptx:** editable source of the IoC analysis.
- **phishing-response-playbook.pdf:** the phishing incident response playbook and flowchart the triage was structured against.
