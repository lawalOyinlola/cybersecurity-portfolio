# Results matrix

Every case, every phase. Codes are the status the client received through the
listener under test. **403** is a WAF block. `det.` means the WAF detected the
payload (would block at engine On) but the phase was detection-only. A plain
code is the application's own response with the WAF adding nothing.

Generated from the raw `results.jsonl` and `audit.json` for each phase; not
hand-entered.

| Case | Class | Baseline (no WAF) | Detection PL1 | Block PL1 tuned | Block PL2 |
| --- | --- | --- | --- | --- | --- |
| S1 | sqli | app 400 | 400 | 400 | 400 |
| S2 | sqli | app 400 | 400 | 400 | 400 |
| S3 | sqli | app 400 | det. | **403** | **403** |
| S4 | sqli | app 400 | det. | **403** | **403** |
| S5 | sqli | app 400 | det. | **403** | **403** |
| S6 | sqli | app 400 | det. | **403** | **403** |
| X1 | xss | app 200 | det. | **403** | **403** |
| X2 | xss | app 200 | det. | **403** | **403** |
| X3 | xss | app 200 | det. | **403** | **403** |
| X4 | xss | app 201 | det. | **403** | **403** |
| X6 | xss | app 201 | det. | **403** | **403** |
| P1 | traversal | app 400 | 400 | 400 | 400 |
| P3 | traversal | app 404 | det. | **403** | **403** |
| P4 | traversal | app 404 | 404 | 404 | 404 |
| C1 | cmdi | app 400 | 400 | 400 | 400 |
| C2 | cmdi | app 400 | 400 | 400 | 400 |
| C3 | cmdi | app 201 | det. | **403** | **403** |
| C5 | cmdi | app 201 | det. | **403** | **403** |
| A1 | auth | app 401 | 401 | 401 | 401 |
| A2 | auth | app 401 | 401 | 401 | 401 |
| A5 | auth | app 400 | 400 | 400 | 400 |
| A6 | auth | app 400* | 400 | 400 | 400 |
| I1 | idor | app 404 | 404 | 404 | 404 |
| I2 | idor | app 404 | 404 | 404 | 404 |
| I3 | idor | app 404 | det.† | 404 | 404 |
| I5 | idor | app 200 | 200 | 200 | 200 |

\* A6 is rejected 400 by the application (invalid email address) through the WAF
listener in every phase. On the no-WAF control leg the same probe returned 429
in the baseline and detection runs, because earlier login cases in the same run
had already exercised the application's throttler. The WAF verdict is
unaffected either way: no CRS rule fired on A6 at any paranoia level.

† I3 is the one case where the untuned WAF returned 403 on an attack. That block
was not attack detection: it was rule 911100 (method enforcement) firing on the
PATCH verb, the same misfire that produced the N8/N9 false positives below. The
exclusion removed it, and what actually stops I3 in every phase is the
application's tenant isolation (404). Counting it as WAF coverage would be
crediting the WAF for blocking an attack it cannot see, for a reason unrelated
to the attack.

## Normal traffic: false positives

Legitimate requests that must not be blocked. `403 FP` is a false positive.
The untuned column shows the method-enforcement problem; the tuned column
shows the exclusion fixing it; PL2 shows the two content false positives that
a higher paranoia level introduces for no gain in coverage.

| Case | Legitimate request | PL1 untuned | PL1 tuned | PL2 tuned |
| --- | --- | --- | --- | --- |
| N1 | strong password with specials | pass | pass | **403 FP** |
| N2 | signed GPS-ingest webhook | pass | pass | pass |
| N3 | vehicle name O'Brien & Co. | pass | pass | pass |
| N4 | history with ISO timestamps | pass | pass | pass |
| N5 | register orgName A&B <Logistics> | pass | pass | **403 FP** |
| N7 | driverName unicode "José Škoda" | pass | pass | pass |
| N8 | legit PATCH own vehicle (method FP) | **403 FP** | pass | pass |
| N9 | legit PATCH own user (method FP) | **403 FP** | pass | pass |

False-positive totals: PL1 untuned 2 (both method enforcement), PL1 tuned 0,
PL2 tuned 2 (both content, on a strong password and a punctuated business
name).

