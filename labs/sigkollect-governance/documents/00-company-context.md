# Company context

**SigKollect is fictional.** Every person, record and incident in this pack is invented for a lab.
Any resemblance to a real organisation is not intended.

## Summary

- **The company.** SigKollect Limited is a payments company in Lagos, with about 150 people,
  serving merchants in Nigeria and the EU. It holds identity, bank and payment data.
- **The problem.** In 2026 it had five security events: a forgotten server, a five-week patch,
  probes on its payment page, a phishing click and a customer question nobody could answer. Every
  one was found by chance. None was found by a control.
- **The trigger.** A large EU merchant sent a security questionnaire before signing. The founders
  could not answer most of it.
- **The engagement.** The CEO engaged IAM <a href="https://lawaloyinlola.com" aria-label="LAWAL">⅃AWA⅃</a> Ltd to build the security programme, starting with
  governance, and to hand it to a security lead once the role is filled.

## Profile

| Field | Value |
|---|---|
| Legal name | SigKollect Limited |
| Legal form | Private company, registered in Nigeria |
| Founded | 2021 |
| Headquarters | Lagos, Nigeria |
| Staff | About 150, in Lagos and remote |
| Customers | Merchants and small businesses in Nigeria and the EU, served online |
| Annual revenue | About $6 million (2026) |
| Payments processed | About $500 million a year, at average fees of about 1.2% |
| Cloud | Microsoft Azure |

### Products

| Product | What it does | Who uses it |
|---|---|---|
| SigKollect Checkout | Payment gateway and payment links for online merchants | Merchants and their customers |
| SigKollect Business | Account app for small businesses: transfers and payouts | Small businesses |
| Partner API | Lets partners start payments and receive webhooks when a payment changes state | Developers at partner companies |

### Data held

| Data | Whose | Notes |
|---|---|---|
| Card payment data | Merchants' customers | Handled through a card processor, so most card data does not enter SigKollect's systems |
| Identity checks (BVN, NIN) | Small-business owners | Nigerian identity numbers, collected for customer due diligence |
| Bank details | Merchants and small businesses | For payouts |
| Staff records | Employees and contractors | HR data |

### Third parties

A card processor and an identity-verification provider (both fictional and unnamed), Microsoft
Azure, GitHub, Google Workspace and Slack.

### Security state at the start of the engagement

- No security lead. Engineering owns security informally.
- No written security policies.
- Monitoring on some systems only.
- No access reviews have ever taken place.
- No incident response plan.

## People

| Name | Role | Reports to | Team |
|---|---|---|---|
| Adaeze Okafor | Chief Executive Officer, co-founder | Board | |
| Tunde Bakare | Chief Technology Officer, co-founder | CEO | |
| Ruth Adebayo | Chief Operating Officer | CEO | |
| Ibrahim Sule | Chief Financial Officer | CEO | 8 |
| Emeka Onyeka | Head of Engineering | CTO | 52 |
| Uche Nnaji | IT and Systems Lead | CTO | 3 |
| (not named) | Data and Analytics Lead | CTO | 7 |
| Tobi Akande | Head of Customer Operations | COO | 34 |
| Halima Garba | Head of Compliance | COO | 6 |
| Zainab Abubakar | Head of Product | CEO | 12 |
| Kemi Fashola | Head of Sales and Partnerships | CEO | 18 |
| Bisi Ogunleye | Head of People | CEO | 5 |
| Vacant | Security lead | CEO (set by the charter) | |

The board has three directors: the two founders and one director for the seed investors. It meets
quarterly. Before this engagement, security had never been on its agenda.

External: Lawal Oyinlola, security consultant, IAM <a href="https://lawaloyinlola.com" aria-label="LAWAL">⅃AWA⅃</a> Ltd. The engagement is fictional, like
SigKollect.

## Security events in 2026

| # | When | Event | What it revealed |
|---|---|---|---|
| E-1 | Found August | A legacy reporting server, left running after the Azure move, on an unsupported operating system. It held merchant payout reports. Nobody knew who owned it | No asset inventory, no system owners, no decommissioning step |
| E-2 | April to May | A critical fix for the Checkout web framework took five weeks to reach production, after a partner asked | No dependency scanning, no pipeline security gate, no patching target |
| E-3 | June | SQL injection probes against the payment-link page, seen by chance. Logs kept only 14 days | No web application firewall, no alerting, short log retention |
| E-4 | September | A Customer Operations agent entered a password on a phishing page. The support tool had no MFA, and nobody checked its logs | No MFA, no phishing training, no incident response plan, no breach-assessment step |
| E-5 | October | The EU merchant asked how SigKollect would detect a brute-force attack on an administrator login. Nobody could answer | No central logging, no SIEM, no detection rules |

**Pattern:** every event was found by chance (a cost review, a partner's email, an engineer
debugging, an honest agent, a customer's question). None was found by a control.

## Rules in scope of the assessment

These rules may apply to SigKollect. Document 9 assesses each one against its primary text. This
pack is an analysis for a lab, not legal advice.

| # | Rule | Enforced by | Why it is on the list |
|---|---|---|---|
| R-1 | Nigeria Data Protection Act 2023, and the General Application and Implementation Directive (2025) | Nigeria Data Protection Commission (NDPC) | SigKollect processes personal data in Nigeria |
| R-2 | Central Bank of Nigeria risk-based cybersecurity framework | Central Bank of Nigeria | SigKollect collects payments under a CBN licence |
| R-3 | Cybercrimes (Prohibition, Prevention, etc.) Act 2015, amended 2024 | ngCERT, through the sector CERT | SigKollect runs computer systems in Nigeria's financial sector |
| R-4 | EU General Data Protection Regulation | EU data protection authorities | SigKollect processes personal data of people in the EU |
| R-5 | PCI DSS v4.0.1 | Card brands, through the acquirer and processor (contract, not law) | SigKollect takes card payments through a processor |
| R-6 | EU Digital Operational Resilience Act | EU financial supervisors | SigKollect serves EU customers and works in payments |
| R-7 | EU AI Act | EU and national authorities | SigKollect plans an AI assistant |

Three of these rules (R-1, R-3 and R-4) may each start a 72-hour reporting clock on the same event.
E-4 is the test case.
