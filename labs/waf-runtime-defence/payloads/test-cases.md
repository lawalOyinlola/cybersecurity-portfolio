# Payload set and expected behaviour

Seven attack classes against real routes of the target, six of which were
carried through to measurement (see "What was actually executed" at the end).
Each phase runs the same executed set unchanged, so the phases are directly
comparable.

For every case four things are recorded:

- **blocked**: WAF returned 403 (Phase 2/3 only; Phase 1 has no WAF)
- **passed**: request reached the application
- **false positive**: a legitimate request the WAF flagged
- **application response**: what the app itself did, independent of the WAF

The fourth column is the point of the exercise. A payload the WAF blocks that
the application would have rejected anyway (bad UUID, parameterised query,
escaped output, validation pipe) tells us the WAF is adding defence-in-depth,
not primary defence. A payload that only the WAF stops, or that neither stops,
is where the real signal is.

Routes are hit through the single lab origin `https://lab.localhost:PORT`,
`/api/*` path-routed to NestJS, everything else to Next.js.

---

## Target facts that shape expectations

These are properties of the application, established by reading its code, that
predict the "application response" column before the WAF is involved:

- **Prisma parameterises every query.** No string-built SQL. Union/boolean/
  time SQLi should therefore change nothing in the application: the payload is
  bound as a literal value, not interpreted.
- **`ParseUUIDPipe` guards `:id` routes** (vehicles, users, devices). A
  non-UUID id is rejected with 400 by the pipe before any database call. Most
  path-parameter injection therefore dies at the DTO layer.
- **React escapes output by default.** Reflected XSS delivered as a query
  string is escaped when rendered, so stored/DOM sinks are the only realistic
  XSS surface, not reflected.
- **`ValidationPipe({ whitelist: true })` strips unknown fields** and enforces
  DTOs. Login/register/webhook bodies are typed; extra keys are dropped.
- **The GPS-ingest webhook is shared-secret authenticated** (`x-webhook-secret`,
  timing-safe compare) and its body is a typed DTO with `@IsLatitude`,
  `@IsLongitude`, numeric bounds. Malformed coordinates are a 400 from the app.
- **The app has its own throttler** (`CustomThrottlerGuard`) and CSRF
  middleware. Rate and CSRF findings must be read against those, not as if the
  app were bare.

The consequence, stated up front so the Phase 1 baseline is not a surprise:
**the framework already handles most of the classic payload classes.** The
WAF's value has to be argued on what it adds beyond that, plus the classes the
framework does not address (IDOR, business logic) and the ones it addresses
only partially.

---

## Class 1: SQL injection

Target: `GET /api/vehicles/:id`, `GET /api/vehicles/:id/history?from=&to=`,
login body.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| S1 | `1' OR '1'='1` | vehicles/:id | 400 ParseUUIDPipe (not even a query) |
| S2 | `1 UNION SELECT null,null--` | vehicles/:id | 400 ParseUUIDPipe |
| S3 | `1;WAITFOR DELAY '0:0:5'--` | history ?from | 400/200, bound as literal, no delay |
| S4 | `' OR 1=1--` | login email | 400 IsEmail (invalid address) |
| S5 | `admin'--` | login email | 400 IsEmail |
| S6 | `1' AND SLEEP(5)--` | history ?to | no delay; Prisma binds it |

Expectation: the app neutralises all six on its own. The interesting question
is how many the WAF *also* flags, and whether any WAF flag lands on a *valid*
UUID that merely contains a substring CRS dislikes.

## Class 2: Cross-site scripting

Target: reflected via query string to the frontend; stored via `name` fields
in authenticated create/update bodies.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| X1 | `<script>alert(1)</script>` | `/?q=` reflected | React escapes on render |
| X2 | `<img src=x onerror=alert(1)>` | `/?q=` reflected | escaped |
| X3 | `<svg/onload=alert(1)>` | `/?q=` reflected | escaped |
| X4 | `"><script>alert(1)</script>` | vehicle `name` (stored) | stored as text; escaped on render |
| X5 | `javascript:alert(1)` | vehicle `driverName` | stored; not an executable sink |
| X6 | `<script>alert(1)</script>` | register `firstName` | validation + escaped |

Expectation: React defeats reflected XSS unaided. Stored payloads persist as
inert text. The WAF's contribution is blocking them in transit, which matters
only if a future template rendered one unescaped.

## Class 3: Path traversal

Target: any path parameter, plus the public trip token.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| P1 | `../../../../etc/passwd` | vehicles/:id | 400 ParseUUIDPipe |
| P2 | `..%2f..%2f..%2fetc%2fpasswd` | vehicles/:id | 400 |
| P3 | `%252e%252e%252fetc%252fpasswd` | public/trip/:token | 404 token not found |
| P4 | `....//....//etc/passwd` | public/trip/:token | 404 |
| P5 | `..\..\..\windows\win.ini` | vehicles/:id | 400 |

Expectation: no file read is reachable; the app has no file-serving route that
takes user path input. This class tests the WAF against an app that is not
actually vulnerable to it, which is itself a documented result.

## Class 4: Command injection

Target: same parameters. The app shells out nowhere on these paths, so this is
another "not actually vulnerable" class measured against the WAF.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| C1 | `;cat /etc/passwd` | vehicles/:id | 400 ParseUUIDPipe |
| C2 | `` `id` `` | vehicles/:id | 400 |
| C3 | `$(whoami)` | vehicle `name` (stored) | stored as literal text |
| C4 | `\| ls -la` | history ?from | bound as literal |
| C5 | `; ping -c 5 127.0.0.1` | register `organizationName` | stored/validated text |

Expectation: nothing executes. C2 (backtick) is the one to watch: the
Checkpoint 1 smoke test showed CRS PL1 let a bare backtick through. Confirm
whether that holds inside a real parameter.

## Class 5: Authentication bypass and JWT manipulation

Target: `POST /api/auth/login`, and any `Authorization: Bearer` route.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| A1 | `alg:none` forged JWT | Bearer on /api/vehicles | 401 signature check |
| A2 | valid JWT, tampered `role` claim | Bearer | 401 signature invalid |
| A3 | valid JWT, tampered `sub` (other user id) | Bearer | 401 signature invalid |
| A4 | expired JWT | Bearer | 401 |
| A5 | login with `password` as array `[]` | login body | 400 ValidationPipe |
| A6 | login with `email` object `{"$ne":null}` | login body | 400 IsEmail (no Mongo here) |

Expectation: JWT integrity is the app's job and it does it (HS256, secret
verified). The WAF sees well-formed requests here and mostly should not fire.
A6 is a NoSQL-injection reflex that does not apply to a Prisma/MariaDB stack;
recorded to show the class was considered and is N/A.

## Class 6: IDOR / BOLA (the class no WAF addresses)

Target: cross-tenant access. Tenant A owner tries to read tenant B's records.
Fixed seed UUIDs are used so discovery is not part of the test; authorisation
is.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| I1 | GET tenant B vehicle id | Bearer=A owner | 404/403 org scoping |
| I2 | GET tenant B vehicle history | Bearer=A owner | 404/403 |
| I3 | PATCH tenant B vehicle | Bearer=A owner | 404/403 |
| I4 | GET tenant B user id | Bearer=A owner | 404/403 |
| I5 | GET own tenant vehicle (control) | Bearer=A owner | 200 |

Expectation: **every one of these is a perfectly well-formed request.** No CRS
signature can distinguish I1 from I5; they differ only in whose data the id
belongs to. The WAF passes all of them. Whether the *application* enforces
tenant scoping is what decides I1-I4, and that is measured here as the app's
own control, entirely outside the WAF. This is the section that makes the
"compensating control, not a fix" argument concrete.

## Class 7: Enumeration and rate abuse

Target: `POST /api/auth/login`, `POST /api/auth/forgot-password`.

| # | payload | delivery | expected app response |
|---|---------|----------|----------------------|
| E1 | 30x rapid login, wrong password | login | app throttler 429 after limit |
| E2 | login existing vs absent email, compare timing/message | login | should not distinguish (user enum) |
| E3 | forgot-password existing vs absent email | forgot-password | should return same response |
| E4 | 30x forgot-password, one email | forgot-password | throttled |

Expectation: rate limiting is the app's throttler, not the WAF, at PL1. The
finding is whether the WAF adds anything to abuse prevention or whether that is
entirely the application's job. User-enumeration (E2/E3) is a logic property no
signature WAF touches.

---

## Normal-traffic set (false-positive measurement, Phase 2/3)

Legitimate requests that must NOT be blocked. These are where CRS on a JSON API
earns its reputation for false positives.

| # | request | why it might trip CRS |
|---|---------|----------------------|
| N1 | login with a strong password full of specials `P@ss'w0rd!";--` | quotes and comment marker look like SQLi |
| N2 | GPS-ingest webhook, valid signed body, GPS coord array | numeric arrays, JSON depth |
| N3 | vehicle create, `name` = `O'Brien Haulage & Co.` | apostrophe + ampersand |
| N4 | vehicle history with ISO timestamps `from=2026-01-01T00:00:00Z` | colons, encoded chars |
| N5 | register, `organizationName` = `A&B <Logistics>` | angle brackets, ampersand |
| N6 | long valid JWT in Authorization header (many segments) | length and base64 entropy |
| N7 | driverName with unicode `José Škoda` | non-ASCII |
| N10 | bulk position POST, 40-point coordinate array | large numeric JSON body |

Two further cases were added once the blocking phases began, after rule 911100
turned out to be the real false-positive source. They carry no attack content
at all; they exist purely to exercise the REST verbs CRS blocks by default:

| # | request | why it might trip CRS |
|---|---------|----------------------|
| N8 | legitimate PATCH of the caller's own vehicle | CRS 911100 blocks PATCH by default |
| N9 | legitimate PATCH of the caller's own user profile | same |

Each false positive found here becomes a targeted Phase 3 exclusion, documented
with the rule id it fired and why removing that check for that parameter is
safe.

---

## What was actually executed

This document is the plan, written before the runs. The measured set is a
subset of it, and the two are kept distinct on purpose: the results in
[../evidence/results-matrix.md](../evidence/results-matrix.md) cover exactly the
cases below and no others.

**Executed, every run of all three phases (26 attack cases, six classes):** S1-S6, X1-X4, X6,
P1, P3, P4, C1-C3, C5, A1, A2, A5, A6, I1-I3, I5.

**Executed (normal traffic):** N1-N5, N7 from
detection onward; N8 and N9 from the blocking phases, where they were added.

**Planned but not executed, and why:**

- **X5, P2, P5, C4, A3, A4, I4** were duplicate deliveries of a class already
  decided by an earlier case in the same class (the same payload family through
  the same parameter and the same application control). They would have added
  rows, not signal.
- **N6 and N10** were dropped for the same reason: every authenticated case in
  the suite already carries a long valid JWT in the `Authorization` header, and
  N2 already puts a coordinate payload through the WAF's body inspection.
- **Class 7 in full (E1-E4)** was scoped out of the measurement. Rate limiting
  and user enumeration are properties of the application's throttler and of its
  response wording, not of any CRS signature at PL1, so the WAF-versus-control
  comparison that the rest of the suite rests on has nothing to measure here.
  Running them would also have flooded the application-disposition column of
  every other case with 429s from the shared login route. The class is kept in
  this document because the reasoning is the result: abuse prevention on this
  application is the app's job, and a paranoia-level-1 WAF does not change that.

Twenty-six attack cases across six measured classes is therefore the figure the
writeup uses throughout.
