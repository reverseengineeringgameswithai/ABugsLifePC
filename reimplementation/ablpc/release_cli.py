"""Command line for M6 release build, verification, install, and rollback."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tarfile

from .release import (
    RELEASE_SPEC_RELATIVE,
    ReleaseError,
    build_release,
    current_release,
    install_release,
    rollback_release,
    verify_release,
)


def _json_ready(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ablpc-release")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="build a deterministic clean-source release")
    build.add_argument("--repo-root", type=Path, default=Path.cwd())
    build.add_argument("--spec", type=Path)
    build.add_argument("--output-dir", type=Path, required=True)

    verify = subparsers.add_parser("verify", help="verify an asset-free release archive")
    verify.add_argument("archive", type=Path)

    install = subparsers.add_parser("install", help="verify, install, and select a release")
    install.add_argument("archive", type=Path)
    install.add_argument("--install-root", type=Path, required=True)

    rollback = subparsers.add_parser("rollback", help="select the prior verified release")
    rollback.add_argument("--install-root", type=Path, required=True)

    current = subparsers.add_parser("current", help="report the selected verified release")
    current.add_argument("--install-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "build":
            root = args.repo_root.resolve()
            spec = args.spec or root.joinpath(*RELEASE_SPEC_RELATIVE.parts)
            result = build_release(spec, root, args.output_dir)
        elif args.command == "verify":
            verification = verify_release(args.archive)
            result = {key: verification[key] for key in (
                "release_id",
                "toolkit_version",
                "archive_sha256",
                "source_tree_sha256",
                "file_count",
            )}
        elif args.command == "install":
            result = install_release(args.archive, args.install_root)
        elif args.command == "rollback":
            result = rollback_release(args.install_root)
        else:
            result = current_release(args.install_root)
    except (OSError, ReleaseError, tarfile.TarError) as error:
        print(f"ablpc-release: {error}", file=sys.stderr)
        return 2
    print(json.dumps(_json_ready(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
