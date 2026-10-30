#!/usr/bin/env bash
# Record a Wine run under rr for deterministic replay.
#
# rr gives unlimited watchpoints and reverse execution across replays, which
# directly answers "who reads/writes this address" without the 4-slot hardware
# watchpoint budget or the timing pressure of a live window. Two environment
# facts make this a DISTINCT arm from the normal hardware-renderer runs, both
# recorded in metadata:
#   * rr cannot record GPU-written shared memory, so hardware GL is unreplayable;
#     LIBGL_ALWAYS_SOFTWARE=1 forces llvmpipe (CPU) rendering. Valid for memory
#     questions, NOT for pixel-fidelity questions.
#   * Wine's esync/fsync synchronize through cross-process eventfds/futexes that
#     rr's per-process recording treats as divergence sources; WINEESYNC=0 and
#     WINEFSYNC=0 disable them.
#
# This wrapper only RECORDS. Validate a trace with `rr ps`, `rr replay -a`, and
# `rr pack` (see --help) before treating it as evidence.
set -euo pipefail
ROOT=${ABLPC_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
PREFIX_NAME=baseline
CHANNELS="+timestamp"
CWD=
RR_BIN=${RR_BIN:-rr}
PARANOID_FILE=${ABLPC_PERF_PARANOID_FILE:-/proc/sys/kernel/perf_event_paranoid}

usage() {
    cat >&2 <<'EOF'
Usage: rr-record.sh [--prefix baseline|instrumented|compatibility]
                    [--channels SPEC] [--cwd DIR] -- executable [args...]

Records a Wine run under rr. Forces LIBGL_ALWAYS_SOFTWARE=1, WINEESYNC=0,
WINEFSYNC=0 (recorded in metadata with rationale). Refuses to run unless
kernel.perf_event_paranoid <= 1 and refuses while /dev/ntsync is present:
Wine 11's in-kernel ntsync driver issues ioctls rr cannot record. Remove it
first (close all Wine, then: sudo modprobe -r ntsync) or hide the device in an
unshare mount namespace, then restore with sudo modprobe ntsync.

Validate a recorded trace before citing it as evidence:
  rr ps    <trace_dir>     # enumerate recorded processes
  rr replay -a <trace_dir> # autopilot replay; confirm it reaches the exit
  rr pack  <trace_dir>     # make the trace hermetic
EOF
    exit 2
}

refuse() {
    # $1 reason, $2 remedy, plus key=value extras
    local reason=$1 remedy=$2
    shift 2
    printf '{"refused":true,"tool":"rr-record","reason":"%s","remedy":"%s"' \
        "$reason" "$remedy"
    while test $# -gt 0; do printf ',%s' "$1"; shift; done
    printf '}\n'
    exit 3
}

while test $# -gt 0; do
    case "$1" in
        --prefix) PREFIX_NAME=${2:-}; shift 2 ;;
        --channels) CHANNELS=${2:-}; shift 2 ;;
        --cwd) CWD=${2:-}; shift 2 ;;
        --help|-h) usage ;;
        --) shift; break ;;
        *) usage ;;
    esac
done
test $# -gt 0 || usage
case "$PREFIX_NAME" in baseline|instrumented|compatibility) ;; *) usage ;; esac

command -v "$RR_BIN" >/dev/null || refuse "rr_missing" "install rr" \
    '"detail":"rr binary not found on PATH"'

test -r "$PARANOID_FILE" || refuse "paranoid_unreadable" \
    "sudo sysctl kernel.perf_event_paranoid=1" \
    "\"observed\":\"unreadable\""
PARANOID=$(cat "$PARANOID_FILE")
if ! test "$PARANOID" -le 1 2>/dev/null; then
    refuse "perf_event_paranoid" "sudo sysctl kernel.perf_event_paranoid=1" \
        "\"observed\":$PARANOID" '"required_max":1'
fi

# Wine 11's in-kernel ntsync driver issues ioctls rr 5.9.0 cannot model, so
# rr FATAL-aborts during Wine init while /dev/ntsync exists. Remove the module
# (Wine then falls back to server-side sync) or run without the device visible.
NTSYNC_DEV=${ABLPC_NTSYNC_DEV:-/dev/ntsync}
if test -e "$NTSYNC_DEV"; then
    refuse "ntsync_present" "close all Wine, then: sudo modprobe -r ntsync (restore with sudo modprobe ntsync)" \
        "\"device\":\"$NTSYNC_DEV\"" \
        '"detail":"Wine uses the in-kernel ntsync driver, whose ioctls rr cannot record; remove it or hide the device in an unshare namespace"'
fi

EXE=$(readlink -f -- "$1")
shift
test -f "$EXE" || { echo "Executable not found: $EXE" >&2; exit 2; }
case "$EXE" in
    "$ROOT/originals"/*) echo "Refusing to execute from originals/. Use a copy under work/copies/." >&2; exit 2 ;;
esac

PREFIX="$ROOT/work/wine/$PREFIX_NAME"
test -d "$PREFIX" || { echo "Prefix does not exist; run scripts/wine-new-prefix.sh first" >&2; exit 2; }
CWD=${CWD:-$(dirname "$EXE")}
CWD=$(readlink -f -- "$CWD")

STAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="RUN-RR-$STAMP"
RUN="$ROOT/dynamic/wine/$RUN_ID"
test ! -e "$RUN" || { echo "Run already exists: $RUN" >&2; exit 2; }
TRACE_DIR="$ROOT/work/rr/$RUN_ID/trace"
test ! -e "$TRACE_DIR" || { echo "Trace already exists: $TRACE_DIR" >&2; exit 2; }
mkdir -p "$RUN" "$(dirname "$TRACE_DIR")"

STARTED=$(date --iso-8601=seconds)
RR_VERSION=$("$RR_BIN" --version 2>&1 | head -n 1)
WINE_VERSION=$(wine --version 2>/dev/null || echo "unknown")
EXE_SHA=$(sha256sum -- "$EXE" | awk '{print $1}')
argv_json=$(printf '%s\n' "$EXE" "$@" | jq -R . | jq -s .)

jq -n \
    --arg run_id "$RUN_ID" --arg started "$STARTED" --arg exe "$EXE" \
    --arg sha "$EXE_SHA" --arg cwd "$CWD" --arg prefix "$PREFIX" \
    --arg wine "$WINE_VERSION" --arg channels "$CHANNELS" \
    --arg recorder "$RR_VERSION" --arg trace "work/rr/$RUN_ID/trace" \
    --argjson paranoid "$PARANOID" \
    --argjson argv "$argv_json" \
    '{run_id:$run_id,started:$started,executable:$exe,executable_sha256:$sha,argv:$argv,
      environment:"Wine",environment_version:$wine,working_directory:$cwd,
      prefix:$prefix,wine_debug_channels:$channels,
      recorder:"rr",recorder_version:$recorder,trace_dir:$trace,
      perf_event_paranoid:$paranoid,
      forced_env:{LIBGL_ALWAYS_SOFTWARE:"1",WINEESYNC:"0",WINEFSYNC:"0"},
      rationale:{LIBGL_ALWAYS_SOFTWARE:"rr cannot record GPU-written shared memory; llvmpipe renders in-process",
                 WINEESYNC:"cross-process eventfd sync diverges under per-process rr recording",
                 WINEFSYNC:"cross-process futex sync diverges under per-process rr recording"},
      status:"running"}' > "$RUN/metadata.json"

set +e
(
    cd "$CWD"
    WINEPREFIX="$PREFIX" WINEDEBUG="$CHANNELS" \
        LIBGL_ALWAYS_SOFTWARE=1 WINEESYNC=0 WINEFSYNC=0 \
        "$RR_BIN" record -o "$TRACE_DIR" wine "$EXE" "$@" \
        > >(tee "$RUN/stdout.txt") \
        2> >(tee "$RUN/stderr.txt" >&2)
)
STATUS=$?
set -e
ENDED=$(date --iso-8601=seconds)

tmp="$RUN/metadata.json.tmp"
jq --arg ended "$ENDED" --argjson status "$STATUS" \
    '.ended=$ended | .exit_status=$status | .status="complete"
     | .artifacts=["metadata.json","stdout.txt","stderr.txt"]' \
    "$RUN/metadata.json" > "$tmp"
mv "$tmp" "$RUN/metadata.json"

echo "$RUN_ID: exit status $STATUS (trace: work/rr/$RUN_ID/trace)"
echo "Validate before citing: rr ps / rr replay -a / rr pack '$TRACE_DIR'"
exit "$STATUS"
