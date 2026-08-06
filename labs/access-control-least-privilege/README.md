# Access control and least privilege

Two access-control investigations, grouped as one body of work. Both trace an
incident back to a least-privilege failure and map the fix to NIST SP 800-53,
but from opposite directions: one is a scope failure (too much was shared at
once), the other is a lifecycle failure (access that was never revoked).

## The investigations

| # | Investigation | Root cause | Controls mapped |
|---|---|---|---|
| 1 | [Data leak and least privilege](./data-leak-least-privilege/analysis.md) | An entire internal folder shared instead of the one file needed, and never revoked after the meeting | AC-6 (least privilege) |
| 2 | [Orphaned contractor account](./orphaned-account-access-review/analysis.md) | A contractor's Admin account left active nearly four years after the engagement ended | AC-6, AC-2, PS-4, PS-5 |

## What this set demonstrates

- Reading an incident as an access-control failure first, rather than stopping
  at the accidental share or the fraudulent transaction that surfaced it.
- Working familiarity with NIST SP 800-53's access-control and personnel-action
  families, and the judgement to map a concrete failure to the specific control
  that would have prevented it, not the framework in general.
- The two consistent failure modes of least privilege: granting more scope than
  a task requires, and leaving that access in place after the task or the
  relationship that justified it ends. Both investigations recommend fixes on
  both axes, scope and time, rather than treating either alone as sufficient.

Each investigation is written up in full in its own directory, linked in the
table above.