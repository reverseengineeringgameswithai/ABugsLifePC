# PC plant `.ANM` first-level metadata

Generated from the user-owned derived work copy with:

```bash
./scripts/ablpc-mod scan-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS --json
```

Scope: metadata produced by the bounded PC consumer walk at executable
`0x00444B70`. This report contains paths, hashes, sizes, counts, and offsets;
it contains no game-file payload bytes.

| File | SHA-256 | Size | Count | Relative offsets | First nested count | `-2` indices |
|---|---|---:|---:|---|---:|---|
| `PLANT01.ANM` | `f7a9c40be4557d13cdceb908687fcc6d40d240c31e961cec121344be02344e98` | 4502 | 3 | `0x14, 0x680, 0xAD0` | 5 | none |
| `PLANT02.ANM` | `07fbbc07d6db6958b8fbc017f7ba19d628c3ac1249739898a0c5ffd3ecf0af43` | 3344 | 4 | `0x18, 0x3F8, 0x550, 0x930` | 3 | none |
| `PLANT03.ANM` | `bf0160153942f711f6147d176c3bb38c3a8bde3f902a43ce512be976bf1ed2f0` | 5072 | 3 | `0x14, 0x834, 0xC1C` | 7 | `6` |
| `PLANT04.ANM` | `32dce9588272d4bd4d0b2054e58de2b9ca5ae563826d56f7cd12abe8b001e7ce` | 1802 | 3 | `0x14, 0x2AE, 0x470` | 2 | none |
| `PLANT05.ANM` | `d474fe3c374ce47389eb82076909007592d93718689bafaf3414a37bffa542b3` | 1168 | 4 | `0x18, 0x16C, 0x254, 0x3A8` | 1 | none |
| `PLANT06.ANM` | `d90a35b047c4f811ec5d7aec0aa73fb300dbea59a0a1df0dfd4dcef618bc04ec` | 5066 | 3 | `0x14, 0x6EE, 0xC18` | 6 | none |
| `PLANT07.ANM` | `4b9dd5bf3936206b660528e425ff9f55134f6d9ec907479f66b1f1e3fdaa2292` | 5880 | 4 | `0x18, 0x684, 0xA8C, 0x108C` | 5 | none |
| `PLANT08.ANM` | `23cf82a2b31fa5fc18bc81ae02d713ce55c218d28002f5d34b141d93e1ba17d1` | 3542 | 3 | `0x14, 0x53A, 0x8B0` | 4 | none |
| `PLANT09.ANM` | `252b909e592ed577297b6d713da7c2dc0d78942a7d5ee57d51ea77385c8f59fe` | 3542 | 3 | `0x14, 0x53A, 0x8B0` | 4 | none |
| `PLANT10.ANM` | `12d2550ea89b9156acd04ce403d1754aa244d1cedf8531eaca2c8e7bf22b5194` | 1802 | 3 | `0x14, 0x2AE, 0x470` | 2 | none |
| `PLANT11.ANM` | `6ba80512dafcb995de3586f14b8d0a0c9dba118ac9a164c4dab6de2e399650f4` | 3512 | 3 | `0x14, 0x680, 0xAD0` | 5 | none |

All 11 files passed. All have zero on disk at offset-named header fields
`+0x00`, `+0x04`, and `+0x06`; the caller overwrites the first two before the
consumer. Every first offset equals the end of its own offset table. These are
corpus observations rather than complete format semantics.
