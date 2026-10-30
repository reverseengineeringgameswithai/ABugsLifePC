#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ORIGINALS="$ROOT/originals"
OUTPUT="$ROOT/hashes/SHA256SUMS"
mkdir -p "$ROOT/hashes"
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
while IFS= read -r -d '' file; do
    rel=${file#"$ORIGINALS/"}
    hash=$(sha256sum -- "$file" | awk '{print $1}')
    printf '%s  %s\n' "$hash" "$rel"
done < <(find "$ORIGINALS" -type f ! -name .gitkeep -print0 | sort -z) > "$tmp"
mv "$tmp" "$OUTPUT"
trap - EXIT
count=$(wc -l < "$OUTPUT")
printf 'Wrote %s hashes to %s; no original was modified.\n' "$count" "$OUTPUT"
