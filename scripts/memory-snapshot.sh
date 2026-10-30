#!/usr/bin/env bash
# Take a gcore memory snapshot of the game at a natural pause.
#
# A whole-address-space snapshot lets a control-vs-mod core diff locate where
# DAT/asset bytes land in memory without spending hardware watchpoints. gcore
# attaches via ptrace and briefly stops the process (run it at a natural pause,
# like the watch harness). The core contains game bytes, so it is written to a
# caller-supplied, git-ignored evidence dir; only metadata, hashes, and the
# path/range map (maps.txt) are recorded under dynamic/wine/.
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT=${ABLPC_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}
PY="${ABLPC_PYTHON:-$SCRIPT_DIR/../.venv/bin/python}"
test -x "$PY" || PY=python3
LIB="$SCRIPT_DIR/evidence_lib.py"

PID=
EVIDENCE_DIR=
EXPECTED_SHA=
EXE_BASENAME=bugs.exe
ALL_MAPPINGS=0
GCORE_BIN=${GCORE_BIN:-gcore}
LOADER_RE='^/usr/(bin|lib64)/.*wine.*$'
CWD_PREFIX=

usage() {
    cat >&2 <<'EOF'
Usage: memory-snapshot.sh --pid PID --evidence-dir DIR
         [--expected-sha SHA] [--exe-basename bugs.exe] [--all-mappings]
         [--loader-re RE] [--cwd-prefix PREFIX]

Writes a gcore snapshot to the ignored evidence dir and a RUN-CORE-<stamp>
metadata record (with core hash and /proc/PID/maps) under dynamic/wine/.
EOF
    exit 2
}

refuse() {
    local reason=$1 detail=${2:-}
    printf '{"refused":true,"tool":"memory-snapshot","reason":"%s","detail":"%s"}\n' \
        "$reason" "$detail"
    exit 3
}

while test $# -gt 0; do
    case "$1" in
        --pid) PID=${2:-}; shift 2 ;;
        --evidence-dir) EVIDENCE_DIR=${2:-}; shift 2 ;;
        --expected-sha) EXPECTED_SHA=${2:-}; shift 2 ;;
        --exe-basename) EXE_BASENAME=${2:-}; shift 2 ;;
        --all-mappings) ALL_MAPPINGS=1; shift ;;
        --loader-re) LOADER_RE=${2:-}; shift 2 ;;
        --cwd-prefix) CWD_PREFIX=${2:-}; shift 2 ;;
        --help|-h) usage ;;
        *) usage ;;
    esac
done
test -n "$PID" || usage
test -n "$EVIDENCE_DIR" || usage
command -v "$GCORE_BIN" >/dev/null || refuse "gcore_missing" "install gdb (gcore)"

own_args=(--pid "$PID" --exe-basename "$EXE_BASENAME" --loader-re "$LOADER_RE")
test -n "$EXPECTED_SHA" && own_args+=(--expected-sha "$EXPECTED_SHA")
test -n "$CWD_PREFIX" && own_args+=(--cwd-prefix "$CWD_PREFIX")
OWNERSHIP=$("$PY" "$LIB" ownership "${own_args[@]}") || { echo "$OWNERSHIP"; exit 3; }

mkdir -p "$EVIDENCE_DIR"
if ! git -C "$ROOT" check-ignore -q -- "$EVIDENCE_DIR"; then
    refuse "evidence_dir_not_ignored" "$EVIDENCE_DIR is not git-ignored"
fi

STAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="RUN-CORE-$STAMP"
RUN="$ROOT/dynamic/wine/$RUN_ID"
test ! -e "$RUN" || { echo "Run already exists: $RUN" >&2; exit 2; }
mkdir -p "$RUN"

# The mapping table is path/range metadata (no payload bytes); safe to commit.
cp "/proc/$PID/maps" "$RUN/maps.txt" 2>/dev/null || true

CORE_BASE="$EVIDENCE_DIR/bugs-$STAMP"
PAUSE_STARTED=$(date --iso-8601=seconds)
gcore_args=()
test "$ALL_MAPPINGS" -eq 1 && gcore_args+=(-a)
gcore_status=0
"$GCORE_BIN" "${gcore_args[@]}" -o "$CORE_BASE" "$PID" >/dev/null 2>&1 || gcore_status=$?
PAUSE_ENDED=$(date --iso-8601=seconds)

CORE_PATH="${CORE_BASE}.${PID}"
if test ! -f "$CORE_PATH"; then
    # gcore's exact suffix can vary; take the newest match.
    CORE_PATH=$(ls -1t "${CORE_BASE}"* 2>/dev/null | head -n 1 || true)
fi

CORE_SHA=
CORE_SIZE=0
if test -n "$CORE_PATH" && test -f "$CORE_PATH"; then
    CORE_SHA=$(sha256sum -- "$CORE_PATH" | awk '{print $1}')
    CORE_SIZE=$(stat -c %s "$CORE_PATH")
fi
GDB_VERSION=$(gdb --version 2>/dev/null | head -n 1 || echo unknown)

if test "$gcore_status" -eq 0 && test -n "$CORE_SHA"; then
    STATUS_STR=complete
else
    STATUS_STR=gcore-failed
fi

jq -n \
    --arg run_id "$RUN_ID" --arg pid "$PID" --argjson ownership "$OWNERSHIP" \
    --arg core_path "$CORE_PATH" --arg core_sha "$CORE_SHA" \
    --argjson core_size "$CORE_SIZE" --argjson all_mappings "$ALL_MAPPINGS" \
    --arg pause_started "$PAUSE_STARTED" --arg pause_ended "$PAUSE_ENDED" \
    --arg debugger "$GDB_VERSION" --arg status "$STATUS_STR" \
    '{run_id:$run_id,pid:($pid|tonumber),tool:"memory-snapshot",
      ownership:$ownership,
      core_path:$core_path,
      core_sha256:(if $core_sha=="" then null else $core_sha end),
      core_size_bytes:$core_size,
      gcore_all_mappings:($all_mappings==1),
      pause_started:$pause_started,pause_ended:$pause_ended,
      debugger:$debugger,core_committed:false,status:$status,
      artifacts:["metadata.json","maps.txt"]}' > "$RUN/metadata.json"

echo "$RUN_ID: status=$STATUS_STR core=$CORE_PATH"
test "$gcore_status" -eq 0 || exit 1
