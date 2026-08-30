#!/bin/bash
read INPUT_JSON
FILE=$(echo "$INPUT_JSON" | jq -r .parameters.alert.data.virustotal.source.file)
rm -f "$FILE"
exit 0

# ---------------------------------------------------------------------------
# RETAINED FOR COMPARISON ONLY. DO NOT DEPLOY.
#
# This is the script as originally deployed, reproduced from the lab source
# material. It is kept alongside the hardened version so the difference can be
# read directly.
#
# Defects:
#
# 1. Unverified dependency
#    Requires jq. If jq is absent, bash reports command not found, FILE is set
#    to an empty string, `rm -f ""` deletes nothing, and the script still exits
#    0. Failure is indistinguishable from success to anything upstream.
#
# 2. No path validation
#    The extracted value is passed straight to `rm -f` as root, with no check
#    that it falls inside the monitored directory. Any influence over that JSON
#    field yields arbitrary root-level file deletion.
#
# 3. No output
#    Wazuh does not write active-responses.log on the script's behalf. Response
#    scripts log themselves. This one does not, on any path, so neither success
#    nor failure leaves an artifact.
#
# 4. Unconditional exit 0
#    Every path returns success regardless of what actually happened.
#
# See remove-threat.hardened.sh for the deployed version.
# ---------------------------------------------------------------------------
