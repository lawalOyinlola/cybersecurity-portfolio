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
# Hardened against five defects in the original:
#   - dependency is verified before use
#   - empty extraction is rejected rather than passed to rm
#   - deletion is confined to the monitored directory, after the path is
#     canonicalised so traversal cannot escape it
#   - every path writes an outcome to active-responses.log
#   - failure exits non-zero instead of reporting success
#
# MONITORED_DIR must match the <directories> entry under <syscheck>. Widening
# the FIM scope without widening this will cause legitimate deletions to be
# refused; widening this without care removes the containment.

LOG="/var/ossec/logs/active-responses.log"
MONITORED_DIR="/root"

# IFS= and -r keep the JSON byte-exact: -r stops backslashes in a filename
# being consumed as escapes before jq parses it.
IFS= read -r INPUT_JSON

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
#
#    A lexical match is not sufficient on its own. "/root/../tmp/canary" fits
#    the pattern "/root/*" but resolves outside /root, so the containment has
#    to be checked against the resolved path, not the string in the alert.
#
#    The parent directory is resolved, which collapses ".." segments and any
#    symlinked parent component. The final component is deliberately left
#    unresolved so that a symlink is deleted as a symlink rather than followed
#    to whatever it points at.
#
#    cd -P with pwd -P is used rather than realpath, which is not POSIX and is
#    absent on some systems. Depending on a tool that might not be installed is
#    the defect this script exists to correct.

MONITORED_REAL=$(cd -P -- "$MONITORED_DIR" 2>/dev/null && pwd -P) || {
  log "FAIL monitored dir does not resolve: $MONITORED_DIR"
  exit 1
}

BASE=$(basename -- "$FILE")
case "$BASE" in
  . | ..)
    log "REFUSED not a deletable path: $FILE"
    exit 1
    ;;
esac

PARENT_REAL=$(cd -P -- "$(dirname -- "$FILE")" 2>/dev/null && pwd -P) || {
  log "REFUSED unresolvable parent: $FILE"
  exit 1
}

TARGET="$PARENT_REAL/$BASE"

case "$TARGET" in
  "$MONITORED_REAL"/*) ;;
  *)
    log "REFUSED path outside $MONITORED_REAL: $FILE"
    exit 1
    ;;
esac

# 4. Delete, verify the file is actually gone, and record the outcome.
#    -e follows symlinks, so it reports "gone" for a dangling symlink still
#    sitting at the path. -L catches that case.
if rm -f -- "$TARGET" && [ ! -e "$TARGET" ] && [ ! -L "$TARGET" ]; then
  log "OK deleted $TARGET"
else
  log "FAIL could not delete $TARGET"
  exit 1
fi

exit 0
