#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
test $# -eq 4 || {
    echo "Usage: $0 PROJECT_DIR PROJECT_NAME PROGRAM_NAME OUTPUT.json" >&2
    exit 2
}
PROJECT_DIR=$(readlink -f -- "$1")
PROJECT_NAME=$2
PROGRAM_NAME=$3
OUTPUT=$4
case "$OUTPUT" in /*) ;; *) OUTPUT="$ROOT/$OUTPUT" ;; esac
mkdir -p "$(dirname "$OUTPUT")"
"$ROOT/scripts/ghidra-headless.sh" "$PROJECT_DIR" "$PROJECT_NAME" \
    -process "$PROGRAM_NAME" -noanalysis \
    -scriptPath "$ROOT/scripts/ghidra" \
    -postScript ExportEvidence.java "$OUTPUT"
echo "$OUTPUT"
