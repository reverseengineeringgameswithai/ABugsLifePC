#!/usr/bin/env bash
# Install (or remove) the tracked ABLPC git hooks.
#
# The hooks live in `scripts/git-hooks/`, which is tracked, reviewable and
# shared, unlike `.git/hooks/`. Installation only sets `core.hooksPath` to that
# directory, so it is a single reversible repository-local config entry and no
# file is copied into `.git/`.
#
# Exit codes: 0 success (including a no-op re-install), 2 usage error,
# 3 structured refusal (a conflicting hooksPath is already configured, or the
# hook directory is unusable).
set -euo pipefail
ROOT=${ABLPC_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
HOOKS_REL=scripts/git-hooks
MODE=install

usage() {
    cat >&2 <<'EOF'
Usage: install-git-hooks.sh [--uninstall] [--help]

Points this repository's core.hooksPath at the tracked scripts/git-hooks
directory, which installs the fast pre-commit gate (git diff --check,
audit-tracked-files.py, vault-lint.py, compileall of staged Python).

  (no option)  install; idempotent, refuses if another hooksPath is set
  --uninstall  unset core.hooksPath if it is ours; refuses if it is not
  --help       this text

Bypass the hook for one commit with `git commit --no-verify`.

Exit codes: 0 success, 2 usage error, 3 structured refusal.
EOF
    exit 2
}

refuse() {
    # $1 reason, $2 remedy, plus key=value extras
    local reason=$1 remedy=$2
    shift 2
    printf '{"refused":true,"tool":"install-git-hooks","reason":"%s","remedy":"%s"' \
        "$reason" "$remedy"
    while test $# -gt 0; do printf ',%s' "$1"; shift; done
    printf '}\n'
    exit 3
}

while test $# -gt 0; do
    case "$1" in
        --uninstall) MODE=uninstall; shift ;;
        --help|-h) usage ;;
        *) usage ;;
    esac
done

cd "$ROOT"
git rev-parse --git-dir >/dev/null 2>&1 || refuse "not_a_git_repository" \
    "run this from inside an ABLPC clone" "root=\"$ROOT\""

current=$(git config --local --get core.hooksPath || true)

if test "$MODE" = uninstall; then
    if test -z "$current"; then
        echo "install-git-hooks: core.hooksPath is not set; nothing to remove"
        exit 0
    fi
    if test "$current" != "$HOOKS_REL"; then
        refuse "foreign_hooks_path" \
            "core.hooksPath belongs to another tool; unset it yourself if intended" \
            "\"configured\":\"$current\"" "\"expected\":\"$HOOKS_REL\""
    fi
    git config --local --unset core.hooksPath
    echo "install-git-hooks: removed core.hooksPath ($HOOKS_REL)"
    echo "install-git-hooks: git now uses the default .git/hooks again"
    exit 0
fi

test -d "$ROOT/$HOOKS_REL" || refuse "hooks_directory_missing" \
    "expected the tracked hook directory" "\"path\":\"$ROOT/$HOOKS_REL\""
test -x "$ROOT/$HOOKS_REL/pre-commit" || refuse "hook_not_executable" \
    "chmod +x $HOOKS_REL/pre-commit" "\"path\":\"$ROOT/$HOOKS_REL/pre-commit\""

if test "$current" = "$HOOKS_REL"; then
    echo "install-git-hooks: already installed (core.hooksPath=$HOOKS_REL)"
    exit 0
fi
if test -n "$current"; then
    refuse "conflicting_hooks_path" \
        "another core.hooksPath is configured; remove it first or keep it" \
        "\"configured\":\"$current\"" "\"expected\":\"$HOOKS_REL\""
fi

git config --local core.hooksPath "$HOOKS_REL"
echo "install-git-hooks: core.hooksPath=$HOOKS_REL"
echo "install-git-hooks: installed hooks:"
for hook in "$ROOT/$HOOKS_REL"/*; do
    test -f "$hook" || continue
    echo "  $(basename "$hook")"
done
echo "install-git-hooks: bypass one commit with 'git commit --no-verify'"
echo "install-git-hooks: reverse with 'scripts/install-git-hooks.sh --uninstall'"
