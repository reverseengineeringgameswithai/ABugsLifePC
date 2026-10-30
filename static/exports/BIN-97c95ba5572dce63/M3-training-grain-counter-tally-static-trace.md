# M3 Training grain counter and tally static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Accepted patched binary SHA-256:
`8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`

## Pickup counter transition

`0x00417720` contains the Training selector-`0x14` pickup path established in
`EXP-20260814-111`:

- `0x00417D7B–0x00417D8D` increment byte counter `0x0059D9B1`;
- `0x00417DC2` compares the post-increment value with literal `0x32`;
- the equality path reaches `0x00417DCF` when the transition is `49 -> 50`;
- the non-equality target is `0x00417E92`, reached by `50 -> 51`.

The exact-50 path is therefore a one-shot event at 50, not a saturating write.
The two controlled transitions in `EXP-20260814-112` independently confirm
both branch outcomes and retained counter value 51.

## In-level HUD

`0x00416890` reads the same byte counter and renders two decimal digits:

- `0x00416BB7` reads `0x0059D9B1`;
- `0x00416BC2` compares it with 49 only to select the animation phase used by
  higher values;
- `0x00416BEA` and `0x00416C02` draw the cached tens and ones digits;
- `0x00416C2C` reads the counter for division and remainder by 10.

At retained count 51, the live digit cache at `0x00599ABE` is `0x0105`:
bytes `(5,1)`. The HUD therefore already supports and displays 51; no HUD byte
requires modification.

## End-of-level tally

`0x00442E70` contains a separate tally and completion path:

- `0x00442ECA` compares the retained counter with literal 50;
- `0x00442ECE` replaces values above 50 with literal 50;
- `0x00442F01` compares the retained/tally value with 50;
- intervening `MOV` instructions preserve those flags;
- original `0x00442F27 JNE` awards the completion state only when the value is
  exactly 50;
- the displayed numerator is divided by 10 and can render 51;
- the displayed denominator remains a literal `/50`;
- `0x004432C1` compares the animated value with 50 and, when the completion
  state is set, `0x004432EF` reaches the bright completion/emblem sprite path;
- `0x00443442` contains the exact-50 tally sound/event comparison, while the
  animation can continue to 51.

The smallest patch that retains 51 and preserves the original at-least-50
completion milestone changes exactly three bytes:

| File offset | VA | Original | Replacement | Effect |
|---:|---:|---:|---:|---|
| `0x422CB` | `0x00442ECB` | `0x32` | `0x33` | raise tally upper comparison to 51 |
| `0x422CF` | `0x00442ECF` | `0x32` | `0x33` | raise tally clamped value to 51 |
| `0x42327` | `0x00442F27` | `0x75` (`JNE`) | `0x72` (`JB`) | accept retained count >= 50 |

The third edit interprets the flags from the preceding unsigned byte compare:
counts below 50 branch away, while 50 and 51 preserve the completion path.
The patch intentionally leaves the original 50 event, `/50` denominator, and
completion/emblem rendering path intact.

## Rejected candidate and corrected inference

A preliminary candidate also changed the literal loaded at `0x00439F05` from
50 to 51. That edit is rejected. In a 30-second watch window following the
controlled Training `49 -> 50` transition, execution did not reach the
counter write at `0x0043A0EB`. Restoring the original byte still retained and
displayed 51 and completed the final tally. The function contains a static
cap, but its identity and applicability to Training are unconfirmed.

The preliminary tally patch also retained original `JNE` at `0x00442F27`, so
count 51 failed to set the completion state. The accepted three-byte recipe
is discriminated by the runtime completion flag and bright path, not merely by
an output hash.
