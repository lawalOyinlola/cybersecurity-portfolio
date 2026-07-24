# Incident handler's journal

_Incident response journal entries._

A running incident handler's journal kept while working through the Google
Cybersecurity Certificate. Entries 1 and 2 document incident investigations using
the 5 W's framework, entries 3 to 8 document the hands-on use of a cybersecurity
tool (Wireshark, tcpdump, VirusTotal, Suricata, Splunk, and Chronicle), and Entry 9
is a closing reflection on the learning journey. Each entry records the date, a
short description, the tool(s) used, and the supporting analysis. See
[Source materials & attribution](#source-materials--attribution) at the end.

---

## Entry 1 · 19 July 2026

**Description:** Analysis of a ransomware incident at a small U.S. health care
clinic. The clinic's files were encrypted after an employee downloaded a malicious
attachment from a phishing email, halting business operations and blocking access
to patient records. This entry documents the incident using the 5 W's.

**Tool(s) used:** None at this stage. This entry is a documentation and analysis
exercise based on the reported scenario rather than a hands-on investigation. Tools
that would support a real response include a SIEM for log analysis, endpoint
detection and response for the affected workstations, and email security filtering
to trace the phishing source.

**The 5 W's:**

- **Who:** An organized ransomware group known to target the healthcare and
  transportation sectors. The attackers gained entry through targeted phishing
  emails sent to several employees.
- **What:** A phishing email carried a malicious attachment that, once downloaded,
  installed malware on an employee's computer. The attackers deployed ransomware,
  which encrypted critical files. A ransom note demanded payment for the decryption
  key.
- **When:** Tuesday at approximately 9:00 a.m., when employees found they could not
  access files such as medical records.
- **Where:** On the network of a small U.S. health care clinic providing
  primary-care services. The compromise began on an employee workstation and spread
  to file systems holding patient data.
- **Why:** The attackers were financially motivated and sought a ransom payment.
  The entry point was human: employees were tricked into downloading a malicious
  attachment.

**Additional notes:** The root cause was a human-targeted phishing email, so
security awareness training and stronger email filtering are the first preventive
priorities. Offline, tested backups would reduce the leverage of a ransom demand.
Open questions: were files exfiltrated before encryption, which would make this a
HIPAA-reportable breach, and was network segmentation in place to limit spread?

---

## Entry 2 · 21 July 2026

**Description:** Investigation and resolution of a phishing alert (ticket A-2703)
at a financial services company, following the organization's phishing incident
response playbook. The alert concerned a suspicious email attachment whose file
hash had previously been verified as malicious.

**Tool(s) used:** Phishing incident response playbook and flowchart, and the alert
ticketing system. Threat intelligence such as VirusTotal for file-hash reputation,
referenced from the earlier verification of the attachment hash.

**The 5 W's:**

- **Who:** An external threat actor posing as a job applicant, "Clyde West" of "Def
  Communications," using a spoofed sender address to target the company's HR team.
- **What:** A phishing email delivered a password-protected executable
  (`bfsvc.exe`) disguised as a resume and cover letter. The file hash is confirmed
  malicious, and the recipient may have downloaded and opened the attachment.
- **When:** The email was sent on Wednesday, 20 July 2022 at 09:30 a.m., and ticket
  A-2703 was raised for investigation.
- **Where:** At a financial services company, targeting the HR mailbox
  (hr@inergy.com) through the mail server (SERVER-MAIL). The affected endpoint is
  the recipient employee's computer.
- **Why:** To trick an HR employee, who routinely opens resumes, into executing
  malware and gaining a foothold on the company network, likely for financial gain
  given the target sector.

**Additional notes:** The password-protected `.exe` is a deliberate evasion
technique to bypass email scanning, and no legitimate applicant sends a
password-protected executable as a resume. Because the attachment is confirmed
malicious, the playbook directs escalation to a level-two analyst rather than
closure. Follow-up for tier two: did the endpoint execute the file, and does EDR
show signs of compromise or lateral movement? The affected host should be isolated
pending that review.

---

## Entry 3 · 20 July 2026

**Description:** Analyzed a sample packet capture (`sample.pcap`) in Wireshark as a
security analyst investigating traffic to a website, learning to read packet data
and apply display filters to isolate the traffic relevant to an investigation. This
entry documents the use of a cybersecurity tool.

**Tool(s) used:** Wireshark. I opened `sample.pcap` and read the packet-list
columns (No., Time, Source, Destination, Protocol, Length, Info), using Wireshark's
coloring rules to classify traffic types at a glance. I then applied display
filters to narrow the capture: by IP address (`ip.addr`, `ip.src`, and `ip.dst ==
142.250.1.139`), by Ethernet MAC address (`eth.addr == 42:01:ac:15:e0:02`), and by
protocol and port (`udp.port == 53` for DNS, `tcp.port == 80` for HTTP, and `tcp
contains "curl"` to search payload text). To inspect a single packet I opened the
details pane and expanded its protocol stack (the Frame, Ethernet II, Internet
Protocol Version 4, and Transmission Control Protocol subtrees) to read fields such
as TTL, header length, and TCP flags.

**Findings from the capture:**

- The first packet whose Info column showed `Echo (ping) request` used the **ICMP**
  protocol.
- A TCP packet's destination port was **80**, the default HTTP port.
- The DNS traffic (`udp.port == 53`) queried **opensource.google.com**, and the
  Answers section resolved it to **142.250.1.139**.
- A sample HTTP packet, a `curl` request to `http://opensource.google.com`, had
  destination **169.254.169.254**, a TTL of **64**, a frame length of **54 bytes**,
  and an IP header length of **20 bytes**.

**Additional notes:** The core skill is using layered display filters (by address,
MAC, protocol, port, and payload content) to reduce a large capture to just the
packets that matter, then reading one packet's protocol stack from the frame up
through TCP. _Completed in the course Linux and Windows lab environment. The capture
file (`sample.pcap`) remained on the lab machine, so this entry records the workflow
and findings rather than linking a saved artifact._

---

## Entry 4 · 20 July 2026

**Description:** Used tcpdump on a Linux virtual machine (as the user `analyst`) to
identify network interfaces, capture live traffic to a packet-capture file, and
filter the saved capture, the command-line counterpart to the Wireshark analysis in
Entry 3. This entry documents the use of a cybersecurity tool.

**Tool(s) used:** tcpdump. I identified available capture interfaces with `sudo
ifconfig` and `sudo tcpdump -D`, selecting `eth0`, then inspected live traffic with
`sudo tcpdump -i eth0 -v -c5` (`-i` interface, `-v` verbose, `-c5` five packets),
reading the link type, timestamps, IP fields (TOS, TTL, offset, flags, protocol,
length), the source-to-destination flow with ports, and the TCP flags, checksum,
and sequence and acknowledgment numbers. I captured to a file with `sudo tcpdump -i
eth0 -nn -c9 port 80 -w capture.pcap &` (`-nn` no name resolution, `port 80` HTTP
only, `-c9` nine packets, `-w` write to file, `&` run in the background), generated
traffic with `curl opensource.google.com`, and verified the file with `ls -l
capture.pcap`. Finally I read the saved capture back with `sudo tcpdump -nn -r
capture.pcap -v` (`-r` read from file) and inspected packet payloads in hexadecimal
and ASCII with `-X`.

**Additional notes:** Two habits stood out. First, disabling name resolution with
`-nn` during an investigation, because a reverse lookup can alert a malicious actor
and may return unreliable data. Second, scoping a capture tightly (a single
interface, one port, a fixed packet count, written to a file) so the evidence stays
small, relevant, and reviewable later. Together with Entry 3, this covers both
halves of packet work: capturing on the command line and analyzing in a GUI.
_Completed in the course Linux lab environment. The capture file remained on the lab
machine, so this entry records the commands, options, and workflow rather than
linking a saved artifact._

---

## Entry 5 · 20 July 2026

**Description:** Threat-intelligence analysis of the malicious attachment from the
phishing alert (ticket A-2703), investigating its file hash in VirusTotal to
extract indicators of compromise and map them onto the Pyramid of Pain. This is the
tool-driven follow-on to the playbook triage in Entry 2, and it documents the use
of a cybersecurity tool.

**Tool(s) used:** VirusTotal. I searched the attachment's file hash and reviewed
four tabs: Detection (vendor flags), Details (static properties and additional
hashes), Relations (contacted domains, URLs, IPs), and Behavior (sandbox activity
mapped to MITRE ATT&CK techniques). Maliciousness was confirmed from several
agreeing signals rather than a single number: 51 of 69 vendors flagged the file,
the community score was -297, and the threat label `trojan.flagpro/fragtor`
identified it as the Flagpro malware family. The file masqueraded as a legitimate
Windows binary (`bfsvc.exe`, the Boot File Servicing Utility) but was unsigned, and
the sandbox observed process injection, sandbox evasion, and command-and-control
traffic.

**Indicators of compromise (Pyramid of Pain):** _This entry documents tool use and
threat intelligence. The incident's 5 W's are recorded in Entry 2. I selected three
indicators of compromise, one each from the base, middle, and top of the pyramid so
the framework is visible in the result._

- **Hash values (bottom, easiest to change):** additional MD5 and SHA-1 hashes for
  the same file. Blocking a hash stops this exact file but not a recompiled copy.
- **Domain names (middle):** `org.misecure.com`, a contacted domain matching an IDS
  rule for dynamic-DNS command-and-control traffic. Blocking it forces the attacker
  to stand up new infrastructure.
- **Tactics, techniques, and procedures (top, hardest to change):** process
  injection (T1055), masquerading (T1036), virtualization and sandbox evasion
  (T1497), and application-layer C2 (T1071). Detecting on behaviour is the most
  durable defence.

**Additional notes:** The higher up the Pyramid of Pain a defender detects, the
more costly the attack becomes to sustain, so behaviour-based detection (the TTPs)
is the most durable outcome of this analysis. Recommended tier-two follow-up:
confirm whether the endpoint executed the file, review EDR for compromise or
lateral movement, and isolate the affected host pending that review.

---

## Entry 6 · 22 July 2026

**Description:** Explored intrusion detection with Suricata as a security analyst
monitoring network traffic: examined the anatomy of a custom rule (signature), ran
Suricata against a sample capture to trigger alerts, and analyzed the resulting
`fast.log` and `eve.json` logs. This entry documents the use of a cybersecurity
tool.

**Tool(s) used:** Suricata (with `jq` for JSON log analysis). I examined a custom
rule in `custom.rules` with `cat`, breaking the signature into its three parts:
the **action** (`alert`, alongside `drop`, `pass`, and `reject`), the **header**
(protocol, source and destination networks and ports, and direction, for example
`http $HOME_NET any -> $EXTERNAL_NET any`, where `$HOME_NET` is the `172.21.224.0/20`
variable defined in `/etc/suricata/suricata.yaml`), and the **rule options**
(`msg:"GET on wire"`, `flow:established,to_server`, `content:"GET"`, `http_method`,
`sid:12345`, `rev:3`). I ran the rule against the capture with `sudo suricata -r
sample.pcap -S custom.rules -k none` (`-r` read the pcap, `-S` use the custom rule
file, `-k none` disable checksum checks), which wrote alerts to
`/var/log/suricata/fast.log` and detailed events to `eve.json`. I read `fast.log`
with `cat` and analyzed `eve.json` with `jq`: pretty-printing with `jq . | less`,
extracting fields with `jq -c "[.timestamp,.flow_id,.alert.signature,.proto,.dest_ip]"`,
and correlating a single network flow with `jq "select(.flow_id==...)"`.

**Findings from the run:**

- The rule triggers whenever Suricata observes `GET` as the HTTP method in an HTTP
  packet leaving the home network for the external network (alert message "GET on
  wire").
- The first alert had a **severity of 3**, and its signature was **"GET on wire"**.
- `fast.log` is a quick, deprecated alert format useful for QA checks, `eve.json`
  is the standard, detailed JSON event log, and the `flow_id` field ties together
  all packets belonging to the same network flow.

**Additional notes:** The action, header, and options structure is the reusable
mental model for reading or writing any IDS or IPS signature, and the `alert`
versus `drop` distinction is the line between detection (IDS) and prevention (IPS
mode, where `drop` actually takes effect). `jq` turns Suricata's verbose `eve.json`
into targeted, greppable evidence by selecting specific fields and pivoting on
`flow_id` to reconstruct a single conversation. _Completed in the course Linux lab
environment. `sample.pcap` and `custom.rules` remained on the lab machine, so this
entry records the workflow, commands, and findings rather than linking saved
artifacts._

---

## Entry 7 · 22 July 2026

**Description:** Practiced searching and querying events in Splunk using its Search
Processing Language (SPL), as a security analyst locating security events (such as
failed logins and application errors) in a SIEM. This entry documents the use of a
cybersecurity tool.

**Tool(s) used:** Splunk (Search & Reporting, SPL). I built searches from an index
and a search term (`index=main fail`) and refined them with the core SPL
techniques: **piping** to transform results (`index=main fail | chart count by
host`, which counts events by host to surface machines with excessive failures),
**wildcards** to broaden a term (`fail*` matches `failed`, `failure`, and similar),
and **double quotes** to pin an exact phrase (`"login failure"`, rather than events
that merely contain `login` or `failure` separately). In a raw log search against a
fictional online store's data I ran `buttercupgames error OR fail*`, specifying the
index, the Boolean `OR`, and the wildcard, then scoped it with the time-range picker
(last 30 days), read the timeline and events viewer, and refined by excluding a data
source with `host!=www1` so only the `www2` and `www3` hosts remained.

**Findings from the searches:**

- Broad keyword searches (for example, `failed login`) can return thousands of
  results and slow the engine. Adding parameters such as an event ID and a date and
  time range narrows the search and speeds it up.
- The Buttercup Games errors related to HTTP cookies on the website, and each event
  carried a timestamp, raw logged data, and source info (host, source, sourcetype).
- A raw log search is slower because it extracts log fields at search time, and SPL
  provides commands to optimize performance.

**Additional notes:** The reusable idea is that specific queries beat broad ones (the
index, exact terms, and a time range), and that piping, as in the Linux shell, chains
commands to transform results into exactly the view you need, such as a per-host
failure count. _Search methods practiced in the course's Splunk Cloud environment.
The example queries use the course's demonstration datasets._

---

## Entry 8 · 22 July 2026

**Description:** Practiced searching and querying events in Google Security
Operations (Chronicle), locating events such as failed logins with a Unified Data
Model (UDM) search, the SIEM counterpart to the Splunk work in Entry 7. This entry
documents the use of a cybersecurity tool.

**Tool(s) used:** Google SecOps (Chronicle): UDM Search, with awareness of Raw Log
Search and the YARA-L rule language. Using the structured query builder I ran a UDM
search: `metadata.event_type = "USER_LOGIN" AND security_result.action = "BLOCK"`.
Here, `metadata.event_type` selects authentication (user-login) events, the `AND`
operator requires both conditions, and `security_result.action = "BLOCK"` narrows to
blocked or failed logins. I read the results (the UDM search terms, a bar-graph
timeline of failed logins over time for spotting patterns, and a list of timestamped
events each tied to an asset or device), then opened an event's raw log and used
Quick Filters and procedural filtering (for example `target.ip`) to narrow to a
specific IP address.

**Findings and reference notes:**

- **UDM Search** is the default and searches normalized data (indexed and
  structured, so faster). **Raw Log Search** searches un-normalized logs and is used
  to find non-normalized fields or troubleshoot ingestion, and it supports regular
  expressions.
- Searchable fields include hostname, domain, IP, URL, email, username, and file
  hash, and the common UDM field groups are Entities, Event metadata, Network
  metadata, and Security results.
- One result was a blocked login for a user named "alice." Chronicle uses **YARA-L**
  to define detection rules over ingested logs (for example, detecting data
  exfiltration).

**Additional notes:** Together with Entry 7, this shows the query concept transfers
across SIEMs: you specify the data (the index or event type), the terms, boolean
logic, and a time range, while each tool has its own language (SPL versus UDM and
YARA-L) and its own trade-off between normalized and raw search. _Search methods
practiced in the course's Google SecOps environment. The example query uses the
course's demonstration data._

---

## Entry 9 · 23 July 2026 (reflection)

**Description:** A closing reflection on my learning journey through the incident
detection and response work in this course, written as the final entry of the
journal.

**Reflections and notes:**

**1. Were there any specific activities that were challenging for you? Why or why
not?**

The packet analysis work with Wireshark and tcpdump was the most challenging.
Coming from software engineering I was comfortable reading application logs, but a
raw capture is a different skill: I had to learn to follow each request to its
response across hosts and build layered filters, by IP, protocol, and port, to
isolate the traffic that mattered.

**2. Has your understanding of incident detection and response changed since taking
this course?**

Somewhat. My engineering background already gave me strong instincts for tracing a
problem to its root cause, so the biggest change was structural rather than
conceptual. Frameworks like the NIST incident lifecycle, the 5 W's, and the IDS and
SIEM workflow gave those instincts a repeatable shape and a shared vocabulary I can
carry into any investigation.

**3. Was there a specific tool or concept that you enjoyed the most? Why?**

The Pyramid of Pain and the 5 W's framework. I enjoyed the Pyramid of Pain because
it reframes detection as economics: the higher up you detect, the more costly the
attack becomes to sustain, which makes behaviour-based defence the goal. I liked the
5 W's for the opposite reason: its simplicity keeps an incident record complete and
consistent every time.

---

## Source materials & attribution

This is the complete, running incident handler's journal for my Google
Cybersecurity Certificate work. A frozen two-entry snapshot, produced as the
deliverable for the [phishing incident response lab](../phishing-incident-response/analysis.md)
task, is preserved as
[`incident-handlers-journal.pdf`](../phishing-incident-response/incident-handlers-journal.pdf).
The scenarios, lab environments, sample capture, alert ticket, and journal template
are adapted from the Google Cybersecurity Certificate on Coursera:

- **Module 3 (Connect and Protect, Networks and Network Security):** the Wireshark
  "Analyze your first packet" and tcpdump "Capture your first packet" lab activities
  (Entries 3 and 4), and the related network traffic analysis reports.
- **Module 6 (Sound the Alarm, Detection and Response):** the ransomware and
  phishing scenarios, the VirusTotal file-hash and IoC analysis, the Suricata
  signatures-and-logs lab, and the Splunk and Chronicle SIEM search methods
  (Entries 1, 2, 5, 6, 7, and 8).

The packet captures and filtering (Entries 3 and 4) and the Suricata rule and log
analysis (Entry 6) were performed in the course's Linux and Windows lab machines.
Those environments and the sample files (`sample.pcap`, `custom.rules`) are
course-provided and remained in the lab, so those entries record my own workflow,
commands, and findings rather than redistributing the lab files. The Splunk and
Chronicle searches (Entries 7 and 8) were practiced in the course's cloud SIEM
environments, and the example queries use the course's demonstration datasets. The
5 W's write-ups, the playbook-driven escalation decision, the VirusTotal IoC
analysis, the reflection, and all entries in this journal are my own work.

Related labs in this portfolio:

- **Entries 2 and 5:** [Phishing incident response: playbook triage and IoC analysis](../phishing-incident-response/analysis.md)
- **Entries 3 and 4:** [Network traffic analysis and incident reporting](../network-traffic-analysis/analysis.md) (applied tcpdump and Wireshark investigations with saved deliverables)
