#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
GHIDRA_HOME=${GHIDRA_HOME:-"$ROOT/tools/ghidra/current"}
JAVA_HOME=${JAVA_HOME:-"$ROOT/tools/jdk/current"}
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"
ANALYZE="$GHIDRA_HOME/support/analyzeHeadless"
test -x "$ANALYZE" || { echo "Ghidra analyzeHeadless not found: $ANALYZE" >&2; exit 2; }
exec "$ANALYZE" "$@"
