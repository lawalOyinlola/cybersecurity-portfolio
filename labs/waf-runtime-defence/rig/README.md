# WAF runtime defence lab

ModSecurity and the OWASP Core Rule Set in front of OWASP Juice Shop, measured
against a control with the rule engine off. The guide is the lab write-up on
[the portfolio site](https://lawaloyinlola.com/security/labs/waf-runtime-defence); this folder is
everything it runs.

Juice Shop is deliberately vulnerable. Nothing here publishes it: both proxies
bind to `127.0.0.1`, and the target has no published port. Attack only what you own.

## Quick start

```bash
docker compose up -d
./attack/run-phase.sh baseline Off 1 none        # what the app does on its own
./attack/run-all.sh                              # every phase, about 40 seconds
```

Needs Docker with Compose v2, Python 3.9+, curl and jq. Keep the folder inside
your home directory so Docker can share it.

## Layout

```
compose.yml                     juice (target), waf (engine under test), control (engine off)
.env                            not shipped: run-phase.sh writes ENGINE and PARANOIA here (git-ignored)
waf/modsec/                     the exclusions file the WAF loads (run-phase.sh overwrites it)
waf/tuning/                     the tuning options a phase can install
attack/suite.py                 29 requests, each sent to both ports
attack/run-phase.sh             one phase from a clean state
attack/run-all.sh               every phase in order
attack/summarise.py             joins results to the audit log, prints the table
attack/check.py                 pass or fail on a phase's summary
logs/waf/                       the WAF's JSON audit log
evidence/<phase>/               results.jsonl, summary.json, audit.json
```

A phase run rewrites `waf/modsec/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf` and the
`evidence/` folder, so `git status` will show them changed afterwards. Put the exclusions file back with
`git checkout waf/modsec` and keep or discard the evidence as you like.

## Listeners

| URL | What it is |
| --- | --- |
| `http://localhost:8080` | NGINX + ModSecurity + CRS, engine set by the phase |
| `http://localhost:9080` | the same image and config with the engine Off (the control) |

## Phases

| Phase | Engine | Paranoia | Tuning file |
| --- | --- | --- | --- |
| `baseline` | Off | n/a | `none` |
| `detect-pl1` | DetectionOnly | 1 | `none` |
| `block-pl1-untuned` | On | 1 | `none` |
| `block-pl1-excl1` | On | 1 | `excl-1` |
| `block-pl1-tuned` | On | 1 | `tuned` |
| `block-pl1-patched` | On | 1 | `patched` |
| `block-pl2-tuned` | On | 2 | `tuned` |
| `block-pl2-tuned-more` | On | 2 | `tuned-pl2` |

Versions are pinned: Juice Shop v20.3.0, CRS 4.30.0 on NGINX 1.30.5 with
ModSecurity 3.0.17.

## Clean up

```bash
docker compose down -v
```
