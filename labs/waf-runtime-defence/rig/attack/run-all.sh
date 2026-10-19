#!/usr/bin/env bash
# Run every measurement phase in order. Each one starts from a clean state, so
# the order only matters for reading the output. About five minutes.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

./attack/run-phase.sh baseline            Off           1 none
./attack/run-phase.sh detect-pl1          DetectionOnly 1 none
./attack/run-phase.sh block-pl1-untuned   On            1 none
./attack/run-phase.sh block-pl1-excl1     On            1 excl-1
./attack/run-phase.sh block-pl1-tuned     On            1 tuned
./attack/run-phase.sh block-pl2-tuned     On            2 tuned
./attack/run-phase.sh block-pl2-tuned-more On           2 tuned-pl2
./attack/run-phase.sh block-pl1-patched   On            1 patched
