#!/usr/bin/env bash
#
# Run one measurement phase from a known state:
#
#   1. install the phase's tuning file and set the engine and paranoia level
#   2. restart the target, so its data (and any rate limits) start fresh
#   3. empty the audit log and recreate the WAF container
#   4. run the payload suite
#   5. keep the audit log next to the results
#
# Usage: run-phase.sh <phase-label> <engine> <paranoia> [none|tuned]
#   engine  : Off | DetectionOnly | On
#   tuning  : which file in waf/tuning/ to install (default: none)
set -euo pipefail

LAB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PHASE="${1:?phase label}"; ENGINE="${2:?engine}"; PARANOIA="${3:?paranoia}"; TUNING="${4:-none}"
cd "$LAB"
echo "### $PHASE: engine=$ENGINE paranoia=$PARANOIA tuning=$TUNING"

# 1. Written with cat > (not sed -i or an editor's save) so the file keeps its
#    inode: the compose file bind-mounts this single file, and replacing it
#    would leave the container looking at the old one.
cat "waf/tuning/$TUNING.conf" > waf/modsec/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
printf 'ENGINE=%s\nPARANOIA=%s\n' "$ENGINE" "$PARANOIA" > .env

# 2 and 3. Truncate before the container starts, so no running process has the
#          file open while it is emptied.
docker compose stop waf >/dev/null 2>&1 || true
: > logs/waf/audit.log
docker compose up -d juice control >/dev/null
docker compose restart juice >/dev/null
docker compose up -d --force-recreate waf >/dev/null

# Wait until both listeners answer, but not forever: a container that crashed
# at start-up (a bad rule, say) would otherwise leave this looping.
for port in 8080 9080; do
  tries=0
  until curl -sf -o /dev/null --max-time 3 "http://localhost:$port/rest/admin/application-version"; do
    tries=$((tries + 1))
    if [ "$tries" -ge 90 ]; then
      echo "Nothing answered on port $port after 90 seconds. Check: docker compose ps -a; docker compose logs waf" >&2
      exit 1
    fi
    sleep 1
  done
done

# 4 and 5.
python3 attack/suite.py "$PHASE"
cp logs/waf/audit.log "evidence/$PHASE/audit.json"
python3 attack/summarise.py "$PHASE"
