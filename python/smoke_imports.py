#!/usr/bin/env python3
import importlib
import importlib.metadata
import sys

MODULES = {
    "pefile": "pefile",
    "lief": "lief",
    "capstone": "capstone",
    "construct": "construct",
    "rich": "rich",
    "pytest": "pytest",
    "hypothesis": "hypothesis",
    "yaml": "PyYAML",
    "pydantic": "pydantic",
    "networkx": "networkx",
    "unicorn": "unicorn",
}

failed = []
for module_name, distribution in MODULES.items():
    try:
        importlib.import_module(module_name)
        try:
            version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            version = "version unavailable"
        print(f"{module_name}: {version}")
    except Exception as exc:
        failed.append((module_name, exc))
        print(f"{module_name}: FAILED: {exc}", file=sys.stderr)

if failed:
    raise SystemExit(1)
print(f"Python: {sys.version.split()[0]}")
