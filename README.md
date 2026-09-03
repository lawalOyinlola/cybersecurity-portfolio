# Cybersecurity Portfolio

Welcome to my cybersecurity portfolio. This repository documents my transition from frontend software engineering into application and cloud security, with a focus on building secure systems rather than monitoring them. Here you will find hands-on labs, incident analyses, and engineering-security projects that trace my practical skill development.

---

## 👤 About Me

I am a frontend engineer and team lead at a fintech company, moving into application security and DevSecOps. Rather than stepping away from engineering, I lean into it: my strength is understanding how software is built, which is exactly what lets me find where it breaks and fix it. I focus on proactive security, securing code, hardening CI/CD pipelines, and building strong identity and access controls, with a long-term trajectory toward cloud and AI security. My software background is not a separate past life; it is the foundation I build security on.

---

## 🛡️ Technical Skills & Tooling

### 🔐 Application & Cloud Security (In Progress)

- **Application Security:** OWASP Top 10, secure code review, dependency and vulnerability management, threat modeling
- **DevSecOps:** CI/CD security pipelines, SAST and DAST, secrets scanning, GitHub Actions
- **Identity & Cloud:** IAM concepts, authentication mechanics (OAuth2/OIDC, tokens, sessions), Microsoft Entra ID, Azure security fundamentals
- **Foundations:** Threat and incident analysis, NIST CSF, risk assessment, Linux CLI, SQL, core network protocols (TCP/IP, DNS, HTTP/S)

### 🧰 Security Tooling

Semgrep, OWASP ZAP, Trivy, Gitleaks, Dependabot, GitHub Actions, tcpdump and Wireshark (traffic analysis)

### 💻 Software Engineering Foundation

- **Web Architecture:** Frontend system design, secure application logic, web performance
- **Languages:** JavaScript, TypeScript, HTML5/CSS3; SQL and Python for scripting

---

## 🧪 Projects, Labs & Case Studies

Documented using the **CAR (Context, Action, Result)** framework, grouped by theme. Each individual investigation's write-up lives in its own `analysis.md`; grouped labs (multiple investigations under one theme) are indexed by a `README.md` that links out to each.

### 🚀 Application Security Engineering

The core of my work: securing real software and its delivery pipeline.

- **[CI/CD Security Pipeline](./labs/cicd-security-pipeline/analysis.md)** _(featured)_ — Policy-driven SAST, dependency, container, and secrets scanning added to a live, self-hosted SaaS product via GitHub Actions, with every finding individually triaged (fixed, accepted, or false-positive with reasoning) and a fail-open defect in the pipeline's own deploy gate found and fixed after the fact.
- **[Runtime Defence with a WAF](./labs/waf-runtime-defence/analysis.md)** _(featured)_ — ModSecurity and the OWASP Core Rule Set put in front of the same production application as the pipeline above, attacked across six payload classes against a no-WAF control, and measured. Blocked 12 of 26 payloads, every one already handled by the framework; the class that decides real breaches, broken object-level authorisation, passed through untouched, as it must, and was stopped by the application's own tenant isolation instead. Found a rule-placement bypass, and tuned the one false positive that mattered (the Core Rule Set blocking PATCH and DELETE on a REST API) with a single documented exclusion rather than by lowering paranoia. Concludes on the WAF as a compensating control that buys response time, not a fix.
- **[Auditing Automated Malware Response (Wazuh + VirusTotal)](./labs/wazuh-virustotal-response/analysis.md)** — A self-built detection, enrichment, and auto-remediation pipeline that produced a complete and convincing alert chain for a full day while deleting nothing, surfaced only by checking the filesystem by hand. The response step is not a configuration toggle but a shell script running as root against operator-uncontrolled input: the audit found an unverified dependency masked by an unconditional `exit 0`, no logging on any path, and an unvalidated path passed straight to `rm -f`. Rewritten with dependency checks, path confinement, deletion verification, and an audit trail, then re-tested in both directions.
- **[PASTA Threat Model (Sneaker Marketplace App)](./labs/pasta-threat-model/analysis.md)** — Seven-stage application threat model of a payment-handling mobile app, tracing prioritized technology scope through a data flow diagram and attack tree to two vulnerabilities (SQL injection, session hijacking) and the four controls that each close a specific attack path.

### 🔎 Incident Analysis

- **[ADT Home Security Data Breach](./labs/incident-response-adt/analysis.md)** — Architectural breakdown of the April 2026 voice phishing (vishing) intrusion, its impact on SSO identity controls, and customer PII remediation.
- **[Network Traffic & Incident Analysis](./labs/network-traffic-analysis/)** — Four grouped investigations: packet-capture analysis of a DNS service outage, a SYN flood denial of service, and a brute-force attack with malware redirect, plus a full NIST CSF analysis of an ICMP flood, each tracing evidence to root cause and remediation.
- **[Phishing Incident Response (Playbook Triage & IoC Analysis)](./labs/phishing-incident-response/analysis.md)** — Level-one SOC triage of a phishing alert (ticket A-2703) worked through a defined playbook to an auditable escalate decision, then VirusTotal IoC analysis of the malicious attachment mapped onto the Pyramid of Pain and MITRE ATT&CK — one intrusion traced from alert to durable detection.
- **[Incident Handler's Journal](./labs/incident-handler-journal/incident-handlers-journal.md)** — A running nine-entry journal spanning the certificate work: two 5 W's incident investigations (ransomware, phishing) and six hands-on cybersecurity-tool entries (Wireshark, tcpdump, VirusTotal, Suricata, Splunk, and Chronicle), closed by a reflection on the learning journey.

### 📋 Governance, Risk & Compliance

- **[Internal Security Audit (Botium Toys)](./labs/internal-audit-botium-toys/analysis.md)** — Controls and compliance assessment of a fictional retailer against NIST CSF, PCI DSS, GDPR, and SOC, mapping a narrative risk assessment to named frameworks and producing a prioritized remediation roadmap.
- **[Network Hardening Assessment](./labs/network-hardening-assessment/analysis.md)** — Post-breach security risk assessment mapping four network vulnerabilities to a minimal set of hardening controls (MFA, password policies, port filtering), chosen by coverage rather than one tool per finding.
- **[Network Segmentation & Least Privilege (Hospital Network)](./labs/network-segmentation-least-privilege/analysis.md)** — Hands-on Cisco Packet Tracer build of a two-department hospital network, hardened past its connectivity brief with a directional router ACL (doctors reach the pharmacy; the pharmacy cannot initiate into patient-record hosts), switch port security, and SSH-only management, verified by ping asymmetry and live ACL hit counters.
- **[Vulnerability Assessment (Public E-commerce Database)](./labs/vulnerability-assessment-ecommerce-db/analysis.md)** — Qualitative NIST SP 800-30 Rev. 1 risk assessment of a MySQL server left publicly exposed for three years, scoring three threat source/event pairs on likelihood × severity and mapping the ranked risks to a root-cause, defense-in-depth control set.
- **[Access Control & Least Privilege](./labs/access-control-least-privilege/)** — Two grouped investigations: a data-leak incident from over-broad folder sharing, and a fraudulent payroll entry traced to a contractor account never deprovisioned, mapped to NIST SP 800-53 AC-6, AC-2, PS-4, and PS-5.

### 🧪 Technical Skills Labs

- **[Linux File Permissions](./labs/linux-file-permissions/analysis.md)** — Auditing and modifying file and directory authorization using `chmod` and `ls -la`, including interpretation of the permission string.
- **[SQL Filtering for Investigations](./labs/sql-query-filtering/analysis.md)** — Using `AND`, `OR`, `NOT`, `LIKE`, and date and time filters to investigate login activity and asset data.
- **[Python Algorithm for File Updates](./labs/python-file-updates/analysis.md)** — Automating allow list maintenance for a restricted patient-records subnetwork: a read → transform → write script using `with`/`open()`, `.read()`/`.write()`, `.split()`/`.join()`, a `for` loop, and membership-guarded `.remove()`.

---

## 📜 Certifications & Education

### 🔒 Security Certifications

- **Google Cybersecurity Professional Certificate** — Completed (Coursera) · [Verify credential](https://coursera.org/verify/professional-cert/PZZDNMRKGNAL) · [Credly badge](https://www.credly.com/badges/99d514e9-c306-4f55-95db-efd37a099b53/public_url)
- **CompTIA Security+** — Target 2026 (foundational baseline)
- **Microsoft SC-300, Identity & Access Administrator** — Planned
- **Microsoft SC-500, Cloud & AI Security Engineer** — Planned (destination)

### 🎓 Education

- **Higher Diploma in Computing, Griffith College Dublin, Ireland** — Graduation candidate, 2027
- **Frontend Engineering Diploma** — AltSchool Africa
- **Frontend Engineering Finalist** — HNG Internship

---

## 📬 Connect

- **LinkedIn:** [lawalOyinlola](https://www.linkedin.com/in/lawaloyinlola/)
- **GitHub:** [lawalOyinlola](https://github.com/lawalOyinlola/)
