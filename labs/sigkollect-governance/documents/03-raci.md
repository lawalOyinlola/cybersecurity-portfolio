# Security RACI matrix

This matrix says who does each security activity, who owns it, who is asked first and who is told.
Roles come from the charter, section 5. It assumes the security lead is in post. Until April 2027,
the CEO, supported by the consultant, covers the security lead's entries.

## What the letters mean

| Letter             | Meaning                                                            | Question to ask                       |
| ------------------ | ------------------------------------------------------------------ | ------------------------------------- |
| **R**, Responsible | Does the work                                                      | Whose hands are on it?                |
| **A**, Accountable | Owns the outcome and signs it off. Answers for it if it goes wrong | Who gets the blame if it is not done? |
| **C**, Consulted   | Gives input **before** the work is done. Two-way                   | Whose opinion is needed first?        |
| **I**, Informed    | Is told **after** it is done. One-way                              | Who needs to know the result?         |

## Rules

1. **Exactly one A in each row.** Two A's means nobody is accountable.
2. **At least one R in each row.** An A with no R means nobody does the work.
3. **One person can be both.** `A/R` means the owner also does the work.
4. **A blank cell is fine.** Most roles have nothing to do with most activities.
5. **Segregation of duties.** The person who does something (R) is not also the only one who
   checks or approves it. For example, the CTO runs delivery, so the security lead, not the CTO, checks security.
6. **The CEO appears separately only when acting alone,** as executive sponsor in front of the board.
   When a decision goes through the steering committee, the SC column covers the CEO.

## The matrix

Roles: **Board** · **CEO** · **SC** (security steering committee) · **SL** (security lead) · **CTO** ·
**HoE** (Head of Engineering) · **IT** (IT and Systems Lead) · **HoP** (Head of People) ·
**HoC** (Head of Compliance) · **HoS** (Head of Sales and Partnerships) · **SO** (system or data owner) ·
**Staff** (all staff)

| # | Activity | Board | CEO | SC | SL | CTO | HoE | IT | HoP | HoC | HoS | SO | Staff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Approve the charter | A/R | C |  | C |  |  |  |  |  |  |  | I |
| 2 | Approve the risk appetite | A/R | C | C | C |  |  |  |  |  |  |  |  |
| 3 | Maintain the risk register |  |  | I | A/R | C |  | C |  | C |  | C |  |
| 4 | Accept a risk within the appetite (see note 1) |  |  | I | C |  |  |  |  |  |  | R |  |
| 5 | Accept a risk above the appetite | A/R | C | C | C |  |  |  |  |  |  |  |  |
| 6 | Write and update security policies |  |  | C | A/R | C |  | C |  | C |  | C | I |
| 7 | Approve security policies |  |  | A/R | C |  |  |  |  |  |  | C |  |
| 8 | Keep the asset inventory current |  |  |  | C | A |  | R |  |  |  | C |  |
| 9 | Grant access to a system |  |  |  |  |  |  | R | C |  |  | A |  |
| 10a | Tell IT about a leaver on their last day |  |  |  |  |  |  | I | A/R |  |  |  |  |
| 10b | Remove a leaver's access (see note 2) |  |  |  | I |  |  | A/R |  |  |  | I |  |
| 11 | Run the quarterly access review |  |  | I | A |  |  | R |  |  |  | R |  |
| 12 | Patch systems and dependencies |  |  | I | C | A | R | R |  |  |  |  |  |
| 13 | Respond to a security incident |  | I | I | A/R | C | R | R |  | C |  |  |  |
| 14 | Report a personal data breach to regulators (NDPC, EU) |  | C |  | C |  |  |  |  | A/R |  | C |  |
| 15 | Report a cyber incident to ngCERT |  | I |  | A/R |  |  |  |  | C |  |  |  |
| 16 | Assess a new supplier |  |  |  | R | C |  |  |  | C |  | A |  |
| 17 | Run security awareness training |  |  | I | A/R |  |  |  | R | C |  |  | I |
| 18 | Send the quarterly security report to the board | I | C | C | A/R |  |  |  |  |  |  |  |  |
| 19 | Answer a customer's security questionnaire |  | I |  | A/R | C |  |  |  | C | R |  |  |

## Notes on two rows

1. **Row 4.** The accountable person is the approver that the risk appetite names for the risk's
   category: the CEO for customer data, legal and regulatory, and reputation; the CTO for
   availability and technology change; the CFO for financial loss; and the supplier's business
   owner for suppliers (the CEO where the supplier handles customer data). That keeps one A for each
   risk. The system owner prepares the acceptance and records it in the risk register. Nobody
   approves an acceptance they prepared: in that case the approver's line manager approves it, and
   for an executive that is the CEO (rule 5).
2. **Row 10b.** IT removes the access and owns the result. The independent check comes after the
   work, so it is not a C: each month the security lead checks every leaver on the Head of People's
   list against the account state, meaning the account disabled or deleted in the identity provider,
   or the system's own access list or removal log. An IT ticket alone is not evidence (KPI measure
   7). The quarterly access review (row 11) is the backstop.
