# 86Box source patches (RE builds)

These patches modify 86Box and are distributed under 86Box's own license (GNU
GPL), not under this repository's MIT license.

Tracked source patches applied to the **v6.0 GDBSTUB** 86Box build
(tag `v6.0`, commit `4fef696a4eead1d55a28d6ac0e5bd2864e5454da`). The built
binaries are **not** committed (they live git-ignored under
`work/86box/v6/`); these `.patch` files are the reproducible source of record.

Apply inside the build container (`abl-86box-v6`, source at `/root/86Box`):

```sh
cd /root/86Box && git apply /path/to/<patch>
cd build && ninja           # incremental; produces build/src/86Box
```

Then deploy to the runtime container:

```sh
podman cp abl-86box-v6:/root/86Box/build/src/86Box work/86box/v6/86Box
```

## `86box-v6.0-ablrec.patch` — flight-recorder (Phase 0 + 1, DEC-20260818-149)

Adds an in-emulator **write-trace** over a configurable table of game globals
(Flik position `0x0059D910`, level `0x00861C84`, carousel `0x00599AF8`, NextLife
`0x0059A5B0`):

- Hooks (`ablrec_hook`) on the **byte/word/long** write accessors record
  `{tsc, cr3, pc, oldpc(=writer EIP), addr, val, width}` into a 64K circular
  buffer when the address falls in any watched range.
- To defeat 86Box's fast-write cache (`writelookup2`) — which otherwise lets
  repeated writes bypass the accessors — the hook marks each watched page in
  `gdbstub_watch_pages` on first use and `addwritelookup` is gated to never
  cache a marked page, so every write to those pages stays on the slow path.
- `SIGUSR1` to the 86Box process dumps the ring to `/vm/logs/ablrec.txt`
  (host `work/86box/logs/ablrec.txt`), with a header of dump-time regs + ranges.

Result: [[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]] — Phase 0
reliably reproduced the EXP-20260818-001 writer `0x004ab889 → 0x0059D910` without
gdb; Phase 1 generalised to all widths and the range table (one run: 1473 records
across 4 globals, incl. the level-global writer `0x0043dabb`). `cr3` in each
record separates game writes (`00454000`) from boot (`0`); old value is derived
offline. Deferred to Phase 1b: the full `dump_mark()` RAM+frame bookmark package
and qword (8-byte) writes.
