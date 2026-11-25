# Governance KPIs

## Purpose

These measures show whether the security programme works. Each one answers a question that the
steering committee or the board asks. A number that nobody acts on is not a KPI, so each measure
has a target, an owner and a meeting that looks at it.

## KPI and KRI

- A **KPI** (key performance indicator) measures whether the programme is doing its work. Example:
  the share of leavers whose access was removed on time.
- A **KRI** (key risk indicator) warns that a risk is close to its limit. The tolerances in the risk
  appetite are KRIs. Example: minutes of unplanned downtime this month, against the 30-minute limit.

This document has both. The "Type" column says which.

## Baseline

SigKollect measures none of these today. The first measurement, in January 2027, is the baseline.
Targets below are for the charter dates (28 February to 30 April 2027), then for ongoing operation.

## The measures

| # | Measure | How it is calculated | Target | Type | CSF function | Source | Owner | Seen by |
|---|---|---|---|---|---|---|---|---|
| 1 | Charter objectives on track | Objectives a to h that are green ÷ 8 | 8 of 8 green by 30 April 2027 | KPI | Govern | Objectives tracker | Security lead | Steering committee monthly, board quarterly |
| 2 | Risks above the appetite without a decision | Risks above the appetite that have waited more than 30 days for a board decision | 0 | KRI | Govern | Risk register | Security lead | Steering committee monthly, board quarterly |
| 3 | Core policies approved and in date | Approved policies with a review date in the future ÷ 4 (information security, access control, acceptable use, incident response) | 4 of 4 by 30 April 2027 (objective c) | KPI | Govern | Policy register | Security lead | Steering committee monthly |
| 4 | Suppliers assessed | Suppliers with access to SigKollect systems or data that have a current assessment ÷ all such suppliers | 100% (risk appetite row 5) | KPI | Govern | Supplier list | Security lead | Risk review monthly, steering committee quarterly |
| 5 | Systems with a named owner | Systems in the asset inventory with a named owner ÷ all systems in the inventory | 100% by 31 March 2027 (objective b) | KPI | Identify | Asset inventory | IT and Systems Lead | Risk review monthly |
| 6 | MFA on systems with customer data | Users with MFA on systems that hold identity, bank or card data ÷ all users of those systems | 100% (risk appetite row 1) | KRI | Protect | Identity provider reports | IT and Systems Lead | Risk review monthly, board quarterly |
| 7 | Leaver access removed on time | Leavers whose 5-working-day deadline fell this month and whose access was removed by then in every system where they held an account, shown by a timestamped removal record ÷ all leavers whose deadline fell this month. Leavers still inside their 5 days are reported separately as pending | 100% (objective e) | KPI | Protect | Head of People leaver list. Proof: timestamped removal records (the identity provider's audit log, and the removal log of each system with its own accounts) dated by the deadline. Account state and IT tickets back this up, but do not prove when access was removed | Security lead | Risk review monthly |
| 8 | Access review complete | Systems with customer or payment data reviewed this quarter ÷ all such systems | 100% each quarter (RACI row 11) | KPI | Protect | Access review records | Security lead | Steering committee quarterly |
| 9 | Critical vulnerabilities fixed on time | Critical vulnerabilities fixed within the target days ÷ all critical vulnerabilities found | 95% within 72 hours if actively exploited, 7 days for internet-facing systems, 14 days for internal systems | KPI | Protect | Scanner and ticket data | CTO | Risk review monthly, steering committee monthly |
| 10 | Training complete | Staff who finished the yearly security awareness training ÷ all staff. New joiners: essentials module before access to customer data or within the first week, full course within 2 months | 95% of staff each year. 100% of new joiners on both new-joiner deadlines | KPI | Protect | Training platform | Head of People | Steering committee quarterly |
| 11 | Suspected incidents reported on time | Suspected incidents that reached the security lead within 1 hour ÷ all suspected incidents | 100% (the governance cadence, part 3) | KPI | Respond | Incident log | Security lead | Incident review, steering committee monthly |
| 12 | Regulator notifications on time | Notifications sent within the legal time limit ÷ notifications required | 100% (risk appetite row 2) | KRI | Respond | Incident log, Compliance records | Head of Compliance | Board quarterly |
| 13 | Unplanned downtime | Minutes of unplanned downtime this month, Checkout and Partner API | 30 minutes or less (risk appetite row 3) | KRI | Recover | Monitoring | CTO | Steering committee monthly |
| 14 | Customer questionnaires answered on time | Questionnaires answered within 15 working days ÷ all questionnaires received | 100% (risk appetite row 7, objective g) | KPI | Govern | Sales request log | Security lead | Steering committee monthly, board quarterly |

## What the board sees

The board report has 5 slides, so the board sees only measures 1, 2, 6, 12 and 14. These answer
the board's questions: is the programme on track, is any risk waiting for us, is customer data
protected, are we meeting the law, and are customers getting answers. The other measures stay with
the steering committee and the risk review.

## Rules for the measures

1. Each measure has one owner. The owner reports the number. The owner does not have to be the
   person who fixes it.
2. A measure that misses its target for two months in a row goes to the steering committee as a
   decision, not as an update.
3. A KRI that passes its tolerance is a risk outside the appetite. It follows governance cadence
   part 3: the CEO hears within 1 working day.
4. Every number links to its source. A number with no source is not reported.
5. The steering committee reviews this list each year, and when the security lead is appointed.

## Notes on three measures

1. **Measure 9.** For most vulnerabilities, the clock starts when the vulnerability is found or a
   fix is published, whichever is later. Where no fix exists, a documented workaround approved by the
   security lead counts as fixed. A vulnerability that is being actively exploited is different: its
   72 hours start when it is found, whatever the system and whether or not a fix exists. If neither a
   fix nor an approved workaround is in place by then, it is a risk outside the appetite and goes to
   the CEO (governance cadence, part 3).
2. **Measure 10.** New joiners finish a short essentials module (spotting phishing, reporting an
   incident within 1 hour, handling customer data) before they get access to customer data, or
   within their first week, with no exceptions. They finish the full course within 2 months. New
   joiners are the easiest phishing targets (E-4), so the important part comes first.
3. **Detect has no measure yet.** SigKollect cannot measure detection today (E-5). A measure with no
   way to collect it would show red in every report and tell the board nothing new. A Detect
   measure, such as the time from an attack starting to an alert, is added when the detection work
   exists, and at the latest at the first yearly review of this list.
