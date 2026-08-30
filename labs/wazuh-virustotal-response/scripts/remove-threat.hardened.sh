#!/bin/bash
#
# Wazuh active-response: remove a file confirmed malicious by VirusTotal.
#
# Deploy to: /var/ossec/active-response/bin/remove-threat.sh
#   sudo chmod 750 /var/ossec/active-response/bin/remove-threat.sh
#   sudo chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh
#   sudo systemctl restart wazuh-agent
#
# Triggered by rule 87105 (VirusTotal malicious verdict) with location: local.
# Runs as root. Reads alert JSON on stdin.
#
# Hardened against four defects in the original:
#   - dependency is verified before use
#   - empty extraction is rejected rather than passed to rm
#   - deletion is confined to the monitored directory
#   - every path writes an outcome to active-responses.log
#
# MONITORED_DIR must match the <directories> entry under <syscheck>. Widening
# the FIM scope without widening this will cause legitimate deletions to be
# refused; widening this without care removes the containment.

LOG="/var/ossec/logs/active-responses.log"
MONITORED_DIR="/root"

read INPUT_JSON

log() {
  echo "$(date '+%Y/%m/%d %H:%M:%S') remove-threat: $1" >> "$LOG"
}

# 1. Dependency check. Absent jq was the original silent failure.
command -v jq >/dev/null 2>&1 || {
  log "FAIL jq not installed"
  exit 1
}

# 2. Extract the target path. // empty yields "" rather than the string "null".
FILE=$(printf '%s' "$INPUT_JSON" | jq -r '.parameters.alert.data.virustotal.source.file // empty' 2>/dev/null)

[ -n "$FILE" ] || {
  log "FAIL no file path in alert"
  exit 1
}

# 3. Path validation. Deletion is confined to the monitored directory.
case "$FILE" in
  "$MONITORED_DIR"/*) ;;
  *)
    log "REFUSED path outside $MONITORED_DIR: $FILE"
    exit 1
    ;;
esac

# 4. Delete, verify the file is actually gone, and record the outcome.
if rm -f "$FILE" && [ ! -e "$FILE" ]; then
  log "OK deleted $FILE"
else
  log "FAIL could not delete $FILE"
fi

exit 0
