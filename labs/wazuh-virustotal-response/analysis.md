# Automated Malware Response: Building It, and Finding It Silently Broken

**Lab type:** Detection engineering and response automation, with a code audit of the remediation script
**Date:** August 2026
**Environment:** Self-hosted Wazuh 4.x lab, three virtual machines under UTM on Apple Silicon

---

## Context

A privileged Linux server has no legitimate reason to fetch files from the internet, least of all into `/root`. Threat intelligence indicated active campaigns targeting Linux servers, and the requirement was a host-based capability that could do three things without a human in the loop:

1. Detect unauthorised file changes in privileged directories
2. Enrich those detections with external threat intelligence
3. Automatically remove files confirmed to be malicious

No security tooling existed beforehand. The stack was built from scratch.

The scenario was framed as SOC work. The most useful finding turned out to be an application security one, because the remediation step is not a configuration toggle. It is a shell script that executes as root, on a trigger, against input the operator does not control.

---

## Action

### Detection layer

Real-time file integrity monitoring was configured on `/root` using `syscheck` with `realtime="yes"`, which uses inotify and fires on filesystem events rather than on a scan interval.

Two custom rules were written to raise privileged-directory changes above baseline noise:

| Rule ID | Parent (`if_sid`) | Meaning |
|---------|-------------------|---------|
| 100200  | 550               | File modified in `/root` |
| 100201  | 554               | File added to `/root` |

Both at level 7. This is change-based detection, not signature-based. Wazuh has no concept of whether a file is malicious. It knows only that a file appeared somewhere no file should appear, which is precisely why an enrichment step is necessary.

### Enrichment layer

The VirusTotal integration was scoped to rules 100200 and 100201 only, rather than to all FIM activity. This keeps the free-tier quota (4 lookups/minute, 500/day) spent on privileged directories instead of being exhausted by routine filesystem churn.

On a confirmed malicious verdict, Wazuh's built-in rule 87105 fires at level 12.

### Response layer

An active-response block was bound to rule 87105 with `<location>local</location>`, so the manager dispatches and the agent executes. The remediation script extracts the file path from the alert JSON and deletes it.

### Validation

The pipeline was exercised with EICAR, a standardised antivirus test string. Detection and enrichment behaved as designed on the first run. The response did not, which is covered below.

After remediation, the pipeline was re-tested against both a valid deletion path and a deliberately invalid one to confirm the fix worked in both directions.

---

## Result

### Finding 1: The automated response reported success while doing nothing

For approximately one day, the pipeline produced a complete and convincing alert chain. File added to `/root`, VirusTotal returning 64-65 of 67 engines, a level 12 alert. By every signal available upstream, the incident had been handled.

The file was still on disk. This was discovered by checking the filesystem manually, not by any alert or log entry.

**Root cause.** The remediation script piped alert JSON through `jq`. `jq` was not installed on the agent. The script ran, the extraction produced an empty string, `rm -f ""` deleted nothing, and the script returned `exit 0` unconditionally.

Three distinct defects contributed, and only one of them was the missing package:

- The deployment never verified its own dependency
- The script had no error handling, so total failure was indistinguishable from a clean run
- Nothing was written to `active-responses.log` on either path, so there was no artifact to audit

Wazuh does not populate `active-responses.log` on the script's behalf. Response scripts write to it themselves. The bundled `restart.sh` does; the remediation script from the source material did not.

### Finding 2: The remediation script deleted arbitrary paths as root

The original script passed the extracted filename directly to `rm -f`, running as root, with no check that the path fell inside the monitored directory:

```bash
FILE=$(echo "$INPUT_JSON" | jq -r .parameters.alert.data.virustotal.source.file)
rm -f "$FILE"
```

Wazuh's own documentation includes bounds checking for this reason. The abbreviated version in circulation does not. Any influence over that JSON field converts the detection tooling into an arbitrary root-level file deletion primitive.

### Finding 3: Agent and manager disagreed on time by four hours

The agent reported `America/New_York` (UTC-4) while the manager operated on local time, producing a four-hour offset on identical events. `timedatectl` also showed `NTP synchronized: no` despite network time being enabled.

Wazuh alerts carry UTC internally, so correlation inside the SIEM was never broken. The mismatch was in local rendering: `active-responses.log` on the host versus the dashboard view. That distinction matters, because anyone reconstructing a timeline from host artifacts alongside SIEM output would reach a wrong conclusion about ordering.

The `America/New_York` setting is inherited from the base VM image rather than provisioned, which on a real estate would itself indicate a host outside standard build tooling.

### Remediation

The script was rewritten with four changes:

1. **Dependency check.** Verifies `jq` is present before attempting extraction, and logs a failure if not
2. **Empty-value guard.** Refuses to proceed when the alert yields no file path
3. **Path validation.** Confines deletion to `/root/*` and logs a refusal for anything else
4. **Outcome verification and logging.** Confirms the file is actually gone after `rm`, and writes the result to `active-responses.log` on every path

Both branches were tested:

```
2026/08/22 13:43:19 remove-threat: OK deleted /root/eicar.com
2026/08/22 13:43:44 remove-threat: REFUSED path outside /root: /tmp/canary
```

The refusal test used a disposable canary file in `/tmp`. It survived, and the log recorded why.

---

## What this lab does not prove

Stated plainly, because the alternative is overclaiming:

- **EICAR is a test string, not malware.** What was validated is a pipeline, not a real detection.
- **VirusTotal is a hash lookup.** A file it has not seen returns zero detections. A clean verdict is absence of evidence, not evidence of safety. Novel or targeted payloads pass through this design untouched.
- **Engine consensus moves.** The same hash returned 65/67 on one day and 64/67 the next. Consensus is a signal, not a fact.
- **The server is not "safe" after response.** The payload was removed. The access path that delivered it was not identified. Something wrote to `/root` with root privileges, and nothing in this pipeline establishes how, whether persistence was created, or whether it recurs. Detection answers what happened, not how they got in.
- **Deletion destroys the sample.** For confirmed commodity malware on a workstation that is acceptable. On a server under investigation it removes the artifact needed for IOC extraction. Quarantine is the better default and is the next planned change.
- **FIM covers `/root` only.** Anything dropped elsewhere is outside the monitored scope.

### Control gap

The scenario specifies a server with no business need for internet downloads. Egress filtering would have prevented this before FIM ever observed it. This lab addresses detection and response, not prevention.

---

## Conclusion

The pipeline works. The more transferable result is that it appeared to work for a full day while performing no remediation at all, and the only thing that surfaced it was a manual check.

Automated response is not a feature that gets enabled. It is code that executes as root, on a trigger, against input the operator does not control. It warrants the same review as any other privileged code path: dependency verification, input validation, failure that is loud rather than silent, and an audit trail on every branch.

---

## Environment

| Role | OS | Notes |
|------|----|-------|
| Wazuh manager | Ubuntu | Manager, indexer, dashboard |
| Agent 002 | Ubuntu 16.04 LTS (xenial) | Monitored endpoint for this lab |
| Agent (Kali) | Kali Linux | Present in lab, not used for this exercise |

Virtualised under UTM on Apple Silicon.

**Note on the endpoint:** Ubuntu 16.04 is past end of life. The `xenial-security` pocket returns 404 against `old-releases.ubuntu.com`, so `apt update` exits non-zero. `apt install` still succeeds from the reachable `universe` pocket, but chaining the two with `&&` causes the install to be skipped entirely. This is worth knowing before assuming a package is unavailable.

---

## Evidence

See [`evidence/`](evidence/) for screenshots and the index describing each one.

## Artifacts

- [`runbook.html`](runbook.html) — interactive build runbook covering the full environment, from bare VM through to this response pipeline (Flow 5)
- [`config/local_rules.xml`](config/local_rules.xml) — custom FIM rules
- [`config/ossec-snippets.md`](config/ossec-snippets.md) — manager and agent configuration blocks
- [`scripts/remove-threat.original.sh`](scripts/remove-threat.original.sh) — as deployed from the source material
- [`scripts/remove-threat.hardened.sh`](scripts/remove-threat.hardened.sh) — after the audit

## Write-ups

Published on LinkedIn as the third post in a series built on this environment:

1. [Building the SIEM headless](https://lnkd.in/p/eNyR5nCW) — why Ubuntu Server over a desktop VM, and discovering that ARM64 runs native while x86 gets emulated
2. [Two witnesses to one attack](https://lnkd.in/p/eaHkp4MG) — adding Suricata, scanning from Kali, and network plus host telemetry agreeing independently
3. [Automated response that did nothing](https://lnkd.in/p/d8ZM3ufx) — this lab
