#!/usr/bin/env python3
"""
Turn a phase's measurements into a pass or fail, so the WAF configuration can
be checked like any other code.

Reads evidence/<phase>/summary.json (written by summarise.py) and exits 1 when
a rule of the policy is broken:

  --must-stop S1,S2,...   every listed attack must be stopped by the WAF
  --max-false-positives N at most N legitimate requests may be flagged

Usage: check.py <phase-label> --must-stop S1,S2 --max-false-positives 0
"""
import argparse
import json
import os
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument("phase")
parser.add_argument("--must-stop", default="")
parser.add_argument("--max-false-positives", type=int, default=0)
args = parser.parse_args()

with open(os.path.join(LAB, "evidence", args.phase, "summary.json")) as fh:
    summary = json.load(fh)

required = [c for c in args.must_stop.split(",") if c]
missing = [c for c in required if c not in summary["stopped"]]
false_positives = summary["false_positives"]

problems = []
if missing:
    problems.append("not stopped: " + ", ".join(missing))
if len(false_positives) > args.max_false_positives:
    problems.append("false positives (%d, allowed %d): %s" % (
        len(false_positives), args.max_false_positives, ", ".join(false_positives)))

if problems:
    print("FAIL %s" % args.phase)
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("PASS %s: %d required attacks stopped, %d false positives" % (
    args.phase, len(required), len(false_positives)))
