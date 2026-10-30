#!/usr/bin/env bash
# Capture one compositor frame while the game is frozen at a chosen milestone.
#
# The free-running 15-frame comparison method drowns small mod deltas in
# animation noise. Freezing the game process with SIGSTOP holds the last
# committed frame so a control-vs-mod capture is phase-locked and nearly
# noise-free.
#
# Freeze scope: only the single game PID is stopped (all its threads, one
# SIGSTOP). Gamescope, wineserver, and the PipeWire chain keep running, so the
# held frame stays presentable. wineserver is never stopped.
#
# The established game-surface backend is asynchronous compositor capture:
#   GAMESCOPE_WAYLAND_DISPLAY=gamescope-0 gamescopectl screenshot {out}
# Provide it with --capture-cmd or CAPTURE_CMD; use "{out}" where the canonical,
# absolute, initially nonexistent output PNG belongs, then verify the completed
# image. R2c additionally uses its committed executor and strict image gates.
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
MILESTONE=
MILESTONE_TIMEOUT=60
LOG=
CAPTURE_CMD=${CAPTURE_CMD:-}
CAPTURE_TIMEOUT=20
LOADER_RE='^/usr/(bin|lib64)/.*wine.*$'
CWD_PREFIX=

usage() {
    cat >&2 <<'EOF'
Usage: frozen-capture.sh --pid PID --evidence-dir DIR
         [--expected-sha SHA] [--exe-basename bugs.exe]
         [--milestone STRING] [--milestone-timeout SECS] [--log FILE]
         [--capture-cmd 'TEMPLATE'] [--capture-timeout SECS]
         [--loader-re RE] [--cwd-prefix PREFIX]

Freezes the game PID, captures one frame via the capture template ({out}
placeholder), then resumes. The frame is written to the ignored evidence dir;
a RUN-FRZ-<stamp> metadata record is written under dynamic/wine/.
EOF
    exit 2
}

refuse() {
    local reason=$1 detail=${2:-}
    printf '{"refused":true,"tool":"frozen-capture","reason":"%s","detail":"%s"}\n' \
        "$reason" "$detail"
    exit 3
}

while test $# -gt 0; do
    case "$1" in
        --pid) PID=${2:-}; shift 2 ;;
        --evidence-dir) EVIDENCE_DIR=${2:-}; shift 2 ;;
        --expected-sha) EXPECTED_SHA=${2:-}; shift 2 ;;
        --exe-basename) EXE_BASENAME=${2:-}; shift 2 ;;
        --milestone) MILESTONE=${2:-}; shift 2 ;;
        --milestone-timeout) MILESTONE_TIMEOUT=${2:-}; shift 2 ;;
        --log) LOG=${2:-}; shift 2 ;;
        --capture-cmd) CAPTURE_CMD=${2:-}; shift 2 ;;
        --capture-timeout) CAPTURE_TIMEOUT=${2:-}; shift 2 ;;
        --loader-re) LOADER_RE=${2:-}; shift 2 ;;
        --cwd-prefix) CWD_PREFIX=${2:-}; shift 2 ;;
        --help|-h) usage ;;
        *) usage ;;
    esac
done
test -n "$PID" || usage
test -n "$EVIDENCE_DIR" || usage

# Ownership proof BEFORE any signal.
own_args=(--pid "$PID" --exe-basename "$EXE_BASENAME" --loader-re "$LOADER_RE")
test -n "$EXPECTED_SHA" && own_args+=(--expected-sha "$EXPECTED_SHA")
test -n "$CWD_PREFIX" && own_args+=(--cwd-prefix "$CWD_PREFIX")
OWNERSHIP=$("$PY" "$LIB" ownership "${own_args[@]}") || {
    echo "$OWNERSHIP"
    exit 3
}

# The evidence dir must be git-ignored (it will hold game-frame bytes).
mkdir -p "$EVIDENCE_DIR"
if ! git -C "$ROOT" check-ignore -q -- "$EVIDENCE_DIR"; then
    refuse "evidence_dir_not_ignored" "$EVIDENCE_DIR is not git-ignored"
fi
test -n "$CAPTURE_CMD" || refuse "capture_backend_not_established" \
    "provide --capture-cmd or CAPTURE_CMD with a {out} placeholder"

CWD=$(readlink -f "/proc/$PID/cwd" 2>/dev/null || true)
if test -z "$LOG" && test -n "$CWD"; then LOG="$CWD/bugs.log"; fi

LOG_START_OFFSET=0
MILESTONE_SEEN_AT=
if test -n "$MILESTONE"; then
    if test -f "$LOG"; then LOG_START_OFFSET=$(stat -c %s "$LOG"); fi
    deadline=$((SECONDS + MILESTONE_TIMEOUT))
    while true; do
        if test -f "$LOG"; then
            if tail -c +$((LOG_START_OFFSET + 1)) "$LOG" 2>/dev/null | grep -qF -- "$MILESTONE"; then
                MILESTONE_SEEN_AT=$(date --iso-8601=seconds)
                break
            fi
        fi
        if test "$SECONDS" -ge "$deadline"; then
            refuse "milestone_timeout" "milestone '$MILESTONE' not seen in ${MILESTONE_TIMEOUT}s"
        fi
        sleep 0.2
    done
fi

STAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="RUN-FRZ-$STAMP"
RUN="$ROOT/dynamic/wine/$RUN_ID"
test ! -e "$RUN" || { echo "Run already exists: $RUN" >&2; exit 2; }
mkdir -p "$RUN"
FRAME="$EVIDENCE_DIR/frame-$STAMP.png"

# Always resume the game, even on error.
resumed=false
cont() { kill -CONT "$PID" 2>/dev/null || true; resumed=true; }
trap cont EXIT

FROZEN_AT=$(date --iso-8601=seconds)
kill -STOP "$PID"
# Confirm the process reached the stopped state.
for _ in 1 2 3 4 5 6 7 8 9 10; do
    state=$(awk '{print $3}' "/proc/$PID/stat" 2>/dev/null || echo "?")
    test "$state" = "T" && break
    sleep 0.1
done

capture_status=0
CAPTURED_AT=$(date --iso-8601=seconds)
cmd=${CAPTURE_CMD//\{out\}/$FRAME}
timeout "$CAPTURE_TIMEOUT" bash -c "$cmd" || capture_status=$?

kill -CONT "$PID" 2>/dev/null || true
resumed=true
trap - EXIT
RESUMED_AT=$(date --iso-8601=seconds)

FRAME_SHA=
FRAME_PRESENT=false
if test -f "$FRAME"; then
    FRAME_SHA=$(sha256sum -- "$FRAME" | awk '{print $1}')
    FRAME_PRESENT=true
fi

FROZEN_EPOCH=$(date -d "$FROZEN_AT" +%s%3N)
RESUMED_EPOCH=$(date -d "$RESUMED_AT" +%s%3N)
if test "$capture_status" -eq 0 && test "$FRAME_PRESENT" = true; then
    STATUS_STR=complete
else
    STATUS_STR=capture-failed
fi

jq -n \
    --arg run_id "$RUN_ID" --arg pid "$PID" \
    --argjson ownership "$OWNERSHIP" \
    --arg milestone "$MILESTONE" --argjson log_offset "$LOG_START_OFFSET" \
    --arg milestone_seen "$MILESTONE_SEEN_AT" \
    --arg frozen "$FROZEN_AT" --arg captured "$CAPTURED_AT" --arg resumed_at "$RESUMED_AT" \
    --argjson freeze_ms "$((RESUMED_EPOCH - FROZEN_EPOCH))" \
    --arg capture_cmd "$CAPTURE_CMD" --argjson capture_status "$capture_status" \
    --arg frame_path "$FRAME" --arg frame_sha "$FRAME_SHA" \
    --argjson frame_present "$FRAME_PRESENT" --arg status "$STATUS_STR" \
    '{run_id:$run_id,pid:($pid|tonumber),tool:"frozen-capture",
      ownership:$ownership,
      milestone:(if $milestone=="" then null else $milestone end),
      log_start_offset:$log_offset,
      milestone_seen_at:(if $milestone_seen=="" then null else $milestone_seen end),
      frozen_at:$frozen,captured_at:$captured,resumed_at:$resumed_at,
      freeze_duration_ms:$freeze_ms,
      capture_cmd:$capture_cmd,capture_status:$capture_status,
      frame_path:$frame_path,frame_sha256:(if $frame_sha=="" then null else $frame_sha end),
      frame_present:$frame_present,frame_committed:false,
      status:$status,
      artifacts:["metadata.json"]}' > "$RUN/metadata.json"

echo "$RUN_ID: capture_status=$capture_status frame_present=$FRAME_PRESENT"
test "$capture_status" -eq 0 || exit 1
