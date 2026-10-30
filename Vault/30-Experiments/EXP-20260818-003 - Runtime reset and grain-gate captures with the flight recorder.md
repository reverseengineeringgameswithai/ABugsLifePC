---
type: experiment
id: EXP-20260818-003
date: 2026-08-18
question: 'Applying the flight recorder to real questions: does Level06/Cliffside use the type-1 reset selector (KU-063)? And what are the runtime grain-gate globals in Level03/Tunnels — the grain count and gate-state flags, and who reads/writes them?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: 86Box v6.0 GDBSTUB build + ABLREC flight-recorder patch (extended watched-range table), real Win95 OSR2 + A Bug`s Life in podman abl-win95; scripts/ablrec-analyze.py for offline analysis; one authorized guest-memory write via the GDB stub
environment_version: 86Box tag v6.0 (4fef696) + tools/86box/patches/86box-v6.0-ablrec.patch (aux + grain-gate ranges added)
working_directory: /home/dev/ABLPC
configuration: Cliffside (internal level 6) natural death; Level03/Tunnels (internal level 3) natural grain collection + one authorized grain-count write to open a gate
artifacts:
  - work/86box/logs/ablrec-cliffside-reset.txt
  - work/86box/logs/ablrec-tunnels-grain.txt
  - work/86box/patches/86box-v6.0-ablrec.patch
addresses:
  - "0x0059D9B1"
  - "0x00417D8D"
  - "0x00432F0C"
  - "0x00599C68"
  - "0x00599C69"
  - "0x00599C6A"
  - "0x0042E5C0"
  - "0x0042DDF3"
  - "0x0041C8DC"
  - "0x00433807"
file_offsets: []
result: grain-count-0x0059D9B1-and-gate-flag-writers-static-confirmed + authorized-write-confirms-grain-byte; cliffside-not-type1 (KU-063, fully captured); tunnels runtime value-chains observed-live-but-evicted-by-truncation, clean re-run deferred
created: 2026-08-18T22:30:00
---

# Runtime reset and grain-gate captures with the flight recorder

First application of the flight recorder ([[Flight Recorder]],
`DEC-20260818-149`) to open RE questions. Two levels driven headlessly with the
recorder`s watched-range table extended per target.

## KU-063 — Cliffside (internal level 6) does NOT use the type-1 reset selector

Watching the Flik position + aux triple + NextLife, a **natural death/reset** in
Cliffside (trace `work/86box/logs/ablrec-cliffside-reset.txt`) shows:
- **NextLife `0 → 2`** written by `0x0041c8dc` (the reset-state producer,
  near the `0x0041C8CC` state-bit producer of EXP-116) — the "fell in a pit"
  signature from EXP-129.
- Flik`s position reset by a **direct absolute store `0x0042ddf3`**
  (`FUN_0042ddb0`, `mov ds:0x59d910,ecx`) — not the per-frame updater.
- **No writer anywhere in the type-1 selector region `0x004328xx–0x004338xx`.**

So Cliffside resets via `FUN_0042ddb0`, **not** the type-1 selector `0x00432930`.
This is a `KU-063` datapoint: type-1 reset is not universal; it is confirmed for
Level03/Tunnels (EXP-129/131) but Cliffside uses a different reset path. (This
also means Cliffside cannot answer `KU-062`, which is specific to the type-1
query — that needs Level03, where provoking the natural pit-fall headlessly
remained the blocker.)

## Level03/Tunnels grain-gate globals

Level is Tunnels (carousel selection + cave environment in the run screenshots).
**Evidence sourcing (important):** the committed trace
`work/86box/logs/ablrec-tunnels-grain.txt` is the **final dump and is TRUNCATED**
(`total=153693 shown=65536`; the analyzer flags it). It retains only the *tail*
(post-authorized-write). The **load-time and early-collection writes below were
observed live in an earlier dump that `SIGUSR1` overwrote, and are NOT in the
committed trace** — so their *writer/reader identities* are cited to **static
disasm** (independently objdump-verified), and the *runtime value observations*
are flagged as live-but-not-in-committed-dump. A narrow-range re-run (see
Limitation) would capture them cleanly.

- **Grain count = `0x0059D9B1`** (byte) — the grain byte the gates check.
  **Confirmed (committed):** static disasm shows the grain-gate loop **reads** it
  at `0x00432f0c` (`8a 0d b1 d9 59 00  mov cl,BYTE PTR ds:0x59d9b1`, then `cmp
  ecx,eax`, then reads Flik`s position `0x0059D910/18`), comparing to a per-gate
  threshold from `0x004DA9D0[gate*4]`; and the **authorized write** (below) writing
  this exact byte to 10 made the HUD read 10 and opened the gate — so `0x0059D9B1`
  is the operative grain count. The **collection writer is `0x00417d8d`**
  (`FUN_00417720`, `88 15 b1 d9 59 00  mov BYTE PTR ds:0x59d9b1,dl` — static).
  **Observed live (not in committed dump):** it incremented `0→1→2→3→4` in step
  with the HUD during collection, and is zeroed at load by `0x0043e6ee`.
  (Matches the M5.7 resolver [[EXP-20260816-170 - M5.7 grain-gate opening resolver]]
  and EXP-111`s Training counter `0x0059D9B1`.)
- **Gate-state flags `0x00599C68/69/6A`** (bytes). **Confirmed (static):**
  `FUN_0042e5c0` writes them at `0x0042e838/83e/844`
  (`mov ds:0x599c68/69/6a,bl` — a register `bl`, not an immediate). `0x00599C69`
  is the M5.7/KU-067 byte, and static disasm confirms the gate-open path writes it
  at `0x00433807` (`c6 05 69 9c 59 00 01  mov BYTE PTR ds:0x599c69,0x1`).
  **Observed live (not in committed dump):** the three flags were 0 after load
  (so `bl` was 0 there). The `=0` value is a live observation, not static.
- **Level index = 3 (Tunnels).** Observed live (`0x0041014b` writes
  `0x00861C84 = 3`, the level-index writer also seen in
  [[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]]); **not in the
  committed truncated trace.**
- **`0x00599C60` is NOT gate state** — a busy object-pointer slot (values
  `0x0081B4xx`, written by **18** distinct EIPs in the retained window). Do not
  treat the low bytes of that word as gate flags. (This pointer plus the counter
  at `0x0059D9B5` — **5,041** writes in the retained window alone — are what
  flooded the ring.)

## Authorized guest-memory write (receipt)

To exercise the gate-open path, one **explicitly user-authorized** compare-before-
write (reproducing EXP-129`s "grain 1→10 lowers the first gate"): via the GDB
stub, with `$pc` in game code and `CR3 = 0x00454000`, the grain byte was
read-verified then written:

```
RECEIPT: wrote grain@0x59d9b1  4 -> 10  cr3=00454000 pc=00481f93  OK
```

The HUD then showed grain = 10 and the gate mechanism responded.

## Limitation — the committed Tunnels trace is truncated, evicting all load-time writes

The watched ranges were too broad — the busy `0x00599C60` pointer (**18,730**
writes) and the `0x0059D9B5` counter (**5,041** writes) flooded the 64K ring, so
the analyzer correctly reported the committed trace **truncated** (153,693 writes,
65,536 retained — only the post-write tail, tsc ~117.8e9→167.1e9). This evicted
**every load-time / early write** from the committed artifact: the grain chain
`0→…→4`, the level-index write, and the gate-flag inits (all observed live in an
earlier, overwritten dump), **and** the gate-open write `0x00433807 → 0x00599C69`
(which likely also did not fire — Flik may have passed down the main tunnel rather
than into the gate`s trigger passage). Those identities are static-confirmed above;
their runtime capture is the follow-up.

**Clean re-run to close this:** narrow the watched ranges to just the flags
(`0x00599C68`–`0x00599C6C`) and the grain count (`0x0059D9B1`) — dropping the
`0x00599C60` pointer and the `0x0059D9B5` counter — and position Flik in the gate
passage before the authorized write. With no flooding the ring will retain the
load-time writes and the gate-open write, giving a committed trace that actually
contains the grain chain, level index, gate-flag inits, and `0x00433807`.

## Links

- [[Flight Recorder]], `DEC-20260818-149`,
  [[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]],
  [[EXP-20260816-170 - M5.7 grain-gate opening resolver]], `KU-062`, `KU-063`,
  `KU-067`, EXP-129 (`[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]]`).
