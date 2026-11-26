# Governance gap analysis

This analysis compares what exists at SigKollect today with what a security governance programme
needs. Each row cites the evidence from the company context. A gap with no evidence is an opinion.

| Priority | Meaning |
|---|---|
| **H** (high) | Critical. Needs action now, because it could cause serious harm or it blocks other work |
| **M** (medium) | Important. Address within the next 3 to 6 months |
| **L** (low) | A worthwhile improvement. It can wait for a later phase |

## Findings

| # | Area | Current state | Gap | Priority | Why this priority | Evidence |
|---|---|---|---|---|---|---|
| 1 | Governance charter | None | No document says what the security programme covers, who authorises it and who runs it | H | Every other governance item needs its authority and scope from the charter | Security state, people |
| 2 | Security lead (CISO) | None. The founders approved the role, but nobody holds it. The CTO owns security informally, alongside delivery | No dedicated, accountable owner for security. Reporting line not decided | H | Without an owner, no other fix has anyone to keep it running | People (vacant) |
| 3 | GRC function or team | None for security. A compliance team of 6 covers payments regulation and anti-money-laundering only | Nobody owns security governance, risk or data protection | M | At 150 staff, the security lead and the consultant can carry GRC at first | People (Compliance) |
| 4 | Security policies | None written | No rules for access, patching, data handling or incident response | H | Every event E-1 to E-5 traces back to a missing rule | Security state, E-1 to E-5 |
| 5 | Risk appetite statement | None | No agreed limit on how much risk the company accepts, so no basis to accept or treat a risk | H | Risk treatment cannot start without it | Board never discussed security |
| 6 | Steering committee | None. The leaders who would sit on it exist, but no forum meets about security | No place where security decisions are made, funded and followed up | M | The CEO can make the first decisions directly. The committee matters once the programme runs | People |
| 7 | Adopted framework | None | No reference standard to measure the programme against | M | Needed for the questionnaire answers, but the choice can wait until the charter exists | Security state |
| 8 | Board reporting on security | The board meets quarterly. Security has never been on its agenda | The board cannot oversee a risk it never hears about | M | The board first needs a programme to report on | Board |
| 9 | Three lines model | 1st line exists. 2nd line partial (compliance for payments only). 3rd line none (no internal audit) | No independent check, and no security oversight function | L | The missing 2nd line is already row 2. Rating it higher counts the same gap twice | People |
| 10 | Governance KPIs | None | Nothing measures whether security is improving | L | A programme must exist before it can be measured | Security state |
| 11 | Access reviews | None ever. Access is granted on request in Slack. HR records leavers, but IT is not always told | Leavers can keep access, and nobody checks who has what | H | Customer and payment data are reachable, and E-4 showed one stolen password is enough | People, E-4 |
| 12 | Security awareness training | None | Staff are not taught to recognise phishing | M | E-4 shows the risk, but the agent did report it. MFA cuts the same risk faster | E-4 |
| 13 | Incident response plan | None. E-4 was handled ad hoc | No steps, roles or reporting route when something happens | H | E-4 may have started three reporting clocks, one of them immediate, and nobody knew | E-4, rules R-1, R-3, R-4 |
| 14 | Asset inventory | None | Nobody knows what systems exist or who owns them | H | You cannot protect what you do not know you have | E-1 |
| 15 | Supplier risk management | None | The card processor and the identity-verification provider handle sensitive data, unassessed | M | Real exposure, but the suppliers are specialists. Assess them after the internal basics | Third parties |

## Control gaps, sent to the risk register

These are control gaps, not governance gaps. They go to the risk register (lab 2).

- No MFA on the support tool (E-4).
- No dependency scanning or patching target (E-2).
- No central logging, alerting or detection (E-3, E-5). Logs kept only 14 days (E-3).
- No owner for data protection, and an open question about a data protection officer (R-1).
- No security step in the deployment pipeline (E-2).

## Top three priorities

1. **Security lead and charter (rows 1 and 2), together.** Accountability first. Without an owner and
   a mandate, every other fix depends on goodwill.
2. **Incident response plan (row 13).** Reporting clocks under three laws may apply. The next event must not be
   handled ad hoc.
3. **Asset inventory (row 14).** Access reviews, risk scoring and monitoring all need the list of
   what exists. E-1 shows the cost of not having it.
