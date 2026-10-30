#!/usr/bin/env bash
set -euo pipefail
ROOT=${ABLPC_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
PREFIX_NAME=baseline
CHANNELS="+loaddll,+seh,+timestamp"
CWD=
DEEP=0
SYSCALLS=0
RELAY_INCLUDE=
RELAY_EXCLUDE=
FILE_TRACE=0
RELAY_FLAGS=0
RELAY_ACTIVE=0
RELAY_HAD_INCLUDE=0
RELAY_HAD_EXCLUDE=0
RELAY_PRIOR_INCLUDE=
RELAY_PRIOR_EXCLUDE=
RUN=
usage() {
    echo "Usage: $0 [--prefix baseline|instrumented|compatibility] [--channels SPEC] [--cwd DIR] [--deep] [--strace] [--file-trace] [--relay-include LIST] [--relay-exclude LIST] -- executable [args...]" >&2
    echo "  --relay-include/--relay-exclude take Wine relay filter lists (semicolon-separated," >&2
    echo "  e.g. 'kernel32.CreateFileA;ddraw.*'). They mutate the prefix registry so they" >&2
    echo "  require --prefix instrumented and +relay in the channels; prior values are" >&2
    echo "  restored on exit." >&2
    exit 2
}

# Wine relay filtering is applied through HKCU\Software\Wine\Debug registry
# values, which persist in the prefix. These helpers query, set, and restore
# them so an instrumented run leaves the prefix as it found it.
_relay_reg() { WINEPREFIX="$PREFIX" WINEDEBUG=-all wine reg "$@"; }

_relay_query_prior() {
    local name=$1 out
    if out=$(_relay_reg query 'HKCU\Software\Wine\Debug' /v "$name" 2>/dev/null); then
        printf '%s\n' "$out" \
            | awk -F 'REG_SZ' '/REG_SZ/ {v=$2; sub(/^[ \t]+/,"",v); sub(/[ \t\r]+$/,"",v); print v; exit 0} END{exit 1}'
        return $?
    fi
    return 1
}

restore_relay() {
    test "$RELAY_ACTIVE" -eq 1 || return 0
    if test "$RELAY_HAD_INCLUDE" -eq 1; then
        _relay_reg add 'HKCU\Software\Wine\Debug' /v RelayInclude /t REG_SZ /d "$RELAY_PRIOR_INCLUDE" /f >/dev/null 2>&1 || true
    elif test -n "$RELAY_INCLUDE"; then
        _relay_reg delete 'HKCU\Software\Wine\Debug' /v RelayInclude /f >/dev/null 2>&1 || true
    fi
    if test "$RELAY_HAD_EXCLUDE" -eq 1; then
        _relay_reg add 'HKCU\Software\Wine\Debug' /v RelayExclude /t REG_SZ /d "$RELAY_PRIOR_EXCLUDE" /f >/dev/null 2>&1 || true
    elif test -n "$RELAY_EXCLUDE"; then
        _relay_reg delete 'HKCU\Software\Wine\Debug' /v RelayExclude /f >/dev/null 2>&1 || true
    fi
    RELAY_ACTIVE=0
    if test -n "$RUN" && test -f "$RUN/metadata.json"; then
        local t="$RUN/metadata.json.restore"
        jq '.relay_registry_restored=true' "$RUN/metadata.json" > "$t" && mv "$t" "$RUN/metadata.json"
    fi
}

while test $# -gt 0; do
    case "$1" in
        --prefix) PREFIX_NAME=${2:-}; shift 2 ;;
        --channels) CHANNELS=${2:-}; shift 2 ;;
        --cwd) CWD=${2:-}; shift 2 ;;
        --deep) DEEP=1; shift ;;
        --strace) SYSCALLS=1; shift ;;
        --file-trace) FILE_TRACE=1; shift ;;
        --relay-include) RELAY_INCLUDE=${2:-}; shift 2 ;;
        --relay-exclude) RELAY_EXCLUDE=${2:-}; shift 2 ;;
        --) shift; break ;;
        *) usage ;;
    esac
done
test $# -gt 0 || usage
case "$PREFIX_NAME" in baseline|instrumented|compatibility) ;; *) usage ;; esac
command -v wine >/dev/null || { echo "wine is required" >&2; exit 2; }
if test "$SYSCALLS" -eq 1; then
    command -v strace >/dev/null || { echo "--strace requested but strace is not installed" >&2; exit 2; }
fi
EXE=$(readlink -f -- "$1")
shift
test -f "$EXE" || { echo "Executable not found: $EXE" >&2; exit 2; }
case "$EXE" in
    "$ROOT/originals"/*) echo "Refusing to execute from originals/. Use a copy under work/copies/." >&2; exit 2 ;;
esac
if test "$DEEP" -eq 1; then CHANNELS="+relay,+snoop,+loaddll,+seh,+timestamp"; fi
if test "$FILE_TRACE" -eq 1; then
    case ",$CHANNELS," in
        *,+file,*) ;;
        *) if test -n "$CHANNELS"; then CHANNELS="$CHANNELS,+file"; else CHANNELS="+file"; fi ;;
    esac
fi
if test -n "$RELAY_INCLUDE" || test -n "$RELAY_EXCLUDE"; then RELAY_FLAGS=1; fi
if test "$RELAY_FLAGS" -eq 1; then
    if test "$PREFIX_NAME" = baseline; then
        echo "Refusing relay filters on the baseline prefix: they mutate HKCU\\Software\\Wine\\Debug. Use --prefix instrumented." >&2
        exit 2
    fi
    case ",$CHANNELS," in
        *,+relay,*) ;;
        *) echo "Relay filters require +relay in the channels (use --deep or --channels '+relay,...')." >&2; exit 2 ;;
    esac
fi
PREFIX="$ROOT/work/wine/$PREFIX_NAME"
test -d "$PREFIX" || { echo "Prefix does not exist; run scripts/wine-new-prefix.sh first" >&2; exit 2; }
CWD=${CWD:-$(dirname "$EXE")}
CWD=$(readlink -f -- "$CWD")
STAMP=$(date +%Y%m%d-%H%M%S)
RUN_ID="RUN-WINE-$STAMP"
RUN="$ROOT/dynamic/wine/$RUN_ID"
test ! -e "$RUN" || { echo "Run already exists: $RUN" >&2; exit 2; }
mkdir -p "$RUN"
if test "$RELAY_FLAGS" -eq 1; then
    trap restore_relay EXIT
    if PRIOR=$(_relay_query_prior RelayInclude); then RELAY_HAD_INCLUDE=1; RELAY_PRIOR_INCLUDE=$PRIOR; fi
    if PRIOR=$(_relay_query_prior RelayExclude); then RELAY_HAD_EXCLUDE=1; RELAY_PRIOR_EXCLUDE=$PRIOR; fi
    RELAY_ACTIVE=1
    if test -n "$RELAY_INCLUDE"; then
        _relay_reg add 'HKCU\Software\Wine\Debug' /v RelayInclude /t REG_SZ /d "$RELAY_INCLUDE" /f >/dev/null 2>&1
    fi
    if test -n "$RELAY_EXCLUDE"; then
        _relay_reg add 'HKCU\Software\Wine\Debug' /v RelayExclude /t REG_SZ /d "$RELAY_EXCLUDE" /f >/dev/null 2>&1
    fi
fi
STARTED=$(date --iso-8601=seconds)
WINE_VERSION=$(wine --version)
EXE_SHA=$(sha256sum -- "$EXE" | awk '{print $1}')
if test -f "$CWD/bugs.log"; then
    GAME_LOG_BEFORE=$(sha256sum -- "$CWD/bugs.log" | awk '{print $1}')
else
    GAME_LOG_BEFORE=
fi
if test "$SYSCALLS" -eq 1; then
    SYSCALL_MODE=strace
else
    SYSCALL_MODE=disabled
fi
jq -n \
    --arg run_id "$RUN_ID" --arg started "$STARTED" --arg exe "$EXE" \
    --arg sha "$EXE_SHA" --arg cwd "$CWD" --arg prefix "$PREFIX" \
    --arg wine "$WINE_VERSION" --arg channels "$CHANNELS" --arg syscalls "$SYSCALL_MODE" \
    --argjson argv "$(printf '%s\0' "$EXE" "$@" | jq -Rs 'split("\u0000")[:-1]')" \
    '{run_id:$run_id,started:$started,executable:$exe,executable_sha256:$sha,argv:$argv,
      environment:"Wine",environment_version:$wine,working_directory:$cwd,
      prefix:$prefix,wine_debug_channels:$channels,syscall_capture:$syscalls,status:"running"}' > "$RUN/metadata.json"
if test "$FILE_TRACE" -eq 1 || test "$RELAY_FLAGS" -eq 1; then
    add_tmp="$RUN/metadata.json.add"
    jq \
        --argjson file_trace "$(test "$FILE_TRACE" -eq 1 && echo true || echo false)" \
        --argjson relay_flags "$RELAY_FLAGS" \
        --arg ri "$RELAY_INCLUDE" --arg re "$RELAY_EXCLUDE" \
        --argjson rhi "$RELAY_HAD_INCLUDE" --arg rpi "$RELAY_PRIOR_INCLUDE" \
        --argjson rhe "$RELAY_HAD_EXCLUDE" --arg rpe "$RELAY_PRIOR_EXCLUDE" \
        '(if $file_trace then .file_trace=true else . end)
         | (if $relay_flags == 1 then
              .relay_include=(if $ri=="" then null else $ri end)
              | .relay_exclude=(if $re=="" then null else $re end)
              | .relay_prior_include=(if $rhi==1 then $rpi else null end)
              | .relay_prior_exclude=(if $rhe==1 then $rpe else null end)
              | .relay_registry_restored=false
            else . end)' \
        "$RUN/metadata.json" > "$add_tmp"
    mv "$add_tmp" "$RUN/metadata.json"
fi
cat > "$RUN/experiment.md" <<EOF
# $RUN_ID

- Binary SHA-256: \`$EXE_SHA\`
- Environment: \`$WINE_VERSION\`
- Prefix: \`$PREFIX_NAME\`
- Working directory: \`$CWD\`
- Wine debug channels: \`$CHANNELS\`
- Started: \`$STARTED\`

## Procedure

Run the recorded argv under Wine with the configured Wine debug channels and optional syscall capture.

## Expected

Record before execution.

## Observed

Pending.

## Artifacts

- \`metadata.json\`
- \`stdout.txt\`
- \`stderr.txt\`
- \`wine-debug.txt\`
- Syscall capture: \`$SYSCALL_MODE\`
EOF
if test "$SYSCALLS" -eq 1; then
    cat >> "$RUN/experiment.md" <<EOF
- \`strace.txt\`
EOF
fi
set +e
if test "$SYSCALLS" -eq 1; then
    (
        cd "$CWD"
        WINEPREFIX="$PREFIX" WINEDEBUG="$CHANNELS" \
            strace -f -e trace=process,file,network -o "$RUN/strace.txt" \
            wine "$EXE" "$@" \
            > >(tee "$RUN/stdout.txt") \
            2> >(tee "$RUN/stderr.txt" "$RUN/wine-debug.txt" >&2)
    )
else
    (
        cd "$CWD"
        WINEPREFIX="$PREFIX" WINEDEBUG="$CHANNELS" \
            wine "$EXE" "$@" \
            > >(tee "$RUN/stdout.txt") \
            2> >(tee "$RUN/stderr.txt" "$RUN/wine-debug.txt" >&2)
    )
fi
STATUS=$?
set -e
ENDED=$(date --iso-8601=seconds)
GAME_LOG_CAPTURED=0
if test -f "$CWD/bugs.log"; then
    GAME_LOG_AFTER=$(sha256sum -- "$CWD/bugs.log" | awk '{print $1}')
    if test "$GAME_LOG_AFTER" != "$GAME_LOG_BEFORE"; then
        cp -- "$CWD/bugs.log" "$RUN/bugs.log"
        GAME_LOG_CAPTURED=1
    fi
fi
tmp="$RUN/metadata.json.tmp"
jq --arg ended "$ENDED" --argjson status "$STATUS" --argjson game_log "$GAME_LOG_CAPTURED" \
    '.ended=$ended | .exit_status=$status | .status="complete"
     | .artifacts=["metadata.json","stdout.txt","stderr.txt","wine-debug.txt"]
     | if $game_log == 1 then .artifacts += ["bugs.log"] else . end' \
    "$RUN/metadata.json" > "$tmp"
mv "$tmp" "$RUN/metadata.json"
cat >> "$RUN/experiment.md" <<EOF

## Capture result

- Ended: \`$ENDED\`
- Exit status: \`$STATUS\`
- Game log copied: \`$GAME_LOG_CAPTURED\`

Interpretation is intentionally left for a linked experiment note.
EOF
echo "$RUN_ID: exit status $STATUS"
exit "$STATUS"
