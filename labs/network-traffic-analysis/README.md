# Network traffic analysis and incident reporting

Four packet-capture and incident-report investigations, grouped as one body of
foundational analysis work. Each takes a raw signal, a tcpdump or Wireshark
capture, or an incident brief, and traces it from observable symptom to root
cause, then records the finding and a proportionate remediation in the format a
team would actually circulate.

These are transferable fundamentals rather than expert-level practice. The same
habits they build, reading evidence as a sequence rather than a flat log,
separating symptom from cause, and mapping a finding to a control, are the habits
that carry directly into application and pipeline security.

## The investigations

| # | Investigation | Evidence | Finding | Key control |
|---|---|---|---|---|
| 1 | [DNS service outage](./dns-service-outage/analysis.md) | tcpdump DNS/ICMP capture | DNS server reachable but not answering on port 53 | Service and firewall diagnosis |
| 2 | [SYN flood denial of service](./syn-flood-dos/analysis.md) | Wireshark TCP/HTTP capture | Direct DoS from a single source flooding half-open connections | Containment and its limits (IP spoofing) |
| 3 | [Brute force attack and malware redirect](./brute-force-malware-redirect/analysis.md) | tcpdump DNS/HTTP capture, helpdesk reports, source review | Default admin password brute forced, then malware redirect injected | Two-factor / MFA on privileged logins |
| 4 | [ICMP flood, NIST CSF analysis](./nist-csf-icmp-flood/analysis.md) | Incident brief | ICMP flood DoS through an unconfigured firewall | Firewall hardening across all five NIST CSF functions |

## What this set demonstrates

- Reading packet captures (tcpdump and Wireshark) as a conversation between hosts
  rather than a flat list, following each request to its response.
- Working knowledge of the protocols involved: DNS resolution and port 53, the TCP
  three-way handshake, HTTP over ports 80 and 443, and ICMP error semantics.
- Separating network reachability from service availability, and a direct DoS from
  a distributed one, from the evidence rather than the symptom.
- Correlating network evidence with out-of-band signals (helpdesk reports, a
  source-code review) to move from symptom to root cause.
- Structuring a technical finding through the NIST Cybersecurity Framework and into
  a proportionate remediation, from MFA and password policy to firewall hardening.

Each investigation is written up in full in its own directory, linked in the table
above.
