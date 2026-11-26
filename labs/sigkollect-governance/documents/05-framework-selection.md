# Framework selection

This document compares three frameworks against SigKollect's situation and records the choice.

## Laws, standards and frameworks: three different things

| Type                      | What it is                                                                                           | Choice?                | SigKollect examples                             |
| ------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------- |
| **Law or regulation**     | Mandatory. Breaking it has legal consequences                                                        | No choice              | NDPA 2023, GDPR, the Cybercrimes Act, CBN rules |
| **Contractual standard**  | Mandatory because a contract says so                                                                 | No choice once signed  | PCI DSS (through the card processor)            |
| **Standard or framework** | A model for building and measuring a programme. Voluntary unless a customer or regulator asks for it | **This is the choice** | ISO/IEC 27001, NIST CSF 2.0, CIS Controls       |

The framework does not replace the laws. It is the structure SigKollect uses to meet them, and the
yardstick it measures itself against.

## The candidates

|               | ISO/IEC 27001:2022                                                                                            | NIST Cybersecurity Framework 2.0                                   | CIS Critical Security Controls v8.1                                                     |
| ------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| From          | ISO and IEC (international)                                                                                   | NIST (US government agency)                                        | Center for Internet Security (non-profit)                                               |
| What it is    | A standard for an information security management system (ISMS): clauses 4 to 10, plus 93 controls in Annex A | Six functions: Govern, Identify, Protect, Detect, Respond, Recover | 18 technical controls, ordered by priority, in three implementation groups (IG1 to IG3) |
| Certification | Yes, by an accredited certification body                                                                      | No. Self-assessment only                                           | No. Self-assessment only                                                                |
| Cost to read  | The standard is sold. Certification audits cost extra                                                         | Free                                                               | Free (registration)                                                                     |
| Strongest at  | Governance, risk management, proving it to customers                                                          | Structure and communication, a plain map of the whole programme    | Concrete technical safeguards that engineers can build                                  |
| Source        | iso.org/standard/27001                                                                                        | nist.gov/cyberframework                                            | cisecurity.org/controls                                                                 |

## Criteria and scores

Each framework is scored from 1 (poor fit) to 3 (good fit) for SigKollect. Each criterion has a
weight from 1 (nice to have) to 3 (essential). Weighted score = weight × score. On cost and effort,
the cheaper and lighter framework is the better fit, so it scores higher.

| #   | Criterion                               | Why it matters for SigKollect                                                       | Weight | ISO 27001 | NIST CSF 2.0 | CIS Controls |
| --- | --------------------------------------- | ----------------------------------------------------------------------------------- | ------ | --------- | ------------ | ------------ |
| 1   | Answers the EU merchant's questionnaire | The trigger for the whole programme. What evidence does a large EU customer accept? | 3 | 3 | 2 | 2 |
| 2   | Can be certified                        | A certificate answers many future questionnaires at once                            | 2 | 3 | 1 | 1 |
| 3   | Cost                                    | 150 people, about $6 million revenue, no security budget yet                        | 2 | 1 | 3 | 3 |
| 4   | Effort to start                         | No security lead until April 2027, one consultant now                               | 3 | 1 | 2 | 3 |
| 5   | Covers governance and risk              | The charter, the risk appetite and the risk register                               | 3 | 3 | 2 | 1 |
| 6   | Gives engineers concrete controls       | E-1 to E-5 were technical failures                                                  | 2 | 2 | 1 | 3 |
| 7   | Helps with Nigerian rules               | R-1 to R-3: the NDPA, the CBN framework, the Cybercrimes Act                        | 1 | 2 | 2 | 2 |
| 8   | Fits the charter's 2027 targets         | Objectives a to h, February to April 2027                                           | 3 | 2 | 3 | 2 |
|     | **Weighted total**                      |                                                                                     |        | **41** | **39** | **40** |

## Decision

The three totals are within 2 points, so the totals alone do not decide. The tie-breaker is
SigKollect's situation: **ease of starting and completing the work comes before certification.
Certify later.**

| Role | Framework | Its job |
|---|---|---|
| Primary | NIST Cybersecurity Framework 2.0 | Structures the whole programme and the answers to customer questionnaires |
| Technical baseline | CIS Critical Security Controls v8.1, Implementation Group 1 | Tells engineers how to close the gaps behind E-1 to E-5 |
| Later target | ISO/IEC 27001:2022 | Certification, once the programme has run under a security lead |

**Why.** The CSF Govern function gives a structure for the charter, the risk appetite and the risk
register. Both frameworks are free and light to start, which fits a company with no security
budget and no security lead until April 2027. The CSF points to the CIS Controls for the "how", so
the two fit together and each charter objective maps to one of them.

**Rejected.**

- *ISO/IEC 27001 now:* the highest total (41), but the heaviest start and a paid standard. A
  certificate proves a management system that has run for a while. Today SigKollect would only
  certify paperwork.
- *CIS Controls alone:* fast to start, but weak on governance. The charter, the appetite and the
  register would have no structure.

**Revisit when:**

- the security lead is in post and the CSF and CIS baseline is running: start ISO/IEC 27001
  certification;
- a key customer or the card processor makes an ISO/IEC 27001 certificate a contract condition;
- the CBN or the NDPC names a framework that payment service providers must follow. Not yet
  checked against the primary texts.
