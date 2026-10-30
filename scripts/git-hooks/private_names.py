#!/usr/bin/env python3
"""Refuse commits and pushes that would publish a private name.

Names come from .git/info/private-names (one per line; blank lines and lines
starting with # are ignored). Git never pushes .git/info, so the list stays
local. A name matches case-insensitively as plain bytes, as UTF-16 (either byte
order), as hex (either digit case, optional separators or 0x/\\x prefixes) and
as base64 (standard or URL-safe, any alignment, for the lower, capitalised and
upper spellings). File contents, binary files included, file paths, commit
messages and author/committer identities are all checked. Reports name the
commit, the kind of match and the path with every match redacted, so they are
safe to print in public CI logs.

Modes:
  staged     the index (pre-commit)
  push       the commits git's pre-push hook names on stdin
  pending    local commits not reachable from any remote-tracking ref
  history    every commit reachable from any ref
Options:
  --require-list  fail closed when the list is missing or empty

Exit codes: 0 clean, 1 a private name was found, 2 usage error,
3 the check could not run (treated as a refusal by every caller).
"""
from __future__ import annotations

import base64
import re
import subprocess
import sys

ZERO = "0" * 40


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", *args], input=data, capture_output=True, check=True).stdout


def load_names(require: bool) -> list[bytes]:
    path = git("rev-parse", "--git-path", "info/private-names").decode().strip()
    try:
        lines = open(path, "rb").read().splitlines()
    except FileNotFoundError:
        lines = []
    names = [l.strip() for l in lines if l.strip() and not l.strip().startswith(b"#")]
    if require and not names:
        print("private-names: no names listed in .git/info/private-names", file=sys.stderr)
        sys.exit(3)
    return names


def ascii_class(byte: int) -> bytes:
    ch = bytes([byte])
    if ch.isalpha():
        return b"[" + ch.lower() + ch.upper() + b"]"
    return re.escape(ch)


def patterns(names: list[bytes]) -> tuple[re.Pattern, re.Pattern]:
    folded, exact = [], []
    for name in names:
        folded.append(re.escape(name))
        folded.append(b"".join(ascii_class(b) + b"\x00" for b in name))
        folded.append(b"".join(b"\x00" + ascii_class(b) for b in name))
        hex_bytes = []
        for b in name:
            ch = bytes([b])
            options = {ch.lower().hex().encode(), ch.upper().hex().encode()}
            hex_bytes.append(b"(?:0x|\\\\x)?(?:" + b"|".join(sorted(options)) + b")")
        folded.append(b"[\\s:,-]?".join(hex_bytes))
        for spelling in {name.lower(), name.capitalize(), name.upper()}:
            for align in range(3):
                for encode in (base64.b64encode, base64.urlsafe_b64encode):
                    encoded = encode(b"\x00" * align + spelling)
                    core = encoded[(0, 2, 3)[align]:((align + len(spelling)) * 8) // 6]
                    if len(core) >= 4:
                        exact.append(re.escape(core))
    return (re.compile(b"|".join(folded), re.IGNORECASE),
            re.compile(b"|".join(sorted(set(exact)))))


class Scanner:
    def __init__(self, names: list[bytes]):
        self.folded, self.exact = patterns(names)
        self.blob_hits: dict[str, bool] = {}
        self.found = 0

    def hit(self, data: bytes) -> bool:
        return bool(self.folded.search(data) or self.exact.search(data))

    def redact(self, text: bytes) -> str:
        return self.exact.sub(b"<private>", self.folded.sub(b"<private>", text)).decode(errors="replace")

    def report(self, where: str, kind: str, path: bytes = b"") -> None:
        self.found += 1
        suffix = f": {self.redact(path)}" if path else ""
        print(f"private-names: {where} {kind}{suffix}", file=sys.stderr)

    def blobs(self, shas: list[str]) -> None:
        todo = sorted({s for s in shas if s not in self.blob_hits})
        if not todo:
            return
        out = git("cat-file", "--batch", data="".join(s + "\n" for s in todo).encode())
        pos = 0
        for sha in todo:
            header_end = out.index(b"\n", pos)
            size = int(out[pos:header_end].split()[2])
            body = out[header_end + 1:header_end + 1 + size]
            self.blob_hits[sha] = self.hit(body)
            pos = header_end + 1 + size + 1

    def tree(self, where: str, entries: list[tuple[str, bytes]]) -> None:
        self.blobs([sha for sha, _ in entries])
        for sha, path in entries:
            if self.hit(path):
                self.report(where, "path", path)
            elif self.blob_hits[sha]:
                self.report(where, "content", path)

    def commit(self, sha: str) -> None:
        where = f"commit {sha[:12]}"
        meta = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%B", sha)
        if self.hit(meta):
            self.report(where, "message or identity")
        entries = []
        for rec in git("ls-tree", "-r", "-z", sha).split(b"\0"):
            if rec:
                info, path = rec.split(b"\t", 1)
                mode, kind, obj = info.split()
                if kind == b"blob":
                    entries.append((obj.decode(), path))
        self.tree(where, entries)


def commits_for_push(scanner: Scanner) -> list[str]:
    shas: list[str] = []
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) != 4:
            continue
        local_ref, local_sha, remote_ref, remote_sha = parts
        if local_sha == ZERO:
            continue
        if scanner.hit(local_ref.encode()) or scanner.hit(remote_ref.encode()):
            scanner.report("ref", "name")
        known = remote_sha != ZERO and subprocess.run(
            ["git", "cat-file", "-e", remote_sha + "^{commit}"], capture_output=True).returncode == 0
        spec = [f"{remote_sha}..{local_sha}"] if known else [local_sha]
        shas += git("rev-list", *spec).decode().split()
    return shas


def main(argv: list[str]) -> int:
    modes = {"staged", "push", "pending", "history"}
    args = [a for a in argv if a != "--require-list"]
    if len(args) != 1 or args[0] not in modes:
        print(__doc__, file=sys.stderr)
        return 2
    mode = args[0]
    names = load_names("--require-list" in argv)
    if not names:
        return 0
    scanner = Scanner(names)
    if mode == "staged":
        entries = []
        for rec in git("ls-files", "-s", "-z").split(b"\0"):
            if rec:
                info, path = rec.split(b"\t", 1)
                entries.append((info.split()[1].decode(), path))
        scanner.tree("staged", entries)
    else:
        if mode == "push":
            shas = commits_for_push(scanner)
        elif mode == "pending":
            shas = git("rev-list", "--branches", "--tags", "--not", "--remotes").decode().split()
        else:
            shas = git("rev-list", "--all").decode().split()
        for sha in dict.fromkeys(shas):
            scanner.commit(sha)
    if scanner.found:
        print(f"private-names: refused ({scanner.found} match(es)); remove them before "
              "committing or pushing", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
        print(f"private-names: check could not run: {exc}", file=sys.stderr)
        sys.exit(3)
