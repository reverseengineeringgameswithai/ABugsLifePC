#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ORIGINALS="$ROOT/originals"
if ! find "$ORIGINALS" -type f ! -name .gitkeep -print -quit | grep -q .; then
    echo "No original files found; nothing changed."
    exit 0
fi
echo "This opt-in command removes write bits from files under $ORIGINALS."
read -r -p "Type READONLY to continue: " answer
test "$answer" = READONLY || { echo "Cancelled."; exit 1; }
find "$ORIGINALS" -type f ! -name .gitkeep -exec chmod a-w -- {} +
echo "Original files are now read-only where filesystem permissions permit."
