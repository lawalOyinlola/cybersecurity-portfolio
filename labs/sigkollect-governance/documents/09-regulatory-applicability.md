# Regulatory applicability assessment

This assessment checks which laws, regulations and contractual standards apply to SigKollect, against
their primary texts. Each row is revisable and has a review date.

**SigKollect is fictional.** This is an analysis for a lab, not legal advice. No row says that
SigKollect is "compliant". Where a result depends on facts a real company would have to confirm, or
on a reading a regulator could dispute, the row says so and names the lawyer it needs.

## Method

1. **Jurisdiction first.** Answer the four gate questions before reading any rule.
2. **Primary sources first.** Read the text of the law, regulation or standard. Use a law-firm
   summary only where the primary text could not be found, and mark the row "secondary only".
3. **One result per rule:** Applies, Likely applies, Unclear, Not applicable, or Out of scope (a
   programme decision, not a legal finding).
4. **Confidence:** High (the primary text answers it), Medium (the text answers it, but a fact about
   SigKollect is assumed), Low (secondary sources only, or the sources conflict).

Sources were read on 25 November 2026. Laws change. Each row is reviewed by its review date.

## Jurisdiction gate

| Question | Answer for SigKollect | What it decides |
|---|---|---|
| Where is the entity incorporated? | Nigeria (SigKollect Limited, Lagos) | Nigerian law applies by default. The NDPC, the CBN and ngCERT are the home regulators |
| Where do the people whose data it holds live? | Nigeria and the EU | Nigerian data law, and the GDPR question (R-4). No US or UK customers, so US and UK rules are not assessed |
| Business to business, or to consumers? | Both. Merchants are businesses, but SigKollect also processes the personal data of sole traders, small-business owners and the people who pay merchants | Consumer data is in scope even though the customers are businesses |
| How is it distributed? | Web (Checkout, Business) and an API. No app store apps | App store rules: not applicable |

## Summary

| # | Rule | Result | Confidence | Source type | Owner at SigKollect | Review by |
|---|---|---|---|---|---|---|
| R-1 | Nigeria Data Protection Act 2023 and the GAID 2025 | **Applies.** SigKollect is a data controller of major importance, at the highest level (UHL) | High | Primary | Head of Compliance (DPO) | 30 June 2027 |
| R-2 | CBN Risk-Based Cybersecurity Framework 2024 | **Unclear.** The 2024 framework covers banks only. The 2018 framework it replaced also covered payment service providers. What covers SigKollect now is not settled | Medium | Primary | Head of Compliance | 31 March 2027 |
| R-3 | Cybercrimes Act 2015, amended 2024, section 21 | **Applies.** Report cyber incidents to ngCERT, through the sector CERT or SOC, immediately. Not reporting within 72 hours of detection is an offence | High | Primary | Security lead | 31 March 2027 |
| R-4 | EU GDPR | **Likely applies** (Article 3(2)), and with it an EU representative (Article 27) | Medium | Primary | Head of Compliance | 31 March 2027 |
| R-5 | PCI DSS v4.0.1 | **Applies, by contract, as a service provider**, not as a merchant | Medium | Primary | CTO | 31 March 2027 |
| R-6 | EU DORA | **Not applicable** to SigKollect directly | Medium | Primary (mirror) | Head of Compliance | 30 June 2027 |
| R-7 | EU AI Act | **Out of scope** for this phase (programme decision) | n/a | n/a | Security lead | Before Litir Triage is used on real data |

## R-1 · Nigeria Data Protection Act 2023 and the GAID 2025

**Result: Applies. Confidence: High.**

What the primary text says:

- **Scope.** The Act applies where the controller or processor is "domiciled in, resident in, or
  operating in Nigeria" (NDPA s.2(2)(a)). SigKollect is incorporated in Lagos.
- **Major importance.** The GAID's Schedule 7 (the NDPC Guidance Notice on registration) designates as
  of major importance any controller that processes personal data "as an organisation or a service
  provider" in listed sectors, including **Financial** and **E-Commerce**, or that processes the data
  of more than 200 data subjects in six months. It places **"Payment gateway service providers"** and
  **"Fintechs"** in the **Ultra-High Level (UHL)** category.
- **What that brings:**
  - register with the NDPC (s.44(1));
  - designate a Data Protection Officer "with expert knowledge of data protection law and practices"
    (s.32(1)). The DPO may be an employee or an external party (s.32(2));
  - file Compliance Audit Returns with the NDPC (GAID Article 10 and Schedule 2).
- **Breach reporting.** A controller must notify the NDPC "within 72 hours of becoming aware of a
  breach which is likely to result in a risk to the rights and freedoms of individuals" (s.40(2)).
  Where the risk to a person is high, the controller must tell that person "immediately" (s.40(3);
  GAID Article 33(3)). GAID Article 33(2) treats a breach as high risk where the person "may become a
  victim of fraud, identity theft or exposure of sensitive personal data". BVN, NIN and bank details
  fit that description.
- **Phases and immediate notice.** Where the information cannot all be given at once, it "may be
  provided in phases without undue delay" (s.40(9)), so a first notification does not wait for every
  detail. GAID Article 33(4) also asks for "immediate information" to the NDPC and other relevant
  authorities where it may help contain imminent breaches on a national scale, where containment measures may be necessary at national, sectoral or individual level, or "where it may affect members of the general public".
- **Processors.** A processor (such as a SaaS supplier) must tell SigKollect on becoming aware of a
  breach (s.40(1)).
- **Automated decisions.** A person has the right not to be subject to a decision "based solely on
  automated processing" with legal or similarly significant effects (s.37(1)), with exceptions in
  s.37(2), including a contract.
- **Cross-border transfer.** Data may leave Nigeria only on a basis in s.41 to s.43, and the basis must
  be recorded (s.41(2)). SigKollect runs on Azure. Where its Azure regions are is not yet recorded.

What it means for the pack:

- The charter says the Head of Compliance holds data protection duties "until a data protection
  officer is named". Under s.32(1), a DPO is required, not optional. See decision 1.
- The AI use policy (sections 6 and 7) already sends legal questions to the Head of Compliance. The
  NDPA s.37 reference now has a primary source, so the policy's "not checked" note can be removed.
- Not checked: the 2024 court ruling on the major-importance guidance that secondary sources mention. The
  GAID (March 2025) still reproduces the guidance as Schedule 7.

## R-2 · CBN Risk-Based Cybersecurity Framework

**Result: Unclear. Confidence: Medium.**

What the primary text says:

- The 2024 framework (circular BSD/DIR/PUB/LAB/017/008, 31 May 2024, in force 1 July 2024) "shall
  apply to ... Commercial banks, Merchant banks, Non-Interest banks and Payment Service banks".
- It "replaces the Risk-based Cybersecurity Framework and Guidelines for Deposit Money Banks and
  Payment Service Providers issued in October 2018".
- Banks covered by it must report cyber incidents to the CBN "not later than 24 hours" after
  detection.

What it means for SigKollect:

- SigKollect is a payment service provider (a payment gateway), not a bank. The 2024 framework does
  not name it.
- The 2018 framework did name payment service providers, and the 2024 framework replaced it. So
  whether the 2018 framework still binds payment service providers, or whether a separate CBN
  directive now covers them, cannot be answered from these texts.
- SigKollect's licence category is not yet recorded.

Open questions, for a Nigerian payments lawyer or the CBN's Payments System Management Department:

1. Which licence category does SigKollect hold?
2. Which CBN cybersecurity framework or directive applies to that category today?
3. Does any CBN rule set an incident reporting time for that category?

Until answered, the programme treats the 2024 framework as **good practice, not an obligation**. Its
structure (board oversight, a CISO, a risk management system, metrics) matches what this pack sets up.

## R-3 · Cybercrimes Act 2015, amended 2024, section 21

**Result: Applies. Confidence: High.**

What the primary text says (the 2015 Act and the 2024 Amendment Act, as published in WIPO Lex):

- Section 21(1): a person or institution "who operates a Computer System or a Network, whether
  Public or Private, shall immediately inform" the National CERT Coordination Center of "any
  attack, intrusion and other disruption liable to hinder the functioning of another Computer System
  or Network". Section 3(a) of the 2024 Amendment Act adds the route: "through their respective
  sectoral CERTs or sectoral Security Operations Centres (SOC)".
- Section 21(3): a person who fails to report "within 7 days of its occurrence" commits an offence.
  Section 3(b) of the 2024 Amendment Act replaces those words with "72 hours of its detection". The
  penalty is denial of internet services and a mandatory fine of ₦2,000,000 paid into the National
  Cyber Security Fund.

What it means for SigKollect:

- SigKollect operates computer systems and networks, so section 21 reaches it.
- There are two duties, not one. The duty is to report **immediately** (s.21(1)). The 72 hours from
  **detection** (s.21(3)) is the point after which not reporting is an offence. It is not a deadline
  to plan to.
- The clock starts at detection, not at occurrence. An earlier draft of this assessment used
  occurrence as the stricter reading, because law-firm summaries disagreed. The primary text settles
  it.
- Open: which sectoral CERT or SOC receives reports from a payment service provider. A law-firm
  note names the Nigeria Financial CERT (NigFinCERT) as one sectoral CERT. Not checked with a primary
  source.

Sources: the two Acts, read through WIPO Lex (primary). Earlier, and for the NigFinCERT name: PLAC
(placng.org), Aluko & Oyebode (aluko-oyebode.com), Templars (templars-law.com), TechHive Advisory
(techhiveadvisory.africa), all secondary.

## R-4 · EU General Data Protection Regulation

**Result: Likely applies. Confidence: Medium.**

What the primary text says:

- Article 3(2) applies the GDPR to a controller or processor "not established in the Union" where the
  processing relates to "the offering of goods or services ... to such data subjects in the Union".
- Article 27(1): where Article 3(2) applies, the controller or processor "shall designate in writing a
  representative in the Union". Article 27(2)(a) exempts processing that is "occasional" and
  "unlikely to result in a risk".
- Article 33(1): notify the supervisory authority "without undue delay and, where feasible, not later
  than 72 hours after having become aware" of a breach, unless it is unlikely to result in a risk.
- Article 33(2): a processor tells the controller "without undue delay".
- Article 33(4): where the information cannot all be given at once, it "may be provided in phases
  without undue further delay".

What it means for SigKollect:

- SigKollect offers its services to EU merchants, some of whom are sole traders (natural persons),
  and it processes the data of the people who pay them in the EU. That points to Article 3(2)(a).
- Its processing is regular, not occasional, and includes bank details. The Article 27(2)(a)
  exemption is unlikely to fit. So SigKollect likely needs an EU representative.
- Whether SigKollect is a controller or a processor for each data set (for example, the payer's data
  at Checkout) is not settled. It decides who notifies a breach. See decision 3.
- Not checked: the EDPB Guidelines 3/2018 on territorial scope, which a lawyer would apply here.

Needs an EU data protection lawyer before any real EU processing.

## R-5 · PCI DSS v4.0.1

**Result: Applies, by contract, as a service provider. Confidence: Medium.**

What the primary text says:

- PCI SSC: SAQ D for Service Providers "is the ONLY SAQ option for service providers". All other SAQs
  are for merchants.
- Whether a service provider may self-assess at all is decided by the card brands and the acquirer.
  Many service providers must have a Report on Compliance (ROC) by a Qualified Security Assessor.

What it means for SigKollect:

- The first scoping asked which self-assessment questionnaire follows from how Checkout passes card
  data. That question assumed SigKollect is a merchant. It is not. A payment gateway that handles card
  payments for merchants is a **service provider**, so the merchant SAQs (A, A-EP and others) do not
  apply to it.
- Using a card processor still matters: if no card data enters SigKollect's systems, the scope of the
  assessment is small. But the form is SAQ D for Service Providers or a ROC, whichever the processor
  and the acquirer require.
- PCI DSS is a contract, not a law. The obligation comes from the agreement with the card processor.

Open: ask the card processor which validation it requires (SAQ D for Service Providers or a ROC), and
by when.

Sources: PCI DSS v4.0.1 SAQ D for Service Providers, revision 2 (January 2025), and the PCI SSC blog
"PCI DSS v4: What's New with Self-Assessment Questionnaires" (pcisecuritystandards.org).

## R-6 · EU Digital Operational Resilience Act

**Result: Not applicable to SigKollect directly. Confidence: Medium.**

- DORA Article 2(1) lists the entities in scope, such as credit institutions and "payment
  institutions" under the EU Payment Services Directive. All are EU-authorised financial entities.
  SigKollect holds no EU authorisation.
- Article 2(1)(u) also lists "ICT third-party service providers". DORA reaches them through the
  contracts of the EU financial entities they serve.
- SigKollect's EU customers are merchants, not financial entities. So no DORA terms reach it today.

Revisit if an EU bank, payment institution or other financial entity becomes a customer.

Source: Regulation (EU) 2022/2554, Article 2, read through a mirror of the official text
(digital-operational-resilience-act.com). Not checked against EUR-Lex directly.

## R-7 · EU AI Act

**Result: Out of scope for this phase.** This is a programme decision, not a legal finding. The Litir
Triage lab uses an AI assistant on fictional data only. Assess the AI Act before any AI feature
processes real data or is offered to EU users.

## Test case: E-4, the phishing email

E-4 was reported "the next morning". Nobody assessed whether the attacker used the account or viewed
customer records. Had the assessment found a likely risk, these clocks would have run at once:

| Clock | To whom | Deadline | Starts when | Source |
|---|---|---|---|---|
| NDPA | NDPC | 72 hours; the rest in phases | SigKollect becomes aware of a breach likely to result in a risk | NDPA s.40(2) and (9) |
| GAID immediate notice | NDPC and every other relevant authority | Immediately | Immediate information may help contain imminent breaches on a national scale, containment measures may be necessary at national, sectoral or individual level, or the breach may affect members of the general public. No finding of risk to individuals is needed first | GAID Art 33(4) |
| NDPA, high risk | The affected people | Immediately | Same | NDPA s.40(3), GAID Art 33(3) |
| GDPR, where SigKollect is the controller | EU supervisory authority | Without undue delay and, where feasible, within 72 hours | SigKollect becomes aware, for EU data subjects | GDPR Art 33(1) |
| GDPR, where SigKollect is a processor | The controller (for example, the EU merchant) | Without undue delay | SigKollect becomes aware | GDPR Art 33(2) |
| Cybercrimes Act | ngCERT, through the sectoral CERT or SOC | Immediately. Not reporting within 72 hours is an offence | Detection | s.21(1) and (3), as amended in 2024 |

Which GDPR row applies depends on the controller and processor roles, which are under legal review
(R-4 and action 3 below). Until they are settled, SigKollect prepares both notifications.

What E-4 teaches: every clock starts from awareness or detection, not from the end of the
investigation, and the ngCERT report is due at once, not at 72 hours. So the cadence's internal steps (1 hour to the security lead, 4 hours to the CEO and
Head of Compliance) matter more than any later step. The governance cadence already sets them.

## Actions agreed

1. **Data protection officer:** the Head of Compliance is designated as the DPO under NDPA s.32,
   supported by an external data protection adviser.
2. **Charter:** a new objective h, due 31 March 2027: NDPC registration, the DPO designated, and the
   first Compliance Audit Return filed. See charter version 0.5.
3. **GDPR roles:** the answer to the EU merchant's questionnaire states that the controller and
   processor roles are under legal review. An EU data protection lawyer is engaged in parallel.

## Sources

Primary:

- Nigeria Data Protection Act 2023, Official Gazette No. 119, Vol. 110:
  ndpc.gov.ng/wp-content/uploads/2024/03/Nigeria_Data_Protection_Act_2023.pdf (s.2, 32, 37, 40, 41,
  44, 65)
- NDP Act General Application and Implementation Directive 2025 (NDPC/NDP ACT-GAID/01/2025):
  ndpc.gov.ng/wp-content/uploads/2025/03/NDP-ACT-GAID-2025-MARCH-20TH.pdf (Articles 8, 10, 33;
  Schedule 7)
- CBN Risk-Based Cybersecurity Framework and Guidelines for DMBs and PSBs 2024:
  cbn.gov.ng/Out/2024/BSD/CBN Risk-Based Cybersecurity Framework for DMBs and PSBs_2024.pdf
- Cybercrimes (Prohibition, Prevention, Etc.) Act 2015 (Act No. 17 of 2015), section 21, and the
  Cybercrimes (Prohibition, Prevention, Etc.) (Amendment) Act 2024, section 3: official texts read
  through WIPO Lex (wipo.int/wipolex, records 22696 and 22699). The ngCERT site could not be reached
  from this lab
- Regulation (EU) 2016/679 (GDPR), Articles 3, 27, 33, read through gdpr-info.eu
- Regulation (EU) 2022/2554 (DORA), Article 2, read through digital-operational-resilience-act.com
- PCI DSS v4.0.1 SAQ D for Service Providers, r2, January 2025: docs-prv.pcisecuritystandards.org

Secondary (R-3, used before the primary text was found, and for the sectoral CERT name): placng.org,
aluko-oyebode.com, templars-law.com, techhiveadvisory.africa.
