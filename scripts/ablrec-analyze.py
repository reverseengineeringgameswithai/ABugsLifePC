#!/usr/bin/env python3
"""Offline analysis for the ABLREC flight-recorder write-trace (Phase 2).

Reads a `SIGUSR1` dump (default ``work/86box/logs/ablrec.txt``) produced by the
86Box ABLREC patch (``tools/86box/patches/86box-v6.0-ablrec.patch``,
DEC-20260818-149) and answers forensic questions about who wrote a guest global:

  who-wrote <addr>   writers of an address (grouped by writer EIP), with counts
  timeline <addr>    chronological old->new value history for one address
  writers            the writer census (every writer EIP and what it touched)
  cr3-split          record counts per CR3 (separates game from boot writes)
  name <eip...>      resolve writer EIPs to their instruction + Ghidra function

Parsing and the queries are pure (see the fixture tests in
``tests/test_ablrec_analyze.py``); ``--name`` / ``name`` enrichment is live
(needs ``objdump`` + the game executable + the Ghidra export index).

Semantics / limitations (documented on purpose):
- Records match a query address by byte OVERLAP: a write of ``width`` bytes at
  ``r.addr`` matches query ``[addr, addr+qwidth)`` iff the ranges overlap.
- ``timeline`` chains records with the *exact* same ``addr`` in ``tsc`` order and
  derives ``old`` as the previous record's ``val``. The first record's ``old`` is
  **unknown** (the trace is a bounded ring window), reported as ``?`` not ``0``.
- ``val`` is the value the instruction wrote; for widths < 4 it is the written
  low bytes, not the reconstructed full field.
- ``--cr3`` defaults to the ABL game space ``0x00454000``; pass ``all`` to include
  boot/other-process writes. The recorder logs CR3 per record so this is a filter,
  not an assumption.
- Containing-function resolution uses the nearest function entry <= EIP (the
  Ghidra export has no per-function size), so it is APPROXIMATE and labelled so.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME_CR3 = 0x00454000
DEFAULT_DUMP = ROOT / "work" / "86box" / "logs" / "ablrec.txt"
DEFAULT_EXE = ROOT / "work" / "copies" / "BUGS_PC-full-disc" / "bugs.exe"
DEFAULT_INDEX = ROOT / "static" / "exports" / "BIN-97c95ba5572dce63" / "ghidra-evidence.index.json"


@dataclass(frozen=True)
class Record:
    tsc: int
    cr3: int
    pc: int
    oldpc: int
    addr: int
    val: int
    width: int


@dataclass
class Dump:
    total: int = 0
    shown: int = 0
    dump_eip: int | None = None
    dump_cr3: int | None = None
    ranges: list[tuple[int, int]] = field(default_factory=list)
    records: list[Record] = field(default_factory=list)
    skipped: int = 0

    @property
    def truncated(self) -> bool:
        """True if the ring overwrote older records before the dump (total > shown)."""
        return self.total > self.shown


_REC_RE = re.compile(
    r"^(?P<tsc>\d+)\s+cr3=(?P<cr3>[0-9a-fA-F]+)\s+pc=(?P<pc>[0-9a-fA-F]+)\s+"
    r"oldpc=(?P<oldpc>[0-9a-fA-F]+)\s+addr=(?P<addr>[0-9a-fA-F]+)\s+"
    r"val=(?P<val>[0-9a-fA-F]+)\s+w=(?P<w>\d+)\s*$"
)
_RANGE_RE = re.compile(r"\[([0-9a-fA-F]+),\s*([0-9a-fA-F]+)\)")


def parse_dump(text: str) -> Dump:
    """Parse an ABLREC text dump (Phase 0 or Phase 1 header). Malformed record
    lines are counted in ``skipped`` rather than raising."""
    d = Dump()
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = re.search(r"total=(\d+)\s+shown=(\d+)", line)
            if m:
                d.total = int(m.group(1))
                d.shown = int(m.group(2))
                me = re.search(r"dump_eip=([0-9a-fA-F]+)", line)
                mc = re.search(r"dump_cr3=([0-9a-fA-F]+)", line)
                if me:
                    d.dump_eip = int(me.group(1), 16)
                if mc:
                    d.dump_cr3 = int(mc.group(1), 16)
            for lo, hi in _RANGE_RE.findall(line):
                d.ranges.append((int(lo, 16), int(hi, 16)))
            continue
        m = _REC_RE.match(line)
        if not m:
            d.skipped += 1
            continue
        d.records.append(
            Record(
                tsc=int(m.group("tsc")),
                cr3=int(m.group("cr3"), 16),
                pc=int(m.group("pc"), 16),
                oldpc=int(m.group("oldpc"), 16),
                addr=int(m.group("addr"), 16),
                val=int(m.group("val"), 16),
                width=int(m.group("w")),
            )
        )
    return d


def load_dump(path: Path) -> Dump:
    return parse_dump(Path(path).read_text())


def _cr3_ok(r: Record, cr3: int | None) -> bool:
    return cr3 is None or r.cr3 == cr3


def _overlaps(r: Record, lo: int, hi: int) -> bool:
    return r.addr < hi and (r.addr + r.width) > lo


def who_wrote(dump: Dump, addr: int, qwidth: int = 1, cr3: int | None = GAME_CR3) -> dict[int, list[Record]]:
    """Records whose written bytes overlap ``[addr, addr+qwidth)``, grouped by writer EIP."""
    lo, hi = addr, addr + qwidth
    by_writer: dict[int, list[Record]] = {}
    for r in dump.records:
        if _cr3_ok(r, cr3) and _overlaps(r, lo, hi):
            by_writer.setdefault(r.oldpc, []).append(r)
    return by_writer


def timeline(dump: Dump, addr: int, cr3: int | None = GAME_CR3) -> list[tuple[Record, int | None]]:
    """Exact-``addr`` records in ``tsc`` order as (record, old_value_or_None)."""
    recs = sorted((r for r in dump.records if _cr3_ok(r, cr3) and r.addr == addr), key=lambda r: r.tsc)
    out: list[tuple[Record, int | None]] = []
    prev: int | None = None
    for r in recs:
        out.append((r, prev))
        prev = r.val
    return out


def writers(dump: Dump, cr3: int | None = GAME_CR3) -> dict[int, dict]:
    """Writer census: writer EIP -> {count, addrs, widths}."""
    m: dict[int, dict] = {}
    for r in dump.records:
        if not _cr3_ok(r, cr3):
            continue
        e = m.setdefault(r.oldpc, {"count": 0, "addrs": set(), "widths": set()})
        e["count"] += 1
        e["addrs"].add(r.addr)
        e["widths"].add(r.width)
    return m


def cr3_split(dump: Dump) -> dict[int, int]:
    c: dict[int, int] = {}
    for r in dump.records:
        c[r.cr3] = c.get(r.cr3, 0) + 1
    return c


# ---- live enrichment (needs the Ghidra export index and objdump + exe) ----

def load_functions(index_path: Path = DEFAULT_INDEX) -> list[tuple[int, str]]:
    p = Path(index_path)
    if not p.exists():
        # The index is a regenerable cache (git-ignored). Ask ghidra-query to
        # build it from the tracked export; best-effort — return [] if unavailable.
        gq = ROOT / "scripts" / "ghidra-query.py"
        try:
            subprocess.run([sys.executable, str(gq), "index"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return []
        if not p.exists():
            return []
    idx = json.loads(p.read_text())
    funcs = idx.get("functions", {})
    return sorted((int(a, 16), meta.get("name", "?")) for a, meta in funcs.items())


def containing_function(func_list: list[tuple[int, str]], eip: int) -> tuple[int, str] | None:
    """Nearest function entry <= eip (approximate: the export has no sizes)."""
    keys = [e for e, _ in func_list]
    i = bisect.bisect_right(keys, eip) - 1
    if i < 0:
        return None
    return func_list[i]


def extract_disasm(objdump_text: str, eip: int) -> str | None:
    """Pure: pull the mnemonic for `eip` out of objdump -d output."""
    prefix = f"{eip:x}:"
    for line in objdump_text.splitlines():
        s = line.strip()
        if s.startswith(prefix):
            parts = line.split("\t")
            if len(parts) >= 3:
                return parts[2].strip()
            return s[len(prefix):].strip() or None
    return None


def disasm_at(exe_path: Path, eip: int) -> str | None:
    try:
        out = subprocess.run(
            ["objdump", "-d", "-M", "intel",
             f"--start-address={eip:#x}", f"--stop-address={eip + 16:#x}", str(exe_path)],
            capture_output=True, text=True, check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return extract_disasm(out, eip)


def resolve(eips: list[int], exe: Path = DEFAULT_EXE, index: Path = DEFAULT_INDEX) -> dict[int, dict]:
    # load_functions self-heals a missing (git-ignored) index via ghidra-query and
    # returns [] if unavailable, so call it unconditionally rather than gating on
    # the index existing (which would make the self-heal dead code).
    func_list = load_functions(index)
    have_exe = Path(exe).exists()
    out: dict[int, dict] = {}
    for eip in eips:
        fn = containing_function(func_list, eip) if func_list else None
        out[eip] = {
            "func_entry": fn[0] if fn else None,
            "func_name": fn[1] if fn else None,
            "disasm": disasm_at(exe, eip) if have_exe else None,
        }
    return out


# ---- CLI ----

def _parse_cr3(s: str) -> int | None:
    if s.lower() == "all":
        return None
    if s.lower() == "game":
        return GAME_CR3
    return int(s, 16)


def _hex(v: int, width: int = 8) -> str:
    return f"{v:0{width}x}"


def _fmt_writer_line(eip: int, res: dict | None) -> str:
    if not res:
        return f"0x{_hex(eip)}"
    fn = ""
    if res.get("func_entry") is not None:
        fn = f"  in ~0x{_hex(res['func_entry'])} {res.get('func_name') or ''}".rstrip()
    dis = f"  [{res['disasm']}]" if res.get("disasm") else ""
    return f"0x{_hex(eip)}{fn}{dis}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Analyze an ABLREC flight-recorder dump.")
    ap.add_argument("--dump", type=Path, default=DEFAULT_DUMP, help="dump file (default work/86box/logs/ablrec.txt)")
    ap.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    ap.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("who-wrote", help="writers of an address")
    p.add_argument("addr")
    p.add_argument("--width", type=int, default=1, help="query width in bytes (default 1)")
    p.add_argument("--cr3", default="game")
    p.add_argument("--name", action="store_true", help="resolve writer EIP -> function + disasm")

    p = sub.add_parser("timeline", help="value history of an exact address")
    p.add_argument("addr")
    p.add_argument("--cr3", default="game")

    p = sub.add_parser("writers", help="writer census")
    p.add_argument("--cr3", default="game")
    p.add_argument("--name", action="store_true")

    sub.add_parser("cr3-split", help="record counts per CR3")

    p = sub.add_parser("name", help="resolve EIPs to function + disasm")
    p.add_argument("eips", nargs="+")

    args = ap.parse_args(argv)
    if not Path(args.dump).exists() and args.cmd != "name":
        print(f"error: dump not found: {args.dump}", file=sys.stderr)
        return 2

    if args.cmd == "name":
        eips = [int(e, 16) for e in args.eips]
        res = resolve(eips, args.exe, args.index)
        for eip in eips:
            print(_fmt_writer_line(eip, res[eip]))
        return 0

    dump = load_dump(args.dump)
    if dump.truncated:
        print(f"# NOTE: trace truncated — {dump.total} writes occurred, {dump.shown} retained "
              f"(older records overwritten). Results cover the retained window only.")

    if args.cmd == "cr3-split":
        for cr3, n in sorted(cr3_split(dump).items(), key=lambda kv: -kv[1]):
            tag = " (ABL game)" if cr3 == GAME_CR3 else (" (boot/real-mode)" if cr3 == 0 else "")
            print(f"cr3=0x{_hex(cr3)}  {n} records{tag}")
        return 0

    cr3 = _parse_cr3(args.cr3)

    if args.cmd == "who-wrote":
        addr = int(args.addr, 16)
        groups = who_wrote(dump, addr, args.width, cr3)
        if not groups:
            print(f"no writers of [0x{_hex(addr)},0x{_hex(addr + args.width)}) "
                  f"(cr3={'all' if cr3 is None else '0x' + _hex(cr3)})")
            return 0
        res = resolve(sorted(groups), args.exe, args.index) if args.name else {}
        print(f"writers of [0x{_hex(addr)},0x{_hex(addr + args.width)}) "
              f"(cr3={'all' if cr3 is None else '0x' + _hex(cr3)}):")
        for eip in sorted(groups, key=lambda e: -len(groups[e])):
            recs = groups[eip]
            vals = sorted({r.val for r in recs})
            vpreview = ", ".join(f"0x{_hex(v)}" for v in vals[:4]) + (" …" if len(vals) > 4 else "")
            print(f"  {_fmt_writer_line(eip, res.get(eip))}  x{len(recs)}  vals[{vpreview}]")
        return 0

    if args.cmd == "timeline":
        addr = int(args.addr, 16)
        tl = timeline(dump, addr, cr3)
        if not tl:
            print(f"no writes to 0x{_hex(addr)} (cr3={'all' if cr3 is None else '0x' + _hex(cr3)})")
            return 0
        print(f"timeline of 0x{_hex(addr)} ({len(tl)} writes, cr3={'all' if cr3 is None else '0x' + _hex(cr3)}):")
        for r, old in tl:
            olds = "?" if old is None else f"0x{_hex(old)}"
            print(f"  tsc={r.tsc}  writer=0x{_hex(r.oldpc)}  {olds} -> 0x{_hex(r.val)}  (w={r.width})")
        return 0

    if args.cmd == "writers":
        cen = writers(dump, cr3)
        res = resolve(sorted(cen), args.exe, args.index) if args.name else {}
        print(f"writer census (cr3={'all' if cr3 is None else '0x' + _hex(cr3)}): {len(cen)} writers")
        for eip in sorted(cen, key=lambda e: -cen[e]["count"]):
            e = cen[eip]
            addrs = ", ".join(f"0x{_hex(a)}" for a in sorted(e["addrs"])[:6]) + (" …" if len(e["addrs"]) > 6 else "")
            print(f"  {_fmt_writer_line(eip, res.get(eip))}  x{e['count']}  w={sorted(e['widths'])}  addrs[{addrs}]")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
