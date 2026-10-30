---
type: experiment
id: EXP-20261018-008
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of all of retail bugs.exe's .text, with Direct3D constants and Wine's device defaults read from Wine's source (SRC-WINE-SOURCE); no game launch
question: Does the game set any depth (Z) render state, or do its results sprites stack by Direct3D's default depth test (EXP-20260930-001)?
result: No SetRenderState call in the executable touches ZENABLE, ZWRITEENABLE or ZFUNC. All 24 calls pass constant states, in four places (renderer init, the texture filter/address setter and the two batch functions), and none is 7, 14 or 23. The depth test therefore stays at the device's default, which Wine sets to Z on, writes on, LESSEQUAL. That is the rule EXP-20260930-001 inferred for tpage 51
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260930-001, EXP-20260907-001]
tags: [experiment/static, re/rendering]
---

# EXP-20261018-008 - Direct3D render states and the depth rule

## Question

EXP-20260930-001 saw tpage 51 draw above
every other results sprite. It inferred, without tracing, that this follows
Direct3D's default LESSEQUAL depth test because "`00420C80` sets no Z
state". The open item is under
[[Known Unknowns#Engine questions from derived test builds]], and section 7
of [[Next Tasks]] listed it as "the depth state in `00420C80`".

## Method

- **Interface.** The renderer draws through `IDirect3DDevice2`
  (EXP-20260907-001,
  `M2-direct3d-renderer-path-reconciliation.md`). Its `SetRenderState` is
  vtable slot 23, `+0x5C`.
- **Scan.** Every `call dword ptr [reg + 0x5C]` was listed with the
  arguments pushed before it: device, state, value. A raw byte scan of all of
  `.text` for each encoding of that call (`FF 50..57 5C` and the disp32
  forms) finds the same 27 sites. The first linear disassembly stopped at
  `0x004269AB`, so the byte scan is what makes the census complete.
- **Constants.** The state and value numbers are checked against Wine's
  `d3dtypes.h`. ZENABLE is 7, ZWRITEENABLE 14, ZFUNC 23
  ([[External Source Registry#SRC-WINE-SOURCE]]).

## Results

27 calls go through `+0x5C`.

- **The 24 SetRenderState calls** all push a constant state:

  | Function | Calls | States (value) |
  |---|---:|---|
  | `0x00420C80` renderer init | 13 | CULLMODE (NONE), COLORKEYENABLE (1), ALPHABLENDENABLE (1), SRCBLEND (BOTHSRCALPHA), TEXTUREADDRESS (CLAMP), TEXTUREMAG and TEXTUREMIN (NEAREST), ALPHATESTENABLE (1, twice), SUBPIXELX (1), TEXTUREMAPBLEND (MODULATE), ALPHAREF (`0x1000`), ALPHAFUNC (GREATEREQUAL) |
  | `0x00404410` | 9 | TEXTUREADDRESSU/V (WRAP or CLAMP), TEXTUREMAG/MIN (LINEAR or NEAREST), TEXTUREHANDLE |
  | `0x004056A0`, `0x004058D0` (the two batch functions) | 2 | TEXTUREHANDLE |

  Together that is 15 distinct states. None is ZENABLE, ZWRITEENABLE or
  ZFUNC.
- **The other three** (`0x0041F296`, `0x0042034C`, `0x00420397`) pass four
  pointers, not a state. That is a different interface's slot 23, the shape
  of `IDirectDraw2::GetAvailableVidMem`.
- **No other route.** The executable creates a Z-buffer
  (`d3dappi.lpZBuffer`, attached to the back buffer), and has no
  execute-buffer path. Its "EXECUTE" strings are only the D3D error-name
  table.

## The default

Wine's `init_default_render_states` sets, unconditionally:

- `rs[WINED3D_RS_ZENABLE] = WINED3D_ZB_TRUE;`
- `rs[WINED3D_RS_ZWRITEENABLE] = TRUE;`
- `rs[WINED3D_RS_ZFUNC] = WINED3D_CMP_LESSEQUAL;`

These are Wine master's lines. The installed Wine 11 is assumed, not
checked, to match.

## Confirmed, inferred, unknown

- **Confirmed (static, the whole image).** The game never sets a Z render
  state through `SetRenderState`.
- **Confirmed (Wine source).** Wine's default is depth testing on, writes
  on, LESSEQUAL.
- **Inferred.**
  - Under Wine the results sprites therefore stack by LESSEQUAL with depth
    writes, as EXP-20260930-001 inferred. Its hardware captures are the
    runtime form.
  - Under a Windows Direct3D runtime the defaults come from that runtime and
    were not checked.
- **Unknown.** Whether Wine's ddraw layer changes ZENABLE when it attaches
  the depth buffer (`d3d_device_update_depth_stencil` was not read). It is
  irrelevant while a Z-buffer is attached, as here.

## Consequences

The "depth rule" item is closed at the static boundary. For results and HUD
sprites, stacking follows from each quad's depth value and the draw order
(the tpage order of the flush `0x00405EF0`) under LESSEQUAL; no render-state
call intervenes.
