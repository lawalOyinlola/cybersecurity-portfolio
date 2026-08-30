# Configuration Snippets

Extracts from `ossec.conf` on both the manager and the monitored agent. These are
fragments, not complete files. Apply them into the existing blocks rather than
replacing anything wholesale.

---

## Agent: real-time FIM on /root

File: `/var/ossec/etc/ossec.conf`

Added inside the existing `<syscheck>` block, alongside the other `<directories>`
entries:

```xml
<directories realtime="yes">/root</directories>
```

`realtime="yes"` uses inotify, so the event fires on the filesystem write rather
than waiting for the next scheduled scan.

### Agent-side active response

Also on the agent, confirm this is not disabled. Default is `no`; if it reads
`yes`, the manager can dispatch and nothing will run:

```xml
<active-response>
  <disabled>no</disabled>
  <ca_store>etc/wpk_root.pem</ca_store>
  <ca_verification>yes</ca_verification>
</active-response>
```

---

## Manager: VirusTotal integration

File: `/var/ossec/etc/ossec.conf`

```xml
<integration>
  <name>virustotal</name>
  <api_key>PASTE_YOUR_VT_API_KEY_HERE</api_key>
  <rule_id>100200,100201</rule_id>
  <alert_format>json</alert_format>
</integration>
```

Scoped deliberately to the two custom rules. The free tier allows 4 lookups per
minute and 500 per day, so widening this to all FIM activity will exhaust the
quota and lookups will begin failing quietly.

---

## Manager: command definition and active response

File: `/var/ossec/etc/ossec.conf`

```xml
<command>
  <name>remove-threat</name>
  <executable>remove-threat.sh</executable>
  <timeout_allowed>no</timeout_allowed>
</command>

<active-response>
  <command>remove-threat</command>
  <location>local</location>
  <rules_id>87105</rules_id>
</active-response>
```

`87105` is Wazuh's built-in rule for a VirusTotal malicious verdict.
`location: local` means the script executes on whichever agent generated the
alert.

### Ordering constraint

**Every `<command>` block must appear above every `<active-response>` block.**
Violating this prevents `wazuh-manager` from starting.

### Two failure modes worth knowing

**The commented sample block.** The default config ships an `<active-response>`
example wrapped in `<!-- -->`. Pasting a real block inside those comment markers
leaves it inert while the config still looks correct on a quick read. Verify
placement with:

```bash
sudo grep -n -B2 -A6 "remove-threat" /var/ossec/etc/ossec.conf
```

**Silent startup failure.** `systemctl status` can report active while the
manager is not processing correctly. After any config change:

```bash
sudo systemctl restart wazuh-manager
sudo grep -iE "error|critical" /var/ossec/logs/ossec.log | tail -20
```

---

## Verification commands

On the agent, after deploying the response script:

```bash
which jq
ls -l /var/ossec/active-response/bin/remove-threat.sh    # expect -rwxr-x--- root:wazuh
head -1 /var/ossec/active-response/bin/remove-threat.sh  # expect #!/bin/bash, no leading whitespace
```

End-to-end test. Terminal one on the agent:

```bash
sudo tail -f /var/ossec/logs/active-responses.log
```

Terminal two:

```bash
sudo curl -Lo /root/eicar.com https://secure.eicar.org/eicar.com
```

Then confirm removal independently:

```bash
sudo ls -la /root
```

Expected alert chain in the dashboard: `100201` (file added), `87105`
(VirusTotal malicious verdict, level 12), `553` (file deleted). Rule 553 is
useful corroboration because it is the SIEM observing the outcome rather than
the script reporting on itself.

---

## Known unresolved

`wazuh-analysisd: ERROR: Too many fields for JSON decoder.` appears in the
manager log in bursts. It did not prevent VirusTotal alerts from decoding
correctly and was not investigated. Noted here so it is not mistaken for a
symptom of the response-path failure.
