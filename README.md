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

Documented using the **CAR (Context, Action, Result)** framework, grouped by theme. Each lab's write-up lives in its own `analysis.md`.

### 🚀 Application Security Engineering

The core of my work: securing real software and its delivery pipeline.

- **CI/CD Security Pipeline** _(featured, in progress)_ — Automated security scanning (SAST, dependency, and secrets scanning) added to a production web application through GitHub Actions, including triage and remediation of real dependency advisories surfaced by Dependabot.
- **[PASTA Threat Model (Sneaker Marketplace App)](./labs/pasta-threat-model/analysis.md)** — Seven-stage application threat model of a payment-handling mobile app, tracing prioritized technology scope through a data flow diagram and attack tree to two vulnerabilities (SQL injection, session hijacking) and the four controls that each close a specific attack path.

### 🔎 Incident Analysis

- **[ADT Home Security Data Breach](./labs/incident-response-adt/analysis.md)** — Architectural breakdown of the April 2026 voice phishing (vishing) intrusion, its impact on SSO identity controls, and customer PII remediation.
- **[Network Traffic & Incident Analysis](./labs/network-traffic-analysis/analysis.md)** — Four grouped investigations: packet-capture analysis of a DNS service outage, a SYN flood denial of service, and a brute-force attack with malware redirect, plus a full NIST CSF analysis of an ICMP flood, each tracing evidence to root cause and remediation.

### 📋 Governance, Risk & Compliance

- **[Internal Security Audit (Botium Toys)](./labs/internal-audit-botium-toys/analysis.md)** — Controls and compliance assessment of a fictional retailer against NIST CSF, PCI DSS, GDPR, and SOC, mapping a narrative risk assessment to named frameworks and producing a prioritized remediation roadmap.
- **[Network Hardening Assessment](./labs/network-hardening-assessment/analysis.md)** — Post-breach security risk assessment mapping four network vulnerabilities to a minimal set of hardening controls (MFA, password policies, port filtering), chosen by coverage rather than one tool per finding.
- **[Vulnerability Assessment (Public E-commerce Database)](./labs/vulnerability-assessment-ecommerce-db/analysis.md)** — Qualitative NIST SP 800-30 Rev. 1 risk assessment of a MySQL server left publicly exposed for three years, scoring three threat source/event pairs on likelihood × severity and mapping the ranked risks to a root-cause, defense-in-depth control set.
- **[Data Leak & Least Privilege](./labs/data-leak-least-privilege/analysis.md)** — Analysis of a data-leak incident and the NIST SP 800-53 AC-6 control improvements (role-based access, time-bound revocation) that would enforce least privilege and prevent recurrence.
- **[Orphaned Account Access Review](./labs/orphaned-account-access-review/analysis.md)** — Event-log and directory correlation tracing a fraudulent payroll entry to a contractor account left active four years after offboarding, mapped to NIST SP 800-53 AC-6, AC-2, PS-4, and PS-5.

### 🧪 Technical Skills Labs

- **[Linux File Permissions](./labs/linux-file-permissions/analysis.md)** — Auditing and modifying file and directory authorization using `chmod` and `ls -la`, including interpretation of the permission string.
- **[SQL Filtering for Investigations](./labs/sql-query-filtering/analysis.md)** — Using `AND`, `OR`, `NOT`, `LIKE`, and date and time filters to investigate login activity and asset data.

---

## 📜 Certifications & Education

### 🔒 Security Certifications

- **CompTIA Security+** — Target 2026 (foundational baseline)
- **Microsoft SC-300, Identity & Access Administrator** — Planned
- **Microsoft SC-500, Cloud & AI Security Engineer** — Planned (destination)
- **Google Cybersecurity Professional Certificate** — In progress (Coursera)

### 🎓 Education

- **Higher Diploma in Computing, Griffith College Dublin, Ireland** — Graduation candidate, 2027
- **Frontend Engineering Diploma** — AltSchool Africa
- **Frontend Engineering Finalist** — HNG Internship

---

## 📬 Connect

- **LinkedIn:** [lawalOyinlola](https://www.linkedin.com/in/lawaloyinlola/)
- **GitHub:** [lawalOyinlola](https://github.com/lawalOyinlola/)
