SHELL := /bin/bash
PYTHON := .venv/bin/python

.PHONY: check doctor python-doctor vault-lint m4-compatibility audit-tracked hash-originals inventory-originals originals-readonly new-experiment test mod-help release-help smoke-help play-help harness-caps input-movie-caps coordinate-caps rr-help \
	briefing budget session-caps memory-caps keys-caps wait-caps session-audit session-list ghidra-index ghidra-stats run-index run-orphans install-hooks uninstall-hooks criu-caps criu-check savestate-caps savestate-list

check: python-doctor vault-lint m4-compatibility test audit-tracked
	@git diff --check
	@git diff --cached --check

doctor:
	@./scripts/doctor.sh

python-doctor:
	@$(PYTHON) python/smoke_imports.py

vault-lint:
	@$(PYTHON) scripts/vault-lint.py

m4-compatibility:
	@$(PYTHON) scripts/check-m4-compatibility.py

audit-tracked:
	@$(PYTHON) scripts/audit-tracked-files.py

hash-originals:
	@./scripts/hash-originals.sh

inventory-originals:
	@$(PYTHON) scripts/inventory-originals.py

originals-readonly:
	@./scripts/make-originals-readonly.sh

new-experiment:
	@test -n "$(QUESTION)" || { echo 'Usage: make new-experiment QUESTION="question"'; exit 2; }
	@$(PYTHON) scripts/new-experiment.py "$(QUESTION)"

test:
	@PYTHONPATH="$(CURDIR)/reimplementation:$${PYTHONPATH:-}" $(PYTHON) -m pytest -q tests

mod-help:
	@./scripts/ablpc-mod --help

release-help:
	@./scripts/ablpc-release --help

smoke-help:
	@./scripts/m6-smoke --help

play-help:
	@./scripts/play-pristine.sh --help

harness-caps:
	@$(PYTHON) scripts/gdb-harness.py --capabilities

input-movie-caps:
	@$(PYTHON) scripts/input-movie.py --capabilities

coordinate-caps:
	@$(PYTHON) scripts/coordinate-overlay.py --capabilities

rr-help:
	@./scripts/rr-record.sh --help || true

# --------------------------------------------------------------------------
# Session control (see Vault/10-Environment/PC autonomous game control.md)
# --------------------------------------------------------------------------

# Bounded startup context: the mandated reading set does not fit in a session,
# so read this first and follow its pointers.
briefing:
	@$(PYTHON) scripts/briefing.py brief $(if $(TASK),--task "$(TASK)",)

budget:
	@$(PYTHON) scripts/vault-lint.py --budget-only

session-caps:
	@$(PYTHON) scripts/game-session.py --capabilities

memory-caps:
	@$(PYTHON) scripts/game-memory.py --capabilities

criu-caps:
	@$(PYTHON) scripts/criu-feasibility.py --capabilities

# Read-only survey of whether a durable CRIU savestate is viable on this host.
criu-check:
	@$(PYTHON) scripts/criu-feasibility.py check

savestate-caps:
	@$(PYTHON) scripts/savestate-hotkeys.py --capabilities

# List existing in-session save states for the running game (needs --pid/--session).
savestate-list:
	@$(PYTHON) scripts/savestate-hotkeys.py list $(if $(PID),--pid $(PID),)

keys-caps:
	@$(PYTHON) scripts/send-keys.py --capabilities

wait-caps:
	@$(PYTHON) scripts/wait-for.py --capabilities

# Classify every runtime process and audio sink as owned by a recorded session
# or unattributed.  Run before launching and after closing.
session-audit:
	@$(PYTHON) scripts/game-session.py audit

session-list:
	@$(PYTHON) scripts/game-session.py list

# --------------------------------------------------------------------------
# Evidence and static-analysis indexes
# --------------------------------------------------------------------------

ghidra-index:
	@$(PYTHON) scripts/ghidra-query.py index

ghidra-stats:
	@$(PYTHON) scripts/ghidra-query.py stats

run-index:
	@$(PYTHON) scripts/run-index.py build --markdown reports/run-index.md

run-orphans:
	@$(PYTHON) scripts/run-index.py orphans

install-hooks:
	@./scripts/install-git-hooks.sh

uninstall-hooks:
	@./scripts/install-git-hooks.sh --uninstall
