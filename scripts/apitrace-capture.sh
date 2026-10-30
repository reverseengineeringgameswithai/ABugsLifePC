#!/usr/bin/env bash
# Trace the GL stream a Wine run produces, for renderer-fidelity questions.
#
# This system's apitrace ships only GL wrappers (no Windows/ddraw wrapper DLL).
# Under Wine WoW64, wined3d executes the game's ddraw as host GL on the 64-bit
# unix side, so an LD_PRELOADed glxtrace captures exactly what wined3d emits:
# the GL texture uploads and formats behind KU-012's texture-translation
# question. This is complementary to `wine-capture.sh --relay-include ddraw.*`,
# which records the Windows-side ddraw API surface.
#
# Trace files contain rendered game content and are written under the
# git-ignored work/apitrace/ tree; only metadata and hashes are committed.
set -euo pipefail
ROOT=${ABLPC_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
PREFIX_NAME=baseline
CWD=
API=gl
CHANNELS="+timestamp"
APITRACE_BIN=${APITRACE_BIN:-apitrace}
APITRACE_WRAPPER_DIR=${APITRACE_WRAPPER_DIR:-/usr/lib64/apitrace/wrappers}

usage() {
    cat >&2 <<'EOF'
Usage: apitrace-capture.sh [--prefix baseline|instrumented|compatibility]
         [--cwd DIR] [--api gl|egl] [--channels SPEC] -- executable [args...]

Traces the GL stream wined3d emits under Wine. v1 runs without gamescope for a
simpler capture chain. Trace files land under work/apitrace/; a RUN-APITRACE
metadata record is written under dynamic/wine/.
EOF
    exit 2
}

refuse() {
    local reason=$1 detail=${2:-}
    printf '{"refused":true,"tool":"apitrace-capture","reason":"%s","detail":"%s"}\n' \
        "$reason" "$detail"
    exit 3
}

while test $# -gt 0; do
    case "$1" in
        --prefix) PREFIX_NAME=${2:-}; shift 2 ;;
        --cwd) CWD=${2:-}; shift 2 ;;
        --api) API=${2:-}; shift 2 ;;
        --channels) CHANNELS=${2:-}; shift 2 ;;
        --help|-h) usage ;;
        --) shift; break ;;
        *) usage ;;
    esac
done
test $# -gt 0 || usage
case "$PREFIX_NAME" in baseline|instrumented|compatibility) ;; *) usage ;; esac
case "$API" in gl|egl) ;; *) usage ;; esac

command -v "$APITRACE_BIN" >/dev/null || refuse "apitrace_missing" "install apitrace"
# apitrace wrapper file names: GL is glxtrace.so, EGL is egltrace.so.
case "$API" in
    gl) WRAPPER_NAME=glxtrace.so ;;
    egl) WRAPPER_NAME=egltrace.so ;;
esac
WRAPPER="$APITRACE_WRAPPER_DIR/$WRAPPER_NAME"
test -f "$WRAPPER" || refuse "wrapper_missing" "$WRAPPER not found"

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
RUN_ID="RUN-APITRACE-$STAMP"
RUN="$ROOT/dynamic/wine/$RUN_ID"
test ! -e "$RUN" || { echo "Run already exists: $RUN" >&2; exit 2; }
TRACE_DIR="$ROOT/work/apitrace/$RUN_ID"
test ! -e "$TRACE_DIR" || { echo "Trace already exists: $TRACE_DIR" >&2; exit 2; }
mkdir -p "$RUN" "$TRACE_DIR"
TRACE="$TRACE_DIR/bugs.trace"

STARTED=$(date --iso-8601=seconds)
APITRACE_VERSION=$("$APITRACE_BIN" version 2>&1 | head -n 1 || echo unknown)
WINE_VERSION=$(wine --version 2>/dev/null || echo unknown)
EXE_SHA=$(sha256sum -- "$EXE" | awk '{print $1}')
argv_json=$(printf '%s\n' "$EXE" "$@" | jq -R . | jq -s .)

jq -n \
    --arg run_id "$RUN_ID" --arg started "$STARTED" --arg exe "$EXE" \
    --arg sha "$EXE_SHA" --arg cwd "$CWD" --arg prefix "$PREFIX" \
    --arg wine "$WINE_VERSION" --arg channels "$CHANNELS" \
    --arg tracer "$APITRACE_VERSION" --arg api "$API" --arg wrapper "$WRAPPER" \
    --argjson argv "$argv_json" \
    '{run_id:$run_id,started:$started,executable:$exe,executable_sha256:$sha,argv:$argv,
      environment:"Wine",environment_version:$wine,working_directory:$cwd,
      prefix:$prefix,wine_debug_channels:$channels,
      tracer:"apitrace",tracer_version:$tracer,api:$api,wrapper_path:$wrapper,
      rationale:"apitrace ships only GL wrappers; under WoW64 wined3d runs the game ddraw as host GL, so glxtrace captures the wined3d GL translation stream (KU-012). Complementary to wine-capture relay ddraw.*",
      status:"running"}' > "$RUN/metadata.json"

set +e
(
    cd "$CWD"
    WINEPREFIX="$PREFIX" WINEDEBUG="$CHANNELS" \
        "$APITRACE_BIN" trace --api "$API" --output "$TRACE" -- wine "$EXE" "$@" \
        > >(tee "$RUN/stdout.txt") \
        2> >(tee "$RUN/stderr.txt" >&2)
)
STATUS=$?
set -e
ENDED=$(date --iso-8601=seconds)

# apitrace suffixes extra processes (bugs.1.trace, ...): hash every trace.
traces_json="[]"
for f in "$TRACE_DIR"/*.trace; do
    test -f "$f" || continue
    sha=$(sha256sum -- "$f" | awk '{print $1}')
    size=$(stat -c %s "$f")
    rel="work/apitrace/$RUN_ID/$(basename "$f")"
    traces_json=$(jq --arg p "$rel" --arg s "$sha" --argjson z "$size" \
        '. + [{path:$p,sha256:$s,size_bytes:$z}]' <<<"$traces_json")
done

tmp="$RUN/metadata.json.tmp"
jq --arg ended "$ENDED" --argjson status "$STATUS" --argjson traces "$traces_json" \
    '.ended=$ended | .exit_status=$status | .status="complete"
     | .traces=$traces
     | .artifacts=["metadata.json","stdout.txt","stderr.txt"]' \
    "$RUN/metadata.json" > "$tmp"
mv "$tmp" "$RUN/metadata.json"

echo "$RUN_ID: exit status $STATUS ($(jq '.traces|length' "$RUN/metadata.json") trace file(s))"
exit "$STATUS"
