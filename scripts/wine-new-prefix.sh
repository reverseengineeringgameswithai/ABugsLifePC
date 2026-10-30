#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
usage() { echo "Usage: $0 [--prepare-only] {baseline|instrumented|compatibility}" >&2; exit 2; }
PREPARE=0
if test "${1:-}" = --prepare-only; then PREPARE=1; shift; fi
test $# -eq 1 || usage
case "$1" in baseline|instrumented|compatibility) NAME=$1 ;; *) usage ;; esac
PREFIX="$ROOT/work/wine/$NAME"
mkdir -p "$PREFIX"
if test "$PREPARE" -eq 1; then
    echo "Prepared empty prefix directory: $PREFIX"
    exit 0
fi
if find "$PREFIX" -mindepth 1 -print -quit | grep -q .; then
    echo "Refusing to mutate non-empty prefix: $PREFIX" >&2
    exit 2
fi
WINEPREFIX="$PREFIX" WINEDEBUG=-all wineboot --init
echo "Initialized baseline Wine prefix: $PREFIX"
