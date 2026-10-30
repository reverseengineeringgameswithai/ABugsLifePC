#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export JAVA_HOME=${JAVA_HOME:-"$ROOT/tools/jdk/current"}
export PATH="$JAVA_HOME/bin:$PATH"
exec "$ROOT/tools/ghidra/current/ghidraRun" "$@"
