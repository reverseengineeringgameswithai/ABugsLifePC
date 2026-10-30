#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
test $# -eq 1 || { echo "Usage: $0 /path/to/copy.exe" >&2; exit 2; }
INPUT=$(readlink -f -- "$1")
test -f "$INPUT" || { echo "Not a regular file: $INPUT" >&2; exit 2; }
case "$INPUT" in
    "$ROOT/originals"/*) echo "Refusing to triage in place under originals/. Copy it to work/copies/ first." >&2; exit 2 ;;
esac
SHA=$(sha256sum -- "$INPUT" | awk '{print $1}')
ID="BIN-${SHA:0:16}"
OUT="$ROOT/static/pe/$ID"
test ! -e "$OUT" || { echo "Output already exists: $OUT" >&2; exit 2; }
mkdir -p "$OUT"

printf '%s  %s\n' "$SHA" "$(basename "$INPUT")" > "$OUT/SHA256SUMS"
file -- "$INPUT" > "$OUT/file.txt"
"$ROOT/.venv/bin/python" "$ROOT/python/pe_report.py" "$INPUT" > "$OUT/pefile.json"

OBJDUMP=
for candidate in i686-w64-mingw32-objdump x86_64-w64-mingw32-objdump objdump; do
    if command -v "$candidate" >/dev/null; then OBJDUMP=$candidate; break; fi
done
if test -n "$OBJDUMP"; then
    "$OBJDUMP" -x "$INPUT" > "$OUT/objdump.txt" 2>&1 || true
fi
if command -v rabin2 >/dev/null; then
    rabin2 -Ij "$INPUT" > "$OUT/rabin2-info.json" 2>&1 || true
    rabin2 -Sj "$INPUT" > "$OUT/rabin2-sections.json" 2>&1 || true
    rabin2 -ij "$INPUT" > "$OUT/rabin2-imports.json" 2>&1 || true
    rabin2 -Ej "$INPUT" > "$OUT/rabin2-exports.json" 2>&1 || true
    rabin2 -zzj "$INPUT" > "$OUT/rabin2-strings.json" 2>&1 || true
fi
strings -a -n 4 -- "$INPUT" > "$OUT/strings.txt"
cat > "$OUT/README.md" <<EOF
# $ID PE triage

- Input basename: \`$(basename "$INPUT")\`
- SHA-256: \`$SHA\`
- Input was read only; this workflow did not modify it.
- Independent views: \`file.txt\`, \`pefile.json\`, \`objdump.txt\`, and available radare2 JSON.
EOF
echo "$OUT"
