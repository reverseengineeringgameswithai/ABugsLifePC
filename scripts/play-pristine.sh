#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
EXPECTED_EXE_SHA256=97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
AUTO_HARDWARE_EXE_SHA256=1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
AUTO_HARDWARE_CACHE="$ROOT/work/copies/auto-hardware/bugs.exe"
GAME_DIR="$ROOT/work/copies/BUGS_PC-full-disc/PC/BUGS"
PREFIX="$ROOT/work/wine/baseline"
OUTPUT_WIDTH=2560
OUTPUT_HEIGHT=1440
FILTER=nearest
RESEARCH=0
DRY_RUN=0
MUTE=0
WINDOWED=0
AUTO_HARDWARE=0
OUTPUT_SET=0
SINK_NAME="ablpc_mute_$$"

usage() {
    cat <<'EOF'
Usage: scripts/play-pristine.sh [OPTIONS]

Launch the unchanged PC executable under Wine inside an aspect-preserving
Gamescope session. The first selector's current state is not inferable from
pixels or an assumed default. Apply only the active experiment's preregistered
input sequence and classify the result from its complete renderer log gate.

Options:
  --game-dir DIR       Derived PC/BUGS work copy
  --prefix DIR         Wine prefix (default: work/wine/baseline)
  --output WIDTHxHEIGHT
                        Gamescope output size (default: 2560x1440)
  --filter FILTER      nearest or linear (default: nearest)
  --research           Add the tested log and cheat arguments
  --windowed           Run in a desktop window instead of fullscreen
                        (defaults the window to 1280x960 4:3 unless --output set)
  --mute               Route the game's audio to a private null sink so nothing
                        reaches the speakers. The game's audio subsystem still
                        runs normally (DirectSound init, track playback), so it
                        does not interfere with audio reverse engineering; only
                        the final output is discarded. Requires pactl.
  --auto-hardware      Build (or reuse) the guarded auto-hardware patched copy
                        and launch it so the game boots straight into hardware
                        Direct3D with no manual chooser. The patch edits only
                        the exe; retail assets are unchanged. Cached at
                        work/copies/auto-hardware/bugs.exe. (EXP-20260816-150/151)
  --dry-run            Validate and print the command without launching
  -h, --help            Show this help

The launcher verifies the executable SHA-256 and refuses paths outside
work/copies/. It never executes from originals/.
EOF
}

while test $# -gt 0; do
    case "$1" in
        --game-dir)
            test $# -ge 2 || { usage >&2; exit 2; }
            GAME_DIR=$2
            shift 2
            ;;
        --prefix)
            test $# -ge 2 || { usage >&2; exit 2; }
            PREFIX=$2
            shift 2
            ;;
        --output)
            test $# -ge 2 || { usage >&2; exit 2; }
            case "$2" in
                *x*) OUTPUT_WIDTH=${2%%x*}; OUTPUT_HEIGHT=${2#*x}; OUTPUT_SET=1 ;;
                *) usage >&2; exit 2 ;;
            esac
            shift 2
            ;;
        --filter)
            test $# -ge 2 || { usage >&2; exit 2; }
            FILTER=$2
            shift 2
            ;;
        --research) RESEARCH=1; shift ;;
        --windowed) WINDOWED=1; shift ;;
        --mute) MUTE=1; shift ;;
        --auto-hardware) AUTO_HARDWARE=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done

# In windowed mode, default to a modest 4:3 window unless the caller set --output.
if test "$WINDOWED" -eq 1 && test "$OUTPUT_SET" -eq 0; then
    OUTPUT_WIDTH=1280
    OUTPUT_HEIGHT=960
fi

case "$OUTPUT_WIDTH:$OUTPUT_HEIGHT" in
    *[!0-9:]*|:*|*:) echo "Output must be WIDTHxHEIGHT with positive integers" >&2; exit 2 ;;
esac
test "$OUTPUT_WIDTH" -gt 0 && test "$OUTPUT_HEIGHT" -gt 0 || {
    echo "Output dimensions must be positive" >&2
    exit 2
}
case "$FILTER" in
    nearest|linear) ;;
    *) echo "Filter must be nearest or linear" >&2; exit 2 ;;
esac

command -v gamescope >/dev/null || { echo "gamescope is required" >&2; exit 2; }
command -v wine >/dev/null || { echo "wine is required" >&2; exit 2; }
if test "$MUTE" -eq 1; then
    command -v pactl >/dev/null || { echo "--mute requires pactl (pipewire-pulse)" >&2; exit 2; }
fi

GAME_DIR=$(readlink -f -- "$GAME_DIR")
PREFIX=$(readlink -f -- "$PREFIX")
case "$GAME_DIR/" in
    "$ROOT/work/copies/"*) ;;
    *) echo "Refusing game directory outside work/copies/: $GAME_DIR" >&2; exit 2 ;;
esac

EXE="$GAME_DIR/bugs.exe"
test -f "$EXE" || { echo "Executable not found: $EXE" >&2; exit 2; }
test -d "$PREFIX" || { echo "Wine prefix not found: $PREFIX" >&2; exit 2; }
ACTUAL_EXE_SHA256=$(sha256sum -- "$EXE" | awk '{print $1}')
test "$ACTUAL_EXE_SHA256" = "$EXPECTED_EXE_SHA256" || {
    echo "Refusing unexpected bugs.exe SHA-256: $ACTUAL_EXE_SHA256" >&2
    exit 2
}

# Default: run the verified retail exe from the game directory. With
# --auto-hardware, build (or reuse) the guarded auto-hardware patched copy and
# run that instead; the retail assets under Y: are unchanged (the patch only
# edits the exe). Evidence: EXP-20260816-150/151.
EXE_RUN="./bugs.exe"
if test "$AUTO_HARDWARE" -eq 1; then
    PY="$ROOT/.venv/bin/python"
    test -x "$PY" || PY=python3
    mkdir -p "$(dirname -- "$AUTO_HARDWARE_CACHE")"
    if ! test -f "$AUTO_HARDWARE_CACHE" \
        || test "$(sha256sum -- "$AUTO_HARDWARE_CACHE" | awk '{print $1}')" \
            != "$AUTO_HARDWARE_EXE_SHA256"; then
        rm -f -- "$AUTO_HARDWARE_CACHE"
        "$PY" "$ROOT/scripts/make-auto-hardware" "$EXE" "$AUTO_HARDWARE_CACHE" \
            >/dev/null || {
            echo "Failed to build the auto-hardware executable" >&2
            exit 2
        }
    fi
    AH_SHA256=$(sha256sum -- "$AUTO_HARDWARE_CACHE" | awk '{print $1}')
    test "$AH_SHA256" = "$AUTO_HARDWARE_EXE_SHA256" || {
        echo "Refusing unexpected auto-hardware SHA-256: $AH_SHA256" >&2
        exit 2
    }
    EXE_RUN="$AUTO_HARDWARE_CACHE"
fi

GAME_ARGS=(mpeg)
if test "$RESEARCH" -eq 1; then
    GAME_ARGS=(log cheat mpeg)
fi

# Fullscreen unless windowed (a bare nested gamescope window is windowed).
FULLSCREEN_FLAG=(-f)
if test "$WINDOWED" -eq 1; then FULLSCREEN_FLAG=(); fi

# Wine environment; muting prepends the private null sink for this process.
WINE_ENV=("WINEPREFIX=$PREFIX" WINEDEBUG=-all)
if test "$MUTE" -eq 1; then WINE_ENV=("PULSE_SINK=$SINK_NAME" "${WINE_ENV[@]}"); fi

COMMAND=(
    gamescope --backend wayland
    -w 640 -h 480
    -W "$OUTPUT_WIDTH" -H "$OUTPUT_HEIGHT"
    -S fit -F "$FILTER" "${FULLSCREEN_FLAG[@]}"
    -- env "${WINE_ENV[@]}"
    wine "$EXE_RUN" "${GAME_ARGS[@]}"
)

echo "Verified bugs.exe: $ACTUAL_EXE_SHA256" >&2
echo "At the renderer selector, use only the experiment's preregistered sequence;" >&2
echo "do not infer selection from pixels or an assumed default." >&2
if test "$AUTO_HARDWARE" -eq 1; then
    echo "  Auto-hardware active: the patched build ($AUTO_HARDWARE_EXE_SHA256)" >&2
    echo "  selects Direct3D automatically; this is not a retail-executable control." >&2
fi
if test "$FILTER" = nearest; then
    echo "Presentation: aspect-preserving fit with crisp nearest-neighbor scaling." >&2
else
    echo "Presentation: aspect-preserving fit with softer linear scaling." >&2
fi

if test "$WINDOWED" -eq 1; then
    echo "Presentation: windowed (${OUTPUT_WIDTH}x${OUTPUT_HEIGHT} desktop window)." >&2
fi
if test "$MUTE" -eq 1; then
    echo "Audio: routed to a private null sink ($SINK_NAME); the game's audio" >&2
    echo "subsystem still runs, only the output is discarded." >&2
fi

if test "$DRY_RUN" -eq 1; then
    if test "$MUTE" -eq 1; then
        echo "# --mute would create null sink '$SINK_NAME' via pactl and remove it on exit" >&2
    fi
    printf 'cd %q\n' "$GAME_DIR"
    printf '%q ' "${COMMAND[@]}"
    printf '\n'
    exit 0
fi

cd "$GAME_DIR"

if test "$MUTE" -eq 1; then
    # Create a private null sink; the game outputs there (silent) with its audio
    # code path unchanged. Remove the sink on any exit path.
    MODULE_ID=$(pactl load-module module-null-sink \
        sink_name="$SINK_NAME" \
        sink_properties="device.description=ABLPC-Mute") || {
        echo "Failed to create null sink for --mute" >&2
        exit 2
    }
    cleanup_sink() { pactl unload-module "$MODULE_ID" 2>/dev/null || true; }
    trap cleanup_sink EXIT
    "${COMMAND[@]}"
    exit $?
fi

exec "${COMMAND[@]}"
