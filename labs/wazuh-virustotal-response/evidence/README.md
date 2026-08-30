# Evidence Index

Screenshots supporting the findings in [`../analysis.md`](../analysis.md).

Each entry below names the file, what it has to show, and which finding it
carries. All five frames are present.

Note on addressing: the runbook is neutralised to placeholders, but these frames
show the real manager hostname and RFC1918 lab addresses. That is intentional
and harmless, but it is why the two do not match.

---

## Required

### `01-alert-chain.png`
Threat Hunting → Events, filtered to the agent, showing the full sequence in one
frame:

| Rule | Description |
|------|-------------|
| 100201 | File added to /root |
| 87105  | VirusTotal malicious verdict, level 12 |
| 553    | File deleted |

Timestamp ordering is the substance of this shot, so keep the timestamp column
visible. Rule 553 matters because it is the SIEM independently observing the
removal rather than the script reporting on itself.

**In repo.**

---

### `02-virustotal-enrichment.png`
The expanded alert document for rule 87105, showing the `data.virustotal`
fields: `source.file`, `source.md5`, `source.sha1`, `positives`, `total`, and
`permalink`.

This is the difference between a screenshot of a dashboard and actual evidence.

**In repo.**

---

### `03-script-diff.png`
Side-by-side comparison of the original and hardened remediation scripts:

```bash
sudo diff -y --width=200 \
  /var/ossec/active-response/bin/remove-threat.sh.orig \
  /var/ossec/active-response/bin/remove-threat.sh
```

`rm -f "$FILE"` must be legible on the left with nothing guarding it. This frame
carries Finding 2 and is the one a reviewer will look at longest, so use a wide
enough terminal that the right column is not truncated mid-line.

**In repo**, captured at `--width=120`. Both columns clip at the right edge. The line that carries the finding, `rm -f "$FILE"` unguarded on the left, is fully legible, so this stands. A re-run at `--width=200` would show the hardened branches in full.

---

### `04-response-log.png`
`active-responses.log` showing both outcomes from the hardened script:

```
2026/08/22 13:43:19 remove-threat: OK deleted /root/eicar.com
2026/08/22 13:43:44 remove-threat: REFUSED path outside /root: /tmp/canary
```

Ideally with the surviving `/tmp/canary` visible in the same frame. This proves
the path validation is functional rather than decorative.

**In repo.**

---

## Optional

### `05-virustotal-eicar.png`
The VirusTotal file page showing the detection ratio alongside the Code Insights
panel stating that EICAR is a test string and not a real virus.

Supports the honesty of the "what this lab does not prove" section. Worth
holding in reserve rather than leading with.

**In repo.**

---

## Reading the timestamps across `01` and `04`

The two frames disagree by four hours on the same event, and that is Finding 3
rather than an error in the evidence:

| Frame | Source | Deletion recorded at |
|-------|--------|----------------------|
| `04-response-log.png` | `active-responses.log` on the agent | `2026/08/22 13:43:19` |
| `01-alert-chain.png`  | Dashboard, rule 553 "File deleted" | `Aug 22, 2026 @ 17:43:19` |

Same event, same second, four hours apart. The agent renders local time on
`America/New_York` inherited from the base VM image; the dashboard renders the
manager's. Wazuh carries UTC internally, so correlation inside the SIEM was
never affected, which is exactly why this survived unnoticed.

No `timedatectl` screenshot was taken. It is not needed: these two frames
demonstrate the offset on a single real event, which is stronger than a
configuration readout would have been. Anyone reconstructing a timeline from
host artifacts alongside SIEM output would land four hours off, and that is the
transferable point.

---

## Disclosure check

Run against all five frames before they were committed:

- No VirusTotal API key visible in any frame
- No email address visible in any terminal shot
- Internal addressing is RFC1918 (`192.168.64.0/24`) and fine to leave
- The VirusTotal page in `05` shows the account display name. That name is
  already public on this repo, so it stays.
- `sudo` password prompts appear in `03` and `04`; no password is echoed
