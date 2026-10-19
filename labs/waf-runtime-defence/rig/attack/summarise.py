#!/usr/bin/env python3
"""
Join a phase's suite results to its ModSecurity audit log and print, per case,
what the application did on its own and what the WAF did or would have done.

In DetectionOnly mode the WAF blocks nothing, so the HTTP status cannot say what
it caught. The audit log can: a request that fires rule 949110 ("Inbound Anomaly
Score Exceeded") is one the engine would have answered with 403 once switched
on. summarise.py joins the log to each case by the X-Case-Id header.

Usage: summarise.py <phase-label>
"""
import collections
import json
import os
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANOMALY = "949110"  # inbound anomaly score exceeded: the rule that blocks
BOOKKEEPING = {"949110", "949111", "980130", "980170"}

phase = sys.argv[1]
base = os.path.join(LAB, "evidence", phase)
results = [json.loads(line) for line in open(os.path.join(base, "results.jsonl"))]

by_case = collections.defaultdict(list)
audit_path = os.path.join(base, "audit.json")
if os.path.exists(audit_path):
    for line in open(audit_path):
        # A log truncated under a running process leaves NUL padding; drop it.
        line = line.replace("\x00", "").strip()
        if not line:
            continue
        tx = json.loads(line)["transaction"]
        headers = {k.lower(): v for k, v in tx.get("request", {}).get("headers", {}).items()}
        if "x-case-id" in headers:
            by_case[headers["x-case-id"]].append(tx)


def look(case_id):
    """(flagged, score, rule ids) for one case across its WAF-side transactions."""
    flagged, score, rules = False, 0, set()
    for tx in by_case.get(case_id, []):
        for m in tx.get("messages", []):
            rid = m["details"]["ruleId"]
            rules.add(rid)
            if rid == ANOMALY:
                flagged = True
                text = m["message"]
                if "Total Score:" in text:
                    score = max(score, int(text.split("Total Score:")[1].split(")")[0]))
    return flagged, score, sorted(rules - BOOKKEEPING)


def app_column(row):
    if row["kind"] == "normal":
        return "ok" if row["control_hit"] else "FAIL"
    if row["control_hit"] is None:
        return "n/a"
    return "EXPLOITED" if row["control_hit"] else "safe"


print("\n=== %s ===" % phase)
print("%-4s %-10s %-9s %-11s %-5s %s" % ("ID", "CLASS", "APP", "WAF", "SCORE", "RULES"))
tally = collections.Counter()
fps, missed, caught = [], [], []

for row in results:
    flagged, score, rules = look(row["id"])
    blocked = row["waf_code"] == 403 and row["control_code"] != 403
    if blocked:
        verdict = "BLOCKED"
    elif flagged:
        verdict = "would-block"
    elif rules:
        verdict = "logged"
    else:
        verdict = "-"
    row["verdict"], row["score"], row["rules"] = verdict, score, rules
    stopped = blocked or flagged
    if row["kind"] == "normal":
        if stopped:
            tally["false_positives"] += 1
            fps.append(row["id"])
    else:
        if stopped:
            tally["attacks_stopped"] += 1
            caught.append(row["id"])
        else:
            missed.append(row["id"])
    print("%-4s %-10s %-9s %-11s %-5s %s" % (
        row["id"], row["class"], app_column(row), verdict, score or "", ",".join(rules)))

attacks = [r for r in results if r["kind"] == "attack"]
normal = [r for r in results if r["kind"] == "normal"]
print("\nattacks : %d   stopped by the WAF %d   not stopped %d" % (
    len(attacks), tally["attacks_stopped"], len(missed)))
print("normal  : %d   false positives %d%s" % (
    len(normal), tally["false_positives"], ("  (" + ", ".join(fps) + ")") if fps else ""))
if caught:
    print("stopped : " + ", ".join(caught))
if missed:
    print("passed  : " + ", ".join(missed))

with open(os.path.join(base, "summary.json"), "w") as fh:
    json.dump({"phase": phase, "attacks": len(attacks), "stopped": caught,
               "not_stopped": missed, "false_positives": fps, "rows": results}, fh, indent=1)
