# M3 Training grain static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Source Training DAT SHA-256:
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`

## Type-0x3F layout and fixup

- `0x0044BB70` installs the relocated type-`0x3F` record at global pointer
  slot `0x005C595C` and uses a 16-byte entry stride.
- In the exact source DAT, the first top record begins at file offset `0x4`,
  has type `0x3F`, count 62, and occupies `[0x4,0x3E8)`. Its first 50 entries
  have selector byte `0x14` at entry offset `+0x0C`.
- Inserting one 16-byte entry at `0x3E8` moves the remainder of the physical
  file. The same loader's known file-relative fixups require every subsequent
  primary/secondary record payload pointer, selected payload target pointer,
  optional flag-`0x20` pointer, and nonzero index-table pointer to move by
  `0x10`. The exact Training census is 556 pointer fields.

## Selector-0x14 initialization

`0x00456A90` walks the count at `0x005C595C` with a 16-byte stride:

- `0x00456AB2` loads literal selector `0x14`;
- `0x00456ACC–0x00456AD1` compare entry byte `+0x0C` with `0x14`;
- `0x00456AD3–0x00456AEA` query terrain height using the entry coordinates;
- `0x00456AF2–0x00456AF5` store the resulting signed height at entry `+0x0E`.

This establishes a distinct PC-native initialization path for selector
`0x14`; it does not by itself name the item.

## Selector-0x14 collection path

`0x00417720` walks the same pointer/count and 16-byte entries. On the active
nearby-object route:

- `0x00417991–0x0041799D` compare entry byte `+0x0C` with `0x14` and apply a
  selector-specific distance threshold;
- `0x004179C4` writes `0x80000000` to entry dword `+0x04` on the alternate
  selector-`0x14` effect route;
- the normal close-object path writes the same sentinel at `0x00417A30`, then
  dispatches on entry byte `+0x0C` at `0x00417A39–0x00417A52`;
- selector-`0x14` reaches `0x00417CCC`; after its event checks,
  `0x00417D7B–0x00417D8D` increment byte counter `0x0059D9B1`;
- `0x00417DC2–0x00417DC9` compare the new counter with literal `0x32` for an
  exact-50 event branch.

The isolated runtime result in `EXP-20260814-111` independently confirms that
the inserted selector-`0x14` record can be the only record sent to the
consumed sentinel while `0x0059D9B1` increments from zero to one.

## Counter boundary

`0x00439E90` loads literal `0x32` at `0x00439F05` and contains a write that
caps `0x0059D9B1` at `0x0043A0EB–0x0043A0F3`. At this experiment boundary,
its applicability to Training and a displayed/current counter above 50 were
not yet demonstrated.

`EXP-20260814-112` corrects the earlier Training-specific inference: a
controlled post-pickup watch did not reach this function's cap, and the
unchanged retail bytes still retained/displayed 51. The cap exists, but its
runtime identity remains unconfirmed. See
`M3-training-grain-counter-tally-static-trace.md`.
