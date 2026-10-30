#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export JAVA_HOME=${JAVA_HOME:-"$ROOT/tools/jdk/current"}
export PATH="$JAVA_HOME/bin:$PATH"
export GHIDRA_INSTALL_DIR=${GHIDRA_INSTALL_DIR:-"$ROOT/tools/ghidra/current"}
exec "$ROOT/tools/ghidra/.venv/bin/python" -m pyghidra --install-dir "$GHIDRA_INSTALL_DIR" "$@"
